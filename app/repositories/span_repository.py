from typing import Protocol
from uuid import UUID

from app.models.span import Span
from app.schemas.observability import SpanCreate, SpanUpdate


class SpanRepository(Protocol):
    def create(self, data: SpanCreate) -> Span:
        ...

    def get(self, span_id: UUID) -> Span | None:
        ...

    def list_by_run(self, run_id: UUID) -> list[Span]:
        ...

    def update(self, span_id: UUID, data: SpanUpdate) -> Span:
        ...
