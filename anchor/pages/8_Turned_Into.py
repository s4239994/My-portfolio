import streamlit as st

from common import db, style

st.set_page_config(page_title="Turned Into — Anchor", page_icon="\U0001F331", layout="centered")
style.inject_base_css()

conn = db.get_connection()

st.markdown("### What this built in you.")
st.markdown(
    '<p class="muted">This page is for later -- once you\'re through a hard stretch, not while you\'re in one. '
    "Pain doesn't need to be useful to be valid, but if something did grow out of it, this is where it goes.</p>",
    unsafe_allow_html=True,
)

st.write("")
entry = st.text_area("What did you learn, or get stronger at, because of a hard time?", height=140,
                      placeholder="e.g. I learned I can actually ask for help instead of disappearing")
if st.button("Save this") and entry.strip():
    db.add_growth_reflection(conn, entry.strip())
    st.success("Saved.")
    st.rerun()

st.write("")
reflections = db.list_growth_reflections(conn)
if reflections:
    st.markdown("##### What you've written before")
    for r in reflections:
        st.markdown(
            f'<div class="calm-card">{r["text"]}<br>'
            f'<span class="muted" style="font-size:0.8rem;">{r["logged_at"][:10]}</span></div>',
            unsafe_allow_html=True,
        )
