import json
from pathlib import Path

PERSONA_FILE = Path(__file__).parent / "config" / "persona.json"


def load_persona() -> dict:
    with open(PERSONA_FILE, encoding="utf-8") as f:
        return json.load(f)


def build_system_prompt(persona: dict, customer: dict | None) -> str:
    lines = [
        f"You are {persona['brand_name']}'s AI customer support assistant.",
        f"Tone: {persona['tone']}",
        persona["escalation_policy"],
        "",
        "Write a complete, helpful reply of 1-3 sentences that directly addresses what "
        "the customer just said -- never respond with just a greeting. Then classify "
        "the customer's most recent message by sentiment, and decide whether this "
        "conversation should be handed off to a human agent.",
    ]

    if customer:
        lines += [
            "",
            "The customer has consented to you viewing their account details:",
            f"- Name: {customer['name']}",
            f"- Plan: {customer['plan_tier']}",
            f"- Recent order: {customer['recent_order']} (status: {customer['order_status']})",
            "Use these details naturally to personalize your response when relevant.",
        ]
    else:
        lines += [
            "",
            "The customer has not shared their account details, so answer generally "
            "and don't invent specifics about their account or orders.",
        ]

    return "\n".join(lines)
