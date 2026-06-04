"""
app.py — Entry point Streamlit PredixViz
"""

import streamlit as st

st.set_page_config(
    page_title="PredixViz — Retail Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme State ──
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dm = st.session_state.dark_mode

# ── CSS Global ──
bg_main   = "#0F1117" if dm else "#F8FAFC"
bg_card   = "#1A1D27" if dm else "#FFFFFF"
bg_side   = "#13151F" if dm else "#FFFFFF"
border_c  = "#2D3148" if dm else "#E2E8F0"
text_main = "#F1F5F9" if dm else "#0F172A"
text_mute = "#94A3B8" if dm else "#64748B"
accent    = "#6366F1"
accent2   = "#22D3EE"
metric_val= "#F1F5F9" if dm else "#0F172A"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {{
  --bg-main: {bg_main};
  --bg-card: {bg_card};
  --bg-side: {bg_side};
  --border:  {border_c};
  --text:    {text_main};
  --muted:   {text_mute};
  --accent:  {accent};
  --accent2: {accent2};
}}

html, body, [class*="css"] {{
  font-family: 'DM Sans', sans-serif;
  background-color: var(--bg-main) !important;
  color: var(--text) !important;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}

[data-testid="stSidebar"] {{
  background: var(--bg-side) !important;
  border-right: 1px solid var(--border) !important;
}}

[data-testid="stSidebar"] * {{
  color: var(--text) !important;
}}

.main .block-container {{
  padding-top: 1.5rem;
  padding-bottom: 3rem;
  max-width: 1280px;
}}

[data-testid="stMetric"] {{
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  padding: 1.25rem 1.5rem !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}}
[data-testid="stMetricLabel"] p {{
  font-size: 0.7rem !important;
  font-weight: 600 !important;
  color: var(--muted) !important;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}}
[data-testid="stMetricValue"] {{
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 1.4rem !important;
  font-weight: 600 !important;
  color: {metric_val} !important;
}}

.stButton > button {{
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 0.5rem 1.25rem;
  transition: all 0.15s;
  width: 100%;
}}
.stButton > button:hover {{
  background: #4F46E5;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99,102,241,0.3);
}}

h1, h2, h3 {{
  font-family: 'Syne', sans-serif !important;
  color: var(--text) !important;
}}
h1 {{ font-size: 1.6rem !important; font-weight: 700 !important; }}

[data-testid="stSelectbox"] > div > div {{
  background: var(--bg-card) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
}}

.stDataFrame {{ background: var(--bg-card) !important; }}

/* Tab styling */
[data-testid="stTabs"] [role="tab"] {{
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.85rem !important;
  color: var(--muted) !important;
}}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
  color: var(--accent) !important;
}}

