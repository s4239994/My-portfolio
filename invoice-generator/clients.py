import csv
from pathlib import Path

CLIENTS_FILE = Path(__file__).parent / "data" / "clients.csv"
REQUIRED_FIELDS = ["client_id", "name", "email", "payment_terms_days"]


def load_clients() -> dict:
    """Read clients.csv and return {client_id: normalized client info}."""
    clients = {}
    with open(CLIENTS_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not all(row.get(field, "").strip() for field in REQUIRED_FIELDS):
                print(f"Skipping incomplete client row: {row}")
                continue

            client_id = row["client_id"].strip()
            clients[client_id] = {
                "client_id": client_id,
                "name": row["name"].strip(),
                "email": row["email"].strip().lower(),
                "address": row.get("address", "").strip(),
                "payment_terms_days": int(row["payment_terms_days"]),
                "discount_percent": float(row.get("discount_percent") or 0),
            }
    return clients
