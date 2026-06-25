from uuid import UUID

from app.repositories import RunRepository, SpanRepository
from app.schemas.observability import TimelineResponse


class TimelineService:
    def __init__(
        self,
        run_repository: RunRepository,
        span_repository: SpanRepository,
    ):
        self.run_repository = run_repository
        self.span_repository = span_repository

    def get_timeline(self, agent_id: UUID, run_id: UUID) -> TimelineResponse:
        run = self.run_repository.get(run_id)

        if run is None or run.agent_id != agent_id:
            raise ValueError("Run not found")

        spans = self.span_repository.list_by_run(run_id)

        return TimelineResponse.model_validate(
            {
                "run": run,
                "spans": spans,
            }
        )
