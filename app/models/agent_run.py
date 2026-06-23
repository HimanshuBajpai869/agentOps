import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    agent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agents.id"), nullable=False)

    version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("agent_versions.id"), nullable=False
    )

    input_prompt: Mapped[str] = mapped_column(Text, nullable=True)

    output: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="tinyllama",
    )
