"""
pages/03_Evaluasi_Model.py
"""
import streamlit as st, pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Evaluasi Model · PredixViz", layout="wide")
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

from _theme_helper import (
    get_theme, inject_global_css, render_toggle,
    section_label, status_badge,
    ACCENT, ACCENT2, CAT_COLORS, VALID_CATEGORIES, MODEL_LABEL
)
from utils.api_client import check_health, fetch_metrics

inject_global_css()
render_toggle()
t = get_theme(); dm = t["dm"]

with st.sidebar:
    st.markdown(f"""
    <div style='padding:0.5rem 0.25rem 1.25rem;'>
      <div style='display:flex;align-items:center;gap:10px;'>
        <div style='width:36px;height:36px;background:linear-gradient(135deg,{ACCENT},{ACCENT2});
          border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;'>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"
              stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M3 6h18" stroke="white" stroke-width="2" stroke-linecap="round"/>
            <path d="M16 10a4 4 0 01-8 0" stroke="white" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div>
          <div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;color:{t["text"]};'>PredixViz</div>
          <div style='font-size:0.67rem;color:{t["muted"]};'>Retail Analytics</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown(status_badge(check_health(), t), unsafe_allow_html=True)
    st.divider()
    st.markdown(f"<div style='font-size:0.68rem;color:{t['muted']};padding:0 0.25rem;'>PredixViz · 2026</div>",
                unsafe_allow_html=True)

st.markdown("# Evaluasi Model")
st.markdown(f"<p style='color:{t['muted']};font-size:0.875rem;margin-top:-0.5rem;margin-bottom:1rem;'>"
            "Perbandingan performa model prediksi — MAE, RMSE, MAPE, R²</p>",
            unsafe_allow_html=True)

# Load metrik
all_metrics = {}
load_errors = []
prog = st.progress(0, text="Memuat metrik dari API…")
for i, cat in enumerate(VALID_CATEGORIES):
    try:
        all_metrics[cat] = fetch_metrics(cat)
    except Exception as e:
        load_errors.append(f"{cat}: {e}")
    prog.progress((i+1)/len(VALID_CATEGORIES))
prog.empty()

for err in load_errors:
    st.warning(f"⚠️ Gagal memuat metrik — {err}")

if not all_metrics:
    st.markdown(f"""
    <div style='background:{t["err_bg"]};border:1px solid {t["err_border"]};
      border-radius:12px;padding:2rem;text-align:center;'>
      <div style='font-size:2rem;margin-bottom:0.75rem;'>⚠️</div>
      <div style='font-size:1rem;font-weight:600;color:{t["err_text"]};margin-bottom:0.5rem;'>
        Tidak Ada Data Metrik</div>
      <div style='font-size:0.85rem;color:{t["muted"]};'>
        Pastikan FastAPI sudah berjalan:<br/>
        <code>uvicorn api.main:app --reload</code>
      </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# Tabel perbandingan
st.markdown(section_label("Perbandingan Semua Model", t), unsafe_allow_html=True)

def build_rows(metric_key):
    rows = []
    for cat, m in all_metrics.items():
        met = m.get(metric_key, {}) or {}
        rows.append({
            "Kategori" : cat,
            "Model"    : m.get("model_used", MODEL_LABEL.get(cat,"—")),
            "MAE"      : f'Rp {met["mae"]:,.2f}'   if met.get("mae")  is not None else "—",
            "RMSE"     : f'Rp {met["rmse"]:,.2f}'  if met.get("rmse") is not None else "—",
            "MAPE (%)" : f'{met["mape"]:.2f}%'     if met.get("mape") is not None else "—",
            "R²"       : f'{met["r2"]:.4f}'        if met.get("r2")   is not None else "—",
        })
    return pd.DataFrame(rows)

tab_val, tab_test = st.tabs(["📊 Validation", "🧪 Test"])
with tab_val:
    df_v = build_rows("val_metrics")
    st.dataframe(df_v if not df_v.empty else pd.DataFrame(), use_container_width=True, hide_index=True)
with tab_test:
    df_te = build_rows("test_metrics")
    st.dataframe(df_te if not df_te.empty else pd.DataFrame(), use_container_width=True, hide_index=True)

st.divider()

# Detail per kategori
st.markdown(section_label("Detail per Kategori", t), unsafe_allow_html=True)
sel = st.selectbox("Pilih Kategori", list(all_metrics.keys()), label_visibility="collapsed")

if sel in all_metrics:
    m    = all_metrics[sel]
    val  = m.get("val_metrics",  {}) or {}
    test = m.get("test_metrics", {}) or {}

    st.markdown(f"<div style='font-size:0.8rem;color:{t['text']};margin-bottom:1rem;'>"
                f"Model: <code>{m.get('model_used','—')}</code> &nbsp;·&nbsp; Kategori: <b>{sel}</b></div>",
                unsafe_allow_html=True)

    for label, met in [("Validation", val), ("Test", test)]:
        st.markdown(f"<div style='font-size:0.75rem;font-weight:600;color:{t['muted']};"
                    f"text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;'>{label}</div>",
                    unsafe_allow_html=True)
        mc1,mc2,mc3,mc4 = st.columns(4)
        mc1.metric("MAE",  f'Rp {met["mae"]:,.2f}'  if met.get("mae")  is not None else "—")
        mc2.metric("RMSE", f'Rp {met["rmse"]:,.2f}' if met.get("rmse") is not None else "—")
        mc3.metric("MAPE", f'{met["mape"]:.2f}%'    if met.get("mape") is not None else "—")
        mc4.metric("R²",   f'{met["r2"]:.4f}'       if met.get("r2")   is not None else "—")
        st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)

    if val and test:
        color = CAT_COLORS.get(sel, "#1D4ED8")
        fig = go.Figure()
        for label, met, clr in [("Validation",val,color),("Test",test,ACCENT)]:
            vals = [met.get(k,0) or 0 for k in ["mae","rmse"]]
            fig.add_trace(go.Bar(
                name=label, x=["MAE","RMSE"], y=vals,
                marker_color=clr,
                text=[f"Rp {v:,.0f}" for v in vals],
                textposition="outside",
                textfont=dict(size=11, color=t["text"]),
            ))
        fig.update_layout(
            barmode="group", height=280,
            title=dict(text=f"MAE & RMSE — {sel}",
                       font=dict(size=13,family="Syne",color=t["text"]),x=0),
            plot_bgcolor=t["plot_bg"], paper_bgcolor=t["plot_paper"],
            yaxis=dict(tickformat=",.0f", showgrid=True, gridcolor=t["grid"],
                       title="Rp", titlefont=dict(color=t["tick"]),
                       tickfont=dict(color=t["tick"])),
            xaxis=dict(showgrid=False, tickfont=dict(color=t["tick"])),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        font=dict(color=t["text"])),
            margin=dict(l=10,r=10,t=50,b=10),
            font=dict(family="DM Sans", color=t["text"]),
        )
        st.plotly_chart(fig, use_container_width=True)
