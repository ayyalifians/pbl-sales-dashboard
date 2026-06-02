"""
app.py — Entry point Streamlit
Jalankan: streamlit run streamlit_app/app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 1.25rem 1.5rem !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
[data-testid="stMetricLabel"] p {
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    color: #6B7280 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: #111827 !important;
}

.stButton > button {
    background: #1D4ED8;
    color: white;
    border: none;
    border-radius: 6px;
    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;
    font-weight: 500;
    padding: 0.5rem 1.25rem;
    transition: background 0.15s;
    width: 100%;
}
.stButton > button:hover { background: #1E40AF; border: none; }

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

h1 {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: #111827 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style='padding:0 0.5rem 1rem;'>
        <div style='display:flex;align-items:center;gap:10px;'>
            <div style='width:32px;height:32px;background:#1D4ED8;border-radius:6px;
                display:flex;align-items:center;justify-content:center;
                color:white;font-size:15px;font-weight:700;flex-shrink:0;'>S</div>
            <div>
                <div style='font-size:0.875rem;font-weight:600;color:#111827;line-height:1.2;'>Superstore</div>
                <div style='font-size:0.7rem;color:#9CA3AF;'>Sales Analytics</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    from utils.api_client import check_health
    if check_health():
        st.markdown("""<div style='display:flex;align-items:center;gap:8px;padding:8px 12px;
            background:#F0FDF4;border:1px solid #BBF7D0;border-radius:6px;
            font-size:0.8rem;color:#166534;font-weight:500;'>
            <div style='width:7px;height:7px;border-radius:50%;background:#16A34A;flex-shrink:0;'></div>
            API terhubung</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style='display:flex;align-items:center;gap:8px;padding:8px 12px;
            background:#FEF2F2;border:1px solid #FECACA;border-radius:6px;
            font-size:0.8rem;color:#991B1B;font-weight:500;'>
            <div style='width:7px;height:7px;border-radius:50%;background:#DC2626;flex-shrink:0;'></div>
            API tidak aktif</div>""", unsafe_allow_html=True)
        st.caption("Jalankan: `uvicorn api.main:app --reload`")

    st.divider()

    for label, items in [
        ("Dataset", [("Superstore 2014–2017", None)]),
        ("Model Prediksi", [("Furniture", "OMP"), ("Office Supplies", "ARIMA"), ("Technology", "Theta")]),
    ]:
        st.markdown(f"<div style='font-size:0.7rem;font-weight:600;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.05em;padding:0 0.25rem;margin-bottom:0.4rem;'>{label}</div>", unsafe_allow_html=True)
        for name, val in items:
            if val:
                st.markdown(f"<div style='font-size:0.8rem;color:#374151;padding:2px 0.25rem;'>{name} <span style='color:#D1D5DB;'>→</span> <code style='color:#1D4ED8;font-size:0.75rem;'>{val}</code></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='font-size:0.8rem;color:#374151;padding:2px 0.25rem;'>{name}</div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='font-size:0.7rem;color:#9CA3AF;padding:0 0.25rem;'>PBL Kelompok 6 · 2025</div>", unsafe_allow_html=True)

# ── Home ──
st.markdown("# Superstore Sales Dashboard")
st.markdown("<p style='color:#6B7280;font-size:0.875rem;margin-top:-0.5rem;margin-bottom:1.5rem;'>Sistem prediksi dan monitoring penjualan berbasis machine learning</p>", unsafe_allow_html=True)
st.divider()

c1, c2, c3 = st.columns(3)
for col, title, desc in [
    (c1, "Overview", "KPI penjualan, tren bulanan per kategori, distribusi sales, dan insight bisnis"),
    (c2, "Prediksi Sales", "Forecast penjualan dengan confidence interval menggunakan model OMP, ARIMA, dan Theta"),
    (c3, "Evaluasi Model", "Perbandingan performa model: MAE, RMSE, MAPE, dan R² per kategori"),
]:
    with col:
        st.markdown(f"""
        <div style='border:1px solid #E5E7EB;border-radius:8px;padding:1.25rem;background:white;height:100%;'>
            <div style='font-size:0.7rem;font-weight:600;color:#6B7280;text-transform:uppercase;
                letter-spacing:0.05em;margin-bottom:0.5rem;'>{title}</div>
            <div style='font-size:0.85rem;color:#374151;line-height:1.6;'>{desc}</div>
        </div>""", unsafe_allow_html=True)
