"""
pages/01_Overview.py
KPI cards + tren bulanan + distribusi kategori + insight bisnis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.api_client import fetch_summary, fetch_sales_monthly, fetch_sales_by_category

st.set_page_config(page_title="Overview · Superstore", layout="wide")

# ── CSS tambahan halaman ini ──
st.markdown("""
<style>
.section-label {
    font-size:0.7rem;font-weight:600;color:#6B7280;
    text-transform:uppercase;letter-spacing:0.05em;
    margin-bottom:0.75rem;
}
.insight-card {
    border:1px solid #E5E7EB;border-radius:8px;
    padding:1.25rem;background:white;height:100%;
}
.insight-title {
    font-size:0.8rem;font-weight:600;color:#374151;margin-bottom:0.5rem;
}
.insight-body {
    font-size:0.8rem;color:#6B7280;line-height:1.6;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# Overview")
st.markdown("<p style='color:#6B7280;font-size:0.875rem;margin-top:-0.5rem;'>Ringkasan performa penjualan Superstore 2014–2017</p>", unsafe_allow_html=True)
st.divider()

COLORS = {"Furniture": "#1D4ED8", "Office Supplies": "#059669", "Technology": "#D97706"}

def api_err(e):
    st.error(f"Gagal memuat data dari API: {e}")
    st.info("Pastikan FastAPI sudah jalan: `uvicorn api.main:app --reload`")
    st.stop()

def fmt_rp(n):
    sign = "-" if n < 0 else ""
    n = abs(n)
    if n >= 1_000_000_000: return f"{sign}Rp {n/1_000_000_000:.2f}B"
    if n >= 1_000_000:     return f"{sign}Rp {n/1_000_000:.2f}M"
    if n >= 1_000:         return f"{sign}Rp {n/1_000:.1f}K"
    return f"{sign}Rp {n:,.0f}"

# ════════════════════════════════
#   KPI CARDS
# ════════════════════════════════
try:
    summary = fetch_summary()
except Exception as e:
    api_err(e)

st.markdown("<div class='section-label'>Ringkasan Keseluruhan</div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales",     fmt_rp(summary["total_sales"]))
c2.metric("Total Profit",    fmt_rp(summary["total_profit"]))
c3.metric("Total Orders",    f'{summary["total_orders"]:,}')
c4.metric("Total Customers", f'{summary["total_customers"]:,}')

st.divider()

# ════════════════════════════════
#   TREN BULANAN
# ════════════════════════════════
st.markdown("<div class='section-label'>Tren Bulanan</div>", unsafe_allow_html=True)

col_f1, col_f2, _ = st.columns([1, 1, 3])
with col_f1:
    metric_opt = st.selectbox("Metrik", ["Sales", "Profit", "Jumlah Order"], label_visibility="collapsed")
with col_f2:
    year_opt = st.selectbox("Tahun", ["Semua", 2014, 2015, 2016, 2017], label_visibility="collapsed")

try:
    year_param = None if year_opt == "Semua" else int(year_opt)
    monthly    = fetch_sales_monthly(year=year_param)
    df         = pd.DataFrame(monthly["data"])
except Exception as e:
    api_err(e)

metric_col = {"Sales": "total_sales", "Profit": "total_profit", "Jumlah Order": "num_orders"}[metric_opt]
unit       = "" if metric_opt == "Jumlah Order" else "Rp"

fig = go.Figure()
if not df.empty:
    df["ym"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)
    for cat, color in COLORS.items():
        d = df[df["category"] == cat].sort_values("ym")
        fig.add_trace(go.Scatter(
            x=d["ym"], y=d[metric_col], name=cat,
            line=dict(color=color, width=2),
            mode="lines+markers", marker=dict(size=3),
        ))
    if metric_opt == "Profit":
        fig.add_hline(y=0, line_dash="dash", line_color="#9CA3AF", line_width=1)

fig.update_layout(
    height=320, hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=12)),
    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    yaxis=dict(showgrid=True, gridcolor="#F3F4F6", tickformat=",.0f",
               tickfont=dict(size=11), title=unit),
    plot_bgcolor="white", paper_bgcolor="white",
    margin=dict(l=0, r=0, t=30, b=0),
    font=dict(family="Inter"),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ════════════════════════════════
#   DISTRIBUSI PER KATEGORI
# ════════════════════════════════
st.markdown("<div class='section-label'>Distribusi per Kategori</div>", unsafe_allow_html=True)

