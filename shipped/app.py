import html

import pandas as pd
import streamlit as st

import parser
import recap_ai

st.set_page_config(page_title="Shipped", page_icon="🚀", layout="wide")

SAMPLE_FILE = "data/sample_tickets.csv"

CANVAS = "#15123a"
ACCENT = "#ff6a3d"
ACCENT_2 = "#ffd23f"
PAPER = "#ffffff"

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{ background: {CANVAS}; }}
    h1, h2, h3 {{ color: #ffffff; font-weight: 800 !important; }}
    [data-testid="stSidebar"] {{ background: #1d1a4a; }}

    .hero-card {{
        background: linear-gradient(135deg, #1d1a4a, #2a2470 60%, {ACCENT});
        border-radius: 22px; padding: 2.2rem 2.4rem; margin-bottom: 1.6rem;
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    }}
    .hero-title {{ font-size: 2.6rem; font-weight: 900; color: #fff; margin: 0.2rem 0 0.5rem; }}
    .hero-caption {{ color: #d8d4f0; font-size: 1.02rem; max-width: 640px; margin: 0; }}

    .wrapped-card {{
        background: linear-gradient(160deg, {ACCENT}, #ff3d7a 55%, #2a2470);
        border-radius: 26px; padding: 2.6rem; color: #fff;
        box-shadow: 0 24px 60px rgba(0,0,0,0.4);
        max-width: 480px;
    }}
    .wrapped-eyebrow {{ font-weight: 700; letter-spacing: 2px; font-size: 0.75rem; text-transform: uppercase; opacity: 0.85; }}
    .wrapped-archetype {{ font-size: 2.2rem; font-weight: 900; margin: 0.3rem 0 1rem; }}
    .wrapped-stat-num {{ font-size: 3.2rem; font-weight: 900; color: {ACCENT_2}; line-height: 1; }}
    .wrapped-stat-label {{ font-size: 0.85rem; opacity: 0.85; margin-top: 0.2rem; }}
    .wrapped-narrative {{ font-size: 1.02rem; line-height: 1.55; margin-top: 1.4rem; }}
    .wrapped-fact {{ background: rgba(255,255,255,0.15); border-radius: 12px; padding: 0.8rem 1rem; margin-top: 1.2rem; font-size: 0.92rem; }}

    .stat-card {{
        background: #1d1a4a; border-radius: 14px; padding: 1.1rem; text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    }}
    .stat-card .value {{ font-size: 1.6rem; font-weight: 800; color: {ACCENT_2}; }}
    .stat-card .label {{ font-size: 0.8rem; color: #cfcae8; margin-top: 2px; }}

    .stButton > button {{
        background: {ACCENT} !important; color: #ffffff !important; border: none !important;
        font-weight: 800 !important; border-radius: 999px !important; padding: 0.6rem 1.6rem !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <p class="hero-title">🚀 Shipped</p>
        <p class="hero-caption">A Rovo Agent concept for Atlassian -- turns your Jira ticket history into a
        shareable sprint recap. Spotify Wrapped energy, but for what you actually shipped.
        Real stats, an AI-written recap grounded in your real ticket titles, no invented numbers.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader("Upload a CSV with 'title', 'type', 'resolved_date'", type=["csv"])
    use_sample = st.checkbox("Use sample sprint data instead", value=uploaded is None)
    st.divider()
    generate_ai = st.checkbox(
        "Generate AI recap (Claude)",
        value=True,
        help="Costs a small fraction of a cent. Needs ANTHROPIC_API_KEY in secrets.",
    )

if use_sample:
    df = parser.load_tickets(SAMPLE_FILE)
elif uploaded is not None:
    df = parser.load_tickets(uploaded)
else:
    df = None

if df is not None:
    st.dataframe(df, use_container_width=True, height=150)
    run_clicked = st.button("Wrap my sprint", type="primary")
else:
    st.info("Upload a CSV or use the sample data to get started.")
    run_clicked = False

if run_clicked:
    stats = parser.compute_stats(df)
    st.session_state["stats"] = stats

    if generate_ai:
        with st.spinner("Writing your recap..."):
            try:
                client = recap_ai.get_client()
                sample_titles = df["title"].sample(min(10, len(df)), random_state=1).tolist()
                st.session_state["recap"] = recap_ai.write_recap(client, stats, sample_titles)
            except Exception as exc:
                st.warning(f"Skipping AI recap: {exc}")
                st.session_state["recap"] = None
    else:
        st.session_state["recap"] = None

if "stats" in st.session_state:
    stats = st.session_state["stats"]
    recap = st.session_state.get("recap")

    col1, col2 = st.columns([1, 1.3])

    with col1:
        narrative_html = (
            f'<div class="wrapped-narrative">{html.escape(recap.narrative)}</div>'
            f'<div class="wrapped-fact">💡 {html.escape(recap.fun_fact)}</div>'
            if recap
            else '<div class="wrapped-narrative">Turn on the AI recap in the sidebar for the full write-up.</div>'
        )
        st.markdown(
            f"""
            <div class="wrapped-card">
                <p class="wrapped-eyebrow">Sprint Wrapped · {stats['date_start']} → {stats['date_end']}</p>
                <p class="wrapped-archetype">{html.escape(recap.headline) if recap else stats['archetype_name']}</p>
                <p class="wrapped-stat-num">{stats['total']}</p>
                <p class="wrapped-stat-label">tickets shipped</p>
                {narrative_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.subheader("The numbers")
        stat_cols = st.columns(2)
        stat_cols[0].markdown(
            f'<div class="stat-card"><div class="value">{stats["top_type"]} ({stats["top_type_pct"]}%)</div>'
            f'<div class="label">most common type</div></div>',
            unsafe_allow_html=True,
        )
        stat_cols[1].markdown(
            f'<div class="stat-card"><div class="value">{stats["busiest_weekday"]}</div>'
            f'<div class="label">busiest ship day</div></div>',
            unsafe_allow_html=True,
        )
        st.write("")
        stat_cols2 = st.columns(2)
        stat_cols2[0].markdown(
            f'<div class="stat-card"><div class="value">{stats["longest_streak"]} days</div>'
            f'<div class="label">longest ship streak</div></div>',
            unsafe_allow_html=True,
        )
        stat_cols2[1].markdown(
            f'<div class="stat-card"><div class="value">{sum(stats["by_type"].values())}</div>'
            f'<div class="label">total across all types</div></div>',
            unsafe_allow_html=True,
        )

        st.write("")
        st.caption("Breakdown by type")
        breakdown_df = pd.DataFrame(
            {"type": list(stats["by_type"].keys()), "count": list(stats["by_type"].values())}
        ).set_index("type")
        st.bar_chart(breakdown_df)

        st.caption(f'Longest ticket title: "{stats["longest_title"]}"')
