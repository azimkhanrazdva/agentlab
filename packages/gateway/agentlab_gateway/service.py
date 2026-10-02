from datetime import UTC, datetime
from time import perf_counter
from typing import Any, cast
from uuid import UUID

from agentlab_api.db import EventModel, SpanModel, TraceModel
from agentlab_providers.mock import MockProvider
from agentlab_providers.openai_compatible import OpenAICompatibleProvider
from agentlab_security.secrets import redact_secrets
from sqlalchemy.ext.asyncio import AsyncSession


def provider_from_config(base_url: str, api_key: str) -> object:
    if base_url.startswith("mock://"):
        return MockProvider()
    return OpenAICompatibleProvider(base_url, api_key)


async def proxy_chat_completion(
    session: AsyncSession,
    provider: Any,
    payload: dict[str, Any],
    session_id: str | None = None,
) -> dict[str, Any]:
    trace = TraceModel(session_id=session_id, name="Chat completion", meta={"gateway": "openai-compatible"})
    session.add(trace)
    await session.flush()

    started = perf_counter()
    span = SpanModel(
        trace_id=trace.id,
        type="llm",
        name="POST /v1/chat/completions",
        input=cast(dict[str, Any], redact_secrets(payload)),
        model=payload.get("model"),
        provider=getattr(provider, "name", "unknown"),
        token_usage={},
    )
    session.add(span)
    await session.flush()

    try:
        response = await provider.chat_completions(payload)
        elapsed = int((perf_counter() - started) * 1000)
        usage = response.get("usage", {})
        span.status = "ok"
        span.output = cast(dict[str, Any], redact_secrets(response))
        span.token_usage = {
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        }
        span.ended_at = datetime.now(UTC)
        span.duration_ms = elapsed
        trace.status = "ok"
        trace.ended_at = datetime.now(UTC)
        session.add(EventModel(trace_id=trace.id, span_id=span.id, type="llm.completed", payload={"latency_ms": elapsed}))
        await session.commit()
        response.setdefault("agentlab", {})["trace_id"] = trace.id
        return cast(dict[str, Any], response)
    except Exception as exc:
        span.status = "error"
        span.error = str(exc)
        span.ended_at = datetime.now(UTC)
        span.duration_ms = int((perf_counter() - started) * 1000)
        trace.status = "error"
        trace.ended_at = datetime.now(UTC)
        await session.commit()
        raise


def as_uuid(value: str) -> UUID:
    return UUID(value)
