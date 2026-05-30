"""
pages/01_Overview.py  —  KPI + tren bulanan + sales per kategori
Endpoint yang dipakai:
  GET /dashboard/summary
  GET /dashboard/sales-monthly
  GET /dashboard/sales-by-category
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import fetch_summary, fetch_sales_monthly, fetch_sales_by_category

st.set_page_config(page_title="Overview · Superstore", page_icon="📊", layout="wide")

st.markdown("## 📊 Overview")
st.markdown("Ringkasan performa penjualan Superstore 2014–2017")
st.divider()

# ── Error handler ──
def api_error(e):
    st.error(f"⚠️ Gagal memuat data: `{e}`")
    st.info("Pastikan FastAPI sudah jalan:\n```\nuvicorn api.main:app --reload\n```")
    st.stop()

# ════════════════════════════════
#   KPI CARDS dari /dashboard/summary
# ════════════════════════════════
try:
    summary = fetch_summary()
except Exception as e:
    api_error(e)

def fmt_rp(n):
    if abs(n) >= 1_000_000:
        return f"Rp {n/1_000_000:.2f}M"
    if abs(n) >= 1_000:
        return f"Rp {n/1_000:.1f}K"
    return f"Rp {n:,.0f}"

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Total Sales",     fmt_rp(summary["total_sales"]))
c2.metric("📈 Total Profit",    fmt_rp(summary["total_profit"]))
c3.metric("📦 Total Orders",    f'{summary["total_orders"]:,}')
c4.metric("👥 Total Customers", f'{summary["total_customers"]:,}')

st.divider()

# ════════════════════════════════
#   TREN BULANAN dari /dashboard/sales-monthly
# ════════════════════════════════
st.markdown("### Tren Bulanan per Kategori")

col_filter1, col_filter2 = st.columns([1, 4])
with col_filter1:
    metric_opt = st.selectbox("Metrik", ["Sales", "Profit"], key="ov_metric")
    year_opt   = st.selectbox("Tahun", ["Semua", 2014, 2015, 2016, 2017], key="ov_year")

try:
    year_param = None if year_opt == "Semua" else int(year_opt)
    monthly    = fetch_sales_monthly(year=year_param)
    df         = pd.DataFrame(monthly["data"])
except Exception as e:
    api_error(e)

if df.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
else:
    # Buat kolom YearMonth untuk sumbu X
    df["ym"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)
    metric_col = "total_sales" if metric_opt == "Sales" else "total_profit"

    COLORS = {"Furniture": "#185FA5", "Office Supplies": "#0F6E56", "Technology": "#854F0B"}
    fig = go.Figure()

    for cat, color in COLORS.items():
        df_cat = df[df["category"] == cat].sort_values("ym")
        fig.add_trace(go.Scatter(
            x=df_cat["ym"], y=df_cat[metric_col],
            name=cat, line=dict(color=color, width=2),
            mode="lines+markers", marker=dict(size=4),
        ))

    if metric_opt == "Profit":
        fig.add_hline(y=0, line_dash="dash", line_color="#A32D2D",
                      annotation_text="Break-even", annotation_position="right")

    fig.update_layout(
        height=380, hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis=dict(showgrid=True, gridcolor="#F1F3F5"),
        yaxis=dict(showgrid=True, gridcolor="#F1F3F5", tickformat=",.0f"),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ════════════════════════════════
#   SALES BY CATEGORY dari /dashboard/sales-by-category
# ════════════════════════════════
st.markdown("### Sales & Profit per Kategori")

col_left, col_right = st.columns(2)

try:
    by_cat   = fetch_sales_by_category()
    df_cat   = pd.DataFrame(by_cat["data"])
except Exception as e:
    api_error(e)

with col_left:
    fig_pie = px.pie(
        df_cat, values="total_sales", names="category",
        color="category",
        color_discrete_map={"Furniture":"#185FA5","Office Supplies":"#0F6E56","Technology":"#854F0B"},
        title="Distribusi Sales"
    )
    fig_pie.update_layout(height=300, margin=dict(l=0,r=0,t=40,b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="Sales",
        x=df_cat["category"], y=df_cat["total_sales"],
        marker_color=["#185FA5","#0F6E56","#854F0B"],
    ))
    fig_bar.add_trace(go.Bar(
        name="Profit",
        x=df_cat["category"], y=df_cat["total_profit"],
        marker_color=["#5B9AD5","#40B090","#D4862A"],
    ))
    fig_bar.update_layout(
        barmode="group", height=300, title="Perbandingan Sales vs Profit",
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=0,r=0,t=40,b=0),
        yaxis=dict(tickformat=",.0f"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)
