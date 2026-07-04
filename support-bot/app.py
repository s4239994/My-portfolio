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
ACCENT_BLUE = "#4da6ff"

st.markdown(
    """
    <style>
    .terminal-tag {
        font-family: "Consolas", "SFMono-Regular", Menlo, monospace;
        color: #39FF88;
        opacity: 0.85;
        letter-spacing: 2px;
        font-size: 0.8rem;
    }
    .hero-card {
        background: linear-gradient(135deg, rgba(77,166,255,0.10), rgba(57,255,136,0.02));
        border: 1px solid #2a2b2f;
        border-left: 4px solid #4da6ff;
        border-radius: 12px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.75rem;
    }
    .hero-title { margin: 0.3rem 0 0.4rem; font-size: 1.9rem; }
    .hero-caption { color: #9a9a9a; margin: 0; font-size: 0.95rem; }
    .sentiment-tag {
        display: inline-block; padding: 2px 10px; margin-top: 4px;
        border-radius: 999px; font-family: monospace; font-size: 0.75rem;
    }
    .agent-card {
        background: #17181b; border: 1px solid #2a2b2f; border-radius: 10px;
        padding: 0.9rem 1rem; margin-bottom: 1rem;
    }
    .agent-status { color: #39FF88; font-size: 0.8rem; font-family: monospace; }
    .customer-card {
        background: #17181b; border: 1px solid #2a2b2f; border-radius: 10px;
        padding: 0.8rem 1rem; margin-top: 0.75rem; font-size: 0.85rem;
    }
    .customer-card b { color: #4da6ff; }
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

st.markdown(
    f"""
    <div class="hero-card">
        <p class="terminal-tag">&gt; VIBE STATE: ACTIVE ENGAGEMENT</p>
        <p class="hero-title">💬 {persona['brand_name']}</p>
        <p class="hero-caption">AI-powered customer support -- with sentiment detection
        and human hand-off.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        f"""
        <div class="agent-card">
            <b>{persona['brand_name']}</b><br>
            <span class="agent-status">&#9679; Online -- responding via local AI</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Your account")
    consent = st.checkbox("Let the assistant look up my account details", value=False)
    customer_id = None
    if consent:
        choice = st.selectbox("Pick a demo account", ["None"] + list(customers.keys()))
        customer_id = None if choice == "None" else choice

    if customer_id:
        c = customers[customer_id]
        st.markdown(
            f"""
            <div class="customer-card">
                <b>{c['name']}</b><br>
                Plan: {c['plan_tier']}<br>
                Recent order: {c['recent_order']} ({c['order_status']})
            </div>
            """,
            unsafe_allow_html=True,
        )

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
