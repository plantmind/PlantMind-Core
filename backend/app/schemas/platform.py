"""
PlantMind Platform Schemas
"""

from pydantic import BaseModel


class PlatformInfo(BaseModel):
    """
    Platform identity information.
    """

    name: str
    edition: str
    deployment: str
    version: str


class RuntimeInfo(BaseModel):
    """
    Runtime information.
    """

    status: str
    environment: str


class PlatformStatus(BaseModel):
    """
    Root response returned by the PlantMind API.
    """

    platform: PlatformInfo
    runtime: RuntimeInfo


class RuntimeStatus(BaseModel):
    """
    Runtime capability status.
    """

    platform: str
    version: str
    environment: str
    deployment: str
    ready: bool