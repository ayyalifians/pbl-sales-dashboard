"""
_theme_helper.py
Pusat tema PredixViz — dark/light mode, CSS global, komponen HTML reusable.
Import di setiap page: from _theme_helper import get_theme, inject_global_css, render_toggle
"""

import streamlit as st

# ── Brand ──────────────────────────────────────────────────────────────────
ACCENT   = "#6366F1"
ACCENT2  = "#22D3EE"
GREEN    = "#4ADE80"
RED      = "#F87171"
AMBER    = "#FCD34D"
PINK     = "#F472B6"

CAT_COLORS = {
    "Furniture"      : "#1D4ED8",
    "Office Supplies": "#059669",
    "Technology"     : "#D97706",
}
VALID_CATEGORIES = ["Furniture", "Office Supplies", "Technology"]
MODEL_LABEL      = {"Furniture": "OMP", "Office Supplies": "ARIMA", "Technology": "Theta"}

# ── Theme tokens ──────────────────────────────────────────────────────────
def get_theme() -> dict:
    dm = st.session_state.get("dark_mode", False)
    return {
        "dm"         : dm,
        "bg_main"    : "#0F1117" if dm else "#F8FAFC",
        "bg_card"    : "#1A1D27" if dm else "#FFFFFF",
        "bg_side"    : "#13151F" if dm else "#FFFFFF",
        "border"     : "#2D3148" if dm else "#E2E8F0",
        "text"       : "#F1F5F9" if dm else "#0F172A",
        "muted"      : "#94A3B8" if dm else "#64748B",
        "plot_bg"    : "#1A1D27" if dm else "#FFFFFF",
        "plot_paper" : "#1A1D27" if dm else "#FFFFFF",
        "grid"       : "#2D3148" if dm else "#F1F5F9",
        "tick"       : "#94A3B8" if dm else "#6B7280",
        "accent"     : ACCENT,
        "accent2"    : ACCENT2,
        # status colours
        "ok_bg"      : "#0A2A1A" if dm else "#F0FDF4",
        "ok_border"  : "#1A4A2A" if dm else "#BBF7D0",
        "ok_text"    : "#4ADE80" if dm else "#166534",
        "err_bg"     : "#2A0A0A" if dm else "#FEF2F2",
        "err_border" : "#4A1A1A" if dm else "#FECACA",
        "err_text"   : "#F87171" if dm else "#991B1B",
        "code_bg"    : "rgba(255,255,255,0.08)" if dm else "#F3F4F6",
    }


