from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from agentlab_attacks.scenario import load_scenario, run_scenario
from agentlab_gateway.service import provider_from_config, proxy_chat_completion
from agentlab_policies.engine import ToolAction, decide, score_action
from agentlab_security.secrets import has_secret, redact_secrets
from fastapi import Depends, FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agentlab_api.config import Settings, get_settings
from agentlab_api.db import EventModel, SpanModel, TraceModel, get_session, init_db


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await init_db()
    yield


SessionDep = Depends(get_session)
SettingsDep = Depends(get_settings)

app = FastAPI(title="AgentLab API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/v1/models")
async def models(settings: Settings = SettingsDep) -> dict[str, Any]:
    if settings.openai_base_url.startswith("mock://"):
        return {"object": "list", "data": [{"id": "mock/local", "object": "model", "owned_by": "agentlab"}]}
    return {"object": "list", "data": [{"id": "configured-provider", "object": "model", "owned_by": "external"}]}


@app.post("/v1/chat/completions")
async def chat_completions(
    payload: dict[str, Any],
    session: AsyncSession = SessionDep,
    settings: Settings = SettingsDep,
) -> dict[str, Any]:
    provider = provider_from_config(settings.openai_base_url, settings.openai_api_key)
    response: dict[str, Any] = await proxy_chat_completion(session, provider, payload, session_id=payload.get("user"))
    return response


@app.get("/api/v1/traces")
async def traces(session: AsyncSession = SessionDep) -> list[dict[str, Any]]:
    result = await session.execute(select(TraceModel).order_by(TraceModel.started_at.desc()).limit(100))
    return [
        {
            "id": trace.id,
            "session_id": trace.session_id,
            "name": trace.name,
            "status": trace.status,
            "started_at": trace.started_at,
            "ended_at": trace.ended_at,
            "metadata": trace.meta,
        }
        for trace in result.scalars()
    ]


@app.get("/api/v1/traces/{trace_id}")
async def trace_detail(trace_id: str, session: AsyncSession = SessionDep) -> dict[str, Any]:
    trace = await session.get(TraceModel, trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail={"error": {"code": "TRACE_NOT_FOUND", "message": "Trace not found."}})
    spans = (
        await session.execute(select(SpanModel).where(SpanModel.trace_id == trace_id).order_by(SpanModel.started_at))
    ).scalars()
    events = (
        await session.execute(select(EventModel).where(EventModel.trace_id == trace_id).order_by(EventModel.created_at))
    ).scalars()
    return {
        "trace": {
            "id": trace.id,
            "session_id": trace.session_id,
            "name": trace.name,
            "status": trace.status,
            "started_at": trace.started_at,
            "ended_at": trace.ended_at,
            "metadata": trace.meta,
        },
        "spans": [
            {
                "id": span.id,
                "trace_id": span.trace_id,
                "parent_id": span.parent_id,
                "type": span.type,
                "name": span.name,
                "status": span.status,
                "started_at": span.started_at,
                "ended_at": span.ended_at,
                "duration_ms": span.duration_ms,
                "input": span.input,
                "output": span.output,
                "metadata": span.meta,
                "error": span.error,
                "token_usage": span.token_usage,
                "model": span.model,
                "provider": span.provider,
                "risk_score": span.risk_score,
            }
            for span in spans
        ],
        "events": [{"id": e.id, "trace_id": e.trace_id, "span_id": e.span_id, "type": e.type, "payload": e.payload, "created_at": e.created_at} for e in events],
    }


@app.post("/api/v1/tools/evaluate")
async def evaluate_tool(payload: dict[str, Any]) -> dict[str, Any]:
    action = ToolAction(
        tool=str(payload.get("tool", "")),
        operation=str(payload.get("operation", "")),
        resource=str(payload.get("resource", "")),
        arguments=payload.get("arguments") or {},
        side_effect=bool(payload.get("side_effect", False)),
        network_target=payload.get("network_target"),
        filesystem_target=payload.get("filesystem_target"),
    )
    score = score_action(action)
    action = ToolAction(**{**action.__dict__, "risk": score})
    decision = decide(action)
    return {"decision": decision, "risk_score": score, "redacted_arguments": redact_secrets(action.arguments or {}), "secret_detected": has_secret(action.arguments or {})}


@app.post("/api/v1/attacks/run")
async def run_attack(payload: dict[str, Any]) -> dict[str, Any]:
    scenario_path = Path(str(payload.get("scenario_path", "examples/vulnerable-agent/scenario.yml")))
    if not scenario_path.exists():
        raise HTTPException(status_code=404, detail={"error": {"code": "SCENARIO_NOT_FOUND", "message": "Scenario not found."}})
    scenario = load_scenario(scenario_path)
    return run_scenario(scenario).model_dump()


@app.websocket("/ws/traces/{trace_id}")
async def trace_socket(websocket: WebSocket, trace_id: str) -> None:
    await websocket.accept()
    await websocket.send_json({"type": "connected", "trace_id": trace_id})
    await websocket.close()
