from datetime import date, timedelta

import requests

ARPANSA_URL = "https://uvdata.arpansa.gov.au/api/uvlevel/"
TIMEOUT = 8

CITIES = {
    "Melbourne": (-37.8136, 144.9631),
    "Sydney": (-33.8688, 151.2093),
    "Brisbane": (-27.4698, 153.0251),
    "Perth": (-31.9523, 115.8613),
    "Adelaide": (-34.9285, 138.6007),
    "Darwin": (-12.4634, 130.8456),
    "Hobart": (-42.8821, 147.3272),
    "Canberra": (-35.2809, 149.1300),
    "Gold Coast": (-28.0167, 153.4000),
    "Cairns": (-16.9186, 145.7781),
    "Newcastle": (-32.9283, 151.7817),
    "Wollongong": (-34.4278, 150.8931),
    "Geelong": (-38.1499, 144.3617),
    "Townsville": (-19.2590, 146.8169),
    "Alice Springs": (-23.6980, 133.8807),
    "Sunshine Coast": (-26.6500, 153.0667),
    "Ballarat": (-37.5622, 143.8503),
    "Bendigo": (-36.7570, 144.2794),
    "Launceston": (-41.4332, 147.1441),
    "Broome": (-17.9614, 122.2359),
    "Byron Bay": (-28.6474, 153.6020),
    "Coffs Harbour": (-30.2963, 153.1157),
    "Rockhampton": (-23.3791, 150.5100),
    "Albury": (-36.0737, 146.9135),
}


def _fetch_day(lat: float, lon: float, day: date) -> list:
    response = requests.get(
        ARPANSA_URL,
        params={"longitude": lon, "latitude": lat, "date": day.isoformat()},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("GraphData", [])


def get_current_uv(city: str) -> dict:
    """Live UV Index for an Australian capital city, straight from ARPANSA's
    real-time monitoring network. Falls back to the most recent day that
    actually has data yet (today's row is empty until ARPANSA's forecast
    job runs each morning)."""
    lat, lon = CITIES[city]

    for days_back in range(0, 3):
        day = date.today() - timedelta(days=days_back)
        try:
            rows = _fetch_day(lat, lon, day)
        except Exception:
            continue

        readings = [r for r in rows if r.get("Measured") is not None or r.get("Forecast") is not None]
        if not readings:
            continue

        latest = readings[-1]
        uv_value = latest["Measured"] if latest["Measured"] is not None else latest["Forecast"]
        peak = max(
            (r["Measured"] if r["Measured"] is not None else r["Forecast"]) or 0
            for r in readings
        )
        return {
            "city": city,
            "uv_index": round(uv_value, 1),
            "peak_today": round(peak, 1),
            "as_of": latest["Date"],
            "is_live": days_back == 0,
            "source": "ARPANSA",
        }

    return {
        "city": city,
        "uv_index": None,
        "peak_today": None,
        "as_of": None,
        "is_live": False,
        "source": "ARPANSA",
    }
