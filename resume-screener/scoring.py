import semantic


def compute_match(resume_skills: set, jd_skills: set, resume_years: int, jd_years_required: int) -> dict:
    exact_matches = resume_skills & jd_skills
    gaps = jd_skills - resume_skills
    related = semantic.find_related_matches(gaps, resume_skills)

    if jd_skills:
        skill_score = min((len(exact_matches) + 0.5 * len(related)) / len(jd_skills), 1.0)
    else:
        skill_score = 1.0

    if jd_years_required > 0:
        experience_score = min(resume_years / jd_years_required, 1.0)
    else:
        experience_score = 1.0

    overall = round((0.7 * skill_score + 0.3 * experience_score) * 100)

    if overall >= 75:
        tier = "good"
    elif overall >= 45:
        tier = "partial"
    else:
        tier = "weak"

    return {
        "overall_score": overall,
        "tier": tier,
        "skill_score": round(skill_score * 100),
        "experience_score": round(experience_score * 100),
        "exact_matches": exact_matches,
        "gaps": gaps,
        "related": related,
    }
