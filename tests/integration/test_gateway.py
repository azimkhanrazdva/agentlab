import pytest
from agentlab_api.db import init_db
from agentlab_api.main import app
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_gateway_creates_trace() -> None:
    await init_db()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.get("/health")
        response = await client.post(
            "/v1/chat/completions",
            json={"model": "mock/local", "messages": [{"role": "user", "content": "hello"}]},
        )
        assert response.status_code == 200
        trace_id = response.json()["agentlab"]["trace_id"]
        trace = await client.get(f"/api/v1/traces/{trace_id}")
        assert trace.status_code == 200
        assert trace.json()["spans"][0]["status"] == "ok"
