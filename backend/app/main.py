from fastapi import FastAPI
from app.schemas.platform import PlatformInfo, RuntimeInfo, PlatformStatus
app = FastAPI(
    title="PlantMind API",
    description="Enterprise Operational Intelligence Platform",
    version="1.0.0"
)

@app.get("/", response_model=PlatformStatus)
def root():
    return PlatformStatus(
        platform=PlatformInfo(
            name="PlantMind",
            edition="Enterprise",
            deployment="On-Premise",
            version="1.0.0",
        ),
        runtime=RuntimeInfo(
            status="Running",
            environment="Development",
        ),
    )
    

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