p, li, div, span, label {{
  color: var(--text) !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    # Logo PredixViz
    st.markdown(f"""
    <div style='padding:0.5rem 0.25rem 1.25rem;'>
        <div style='display:flex;align-items:center;gap:10px;'>
            <div style='width:38px;height:38px;background:linear-gradient(135deg,{accent},{accent2});border-radius:10px;
                display:flex;align-items:center;justify-content:center;flex-shrink:0;'>
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M3 6h18" stroke="white" stroke-width="2" stroke-linecap="round"/>
                  <path d="M16 10a4 4 0 01-8 0" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <div style='font-family:Syne,sans-serif;font-size:1.05rem;font-weight:700;color:{text_main};line-height:1.1;'>PredixViz</div>
                <div style='font-size:0.68rem;color:{text_mute};letter-spacing:0.05em;'>Retail Analytics</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Dark mode toggle
    col_dm1, col_dm2 = st.columns([2.5, 1])
    with col_dm1:
        st.markdown(f"<div style='font-size:0.8rem;color:{text_mute};padding-top:0.4rem;'>{'🌙 Dark Mode' if dm else '☀️ Light Mode'}</div>", unsafe_allow_html=True)
    with col_dm2:
        if st.button("⟳", key="toggle_dm", help="Toggle dark/light mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.divider()

    # API status
    from utils.api_client import check_health
    if check_health():
        st.markdown(f"""<div style='display:flex;align-items:center;gap:8px;padding:8px 12px;
            background:{"#0A2A1A" if dm else "#F0FDF4"};border:1px solid {"#1A4A2A" if dm else "#BBF7D0"};border-radius:8px;
            font-size:0.8rem;color:{"#4ADE80" if dm else "#166534"};font-weight:500;'>
            <div style='width:7px;height:7px;border-radius:50%;background:#16A34A;flex-shrink:0;'></div>
            API terhubung</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div style='display:flex;align-items:center;gap:8px;padding:8px 12px;
            background:{"#2A0A0A" if dm else "#FEF2F2"};border:1px solid {"#4A1A1A" if dm else "#FECACA"};border-radius:8px;
            font-size:0.8rem;color:{"#F87171" if dm else "#991B1B"};font-weight:500;'>
            <div style='width:7px;height:7px;border-radius:50%;background:#DC2626;flex-shrink:0;'></div>
            API tidak aktif</div>""", unsafe_allow_html=True)
        st.caption("Jalankan: `uvicorn api.main:app --reload`")

    st.divider()

    for label, items in [
        ("Dataset", [("Superstore 2014–2017", None)]),
        ("Model Prediksi", [("Furniture", "OMP"), ("Office Supplies", "ARIMA"), ("Technology", "Theta")]),
    ]:
        st.markdown(f"<div style='font-size:0.68rem;font-weight:600;color:{text_mute};text-transform:uppercase;letter-spacing:0.08em;padding:0 0.25rem;margin-bottom:0.4rem;'>{label}</div>", unsafe_allow_html=True)
        for name, val in items:
            if val:
                st.markdown(f"<div style='font-size:0.8rem;color:{text_main};padding:2px 0.25rem;'>{name} <span style='color:{text_mute};'>→</span> <code style='color:{accent};font-size:0.75rem;'>{val}</code></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='font-size:0.8rem;color:{text_main};padding:2px 0.25rem;'>{name}</div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)

    st.divider()
    st.markdown(f"<div style='font-size:0.68rem;color:{text_mute};padding:0 0.25rem;'>PBL Kelompok 6 · 2025</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
#   LANDING PAGE
# ══════════════════════════════════════════

dm = st.session_state.dark_mode
bg_hero   = "linear-gradient(135deg,#0F1117 0%,#1a1d2e 50%,#0F1117 100%)" if dm else "linear-gradient(135deg,#EEF2FF 0%,#F0F9FF 50%,#F8FAFC 100%)"
card_bg   = "#1A1D27" if dm else "#FFFFFF"
border_lp = "#2D3148" if dm else "#E2E8F0"
txt_h     = "#F1F5F9" if dm else "#0F172A"
txt_s     = "#94A3B8" if dm else "#64748B"
stat_bg   = "#252839" if dm else "#F8FAFC"

st.markdown(f"""
<style>
.hero-section {{
  background: {bg_hero};
  border-radius: 20px;
  padding: 3rem 3rem 2.5rem;
  margin-bottom: 2rem;
  border: 1px solid {border_lp};
  position: relative;
  overflow: hidden;
}}
.hero-section::before {{
  content: '';
  position: absolute;
  top: -80px; right: -80px;
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
  pointer-events: none;
}}
.hero-section::after {{
  content: '';
  position: absolute;
  bottom: -60px; left: -40px;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(34,211,238,0.08) 0%, transparent 70%);
  pointer-events: none;
}}
.hero-logo-badge {{
  display:inline-flex;align-items:center;gap:10px;
  background: {"rgba(99,102,241,0.15)" if dm else "rgba(99,102,241,0.08)"};
  border: 1px solid {"rgba(99,102,241,0.3)" if dm else "rgba(99,102,241,0.2)"};
  border-radius: 50px;
  padding: 6px 16px 6px 8px;
  margin-bottom: 1.25rem;
}}
.feat-card {{
  background: {card_bg};
  border: 1px solid {border_lp};
  border-radius: 14px;
  padding: 1.5rem;
  height: 100%;
  transition: transform 0.2s, box-shadow 0.2s;
}}
.feat-card:hover {{
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(99,102,241,0.12);
}}
.stat-badge {{
  background: {stat_bg};
  border: 1px solid {border_lp};
  border-radius: 10px;
  padding: 1rem 1.25rem;
  text-align: center;
}}
.insight-strip {{
  background: {card_bg};
  border: 1px solid {border_lp};
  border-left: 3px solid {accent};
  border-radius: 10px;
  padding: 1rem 1.25rem;
  margin-bottom: 0.75rem;
}}
</style>
""", unsafe_allow_html=True)

# ── Hero ──
st.markdown(f"""
<div class="hero-section">
  <div class="hero-logo-badge">
    <div style='width:28px;height:28px;background:linear-gradient(135deg,{accent},{accent2});border-radius:7px;
      display:flex;align-items:center;justify-content:center;'>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M3 6h18" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M16 10a4 4 0 01-8 0" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <span style='font-family:Syne,sans-serif;font-size:0.85rem;font-weight:600;color:{txt_h};'>PredixViz</span>
    <span style='font-size:0.72rem;color:{accent};font-weight:500;padding:2px 8px;background:rgba(99,102,241,0.15);border-radius:20px;'>Beta</span>
  </div>

  <h1 style='font-family:Syne,sans-serif;font-size:2.4rem;font-weight:800;color:{txt_h};
    line-height:1.15;margin:0 0 0.75rem;max-width:600px;'>
    Retail Analytics &amp;<br/>
    <span style='background:linear-gradient(90deg,{accent},{accent2});-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
    Sales Intelligence</span>
  </h1>
  <p style='font-size:1rem;color:{txt_s};max-width:580px;line-height:1.65;margin:0 0 1.75rem;'>
    Eksplorasi data Superstore 2014–2017 dengan dashboard interaktif. Pantau performa penjualan,
    prediksi tren ke depan menggunakan model ML, dan evaluasi akurasi model secara mendalam.
  </p>

  <div style='display:flex;gap:1rem;align-items:center;flex-wrap:wrap;'>
    <div style='display:flex;align-items:center;gap:6px;font-size:0.82rem;color:{txt_s};'>
      <span style='color:{accent};font-size:1rem;'>◈</span> Superstore Dataset 2014–2017
    </div>
    <div style='display:flex;align-items:center;gap:6px;font-size:0.82rem;color:{txt_s};'>
      <span style='color:{accent2};font-size:1rem;'>◈</span> OMP · ARIMA · Theta Models
    </div>
    <div style='display:flex;align-items:center;gap:6px;font-size:0.82rem;color:{txt_s};'>
      <span style='color:#4ADE80;font-size:1rem;'>◈</span> 3 Kategori · 17 Sub-kategori
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Stats ──
sc1, sc2, sc3, sc4 = st.columns(4)
for col, val, lbl, clr in [
    (sc1, "9,994",   "Total Orders",    accent),
    (sc2, "4 Tahun", "Data Historis",   accent2),
    (sc3, "3",       "Model Prediksi",  "#4ADE80"),
    (sc4, "17",      "Sub-kategori",    "#F472B6"),
]:
    with col:
        st.markdown(f"""
        <div class="stat-badge">
          <div style='font-family:JetBrains Mono,monospace;font-size:1.5rem;font-weight:700;color:{clr};'>{val}</div>
          <div style='font-size:0.72rem;color:{txt_s};margin-top:2px;'>{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:1.75rem;'></div>", unsafe_allow_html=True)

# ── Feature Cards ──
st.markdown(f"<div style='font-family:Syne,sans-serif;font-size:0.68rem;font-weight:700;color:{txt_s};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.9rem;'>Fitur Aplikasi</div>", unsafe_allow_html=True)

fc1, fc2, fc3, fc4 = st.columns(4)
features = [
    ("fc1", "📊", "Overview", accent, "KPI penjualan, tren bulanan per kategori, distribusi sales, dan insight bisnis dari 4 tahun data."),
    ("fc2", "🔮", "Prediksi Sales", accent2, "Forecast penjualan multi-periode dengan confidence interval menggunakan OMP, ARIMA, dan Theta."),
    ("fc3", "📐", "Evaluasi Model", "#4ADE80", "Perbandingan performa model: MAE, RMSE, MAPE, dan R² untuk validation dan test set."),
    ("fc4", "🏆", "Top Produk", "#F472B6", "Ranking produk berdasarkan total sales dan profit, dengan filter kategori."),
]
for col, (key, icon, title, clr, desc) in zip([fc1, fc2, fc3, fc4], features):
    with col:
        st.markdown(f"""
        <div class="feat-card">
          <div style='width:40px;height:40px;background:{"rgba(99,102,241,0.12)" if clr==accent else f"rgba({",".join(str(int(clr.lstrip("#")[i:i+2],16)) for i in (0,2,4))},0.12)"};
            border-radius:10px;display:flex;align-items:center;justify-content:center;
            font-size:1.2rem;margin-bottom:0.85rem;'>{icon}</div>
          <div style='font-family:Syne,sans-serif;font-size:0.95rem;font-weight:700;color:{txt_h};margin-bottom:0.5rem;'>{title}</div>
          <div style='font-size:0.8rem;color:{txt_s};line-height:1.6;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)

# ── Dataset Info ──
st.markdown(f"<div style='font-family:Syne,sans-serif;font-size:0.68rem;font-weight:700;color:{txt_s};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.9rem;'>Tentang Dataset</div>", unsafe_allow_html=True)

di1, di2 = st.columns([1.6, 1])
with di1:
    st.markdown(f"""
    <div class="feat-card" style='padding:1.75rem;'>
      <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:{txt_h};margin-bottom:0.75rem;'>
        Superstore Sales Dataset
      </div>
      <p style='font-size:0.85rem;color:{txt_s};line-height:1.7;margin-bottom:1rem;'>
        Dataset retail populer yang mencakup transaksi penjualan sebuah superstore Amerika Serikat
        periode 2014–2017. Berisi informasi pesanan, pelanggan, produk, dan performa finansial
        yang kaya untuk analisis bisnis.
      </p>
      <div style='display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;'>
        {"".join(f'<div style="background:{stat_bg};border-radius:8px;padding:0.6rem 0.9rem;"><div style="font-size:0.68rem;color:{txt_s};text-transform:uppercase;letter-spacing:0.05em;">{k}</div><div style="font-size:0.85rem;font-weight:600;color:{txt_h};margin-top:1px;">{v}</div></div>' for k,v in [("Periode","2014 – 2017"),("Region","Amerika Serikat"),("Kategori","3 Utama"),("Sub-kategori","17 Tipe")])}
      </div>
    </div>
    """, unsafe_allow_html=True)

with di2:
    st.markdown(f"""
    <div class="feat-card" style='padding:1.75rem;'>
      <div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;color:{txt_h};margin-bottom:1rem;'>
        Kategori Produk
      </div>
      <div class="insight-strip" style='border-left-color:#1D4ED8;'>
        <div style='font-size:0.78rem;font-weight:600;color:{"#93C5FD" if dm else "#1D4ED8"};'>🪑 Furniture</div>
        <div style='font-size:0.75rem;color:{txt_s};margin-top:2px;'>Bookcases, Chairs, Tables, Storage…</div>
      </div>
      <div class="insight-strip" style='border-left-color:#059669;'>
        <div style='font-size:0.78rem;font-weight:600;color:{"#6EE7B7" if dm else "#059669"};'>📎 Office Supplies</div>
        <div style='font-size:0.75rem;color:{txt_s};margin-top:2px;'>Binders, Paper, Art, Labels…</div>
      </div>
      <div class="insight-strip" style='border-left-color:#D97706;'>
        <div style='font-size:0.78rem;font-weight:600;color:{"#FCD34D" if dm else "#D97706"};'>💻 Technology</div>
        <div style='font-size:0.75rem;color:{txt_s};margin-top:2px;'>Phones, Copiers, Accessories…</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center;font-size:0.75rem;color:{txt_s};'>Gunakan menu navigasi di sidebar untuk menjelajahi fitur PredixViz ↑</div>", unsafe_allow_html=True)
