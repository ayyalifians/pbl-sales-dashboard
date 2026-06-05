"""
pages/04_Top_Produk.py
"""
import streamlit as st, pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Top Produk · PredixViz", layout="wide")
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

from _theme_helper import (
    get_theme, inject_global_css, render_toggle,
    section_label, status_badge,
    ACCENT, ACCENT2, CAT_COLORS, VALID_CATEGORIES
)
from api_client import check_health, fetch_top_products

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

st.markdown("# Top Produk")
st.markdown(f"<p style='color:{t['muted']};font-size:0.875rem;margin-top:-0.5rem;margin-bottom:1rem;'>"
            "Produk dengan total penjualan tertinggi</p>", unsafe_allow_html=True)

cf1,cf2,_ = st.columns([1,1,3])
with cf1: limit      = st.selectbox("Tampilkan",[5,10,20], index=1, label_visibility="collapsed")
with cf2: cat_filter = st.selectbox("Kategori",["Semua"]+VALID_CATEGORIES, label_visibility="collapsed")

try:
    result = fetch_top_products(limit=limit,
                                category=None if cat_filter=="Semua" else cat_filter)
    df     = pd.DataFrame(result["data"])
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

if df.empty:
    st.info("Tidak ada data untuk filter yang dipilih.")
    st.stop()

st.markdown(section_label("Berdasarkan Total Sales", t), unsafe_allow_html=True)

# Legend universal
legend_html = " ".join([
    f'<span style="display:inline-flex;align-items:center;gap:5px;margin-right:12px;'
    f'font-size:0.78rem;color:{t["text"]};">'
    f'<span style="width:12px;height:12px;border-radius:3px;background:{clr};'
    f'display:inline-block;flex-shrink:0;"></span>{cat}</span>'
    for cat, clr in CAT_COLORS.items()
])
st.markdown(f"<div style='margin-bottom:0.65rem;'>{legend_html}</div>", unsafe_allow_html=True)

# Horizontal bar — nilai tertinggi di atas (sort ascending untuk horizontal)
df_sorted = df.sort_values("total_sales", ascending=True)
fig = go.Figure(go.Bar(
    x=df_sorted["total_sales"],
    y=df_sorted["product_name"],
    orientation="h",
    marker_color=[CAT_COLORS.get(c,"#6B7280") for c in df_sorted["category"]],
    text=[f"Rp {v:,.0f}" for v in df_sorted["total_sales"]],
    textposition="outside",
    textfont=dict(size=10, family="DM Sans", color=t["text"]),
))
fig.update_layout(
    height=max(300, limit*36),
    plot_bgcolor=t["plot_bg"], paper_bgcolor=t["plot_paper"],
    xaxis=dict(tickformat=",.0f", showgrid=True, gridcolor=t["grid"],
               tickfont=dict(color=t["tick"])),
    yaxis=dict(showgrid=False, tickfont=dict(size=11, color=t["text"]), automargin=True),
    margin=dict(l=10,r=110,t=10,b=10),
    font=dict(family="DM Sans", color=t["text"]),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown(section_label(f"Tabel Detail — {result['total_records']} Produk", t),
            unsafe_allow_html=True)

df_show = df[["product_name","category","sub_category","total_sales","total_profit","total_orders"]].copy()
df_show["total_sales"]  = df_show["total_sales"].apply(lambda x: f"Rp {x:,.2f}")
df_show["total_profit"] = df_show["total_profit"].apply(lambda x: f"Rp {x:,.2f}")
df_show.columns = ["Nama Produk","Kategori","Sub-Kategori","Total Sales","Total Profit","Orders"]
st.dataframe(df_show, use_container_width=True, hide_index=True)
