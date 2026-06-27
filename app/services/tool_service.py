from uuid import UUID

from sqlalchemy.orm import Session

from app.models.tool import Tool
from app.models.agent_version import AgentVersion


class ToolService:

    @staticmethod
    def create_tool(
        db: Session,
        name: str,
        description: str | None,
    ):

        existing = db.query(Tool).filter(Tool.name == name).first()

        if existing:
            raise ValueError(f"Tool '{name}' already exists.")

        tool = Tool(
            name=name,
            description=description,
        )

        db.add(tool)
        db.commit()
        db.refresh(tool)

        return tool

    @staticmethod
    def list_tools(
        db: Session,
    ):
        return db.query(Tool).all()

    @staticmethod
    def attach_tool(
        db: Session,
        version_id: UUID,
        tool_id: UUID,
    ):

        version = db.get(AgentVersion, version_id)
        tool = db.get(Tool, tool_id)

        if not version:
            raise ValueError("Version not found")

        if not tool:
            raise ValueError("Tool not found")

        if tool not in version.tools:
            version.tools.append(tool)

        db.commit()

        return version

    @staticmethod
    def list_version_tools(
        db: Session,
        version_id: UUID,
    ):

        version = db.get(
            AgentVersion,
            version_id,
        )

        if not version:
            raise ValueError("Version not found")

        return version.tools
