from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.agent_version import (
    AgentVersionCreate,
    AgentVersionResponse,
)
from app.services.agent_version_service import AgentVersionService

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


@router.get("", response_model=list[AgentVersionResponse])
def list_versions(
    agent_id: UUID,
    db: Session = Depends(get_db),
):
    return AgentVersionService.list_versions(db, agent_id)
