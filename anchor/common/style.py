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


def render_metaphor(metaphor: dict, intensity: float, size: int = 220):
    """intensity: 1.0 = full storm, 0.0 = fully calmed."""
    intensity = max(0.0, min(1.0, intensity))
    duration = 4.0 - intensity * 2.6
    opacity = 0.32 + intensity * 0.42
    blur = 14 - intensity * 7
    color = metaphor["color"]
    emoji = metaphor["emoji"]

    html = f"""
    <div style="display:flex; justify-content:center; align-items:center; height:{size + 40}px; position:relative;">
      <div style="position:relative; width:{size}px; height:{size}px;">
        <div style="position:absolute; inset:0; border-radius:50%;
                    background:{color}; opacity:{opacity};
                    filter: blur({blur}px);
                    animation: drift {duration}s ease-in-out infinite;"></div>
        <div style="position:absolute; inset:15%; border-radius:50%;
                    background:{color}; opacity:{opacity * 0.8};
                    filter: blur({blur * 0.7}px);
                    animation: drift {duration * 1.3}s ease-in-out infinite reverse;"></div>
        <div style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
                    font-size:{int(size * 0.28)}px;">{emoji}</div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
