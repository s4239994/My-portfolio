import streamlit as st
from anthropic import Anthropic
from pydantic import BaseModel

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = (
    "You write short, punchy 'wrapped' recaps of a software team's sprint, "
    "in the tone of Spotify Wrapped -- celebratory, specific, a little "
    "playful, never corporate. You're given real ticket titles and stats. "
    "Reference at least one specific real ticket title in your recap. "
    "Never invent a ticket, a number, or a detail that isn't in the data "
    "given to you."
)


class Recap(BaseModel):
    headline: str
    narrative: str
    fun_fact: str


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


def write_recap(client: Anthropic, stats: dict, sample_titles: list) -> Recap:
    context = f"""Sprint stats:
- Total tickets shipped: {stats['total']}
- Breakdown by type: {stats['by_type']}
- Dominant type: {stats['top_type']} ({stats['top_type_pct']}% of all tickets)
- Busiest day of the week: {stats['busiest_weekday']}
- Longest streak of consecutive days shipping something: {stats['longest_streak']}
- Date range: {stats['date_start']} to {stats['date_end']}
- Longest ticket title: "{stats['longest_title']}"

A sample of real ticket titles from this period:
{chr(10).join('- ' + t for t in sample_titles)}

Write a headline, a 2-3 sentence narrative recap, and one fun_fact -- all grounded only in the data above."""

    response = client.messages.parse(
        model=MODEL,
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": context}],
        output_format=Recap,
    )
    return response.parsed_output
