import time
import winsound


def play_screening_cue() -> None:
    """A quick rhythmic beat while screening is running -- the 'sound texture' for the process itself."""
    try:
        for _ in range(2):
            winsound.Beep(500, 90)
            time.sleep(0.05)
    except RuntimeError:
        pass  # no speaker available


def play_result_cue(tier: str) -> None:
    """Distinct tone per match tier -- the substitute for haptic feedback."""
    try:
        if tier == "good":
            winsound.Beep(700, 120)
            winsound.Beep(900, 160)
        elif tier == "partial":
            winsound.Beep(600, 150)
        else:
            winsound.Beep(300, 250)
    except RuntimeError:
        pass
