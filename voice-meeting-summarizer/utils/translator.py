from deep_translator import GoogleTranslator

MAX_CHUNK_CHARS = 4500  # keeps requests under the free translation service's limit

SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Russian": "ru",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
}


def _split_into_chunks(text: str, max_chars: int) -> list[str]:
    words = text.split(" ")
    chunks, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 > max_chars:
            chunks.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        chunks.append(current)
    return chunks


def translate_text(text: str, target_language_code: str) -> str:
    """Translate text into the target language. Needs an internet connection."""
    text = text.strip()
    if not text:
        return text

    translator = GoogleTranslator(source="auto", target=target_language_code)

    if len(text) <= MAX_CHUNK_CHARS:
        return translator.translate(text)

    chunks = _split_into_chunks(text, MAX_CHUNK_CHARS)
    return " ".join(translator.translate(chunk) for chunk in chunks)
