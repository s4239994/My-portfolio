import streamlit as st

from common import db, style

st.set_page_config(page_title="My History — Anchor", page_icon="\U0001F4C8", layout="centered")
style.inject_base_css()

conn = db.get_connection()

st.markdown("### How you've been.")
st.markdown('<p class="muted">Just for you. Never used to predict anything -- only so you can look back and see: you\'ve felt this heavy before, and it passed.</p>', unsafe_allow_html=True)

st.write("")
st.markdown("##### Log how today feels")
mood = st.slider("Mood", 1, 5, 3, label_visibility="collapsed",
                  help="1 = really hard, 5 = genuinely good")
note = st.text_input("Anything you want to note (optional)")
if st.button("Log today"):
    db.log_mood(conn, mood, note)
    st.success("Logged.")

st.write("")
history = db.list_mood_log(conn)
if history:
    st.markdown("##### Your last check-ins")
    labels = {1: "\U0001F62B really hard", 2: "\U0001F614 hard", 3: "\U0001F610 okay", 4: "\U0001F642 good", 5: "\U0001F60A really good"}
    for h in history:
        note_html = f' -- <span class="muted">{h["note"]}</span>' if h["note"] else ""
        st.markdown(
            f'<div class="calm-card">{labels.get(h["mood"], "")}{note_html}'
            f'<br><span class="muted" style="font-size:0.8rem;">{h["logged_at"][:16].replace("T", " ")}</span></div>',
            unsafe_allow_html=True,
        )
else:
    st.markdown('<p class="muted">No check-ins yet.</p>', unsafe_allow_html=True)
