import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from app.db.base import Base


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(1024),
        nullable=True,
    )

    owner: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    active_version_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("agent_versions.id"),
        nullable=True,
    )

    versions = relationship(
        "AgentVersion",
        back_populates="agent",
        foreign_keys="AgentVersion.agent_id",
    )

    # Why post_update=True is needed
    # Because you now have a cycle dependency:
    # Agent → active_version_id → AgentVersion
    # AgentVersion → agent_id → Agent
    # SQLAlchemy needs:
    # “insert first, then update FK”
    # That’s what post_update=True enables.

    active_version = relationship(
        "AgentVersion",
        foreign_keys=[active_version_id],
        post_update=True,  # IMPORTANT for circular dependency
    )
