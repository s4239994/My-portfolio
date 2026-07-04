import re
from pathlib import Path

import pdfplumber
from docx import Document


def extract_text(file_path: str) -> str:
    """Pull raw text out of a PDF, DOCX, or plain text file."""
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        raw = _extract_pdf(file_path)
    elif suffix == ".docx":
        raw = _extract_docx(file_path)
    else:
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            raw = f.read()

    return clean_text(raw)


def _extract_pdf(file_path: str) -> str:
    parts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                parts.append(text)
    return "\n".join(parts)


def _extract_docx(file_path: str) -> str:
    document = Document(file_path)
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
