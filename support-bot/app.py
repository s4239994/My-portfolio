import streamlit as st

from chatbot import SupportConversation
from persona import load_persona
from profiles import load_customers

st.set_page_config(page_title="Customer Support Chat", page_icon="💬", layout="wide")

SENTIMENT_COLORS = {
    "positive": "#39FF88",
    "neutral": "#9a9a9a",
    "frustrated": "#f5c542",
    "angry": "#ff6666",
}

st.markdown(
    """
    <style>
    .terminal-tag {
        font-family: "Consolas", "SFMono-Regular", Menlo, monospace;
        color: #39FF88;
        opacity: 0.85;
        letter-spacing: 2px;
        font-size: 0.85rem;
    }
    .sentiment-tag {
        display: inline-block; padding: 2px 10px; margin-top: 4px;
        border-radius: 999px; font-family: monospace; font-size: 0.75rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def sentiment_badge(sentiment: str) -> str:
    color = SENTIMENT_COLORS.get(sentiment, "#9a9a9a")
    return (
        f'<span class="sentiment-tag" style="background:{color}22; color:{color}; '
        f'border:1px solid {color};">{sentiment}</span>'
    )


persona = load_persona()
customers = load_customers()

st.markdown('<p class="terminal-tag">&gt; GET SET GO</p>', unsafe_allow_html=True)
st.title(f"💬 {persona['brand_name']}")
st.caption("AI-powered customer support -- with sentiment detection and human handoff.")

with st.sidebar:
    st.header("Your account")
    consent = st.checkbox("Let the assistant look up my account details", value=False)
    customer_id = None
    if consent:
        choice = st.selectbox("Pick a demo account", ["None"] + list(customers.keys()))
        customer_id = None if choice == "None" else choice

if "conversation" not in st.session_state or st.session_state.get("customer_id") != customer_id:
    customer = customers.get(customer_id) if customer_id else None
    st.session_state.conversation = SupportConversation(persona, customer)
    st.session_state.customer_id = customer_id
    st.session_state.chat_log = [{"role": "assistant", "content": persona["greeting"], "sentiment": None}]

conversation: SupportConversation = st.session_state.conversation

for entry in st.session_state.chat_log:
    with st.chat_message(entry["role"]):
        st.write(entry["content"])
        if entry.get("sentiment"):
            st.markdown(sentiment_badge(entry["sentiment"]), unsafe_allow_html=True)

if conversation.handed_off:
    st.warning("This conversation has been flagged for a human agent. They'll follow up shortly.")

user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.chat_log.append({"role": "user", "content": user_input, "sentiment": None})

    with st.spinner("Thinking..."):
        result = conversation.send(user_input)

    st.session_state.chat_log.append({
        "role": "assistant",
        "content": result["reply"],
        "sentiment": result["sentiment"],
    })
    st.rerun()
