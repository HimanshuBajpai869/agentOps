from sqlalchemy.orm import Session

from app.models.agent_version import AgentVersion


class AgentVersionService:

    @staticmethod
    def create_version(
        db: Session,
        agent_id,
        version: str,
        prompt: str | None,
        agent_config: str | None,
    ):

        existing = (
            db.query(AgentVersion)
            .filter(
                AgentVersion.agent_id == agent_id,
                AgentVersion.version == version,
            )
            .first()
        )

        if existing:
            raise ValueError("Version already exists for this agent")

        v = AgentVersion(
            agent_id=agent_id,
            version=version,
            prompt=prompt,
            agent_config=agent_config,
        )

        db.add(v)
        db.commit()
        db.refresh(v)

        return v

    @staticmethod
    def list_versions(db: Session, agent_id):
        return db.query(AgentVersion).filter(AgentVersion.agent_id == agent_id).all()

    @staticmethod
    def get_agent_version(db, agent_id, agent_version_id):
        return (
            db.query(AgentVersion)
            .filter(
                AgentVersion.id == agent_version_id, AgentVersion.agent_id == agent_id
            )
            .first()
        )
