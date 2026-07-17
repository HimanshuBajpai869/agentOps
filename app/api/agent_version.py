from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.agent_version import (
    AgentVersionCreate,
    AgentVersionResponse,
)
from app.services.agent_version_service import AgentVersionService
from app.schemas.tool import ToolResponse
from app.services.tool_service import ToolService

router = APIRouter(
    prefix="/agents/{agent_id}/versions",
    tags=["agent-versions"],
)


@router.post("", response_model=AgentVersionResponse)
def create_version(
    agent_id: UUID,
    request: AgentVersionCreate,
    db: Session = Depends(get_db),
):
    try:
        return AgentVersionService.create_version(
            db=db,
            agent_id=agent_id,
            version=request.version,
            prompt=request.prompt,
            agent_config=request.agent_config,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get(
    "/{agent_version_id}",
    response_model=AgentVersionResponse,
)
def get_version(
    agent_id: UUID,
    agent_version_id: UUID,
    db: Session = Depends(get_db),
):
    version = AgentVersionService.get_agent_version(db, agent_id, agent_version_id)
    if not version:
        raise HTTPException(
            status_code=404, detail=f"Agent version {agent_version_id} not found"
        )
    return version


@router.get("", response_model=list[AgentVersionResponse])
def list_versions(
    agent_id: UUID,
    db: Session = Depends(get_db),
):
    return AgentVersionService.list_versions(db, agent_id)


@router.post(
    "/{version_id}/tools/{tool_id}",
    response_model=list[ToolResponse],
)
def attach_tool(
    version_id: UUID,
    tool_id: UUID,
    db: Session = Depends(get_db),
):

    version = ToolService.attach_tool(
        db,
        version_id,
        tool_id,
    )

    return version.tools


@router.get(
    "/{version_id}/tools",
    response_model=list[ToolResponse],
)
def list_tools(
    version_id: UUID,
    db: Session = Depends(get_db),
):

    return ToolService.list_version_tools(
        db,
        version_id,
    )
