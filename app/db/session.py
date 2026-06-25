from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.repositories.sqlalchemy.run_repository import SQLAlchemyRunRepository
from app.repositories.sqlalchemy.span_repository import SQLAlchemySpanRepository
from app.services.timeline_service import TimelineService
from app.services.tracer_service import TracerService


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_run_repository(db: Session) -> SQLAlchemyRunRepository:
    return SQLAlchemyRunRepository(db)


def get_span_repository(db: Session) -> SQLAlchemySpanRepository:
    return SQLAlchemySpanRepository(db)


def get_tracer_service(db: Session = Depends(get_db)) -> TracerService:
    return TracerService(
        run_repository=get_run_repository(db),
        span_repository=get_span_repository(db),
    )


def get_timeline_service(db: Session = Depends(get_db)) -> TimelineService:
    return TimelineService(
        run_repository=get_run_repository(db),
        span_repository=get_span_repository(db),
    )
