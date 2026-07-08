import html
from pathlib import Path

import pandas as pd
import streamlit as st

import enrichment
import scoring
import vibe_ai

st.set_page_config(page_title="Vibe Check", page_icon="🔍", layout="wide")

SAMPLE_COMPANIES_FILE = Path(__file__).parent / "data" / "sample_companies.csv"

INK = "#0a0a0a"
PINK = "#ff2f92"
LIME = "#c6ff1e"
YELLOW = "#ffe600"
BG = "#f7f4ec"


def tier(score: int) -> tuple[str, str]:
    """Returns (label, color) for a score tier."""
    if score >= 70:
        return "APPROVED", LIME
    if score >= 40:
        return "MID", YELLOW
    return "RED FLAG", PINK


st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-color: {BG};
        background-image: radial-gradient(circle, rgba(10,10,10,0.10) 1.2px, transparent 1.2px);
        background-size: 18px 18px;
    }}
    [data-testid="stSidebar"] {{
        background: #ffffff; border-right: 4px solid {INK};
    }}
    h1, h2, h3 {{ text-transform: uppercase; letter-spacing: -0.5px; font-weight: 900 !important; }}

    .brutal-card {{
        background: #ffffff; border: 4px solid {INK}; border-radius: 0px;
        box-shadow: 8px 8px 0 {INK}; padding: 1.6rem 1.9rem; margin-bottom: 1.6rem;
    }}
    .hero-title {{
        margin: 0 0 0.6rem; font-size: 3rem; font-weight: 900; text-transform: uppercase;
        letter-spacing: -1px; line-height: 1;
    }}
    .hero-caption {{ font-size: 1.05rem; line-height: 1.55; max-width: 680px; margin: 0; }}
    .tag-pill {{
        display: inline-block; font-weight: 800; letter-spacing: 1px; font-size: 0.75rem;
        text-transform: uppercase; background: {YELLOW}; color: {INK};
        border: 3px solid {INK}; padding: 0.25rem 0.75rem; margin-bottom: 0.9rem;
        box-shadow: 4px 4px 0 {INK};
    }}

    .stamp {{
        display: inline-block; font-size: 2.6rem; font-weight: 900; text-transform: uppercase;
        border: 5px solid {INK}; padding: 0.5rem 1.4rem; transform: rotate(-5deg);
        box-shadow: 8px 8px 0 {INK}; margin: 0.5rem 0 1rem;
    }}

    .flag-card {{
        border: 3px solid {INK}; border-radius: 0px; padding: 0.8rem 1.1rem;
        margin-bottom: 0.7rem; box-shadow: 5px 5px 0 {INK};
    }}
    .flag-red {{ background: rgba(255,47,146,0.12); }}
    .flag-green {{ background: rgba(198,255,30,0.18); }}
    .flag-quote {{ font-style: italic; font-weight: 700; }}
    .flag-reason {{ font-size: 0.9rem; margin-top: 0.3rem; }}

    .phrase-chip {{
        display: inline-block; border: 2px solid {INK}; padding: 0.15rem 0.55rem;
        margin: 0.15rem; font-size: 0.78rem; font-weight: 700; text-transform: uppercase;
    }}
    .chip-red {{ background: {PINK}; }}
    .chip-green {{ background: {LIME}; }}

    .stButton > button {{
        background: {INK} !important; color: #ffffff !important; border: 3px solid {INK} !important;
        border-radius: 0px !important; font-weight: 800 !important; text-transform: uppercase !important;
        letter-spacing: 0.5px !important; padding: 0.6rem 1.6rem !important;
        box-shadow: 6px 6px 0 rgba(10,10,10,0.35) !important;
        transition: transform 0.1s ease, box-shadow 0.1s ease !important;
    }}
    .stButton > button:hover {{
        transform: translate(-2px, -2px) !important;
        box-shadow: 8px 8px 0 rgba(10,10,10,0.5) !important;
    }}
    .stButton > button:active {{
        transform: translate(2px, 2px) !important;
        box-shadow: 2px 2px 0 rgba(10,10,10,0.5) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="brutal-card">
        <span class="tag-pill">no cap zone</span>
        <p class="hero-title">Vibe Check</p>
        <p class="hero-caption">Paste a company's careers page and it gets scanned for real --
        buzzword red flags, missing pay transparency, and generic corporate-speak, plus
        an AI-written, no-sugarcoating verdict quoting their own words back at them.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

signals_config = scoring.load_signals_config()

with st.sidebar:
    st.header("Signal rules")
    red_input = st.text_area(
        "Red-flag phrases (comma-separated)",
        value=", ".join(signals_config["red_flag_phrases"]),
        height=120,
    )
    green_input = st.text_area(
        "Green-flag phrases (comma-separated)",
        value=", ".join(signals_config["green_flag_phrases"]),
        height=120,
    )
    signals_config = {
        **signals_config,
        "red_flag_phrases": [p.strip().lower() for p in red_input.split(",") if p.strip()],
        "green_flag_phrases": [p.strip().lower() for p in green_input.split(",") if p.strip()],
    }
    st.divider()
    use_ai = st.checkbox(
        "Full AI vibe check (Claude)",
        value=True,
        help="Costs a small fraction of a cent per check. Needs ANTHROPIC_API_KEY in secrets. "
        "Without it, you still get the free deterministic score.",
    )

sample_df = pd.read_csv(SAMPLE_COMPANIES_FILE)
sample_choice = st.selectbox(
    "Quick-pick a real Melbourne/AU company (or fill in your own below)",
    ["-- type your own --"] + sample_df["name"].tolist(),
)

if sample_choice != "-- type your own --":
    row = sample_df[sample_df["name"] == sample_choice].iloc[0]
    default_name, default_url = row["name"], row["url"]
else:
    default_name, default_url = "", ""

col1, col2 = st.columns(2)
company_name = col1.text_input("Company name", value=default_name)
careers_url = col2.text_input("Careers/about page URL", value=default_url)
extra_text = st.text_area(
    "Optional: paste a job posting or review snippets (Glassdoor/Indeed/LinkedIn text you copied yourself)",
    height=100,
)

run_clicked = st.button("Run Vibe Check", type="primary", disabled=not careers_url)

if run_clicked:
    with st.spinner("Fetching and scanning..."):
        page = enrichment.fetch_page_text(careers_url)
        full_text = f"{page['title']} {page['text']} {extra_text}"
        result = scoring.score_vibe(full_text, signals_config)

        ai_result = None
        if use_ai:
            try:
                client = vibe_ai.get_client()
                ai_result = vibe_ai.run_vibe_check(
                    client,
                    company_name or careers_url,
                    page["text"],
                    extra_text,
                    result["score"],
                    result["matched_red"],
                    result["matched_green"],
                )
            except Exception as exc:
                st.warning(f"Skipping AI vibe check: {exc}")

    st.session_state["vibe_result"] = {
        "page": page,
        "result": result,
        "ai_result": ai_result,
        "company_name": company_name or careers_url,
    }

if "vibe_result" in st.session_state:
    data = st.session_state["vibe_result"]
    page, result, ai_result = data["page"], data["result"], data["ai_result"]

    if page["note"]:
        st.info(page["note"])

    label, color = tier(result["score"])
    st.markdown(
        f"""
        <span class="stamp" style="background:{color};">{label} -- {result['score']}/100</span>
        """,
        unsafe_allow_html=True,
    )

    if ai_result:
        st.markdown(
            f"""
            <div class="brutal-card">
                <p class="tag-pill" style="background:{YELLOW};">{html.escape(ai_result.verdict)}</p>
                <p style="font-size:1.05rem; line-height:1.6;">{html.escape(ai_result.summary)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_red, col_green = st.columns(2)
        with col_red:
            st.subheader("🚩 Red flags")
            if not ai_result.red_flags:
                st.write("None found -- surprisingly clean.")
            for flag in ai_result.red_flags:
                st.markdown(
                    f"""
                    <div class="flag-card flag-red">
                        <div class="flag-quote">"{html.escape(flag.quote)}"</div>
                        <div class="flag-reason">{html.escape(flag.reason)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        with col_green:
            st.subheader("✅ Green flags")
            if not ai_result.green_flags:
                st.write("None found.")
            for flag in ai_result.green_flags:
                st.markdown(
                    f"""
                    <div class="flag-card flag-green">
                        <div class="flag-quote">"{html.escape(flag.quote)}"</div>
                        <div class="flag-reason">{html.escape(flag.reason)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.caption("Free scan only -- turn on the AI vibe check in the sidebar for the full roast with quotes.")
        red_chips = "".join(
            f'<span class="phrase-chip chip-red">{html.escape(p)}</span>' for p in result["matched_red"]
        ) or "none"
        green_chips = "".join(
            f'<span class="phrase-chip chip-green">{html.escape(p)}</span>' for p in result["matched_green"]
        ) or "none"
        st.markdown(f"**Red-flag phrases found:** {red_chips}", unsafe_allow_html=True)
        st.markdown(f"**Green-flag phrases found:** {green_chips}", unsafe_allow_html=True)
        if result["has_salary_number"]:
            st.markdown("💰 Mentions an actual pay number -- rare and respected.")
