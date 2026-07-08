import random
from datetime import datetime, timedelta

import db

TEAM = [
    "Priya", "Jordan", "Wei", "Sam", "Aisha", "Liam",
    "Noor", "Tyler", "Mei", "Diego", "Chloe", "Kai",
]

MOODS = [
    ("thriving", "🔥", 5),
    ("good", "😊", 4),
    ("mid", "😐", 3),
    ("rough", "😩", 2),
    ("done", "💀", 1),
]

NORMAL_NOTES = [
    "shipped a small win today",
    "quiet day, nothing major",
    "good sync with the team",
    "made progress on my project",
    "coffee was good, code was fine",
    "",
    "",
]

CRUNCH_NOTES = [
    "third late night this week, deadline is brutal",
    "no real breaks today, back to back meetings",
    "feeling behind on everything",
    "release crunch is draining",
    "worked through lunch again",
]

RECOVERY_NOTES = [
    "finally shipped it, relieved",
    "took an actual lunch break today",
    "manager gave us a breather day, appreciated",
    "catching up on sleep this week",
    "",
]


def generate_demo_data(conn, days: int = 28) -> None:
    """Seeds a plausible demo team with a deliberate mid-period 'crunch week'
    dip and recovery, so the AI briefing has a real pattern to notice."""
    db.clear_all(conn)
    random.seed(42)

    crunch_start = days - 18
    crunch_end = days - 11

    today = datetime.now()
    for day_offset in range(days, 0, -1):
        date = today - timedelta(days=day_offset)
        in_crunch = crunch_start >= day_offset >= crunch_end
        just_recovered = crunch_end - 4 <= day_offset < crunch_end

        for person in TEAM:
            if random.random() < 0.25:
                continue  # not everyone checks in every day, realistically

            if in_crunch:
                weights = [1, 2, 4, 6, 4]
                note_pool = CRUNCH_NOTES
                note_chance = 0.55
            elif just_recovered:
                weights = [4, 5, 3, 1, 1]
                note_pool = RECOVERY_NOTES
                note_chance = 0.4
            else:
                weights = [3, 5, 4, 2, 1]
                note_pool = NORMAL_NOTES
                note_chance = 0.3

            label, emoji, score = random.choices(MOODS, weights=weights, k=1)[0]
            note = random.choice(note_pool) if random.random() < note_chance else ""

            timestamp = date.replace(
                hour=random.randint(8, 17), minute=random.randint(0, 59)
            ).isoformat(timespec="seconds")

            db.insert_checkin(
                conn,
                {
                    "person": person,
                    "mood_label": label,
                    "mood_emoji": emoji,
                    "mood_score": score,
                    "note": note,
                    "created_at": timestamp,
                },
            )
