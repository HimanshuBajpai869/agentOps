from uuid import UUID

from sqlalchemy.orm import Session

from app.models.agent_run import AgentRun
from app.schemas.observability import RunCreate, RunUpdate


class SQLAlchemyRunRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: RunCreate) -> AgentRun:
        run = AgentRun(
            agent_id=data.agent_id,
            version_id=data.version_id,
            input_prompt=data.input_prompt,
            model=data.model,
            run_metadata=data.metadata,
        )

        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)

        return run

    def get(self, run_id: UUID) -> AgentRun | None:
        return self.db.query(AgentRun).filter(AgentRun.id == run_id).first()

    def list_by_agent(
        self,
        agent_id: UUID,
        version_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[AgentRun]:
        query = self.db.query(AgentRun).filter(AgentRun.agent_id == agent_id)

        if version_id:
            query = query.filter(AgentRun.version_id == version_id)

        return (
            query.order_by(AgentRun.created_at.desc()).offset(offset).limit(limit).all()
        )

    def update(self, run_id: UUID, data: RunUpdate) -> AgentRun:
        run = self.get(run_id)

        if run is None:
            raise ValueError("Run not found")

        values = data.model_dump(exclude_unset=True)

        metadata = values.pop("metadata", None)
        if metadata is not None:
            run.run_metadata = metadata

        for key, value in values.items():
            setattr(run, key, value)

        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)

        return run
