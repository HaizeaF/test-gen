"""FastAPI application entry point."""

from fastapi import FastAPI

from src.backend.routes import health

app = FastAPI(title="TestGen API", version="0.1.0")
app.include_router(health.router)
