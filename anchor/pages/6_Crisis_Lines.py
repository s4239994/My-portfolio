import streamlit as st

from common import style

st.set_page_config(page_title="Crisis Lines — Anchor", page_icon="\U0001F6A8", layout="centered")
style.inject_base_css()

st.markdown("### Real people, right now.")
st.markdown('<p class="muted">These are staffed by trained people, not an app. Calling one isn\'t giving up — it\'s the strongest move available.</p>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="crisis-line-card">
    <b>Immediate danger:</b> Call <b>000</b> (Australia)
    </div>
    <div class="crisis-line-card">
    <b>Lifeline Australia</b> — 24/7 crisis support<br>
    Call <b>13 11 14</b> · Text <b>0477 13 11 14</b>
    </div>
    <div class="crisis-line-card">
    <b>Beyond Blue</b> — anxiety, depression, suicide prevention<br>
    Call <b>1300 22 4636</b>
    </div>
    <div class="crisis-line-card">
    <b>Kids Helpline</b> — for under-25s<br>
    Call <b>1800 55 1800</b>
    </div>
    <div class="crisis-line-card">
    <b>13YARN</b> — for Aboriginal and Torres Strait Islander peoples<br>
    Call <b>13 92 76</b>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("##### Outside Australia?")
st.markdown(
    """
    <div class="calm-card">
    <b>United States:</b> 988 Suicide & Crisis Lifeline — call or text 988<br>
    <b>United Kingdom:</b> Samaritans — call 116 123<br>
    <b>Elsewhere:</b> search "[your country] crisis line" or "[your country] suicide prevention" —
    most countries have a free, anonymous number like this.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.markdown('<a href="tel:131114"><button style="width:100%; padding:0.9rem; border-radius:16px; border:none; background:#e35d5d; color:white; font-weight:700; font-size:1.1rem;">Call Lifeline now — 13 11 14</button></a>', unsafe_allow_html=True)
