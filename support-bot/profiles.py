import csv
from pathlib import Path

CUSTOMERS_FILE = Path(__file__).parent / "data" / "customers.csv"


def load_customers() -> dict:
    """Return {customer_id: row} -- only looked up when the customer consents."""
    customers = {}
    with open(CUSTOMERS_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            customers[row["customer_id"]] = row
    return customers
