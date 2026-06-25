from uuid import UUID

from sqlalchemy.orm import Session

from app.models.span import Span
from app.schemas.observability import SpanCreate, SpanUpdate


class SQLAlchemySpanRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SpanCreate) -> Span:
        span = Span(
            run_id=data.run_id,
            parent_span_id=data.parent_span_id,
            name=data.name,
            span_type=data.span_type,
            span_metadata=data.metadata,
        )

        self.db.add(span)
        self.db.commit()
        self.db.refresh(span)

        return span

    def get(self, span_id: UUID) -> Span | None:
        return self.db.query(Span).filter(Span.id == span_id).first()

    def list_by_run(self, run_id: UUID) -> list[Span]:
        return (
            self.db.query(Span)
            .filter(Span.run_id == run_id)
            .order_by(Span.started_at.asc())
            .all()
        )

    def update(self, span_id: UUID, data: SpanUpdate) -> Span:
        span = self.get(span_id)

        if span is None:
            raise ValueError("Span not found")

        values = data.model_dump(exclude_unset=True)

        metadata = values.pop("metadata", None)
        if metadata is not None:
            span.span_metadata = metadata

        for key, value in values.items():
            setattr(span, key, value)

        self.db.add(span)
        self.db.commit()
        self.db.refresh(span)

        return span
