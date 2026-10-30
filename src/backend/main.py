"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.config.config import Config
from src.backend.routes import health, questions, sections, topics
from src.backend.routes.errors import register_error_handlers

app = FastAPI(title="TestGen API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
register_error_handlers(app)

for router in (health.router, questions.router, sections.router, topics.router):
    app.include_router(router)
