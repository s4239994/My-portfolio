import json
import re
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "data" / "signals_config.json"
SALARY_PATTERN = re.compile(r"\$\s?\d{2,3}(,\d{3})?(k\b|,000)?")


def load_signals_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def score_vibe(text: str, config: dict) -> dict:
    """Deterministic, free vibe score based on buzzword/red-flag phrase
    matching -- no API call needed. Returns matched phrases so the AI step
    (if used) can quote them directly instead of guessing."""
    text_lower = text.lower()
    weights = config["weights"]

    matched_red = [p for p in config["red_flag_phrases"] if p in text_lower]
    matched_green = [p for p in config["green_flag_phrases"] if p in text_lower]
    has_salary_number = bool(SALARY_PATTERN.search(text_lower))

    score = weights["base"]
    score += len(matched_green) * weights["green_flag"]
    score -= len(matched_red) * weights["red_flag"]
    if has_salary_number:
        score += weights["salary_number_bonus"]
    score = max(0, min(100, score))

    return {
        "score": score,
        "matched_red": matched_red,
        "matched_green": matched_green,
        "has_salary_number": has_salary_number,
    }
