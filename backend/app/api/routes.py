from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "application": "PlantMind",
        "version": "1.0.0",
        "status": "Running"
    }


@router.get("/health")
def health():
    return {
        "status": "Healthy"
    }
