from datetime import datetime

import streamlit as st

from common import db, particles, style

st.set_page_config(page_title="Anchor", page_icon="⚓", layout="centered")
style.inject_base_css()

conn = db.get_connection()
meta = db.get_meta(conn)

hour = datetime.now().hour
greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"

st.markdown(f"### {greeting} \U0001F44B")
st.markdown(
    '<p class="muted">This is your space. Nothing here is being watched, tracked, or sent anywhere. '
    "It's just yours.</p>",
    unsafe_allow_html=True,
)

st.write("")
st.markdown('<div class="big-button-wrap">', unsafe_allow_html=True)
if st.button("\U0001F198 I need this right now", use_container_width=True):
    st.switch_page("pages/2_Right_Now.py")
st.markdown("</div>", unsafe_allow_html=True)
st.write("")

if meta["metaphor"]:
    m = db.METAPHORS[meta["metaphor"]]
    st.markdown(
        f'<p class="muted" style="text-align:center;">Right now, things feel steady. Your plan is ready if you need it.</p>',
        unsafe_allow_html=True,
    )
    particles.render_scene(meta["metaphor"], m["color"], intensity=0.15, height=220)
else:
    st.markdown(
        """
        <div class="calm-card">
            <b>You haven't built your plan yet.</b>
            <p class="muted" style="margin-top:0.4rem;">
            It only takes a few minutes, and it means everything you need is ready
            <em>before</em> you're having a hard time, not something you have to
            figure out in the moment.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Build my plan →"):
        st.switch_page("pages/1_Build_My_Plan.py")

st.write("")
st.markdown("---")
st.markdown('<p class="muted" style="text-align:center; font-size:0.85rem;">'
            "Anchor isn't a replacement for professional support. If you're in immediate danger, "
            "call 000. Lifeline (Australia): 13 11 14, anytime.</p>", unsafe_allow_html=True)
