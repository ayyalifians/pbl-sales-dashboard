"""
app.py — Landing page PredixViz
"""
import streamlit as st

st.set_page_config(
    page_title="PredixViz — Retail Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

from _theme_helper import (
    get_theme, inject_global_css, render_toggle,
    section_label, card_wrap, status_badge,
    ACCENT, ACCENT2, CAT_COLORS
)
from utils.api_client import check_health

inject_global_css()
render_toggle()

t = get_theme()
dm = t["dm"]

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding:0.5rem 0.25rem 1.25rem;'>
        <div style='display:flex;align-items:center;gap:10px;'>
            <div style='width:38px;height:38px;
                background:linear-gradient(135deg,{ACCENT},{ACCENT2});
                border-radius:10px;display:flex;align-items:center;
                justify-content:center;flex-shrink:0;'>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"
                        stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M3 6h18" stroke="white" stroke-width="2" stroke-linecap="round"/>
                    <path d="M16 10a4 4 0 01-8 0" stroke="white" stroke-width="2"
                        stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <div style='font-family:Syne,sans-serif;font-size:1.05rem;font-weight:700;
                    color:{t["text"]};line-height:1.1;'>PredixViz</div>
                <div style='font-size:0.68rem;color:{t["muted"]};letter-spacing:0.05em;'>
                    Retail Analytics</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown(status_badge(check_health(), t), unsafe_allow_html=True)
    st.divider()
    st.markdown(f"<div style='font-size:0.68rem;color:{t['muted']};padding:0 0.25rem;'>PredixViz · 2026</div>",
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  LANDING PAGE
# ══════════════════════════════════════════════════════════════════════
bg_hero  = ("linear-gradient(135deg,#0F1117 0%,#1a1d2e 50%,#0F1117 100%)"
            if dm else "linear-gradient(135deg,#EEF2FF 0%,#F0F9FF 50%,#F8FAFC 100%)")
stat_bg  = "#252839" if dm else "#F8FAFC"
ins_bg   = "#1A1D27" if dm else "#FFFFFF"

st.markdown(f"""
<style>
.hero {{
    background:{bg_hero};border-radius:20px;padding:3rem 3rem 2.5rem;
    margin-bottom:2rem;border:1px solid {t["border"]};
    position:relative;overflow:hidden;
}}
.hero::before {{
    content:'';position:absolute;top:-80px;right:-80px;
    width:300px;height:300px;
    background:radial-gradient(circle,rgba(99,102,241,0.12) 0%,transparent 70%);
    pointer-events:none;
}}
.hero::after {{
    content:'';position:absolute;bottom:-60px;left:-40px;
    width:200px;height:200px;
    background:radial-gradient(circle,rgba(34,211,238,0.08) 0%,transparent 70%);
    pointer-events:none;
}}
.feat-card {{
    background:{t["bg_card"]};border:1px solid {t["border"]};border-radius:14px;
    padding:1.5rem;height:100%;transition:transform 0.2s,box-shadow 0.2s;
}}
.feat-card:hover {{
    transform:translateY(-3px);
    box-shadow:0 8px 24px rgba(99,102,241,0.12);
}}
.stat-badge {{
    background:{stat_bg};border:1px solid {t["border"]};
    border-radius:10px;padding:1rem 1.25rem;text-align:center;
}}
.ins-strip {{
    background:{ins_bg};border:1px solid {t["border"]};
    border-radius:10px;padding:0.85rem 1.1rem;margin-bottom:0.65rem;
}}
</style>

<!-- HERO -->
<div class="hero">
  <div style='display:inline-flex;align-items:center;gap:10px;
    background:{"rgba(99,102,241,0.15)" if dm else "rgba(99,102,241,0.08)"};
    border:1px solid {"rgba(99,102,241,0.3)" if dm else "rgba(99,102,241,0.2)"};
    border-radius:50px;padding:6px 16px 6px 8px;margin-bottom:1.25rem;'>
      <div style='width:26px;height:26px;background:linear-gradient(135deg,{ACCENT},{ACCENT2});
        border-radius:7px;display:flex;align-items:center;justify-content:center;'>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
          <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"
            stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M3 6h18" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
          <path d="M16 10a4 4 0 01-8 0" stroke="white" stroke-width="2.2"
            stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <span style='font-family:Syne,sans-serif;font-size:0.85rem;font-weight:600;
        color:{t["text"]};'>PredixViz</span>
      <span style='font-size:0.72rem;color:{ACCENT};font-weight:500;
        padding:2px 8px;background:rgba(99,102,241,0.15);border-radius:20px;'>Beta</span>
  </div>

  <h1 style='font-family:Syne,sans-serif;font-size:2.4rem;font-weight:800;
    color:{t["text"]};line-height:1.15;margin:0 0 0.75rem;max-width:600px;'>
    Retail Analytics &amp;<br/>
    <span style='background:linear-gradient(90deg,{ACCENT},{ACCENT2});
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
      Sales Intelligence</span>
  </h1>
  <p style='font-size:1rem;color:{t["muted"]};max-width:580px;line-height:1.65;margin:0 0 1.75rem;'>
    Eksplorasi data Superstore 2014–2017 dengan dashboard interaktif. Pantau performa
    penjualan, prediksi tren ke depan menggunakan model ML, dan evaluasi akurasi model.
  </p>
  <div style='display:flex;gap:1.25rem;flex-wrap:wrap;'>
    <span style='display:flex;align-items:center;gap:6px;font-size:0.82rem;color:{t["muted"]};'>
      <span style='color:{ACCENT};'>◈</span> Superstore Dataset 2014–2017</span>
    <span style='display:flex;align-items:center;gap:6px;font-size:0.82rem;color:{t["muted"]};'>
      <span style='color:{ACCENT2};'>◈</span> OMP · ARIMA · Theta</span>
    <span style='display:flex;align-items:center;gap:6px;font-size:0.82rem;color:{t["muted"]};'>
      <span style='color:#4ADE80;'>◈</span> 3 Kategori · 17 Sub-kategori</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Stats row
sc1, sc2, sc3, sc4 = st.columns(4)
for col, val, lbl, clr in [
    (sc1, "9,994",   "Total Orders",   ACCENT),
    (sc2, "4 Tahun", "Data Historis",  ACCENT2),
    (sc3, "3",       "Model Prediksi", "#4ADE80"),
    (sc4, "17",      "Sub-kategori",   "#F472B6"),
]:
    with col:
        st.markdown(f"""
        <div class="stat-badge">
          <div style='font-family:JetBrains Mono,monospace;font-size:1.5rem;
            font-weight:700;color:{clr};'>{val}</div>
          <div style='font-size:0.72rem;color:{t["muted"]};margin-top:2px;'>{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)

# Feature cards
st.markdown(section_label("Fitur Aplikasi", t), unsafe_allow_html=True)
fc1, fc2, fc3, fc4 = st.columns(4)
for col, icon, title, desc in [
    (fc1, "📊", "Overview",
     "KPI penjualan, tren bulanan per kategori, distribusi sales, dan insight bisnis dari 4 tahun data."),
    (fc2, "🔮", "Prediksi Sales",
     "Forecast penjualan hingga target bulan tertentu dengan confidence interval — OMP, ARIMA, Theta."),
    (fc3, "📐", "Evaluasi Model",
     "Perbandingan performa model: MAE, RMSE, MAPE, R² untuk validation dan test set."),
    (fc4, "🏆", "Top Produk",
     "Ranking produk berdasarkan total sales dengan filter kategori."),
]:
    with col:
        st.markdown(f"""
        <div class="feat-card">
          <div style='font-size:1.4rem;margin-bottom:0.85rem;'>{icon}</div>
          <div style='font-family:Syne,sans-serif;font-size:0.95rem;font-weight:700;
            color:{t["text"]};margin-bottom:0.5rem;'>{title}</div>
          <div style='font-size:0.8rem;color:{t["muted"]};line-height:1.6;'>{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)

# Dataset info
st.markdown(section_label("Tentang Dataset", t), unsafe_allow_html=True)
di1, di2 = st.columns([1.6, 1])

with di1:
    stat_items = "".join([
        f'<div style="background:{stat_bg};border-radius:8px;padding:0.6rem 0.9rem;">'
        f'<div style="font-size:0.68rem;color:{t["muted"]};text-transform:uppercase;letter-spacing:0.05em;">{k}</div>'
        f'<div style="font-size:0.85rem;font-weight:600;color:{t["text"]};margin-top:1px;">{v}</div></div>'
        for k, v in [("Periode","2014 – 2017"),("Region","Amerika Serikat"),
                     ("Kategori","3 Utama"),("Sub-kategori","17 Tipe")]
    ])
    st.markdown(card_wrap(f"""
        <div style='font-family:Syne,sans-serif;font-size:1.05rem;font-weight:700;
            color:{t["text"]};margin-bottom:0.65rem;'>Superstore Sales Dataset</div>
        <p style='font-size:0.85rem;color:{t["muted"]};line-height:1.7;margin-bottom:1rem;'>
            Dataset retail populer yang mencakup transaksi penjualan sebuah superstore
            Amerika Serikat periode 2014–2017. Berisi informasi pesanan, pelanggan, produk,
            dan performa finansial yang kaya untuk analisis bisnis.
        </p>
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;'>{stat_items}</div>
    """, t), unsafe_allow_html=True)

with di2:
    cats = [
        ("#1D4ED8", "#93C5FD", "🪑 Furniture",       "Bookcases, Chairs, Tables, Storage…"),
        ("#059669", "#6EE7B7", "📎 Office Supplies",  "Binders, Paper, Art, Labels…"),
        ("#D97706", "#FCD34D", "💻 Technology",       "Phones, Copiers, Accessories…"),
    ]
    strips = "".join([
        f'<div class="ins-strip" style="border-left:3px solid {dc};">'
        f'<div style="font-size:0.78rem;font-weight:600;color:{dc if not dm else lc};">{label}</div>'
        f'<div style="font-size:0.75rem;color:{t["muted"]};margin-top:2px;">{sub}</div></div>'
        for dc, lc, label, sub in cats
    ])
    st.markdown(card_wrap(f"""
        <div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;
            color:{t["text"]};margin-bottom:1rem;'>Kategori Produk</div>
        {strips}
    """, t), unsafe_allow_html=True)

st.markdown(f"""
<div style='text-align:center;margin-top:1.75rem;font-size:0.75rem;color:{t["muted"]};'>
  Gunakan menu di sidebar untuk menjelajahi fitur PredixViz
</div>""", unsafe_allow_html=True)
