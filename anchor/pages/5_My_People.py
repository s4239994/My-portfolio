import streamlit as st

from common import db, style

st.set_page_config(page_title="My People — Anchor", page_icon="\U0001F4DE", layout="centered")
style.inject_base_css()

conn = db.get_connection()

st.markdown("### Your people.")
st.markdown('<p class="muted">One tap to call, or send a quick "having a hard day" message so you don\'t have to find the words.</p>', unsafe_allow_html=True)

contacts = db.list_contacts(conn)

if not contacts:
    st.markdown('<p class="muted">No one saved yet.</p>', unsafe_allow_html=True)
    if st.button("Add trusted people →"):
        st.session_state.plan_step = 3
        st.switch_page("pages/1_Build_My_Plan.py")
else:
    default_msg = "Hey, I'm having a hard day. Not urgent, but could you check in with me when you can?"
    for c in contacts:
        st.markdown(f'<div class="calm-card"><b>{c["name"]}</b><br><span class="muted">{c["relationship"]}</span></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f'<a href="tel:{c["phone"]}"><button style="width:100%; padding:0.6rem; border-radius:10px; border:none; background:#7c8fd6; color:white; font-weight:700;">Call</button></a>',
                unsafe_allow_html=True,
            )
        with col2:
            sms_href = f'sms:{c["phone"]}?body={default_msg.replace(" ", "%20")}'
            st.markdown(
                f'<a href="{sms_href}"><button style="width:100%; padding:0.6rem; border-radius:10px; border:none; background:#a9b8e8; color:white; font-weight:700;">Text: having a hard day</button></a>',
                unsafe_allow_html=True,
            )
        st.write("")
