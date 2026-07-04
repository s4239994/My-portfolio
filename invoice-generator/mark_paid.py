import sys

from invoices import load_records, save_records


def mark_paid(invoice_number: str) -> None:
    records = load_records()
    for record in records:
        if record["invoice_number"] == invoice_number:
            record["paid"] = True
            save_records(records)
            print(f"Marked {invoice_number} as paid.")
            return
    print(f"Invoice {invoice_number} not found.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mark_paid.py INV-0001")
    else:
        mark_paid(sys.argv[1])
