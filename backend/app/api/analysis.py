"""PlantMind Analysis API."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.get("/health")
def health() -> dict[str, str]:
    """
    Health endpoint for the Analysis API.
    """
    return {
        "status": "ok",
        "service": "PlantMind Analysis API",
    }