"""
pages/02_Prediksi_Sales.py
Forecast sales per kategori dengan confidence interval
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.api_client import fetch_forecast, predict_sales_next, fetch_sales_monthly, VALID_CATEGORIES

st.set_page_config(page_title="Prediksi Sales · Superstore", layout="wide")

st.markdown("# Prediksi Sales")
st.markdown("<p style='color:#6B7280;font-size:0.875rem;margin-top:-0.5rem;'>Forecast penjualan per kategori dengan confidence interval</p>", unsafe_allow_html=True)
st.divider()

COLORS      = {"Furniture": "#1D4ED8", "Office Supplies": "#059669", "Technology": "#D97706"}
MODEL_LABEL = {"Furniture": "OMP", "Office Supplies": "ARIMA", "Technology": "Theta"}

col_form, col_result = st.columns([1, 2.8])

with col_form:
    st.markdown("<div style='font-size:0.7rem;font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;'>Parameter</div>", unsafe_allow_html=True)

    category = st.selectbox("Kategori", VALID_CATEGORIES, label_visibility="collapsed")

    st.markdown(f"""
    <div style='background:#EFF6FF;border:1px solid #BFDBFE;border-radius:6px;
        padding:8px 12px;font-size:0.8rem;color:#1E40AF;margin:0.5rem 0;'>
        Model: <strong>{MODEL_LABEL[category]}</strong>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.75rem;color:#374151;font-weight:500;margin-bottom:0.25rem;'>Prediksi 1 Periode Berikutnya</div>", unsafe_allow_html=True)
    run_single = st.button("Prediksi Cepat", key="btn_single")

    st.markdown("<div style='margin-top:0.75rem;'></div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.75rem;color:#374151;font-weight:500;margin-bottom:0.25rem;'>Forecast Semua Periode</div>", unsafe_allow_html=True)
    run_forecast = st.button("Tampilkan Forecast", key="btn_forecast")

with col_result:
    if run_single:
        with st.spinner("Memproses..."):
            try:
                res = predict_sales_next(category)
                st.markdown(f"""
                <div style='background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;
                    padding:1rem 1.25rem;'>
                    <div style='font-size:0.75rem;font-weight:600;color:#166534;
                        text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.25rem;'>
                        Prediksi Sales Berikutnya
                    </div>
                    <div style='font-size:1.5rem;font-weight:700;color:#111827;
                        font-family:monospace;'>
                        Rp {res['predicted_sales']:,.2f}
                    </div>
                    <div style='font-size:0.75rem;color:#6B7280;margin-top:0.25rem;'>
                        {res['category']} &nbsp;·&nbsp; Model: {res['model_used']}
                    </div>
                </div>""", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

    if run_forecast:
        with st.spinner("Memuat forecast..."):
            try:
                data         = fetch_forecast(category)
                df_fore      = pd.DataFrame(data["forecast"])
                model_used   = data["model_used"]
                color        = COLORS.get(category, "#1D4ED8")

                # Ambil historis
                try:
                    hist    = fetch_sales_monthly(category=category)
                    df_hist = pd.DataFrame(hist["data"])
                    df_hist["ym"] = df_hist["year"].astype(str) + "-" + df_hist["month"].astype(str).str.zfill(2)
                    df_hist = df_hist.sort_values("ym")
                    has_hist = True
                except Exception:
                    has_hist = False

                fig = go.Figure()

                # Confidence interval area
                fig.add_trace(go.Scatter(
                    x=list(df_fore["period"]) + list(df_fore["period"])[::-1],
                    y=list(df_fore["upper_bound"]) + list(df_fore["lower_bound"])[::-1],
                    fill="toself",
                    fillcolor="rgba(99,102,241,0.08)",
                    line=dict(color="rgba(0,0,0,0)"),
                    name="Confidence Interval",
                    showlegend=True,
                ))

                # Upper / lower bound
                for bound_col, label in [("upper_bound","Upper Bound"),("lower_bound","Lower Bound")]:
                    fig.add_trace(go.Scatter(
                        x=df_fore["period"], y=df_fore[bound_col],
                        line=dict(color="#6366F1", width=1, dash="dot"),
                        mode="lines", showlegend=False, name=label,
                    ))

                # Historis
                if has_hist:
                    fig.add_trace(go.Scatter(
                        x=df_hist["ym"], y=df_hist["total_sales"],
                        name="Historis", line=dict(color=color, width=2),
                        mode="lines+markers", marker=dict(size=3),
                    ))

                # Forecast
                fig.add_trace(go.Scatter(
                    x=df_fore["period"], y=df_fore["forecast_sales"],
                    name=f"Forecast ({model_used})",
                    line=dict(color="#6366F1", width=2.5, dash="dash"),
                    mode="lines+markers",
                    marker=dict(size=6, symbol="circle-open", line=dict(width=2, color="#6366F1")),
                ))

                fig.update_layout(
                    title=dict(text=f"Forecast Sales — {category}", font=dict(size=14, family="Inter"), x=0),
                    height=360, hovermode="x unified",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=11)),
                    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
                    yaxis=dict(showgrid=True, gridcolor="#F3F4F6", tickformat=",.0f", tickfont=dict(size=11)),
                    plot_bgcolor="white", paper_bgcolor="white",
                    margin=dict(l=0, r=0, t=50, b=0),
                    font=dict(family="Inter"),
                )
                st.plotly_chart(fig, use_container_width=True)

                # Tabel detail
                st.markdown("<div style='font-size:0.7rem;font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;'>Detail Forecast</div>", unsafe_allow_html=True)
                df_show = df_fore.copy()
                df_show.columns = ["Periode", "Forecast Sales", "Lower Bound", "Upper Bound"]
                for c in ["Forecast Sales", "Lower Bound", "Upper Bound"]:
                    df_show[c] = df_show[c].apply(lambda x: f"Rp {x:,.2f}")
                st.dataframe(df_show, use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"Error: {e}")

    if not run_single and not run_forecast:
        st.markdown("""
        <div style='text-align:center;padding:60px 20px;background:#F9FAFB;
            border-radius:8px;border:1px dashed #E5E7EB;'>
            <div style='font-size:0.875rem;color:#9CA3AF;'>
                Pilih kategori dan klik salah satu tombol prediksi
            </div>
        </div>""", unsafe_allow_html=True)
