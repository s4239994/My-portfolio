import html

import pandas as pd
import streamlit as st

import briefing_ai
import db
import seed

st.set_page_config(page_title="Pulse", page_icon="💓", layout="wide")

ACCENT = "#ff6b4a"
NAVY = "#1e2a4a"
BG = "#fffaf5"

MOODS = [
    ("thriving", "🔥", 5),
    ("good", "😊", 4),
    ("mid", "😐", 3),
    ("rough", "😩", 2),
    ("done", "💀", 1),
]

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{ background: {BG}; }}
    h1, h2, h3 {{ color: {NAVY}; font-weight: 800 !important; }}

    .hero-card {{
        background: #ffffff; border-radius: 20px; padding: 2rem 2.2rem; margin-bottom: 1.6rem;
        box-shadow: 0 8px 28px rgba(30,42,74,0.08); border-top: 5px solid {ACCENT};
    }}
    .hero-title {{ margin: 0.2rem 0 0.5rem; font-size: 2.3rem; font-weight: 800; color: {NAVY}; }}
    .hero-caption {{ color: #5b6478; margin: 0; font-size: 1.02rem; line-height: 1.6; max-width: 680px; }}

    .stat-card {{
        background: #ffffff; border-radius: 16px; padding: 1.1rem; text-align: center;
        box-shadow: 0 6px 18px rgba(30,42,74,0.07);
    }}
    .stat-card .value {{ font-size: 1.7rem; font-weight: 800; color: {ACCENT}; }}
    .stat-card .label {{ font-size: 0.82rem; color: #5b6478; margin-top: 2px; }}

    .note-card {{
        background: #ffffff; border-radius: 14px; padding: 0.7rem 1rem; margin-bottom: 0.5rem;
        box-shadow: 0 4px 14px rgba(30,42,74,0.06); font-size: 0.92rem; color: {NAVY};
    }}

    .briefing-card {{
        background: #ffffff; border-radius: 18px; padding: 1.4rem 1.7rem; margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(30,42,74,0.08); border-left: 5px solid {ACCENT};
    }}
    .briefing-label {{ font-size: 0.75rem; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; color: {ACCENT}; }}

    .stButton > button {{
        background: {ACCENT} !important; color: #ffffff !important; border: none !important;
        font-weight: 700 !important; border-radius: 12px !important; padding: 0.6rem 1.4rem !important;
        box-shadow: 0 6px 16px rgba(255,107,74,0.35) !important;
        transition: transform 0.12s ease !important;
    }}
    .stButton > button:hover {{ transform: translateY(-2px) !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <p class="hero-title">💓 Pulse</p>
        <p class="hero-caption">A 5-second team check-in people actually do -- tap an emoji,
        add a one-liner if you feel like it. No 40-question survey, no login wall. Managers get
        a live mood trend and an AI-written weekly briefing grounded in what the team actually wrote.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

conn = db.get_connection()

with st.sidebar:
    st.header("Demo controls")
    st.caption("This is a demo -- data lives in a local file and resets when the app restarts.")
    if st.button("Load demo team (28 days)"):
        seed.generate_demo_data(conn)
        st.success("Seeded a demo team with a realistic mid-month crunch week.")
        st.rerun()
    if st.button("Clear all data"):
        db.clear_all(conn)
        st.rerun()

st.subheader("Check in")
col1, col2 = st.columns([1, 2])
person = col1.text_input("Your name", placeholder="e.g. Sam")
note = col2.text_input("One line about today (optional)", placeholder="e.g. shipped a big feature")

mood_cols = st.columns(5)
for i, (label, emoji, score) in enumerate(MOODS):
    if mood_cols[i].button(f"{emoji} {label}", key=f"mood_{label}", use_container_width=True):
        db.insert_checkin(
            conn,
            {
                "person": person.strip() or "Anonymous",
                "mood_label": label,
                "mood_emoji": emoji,
                "mood_score": score,
                "note": note.strip(),
                "created_at": db.now_iso(),
            },
        )
        st.balloons()
        st.success("Checked in -- thanks!")
        st.rerun()

st.divider()

all_checkins = db.fetch_all(conn)

if not all_checkins:
    st.info("No check-ins yet. Load the demo team from the sidebar, or check in above.")
else:
    df = pd.DataFrame(all_checkins)
    df["date"] = pd.to_datetime(df["created_at"]).dt.date
    recent = db.fetch_recent(conn, days=7)

    st.subheader("Team pulse")
    stat_cols = st.columns(3)
    avg_week = round(sum(c["mood_score"] for c in recent) / len(recent), 1) if recent else 0
    stat_cols[0].markdown(
        f'<div class="stat-card"><div class="value">{len(all_checkins)}</div><div class="label">total check-ins</div></div>',
        unsafe_allow_html=True,
    )
    stat_cols[1].markdown(
        f'<div class="stat-card"><div class="value">{avg_week}/5</div><div class="label">avg mood, last 7 days</div></div>',
        unsafe_allow_html=True,
    )
    stat_cols[2].markdown(
        f'<div class="stat-card"><div class="value">{len(recent)}</div><div class="label">check-ins, last 7 days</div></div>',
        unsafe_allow_html=True,
    )

    st.write("")
    daily_avg = df.groupby("date")["mood_score"].mean()
    st.line_chart(daily_avg)

    st.subheader("Recent notes")
    with_notes = [c for c in reversed(all_checkins) if c["note"]][:10]
    if not with_notes:
        st.caption("No notes left yet.")
    for c in with_notes:
        st.markdown(
            f'<div class="note-card">{c["mood_emoji"]} <b>{html.escape(c["person"])}</b> -- '
            f'{html.escape(c["note"])} <span style="color:#9aa1b2;">({c["created_at"][:10]})</span></div>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.subheader("Weekly manager briefing")
    generate_clicked = st.button("Generate this week's briefing (Claude)", disabled=not recent)

    if generate_clicked:
        with st.spinner("Reading the week..."):
            try:
                client = briefing_ai.get_client()
                briefing = briefing_ai.write_briefing(client, recent)
                st.session_state["briefing"] = briefing
            except Exception as exc:
                st.warning(f"Couldn't generate a briefing: {exc}")

    if "briefing" in st.session_state:
        b = st.session_state["briefing"]
        st.markdown(
            f"""
            <div class="briefing-card">
                <div class="briefing-label">Headline</div>
                <p style="font-size:1.2rem; font-weight:700; color:{NAVY};">{html.escape(b.headline)}</p>
                <div class="briefing-label">Summary</div>
                <p>{html.escape(b.summary)}</p>
                <div class="briefing-label">Watch out for</div>
                <p>{html.escape(b.watch_out_for)}</p>
                <div class="briefing-label">Suggested action</div>
                <p style="margin-bottom:0;">{html.escape(b.suggested_action)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
