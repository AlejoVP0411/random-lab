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


@app.middleware("http")
async def restore_api_path_after_vercel_rewrite(request, call_next):
    """Remove the Vercel function path before FastAPI matches application routes."""
    function_path = "/api/index.py"
    path = request.scope["path"]
    if path == function_path or path.startswith(f"{function_path}/"):
        restored_path = path.removeprefix(function_path) or "/"
        request.scope["path"] = restored_path
        request.scope["raw_path"] = restored_path.encode()
    return await call_next(request)


# Static files in public/ own the frontend; this router owns every /api endpoint.
app.include_router(random_lab_api.router, prefix="/api")


@app.get("/")
@app.get("/api")
def root():
    return {"status": "ok", "message": "Random Lab API is running"}
