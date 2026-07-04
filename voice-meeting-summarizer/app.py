import os
import tempfile

import streamlit as st

from utils.summarizer import (
    extract_action_items,
    load_action_extractor,
    load_summarizer,
    summarize_transcript,
)
from utils.transcriber import load_model, transcribe_audio
from utils.translator import SUPPORTED_LANGUAGES, translate_text

st.set_page_config(
    page_title="Voice-to-Text Meeting Summarizer",
    page_icon="🎙️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .terminal-tag {
        font-family: "Consolas", "SFMono-Regular", Menlo, monospace;
        color: #39FF88;
        opacity: 0.85;
        letter-spacing: 2px;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="terminal-tag">&gt; GET SET GO</p>', unsafe_allow_html=True)
st.title("🎙️ Voice-to-Text Meeting Summarizer")
st.caption(
    "Upload a meeting recording. Get a clean transcript, a summary, and action items — "
    "automatically, running on your own computer, for free."
)

with st.sidebar:
    st.header("Settings")
    model_size = st.selectbox(
        "Transcription quality",
        options=["tiny", "base", "small"],
        index=1,
        help="Bigger models are more accurate but slower. 'base' is a good default.",
    )
    auto_translate_english = st.checkbox(
        "Someone spoke in another language? Auto-translate their speech to English",
        value=False,
        help="Handled by the same offline speech model — no internet needed for this.",
    )
    target_language_label = st.selectbox(
        "Also translate the final summary into...",
        options=["Keep as-is"] + list(SUPPORTED_LANGUAGES.keys()),
        index=0,
        help="This one step needs an internet connection. Everything else works offline.",
    )
    st.divider()
    st.caption(
        "First run only: the app downloads a few free AI models (about 2-3 GB total). "
        "After that, transcription and summarizing work fully offline."
    )

uploaded_file = st.file_uploader(
    "Upload your meeting recording",
    type=["wav", "mp3", "m4a", "mp4", "ogg", "flac", "webm"],
)

process_clicked = st.button("Summarize Meeting", type="primary", disabled=uploaded_file is None)


@st.cache_resource(show_spinner=False)
def get_whisper_model(size: str):
    return load_model(size)


@st.cache_resource(show_spinner=False)
def get_summarizer_model():
    return load_summarizer()


@st.cache_resource(show_spinner=False)
def get_action_model():
    return load_action_extractor()


if process_clicked and uploaded_file is not None:
    suffix = os.path.splitext(uploaded_file.name)[1] or ".wav"
    tmp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name

        with st.status("Working on your meeting...", expanded=True) as status:
            status.write("Loading the speech-to-text model (first time only downloads it)...")
            whisper_model = get_whisper_model(model_size)

            status.write("Listening and transcribing your audio...")
            result = transcribe_audio(whisper_model, tmp_path, translate_to_english=auto_translate_english)

            if not result["text"]:
                status.update(label="Couldn't find any speech", state="error", expanded=True)
                st.warning(
                    "No speech was detected in this file. Please check the recording "
                    "isn't silent or corrupted, and try again."
                )
                st.stop()

            status.write("Loading the summarization model (first time only downloads it)...")
            summarizer = get_summarizer_model()

            status.write("Writing the summary...")
            summary = summarize_transcript(summarizer, result["text"])

            status.write("Loading the action-item model (first time only downloads it)...")
            action_model = get_action_model()

            status.write("Finding action items...")
            action_items = extract_action_items(action_model, result["text"])

            translated_summary = None
            if target_language_label != "Keep as-is":
                status.write(f"Translating summary into {target_language_label}...")
                try:
                    translated_summary = translate_text(summary, SUPPORTED_LANGUAGES[target_language_label])
                except Exception:
                    status.write(
                        "Translation needs an internet connection — skipped this step, "
                        "everything else is ready below."
                    )

            status.update(label="Done!", state="complete", expanded=False)

        st.success(
            f"Detected language: **{result['language']}** "
            f"(confidence {result['language_probability']:.0%})"
        )

        tab_summary, tab_actions, tab_transcript = st.tabs(
            ["📋 Summary", "✅ Action Items", "📝 Full Transcript"]
        )

        with tab_summary:
            st.write(summary or "_No summary could be generated from this recording._")
            if translated_summary:
                st.divider()
                st.markdown(f"**Translated into {target_language_label}:**")
                st.write(translated_summary)

        with tab_actions:
            if action_items:
                for idx, item in enumerate(action_items):
                    st.checkbox(item, key=f"action_{idx}", value=False)
            else:
                st.write("No specific action items were found in this meeting.")

        with tab_transcript:
            st.text_area("Transcript", result["text"], height=300)

        action_lines = [f"- {item}" for item in action_items] if action_items else ["(none)"]
        report_lines = [
            "MEETING SUMMARY",
            "=" * 40,
            summary or "(no summary)",
            "",
            "ACTION ITEMS",
            "=" * 40,
            *action_lines,
            "",
            "FULL TRANSCRIPT",
            "=" * 40,
            result["text"],
        ]
        st.download_button(
            "Download report as text file",
            data="\n".join(report_lines),
            file_name="meeting_summary.txt",
            mime="text/plain",
        )

    except Exception as exc:
        st.error(
            "Something went wrong while processing this file. Try a different audio "
            "file, or a shorter recording, and try again.\n\n"
            f"Details: {exc}"
        )
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
