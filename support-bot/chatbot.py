import uuid
from typing import Optional

from handoff import keyword_triggered, log_handoff
from llm import get_reply
from persona import build_system_prompt


class SupportConversation:
    """Channel-agnostic conversation engine -- the Streamlit app and the CLI
    channel both just call .send() on one of these."""

    def __init__(self, persona: dict, customer: Optional[dict] = None):
        self.session_id = str(uuid.uuid4())[:8]
        self.persona = persona
        self.customer = customer
        self.messages: list = []
        self.handed_off = False

    def send(self, user_message: str) -> dict:
        self.messages.append({"role": "user", "content": user_message})
        system_prompt = build_system_prompt(self.persona, self.customer)

        try:
            result = get_reply(system_prompt, self.messages)
            reply = result.reply
            sentiment = result.sentiment
            handoff_recommended = result.handoff_recommended
            handoff_reason = result.handoff_reason
        except Exception as exc:
            reply = "Sorry, I'm having trouble responding right now. Let me get a human to help you."
            sentiment = "neutral"
            handoff_recommended = True
            handoff_reason = f"AI service error: {exc}"

        self.messages.append({"role": "assistant", "content": reply})

        handoff_needed = handoff_recommended or keyword_triggered(user_message)
        if handoff_needed and not self.handed_off:
            self.handed_off = True
            log_handoff(
                self.session_id,
                self.customer["customer_id"] if self.customer else None,
                handoff_reason or "Customer requested a human agent.",
                self.messages,
            )

        return {
            "reply": reply,
            "sentiment": sentiment,
            "handoff_needed": handoff_needed,
            "handoff_reason": handoff_reason,
        }
