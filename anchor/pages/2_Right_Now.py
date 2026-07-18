import streamlit as st

from common import db, style

st.set_page_config(page_title="Right Now — Anchor", page_icon="\U0001F198", layout="centered")
style.inject_base_css()

conn = db.get_connection()
meta = db.get_meta(conn)
metaphor_key = meta["metaphor"] or "fog"
metaphor = db.METAPHORS[metaphor_key]

if "rn_step" not in st.session_state:
    st.session_state.rn_step = 0

TOTAL_STEPS = 5


def always_visible_crisis_line():
    st.markdown(
        """
        <div class="crisis-line-card">
        <b>If you're in immediate danger, call 000.</b><br>
        Lifeline (Australia): <b>13 11 14</b> — call or text, anytime.
        </div>
        """,
        unsafe_allow_html=True,
    )


always_visible_crisis_line()

intensity = max(0.0, 1.0 - (st.session_state.rn_step / TOTAL_STEPS))
style.render_metaphor(metaphor, intensity=intensity, size=180)

step = st.session_state.rn_step

if step == 0:
    st.markdown("### Let's just breathe for a moment.")
    st.markdown('<p class="muted">You don\'t have to fix anything yet. Just this.</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align:center; margin: 1.5rem 0;">
            <div style="display:inline-block; width:120px; height:120px; border-radius:50%;
                        background: radial-gradient(circle, #a9b8e8, #7c8fd6);
                        animation: breathe 8s ease-in-out infinite;"></div>
        </div>
        <style>
        @keyframes breathe {
            0%, 100% { transform: scale(0.75); opacity: 0.6; }
            50% { transform: scale(1.15); opacity: 1; }
        }
        </style>
        <p class="muted" style="text-align:center;">In slowly as it grows. Out slowly as it shrinks. A few times.</p>
        """,
        unsafe_allow_html=True,
    )
    if st.button("I've taken a few breaths →", use_container_width=True):
        st.session_state.rn_step = 1
        st.rerun()

elif step == 1:
    st.markdown("### This is what you told yourself to watch for.")
    signs = db.list_warning_signs(conn)
    if signs:
        st.markdown('<p class="muted">You wrote these when you were steady, so you\'d recognize this moment. You did.</p>', unsafe_allow_html=True)
        for s in signs:
            st.markdown(f'<div class="calm-card">{s["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="muted">You haven\'t written any warning signs yet — that\'s okay, keep going.</p>', unsafe_allow_html=True)
    if st.button("Okay, what helps →", use_container_width=True):
        st.session_state.rn_step = 2
        st.rerun()

elif step == 2:
    st.markdown("### Here's what you said helps.")
    strategies = db.list_coping_strategies(conn)
    if strategies:
        for s in strategies:
            st.markdown(f'<div class="calm-card">{s["text"]}</div>', unsafe_allow_html=True)
        st.markdown('<p class="muted">Try one, if you can. There\'s no rush.</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="muted">No coping strategies saved yet. Try a slow walk, cold water on your face, or calling someone below.</p>', unsafe_allow_html=True)
    if st.button("Continue →", use_container_width=True):
        st.session_state.rn_step = 3
        st.rerun()

elif step == 3:
    st.markdown("### Here's why you're staying, and where you're headed.")
    reasons = db.list_reasons(conn)
    goals = db.list_goals(conn)
    for r in reasons:
        st.markdown(f'<div class="calm-card">\U0001F49B {r["text"]}</div>', unsafe_allow_html=True)
    for g in goals:
        st.markdown(f'<div class="calm-card">\U0001F331 {g["text"]}</div>', unsafe_allow_html=True)
    if not reasons and not goals:
        st.markdown('<p class="muted">Nothing saved here yet. That\'s okay — you can still keep going.</p>', unsafe_allow_html=True)
    if meta["future_message"]:
        st.markdown("##### A message you left for yourself:")
        st.markdown(f'<div class="calm-card"><i>{meta["future_message"]}</i></div>', unsafe_allow_html=True)
    if st.button("Continue →", use_container_width=True):
        st.session_state.rn_step = 4
        st.rerun()

elif step == 4:
    st.markdown("### You don't have to do this part alone.")
    contacts = db.list_contacts(conn)
    if contacts:
        for c in contacts:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f'<div class="calm-card"><b>{c["name"]}</b><br><span class="muted">{c["relationship"]}</span></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<a href="tel:{c["phone"]}"><button style="width:100%; padding:0.6rem; border-radius:10px; border:none; background:#7c8fd6; color:white; font-weight:700;">Call</button></a>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="muted">No trusted contacts saved yet. Please use the numbers below.</p>', unsafe_allow_html=True)
    st.markdown("##### Or a crisis line, right now:")
    st.markdown('<a href="tel:131114"><button style="width:100%; padding:0.8rem; border-radius:14px; border:none; background:#e35d5d; color:white; font-weight:700; font-size:1.05rem;">Call Lifeline — 13 11 14</button></a>', unsafe_allow_html=True)
    st.write("")
    if st.button("I've reached out / I'm okay to continue →", use_container_width=True):
        st.session_state.rn_step = 5
        st.rerun()

elif step == 5:
    st.markdown("### You made it through this round.")
    st.markdown('<p class="muted">That counts for something. It really does. This page will be here again, exactly the same, whenever you need it.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Go through it again", use_container_width=True):
            st.session_state.rn_step = 0
            st.rerun()
    with col2:
        if st.button("Back to Home", use_container_width=True):
            st.session_state.rn_step = 0
            st.switch_page("app.py")
