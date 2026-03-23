from enum import Enum

from pydantic import BaseModel


class FieldOutput(BaseModel):
    value: str | None
    confidence: float
    method: str
    raw_text: str | None
    errors: list[str] = []


class RoutingOverride(str, Enum):
    IMAGE = "image"
