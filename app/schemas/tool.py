from uuid import UUID

from pydantic import BaseModel


class ToolCreate(BaseModel):
    name: str
    description: str | None = None


class ToolResponse(BaseModel):
    id: UUID
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}
