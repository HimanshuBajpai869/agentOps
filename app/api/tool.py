from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.tool import (
    ToolCreate,
    ToolResponse,
)

from app.services.tool_service import ToolService

router = APIRouter(
    prefix="/tools",
    tags=["tools"],
)


@router.post(
    "",
    response_model=ToolResponse,
)
def create_tool(
    request: ToolCreate,
    db: Session = Depends(get_db),
):

    try:
        return ToolService.create_tool(
            db=db,
            name=request.name,
            description=request.description,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[ToolResponse],
)
def list_tools(
    db: Session = Depends(get_db),
):

    return ToolService.list_tools(db)
