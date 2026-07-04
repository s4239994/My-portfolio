import json
from datetime import date
from pathlib import Path

RECORDS_FILE = Path(__file__).parent / "data" / "invoice_records.json"


def load_records() -> list:
    if not RECORDS_FILE.exists():
        return []
    with open(RECORDS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_records(records: list) -> None:
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def next_invoice_number(records: list) -> str:
    return f"INV-{len(records) + 1:04d}"


def has_overdue_invoice(records: list, client_id: str) -> bool:
    """True if this client has an unpaid invoice whose due date has already passed."""
    today = date.today()
    for record in records:
        if record["client_id"] != client_id or record["paid"]:
            continue
        if date.fromisoformat(record["due_date"]) < today:
            return True
    return False


def record_invoice(records: list, invoice_number: str, client_id: str, issue_date: date, due_date: date, total: float) -> None:
    records.append({
        "invoice_number": invoice_number,
        "client_id": client_id,
        "issue_date": issue_date.isoformat(),
        "due_date": due_date.isoformat(),
        "total": total,
        "paid": False,
    })
    save_records(records)
