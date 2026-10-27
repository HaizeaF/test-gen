"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Report basic service health for uptime checks."""
    return {"status": "ok"}
