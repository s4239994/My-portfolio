# AI Resume Screening & Keyword Matcher

Upload a resume and paste a job description -- get a match score blending
exact skill overlap, semantically related skills, and years of experience,
plus an interactive concept graph showing how everything connects.

## What it does

- **Parses resumes** from PDF, DOCX, or plain text
- **Identifies skills** using a real NLP technique (a spaCy phrase matcher
  against a skills taxonomy) -- not just a fuzzy string search
- **Goes beyond exact matches** -- a local sentence-embedding model finds
  *related* skills (e.g. resume has "TensorFlow", job wants "Machine
  Learning") and gives partial credit for them
- **Builds a concept graph** connecting matched skills, resume-only skills,
  and gaps, with real relationships between them (e.g. React relates to
  JavaScript, Docker relates to Kubernetes)
- **Blends a match score** from skill coverage (70%) and years-of-experience
  match (30%)
- **Visual + sound feedback** on the result -- a pulsing green glow for a
  strong match, a subtle red shake for a weak one, and a distinct sound cue
  for each tier

## Setup

```
pip install -r requirements.txt
```

No accounts, no API keys -- everything (skill matching, semantic search)
runs locally. The first run downloads a small free sentence-embedding model
(~90 MB, one-time).

## Running it

```
streamlit run app.py
```

Upload or paste a resume on the left, paste a job description on the right,
and click **Screen Resume**.

## How it's organized

- **[data/skills_taxonomy.json](data/skills_taxonomy.json)** -- the list of
  recognized skills grouped by category, plus which skills are conceptually
  related to which (used for the concept graph's edges). Edit this file to
  add more skills or categories.
- **[extractor.py](extractor.py)** -- pulls text out of PDF/DOCX/TXT files
  and cleans it up.
- **[skills.py](skills.py)** -- the NLP core: a spaCy `PhraseMatcher` finds
  every taxonomy skill mentioned in a piece of text (case-insensitive,
  multi-word aware), plus a regex that picks out "N years of experience."
- **[semantic.py](semantic.py)** -- uses a local sentence-embedding model
  (`all-MiniLM-L6-v2`) to find skills that are conceptually close even when
  they don't share any words.
- **[graph.py](graph.py)** -- builds the skill concept graph (`networkx`) and
  renders it as an interactive HTML visualization (`pyvis`).
- **[scoring.py](scoring.py)** -- combines exact matches, related-skill
  credit, and experience into one overall score.
- **[sound.py](sound.py)** -- the audio cues (see note below).
- **[app.py](app.py)** -- the Streamlit UI tying everything together.

## Honest scope note

The original idea called for **haptic feedback** (a phone-style vibration).
A desktop browser can't reliably trigger that, so it's implemented instead as
a **visual pulse animation** -- a glowing green pulse for a good match, a
subtle red shake for a weak one -- which is the closest thing that's actually
buildable and testable on a computer. Sound feedback is real, using your
computer's speaker.
