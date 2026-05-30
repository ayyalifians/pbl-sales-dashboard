"""
pages/04_Top_Produk.py
Produk dengan penjualan tertinggi.
Endpoint: GET /dashboard/top-products
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import fetch_top_products, VALID_CATEGORIES

st.set_page_config(page_title="Top Produk · Superstore", page_icon="🏆", layout="wide")

st.markdown("## 🏆 Top Produk")
st.markdown("Produk dengan penjualan dan profit tertinggi")
st.divider()

col_f1, col_f2, col_f3 = st.columns([1, 1, 3])
with col_f1:
    limit = st.selectbox("Tampilkan", [5, 10, 20], index=1)
with col_f2:
    cat_filter = st.selectbox("Kategori", ["Semua"] + VALID_CATEGORIES)

try:
    cat_param = None if cat_filter == "Semua" else cat_filter
    result    = fetch_top_products(limit=limit, category=cat_param)
    df        = pd.DataFrame(result["data"])
except Exception as e:
    st.error(f"⚠️ Gagal memuat data: `{e}`")
    st.stop()

if df.empty:
    st.warning("Tidak ada data.")
    st.stop()

# ── Bar chart horizontal ──
fig = px.bar(
    df.sort_values("total_sales"),
    x="total_sales", y="product_name",
    orientation="h",
    color="category",
    color_discrete_map={"Furniture":"#185FA5","Office Supplies":"#0F6E56","Technology":"#854F0B"},
    labels={"total_sales":"Total Sales (Rp)", "product_name":"Produk"},
    title=f"Top {limit} Produk berdasarkan Sales",
)
fig.update_layout(
    height=max(300, limit * 35),
    plot_bgcolor="white", paper_bgcolor="white",
    xaxis=dict(tickformat=",.0f"),
    margin=dict(l=0, r=0, t=40, b=0),
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
)
st.plotly_chart(fig, use_container_width=True)

# ── Tabel ──
st.divider()
st.markdown(f"### Tabel Detail — {result['total_records']} produk")

df_display = df[["product_name", "category", "sub_category", "total_sales", "total_profit", "total_orders"]].copy()
df_display["total_sales"]   = df_display["total_sales"].apply(lambda x: f"Rp {x:,.2f}")
df_display["total_profit"]  = df_display["total_profit"].apply(lambda x: f"Rp {x:,.2f}")
df_display.columns = ["Nama Produk", "Kategori", "Sub-Kategori", "Total Sales", "Total Profit", "Total Orders"]

st.dataframe(df_display, use_container_width=True, hide_index=True)
