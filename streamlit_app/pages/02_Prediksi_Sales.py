"""
pages/02_Prediksi_Sales.py
Forecast sales per kategori dengan confidence interval.
Endpoint:
  GET  /predict/forecast/{category}  ← grafik multi-periode
  POST /predict/predict-sales         ← prediksi 1 nilai berikutnya
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import fetch_forecast, predict_sales_next, fetch_sales_monthly, VALID_CATEGORIES

st.set_page_config(page_title="Prediksi Sales · Superstore", page_icon="💰", layout="wide")

st.markdown("## 💰 Prediksi Sales")
st.markdown("Forecast penjualan berdasarkan kategori — dengan confidence interval (lower & upper bound)")
st.divider()

col_form, col_result = st.columns([1, 2.5])

with col_form:
    st.markdown("### Parameter")
    category = st.selectbox("Kategori", VALID_CATEGORIES)

    model_info = {"Furniture": "OMP", "Office Supplies": "ARIMA", "Technology": "Theta"}
    st.info(f"Model: **{model_info[category]}**")

    st.divider()

    # Prediksi 1 langkah
    st.markdown("#### Prediksi 1 Periode Berikutnya")
    run_single = st.button("⚡ Prediksi Cepat", use_container_width=True)

    st.divider()

    # Forecast multi-periode
    st.markdown("#### Forecast Semua Periode")
    run_forecast = st.button("🔮 Lihat Forecast Lengkap", use_container_width=True)

with col_result:

    # ── Prediksi 1 nilai ──
    if run_single:
        with st.spinner("Memproses..."):
            try:
                result = predict_sales_next(category)
                st.success(f"**Prediksi sales berikutnya: Rp {result['predicted_sales']:,.2f}**")
                st.caption(f"Kategori: {result['category']} · Model: {result['model_used']}")
            except Exception as e:
                st.error(f"⚠️ Error: `{e}`")

    # ── Forecast multi-periode ──
    if run_forecast:
        with st.spinner("Memuat forecast..."):
            try:
                data         = fetch_forecast(category)
                df_fore      = pd.DataFrame(data["forecast"])
                model_used   = data["model_used"]
                total_periods = data["total_periods"]

                # Ambil historis dari DB untuk ditampilkan bersama
                try:
                    hist     = fetch_sales_monthly(category=category)
                    df_hist  = pd.DataFrame(hist["data"])
                    df_hist["ym"] = df_hist["year"].astype(str) + "-" + df_hist["month"].astype(str).str.zfill(2)
                    df_hist  = df_hist.sort_values("ym")
                    has_hist = True
                except Exception:
                    has_hist = False

                cat_color = {"Furniture":"#185FA5","Office Supplies":"#0F6E56","Technology":"#854F0B"}
                color = cat_color.get(category, "#185FA5")

                fig = go.Figure()

                # Historis
                if has_hist:
                    fig.add_trace(go.Scatter(
                        x=df_hist["ym"], y=df_hist["total_sales"],
                        name="Historis", line=dict(color=color, width=2.5),
                        mode="lines+markers", marker=dict(size=3),
                    ))

                # Confidence interval (area)
                fig.add_trace(go.Scatter(
                    x=list(df_fore["period"]) + list(df_fore["period"])[::-1],
                    y=list(df_fore["upper_bound"]) + list(df_fore["lower_bound"])[::-1],
                    fill="toself",
                    fillcolor="#6366F115",
                    line=dict(color="rgba(0,0,0,0)"),
                    name="Confidence Interval",
                    showlegend=True,
                ))

                # Upper & lower bound (tipis)
                fig.add_trace(go.Scatter(
                    x=df_fore["period"], y=df_fore["upper_bound"],
                    name="Upper Bound", line=dict(color="#6366F1", width=1, dash="dot"),
                    mode="lines", showlegend=False,
                ))
                fig.add_trace(go.Scatter(
                    x=df_fore["period"], y=df_fore["lower_bound"],
                    name="Lower Bound", line=dict(color="#6366F1", width=1, dash="dot"),
                    mode="lines", showlegend=False,
                ))

                # Forecast utama
                fig.add_trace(go.Scatter(
                    x=df_fore["period"], y=df_fore["forecast_sales"],
                    name=f"Forecast ({model_used})",
                    line=dict(color="#6366F1", width=2.5, dash="dash"),
                    mode="lines+markers",
                    marker=dict(size=6, symbol="circle-open"),
                ))

                fig.update_layout(
                    title=f"Forecast Sales — {category} ({model_used})",
                    height=400, hovermode="x unified",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02),
                    xaxis=dict(showgrid=True, gridcolor="#F1F3F5"),
                    yaxis=dict(showgrid=True, gridcolor="#F1F3F5", tickformat=",.0f"),
                    plot_bgcolor="white", paper_bgcolor="white",
                    margin=dict(l=0, r=0, t=50, b=0),
                )
                st.plotly_chart(fig, use_container_width=True)

                # ── Tabel detail forecast ──
                st.markdown(f"#### Detail Forecast — {total_periods} periode · Model: {model_used}")
                df_display = df_fore.copy()
                df_display.columns = ["Periode", "Forecast Sales (Rp)", "Lower Bound (Rp)", "Upper Bound (Rp)"]
                for col in ["Forecast Sales (Rp)", "Lower Bound (Rp)", "Upper Bound (Rp)"]:
                    df_display[col] = df_display[col].apply(lambda x: f"Rp {x:,.2f}")
                st.dataframe(df_display, use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"⚠️ Error: `{e}`")
                st.info("Pastikan FastAPI sudah jalan: `uvicorn api.main:app --reload`")

    # Empty state
    if not run_single and not run_forecast:
        st.markdown("""
        <div style='text-align:center;padding:60px 20px;background:#F8F9FA;
            border-radius:12px;border:1px dashed #E4E7EC;color:#9CA3AF;'>
            <div style='font-size:36px'>💰</div>
            <div style='margin-top:10px;font-size:14px'>
                Pilih kategori lalu klik salah satu tombol prediksi
            </div>
        </div>""", unsafe_allow_html=True)
