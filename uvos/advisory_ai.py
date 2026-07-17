import streamlit as st
from anthropic import Anthropic
from pydantic import BaseModel

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = (
    "You are a sun-safety advisory system that writes short system-log-style "
    "messages, like a Linux daemon warning. You're given a real, live UV "
    "Index reading, a person's skin type, and how long they've already been "
    "in the sun. Write one practical, specific piece of advice grounded "
    "only in the numbers given -- never invent medical claims or diagnoses. "
    "Keep the tone like a terminal warning: terse, direct, slightly "
    "deadpan, but genuinely useful. Reference official guidance style (SPF "
    "reapplication every 2 hours, seeking shade, protective clothing) "
    "rather than anything invented."
)


class Advisory(BaseModel):
    log_level: str
    message: str


def get_client() -> Anthropic:
    api_key = None
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        api_key = None

    if not api_key:
        raise RuntimeError(
            "No Anthropic API key found. Add ANTHROPIC_API_KEY to "
            ".streamlit/secrets.toml locally, or to this app's Secrets in "
            "Streamlit Community Cloud settings when deployed."
        )
    return Anthropic(api_key=api_key)


def get_advisory(
    client: Anthropic,
    city: str,
    uv_index: float,
    skin_type: str,
    elapsed_minutes: float,
    burn_time_minutes: float | None,
) -> Advisory:
    context = f"""City: {city}
Current UV Index: {uv_index}
Skin type: {skin_type}
Minutes already exposed this session: {elapsed_minutes}
Estimated unprotected burn time for this skin type at this UV Index: {burn_time_minutes if burn_time_minutes else "negligible risk"} minutes

Write a log_level (one of: INFO, NOTICE, WARNING, CRITICAL) and one message."""

    response = client.messages.parse(
        model=MODEL,
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": context}],
        output_format=Advisory,
    )
    return response.parsed_output
