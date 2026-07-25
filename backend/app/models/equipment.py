from pydantic import BaseModel
from typing import List, Optional


class Equipment(BaseModel):
    tag: str
    name: str
    equipment_type: str
    unit: str

    manufacturer: Optional[str] = None
    model: Optional[str] = None

    description: Optional[str] = None

    pi_tags: List[str] = []
    procedures: List[str] = []
    alarms: List[str] = []

    criticality: str = "Medium"

    status: str = "Available"
