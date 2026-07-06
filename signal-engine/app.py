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

ACCENT = "#a78bfa"


def score_color(score: int) -> str:
    if score >= 60:
        return "#39FF88"
    if score >= 30:
        return "#f5c542"
    return "#ff6666"


st.markdown(
    f"""
    <style>
    .terminal-tag {{
        font-family: "Consolas", "SFMono-Regular", Menlo, monospace;
        color: #39FF88; opacity: 0.85; letter-spacing: 2px; font-size: 0.8rem;
    }}
    .hero-card {{
        background: linear-gradient(135deg, rgba(167,139,250,0.12), rgba(57,255,136,0.02));
        border: 1px solid #2a2b2f; border-left: 4px solid {ACCENT};
        border-radius: 12px; padding: 1.5rem 1.75rem; margin-bottom: 1.5rem;
    }}
    .hero-title {{ margin: 0.3rem 0 0.4rem; font-size: 1.9rem; }}
    .hero-caption {{ color: #9a9a9a; margin: 0; font-size: 0.95rem; }}
    .stat-card {{
        background: #17181b; border: 1px solid #2a2b2f; border-radius: 10px;
        padding: 0.9rem; text-align: center;
    }}
    .stat-card .value {{ font-size: 1.6rem; font-weight: 700; color: {ACCENT}; }}
    .stat-card .label {{ font-size: 0.8rem; color: #9a9a9a; margin-top: 2px; }}
    .terminal-log {{
        background: #0a0a0b; border: 1px solid #2a2b2f; border-radius: 8px;
        padding: 0.85rem 1.1rem; font-family: "Consolas", "SFMono-Regular", Menlo, monospace;
        font-size: 0.8rem; color: #39FF88; max-height: 340px; overflow-y: auto;
        white-space: pre-wrap; line-height: 1.5;
    }}
    .lead-card {{
        background: #17181b; border: 1px solid #2a2b2f; border-radius: 10px;
        padding: 1rem 1.25rem; margin-bottom: 0.6rem;
    }}
    .lead-score {{ font-size: 1.4rem; font-weight: 700; }}
    .opener-box {{
        background: #0e0e10; border-left: 3px solid {ACCENT}; border-radius: 6px;
        padding: 0.6rem 0.9rem; margin-top: 0.5rem; font-size: 0.9rem; color: #e5e5e5;
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
        <p class="terminal-tag">&gt; VIBE STATE: SIGNAL ACQUIRED</p>
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
        color = score_color(r["score"])
        reasons_text = "; ".join(r["reasons"]) or "no strong signals detected"
        opener_html = ""
        if r.get("opener"):
            opener_html = f'<div class="opener-box">💬 {html.escape(r["opener"])}</div>'

        st.markdown(
            f"""
            <div class="lead-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b>{html.escape(r['name'])}</b>
                    <span class="lead-score" style="color:{color};">{r['score']}/100</span>
                </div>
                <div style="color:#9a9a9a; font-size:0.85rem; margin-top:4px;">{html.escape(reasons_text)}</div>
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
