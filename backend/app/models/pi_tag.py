from pydantic import BaseModel


class PITag(BaseModel):
    tag_name: str
    description: str

    unit: str

    value: float = 0.0

    quality: str = "Good"

    source: str = "PI System"
