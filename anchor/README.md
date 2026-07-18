# Anchor

A personal safety-planning app for hard moments -- built for one person's
own use, on their own device. You build your plan while you're steady;
the app makes it instantly reachable when you're not.

**This is not an AI companion, and it doesn't track or predict anything.**
That was a deliberate choice, not a limitation -- see "What this deliberately
doesn't do" below.

## If you're struggling right now

**Call 000 if you're in immediate danger.**
**Lifeline (Australia): 13 11 14** -- call or text, anytime, free.
Outside Australia: 988 (US), 116 123 (UK Samaritans), or search
"[your country] crisis line."

## What it does

- **Build My Plan** -- a short wizard: pick a metaphor for how a hard day
  feels (a storm, a fog, a wave...), write your own warning signs and
  coping strategies in your own words, add trusted contacts, list your
  reasons to stay and what you're working toward, and leave yourself a
  message for later.
- **Right Now** (crisis mode) -- one thing at a time: a breathing pacer,
  then your own warning signs, then what helps, then your reasons and
  goals, then one-tap contact with a trusted person or a crisis line. The
  visual metaphor you picked actually calms down as you move through it.
- **Breathe** -- a standalone breathing pacer, usable anytime, with an
  optional generated ambient tone.
- **Reasons** -- your reasons and goals, revisitable on an ordinary day so
  they're easier to reach on a hard one.
- **My People** -- one-tap call or a pre-written "having a hard day"
  text, so you don't have to find the words in the moment.
- **Crisis Lines** -- real numbers, always one click away.
- **My History** -- a private mood log, for your own reflection only.
- **Turned Into** -- a space for after a hard stretch has passed, to
  write what it built in you. Deliberately separate from crisis mode --
  meaning-making happens after safety, not instead of it.

## The psychology behind the design (named honestly)

- **Cognitive narrowing under stress** -- Right Now shows one thing at a
  time instead of a wall of text, because acute distress reduces how much
  people can process at once.
- **Narrative externalization** (Michael White) -- naming the feeling as
  a storm/fog/wave, separate from your identity, is a real therapeutic
  technique for building a sense of agency against a problem.
- **Vagal/parasympathetic response** -- the breathing pacer leads because
  a slower exhale physically lowers arousal before asking anyone to read
  or decide anything.
- **Mere-exposure effect** -- reasons and goals are revisitable outside
  crisis mode so they're already familiar, not something you're reading
  for the first time on a bad day.
- **Friction reduction** -- one-tap contact exists because the effort of
  finding words is a real, measurable barrier to reaching out.
- **Self-distancing / future-self continuity** (Hershfield, Kross) -- the
  message to your future self is a structured version of a technique
  shown to improve emotional regulation.

## What this deliberately doesn't do

- **No activity or device tracking, of yourself or anyone else.** Signals
  like "who someone blocked" or "which photos got deleted" aren't
  reliably predictive of anything, aren't accessible to a third-party app
  regardless of consent, and the underlying mechanism is identical to
  stalkerware. This app only ever uses what you choose to type into it.
- **No AI in crisis mode.** Right Now is 100% pre-written by you, static,
  and predictable. An AI companion that might say something unpredictable
  in someone's worst moment is a real risk, not a feature.
- **No claims about brainwave science.** The optional ambient tone in
  Breathe is just a pleasant generated sound -- it's described honestly,
  not sold as some kind of neuroscience.
- **Not a replacement for professional help or a crisis line.** It's a
  bridge to reaching real help faster, never a substitute for it.

## Privacy

Everything is stored locally in a SQLite file (`data/anchor.db`), which is
git-ignored and never leaves your machine. This app is not deployed
publicly and shouldn't be -- the data it holds is too personal for a
shared, public URL.

## Running it

```
pip install -r requirements.txt
streamlit run app.py
```

## How it's organized

- **[common/db.py](common/db.py)** -- local SQLite storage for every part of the plan
- **[common/style.py](common/style.py)** -- the calm design system and the animated metaphor visual
- **[common/audio.py](common/audio.py)** -- the honest, generated ambient tone
- **[app.py](app.py)** -- Home
- **[pages/](pages/)** -- Build My Plan, Right Now, Breathe, Reasons, My People, Crisis Lines, My History, Turned Into
