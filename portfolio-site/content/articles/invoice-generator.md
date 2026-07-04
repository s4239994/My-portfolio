Title: Automated IT Service Invoice Generator
Date: 2026-07-04
Tags: python, automation, pdf
Summary: Turns billable work into professional PDF invoices, with tax, discounts, and late fees calculated automatically.

A Python tool that takes plain CSV records of clients and billable work and
turns them into polished PDF invoices -- with automatic tax, discount, and
late-fee logic, and optional one-click emailing to the client.

## How it works

- Clients and billable activities live in simple, editable CSV files
- Line items are generated dynamically from whatever unbilled work exists
- Totals, discounts, and tax are calculated automatically per client
- Every invoice is recorded with its due date; if a client has an unpaid,
  overdue invoice, the next one automatically adds a late fee
- PDFs are generated with `fpdf2` and can be emailed directly via Gmail

## Stack

Python, fpdf2, smtplib.
