import json
from datetime import datetime
from pathlib import Path
from typing import Optional

TICKETS_FILE = Path(__file__).parent / "data" / "handoff_tickets.json"

FRUSTRATION_KEYWORDS = [
    "talk to a human",
    "speak to a person",
    "real person",
    "manager",
    "agent please",
]


def keyword_triggered(message: str) -> bool:
    lowered = message.lower()
    return any(keyword in lowered for keyword in FRUSTRATION_KEYWORDS)


def log_handoff(session_id: str, customer_id: Optional[str], reason: str, transcript: list) -> None:
    tickets = []
    if TICKETS_FILE.exists():
        with open(TICKETS_FILE, encoding="utf-8") as f:
            tickets = json.load(f)

    tickets.append({
        "session_id": session_id,
        "customer_id": customer_id,
        "reason": reason,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "transcript": transcript,
    })

    with open(TICKETS_FILE, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2)
