from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, model_validator

from .generators.middle_product import MiddleProductConfig, generate as generate_middle_product
from .generators.multiplicative import MultiplicativeConfig, generate as generate_multiplicative
from .tests import poker, runs

app = FastAPI(title="Random Lab API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    method: Literal["multiplicative", "middle_product"]
    count: int = Field(default=100, ge=1, le=10_000)
    seed: int | None = None
    multiplier: int | None = None
    modulus: int | None = None
    seed_a: int | None = None
    seed_b: int | None = None
    digits: int | None = None


class TestRequest(BaseModel):
    test: Literal["poker", "runs"]
    values: list[float] = Field(min_length=2, max_length=10_000)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
def generate(request: GenerateRequest):
    try:
        if request.method == "multiplicative":
            if None in (request.seed, request.multiplier, request.modulus):
                raise ValueError("Semilla, multiplicador y módulo son obligatorios.")
            values = generate_multiplicative(MultiplicativeConfig(request.seed, request.multiplier, request.modulus, request.count))
        else:
            if None in (request.seed_a, request.seed_b, request.digits):
                raise ValueError("Las dos semillas y la cantidad de dígitos son obligatorias.")
            values = generate_middle_product(MiddleProductConfig(request.seed_a, request.seed_b, request.digits, request.count))
        return {"values": values, "count": len(values), "method": request.method}
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.post("/test")
def test(request: TestRequest):
    if any(value < 0 or value >= 1 for value in request.values):
        raise HTTPException(status_code=422, detail="Los valores deben estar en el intervalo [0, 1).")
    try:
        return poker.run(request.values) if request.test == "poker" else runs.run(request.values)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
