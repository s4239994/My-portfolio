import streamlit as st
from anthropic import Anthropic
from pydantic import BaseModel

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = (
    "You are an HR insights assistant. You read a week of short daily mood "
    "check-ins from a team (an emoji-based mood score plus an optional "
    "one-line note) and write a concise briefing for their manager. Ground "
    "every claim in what people actually wrote or in the score trend -- "
    "never invent a specific incident that isn't in the notes. Keep the "
    "tone warm but direct and professional, not corporate-fluffy, and not "
    "alarmist over normal day-to-day variation."
)


class Briefing(BaseModel):
    headline: str
    summary: str
    watch_out_for: str
    suggested_action: str


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


def write_briefing(client: Anthropic, checkins: list) -> Briefing:
    lines = [
        f"{c['created_at'][:10]} -- {c['person']}: {c['mood_emoji']} {c['mood_label']}"
        + (f" -- \"{c['note']}\"" if c["note"] else "")
        for c in checkins
    ]
    context = "Check-ins from the last 7 days:\n" + "\n".join(lines)

    response = client.messages.parse(
        model=MODEL,
        max_tokens=700,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": context}],
        output_format=Briefing,
    )
    return response.parsed_output
