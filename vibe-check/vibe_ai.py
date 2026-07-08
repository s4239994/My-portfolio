import streamlit as st
from anthropic import Anthropic
from pydantic import BaseModel

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = (
    "You are a blunt, funny Gen Z friend doing a 'vibe check' on a company's "
    "careers page and any extra material you're given. Quote actual phrases "
    "from the text when calling out red or green flags -- never invent a "
    "quote that isn't there. Keep the tone sharp, honest, and a little "
    "funny, like a smart friend texting you the truth, not corporate "
    "diplomatic language. No sugarcoating, but stay grounded in what's "
    "actually in the text -- don't make things up."
)


class Flag(BaseModel):
    quote: str
    reason: str


class VibeCheckResult(BaseModel):
    verdict: str
    summary: str
    red_flags: list[Flag]
    green_flags: list[Flag]


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


def run_vibe_check(
    client: Anthropic,
    company_name: str,
    page_text: str,
    extra_text: str,
    local_score: int,
    matched_red: list,
    matched_green: list,
) -> VibeCheckResult:
    context = f"""Company: {company_name}

Careers/about page text:
{page_text or "none fetched"}

Additional pasted material (job posting or review snippets, may be empty):
{extra_text or "none provided"}

An automated scan already found these red-flag phrases in the text: {", ".join(matched_red) or "none"}
An automated scan already found these green-flag phrases in the text: {", ".join(matched_green) or "none"}
Automated vibe score (0-100, higher is better): {local_score}

Give your own verdict, a short blunt summary, and lists of red/green flags,
each with an exact quote from the text above and why it matters."""

    response = client.messages.parse(
        model=MODEL,
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": context}],
        output_format=VibeCheckResult,
    )
    return response.parsed_output