# ── Floating dark/light toggle ────────────────────────────────────────────
def render_toggle():
    """Render floating sun/moon button di pojok kanan atas."""
    dm   = st.session_state.get("dark_mode", False)
    icon = "🌙" if dm else "☀️"
    tip  = "Switch to Light Mode" if dm else "Switch to Dark Mode"

    st.markdown(f"""
    <style>
    div[data-testid="stVerticalBlock"]:has(> div > button#dm_toggle_btn) {{display:none;}}
    .dm-fab {{
        position: fixed;
        top: 14px;
        right: 18px;
        z-index: 9999;
        background: {"#1A1D27" if dm else "#FFFFFF"};
        border: 1px solid {"#2D3148" if dm else "#E2E8F0"};
        border-radius: 50%;
        width: 40px; height: 40px;
        display: flex; align-items: center; justify-content: center;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,{"0.4" if dm else "0.1"});
        transition: all 0.2s;
        font-size: 1.1rem;
        text-decoration: none;
    }}
    .dm-fab:hover {{
        transform: scale(1.1);
        box-shadow: 0 4px 14px rgba(99,102,241,0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

    # Pakai st.button tersembunyi, dipicu via JS click proxy
    col_hidden = st.columns([1])[0]
    with col_hidden:
        clicked = st.button(icon, key="dm_fab_btn", help=tip,
                            use_container_width=False)

    # FAB HTML yang visible — klik akan trigger button Streamlit di atas via JS
    st.markdown(f"""
    <div class="dm-fab" title="{tip}" onclick="
        const btns = window.parent.document.querySelectorAll('button');
        for(const b of btns){{
            if(b.innerText.trim()==='{icon}'){{b.click();break;}}
        }}
    ">{icon}</div>
    """, unsafe_allow_html=True)

    if clicked:
        st.session_state.dark_mode = not dm
        st.rerun()


# ── Global CSS injector ───────────────────────────────────────────────────
def inject_global_css():
    t = get_theme()
    dm = t["dm"]
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap');

:root {{
    --bg-main:   {t['bg_main']};
    --bg-card:   {t['bg_card']};
    --bg-side:   {t['bg_side']};
    --border:    {t['border']};
    --text:      {t['text']};
    --muted:     {t['muted']};
    --accent:    {ACCENT};
    --accent2:   {ACCENT2};
}}

/* ── Base reset ── */
html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg-main) !important;
    color: var(--text) !important;
}}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}

/* ── Layout ── */
.main .block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1280px !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {t['bg_side']} !important;
    border-right: 1px solid {t['border']} !important;
}}
[data-testid="stSidebar"] * {{
    color: {t['text']} !important;
}}
[data-testid="stSidebarNav"] {{
    padding-top: 0.5rem;
}}
/* Nav link aktif */
[data-testid="stSidebarNav"] a[aria-current="page"] {{
    background: {"rgba(99,102,241,0.15)" if dm else "rgba(99,102,241,0.08)"} !important;
    border-radius: 8px !important;
}}
[data-testid="stSidebarNav"] a:hover {{
    background: {"rgba(255,255,255,0.05)" if dm else "rgba(0,0,0,0.04)"} !important;
    border-radius: 8px !important;
}}

/* ── Typography ── */
h1, h2, h3, h4 {{
    font-family: 'Syne', sans-serif !important;
    color: {t['text']} !important;
}}
h1 {{ font-size: 1.6rem !important; font-weight: 700 !important; margin-bottom: 0.25rem !important; }}
h2 {{ font-size: 1.2rem !important; font-weight: 600 !important; }}
p, li, label, span, div {{
    color: {t['text']} !important;
}}
code {{
    background: {t['code_bg']} !important;
    color: {ACCENT} !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82em !important;
}}

/* ── Metric cards ── */
[data-testid="stMetric"] {{
    background: {t['bg_card']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 12px !important;
    padding: 1.25rem 1.5rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,{"0.25" if dm else "0.06"}) !important;
}}
[data-testid="stMetricLabel"] p {{
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    color: {t['muted']} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.35rem !important;
    font-weight: 600 !important;
    color: {t['text']} !important;
}}
[data-testid="stMetricDelta"] {{
    font-size: 0.78rem !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: {ACCENT} !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.25rem !important;
    transition: all 0.15s !important;
    width: 100% !important;
}}
.stButton > button:hover {{
    background: #4F46E5 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(99,102,241,0.35) !important;
}}
/* FAB button — override */
button[title*="Mode"] {{
    all: unset !important;
}}

/* ── Selects, inputs ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {{
    background: {t['bg_card']} !important;
    border-color: {t['border']} !important;
    color: {t['text']} !important;
    border-radius: 8px !important;
}}
/* dropdown options */
[data-baseweb="popover"] ul {{
    background: {t['bg_card']} !important;
    border: 1px solid {t['border']} !important;
}}
[data-baseweb="popover"] li {{
    color: {t['text']} !important;
}}
[data-baseweb="popover"] li:hover {{
    background: {"rgba(99,102,241,0.15)" if dm else "rgba(99,102,241,0.07)"} !important;
}}

/* ── Slider ── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {{
    background: {ACCENT} !important;
    border-color: {ACCENT} !important;
}}
[data-testid="stSlider"] div[data-testid="stSliderTickBarMin"],
[data-testid="stSlider"] div[data-testid="stSliderTickBarMax"] {{
    color: {t['muted']} !important;
}}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {{
    border-bottom: 1px solid {t['border']} !important;
    background: transparent !important;
}}
[data-testid="stTabs"] [role="tab"] {{
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    color: {t['muted']} !important;
    border-radius: 8px 8px 0 0 !important;
}}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    color: {ACCENT} !important;
    border-bottom: 2px solid {ACCENT} !important;
    background: {"rgba(99,102,241,0.08)" if dm else "rgba(99,102,241,0.05)"} !important;
}}

/* ── Dataframe ── */
[data-testid="stDataFrame"],
[data-testid="stDataFrameResizable"] {{
    background: {t['bg_card']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}}
/* header row */
[data-testid="stDataFrame"] th {{
    background: {"#252839" if dm else "#F8FAFC"} !important;
    color: {t['muted']} !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}}
[data-testid="stDataFrame"] td {{
    color: {t['text']} !important;
    font-size: 0.83rem !important;
}}

/* ── Divider ── */
[data-testid="stDivider"] hr {{
    border-color: {t['border']} !important;
}}

/* ── Alerts/info ── */
[data-testid="stAlert"] {{
    background: {"rgba(99,102,241,0.1)" if dm else "#EEF2FF"} !important;
    border: 1px solid {"rgba(99,102,241,0.25)" if dm else "#C7D2FE"} !important;
    border-radius: 10px !important;
    color: {t['text']} !important;
}}

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div > div {{
    background: {ACCENT} !important;
}}

/* ── Spinner ── */
[data-testid="stSpinner"] p {{
    color: {t['muted']} !important;
}}
</style>
""", unsafe_allow_html=True)


