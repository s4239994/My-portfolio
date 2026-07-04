def calculate_totals(line_items: list, discount_percent: float, tax_rate_percent: float, late_fee: float) -> dict:
    subtotal = round(sum(item["amount"] for item in line_items), 2)
    discount_amount = round(subtotal * discount_percent / 100, 2)
    taxable_amount = subtotal - discount_amount
    tax_amount = round(taxable_amount * tax_rate_percent / 100, 2)
    total = round(taxable_amount + tax_amount + late_fee, 2)

    return {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "tax_amount": tax_amount,
        "late_fee": late_fee,
        "total": total,
    }
