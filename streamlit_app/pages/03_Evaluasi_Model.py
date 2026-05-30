"""
pages/03_Evaluasi_Model.py
Tampilkan metrik evaluasi model: MAE, RMSE, MAPE, R²
Endpoint: GET /predict/metrics/{category}
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import fetch_metrics, VALID_CATEGORIES

st.set_page_config(page_title="Evaluasi Model · Superstore", page_icon="📋", layout="wide")

st.markdown("## 📋 Evaluasi Model")
st.markdown("Perbandingan performa model prediksi per kategori")
st.divider()

# ── Load semua metrik sekaligus ──
all_metrics = {}
errors      = []

with st.spinner("Memuat metrik semua model..."):
    for cat in VALID_CATEGORIES:
        try:
            all_metrics[cat] = fetch_metrics(cat)
        except Exception as e:
            errors.append(f"{cat}: {e}")

if errors:
    for err in errors:
        st.warning(f"⚠️ Gagal load metrik — {err}")

if not all_metrics:
    st.error("Tidak ada data metrik. Pastikan FastAPI sudah jalan.")
    st.stop()

# ════════════════════════════════
#   RINGKASAN: Tabel perbandingan semua model
# ════════════════════════════════
st.markdown("### Perbandingan Semua Model")

model_map = {"Furniture": "OMP", "Office Supplies": "ARIMA", "Technology": "Theta"}
rows_val, rows_test = [], []

for cat, m in all_metrics.items():
    val  = m.get("val_metrics",  {})
    test = m.get("test_metrics", {})

    rows_val.append({
        "Kategori"   : cat,
        "Model"      : m.get("model_used", model_map.get(cat, "—")),
        "MAE"        : val.get("mae",  "—"),
        "RMSE"       : val.get("rmse", "—"),
        "MAPE (%)"   : val.get("mape", "—"),
        "R²"         : val.get("r2",   "—"),
    })
    rows_test.append({
        "Kategori"   : cat,
        "Model"      : m.get("model_used", model_map.get(cat, "—")),
        "MAE"        : test.get("mae",  "—"),
        "RMSE"       : test.get("rmse", "—"),
        "MAPE (%)"   : test.get("mape", "—"),
        "R²"         : test.get("r2",   "—"),
    })

tab_val, tab_test = st.tabs(["📊 Validation Metrics", "🧪 Test Metrics"])

def format_metrics_df(rows):
    df = pd.DataFrame(rows)
    for col in ["MAE", "RMSE"]:
        df[col] = df[col].apply(lambda x: f"Rp {x:,.2f}" if isinstance(x, (int, float)) else x)
    for col in ["MAPE (%)", "R²"]:
        df[col] = df[col].apply(lambda x: f"{x:.4f}" if isinstance(x, (int, float)) else x)
    return df

with tab_val:
    st.dataframe(format_metrics_df(rows_val), use_container_width=True, hide_index=True)

with tab_test:
    st.dataframe(format_metrics_df(rows_test), use_container_width=True, hide_index=True)

st.divider()

# ════════════════════════════════
#   DETAIL PER KATEGORI
# ════════════════════════════════
st.markdown("### Detail per Kategori")

sel_cat = st.selectbox("Pilih Kategori", VALID_CATEGORIES, key="eval_cat")

if sel_cat in all_metrics:
    m = all_metrics[sel_cat]
    val  = m.get("val_metrics",  {})
    test = m.get("test_metrics", {})

    st.markdown(f"**Model**: `{m.get('model_used', '—')}` &nbsp;·&nbsp; **Kategori**: {sel_cat}")
    if m.get("params"):
        st.caption(f"Parameter: {m['params']}")

    # Metric cards: 4 kolom, validation vs test
    st.markdown("#### Validation Metrics")
    cv1, cv2, cv3, cv4 = st.columns(4)
    cv1.metric("MAE",     f"Rp {val.get('mae',0):,.2f}"  if val.get('mae')  else "—")
    cv2.metric("RMSE",    f"Rp {val.get('rmse',0):,.2f}" if val.get('rmse') else "—")
    cv3.metric("MAPE",    f"{val.get('mape',0):.2f}%"    if val.get('mape') else "—")
    cv4.metric("R²",      f"{val.get('r2',0):.4f}"       if val.get('r2')   is not None else "—")

    st.markdown("#### Test Metrics")
    ct1, ct2, ct3, ct4 = st.columns(4)
    ct1.metric("MAE",     f"Rp {test.get('mae',0):,.2f}"  if test.get('mae')  else "—")
    ct2.metric("RMSE",    f"Rp {test.get('rmse',0):,.2f}" if test.get('rmse') else "—")
    ct3.metric("MAPE",    f"{test.get('mape',0):.2f}%"    if test.get('mape') else "—")
    ct4.metric("R²",      f"{test.get('r2',0):.4f}"       if test.get('r2')   is not None else "—")

    # Bar chart perbandingan val vs test
    if val and test:
        st.markdown("#### Visualisasi Val vs Test")
        metrics_to_plot = ["mae", "rmse"]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Validation",
            x=[m.upper() for m in metrics_to_plot],
            y=[val.get(m, 0) for m in metrics_to_plot],
            marker_color="#185FA5",
        ))
        fig.add_trace(go.Bar(
            name="Test",
            x=[m.upper() for m in metrics_to_plot],
            y=[test.get(m, 0) for m in metrics_to_plot],
            marker_color="#6366F1",
        ))
        fig.update_layout(
            barmode="group", height=280,
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(tickformat=",.0f", title="Rp"),
            margin=dict(l=0, r=0, t=20, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)
