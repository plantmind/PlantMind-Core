from pydantic import BaseModel


class Alarm(BaseModel):

    tag: str

    priority: str

    description: str

    cause: str

    consequence: str

    action: str
