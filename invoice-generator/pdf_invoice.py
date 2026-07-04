from pathlib import Path

from fpdf import FPDF

OUTPUT_DIR = Path(__file__).parent / "generated_invoices"
ACCENT_COLOR = (36, 199, 118)  # a darker variant of the brand green (#39FF88) -- the
# pure neon shade has poor contrast against white text on a PDF's white background


class InvoicePDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*ACCENT_COLOR)
        self.cell(0, 10, "> INVOICE", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, "Generated automatically -- built with a bit of vibe.", align="C")


def generate_invoice_pdf(invoice_number, business, client, line_items, totals,
                          issue_date, due_date, currency, tax_label, applied_late_fee):
    OUTPUT_DIR.mkdir(exist_ok=True)

    pdf = InvoicePDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, business["business_name"], new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Invoice #: {invoice_number}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Issue date: {issue_date.isoformat()}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Due date: {due_date.isoformat()}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "Bill to:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, client["name"], new_x="LMARGIN", new_y="NEXT")
    if client["address"]:
        pdf.cell(0, 6, client["address"], new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, client["email"], new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(*ACCENT_COLOR)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(30, 8, "Date", border=1, fill=True)
    pdf.cell(80, 8, "Description", border=1, fill=True)
    pdf.cell(25, 8, "Qty", border=1, fill=True, align="R")
    pdf.cell(25, 8, "Rate", border=1, fill=True, align="R")
    pdf.cell(30, 8, "Amount", border=1, fill=True, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 10)
    for item in line_items:
        pdf.cell(30, 8, item["date"], border=1)
        pdf.cell(80, 8, item["description"], border=1)
        pdf.cell(25, 8, f'{item["quantity"]:g}', border=1, align="R")
        pdf.cell(25, 8, f'{currency}{item["unit_price"]:.2f}', border=1, align="R")
        pdf.cell(30, 8, f'{currency}{item["amount"]:.2f}', border=1, align="R", new_x="LMARGIN", new_y="NEXT")

    if applied_late_fee:
        pdf.cell(160, 8, "Late fee (previous invoice overdue)", border=1)
        pdf.cell(30, 8, f'{currency}{applied_late_fee:.2f}', border=1, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    pdf.set_font("Helvetica", "", 10)
    _totals_row(pdf, "Subtotal", totals["subtotal"], currency)
    if totals["discount_amount"]:
        _totals_row(pdf, "Discount", -totals["discount_amount"], currency)
    _totals_row(pdf, tax_label, totals["tax_amount"], currency)
    pdf.set_font("Helvetica", "B", 11)
    _totals_row(pdf, "Total due", totals["total"], currency)

    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 6, business["footer_note"])

    output_path = OUTPUT_DIR / f"{invoice_number}.pdf"
    pdf.output(str(output_path))
    return output_path


def _totals_row(pdf, label, amount, currency):
    pdf.cell(160, 7, label, align="R")
    pdf.cell(30, 7, f"{currency}{amount:.2f}", align="R", new_x="LMARGIN", new_y="NEXT")
