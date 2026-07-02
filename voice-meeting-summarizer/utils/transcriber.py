from faster_whisper import WhisperModel


def load_model(model_size: str = "base") -> WhisperModel:
    return WhisperModel(model_size, device="cpu", compute_type="int8")


def transcribe_audio(model: WhisperModel, audio_path: str, translate_to_english: bool = False) -> dict:
    """Transcribe (or translate-to-English) an audio file.

    Returns the detected language, the full transcript text, and per-segment timestamps.
    """
    task = "translate" if translate_to_english else "transcribe"
    segments_iter, info = model.transcribe(audio_path, task=task, vad_filter=True)

    segments = []
    text_parts = []
    for segment in segments_iter:
        clean = segment.text.strip()
        if not clean:
            continue
        segments.append({"start": segment.start, "end": segment.end, "text": clean})
        text_parts.append(clean)

    return {
        "language": info.language,
        "language_probability": info.language_probability,
        "text": " ".join(text_parts).strip(),
        "segments": segments,
    }
