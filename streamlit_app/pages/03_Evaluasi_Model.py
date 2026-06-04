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

st.set_page_config(page_title="Evaluasi Model · PredixViz", layout="wide")

dm = st.session_state.get("dark_mode", False)
bg_main   = "#0F1117" if dm else "#F8FAFC"
bg_card   = "#1A1D27" if dm else "#FFFFFF"
border_c  = "#2D3148" if dm else "#E2E8F0"
text_main = "#F1F5F9" if dm else "#0F172A"
text_mute = "#94A3B8" if dm else "#64748B"
plot_bg   = "#1A1D27" if dm else "#FFFFFF"
plot_paper= "#1A1D27" if dm else "#FFFFFF"
grid_c    = "#2D3148" if dm else "#F1F5F9"
tick_c    = "#94A3B8" if dm else "#6B7280"
accent    = "#6366F1"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
html,body,[class*="css"]{{font-family:'DM Sans',sans-serif;background:{bg_main}!important;color:{text_main}!important;}}
#MainMenu,footer,header{{visibility:hidden;}}.stDeployButton{{display:none;}}
.main .block-container{{padding-top:1.5rem;padding-bottom:3rem;max-width:1280px;}}
[data-testid="stMetric"]{{background:{bg_card}!important;border:1px solid {border_c}!important;border-radius:12px!important;padding:1.25rem 1.5rem!important;box-shadow:0 1px 3px rgba(0,0,0,0.08)!important;}}
[data-testid="stMetricLabel"] p{{font-size:0.7rem!important;font-weight:600!important;color:{text_mute}!important;text-transform:uppercase;letter-spacing:0.08em;}}
[data-testid="stMetricValue"]{{font-family:'JetBrains Mono',monospace!important;font-size:1.4rem!important;font-weight:600!important;color:{text_main}!important;}}
h1,h2,h3{{font-family:'Syne',sans-serif!important;color:{text_main}!important;}}
h1{{font-size:1.6rem!important;font-weight:700!important;}}
[data-testid="stSelectbox"]>div>div{{background:{bg_card}!important;border-color:{border_c}!important;color:{text_main}!important;}}
[data-testid="stTabs"] [role="tab"]{{font-family:'DM Sans',sans-serif!important;font-size:0.85rem!important;color:{text_mute}!important;}}
[data-testid="stTabs"] [role="tab"][aria-selected="true"]{{color:{accent}!important;}}
.stDataFrame{{background:{bg_card}!important;}}
p,li,div,span,label{{color:{text_main}!important;}}
</style>
""", unsafe_allow_html=True)

MODEL_LABEL = {"Furniture": "OMP", "Office Supplies": "ARIMA", "Technology": "Theta"}
COLORS      = {"Furniture": "#1D4ED8", "Office Supplies": "#059669", "Technology": "#D97706"}

st.markdown("# Evaluasi Model")
st.markdown(f"<p style='color:{text_mute};font-size:0.875rem;margin-top:-0.5rem;'>Perbandingan performa model prediksi per kategori</p>", unsafe_allow_html=True)
st.divider()

# Load semua metrik dengan error handling yang lebih baik
all_metrics = {}
load_errors = []

progress_text = "Memuat metrik dari API..."
progress_bar = st.progress(0, text=progress_text)

for i, cat in enumerate(VALID_CATEGORIES):
    try:
        all_metrics[cat] = fetch_metrics(cat)
        progress_bar.progress((i+1)/len(VALID_CATEGORIES), text=f"Memuat metrik {cat}...")
    except Exception as e:
        load_errors.append(f"{cat}: {e}")
        progress_bar.progress((i+1)/len(VALID_CATEGORIES), text=f"Gagal load {cat}: {e}")

progress_bar.empty()

if load_errors:
    for err in load_errors:
        st.warning(f"⚠️ Gagal memuat metrik — {err}")

if not all_metrics:
    st.markdown(f"""
    <div style='background:{"rgba(220,38,38,0.1)" if dm else "#FEF2F2"};border:1px solid {"rgba(220,38,38,0.25)" if dm else "#FECACA"};
        border-radius:12px;padding:2rem;text-align:center;'>
        <div style='font-size:2rem;margin-bottom:0.75rem;'>⚠️</div>
        <div style='font-size:1rem;font-weight:600;color:{"#F87171" if dm else "#991B1B"};margin-bottom:0.5rem;'>Tidak Ada Data Metrik</div>
        <div style='font-size:0.85rem;color:{text_mute};'>
            Pastikan FastAPI sudah berjalan:<br/>
            <code style='background:{"rgba(255,255,255,0.1)" if dm else "#F3F4F6"};padding:2px 8px;border-radius:4px;'>uvicorn api.main:app --reload</code>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ════ TABEL PERBANDINGAN ════
