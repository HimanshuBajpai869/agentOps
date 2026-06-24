from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.agent import (
    AgentCreate,
    AgentResponse,
)

from app.services.agent_service import (
    AgentService,
)

from app.services.agent_version_service import AgentVersionService

from app.models.agent_version import AgentVersion
from app.services.agent_runner_service import AgentRunner

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)


@router.post(
    "",
    response_model=AgentResponse,
)
def create_agent(
    request: AgentCreate,
    db: Session = Depends(get_db),
):

    try:
        return AgentService.create_agent(
            db=db,
            name=request.name,
            description=request.description,
            owner=request.owner,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[AgentResponse],
)
def list_agents(
    db: Session = Depends(get_db),
):
    return AgentService.list_agents(db)


@router.post("/{agent_id}/activate/{version_id}", response_model=AgentResponse)
def activate_agent_version(
    agent_id: UUID,
    version_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        return AgentService.activate_version(db, agent_id, version_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{agent_id}/run")
def run_agent(
    agent_id: UUID,
    input_text: str,
    model_name: str = "tinyllama",
    db: Session = Depends(get_db),
):

    agent = AgentService.get_agent(db, agent_id)

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if not agent.active_version_id:
        raise HTTPException(status_code=400, detail="No active version set")

    version = AgentVersionService.get_agent_version(db, agent.active_version_id)

    if not version:
        raise HTTPException(status_code=404, detail="Active version missing")

    return AgentRunner.run(db, agent, version, input_text, model_name)


@router.get("/{agent_id}/runs")
def get_runs(
    agent_id: UUID,
    version_id: UUID | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):

    return AgentRunner.list_runs(
        db=db,
        agent_id=agent_id,
        version_id=version_id,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{agent_id}",
    response_model=AgentResponse,
)
def get_agent(
    agent_id: UUID,
    db: Session = Depends(get_db),
):
    return AgentService.get_agent(db, agent_id)
