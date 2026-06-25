from datetime import datetime
from typing import Any
from collections.abc import Callable
from uuid import UUID

from app.models.agent_run import AgentRun
from app.models.span import Span
from app.repositories import RunRepository, SpanRepository
from app.schemas.observability import RunCreate, RunUpdate, SpanCreate, SpanUpdate


class TracerService:
    def __init__(
        self,
        run_repository: RunRepository,
        span_repository: SpanRepository,
    ):
        self.run_repository = run_repository
        self.span_repository = span_repository

    def start_run(
        self,
        agent_id: UUID,
        version_id: UUID,
        model: str,
        input_prompt: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AgentRun:
        return self.run_repository.create(
            RunCreate(
                agent_id=agent_id,
                version_id=version_id,
                input_prompt=input_prompt,
                model=model,
                metadata=metadata or {},
            )
        )

    def complete_run(
        self,
        run_id: UUID,
        output: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AgentRun:
        ended_at = datetime.utcnow()
        run = self._get_run(run_id)

        return self.run_repository.update(
            run_id,
            RunUpdate(
                output=output,
                ended_at=ended_at,
                duration_ms=self._duration_ms(run.started_at, ended_at),
                status="completed",
                metadata=metadata if metadata is not None else run.run_metadata,
            ),
        )

    def fail_run(
        self,
        run_id: UUID,
        error: Exception,
        metadata: dict[str, Any] | None = None,
    ) -> AgentRun:
        ended_at = datetime.utcnow()
        run = self._get_run(run_id)

        return self.run_repository.update(
            run_id,
            RunUpdate(
                ended_at=ended_at,
                duration_ms=self._duration_ms(run.started_at, ended_at),
                status="failed",
                error_type=error.__class__.__name__,
                error_message=str(error),
                metadata=metadata if metadata is not None else run.run_metadata,
            ),
        )

    def start_span(
        self,
        run_id: UUID,
        name: str,
        span_type: str,
        parent_span_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Span:
        self._get_run(run_id)

        return self.span_repository.create(
            SpanCreate(
                run_id=run_id,
                parent_span_id=parent_span_id,
                name=name,
                span_type=span_type,
                metadata=metadata or {},
            )
        )

    def complete_span(
        self,
        span_id: UUID,
        metadata: dict[str, Any] | None = None,
    ) -> Span:
        ended_at = datetime.utcnow()
        span = self._get_span(span_id)

        return self.span_repository.update(
            span_id,
            SpanUpdate(
                ended_at=ended_at,
                duration_ms=self._duration_ms(span.started_at, ended_at),
                status="completed",
                metadata=metadata if metadata is not None else span.span_metadata,
            ),
        )

    def fail_span(
        self,
        span_id: UUID,
        error: Exception,
        metadata: dict[str, Any] | None = None,
    ) -> Span:
        ended_at = datetime.utcnow()
        span = self._get_span(span_id)

        return self.span_repository.update(
            span_id,
            SpanUpdate(
                ended_at=ended_at,
                duration_ms=self._duration_ms(span.started_at, ended_at),
                status="failed",
                error_type=error.__class__.__name__,
                error_message=str(error),
                metadata=metadata if metadata is not None else span.span_metadata,
            ),
        )

    def list_run_spans(self, run_id: UUID) -> list[Span]:
        return self.span_repository.list_by_run(run_id)

    def trace_llm_call(
        self,
        run_id: UUID,
        name: str,
        operation: Callable[[], str],
        metadata: dict[str, Any] | None = None,
        parent_span_id: UUID | None = None,
    ) -> str:
        span = self.start_span(
            run_id=run_id,
            name=name,
            span_type="llm",
            parent_span_id=parent_span_id,
            metadata=metadata,
        )

        try:
            result = operation()
        except Exception as error:
            self.fail_span(span.id, error)
            raise

        self.complete_span(span.id)
        return result

    def trace_tool_call(
        self,
        run_id: UUID,
        name: str,
        operation: Callable[[], Any],
        metadata: dict[str, Any] | None = None,
        parent_span_id: UUID | None = None,
    ) -> Any:
        span = self.start_span(
            run_id=run_id,
            name=name,
            span_type="tool",
            parent_span_id=parent_span_id,
            metadata=metadata,
        )

        try:
            result = operation()
        except Exception as error:
            self.fail_span(span.id, error)
            raise

        self.complete_span(span.id)
        return result

    def _get_run(self, run_id: UUID) -> AgentRun:
        run = self.run_repository.get(run_id)

        if run is None:
            raise ValueError("Run not found")

        return run

    def _get_span(self, span_id: UUID) -> Span:
        span = self.span_repository.get(span_id)

        if span is None:
            raise ValueError("Span not found")

        return span

    @staticmethod
    def _duration_ms(started_at: datetime, ended_at: datetime) -> int:
        return int((ended_at - started_at).total_seconds() * 1000)
