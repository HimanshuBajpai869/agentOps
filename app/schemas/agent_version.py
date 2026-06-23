from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class AgentVersionCreate(BaseModel):
    version: str
    prompt: str | None = None
    agent_config: str | None = None


class AgentVersionResponse(BaseModel):
    id: UUID
    agent_id: UUID
    version: str
    prompt: str | None = None
    agent_config: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
