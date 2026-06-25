from typing import Protocol
from uuid import UUID

from app.models.agent_run import AgentRun
from app.schemas.observability import RunCreate, RunUpdate


class RunRepository(Protocol):
    def create(self, data: RunCreate) -> AgentRun:
        ...

    def get(self, run_id: UUID) -> AgentRun | None:
        ...

    def list_by_agent(
        self,
        agent_id: UUID,
        version_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[AgentRun]:
        ...

    def update(self, run_id: UUID, data: RunUpdate) -> AgentRun:
        ...
