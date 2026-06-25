import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    agent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agents.id"), nullable=False)

    version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("agent_versions.id"), nullable=False
    )

    input_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)

    output: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="running")

    error_type: Mapped[str | None] = mapped_column(String(255), nullable=True)

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="tinyllama",
    )

    run_metadata: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSON,
        nullable=False,
        default=dict,
    )

    spans = relationship(
        "Span",
        back_populates="run",
        cascade="all, delete-orphan",
    )
