from typing import Any, Protocol


class LLMProvider(Protocol):
    name: str

    async def chat_completions(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


def estimate_tokens(text: str) -> int:
    return max(1, len(text.split()))
