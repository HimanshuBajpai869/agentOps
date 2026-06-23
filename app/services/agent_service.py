from sqlalchemy.orm import Session

from app.models.agent import Agent
from app.models.agent_version import AgentVersion


class AgentService:

    @staticmethod
    def create_agent(
        db: Session,
        name: str,
        description: str | None,
        owner: str,
    ) -> Agent:

        existing = db.query(Agent).filter(Agent.name == name).first()

        if existing:
            raise ValueError(f"Agent {name} already exists")

        agent = Agent(
            name=name,
            description=description,
            owner=owner,
        )

        db.add(agent)
        db.commit()
        db.refresh(agent)

        return agent

    @staticmethod
    def list_agents(
        db: Session,
    ):
        return db.query(Agent).all()

    @staticmethod
    def get_agent(db, agent_id):
        return db.query(Agent).filter(Agent.id == agent_id).first()

    @staticmethod
    def activate_version(db: Session, agent_id, version_id):
        agent = db.query(Agent).filter(Agent.id == agent_id).first()

        if not agent:
            raise ValueError("Agent not found")

        version = (
            db.query(AgentVersion)
            .filter(
                AgentVersion.id == version_id,
                AgentVersion.agent_id == agent_id,
            )
            .first()
        )

        if not version:
            raise ValueError("Version not found for agent")

        agent.active_version_id = version_id

        db.add(agent)
        db.commit()
        db.refresh(agent)

        return agent
