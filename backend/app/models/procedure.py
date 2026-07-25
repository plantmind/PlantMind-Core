from pydantic import BaseModel


class Procedure(BaseModel):

    procedure_id: str

    title: str

    revision: str

    description: str

    steps: list[str]
