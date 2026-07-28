from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.bootstrap import BootstrapManager
from app.schemas.platform import PlatformInfo, RuntimeInfo, PlatformStatus


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    PlantMind platform startup lifecycle.
    """

    bootstrap = BootstrapManager()
    bootstrap.initialize()

    yield

    # Reserved for future platform shutdown lifecycle.


app = FastAPI(
    title="PlantMind API",
    description="Enterprise Operational Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan,
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