from typing import Optional

import streamlit as st
from anthropic import Anthropic
from pydantic import BaseModel

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = (
    "You write short, genuinely personalized cold outreach openers for a B2B sales "
    "team. Reference one specific, real signal about the company from the context "
    "given -- never generic flattery like 'I love what you're building.' Two "
    "sentences maximum. No greeting, no sign-off, just the opener itself."
)


class OutreachDraft(BaseModel):
    opener: str
    signal_referenced: str


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


def draft_opener(client: Anthropic, lead: dict) -> OutreachDraft:
    context = (
        f"Company: {lead['name']}\n"
        f"Website title: {lead['title']}\n"
        f"Description: {lead['meta_description']}\n"
        f"Signals found: {', '.join(lead['reasons']) or 'none specific'}\n"
    )
    response = client.messages.parse(
        model=MODEL,
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": context}],
        output_format=OutreachDraft,
    )
    return response.parsed_output
