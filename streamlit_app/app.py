"""
app.py — Entry point Streamlit
Jalankan: streamlit run streamlit_app/app.py
Pastikan FastAPI sudah jalan: uvicorn api.main:app --reload
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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E4E7EC;
    border-radius: 10px;
    padding: 16px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,.07);
}
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 1.5rem !important;
}
.stButton > button {
    background: #185FA5; color: white; border: none;
    border-radius: 8px; font-weight: 500;
    transition: all .15s;
}
.stButton > button:hover {
    background: #1353A0;
    box-shadow: 0 4px 12px rgba(24,95,165,.3);
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("## 📦 Superstore")
    st.markdown("**Sales Analytics Dashboard**")
    st.divider()

    from utils.api_client import check_health
    if check_health():
        st.success("🟢 API terhubung")
    else:
        st.error("🔴 API tidak aktif")
        st.caption("Jalankan di terminal:")
        st.code("uvicorn api.main:app --reload", language="bash")

    st.divider()
    st.markdown("**Dataset**: Superstore 2014–2017")
    st.markdown("**Model per kategori:**")
    st.markdown("- 🪑 Furniture → **OMP**")
    st.markdown("- 📎 Office Supplies → **ARIMA**")
    st.markdown("- 💻 Technology → **Theta**")
    st.divider()
    st.caption("PBL Kelompok 6 · 2025")

# ── Halaman Home ──
st.markdown("## 📦 Superstore Sales Dashboard")
st.markdown("Gunakan **menu di sidebar kiri** untuk navigasi.")
st.divider()

c1, c2, c3 = st.columns(3)
c1.info("**📊 Overview**\n\nKPI cards, tren bulanan, sales per kategori")
c2.info("**🔮 Prediksi**\n\nForecast sales + confidence interval per kategori")
c3.info("**📋 Evaluasi Model**\n\nMAE, RMSE, MAPE, R² per model")
