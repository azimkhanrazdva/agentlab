from time import time
from typing import Any
from uuid import uuid4

from agentlab_providers.base import estimate_tokens


class MockProvider:
    name = "mock"

    async def chat_completions(self, payload: dict[str, Any]) -> dict[str, Any]:
        messages = payload.get("messages", [])
        prompt = " ".join(str(message.get("content", "")) for message in messages)
        content = f"Mock provider received: {prompt[:220]}"
        if "Summarize" in prompt and "document" in prompt:
            content = "Summary: the document contains instructions. I will not access secrets."
        input_tokens = estimate_tokens(prompt)
        output_tokens = estimate_tokens(content)
        return {
            "id": f"chatcmpl-{uuid4()}",
            "object": "chat.completion",
            "created": int(time()),
            "model": payload.get("model", "mock/local"),
            "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": input_tokens,
                "completion_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
            },
        }

