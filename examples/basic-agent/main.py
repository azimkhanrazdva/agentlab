import asyncio
import os

import httpx


async def main() -> None:
    base_url = os.getenv("AGENTLAB_BASE_URL", "http://localhost:8000")
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{base_url}/v1/chat/completions",
            json={
                "model": "mock/local",
                "user": "demo-session",
                "messages": [
                    {"role": "system", "content": "You are a concise demo agent."},
                    {"role": "user", "content": "Summarize what AgentLab observes in one sentence."},
                ],
            },
        )
        response.raise_for_status()
        data = response.json()
        print(data["choices"][0]["message"]["content"])
        print(f"trace_id={data['agentlab']['trace_id']}")


if __name__ == "__main__":
    asyncio.run(main())

