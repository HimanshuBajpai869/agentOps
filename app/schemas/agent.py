from pydantic import BaseModel
from uuid import UUID


class AgentCreate(BaseModel):
    name: str
    description: str | None = None
    owner: str


class AgentResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    owner: str
    active_version_id: UUID | None = None
