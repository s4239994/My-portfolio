import re

from transformers import pipeline

SUMMARY_MODEL = "sshleifer/distilbart-cnn-12-6"
ACTION_MODEL = "google/flan-t5-base"

SUMMARY_WORDS_PER_CHUNK = 700
ACTION_WORDS_PER_CHUNK = 350

ACTION_PROMPT = (
    "Read the meeting transcript below and list the concrete action items "
    "(tasks someone needs to do, with the owner and deadline if mentioned). "
    "Write each action item on its own line starting with a dash. "
    "If there are no clear action items, write exactly: None.\n\nTranscript:\n{chunk}"
)


def load_summarizer():
    return pipeline("summarization", model=SUMMARY_MODEL)


def load_action_extractor():
    return pipeline("text2text-generation", model=ACTION_MODEL)


def _chunk_text(text: str, words_per_chunk: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    return [" ".join(words[i:i + words_per_chunk]) for i in range(0, len(words), words_per_chunk)]


def summarize_transcript(summarizer, text: str) -> str:
    text = text.strip()
    if not text:
        return ""

    chunks = _chunk_text(text, SUMMARY_WORDS_PER_CHUNK)
    chunk_summaries = []
    for chunk in chunks:
        word_count = len(chunk.split())
        max_len = max(30, min(140, int(word_count * 0.6) or 30))
        min_len = max(10, int(max_len * 0.4))
        result = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False, truncation=True)
        chunk_summaries.append(result[0]["summary_text"].strip())

    combined = " ".join(chunk_summaries)
    if len(chunks) == 1:
        return combined

    final = summarizer(combined, max_length=150, min_length=40, do_sample=False, truncation=True)
    return final[0]["summary_text"].strip()


def extract_action_items(extractor, text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []

    chunks = _chunk_text(text, ACTION_WORDS_PER_CHUNK)
    raw_outputs = []
    for chunk in chunks:
        prompt = ACTION_PROMPT.format(chunk=chunk)
        result = extractor(prompt, max_new_tokens=200, do_sample=False, truncation=True)
        raw_outputs.append(result[0]["generated_text"].strip())

    items: list[str] = []
    seen: set[str] = set()
    for raw in raw_outputs:
        # the model sometimes echoes a label, or returns one run-on paragraph
        # instead of one item per line -- normalize both cases here.
        cleaned = re.sub(r"(?i)^action items?\s*:?\s*", "", raw).strip()
        if not cleaned or cleaned.lower().strip(". ") == "none":
            continue

        lines = [ln.strip(" -•\t") for ln in cleaned.split("\n") if ln.strip(" -•\t")]
        if len(lines) <= 1:
            lines = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if s.strip()]

        for line in lines:
            clean = line.strip(" -•\t.")
            if clean and clean.lower() not in seen:
                seen.add(clean.lower())
                items.append(clean)

    return items
