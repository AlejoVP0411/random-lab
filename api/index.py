"""Vercel serverless entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.main import app as random_lab_api

app = FastAPI(title="Random Lab API", docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The FastAPI function receives dynamic paths directly. Static files in public/
# take precedence on Vercel, while this router owns every /api endpoint.
app.include_router(random_lab_api.router, prefix="/api")


@app.get("/")
@app.get("/api")
def root():
    return {"status": "ok", "message": "Random Lab API is running"}
