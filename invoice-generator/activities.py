import csv
from pathlib import Path

ACTIVITIES_FILE = Path(__file__).parent / "data" / "activities.csv"
FIELDNAMES = ["client_id", "date", "description", "quantity", "unit_price", "billed"]


def _read_all_rows() -> list:
    with open(ACTIVITIES_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_unbilled_activities() -> dict:
    """Return {client_id: [(row_index, row_dict), ...]} for rows not yet billed."""
    by_client = {}
    for idx, row in enumerate(_read_all_rows()):
        if row.get("billed", "").strip().lower() == "yes":
            continue
        by_client.setdefault(row["client_id"].strip(), []).append((idx, row))
    return by_client


def mark_billed(row_indexes: list) -> None:
    """Flip 'billed' to yes for the given row positions and rewrite the file."""
    rows = _read_all_rows()
    for idx in row_indexes:
        rows[idx]["billed"] = "yes"

    with open(ACTIVITIES_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def build_line_items(activity_rows: list) -> list:
    """Turn raw activity rows into priced line items."""
    line_items = []
    for _, row in activity_rows:
        quantity = float(row["quantity"])
        unit_price = float(row["unit_price"])
        line_items.append({
            "date": row["date"],
            "description": row["description"],
            "quantity": quantity,
            "unit_price": unit_price,
            "amount": round(quantity * unit_price, 2),
        })
    return line_items
