import streamlit as st

from common import audio, style

st.set_page_config(page_title="Breathe — Anchor", page_icon="\U0001F32C️", layout="centered")
style.inject_base_css()

st.markdown("### Just breathe for a bit.")
st.markdown('<p class="muted">No plan needed for this one. Anytime you want a minute, come here.</p>', unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align:center; margin: 2rem 0;">
        <div style="display:inline-block; width:160px; height:160px; border-radius:50%;
                    background: radial-gradient(circle, #b9c6ef, #7c8fd6);
                    animation: breathe2 9s ease-in-out infinite;"></div>
    </div>
    <style>
    @keyframes breathe2 {
        0%, 100% { transform: scale(0.7); opacity: 0.55; }
        50% { transform: scale(1.2); opacity: 1; }
    }
    </style>
    <p class="muted" style="text-align:center;">Breathe in as it grows, out as it shrinks. Try it for a few rounds.</p>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.markdown("##### Want a soft sound to breathe along with?")
st.markdown(
    '<p class="muted" style="font-size:0.85rem;">Just a gentle generated tone -- not any special '
    "brainwave science, just something soft to focus on. Your own music works just as well, if you'd rather use that.</p>",
    unsafe_allow_html=True,
)
if st.button("Generate a soft ambient tone"):
    with st.spinner("Generating..."):
        tone = audio.generate_ambient_tone(duration_sec=45)
    st.audio(tone, format="audio/wav")
