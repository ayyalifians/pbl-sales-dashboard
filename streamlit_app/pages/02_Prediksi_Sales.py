"""
pages/02_Prediksi_Sales.py
Forecast ke target bulan/tahun tertentu — input spesifik user.
"""
import streamlit as st, pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime

st.set_page_config(page_title="Prediksi Sales · PredixViz", layout="wide")
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

from _theme_helper import (
    get_theme, inject_global_css, render_toggle,
    section_label, info_banner, status_badge, card_wrap,
    ACCENT, ACCENT2, CAT_COLORS, VALID_CATEGORIES, MODEL_LABEL
)
from api_client import check_health, fetch_forecast, fetch_sales_monthly

inject_global_css()
render_toggle()
t = get_theme(); dm = t["dm"]

# ── Sidebar ───────────────────────────────────────────────────────────────
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

# ── Header ────────────────────────────────────────────────────────────────
st.markdown("# Prediksi Sales")
st.markdown(f"<p style='color:{t['muted']};font-size:0.875rem;margin-top:-0.5rem;margin-bottom:1rem;'>"
            "Forecast penjualan per kategori hingga target bulan yang ditentukan</p>",
            unsafe_allow_html=True)

# ── Info banner: penjelasan forecast vs prediksi ─────────────────────────
with st.expander("ℹ️ Tentang Forecast & Model", expanded=False):
    st.markdown(f"""
    <div style='font-size:0.85rem;color:{t["muted"]};line-height:1.75;'>
    <b style='color:{t["text"]};'>Forecast vs Prediksi Cepat</b><br/>
    Fitur ini menggunakan <b>forecast multi-periode</b> — model menghasilkan rangkaian prediksi
    beberapa bulan sekaligus disertai <i>confidence interval</i> (batas atas & bawah).
    Berbeda dari "prediksi 1 langkah" yang hanya menghasilkan satu angka,
    forecast menunjukkan <i>tren ke depan</i> yang berguna untuk perencanaan stok, anggaran, dll.<br/><br/>

    <b style='color:{t["text"]};'>Recursive Forecasting</b><br/>
    Model melakukan <b>recursive forecasting</b>: prediksi bulan pertama menjadi input
    untuk bulan kedua, dan seterusnya. Semakin jauh horizon, semakin lebar confidence interval
    — mencerminkan ketidakpastian yang meningkat.<br/><br/>

    <b style='color:{t["text"]};'>Batasan Granularitas</b><br/>
    Dataset Superstore adalah agregat <b>bulanan</b> per kategori.
    Prediksi paling granular yang dapat dilakukan adalah <b>per bulan</b>.
    Input target berupa bulan dan tahun, sistem otomatis menghitung jumlah periode
    yang dibutuhkan dari akhir data historis (Desember 2017).<br/><br/>

    <b style='color:{t["text"]};'>Model per Kategori</b><br/>
    Furniture → <code>OMP</code> &nbsp;·&nbsp;
    Office Supplies → <code>ARIMA</code> &nbsp;·&nbsp;
    Technology → <code>Theta</code>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:1rem;'></div>", unsafe_allow_html=True)

# ── Form + Result ─────────────────────────────────────────────────────────
col_form, col_result = st.columns([1, 2.8])

DATA_END_YEAR, DATA_END_MONTH = 2017, 12  # akhir data historis

with col_form:
    st.markdown(section_label("Parameter Prediksi", t), unsafe_allow_html=True)

    category = st.selectbox("Kategori", VALID_CATEGORIES, label_visibility="collapsed")

    # Chip model
    st.markdown(f"""
    <div style='background:{"rgba(99,102,241,0.1)" if dm else "#EFF6FF"};
      border:1px solid {"rgba(99,102,241,0.2)" if dm else "#BFDBFE"};
      border-radius:8px;padding:8px 12px;font-size:0.8rem;
      color:{"#A5B4FC" if dm else "#1E40AF"};margin:0.5rem 0 1rem;'>
      Model: <strong>{MODEL_LABEL[category]}</strong>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:0.75rem;color:{t['text']};font-weight:500;margin-bottom:0.4rem;'>"
                "Target Bulan Prediksi</div>", unsafe_allow_html=True)

    # Month & year pickers
    m_col, y_col = st.columns(2)
    with m_col:
        target_month = st.selectbox(
            "Bulan", range(1, 13),
            format_func=lambda x: ["Jan","Feb","Mar","Apr","Mei","Jun",
                                    "Jul","Ags","Sep","Okt","Nov","Des"][x-1],
            label_visibility="collapsed"
        )
    with y_col:
        target_year = st.selectbox(
            "Tahun", list(range(2018, 2026)),
            label_visibility="collapsed"
        )

    # Hitung n_periods
    n_periods = (target_year - DATA_END_YEAR) * 12 + (target_month - DATA_END_MONTH)

    if n_periods <= 0:
        st.markdown(f"""
        <div style='background:{"rgba(220,38,38,0.1)" if dm else "#FEF2F2"};
          border:1px solid {"rgba(220,38,38,0.25)" if dm else "#FECACA"};
          border-radius:8px;padding:8px 12px;font-size:0.8rem;
          color:{"#F87171" if dm else "#991B1B"};margin-top:0.5rem;'>
          Target harus setelah Des 2017
        </div>""", unsafe_allow_html=True)
        run_disabled = True
    else:
        bulan_label = ["Jan","Feb","Mar","Apr","Mei","Jun",
                       "Jul","Ags","Sep","Okt","Nov","Des"][target_month-1]
        st.markdown(f"""
        <div style='background:{"rgba(99,102,241,0.08)" if dm else "#F5F3FF"};
          border:1px solid {"rgba(99,102,241,0.2)" if dm else "#DDD6FE"};
          border-radius:8px;padding:8px 12px;font-size:0.8rem;
          color:{t["muted"]};margin-top:0.5rem;'>
          Forecast <b style='color:{ACCENT};'>{n_periods}</b> bulan
          → <b style='color:{t["text"]};'>{bulan_label} {target_year}</b>
        </div>""", unsafe_allow_html=True)
        run_disabled = False

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    run = st.button("Tampilkan Forecast", disabled=run_disabled)

