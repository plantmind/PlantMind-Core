from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.core.bootstrap import BootstrapManager
from app.schemas.platform import (
    PlatformInfo,
    PlatformStatus,
    RuntimeInfo,
)


bootstrap = BootstrapManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    PlantMind platform lifecycle.
    """

    bootstrap.initialize()

    yield

    # Shutdown lifecycle will be introduced
    # during the Composition Root implementation.


app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise Operational Intelligence Platform",
    version=settings.VERSION,
    lifespan=lifespan,
)


@app.get("/", response_model=PlatformStatus)
def root() -> PlatformStatus:
    return PlatformStatus(
        platform=PlatformInfo(
            name=settings.APP_NAME,
            edition="Enterprise",
            deployment=settings.DEPLOYMENT_MODE,
            version=settings.VERSION,
        ),
        runtime=RuntimeInfo(
            status="Running",
            environment=settings.ENVIRONMENT,
        ),
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }