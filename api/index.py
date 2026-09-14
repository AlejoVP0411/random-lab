"""Vercel serverless entrypoint.

The root app mounts the FastAPI backend at /api so the production frontend and
API share a single origin.
"""

from fastapi import FastAPI

from backend.app.main import app as random_lab_api

app = FastAPI(title="Random Lab")
app.mount("/api", random_lab_api)
