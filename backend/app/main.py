from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.request_admission import RequestAdmissionMiddleware
from app.config import settings
from app.core.composition import CompositionRoot
from app.schemas.platform import (
    PlatformInfo,
    PlatformStatus,
    RuntimeInfo,
)


platform = CompositionRoot.build()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    PlantMind platform lifecycle.
    """

    platform.bootstrap.startup()

    yield

    platform.bootstrap.shutdown()


app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise Operational Intelligence Platform",
    version=settings.VERSION,
    lifespan=lifespan,
)


app.add_middleware(
    RequestAdmissionMiddleware,
    runtime=platform.runtime,
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
            status=platform.runtime.state.value,
            environment=platform.runtime.environment,
        ),
    )


@app.get("/health")
def health():
    return platform.health.get_status()