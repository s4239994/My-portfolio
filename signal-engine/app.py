import html
import time
from pathlib import Path

import pandas as pd
import streamlit as st

import personalize
import pipeline
import scoring

st.set_page_config(page_title="Signal Engine", page_icon="📡", layout="wide")

SAMPLE_LEADS_FILE = Path(__file__).parent / "data" / "sample_leads.csv"

ACCENT = "#10b981"
ACCENT_2 = "#047857"
ACCENT_3 = "#1f2937"


def score_color(score: int) -> tuple[str, str]:
    """Returns (text color, tinted background) for a score pill."""
    if score >= 60:
        return "#0f9d58", "#e3f8ec"
    if score >= 30:
        return "#b8860b", "#fff3d6"
    return "#d1495b", "#fde8ea"


st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background:
            radial-gradient(at 10% 0%, rgba(16,185,129,0.16) 0, transparent 45%),
            radial-gradient(at 90% 10%, rgba(31,41,55,0.10) 0, transparent 45%),
            radial-gradient(at 0% 100%, rgba(4,120,87,0.14) 0, transparent 45%),
            #f7f8f7;
    }}
    [data-testid="stSidebar"] {{
        background: rgba(255,255,255,0.75); backdrop-filter: blur(14px);
        border-right: 1px solid rgba(16,185,129,0.18);
    }}
    [data-testid="stSidebar"] h2 {{ color: #1f2937; font-weight: 800; }}

    .tag-pill {{
        display: inline-block; font-family: "Segoe UI", sans-serif; font-weight: 700;
        letter-spacing: 1.5px; font-size: 0.75rem; color: #ffffff;
        background: linear-gradient(135deg, {ACCENT_2}, {ACCENT});
        padding: 0.3rem 0.85rem; border-radius: 999px; margin-bottom: 0.9rem;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35);
    }}
    .hero-card {{
        background: rgba(255,255,255,0.7); backdrop-filter: blur(20px);
        border: 1px solid rgba(31,41,55,0.08);
        border-radius: 24px; padding: 2.4rem 2.6rem; margin-bottom: 1.8rem;
        box-shadow: 0 20px 50px rgba(16, 185, 129, 0.14);
        position: relative; overflow: hidden;
    }}
    .hero-title {{
        margin: 0.2rem 0 0.6rem; font-size: 3.1rem; font-weight: 900; letter-spacing: -1px;
        background: linear-gradient(120deg, {ACCENT_3} 0%, {ACCENT_2} 55%, {ACCENT} 100%);
        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .hero-caption {{ color: #4b5563; margin: 0; font-size: 1.05rem; line-height: 1.6; max-width: 640px; }}

    .stat-card {{
        background: rgba(255,255,255,0.8); backdrop-filter: blur(16px);
        border: 1px solid rgba(31,41,55,0.07);
        border-radius: 16px; padding: 1.2rem; text-align: center;
        box-shadow: 0 10px 24px rgba(16, 185, 129, 0.10);
        transition: transform 0.15s ease;
    }}
    .stat-card .value {{
        font-size: 2rem; font-weight: 900;
        background: linear-gradient(120deg, {ACCENT_2}, {ACCENT});
        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .stat-card .label {{ font-size: 0.82rem; color: #6b7280; margin-top: 3px; font-weight: 600; }}

    .terminal-log {{
        background: linear-gradient(160deg, #111827, #0b0f16);
        border: 1px solid rgba(16,185,129,0.3);
        border-radius: 16px; box-shadow: 0 10px 28px rgba(16, 185, 129, 0.18);
        padding: 1.1rem 1.3rem; font-family: "Consolas", "SFMono-Regular", Menlo, monospace;
        font-size: 0.82rem; color: #6ee7b7; max-height: 340px; overflow-y: auto;
        white-space: pre-wrap; line-height: 1.7;
    }}

    .lead-card {{
        background: rgba(255,255,255,0.85); backdrop-filter: blur(16px);
        border: 1px solid rgba(31,41,55,0.07);
        border-radius: 18px; padding: 1.3rem 1.6rem; margin-bottom: 0.9rem;
        box-shadow: 0 10px 24px rgba(16, 185, 129, 0.10);
        border-left: 6px solid {ACCENT};
        transition: transform 0.15s ease;
    }}
    .lead-card:hover {{ transform: translateY(-2px); }}
    .lead-score {{
        font-size: 1.05rem; font-weight: 900; padding: 0.3rem 0.85rem; border-radius: 999px;
    }}
    .opener-box {{
        background: linear-gradient(120deg, rgba(16,185,129,0.08), rgba(31,41,55,0.05));
        border: 1px solid rgba(16,185,129,0.18); border-left: 4px solid {ACCENT};
        border-radius: 10px; padding: 0.8rem 1.1rem; margin-top: 0.7rem; font-size: 0.92rem;
        color: #1f2937;
    }}

    .stButton > button {{
        background: linear-gradient(120deg, {ACCENT_2}, {ACCENT}) !important;
        color: #ffffff !important; border: none !important; font-weight: 800 !important;
        border-radius: 10px !important; padding: 0.6rem 1.6rem !important;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.35) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 28px rgba(16, 185, 129, 0.45) !important;
    }}
    .stDownloadButton > button {{
        background: linear-gradient(120deg, {ACCENT_3}, #374151) !important;
        color: #ffffff !important; border: none !important; font-weight: 800 !important;
        border-radius: 10px !important; box-shadow: 0 8px 20px rgba(31, 41, 55, 0.3) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def stat_card(value, label: str) -> str:
    return f'<div class="stat-card"><div class="value">{value}</div><div class="label">{label}</div></div>'


st.markdown(
    """
    <div class="hero-card">
        <span class="tag-pill">✨ SIGNAL ACQUIRED</span>
        <p class="hero-title">📡 Signal Engine</p>
        <p class="hero-caption">Upload a lead list. It fetches each company's real public
        signals, scores them against your ideal customer profile, and drafts a
        genuinely personalized outreach opener -- streamed live, one lead at a time.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

default_config = scoring.load_icp_config()

with st.sidebar:
    st.header("Ideal Customer Profile")
    target_tech_input = st.text_input(
        "Target tech stack (comma-separated)",
        value=", ".join(default_config["target_tech"]),
    )
    target_keywords_input = st.text_input(
        "Target keywords (comma-separated)",
        value=", ".join(default_config["target_keywords"]),
    )
    st.caption("Scoring weights")
    w_careers = st.slider("Weight: actively hiring", 0, 50, default_config["weights"]["has_careers_page"])
    w_tech = st.slider("Weight: per matched tech", 0, 30, default_config["weights"]["tech_match"])
    w_keyword = st.slider("Weight: per matched keyword", 0, 20, default_config["weights"]["keyword_match"])

    config = {
        "target_tech": [t.strip() for t in target_tech_input.split(",") if t.strip()],
        "target_keywords": [k.strip() for k in target_keywords_input.split(",") if k.strip()],
        "weights": {"has_careers_page": w_careers, "tech_match": w_tech, "keyword_match": w_keyword},
    }

    st.divider()
    generate_openers = st.checkbox(
        "Generate AI-personalized openers (Claude)",
        value=True,
        help="Costs a small fraction of a cent per lead. Needs ANTHROPIC_API_KEY in secrets.",
    )

st.subheader("Leads")
uploaded = st.file_uploader("Upload a CSV with 'name' and 'url' columns", type=["csv"])
use_sample = st.checkbox("Use sample leads instead", value=uploaded is None)

if use_sample:
    leads_df = pd.read_csv(SAMPLE_LEADS_FILE)
elif uploaded is not None:
    leads_df = pd.read_csv(uploaded)
else:
    leads_df = pd.DataFrame(columns=["name", "url"])

st.dataframe(leads_df, use_container_width=True, height=150)

run_clicked = st.button("Run Signal Engine", type="primary", disabled=leads_df.empty)

log_placeholder = st.empty()
stats_placeholder = st.empty()
results_container = st.container()

if run_clicked:
    client = None
    if generate_openers:
        try:
            client = personalize.get_client()
        except Exception as exc:
            st.warning(f"Skipping AI personalization: {exc}")

    leads = leads_df.to_dict(orient="records")
    log_lines = []
    results = []
    start_time = time.time()

    for i, result in enumerate(pipeline.run_pipeline(leads, config, client=client), start=1):
        results.append(result)
        safe_name = html.escape(result["name"])
        log_lines.append(f"[{i:02d}] {safe_name} -- score {result['score']}/100")
        log_text = "\n".join(log_lines)
        log_placeholder.markdown(
            f'<div class="terminal-log">{log_text}</div>', unsafe_allow_html=True
        )

        elapsed = time.time() - start_time
        stats_placeholder.markdown(
            f'<div style="max-width:260px;">{stat_card(i, f"leads processed -- {elapsed:.1f}s")}</div>',
            unsafe_allow_html=True,
        )

    st.session_state["signal_results"] = results
    st.success(f"Done -- {len(results)} leads scored.")

if "signal_results" in st.session_state and st.session_state["signal_results"]:
    results = st.session_state["signal_results"]

    avg_score = round(sum(r["score"] for r in results) / len(results))
    high_fit = sum(1 for r in results if r["score"] >= 60)

    col1, col2, col3 = st.columns(3)
    col1.markdown(stat_card(len(results), "Total leads"), unsafe_allow_html=True)
    col2.markdown(stat_card(avg_score, "Avg score"), unsafe_allow_html=True)
    col3.markdown(stat_card(high_fit, "High-fit leads (60+)"), unsafe_allow_html=True)

    st.write("")
    st.subheader("Results")

    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        text_color, bg_color = score_color(r["score"])
        reasons_text = "; ".join(r["reasons"]) or "no strong signals detected"
        opener_html = ""
        if r.get("opener"):
            opener_html = f'<div class="opener-box">💬 {html.escape(r["opener"])}</div>'

        st.markdown(
            f"""
            <div class="lead-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#2d2b3a; font-size:1.05rem;">{html.escape(r['name'])}</b>
                    <span class="lead-score" style="color:{text_color}; background:{bg_color};">{r['score']}/100</span>
                </div>
                <div style="color:#6f6b7d; font-size:0.85rem; margin-top:4px;">{html.escape(reasons_text)}</div>
                {opener_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    export_df = pd.DataFrame([
        {
            "Company": r["name"],
            "Website": r["url"],
            "Lead Score": r["score"],
            "Detected Signals": "; ".join(r["reasons"]),
            "Suggested Opener": r.get("opener") or "",
        }
        for r in results
    ])
    st.download_button(
        "Download as CSV (HubSpot-ready)",
        export_df.to_csv(index=False),
        file_name="signal_engine_leads.csv",
    )
