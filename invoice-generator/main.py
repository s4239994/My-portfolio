import sys
from datetime import date, timedelta

from activities import build_line_items, load_unbilled_activities, mark_billed
from billing import calculate_totals
from clients import load_clients
from emailer import send_invoice_email
from invoices import has_overdue_invoice, load_records, next_invoice_number, record_invoice
from pdf_invoice import generate_invoice_pdf
from settings import load_settings


def main(send_emails: bool = False) -> None:
    settings = load_settings()
    clients = load_clients()
    unbilled_by_client = load_unbilled_activities()
    records = load_records()

    if not unbilled_by_client:
        print("No unbilled activity found. Nothing to invoice.")
        return

    for client_id, activity_rows in unbilled_by_client.items():
        client = clients.get(client_id)
        if not client:
            print(f"Skipping unknown client_id '{client_id}' -- add them to clients.csv first.")
            continue

        line_items = build_line_items(activity_rows)
        late_fee = settings["late_fee_flat_amount"] if has_overdue_invoice(records, client_id) else 0.0
        totals = calculate_totals(line_items, client["discount_percent"], settings["tax_rate_percent"], late_fee)

        invoice_number = next_invoice_number(records)
        issue_date = date.today()
        due_date = issue_date + timedelta(days=client["payment_terms_days"])

        pdf_path = generate_invoice_pdf(
            invoice_number=invoice_number,
            business=settings,
            client=client,
            line_items=line_items,
            totals=totals,
            issue_date=issue_date,
            due_date=due_date,
            currency=settings["currency_symbol"],
            tax_label=settings["tax_label"],
            applied_late_fee=late_fee,
        )

        record_invoice(records, invoice_number, client_id, issue_date, due_date, totals["total"])
        mark_billed([idx for idx, _ in activity_rows])

        print(f"Generated {pdf_path.name} for {client['name']} -- total {settings['currency_symbol']}{totals['total']:.2f}")

        if send_emails:
            try:
                send_invoice_email(client["email"], client["name"], invoice_number, pdf_path, settings["business_name"])
                print(f"  Emailed to {client['email']}")
            except Exception as exc:
                print(f"  Could not send email: {exc}")


if __name__ == "__main__":
    main(send_emails="--email" in sys.argv)
