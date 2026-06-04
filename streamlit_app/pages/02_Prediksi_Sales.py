"""
pages/02_Prediksi_Sales.py
Forecast sales per kategori dengan confidence interval + input periode custom
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.api_client import fetch_forecast, predict_sales_next, fetch_sales_monthly, VALID_CATEGORIES

st.set_page_config(page_title="Prediksi Sales · PredixViz", layout="wide")

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
h1,h2,h3{{font-family:'Syne',sans-serif!important;color:{text_main}!important;}}
h1{{font-size:1.6rem!important;font-weight:700!important;}}
[data-testid="stSelectbox"]>div>div{{background:{bg_card}!important;border-color:{border_c}!important;color:{text_main}!important;}}
[data-testid="stNumberInput"]>div>div>input{{background:{bg_card}!important;border-color:{border_c}!important;color:{text_main}!important;}}
.stButton>button{{background:{accent};color:white;border:none;border-radius:8px;font-family:'DM Sans',sans-serif;font-size:0.875rem;font-weight:500;padding:0.5rem 1.25rem;transition:all 0.15s;width:100%;}}
.stButton>button:hover{{background:#4F46E5;transform:translateY(-1px);box-shadow:0 4px 12px rgba(99,102,241,0.3);}}
p,li,div,span,label{{color:{text_main}!important;}}
</style>
""", unsafe_allow_html=True)

st.markdown("# Prediksi Sales")
st.markdown(f"<p style='color:{text_mute};font-size:0.875rem;margin-top:-0.5rem;'>Forecast penjualan per kategori dengan confidence interval</p>", unsafe_allow_html=True)
st.divider()

COLORS      = {"Furniture": "#1D4ED8", "Office Supplies": "#059669", "Technology": "#D97706"}
MODEL_LABEL = {"Furniture": "OMP", "Office Supplies": "ARIMA", "Technology": "Theta"}

# Catatan pemodelan multi-periode
st.markdown(f"""
<div style='background:{"rgba(99,102,241,0.1)" if dm else "#EEF2FF"};border:1px solid {"rgba(99,102,241,0.25)" if dm else "#C7D2FE"};
  border-radius:10px;padding:0.85rem 1.1rem;margin-bottom:1.25rem;font-size:0.82rem;color:{text_mute};line-height:1.6;'>
  <b style='color:{accent};'>ℹ️ Multi-Periode Forecast:</b> Gunakan slider "<b>Jumlah Periode</b>" untuk memilih berapa bulan ke depan yang ingin diprediksi (1–24 bulan).
  Model akan melakukan recursive forecasting — setiap prediksi menjadi input untuk periode berikutnya.
  Semakin panjang horizon, confidence interval akan semakin melebar.
</div>
""", unsafe_allow_html=True)

col_form, col_result = st.columns([1, 2.8])

