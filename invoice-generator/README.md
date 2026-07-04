# Automated IT Service Invoice Generator

Turns billable work into professional PDF invoices automatically — with tax,
discounts, and late fees calculated for you, and optional auto-emailing to clients.

## How it works

1. You list your clients in `data/clients.csv`
2. You log billable work in `data/activities.csv` as it happens
3. Run the script — it groups unbilled work by client, calculates totals, and
   generates one PDF invoice per client in `generated_invoices/`
4. Optionally, it emails each invoice straight to the client

## Setup

```
pip install -r requirements.txt
```

## Adding clients

Edit `data/clients.csv`. Columns:

- `client_id` — any short code you make up (e.g. `C001`)
- `name`, `email`, `address`
- `payment_terms_days` — how many days they have to pay (e.g. `14`, `30`)
- `discount_percent` — a standing discount for this client, or `0`

## Logging billable work

Edit `data/activities.csv` whenever you do billable work. Columns:

- `client_id` — must match a client_id from clients.csv
- `date`, `description`
- `quantity` — hours worked, or units of whatever you're billing
- `unit_price` — your rate per unit
- `billed` — leave as `no`; the script sets this to `yes` once it's invoiced,
  so the same work never gets billed twice

## Generating invoices

```
python main.py
```

This generates a PDF for every client with unbilled activity. To also email
each invoice to the client:

```
python main.py --email
```

## Setting up auto-email (Gmail)

Gmail won't accept your normal password from a script — you need a free
16-character "App Password" instead:

1. Turn on 2-Step Verification on your Google account (if not already on):
   https://myaccount.google.com/signinoptions/two-step-verification
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Copy `email_config.example.json` to `email_config.json`
4. Fill in your Gmail address and the app password you just generated

`email_config.json` is never committed to git (it's in `.gitignore`) since it
holds a real credential.

## How late fees work

Every generated invoice is recorded in `data/invoice_records.json` with its
due date. When generating a new invoice for a client, the script checks: does
this client have any past invoice that's unpaid *and* past its due date? If
so, it automatically adds a late fee line item (amount set in `settings.json`).

## Marking an invoice as paid

```
python mark_paid.py INV-0001
```

This stops that invoice from ever triggering a late fee on future invoices.

## Adjusting settings

Edit `settings.json`:

- `business_name`, `footer_note` — shown on every invoice
- `tax_label`, `tax_rate_percent` — rename to GST/VAT/Sales Tax as needed
- `late_fee_flat_amount` — the flat fee added when an invoice is overdue
- `currency_symbol` — e.g. `$`, `£`, `€`
