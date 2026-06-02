"""
pages/03_Evaluasi_Model.py
Perbandingan performa model: MAE, RMSE, MAPE, R²
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.api_client import fetch_metrics, VALID_CATEGORIES

st.set_page_config(page_title="Evaluasi Model · Superstore", layout="wide")

st.markdown("# Evaluasi Model")
st.markdown("<p style='color:#6B7280;font-size:0.875rem;margin-top:-0.5rem;'>Perbandingan performa model prediksi per kategori</p>", unsafe_allow_html=True)
st.divider()

MODEL_LABEL = {"Furniture": "OMP", "Office Supplies": "ARIMA", "Technology": "Theta"}
COLORS      = {"Furniture": "#1D4ED8", "Office Supplies": "#059669", "Technology": "#D97706"}

# Load semua metrik
all_metrics = {}
with st.spinner("Memuat metrik..."):
    for cat in VALID_CATEGORIES:
        try:
            all_metrics[cat] = fetch_metrics(cat)
        except Exception as e:
            st.warning(f"Gagal load metrik {cat}: {e}")

if not all_metrics:
    st.error("Tidak ada data metrik. Pastikan FastAPI sudah jalan.")
    st.stop()

# ════════════════════════════════
#   TABEL PERBANDINGAN
# ════════════════════════════════
st.markdown("<div style='font-size:0.7rem;font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.75rem;'>Perbandingan Semua Model</div>", unsafe_allow_html=True)

tab_val, tab_test = st.tabs(["Validation", "Test"])

def build_rows(metric_key):
    rows = []
    for cat, m in all_metrics.items():
        met = m.get(metric_key, {})
        rows.append({
            "Kategori" : cat,
            "Model"    : m.get("model_used", MODEL_LABEL.get(cat, "—")),
            "MAE"      : f"Rp {met.get('mae',0):,.2f}"   if met.get("mae")   is not None else "—",
            "RMSE"     : f"Rp {met.get('rmse',0):,.2f}"  if met.get("rmse")  is not None else "—",
            "MAPE (%)" : f"{met.get('mape',0):.2f}%"     if met.get("mape")  is not None else "—",
            "R²"       : f"{met.get('r2',0):.4f}"        if met.get("r2")    is not None else "—",
        })
    return pd.DataFrame(rows)

with tab_val:
    st.dataframe(build_rows("val_metrics"), use_container_width=True, hide_index=True)
with tab_test:
    st.dataframe(build_rows("test_metrics"), use_container_width=True, hide_index=True)

st.divider()

# ════════════════════════════════
#   DETAIL PER KATEGORI
# ════════════════════════════════
st.markdown("<div style='font-size:0.7rem;font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.75rem;'>Detail per Kategori</div>", unsafe_allow_html=True)

sel = st.selectbox("Pilih Kategori", VALID_CATEGORIES, label_visibility="collapsed")

if sel in all_metrics:
    m    = all_metrics[sel]
    val  = m.get("val_metrics",  {})
    test = m.get("test_metrics", {})

    st.markdown(f"<div style='font-size:0.8rem;color:#374151;margin-bottom:1rem;'>Model: <code style='color:#1D4ED8;'>{m.get('model_used','—')}</code> &nbsp;·&nbsp; Kategori: {sel}</div>", unsafe_allow_html=True)

    for label, met in [("Validation", val), ("Test", test)]:
        st.markdown(f"<div style='font-size:0.75rem;font-weight:500;color:#374151;margin-bottom:0.5rem;'>{label}</div>", unsafe_allow_html=True)
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("MAE",    f"Rp {met.get('mae',0):,.2f}"  if met.get('mae')  is not None else "—")
        mc2.metric("RMSE",   f"Rp {met.get('rmse',0):,.2f}" if met.get('rmse') is not None else "—")
        mc3.metric("MAPE",   f"{met.get('mape',0):.2f}%"    if met.get('mape') is not None else "—")
        mc4.metric("R²",     f"{met.get('r2',0):.4f}"       if met.get('r2')   is not None else "—")
        st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)

    # Bar chart val vs test
    if val and test:
        metrics_keys = ["mae", "rmse"]
        fig = go.Figure()
        color = COLORS.get(sel, "#1D4ED8")
        for label, met, opacity in [("Validation", val, 1.0), ("Test", test, 0.6)]:
            fig.add_trace(go.Bar(
                name=label,
                x=[k.upper() for k in metrics_keys],
                y=[met.get(k, 0) for k in metrics_keys],
                marker_color=color,
                opacity=opacity,
                text=[f"Rp {met.get(k,0):,.0f}" for k in metrics_keys],
                textposition="outside",
                textfont=dict(size=11),
            ))
        fig.update_layout(
            barmode="group", height=260,
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(tickformat=",.0f", showgrid=True,
                       gridcolor="#F3F4F6", title="Rp"),
            xaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            margin=dict(l=0, r=0, t=30, b=0),
            font=dict(family="Inter", size=12),
        )
        st.plotly_chart(fig, use_container_width=True)
