from pydantic import BaseModel


class PlatformInfo(BaseModel):
    """
    PlantMind Platform Identity
    """

    name: str
    edition: str
    deployment: str
    version: str


class RuntimeInfo(BaseModel):
    """
    Current runtime status
    """

    status: str
    environment: str


class PlatformStatus(BaseModel):
    """
    Root response returned by the PlantMind API.
    """

    platform: PlatformInfo
    runtime: RuntimeInfo