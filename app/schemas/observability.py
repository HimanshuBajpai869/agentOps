from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class RunCreate(BaseModel):
    agent_id: UUID
    version_id: UUID
    input_prompt: str | None = None
    model: str = "tinyllama"
    metadata: dict[str, Any] = Field(default_factory=dict)


class RunUpdate(BaseModel):
    output: str | None = None
    ended_at: datetime | None = None
    duration_ms: int | None = None
    status: str | None = None
    error_type: str | None = None
    error_message: str | None = None
    metadata: dict[str, Any] | None = None


class RunResponse(BaseModel):
    id: UUID
    agent_id: UUID
    version_id: UUID
    input_prompt: str | None = None
    output: str | None = None
    created_at: datetime
    started_at: datetime
    ended_at: datetime | None = None
    duration_ms: int | None = None
    status: str
    error_type: str | None = None
    error_message: str | None = None
    model: str
    metadata: dict[str, Any] = Field(default_factory=dict, validation_alias="run_metadata")

    model_config = {"from_attributes": True}


class SpanCreate(BaseModel):
    run_id: UUID
    name: str
    span_type: str
    parent_span_id: UUID | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SpanUpdate(BaseModel):
    ended_at: datetime | None = None
    duration_ms: int | None = None
    status: str | None = None
    error_type: str | None = None
    error_message: str | None = None
    metadata: dict[str, Any] | None = None


class SpanResponse(BaseModel):
    id: UUID
    run_id: UUID
    parent_span_id: UUID | None = None
    name: str
    span_type: str
    status: str
    started_at: datetime
    ended_at: datetime | None = None
    duration_ms: int | None = None
    error_type: str | None = None
    error_message: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict, validation_alias="span_metadata")

    model_config = {"from_attributes": True}


class TimelineResponse(BaseModel):
    run: RunResponse
    spans: list[SpanResponse]
