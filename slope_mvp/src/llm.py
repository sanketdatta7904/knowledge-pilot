import os
from typing import TypeVar, Type

from anthropic import Anthropic
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5")
MAX_TOKENS = 8192

_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic()
    return _client


def call_llm(
    system: str,
    user: str,
    response_model: Type[T],
    *,
    max_retries: int = 2,
) -> T:
    """Call Claude with forced tool-use to get a Pydantic-validated response."""
    schema = response_model.model_json_schema()
    tool = {
        "name": "submit_response",
        "description": f"Submit the structured response for {response_model.__name__}.",
        "input_schema": schema,
    }

    last_err: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            resp = _get_client().messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system,
                messages=[{"role": "user", "content": user}],
                tools=[tool],
                tool_choice={"type": "tool", "name": "submit_response"},
            )
            tool_block = next(b for b in resp.content if b.type == "tool_use")
            return response_model.model_validate(tool_block.input)
        except Exception as e:
            last_err = e
            if attempt == max_retries:
                raise
    raise RuntimeError(f"unreachable, last_err={last_err}")
