import time
from datetime import datetime

import streamlit as st

import advisory_ai
import db
import skin
import uv_api

st.set_page_config(page_title="uvos", page_icon="☀️", layout="wide")

CYAN = "#5eead4"
BG_WINDOW = "#0d0d0f"
BG_TITLEBAR = "#16161a"
TEXT = "#e4e4e7"
MUTED = "#7a7a85"

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background:
            radial-gradient(circle at 15% 15%, #2b1055 0%, transparent 55%),
            radial-gradient(circle at 85% 85%, #7303c0 0%, transparent 55%),
            linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }}
    [data-testid="stAppViewContainer"] * {{ font-family: "Consolas", "SFMono-Regular", Menlo, monospace; }}
    [data-testid="stSidebar"] {{ background: {BG_TITLEBAR}; border-right: 1px solid rgba(255,255,255,0.08); }}

    .window {{
        background: {BG_WINDOW}; border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px; box-shadow: 0 30px 80px rgba(0,0,0,0.5);
        margin-bottom: 1.4rem; overflow: hidden;
    }}
    .titlebar {{
        background: {BG_TITLEBAR}; padding: 0.6rem 1rem; display: flex; align-items: center; gap: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }}
    .dot {{ width: 12px; height: 12px; border-radius: 50%; display: inline-block; }}
    .window-body {{ padding: 1.4rem 1.6rem; }}
    .prompt {{ color: {CYAN}; font-weight: 700; }}
    .status-line {{ margin: 0.15rem 0; font-size: 0.95rem; }}
    .status-key {{ color: {MUTED}; }}

    .stButton > button {{
        background: {BG_TITLEBAR} !important; color: {CYAN} !important;
        border: 1px solid {CYAN} !important; font-family: "Consolas", monospace !important;
        border-radius: 6px !important; font-weight: 700 !important;
    }}
    .stButton > button:hover {{ background: rgba(94,234,212,0.12) !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def window_start(title: str):
    st.markdown(
        f"""
        <div class="window"><div class="titlebar">
            <span class="dot" style="background:#ff5f56;"></span>
            <span class="dot" style="background:#ffbd2e;"></span>
            <span class="dot" style="background:#27c93f;"></span>
            <span style="color:{MUTED}; margin-left:8px; font-size:0.85rem;">{title}</span>
        </div><div class="window-body">
        """,
        unsafe_allow_html=True,
    )


def window_end():
    st.markdown("</div></div>", unsafe_allow_html=True)


window_start("uvos — root@sun:~$")

if "booted" not in st.session_state:
    boot_lines = [
        "[  0.001200] uvos kernel booting...",
        "[  0.084213] connecting to ARPANSA satellite feed...",
        "[  0.211004] loading skin profile module...",
        "[  0.302881] calibrating erythemal dose tables...",
        "[  0.400000] uvos ready.",
    ]
    placeholder = st.empty()
    shown = []
    for line in boot_lines:
        shown.append(line)
        placeholder.markdown(
            f'<pre style="color:{CYAN}; font-size:0.85rem;">{chr(10).join(shown)}</pre>',
            unsafe_allow_html=True,
        )
        time.sleep(0.25)
    st.session_state["booted"] = True

st.markdown(
    f'<p class="prompt">$</p> <p style="margin-top:-1.6rem; margin-left:1.2rem;">'
    f"uvos -- a Linux-style sun exposure monitor, powered by live government UV data.</p>",
    unsafe_allow_html=True,
)
st.caption("Real-time UV Index from ARPANSA (Australia's radiation protection agency). Burn-time math uses the WHO UV Index formula and published Minimal Erythema Dose reference ranges -- see README for sources.")
window_end()

with st.sidebar:
    st.header("$ config")
    city = st.selectbox("--city", list(uv_api.CITIES.keys()))
    st.divider()
    st.caption("$ whoami --skin-type")
    quiz = skin.QUIZ_QUESTIONS[0]
    choice_labels = [opt[0] for opt in quiz["options"]]
    choice = st.radio(quiz["question"], choice_labels, index=2)
    skin_type = dict(quiz["options"])[choice]
    st.caption(f"skin_type={skin_type} ({skin.SKIN_TYPES[skin_type]['label']})")

uv_data = uv_api.get_current_uv(city)

window_start(f"uv_status --city={city}")
if uv_data["uv_index"] is None:
    st.warning("Couldn't reach ARPANSA right now. Try again shortly.")
else:
    tier_label, tier_color = skin.risk_tier(uv_data["uv_index"])
    burn_time = skin.burn_time_minutes(uv_data["uv_index"], skin_type)
    live_tag = "LIVE" if uv_data["is_live"] else f"most recent available ({uv_data['as_of'][:10]})"

    st.markdown(
        f"""
        <p class="status-line"><span class="status-key">UV_INDEX........</span>
            <b style="color:{tier_color};">{uv_data['uv_index']} [{tier_label}]</b></p>
        <p class="status-line"><span class="status-key">PEAK_TODAY.......</span> {uv_data['peak_today']}</p>
        <p class="status-line"><span class="status-key">SKIN_TYPE........</span> {skin_type}</p>
        <p class="status-line"><span class="status-key">BURN_TIME........</span>
            {f"{burn_time} min (unprotected)" if burn_time else "negligible risk right now"}</p>
        <p class="status-line"><span class="status-key">DATA_SOURCE......</span> ARPANSA -- {live_tag}</p>
        """,
        unsafe_allow_html=True,
    )
window_end()

window_start("session --track")
conn = db.get_connection()

col1, col2, col3 = st.columns(3)
if col1.button("$ start_session"):
    st.session_state["session_start"] = datetime.now()
    st.rerun()

if "session_start" in st.session_state:
    elapsed = (datetime.now() - st.session_state["session_start"]).total_seconds() / 60
    st.markdown(f'<p class="status-line"><span class="status-key">ELAPSED..........</span> {elapsed:.1f} min</p>', unsafe_allow_html=True)

    if col2.button("$ refresh"):
        st.rerun()

    if col3.button("$ end_session"):
        burn_time = skin.burn_time_minutes(uv_data["uv_index"], skin_type) if uv_data["uv_index"] else None
        exceeded = bool(burn_time and elapsed > burn_time)
        db.log_session(
            conn,
            {
                "city": city,
                "skin_type": skin_type,
                "uv_index": uv_data["uv_index"] or 0,
                "burn_time_minutes": burn_time,
                "elapsed_minutes": round(elapsed, 1),
                "exceeded_budget": int(exceeded),
                "logged_at": db.now_iso(),
            },
        )
        del st.session_state["session_start"]
        st.success("Session logged.")
        st.rerun()

    if st.button("$ generate_advisory (Claude)"):
        with st.spinner("uvos: querying advisory daemon..."):
            try:
                client = advisory_ai.get_client()
                burn_time = skin.burn_time_minutes(uv_data["uv_index"], skin_type) if uv_data["uv_index"] else None
                advisory = advisory_ai.get_advisory(
                    client, city, uv_data["uv_index"] or 0, skin_type, round(elapsed, 1), burn_time
                )
                level_color = {"INFO": CYAN, "NOTICE": "#f5d442", "WARNING": "#ff9d42", "CRITICAL": "#ff5c5c"}.get(
                    advisory.log_level, CYAN
                )
                st.markdown(
                    f'<p style="color:{level_color}; font-family:monospace;">'
                    f"[{advisory.log_level}] uvos: {advisory.message}</p>",
                    unsafe_allow_html=True,
                )
            except Exception as exc:
                st.warning(f"Advisory daemon unreachable: {exc}")
else:
    st.caption("No active session. Click $ start_session to begin tracking.")
window_end()

history = db.fetch_history(conn)
if history:
    window_start("cat session_history.log")
    for h in history[:15]:
        flag = " ⚠ EXCEEDED" if h["exceeded_budget"] else ""
        st.markdown(
            f'<p class="status-line">{h["logged_at"]} -- {h["city"]} -- skin={h["skin_type"]} -- '
            f'UV={h["uv_index"]} -- exposed {h["elapsed_minutes"]}min'
            f'{" / budget " + str(h["burn_time_minutes"]) + "min" if h["burn_time_minutes"] else ""}'
            f'<span style="color:#ff5c5c;">{flag}</span></p>',
            unsafe_allow_html=True,
        )
    window_end()
