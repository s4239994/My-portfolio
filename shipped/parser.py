import pandas as pd

ARCHETYPES = {
    "Bug": ("The Bug Slayer", "Spent the sprint hunting down what was broken."),
    "Feature": ("The Feature Machine", "Spent the sprint shipping new things."),
    "Task": ("The Steady Hand", "Spent the sprint on the unglamorous groundwork."),
    "Chore": ("The Glue", "Spent the sprint keeping everything else running."),
}


def load_tickets(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    df["resolved_date"] = pd.to_datetime(df["resolved_date"])
    return df


def compute_stats(df: pd.DataFrame) -> dict:
    total = len(df)
    by_type = df["type"].value_counts().to_dict()
    top_type = max(by_type, key=by_type.get)
    top_type_pct = round(100 * by_type[top_type] / total)

    weekday_counts = df["resolved_date"].dt.day_name().value_counts()
    busiest_weekday = weekday_counts.idxmax()

    longest_title = df.loc[df["title"].str.len().idxmax(), "title"]

    dates = sorted(df["resolved_date"].dt.normalize().unique())
    longest_streak = _longest_streak(dates)

    archetype_name, archetype_desc = ARCHETYPES.get(top_type, ("The Generalist", "A bit of everything."))

    return {
        "total": total,
        "by_type": by_type,
        "top_type": top_type,
        "top_type_pct": top_type_pct,
        "busiest_weekday": busiest_weekday,
        "longest_title": longest_title,
        "longest_streak": longest_streak,
        "date_start": df["resolved_date"].min().date().isoformat(),
        "date_end": df["resolved_date"].max().date().isoformat(),
        "archetype_name": archetype_name,
        "archetype_desc": archetype_desc,
    }


def _longest_streak(sorted_unique_dates) -> int:
    if not sorted_unique_dates:
        return 0
    best = current = 1
    for i in range(1, len(sorted_unique_dates)):
        gap = (sorted_unique_dates[i] - sorted_unique_dates[i - 1]).days
        current = current + 1 if gap == 1 else 1
        best = max(best, current)
    return best
