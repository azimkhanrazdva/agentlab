from datetime import datetime
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

SpanType = Literal["user", "llm", "tool", "security", "gateway", "attack", "replay"]
SpanStatus = Literal["running", "ok", "error", "blocked", "waiting"]


class TokenUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


class TraceCreate(BaseModel):
    session_id: str | None = None
    name: str = "Agent run"
    metadata: dict[str, Any] = Field(default_factory=dict)


class TraceRead(BaseModel):
    id: UUID
    session_id: str | None
    name: str
    status: str
    started_at: datetime
    ended_at: datetime | None
    metadata: dict[str, Any]


class SpanCreate(BaseModel):
    trace_id: UUID
    parent_id: UUID | None = None
    type: SpanType
    name: str
    status: SpanStatus = "running"
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    model: str | None = None
    provider: str | None = None
    risk_score: int | None = None


class SpanRead(SpanCreate):
    id: UUID = Field(default_factory=uuid4)
    started_at: datetime
    ended_at: datetime | None = None
    duration_ms: int | None = None


class EventRead(BaseModel):
    id: UUID
    trace_id: UUID
    span_id: UUID | None
    type: str
    payload: dict[str, Any]
    created_at: datetime

