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

st.set_page_config(page_title="Top Produk · Superstore", layout="wide")

st.markdown("# Top Produk")
st.markdown("<p style='color:#6B7280;font-size:0.875rem;margin-top:-0.5rem;'>Produk dengan penjualan dan profit tertinggi</p>", unsafe_allow_html=True)
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

st.markdown("<div style='font-size:0.7rem;font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.75rem;'>Berdasarkan Total Sales</div>", unsafe_allow_html=True)

# Bar chart horizontal
fig = go.Figure(go.Bar(
    x=df["total_sales"],
    y=df["product_name"],
    orientation="h",
    marker_color=[COLORS.get(c, "#6B7280") for c in df["category"]],
    text=[f"Rp {v:,.0f}" for v in df["total_sales"]],
    textposition="outside",
    textfont=dict(size=10, family="Inter"),
))
fig.update_layout(
    height=max(280, limit * 32),
    plot_bgcolor="white", paper_bgcolor="white",
    xaxis=dict(tickformat=",.0f", showgrid=True, gridcolor="#F3F4F6"),
    yaxis=dict(showgrid=False, tickfont=dict(size=11)),
    margin=dict(l=0, r=80, t=10, b=0),
    font=dict(family="Inter"),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown(f"<div style='font-size:0.7rem;font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.75rem;'>Tabel Detail — {result['total_records']} produk</div>", unsafe_allow_html=True)

df_show = df[["product_name","category","sub_category","total_sales","total_profit","total_orders"]].copy()
df_show["total_sales"]  = df_show["total_sales"].apply(lambda x: f"Rp {x:,.2f}")
df_show["total_profit"] = df_show["total_profit"].apply(lambda x: f"Rp {x:,.2f}")
df_show.columns = ["Nama Produk", "Kategori", "Sub-Kategori", "Total Sales", "Total Profit", "Orders"]
st.dataframe(df_show, use_container_width=True, hide_index=True)
