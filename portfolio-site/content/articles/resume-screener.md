Title: AI Resume Screening & Keyword Matcher
Date: 2026-07-05
Tags: python, ai, nlp
Summary: Scores a resume against a job description using exact skill matching, semantic search, and an interactive concept graph.

Upload a resume and a job description and get a match score blending exact
skill overlap, semantically related skills, and years of experience -- plus
an interactive graph showing how everything connects.

## How it works

- A spaCy phrase matcher identifies skills from resumes and job descriptions
  against a skills taxonomy -- real NLP, no model download needed
- A local sentence-embedding model finds *related* skills that don't share
  any words (e.g. resume has "TensorFlow", job wants "Machine Learning") and
  gives partial credit for them
- Builds an interactive concept graph connecting matched skills,
  resume-only skills, and gaps
- Blends skill coverage and experience match into one overall score
- Visual pulse animation and sound cues reflect the result, standing in for
  the originally-requested haptic feedback (not achievable in a browser)

## Stack

Python, spaCy, sentence-transformers, NetworkX, Streamlit.
