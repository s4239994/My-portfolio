import winsound


def play_page_hum() -> None:
    """A low tone marking the start of fetching a new page -- the 'rolling hum' of continuous flow."""
    try:
        winsound.Beep(220, 120)
    except RuntimeError:
        pass  # no speaker available


def play_item_click() -> None:
    """A short, distinct click for each item parsed off that page."""
    try:
        winsound.Beep(1200, 25)
    except RuntimeError:
        pass
