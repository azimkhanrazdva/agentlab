from typing import Any, cast

import httpx

SENSITIVE_HEADERS = {"authorization", "x-api-key", "api-key"}


class OpenAICompatibleProvider:
    name = "openai-compatible"

    def __init__(self, base_url: str, api_key: str = "") -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    async def chat_completions(self, payload: dict[str, Any]) -> dict[str, Any]:
        headers = {"content-type": "application/json"}
        if self.api_key:
            headers["authorization"] = f"Bearer {self.api_key}"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
