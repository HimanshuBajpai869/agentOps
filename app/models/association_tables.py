from sqlalchemy import Table, Column, ForeignKey

from app.db.base import Base

agent_version_tools = Table(
    "agent_version_tools",
    Base.metadata,
    Column(
        "agent_version_id",
        ForeignKey("agent_versions.id"),
        primary_key=True,
    ),
    Column(
        "tool_id",
        ForeignKey("tools.id"),
        primary_key=True,
    ),
)
