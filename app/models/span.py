import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Span(Base):
    __tablename__ = "spans"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("agent_runs.id"),
        nullable=False,
        index=True,
    )

    parent_span_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("spans.id"),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    span_type: Mapped[str] = mapped_column(String(100), nullable=False)

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="running")

    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    error_type: Mapped[str | None] = mapped_column(String(255), nullable=True)

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    span_metadata: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSON,
        nullable=False,
        default=dict,
    )

    run = relationship("AgentRun", back_populates="spans")

    parent = relationship(
        "Span",
        remote_side=[id],
    )
