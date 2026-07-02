# Voice-to-Text Meeting Summarizer

Upload a recorded meeting and get back a transcript, a summary, and a list of action items —
automatically translating other languages if you need it to. Runs entirely on your own
computer. No accounts, no API keys, no payment.

## How it works

1. You record your meeting normally (Zoom/Teams/Google Meet's own "record" button, or a
   phone voice recorder — anything that saves an audio file).
2. After the meeting, you upload that audio file to this website.
3. The app turns the speech into text, translates it if needed, and gives you a clean
   summary and action items.

Because it only works on a file *after* your meeting ends (instead of trying to listen live),
it can never interrupt, freeze, or need a restart during your actual call.

## One-time setup

You only need to do this once.

### Step 1 — Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest
   Python for Windows.
2. Run the installer. **Important:** on the first screen, tick the box that says
   **"Add python.exe to PATH"** before clicking Install.

### Step 2 — Install the app's dependencies

Open a terminal (PowerShell) inside this `voice-meeting-summarizer` folder and run:

```
pip install -r requirements.txt
```

This downloads the free tools the app needs. It can take a few minutes the first time.

## Running the app

Every time you want to use it, open a terminal in this folder and run:

```
streamlit run app.py
```

A browser tab will open automatically with the website. Upload a recording, click
**"Summarize Meeting"**, and wait for the result.

> **Heads up:** the very first time you click "Summarize Meeting", the app downloads a few
> free AI models (about 2-3 GB total) — this needs internet and can take several minutes
> depending on your connection. Every time after that, it's fast and works fully offline
> (except the "translate summary into another language" option, which always needs internet).

## Features

- **Upload any common audio format** — mp3, wav, m4a, mp4, ogg, flac, webm.
- **Auto-translate speech to English** — if someone spoke in another language, tick the box
  in the sidebar and it converts their speech straight into English text.
- **Translate the summary into another language** — pick any language from the sidebar
  dropdown to also get the summary in that language.
- **Summary + action items** — a short summary of what was discussed, and a separate
  checklist of concrete tasks mentioned in the meeting.
- **Downloadable report** — save the transcript, summary, and action items as a single
  text file.

## Troubleshooting

- **Error mentioning a `.dll` file or `torch`/`c10.dll` when starting the app:** install the
  [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe),
  restart your terminal, and try again.

## Notes

- Longer recordings take longer to process — the app shows a live progress status so you
  know it's still working.
- The "Transcription quality" setting in the sidebar trades speed for accuracy: `tiny` is
  fastest, `small` is most accurate. `base` is a good default for most meetings.
