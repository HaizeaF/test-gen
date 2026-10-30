"""Translate the errors raised by the services into HTTP responses."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.backend.services.errors import ConflictError, NotFoundError

def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    def not_found(_: Request, error: NotFoundError) -> JSONResponse:
        return JSONResponse({"detail": str(error)}, status_code=status.HTTP_404_NOT_FOUND)

    @app.exception_handler(ConflictError)
    def conflict(_: Request, error: ConflictError) -> JSONResponse:
        return JSONResponse({"detail": str(error)}, status_code=status.HTTP_409_CONFLICT)