with col_form:
    st.markdown(f"<div style='font-size:0.68rem;font-weight:700;color:{text_mute};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;'>Parameter Prediksi</div>", unsafe_allow_html=True)

    category = st.selectbox("Kategori", VALID_CATEGORIES, label_visibility="collapsed")

    st.markdown(f"""
    <div style='background:{"rgba(99,102,241,0.1)" if dm else "#EFF6FF"};border:1px solid {"rgba(99,102,241,0.2)" if dm else "#BFDBFE"};border-radius:8px;
        padding:8px 12px;font-size:0.8rem;color:{"#A5B4FC" if dm else "#1E40AF"};margin:0.5rem 0;'>
        Model: <strong>{MODEL_LABEL[category]}</strong>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:0.75rem;color:{text_main};font-weight:500;margin-bottom:0.25rem;'>Jumlah Periode (Bulan)</div>", unsafe_allow_html=True)
    n_periods = st.slider("Jumlah Periode", min_value=1, max_value=24, value=6,
                          label_visibility="collapsed",
                          help="1–24 bulan ke depan")

    st.markdown(f"<div style='font-size:0.75rem;color:{text_mute};margin-bottom:0.75rem;'>Forecast <b style='color:{accent};'>{n_periods}</b> bulan ke depan</div>", unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:0.75rem;color:{text_main};font-weight:500;margin-bottom:0.25rem;'>Prediksi 1 Periode Berikutnya</div>", unsafe_allow_html=True)
    run_single = st.button("Prediksi Cepat", key="btn_single")

    st.markdown(f"<div style='margin-top:0.75rem;'></div>", unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:0.75rem;color:{text_main};font-weight:500;margin-bottom:0.25rem;'>Forecast {n_periods} Periode</div>", unsafe_allow_html=True)
    run_forecast = st.button("Tampilkan Forecast", key="btn_forecast")

with col_result:
    if run_single:
        with st.spinner("Memproses..."):
            try:
                res = predict_sales_next(category)
                st.markdown(f"""
                <div style='background:{"rgba(74,222,128,0.08)" if dm else "#F0FDF4"};border:1px solid {"rgba(74,222,128,0.2)" if dm else "#BBF7D0"};border-radius:10px;
                    padding:1rem 1.25rem;'>
                    <div style='font-size:0.7rem;font-weight:700;color:{"#4ADE80" if dm else "#166534"};
                        text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.25rem;'>
                        Prediksi Sales Berikutnya
                    </div>
                    <div style='font-size:1.5rem;font-weight:700;color:{text_main};
                        font-family:JetBrains Mono,monospace;'>
                        Rp {res['predicted_sales']:,.2f}
                    </div>
                    <div style='font-size:0.75rem;color:{text_mute};margin-top:0.25rem;'>
                        {res['category']} &nbsp;·&nbsp; Model: {res['model_used']}
                    </div>
                </div>""", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

    if run_forecast:
        with st.spinner("Memuat forecast..."):
            try:
                data         = fetch_forecast(category)
                df_fore_all  = pd.DataFrame(data["forecast"])
                model_used   = data["model_used"]
                color        = COLORS.get(category, "#1D4ED8")

                # Potong ke n_periods yang dipilih user
                df_fore = df_fore_all.head(n_periods)

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

                # Confidence interval
                fig.add_trace(go.Scatter(
                    x=list(df_fore["period"]) + list(df_fore["period"])[::-1],
                    y=list(df_fore["upper_bound"]) + list(df_fore["lower_bound"])[::-1],
                    fill="toself",
                    fillcolor="rgba(99,102,241,0.1)",
                    line=dict(color="rgba(0,0,0,0)"),
                    name="Confidence Interval",
                    showlegend=True,
                ))

                for bound_col, label in [("upper_bound","Upper Bound"),("lower_bound","Lower Bound")]:
                    fig.add_trace(go.Scatter(
                        x=df_fore["period"], y=df_fore[bound_col],
                        line=dict(color="#6366F1", width=1, dash="dot"),
                        mode="lines", showlegend=False, name=label,
                    ))

                if has_hist:
                    fig.add_trace(go.Scatter(
                        x=df_hist["ym"], y=df_hist["total_sales"],
                        name="Historis", line=dict(color=color, width=2.5),
                        mode="lines+markers",
                        marker=dict(size=5, symbol="circle", line=dict(width=1.5, color=color)),
                    ))

                fig.add_trace(go.Scatter(
                    x=df_fore["period"], y=df_fore["forecast_sales"],
                    name=f"Forecast ({model_used}) — {n_periods} bln",
                    line=dict(color="#6366F1", width=2.5, dash="dash"),
                    mode="lines+markers",
                    marker=dict(size=8, symbol="circle-open", line=dict(width=2, color="#6366F1")),
                ))

                fig.update_layout(
                    title=dict(text=f"Forecast Sales — {category} ({n_periods} Periode)", font=dict(size=14, family="Syne", color=text_main), x=0),
                    height=380, hovermode="x unified",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=11, color=text_main)),
                    xaxis=dict(showgrid=False, tickfont=dict(size=11, color=tick_c)),
                    yaxis=dict(showgrid=True, gridcolor=grid_c, tickformat=",.0f",
                               tickfont=dict(size=11, color=tick_c)),
                    plot_bgcolor=plot_bg, paper_bgcolor=plot_paper,
                    margin=dict(l=10, r=10, t=55, b=10),
                    font=dict(family="DM Sans"),
                )
                st.plotly_chart(fig, use_container_width=True)

                st.markdown(f"<div style='font-size:0.68rem;font-weight:700;color:{text_mute};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;'>Detail Forecast — {n_periods} Periode</div>", unsafe_allow_html=True)
                df_show = df_fore.copy()
                df_show.columns = ["Periode", "Forecast Sales", "Lower Bound", "Upper Bound"]
                for c in ["Forecast Sales", "Lower Bound", "Upper Bound"]:
                    df_show[c] = df_show[c].apply(lambda x: f"Rp {x:,.2f}")
                st.dataframe(df_show, use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"Error: {e}")

    if not run_single and not run_forecast:
        st.markdown(f"""
        <div style='text-align:center;padding:60px 20px;background:{bg_card};
            border-radius:12px;border:1px dashed {border_c};'>
            <div style='font-size:2rem;margin-bottom:0.75rem;'>🔮</div>
            <div style='font-size:0.875rem;color:{text_mute};'>
                Pilih kategori &amp; jumlah periode, lalu klik salah satu tombol prediksi
            </div>
        </div>""", unsafe_allow_html=True)
