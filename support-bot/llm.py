from typing import Literal, Optional

import requests
from pydantic import BaseModel, Field

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"


class SupportReply(BaseModel):
    reply: str = Field(
        ...,
        description=(
            "A complete, helpful response that directly answers what the customer just "
            "asked or addresses their concern. Never just greet them -- always address "
            "their actual message."
        ),
    )
    sentiment: Literal["positive", "neutral", "frustrated", "angry"] = Field(
        ...,
        description="The customer's emotional tone in their most recent message, judged from its wording.",
    )
    handoff_recommended: bool = Field(
        ..., description="True if a human agent should take over this conversation."
    )
    handoff_reason: Optional[str] = Field(
        None, description="Why a handoff is recommended, or null if not recommended."
    )


def get_reply(system_prompt: str, conversation: list) -> SupportReply:
    messages = [{"role": "system", "content": system_prompt}] + conversation

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "format": SupportReply.model_json_schema(),
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    content = response.json()["message"]["content"]
    return SupportReply.model_validate_json(content)
