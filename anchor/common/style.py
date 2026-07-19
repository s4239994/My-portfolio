import streamlit as st

CALM_BG = "#eef1fa"
CALM_CARD = "#ffffff"
INK = "#2b2d42"
MUTED = "#6b7089"
CRISIS_RED = "#e35d5d"
ACCENT = "#7c8fd6"

FONT_IMPORT = "https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Nunito:wght@400;600;700&display=swap"


def inject_base_css():
    st.markdown(
        f"""
        <style>
        @import url('{FONT_IMPORT}');

        html, body, [data-testid="stAppViewContainer"] {{
            background: linear-gradient(160deg, {CALM_BG} 0%, #f7f0f6 100%);
            font-family: "Nunito", sans-serif;
            color: {INK};
        }}
        h1, h2, h3 {{ font-family: "Quicksand", sans-serif; color: {INK}; font-weight: 700; }}
        [data-testid="stSidebar"] {{ background: {CALM_CARD}; }}

        .calm-card {{
            background: {CALM_CARD}; border-radius: 20px; padding: 1.5rem 1.8rem;
            box-shadow: 0 8px 28px rgba(90,100,160,0.10); margin-bottom: 1.2rem;
        }}
        .big-button-wrap .stButton > button {{
            background: {CRISIS_RED} !important; color: white !important;
            font-size: 1.3rem !important; font-weight: 700 !important;
            padding: 1.1rem 2rem !important; border-radius: 999px !important; border: none !important;
            box-shadow: 0 10px 28px rgba(227,93,93,0.35) !important;
            width: 100%;
        }}
        .stButton > button {{
            border-radius: 14px; font-family: "Nunito", sans-serif; font-weight: 700;
        }}
        .muted {{ color: {MUTED}; }}
        .crisis-line-card {{
            background: #fff5f5; border: 1.5px solid {CRISIS_RED}; border-radius: 16px;
            padding: 1rem 1.3rem; margin-bottom: 0.7rem;
        }}
        @keyframes drift {{
            0% {{ transform: translate(0px, 0px) scale(1); }}
            50% {{ transform: translate(6px, -8px) scale(1.04); }}
            100% {{ transform: translate(0px, 0px) scale(1); }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


_PALETTE = ["#7c8fd6", "#e39ec4", "#f5c26b", "#6ec6b0", "#a98ede"]


def icon_card(icon: str, text: str, accent: str = ACCENT):
    st.markdown(
        f"""
        <div style="background:{CALM_CARD}; border-radius:16px; padding:0.9rem 1.2rem;
                    margin-bottom:0.6rem; box-shadow:0 6px 20px rgba(90,100,160,0.09);
                    border-left:5px solid {accent}; display:flex; align-items:center; gap:0.7rem;">
            <span style="font-size:1.3rem;">{icon}</span>
            <span>{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def avatar_circle(name: str, index: int = 0, size: int = 46) -> str:
    initials = "".join(w[0].upper() for w in name.split()[:2]) or "?"
    color = _PALETTE[index % len(_PALETTE)]
    return (
        f'<div style="width:{size}px; height:{size}px; border-radius:50%; background:{color}; '
        f'color:white; display:flex; align-items:center; justify-content:center; '
        f'font-weight:700; font-family:Quicksand,sans-serif; font-size:{int(size*0.38)}px; flex-shrink:0;">'
        f"{initials}</div>"
    )


def mood_trend_chart(history: list):
    """history: list of dicts with 'mood' (1-5) and 'logged_at', most recent first."""
    if not history:
        return
    entries = list(reversed(history))
    colors = {1: "#e35d5d", 2: "#f0925f", 3: "#f0c25f", 4: "#8fc98a", 5: "#6ec6b0"}
    bars = ""
    max_h = 70
    for e in entries:
        h = int((e["mood"] / 5) * max_h)
        c = colors.get(e["mood"], ACCENT)
        bars += (
            f'<div style="display:flex; flex-direction:column; align-items:center; gap:4px; flex:1;">'
            f'<div style="width:70%; height:{h}px; background:{c}; border-radius:6px 6px 3px 3px; '
            f'align-self:flex-end;"></div></div>'
        )
    html = (
        '<div style="display:flex; align-items:flex-end; height:90px; gap:6px; '
        f'background:{CALM_CARD}; border-radius:16px; padding:1rem 1.2rem; '
        'box-shadow:0 6px 20px rgba(90,100,160,0.09);">'
        f"{bars}</div>"
        f'<p class="muted" style="font-size:0.78rem; margin-top:0.3rem;">Oldest → most recent, left to right.</p>'
    )
    st.markdown(html, unsafe_allow_html=True)


def growth_garden(reflections: list):
    """A small grid of growing plants, one per reflection, most recent biggest."""
    if not reflections:
        return
    plants = ["\U0001F331", "\U0001F33F", "\U0001F340", "\U0001F33B", "\U0001FAB4"]
    cells = ""
    for i, r in enumerate(reflections):
        plant = plants[i % len(plants)]
        size = 2.4 if i == 0 else 1.7
        cells += (
            f'<div style="text-align:center; background:{CALM_CARD}; border-radius:14px; '
            f'padding:0.8rem; box-shadow:0 6px 16px rgba(90,100,160,0.08);">'
            f'<div style="font-size:{size}rem;">{plant}</div></div>'
        )
    st.markdown(
        f'<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(80px, 1fr)); '
        f'gap:0.7rem; margin-bottom:1rem;">{cells}</div>',
        unsafe_allow_html=True,
    )
