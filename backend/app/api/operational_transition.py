from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict

from app.domain.observation import Observation, ObservationType
from app.services.operational_transition_application_service import (
    OperationalTransitionApplicationService,
)


class OperationalTransitionObservationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    observation_type: ObservationType
    value: str
    observed_at: datetime


class OperationalTransitionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    observations: tuple[OperationalTransitionObservationRequest, ...]


def create_router(
    service: OperationalTransitionApplicationService,
) -> APIRouter:
    router = APIRouter()

    @router.post(
        "/operational-transition",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    def request_operational(
        request: OperationalTransitionRequest,
    ) -> Response:
        try:
            observations = tuple(
                Observation(
                    source=item.source,
                    observation_type=item.observation_type,
                    value=item.value,
                    observed_at=item.observed_at,
                )
                for item in request.observations
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=str(exc),
            ) from exc

        service.request_operational(observations)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
