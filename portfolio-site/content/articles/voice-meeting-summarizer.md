Title: Voice-to-Text Meeting Summarizer
Date: 2026-07-03
Tags: python, ai, streamlit
Summary: Upload a meeting recording and get a transcript, summary, and action items -- fully offline, for free.

A Streamlit web app that turns a recorded meeting into a clean transcript, a
short summary, and a checklist of action items -- with automatic translation
if someone spoke a different language.

## How it works

- **Whisper** (via `faster-whisper`) transcribes the audio locally, no cloud API required
- **DistilBART** writes the summary, **Flan-T5** pulls out the action items
- Everything runs offline after the first model download -- no accounts, no per-use cost
- Processing only ever happens on an uploaded *recording* of a finished meeting, never a live
  microphone feed, so there's no risk of it interrupting an actual call

## Stack

Python, Streamlit, faster-whisper, Hugging Face Transformers, deep-translator.