st.markdown(f"<div style='font-size:0.68rem;font-weight:700;color:{text_mute};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.75rem;'>Perbandingan Semua Model</div>", unsafe_allow_html=True)

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

tab_val, tab_test = st.tabs(["📊 Validation", "🧪 Test"])

with tab_val:
    df_val = build_rows("val_metrics")
    if not df_val.empty:
        st.dataframe(df_val, use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada data validation metrics.")

with tab_test:
    df_test = build_rows("test_metrics")
    if not df_test.empty:
        st.dataframe(df_test, use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada data test metrics.")

st.divider()

# ════ DETAIL PER KATEGORI ════
st.markdown(f"<div style='font-size:0.68rem;font-weight:700;color:{text_mute};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.75rem;'>Detail per Kategori</div>", unsafe_allow_html=True)

sel = st.selectbox("Pilih Kategori", list(all_metrics.keys()), label_visibility="collapsed")

if sel in all_metrics:
    m    = all_metrics[sel]
    val  = m.get("val_metrics",  {}) or {}
    test = m.get("test_metrics", {}) or {}

    st.markdown(f"<div style='font-size:0.8rem;color:{text_main};margin-bottom:1rem;'>Model: <code style='color:{accent};'>{m.get('model_used','—')}</code> &nbsp;·&nbsp; Kategori: <b>{sel}</b></div>", unsafe_allow_html=True)

    for label, met in [("Validation", val), ("Test", test)]:
        st.markdown(f"<div style='font-size:0.78rem;font-weight:600;color:{text_mute};margin-bottom:0.5rem;text-transform:uppercase;letter-spacing:0.05em;'>{label}</div>", unsafe_allow_html=True)
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
        clr2  = "#6366F1"
        for label, met, clr, opacity in [("Validation", val, color, 1.0), ("Test", test, clr2, 1.0)]:
            valid_vals = [met.get(k, 0) or 0 for k in metrics_keys]
            fig.add_trace(go.Bar(
                name=label,
                x=[k.upper() for k in metrics_keys],
                y=valid_vals,
                marker_color=clr,
                opacity=opacity,
                text=[f"Rp {v:,.0f}" for v in valid_vals],
                textposition="outside",
                textfont=dict(size=11, color=text_main),
            ))
        fig.update_layout(
            barmode="group", height=280,
            title=dict(text=f"MAE & RMSE — {sel}", font=dict(size=13, family="Syne", color=text_main), x=0),
            plot_bgcolor=plot_bg, paper_bgcolor=plot_paper,
            yaxis=dict(tickformat=",.0f", showgrid=True,
                       gridcolor=grid_c, title="Rp",
                       titlefont=dict(color=tick_c),
                       tickfont=dict(color=tick_c)),
            xaxis=dict(showgrid=False, tickfont=dict(color=tick_c)),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color=text_main)),
            margin=dict(l=10, r=10, t=50, b=10),
            font=dict(family="DM Sans", size=12, color=text_main),
        )
        st.plotly_chart(fig, use_container_width=True)
