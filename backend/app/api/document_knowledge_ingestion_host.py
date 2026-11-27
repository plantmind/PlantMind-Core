"""Explicit opt-in HTTP host for a caller-built PlantMind platform (AD-069)."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.document_knowledge_ingestion import (
    create_router as create_document_knowledge_ingestion_router,
)
from app.api.document_preparation import (
    create_router as create_document_preparation_router,
)
from app.api.operational_transition import (
    create_router as create_operational_transition_router,
)
from app.api.request_admission import RequestAdmissionMiddleware
from app.config import settings
from app.core.composition import PlatformComposition
from app.schemas.platform import PlatformInfo, PlatformStatus, RuntimeInfo
from app.services.document_content_establishment_application_service import (
    DocumentContentEstablishmentApplicationService,
)
from app.services.enterprise_document_registration_application_service import (
    EnterpriseDocumentRegistrationApplicationService,
)


def create_app(
    *,
    platform: PlatformComposition,
    document_registration_service: EnterpriseDocumentRegistrationApplicationService | None = None,
    document_content_establishment_service: DocumentContentEstablishmentApplicationService | None = None,
) -> FastAPI:
    """Host this platform; the caller dedicates it to one active lifespan."""
    if not isinstance(platform, PlatformComposition):
        raise TypeError("platform must be a PlatformComposition.")

    if (
        (document_registration_service is None)
        != (document_content_establishment_service is None)
        or (
            document_registration_service is not None
            and not isinstance(
                document_registration_service,
                EnterpriseDocumentRegistrationApplicationService,
            )
        )
        or (
            document_content_establishment_service is not None
            and not isinstance(
                document_content_establishment_service,
                DocumentContentEstablishmentApplicationService,
            )
        )
    ):
        raise TypeError("Both preparation services must be supplied together as canonical instances.")

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        platform.bootstrap.startup()
        try:
            yield
        finally:
            platform.bootstrap.shutdown()

    app = FastAPI(
        title=settings.APP_NAME,
        description="Enterprise Operational Intelligence Platform",
        version=settings.VERSION,
        lifespan=lifespan,
    )
    app.add_middleware(RequestAdmissionMiddleware, runtime=platform.runtime)
    app.include_router(
        create_operational_transition_router(
            platform.operational_transition_application_service
        )
    )
    app.include_router(
        create_document_knowledge_ingestion_router(
            facade=platform.application_facade,
            runtime=platform.runtime,
        )
    )

    if document_registration_service is not None:
        app.include_router(
            create_document_preparation_router(
                document_registration_service=document_registration_service,
                document_content_establishment_service=document_content_establishment_service,
                runtime=platform.runtime,
            )
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

    return app