try:
    by_cat = fetch_sales_by_category()
    df_cat = pd.DataFrame(by_cat["data"])
except Exception as e:
    api_err(e)

cl, cr = st.columns(2)

with cl:
    fig_pie = go.Figure(go.Pie(
        labels=df_cat["category"],
        values=df_cat["total_sales"],
        marker_colors=[COLORS.get(c, "#6B7280") for c in df_cat["category"]],
        hole=0.5,
        textinfo="label+percent",
        textfont=dict(size=12, family="Inter"),
    ))
    fig_pie.update_layout(
        title=dict(text="Distribusi Sales", font=dict(size=13, family="Inter"), x=0),
        height=280, showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="white",
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with cr:
    fig_bar = go.Figure()
    for col_key, col_name, opacity in [("total_sales","Sales",1.0),("total_profit","Profit",0.65)]:
        fig_bar.add_trace(go.Bar(
            name=col_name,
            x=df_cat["category"],
            y=df_cat[col_key],
            marker_color=[COLORS.get(c,"#6B7280") for c in df_cat["category"]],
            opacity=opacity,
            text=[fmt_rp(v) for v in df_cat[col_key]],
            textposition="outside",
            textfont=dict(size=10),
        ))
    fig_bar.update_layout(
        barmode="group",
        title=dict(text="Sales vs Profit", font=dict(size=13, family="Inter"), x=0),
        height=280,
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(tickformat=",.0f", showgrid=True, gridcolor="#F3F4F6"),
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=0, r=0, t=40, b=0),
        font=dict(family="Inter"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ════════════════════════════════
#   INSIGHT BISNIS (bagian bawah Overview)
# ════════════════════════════════
st.markdown("<div class='section-label'>Insight Bisnis</div>", unsafe_allow_html=True)

i1, i2 = st.columns(2)

with i1:
    st.markdown("""
    <div class='insight-card' style='border-left:3px solid #DC2626;'>
        <div class='insight-title' style='color:#DC2626;'>Sub-kategori dengan Kerugian Terbesar</div>
        <div class='insight-body'>
            <b>Tables</b> mencatat 83% bulan merugi dengan rata-rata margin –14.8%.
            <b>Bookcases</b> (56.5% bulan rugi, margin –12.7%) dan <b>Binders</b>
            (margin –20.3%) menyusul sebagai sub-kategori paling tidak menguntungkan.
            Diskon berlebih terbukti menjadi penyebab utama.
        </div>
    </div>""", unsafe_allow_html=True)

with i2:
    st.markdown("""
    <div class='insight-card' style='border-left:3px solid #D97706;'>
        <div class='insight-title' style='color:#D97706;'>Ambang Batas Diskon Kritis</div>
        <div class='insight-body'>
            Diskon ≥ 30% pada <b>Tables</b> menyebabkan 93–100% transaksi merugi.
            <b>Binders</b> dengan diskon 70–80% menghasilkan kerugian di 100% transaksi.
            Rata-rata diskon pada transaksi merugi (0.37) vs menguntungkan (0.08).
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:0.75rem;'></div>", unsafe_allow_html=True)
i3, i4 = st.columns(2)

with i3:
    st.markdown("""
    <div class='insight-card' style='border-left:3px solid #059669;'>
        <div class='insight-title' style='color:#059669;'>Sub-kategori Paling Stabil</div>
        <div class='insight-body'>
            Art, Labels, Envelopes, Accessories, Paper, Copiers, dan Fasteners
            tidak pernah mencatat bulan merugi sepanjang 2014–2017.
            Sub-kategori ini dapat diandalkan sebagai sumber pendapatan stabil.
        </div>
    </div>""", unsafe_allow_html=True)

with i4:
    st.markdown("""
    <div class='insight-card' style='border-left:3px solid #1D4ED8;'>
        <div class='insight-title' style='color:#1D4ED8;'>Rekomendasi Strategis</div>
        <div class='insight-body'>
            Batasi diskon Tables dan Bookcases maksimal 20%. Tinjau kembali
            strategi diskon Binders. Prioritaskan promosi pada <b>Technology</b>
            yang memiliki rata-rata margin +15.6% dan <b>Copiers</b> dengan
            margin tertinggi di +37.8%.
        </div>
    </div>""", unsafe_allow_html=True)
