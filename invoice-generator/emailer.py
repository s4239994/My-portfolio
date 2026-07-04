import json
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "email_config.json"


def load_email_config() -> dict:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            "email_config.json not found. Copy email_config.example.json to "
            "email_config.json and fill in your Gmail address and app password."
        )
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


def send_invoice_email(to_email: str, client_name: str, invoice_number: str, pdf_path: Path, business_name: str) -> None:
    config = load_email_config()

    message = EmailMessage()
    message["Subject"] = f"Invoice {invoice_number} from {business_name}"
    message["From"] = config["gmail_address"]
    message["To"] = to_email
    message.set_content(
        f"Hi {client_name},\n\n"
        f"Please find attached invoice {invoice_number}.\n\n"
        f"Thanks for your business,\n{business_name}"
    )

    with open(pdf_path, "rb") as f:
        message.add_attachment(f.read(), maintype="application", subtype="pdf", filename=pdf_path.name)

    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls(context=context)
        server.login(config["gmail_address"], config["gmail_app_password"])
        server.send_message(message)
