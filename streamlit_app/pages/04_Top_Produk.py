"""
pages/04_Top_Produk.py
Produk dengan penjualan tertinggi
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.api_client import fetch_top_products, VALID_CATEGORIES

st.set_page_config(page_title="Top Produk · PredixViz", layout="wide")

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
.stDataFrame{{background:{bg_card}!important;}}
p,li,div,span,label{{color:{text_main}!important;}}
</style>
""", unsafe_allow_html=True)

st.markdown("# Top Produk")
st.markdown(f"<p style='color:{text_mute};font-size:0.875rem;margin-top:-0.5rem;'>Produk dengan penjualan dan profit tertinggi</p>", unsafe_allow_html=True)
st.divider()

COLORS = {"Furniture": "#1D4ED8", "Office Supplies": "#059669", "Technology": "#D97706"}

col_f1, col_f2, _ = st.columns([1, 1, 3])
with col_f1:
    limit = st.selectbox("Tampilkan", [5, 10, 20], index=1, label_visibility="collapsed")
with col_f2:
    cat_filter = st.selectbox("Kategori", ["Semua"] + VALID_CATEGORIES, label_visibility="collapsed")

try:
    cat_param = None if cat_filter == "Semua" else cat_filter
    result    = fetch_top_products(limit=limit, category=cat_param)
    df        = pd.DataFrame(result["data"])
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

if df.empty:
    st.info("Tidak ada data untuk filter yang dipilih.")
    st.stop()

st.markdown(f"<div style='font-size:0.68rem;font-weight:700;color:{text_mute};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.75rem;'>Berdasarkan Total Sales</div>", unsafe_allow_html=True)

# Legend warna kategori — universal, tampil selalu
legend_html = "".join([
    f"<span style='display:inline-flex;align-items:center;gap:5px;margin-right:14px;font-size:0.78rem;color:{text_main};'>"
    f"<span style='width:12px;height:12px;border-radius:3px;background:{clr};display:inline-block;flex-shrink:0;'></span>{cat}</span>"
    for cat, clr in COLORS.items()
])
st.markdown(f"<div style='margin-bottom:0.6rem;'>{legend_html}</div>", unsafe_allow_html=True)

# Bar chart horizontal — sorted descending (nilai tertinggi di atas)
df_sorted = df.sort_values("total_sales", ascending=True)  # ascending=True karena horizontal bar: bawah = kiri

fig = go.Figure(go.Bar(
    x=df_sorted["total_sales"],
    y=df_sorted["product_name"],
    orientation="h",
    marker_color=[COLORS.get(c, "#6B7280") for c in df_sorted["category"]],
    text=[f"Rp {v:,.0f}" for v in df_sorted["total_sales"]],
    textposition="outside",
    textfont=dict(size=10, family="DM Sans", color=text_main),
))
fig.update_layout(
    height=max(300, limit * 36),
    plot_bgcolor=plot_bg, paper_bgcolor=plot_paper,
    xaxis=dict(tickformat=",.0f", showgrid=True, gridcolor=grid_c,
               tickfont=dict(color=tick_c)),
    yaxis=dict(showgrid=False, tickfont=dict(size=11, color=text_main),
               automargin=True),
    margin=dict(l=10, r=100, t=10, b=10),
    font=dict(family="DM Sans"),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown(f"<div style='font-size:0.68rem;font-weight:700;color:{text_mute};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.75rem;'>Tabel Detail — {result['total_records']} produk</div>", unsafe_allow_html=True)

df_show = df[["product_name","category","sub_category","total_sales","total_profit","total_orders"]].copy()
df_show["total_sales"]  = df_show["total_sales"].apply(lambda x: f"Rp {x:,.2f}")
df_show["total_profit"] = df_show["total_profit"].apply(lambda x: f"Rp {x:,.2f}")
df_show.columns = ["Nama Produk", "Kategori", "Sub-Kategori", "Total Sales", "Total Profit", "Orders"]
st.dataframe(df_show, use_container_width=True, hide_index=True)
