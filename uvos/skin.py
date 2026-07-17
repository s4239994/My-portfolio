"""
Burn-time math is grounded in two real, citable references, not invented:

1. The WHO/WMO definition of the UV Index: UVI = 40 x erythemal irradiance
   (in W/m^2). See World Health Organization, "Global Solar UV Index: A
   Practical Guide" (2002).
2. Minimal Erythema Dose (MED) reference ranges by Fitzpatrick skin type,
   commonly cited in dermatology and sun-safety education (in J/m^2).

Combining them: time-to-burn (seconds) = MED / (UVI / 40) = 40 x MED / UVI.
"""

SKIN_TYPES = {
    "I": {"label": "Very fair -- always burns, never tans", "med": 200},
    "II": {"label": "Fair -- burns easily, tans minimally", "med": 250},
    "III": {"label": "Medium -- burns moderately, tans gradually", "med": 300},
    "IV": {"label": "Olive -- burns minimally, tans well", "med": 400},
    "V": {"label": "Brown -- rarely burns, tans darkly", "med": 500},
    "VI": {"label": "Dark brown/black -- never burns", "med": 700},
}

QUIZ_QUESTIONS = [
    {
        "question": "What happens after 30 minutes of unprotected midday summer sun?",
        "options": [
            ("Always burns, painful, peels", "I"),
            ("Burns easily, then maybe a light tan", "II"),
            ("Sometimes burns, tans gradually afterward", "III"),
            ("Rarely burns, tans easily", "IV"),
            ("Almost never burns", "V"),
            ("Never burns", "VI"),
        ],
    },
]


def burn_time_minutes(uv_index: float, skin_type: str) -> float | None:
    """Unprotected time-to-burn in minutes. None if UV is negligible."""
    if not uv_index or uv_index < 0.5:
        return None
    med = SKIN_TYPES[skin_type]["med"]
    seconds = 40 * med / uv_index
    return round(seconds / 60, 1)


def risk_tier(uv_index: float) -> tuple[str, str]:
    """Returns (label, ansi_color_hex) matching the official UV Index scale."""
    if uv_index is None:
        return "UNKNOWN", "#888888"
    if uv_index < 3:
        return "LOW", "#3ddc84"
    if uv_index < 6:
        return "MODERATE", "#f5d442"
    if uv_index < 8:
        return "HIGH", "#ff9d42"
    if uv_index < 11:
        return "VERY HIGH", "#ff5c5c"
    return "EXTREME", "#ff2fb1"
