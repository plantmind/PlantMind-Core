"""
PlantMind API Request Admission

Enforces Runtime-owned request admission at the API hosting boundary.
"""

from __future__ import annotations

from collections.abc import Iterable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from app.core.runtime import Runtime


DEFAULT_ADMISSION_EXEMPT_PATHS: tuple[str, ...] = (
    "/",
    "/health",
)


class RequestAdmissionMiddleware(BaseHTTPMiddleware):
    """Enforce Runtime-owned admission for operational requests."""

    def __init__(
        self,
        app,
        *,
        runtime: Runtime,
        exempt_paths: Iterable[str] = DEFAULT_ADMISSION_EXEMPT_PATHS,
    ) -> None:
        super().__init__(app)
        self.runtime = runtime
        self.exempt_paths = frozenset(exempt_paths)

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        """Allow observations and reject closed operational admission."""

        if request.url.path in self.exempt_paths:
            return await call_next(request)

        if not self.runtime.is_request_admission_enabled:
            return JSONResponse(
                status_code=503,
                content={
                    "detail": (
                        "PlantMind is not accepting operational requests."
                    )
                },
            )

        return await call_next(request)
