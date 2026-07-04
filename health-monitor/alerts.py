import time
import winsound
from pathlib import Path

LOG_FILE = Path(__file__).parent / "health_alerts.log"

WARNING_THRESHOLD = 75
CRITICAL_THRESHOLD = 90


def status_for(value: float) -> str:
    """Turn a percentage into a health label: 'ok', 'warning', or 'critical'."""
    if value >= CRITICAL_THRESHOLD:
        return "critical"
    if value >= WARNING_THRESHOLD:
        return "warning"
    return "ok"


def overall_status(stats: dict) -> str:
    statuses = [status_for(v) for v in stats.values()]
    if "critical" in statuses:
        return "critical"
    if "warning" in statuses:
        return "warning"
    return "ok"


def play_sound(status: str) -> None:
    """A low hum for healthy, a pulsing tone for warning, a sharp ping for critical."""
    try:
        if status == "ok":
            winsound.Beep(300, 150)
        elif status == "warning":
            winsound.Beep(600, 120)
            time.sleep(0.08)
            winsound.Beep(600, 120)
        elif status == "critical":
            winsound.Beep(1200, 250)
    except RuntimeError:
        pass  # no speaker available


def log_alert(message: str) -> None:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
