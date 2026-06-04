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

st.set_page_config(page_title="Overview · PredixViz", layout="wide")

dm = st.session_state.get("dark_mode", False)
bg_main = "#0F1117" if dm else "#F8FAFC"
bg_card = "#1A1D27" if dm else "#FFFFFF"
border_c = "#2D3148" if dm else "#E2E8F0"
text_main = "#F1F5F9" if dm else "#0F172A"
text_mute = "#94A3B8" if dm else "#64748B"
plot_bg = "#1A1D27" if dm else "#FFFFFF"
plot_paper = "#1A1D27" if dm else "#FFFFFF"
grid_c = "#2D3148" if dm else "#F1F5F9"
tick_c = "#94A3B8" if dm else "#6B7280"
accent = "#6366F1"

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
.section-label{{font-size:0.68rem;font-weight:700;color:{text_mute};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.75rem;font-family:'Syne',sans-serif;}}
.insight-card{{border:1px solid {border_c};border-radius:12px;padding:1.25rem;background:{bg_card};height:100%;}}
.insight-title{{font-size:0.8rem;font-weight:600;color:{text_main};margin-bottom:0.5rem;}}
.insight-body{{font-size:0.8rem;color:{text_mute};line-height:1.6;}}
[data-testid="stSelectbox"]>div>div{{background:{bg_card}!important;border-color:{border_c}!important;color:{text_main}!important;}}
p,li,div,span,label{{color:{text_main}!important;}}
</style>
""", unsafe_allow_html=True)

st.markdown("# Overview")
st.markdown(f"<p style='color:{text_mute};font-size:0.875rem;margin-top:-0.5rem;'>Ringkasan performa penjualan Superstore 2014–2017</p>", unsafe_allow_html=True)
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

# ════ KPI CARDS ════
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

# ════ TREN BULANAN ════
st.markdown("<div class='section-label'>Tren Bulanan</div>", unsafe_allow_html=True)

col_f1, col_f2, col_f3, _ = st.columns([1, 1, 1, 2])
with col_f1:
    metric_opt = st.selectbox("Metrik", ["Sales", "Profit", "Jumlah Order"], label_visibility="collapsed")
with col_f2:
    year_opt = st.selectbox("Tahun", ["Semua", 2014, 2015, 2016, 2017], label_visibility="collapsed")
with col_f3:
    cat_opt = st.selectbox("Kategori", ["Semua"] + list(COLORS.keys()), label_visibility="collapsed", key="tren_cat")

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
    cats_to_show = list(COLORS.keys()) if cat_opt == "Semua" else [cat_opt]
    for cat in cats_to_show:
        color = COLORS[cat]
        d = df[df["category"] == cat].sort_values("ym")
        fig.add_trace(go.Scatter(
            x=d["ym"], y=d[metric_col], name=cat,
            line=dict(color=color, width=2.5),
            mode="lines+markers",
            marker=dict(size=6, symbol="circle", line=dict(width=1.5, color=color)),
        ))
    if metric_opt == "Profit":
        fig.add_hline(y=0, line_dash="dash", line_color="#9CA3AF", line_width=1)

fig.update_layout(
    height=320, hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=12, color=text_main)),
    xaxis=dict(showgrid=False, tickfont=dict(size=11, color=tick_c), automargin=True),
    yaxis=dict(showgrid=True, gridcolor=grid_c, tickformat=",.0f",
               tickfont=dict(size=11, color=tick_c), title=unit, titlefont=dict(color=tick_c)),
    plot_bgcolor=plot_bg, paper_bgcolor=plot_paper,
    margin=dict(l=10, r=10, t=40, b=10),
    font=dict(family="DM Sans"),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ════ DISTRIBUSI PER KATEGORI ════
st.markdown("<div class='section-label'>Distribusi per Kategori</div>", unsafe_allow_html=True)

try:
    by_cat = fetch_sales_by_category()
    df_cat = pd.DataFrame(by_cat["data"])
except Exception as e:
    api_err(e)

cl, cr = st.columns(2)

with cl:
    # Donut chart dengan textfont per slice agar kontras
    colors_list = [COLORS.get(c, "#6B7280") for c in df_cat["category"]]
    # Tentukan warna teks per slice berdasarkan warna background
    def get_text_color(bg_hex):
        r = int(bg_hex[1:3],16); g = int(bg_hex[3:5],16); b = int(bg_hex[5:7],16)
        lum = (0.299*r + 0.587*g + 0.114*b)/255
        return "#FFFFFF" if lum < 0.55 else "#1F2937"

    fig_pie = go.Figure(go.Pie(
        labels=df_cat["category"],
        values=df_cat["total_sales"],
        marker=dict(
            colors=colors_list,
            line=dict(color=plot_bg, width=2)
        ),
        hole=0.52,
        textinfo="label+percent",
        textfont=dict(size=12, family="DM Sans", color="#FFFFFF"),
        insidetextfont=dict(color="#FFFFFF"),
        outsidetextfont=dict(color=text_main),
    ))
    fig_pie.update_traces(textposition="outside")
    fig_pie.update_layout(
        title=dict(text="Distribusi Sales", font=dict(size=13, family="Syne", color=text_main), x=0),
        height=300, showlegend=True,
        legend=dict(font=dict(color=text_main, size=11), orientation="h", y=-0.12),
        margin=dict(l=0, r=0, t=40, b=40),
        paper_bgcolor=plot_paper,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with cr:
    # Scatter plot Sales vs Profit — lebih informatif dari grouped bar
    fig_scatter = go.Figure()
    for _, row in df_cat.iterrows():
        cat = row["category"]
        color = COLORS.get(cat, "#6B7280")
        fig_scatter.add_trace(go.Scatter(
            x=[row["total_sales"]],
            y=[row["total_profit"]],
            mode="markers+text",
            name=cat,
            text=[cat],
            textposition="top center",
            textfont=dict(size=11, color=text_main),
            marker=dict(size=22, color=color, opacity=0.85,
                        line=dict(width=2, color=plot_bg)),
        ))
    fig_scatter.update_layout(
        title=dict(text="Sales vs Profit per Kategori", font=dict(size=13, family="Syne", color=text_main), x=0),
        height=300,
        plot_bgcolor=plot_bg, paper_bgcolor=plot_paper,
        xaxis=dict(title="Total Sales", tickformat=",.0f", showgrid=True, gridcolor=grid_c,
                   tickfont=dict(size=10, color=tick_c), titlefont=dict(color=tick_c)),
        yaxis=dict(title="Total Profit", tickformat=",.0f", showgrid=True, gridcolor=grid_c,
                   tickfont=dict(size=10, color=tick_c), titlefont=dict(color=tick_c)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=11, color=text_main)),
        margin=dict(l=10, r=10, t=45, b=10),
        font=dict(family="DM Sans"),
        showlegend=True,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ════ INSIGHT BISNIS ════
st.markdown("<div class='section-label'>Insight Bisnis</div>", unsafe_allow_html=True)

i1, i2 = st.columns(2)
with i1:
    st.markdown(f"""
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
    st.markdown(f"""
    <div class='insight-card' style='border-left:3px solid #D97706;'>
        <div class='insight-title' style='color:#D97706;'>Ambang Batas Diskon Kritis</div>
        <div class='insight-body'>
            Diskon ≥ 30% pada <b>Tables</b> menyebabkan 93–100% transaksi merugi.
            <b>Binders</b> dengan diskon 70–80% menghasilkan kerugian di 100% transaksi.
            Rata-rata diskon transaksi merugi (0.37) vs menguntungkan (0.08).
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:0.75rem;'></div>", unsafe_allow_html=True)
i3, i4 = st.columns(2)
with i3:
    st.markdown(f"""
    <div class='insight-card' style='border-left:3px solid #059669;'>
        <div class='insight-title' style='color:#059669;'>Sub-kategori Paling Stabil</div>
        <div class='insight-body'>
            Art, Labels, Envelopes, Accessories, Paper, Copiers, dan Fasteners
            tidak pernah mencatat bulan merugi sepanjang 2014–2017.
            Sub-kategori ini dapat diandalkan sebagai sumber pendapatan stabil.
        </div>
    </div>""", unsafe_allow_html=True)
with i4:
    st.markdown(f"""
    <div class='insight-card' style='border-left:3px solid #6366F1;'>
        <div class='insight-title' style='color:#6366F1;'>Rekomendasi Strategis</div>
        <div class='insight-body'>
            Batasi diskon Tables dan Bookcases maksimal 20%. Tinjau kembali
            strategi diskon Binders. Prioritaskan promosi pada <b>Technology</b>
            yang memiliki rata-rata margin +15.6% dan <b>Copiers</b> dengan
            margin tertinggi di +37.8%.
        </div>
    </div>""", unsafe_allow_html=True)
