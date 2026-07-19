import streamlit as st

from common import db, particles, style

st.set_page_config(page_title="Reasons — Anchor", page_icon="\U0001F49B", layout="centered")
style.inject_base_css()

conn = db.get_connection()

st.markdown("### Your reasons.")
st.markdown('<p class="muted">Worth reading on an ordinary day too, not just a hard one -- that\'s what makes them easy to find later.</p>', unsafe_allow_html=True)

particles.render_scene("stars", "#ffffff", intensity=0.6, height=180)

reasons = db.list_reasons(conn)
goals = db.list_goals(conn)

if reasons:
    st.markdown("##### Why you're staying")
    for r in reasons:
        style.icon_card("\U0001F49B", r["text"], accent="#e39ec4")

if goals:
    st.write("")
    st.markdown("##### Where you're headed")
    for g in goals:
        style.icon_card("\U0001F331", g["text"], accent="#6ec6b0")

if not reasons and not goals:
    st.markdown('<p class="muted">Nothing here yet.</p>', unsafe_allow_html=True)
    if st.button("Add some in Build My Plan →"):
        st.session_state.plan_step = 4
        st.switch_page("pages/1_Build_My_Plan.py")

meta = db.get_meta(conn)
if meta["future_message"]:
    st.write("")
    st.markdown("##### A message you left for yourself")
    style.icon_card("\U0001F4AC", f'<i>{meta["future_message"]}</i>', accent="#a98ede")