with col_result:
    if run and n_periods > 0:
        with st.spinner("Memuat forecast…"):
            try:
                data       = fetch_forecast(category)
                df_fore_all= pd.DataFrame(data["forecast"])
                model_used = data["model_used"]
                color      = CAT_COLORS.get(category, "#1D4ED8")
                df_fore    = df_fore_all.head(n_periods)

                try:
                    hist    = fetch_sales_monthly(category=category)
                    df_hist = pd.DataFrame(hist["data"])
                    df_hist["ym"] = df_hist["year"].astype(str)+"-"+df_hist["month"].astype(str).str.zfill(2)
                    df_hist = df_hist.sort_values("ym")
                    has_hist = True
                except Exception:
                    has_hist = False

                fig = go.Figure()

                # CI band
                fig.add_trace(go.Scatter(
                    x=list(df_fore["period"])+list(df_fore["period"])[::-1],
                    y=list(df_fore["upper_bound"])+list(df_fore["lower_bound"])[::-1],
                    fill="toself", fillcolor="rgba(99,102,241,0.1)",
                    line=dict(color="rgba(0,0,0,0)"),
                    name="Confidence Interval",
                ))
                for col_name in ["upper_bound","lower_bound"]:
                    fig.add_trace(go.Scatter(
                        x=df_fore["period"], y=df_fore[col_name],
                        line=dict(color="#6366F1", width=1, dash="dot"),
                        mode="lines", showlegend=False,
                    ))

                if has_hist:
                    fig.add_trace(go.Scatter(
                        x=df_hist["ym"], y=df_hist["total_sales"],
                        name="Historis", line=dict(color=color, width=2.5),
                        mode="lines+markers",
                        marker=dict(size=5, symbol="circle",
                                    line=dict(width=1.5, color=color)),
                    ))

                fig.add_trace(go.Scatter(
                    x=df_fore["period"], y=df_fore["forecast_sales"],
                    name=f"Forecast ({model_used})",
                    line=dict(color="#6366F1", width=2.5, dash="dash"),
                    mode="lines+markers",
                    marker=dict(size=8, symbol="circle-open",
                                line=dict(width=2, color="#6366F1")),
                ))

                bulan_label = ["Jan","Feb","Mar","Apr","Mei","Jun",
                               "Jul","Ags","Sep","Okt","Nov","Des"][target_month-1]
                fig.update_layout(
                    title=dict(
                        text=f"Forecast {category} → {bulan_label} {target_year} ({n_periods} periode)",
                        font=dict(size=14,family="Syne",color=t["text"]), x=0),
                    height=380, hovermode="x unified",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                font=dict(size=11,color=t["text"])),
                    xaxis=dict(showgrid=False, tickfont=dict(size=11,color=t["tick"])),
                    yaxis=dict(showgrid=True, gridcolor=t["grid"], tickformat=",.0f",
                               tickfont=dict(size=11,color=t["tick"])),
                    plot_bgcolor=t["plot_bg"], paper_bgcolor=t["plot_paper"],
                    margin=dict(l=10,r=10,t=55,b=10),
                    font=dict(family="DM Sans", color=t["text"]),
                )
                st.plotly_chart(fig, use_container_width=True)

                # Tabel detail
                st.markdown(section_label(f"Detail Forecast — {n_periods} Periode", t),
                            unsafe_allow_html=True)
                df_show = df_fore.copy()
                df_show.columns = ["Periode","Forecast Sales","Lower Bound","Upper Bound"]
                for c in ["Forecast Sales","Lower Bound","Upper Bound"]:
                    df_show[c] = df_show[c].apply(lambda x: f"Rp {x:,.2f}")
                st.dataframe(df_show, use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.markdown(f"""
        <div style='text-align:center;padding:70px 20px;background:{t["bg_card"]};
          border-radius:12px;border:1px dashed {t["border"]};'>
          <div style='font-size:2.5rem;margin-bottom:0.75rem;'>🔮</div>
          <div style='font-size:0.9rem;font-weight:600;color:{t["text"]};margin-bottom:0.4rem;'>
            Pilih Target & Klik Forecast</div>
          <div style='font-size:0.82rem;color:{t["muted"]};'>
            Pilih kategori dan target bulan prediksi, lalu klik <b>Tampilkan Forecast</b>
          </div>
        </div>""", unsafe_allow_html=True)