# ── Reusable HTML components ──────────────────────────────────────────────
def section_label(text: str, t: dict) -> str:
    return f"""<div style='font-size:0.68rem;font-weight:700;color:{t["muted"]};
        text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.75rem;
        font-family:Syne,sans-serif;'>{text}</div>"""

def info_banner(text: str, t: dict) -> str:
    dm = t["dm"]
    return f"""<div style='background:{"rgba(99,102,241,0.1)" if dm else "#EEF2FF"};
        border:1px solid {"rgba(99,102,241,0.25)" if dm else "#C7D2FE"};
        border-radius:10px;padding:0.85rem 1.1rem;font-size:0.82rem;
        color:{t["muted"]};line-height:1.6;'>{text}</div>"""

def card_wrap(inner_html: str, t: dict, border_color: str = None, extra_style: str = "") -> str:
    bc = border_color or t["border"]
    return f"""<div style='background:{t["bg_card"]};border:1px solid {bc};
        border-radius:14px;padding:1.5rem;{extra_style}'>{inner_html}</div>"""

def status_badge(connected: bool, t: dict) -> str:
    if connected:
        return f"""<div style='display:flex;align-items:center;gap:8px;padding:8px 12px;
            background:{t["ok_bg"]};border:1px solid {t["ok_border"]};border-radius:8px;
            font-size:0.8rem;color:{t["ok_text"]};font-weight:500;'>
            <div style='width:7px;height:7px;border-radius:50%;background:#16A34A;flex-shrink:0;'></div>
            API terhubung</div>"""
    else:
        return f"""<div style='display:flex;align-items:center;gap:8px;padding:8px 12px;
            background:{t["err_bg"]};border:1px solid {t["err_border"]};border-radius:8px;
            font-size:0.8rem;color:{t["err_text"]};font-weight:500;'>
            <div style='width:7px;height:7px;border-radius:50%;background:#DC2626;flex-shrink:0;'></div>
            API tidak aktif &nbsp;—&nbsp;
            <code style='background:{t["code_bg"]};color:{t["err_text"]};padding:1px 6px;
            border-radius:4px;font-size:0.75rem;'>uvicorn api.main:app --reload</code>
            </div>"""
