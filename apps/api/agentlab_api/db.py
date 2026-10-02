from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from agentlab_api.config import get_settings


class Base(DeclarativeBase):
    pass


def now() -> datetime:
    return datetime.now(UTC)


class TraceModel(Base):
    __tablename__ = "traces"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    session_id: Mapped[str | None] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, default="Agent run")
    status: Mapped[str] = mapped_column(String, default="running")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    meta: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class SpanModel(Base):
    __tablename__ = "spans"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    trace_id: Mapped[str] = mapped_column(ForeignKey("traces.id"), index=True)
    parent_id: Mapped[str | None] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="running")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(nullable=True)
    input: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    output: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    meta: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    token_usage: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    model: Mapped[str | None] = mapped_column(String, nullable=True)
    provider: Mapped[str | None] = mapped_column(String, nullable=True)
    risk_score: Mapped[int | None] = mapped_column(nullable=True)


class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    trace_id: Mapped[str] = mapped_column(ForeignKey("traces.id"), index=True)
    span_id: Mapped[str | None] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


engine = create_async_engine(get_settings().database_url, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
