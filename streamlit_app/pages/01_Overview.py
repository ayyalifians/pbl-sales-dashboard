"""
pages/01_Overview.py
"""
import streamlit as st, pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Overview · PredixViz", layout="wide")
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

from _theme_helper import (
    get_theme, inject_global_css, render_toggle,
    section_label, status_badge, card_wrap,
    ACCENT, ACCENT2, CAT_COLORS, VALID_CATEGORIES
)
from utils.api_client import check_health, fetch_summary, fetch_sales_monthly, fetch_sales_by_category

inject_global_css()
render_toggle()
t = get_theme(); dm = t["dm"]

# ── Sidebar logo ──────────────────────────────────────────────────────────
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
          <div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;
            color:{t["text"]};'>PredixViz</div>
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

# ── Page header ───────────────────────────────────────────────────────────
st.markdown("# Overview")
st.markdown(f"<p style='color:{t['muted']};font-size:0.875rem;margin-top:-0.5rem;margin-bottom:1rem;'>"
            "Ringkasan performa penjualan Superstore 2014–2017</p>", unsafe_allow_html=True)

def api_err(e):
    st.error(f"Gagal memuat data dari API: {e}")
    st.info("Pastikan FastAPI sudah berjalan: `uvicorn api.main:app --reload`")
    st.stop()

def fmt_rp(n):
    sign = "-" if n < 0 else ""
    n = abs(n)
    if n >= 1_000_000_000: return f"{sign}Rp {n/1_000_000_000:.2f}B"
    if n >= 1_000_000:     return f"{sign}Rp {n/1_000_000:.2f}M"
    if n >= 1_000:         return f"{sign}Rp {n/1_000:.1f}K"
    return f"{sign}Rp {n:,.0f}"

# ── KPI ──────────────────────────────────────────────────────────────────
try:
    summary = fetch_summary()
except Exception as e:
    api_err(e)

st.markdown(section_label("Ringkasan Keseluruhan", t), unsafe_allow_html=True)
c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Sales",     fmt_rp(summary["total_sales"]))
c2.metric("Total Profit",    fmt_rp(summary["total_profit"]))
c3.metric("Total Orders",    f'{summary["total_orders"]:,}')
c4.metric("Total Customers", f'{summary["total_customers"]:,}')
st.divider()

# ── Tren Bulanan ─────────────────────────────────────────────────────────
st.markdown(section_label("Tren Bulanan", t), unsafe_allow_html=True)

cf1,cf2,cf3,_ = st.columns([1,1,1,2])
with cf1: metric_opt = st.selectbox("Metrik",["Sales","Profit","Jumlah Order"], label_visibility="collapsed")
with cf2: year_opt   = st.selectbox("Tahun",["Semua",2014,2015,2016,2017],     label_visibility="collapsed")
with cf3: cat_opt    = st.selectbox("Kategori",["Semua"]+VALID_CATEGORIES,     label_visibility="collapsed", key="tren_cat")

try:
    monthly = fetch_sales_monthly(year=None if year_opt=="Semua" else int(year_opt))
    df      = pd.DataFrame(monthly["data"])
except Exception as e:
    api_err(e)

metric_col = {"Sales":"total_sales","Profit":"total_profit","Jumlah Order":"num_orders"}[metric_opt]

fig = go.Figure()
if not df.empty:
    df["ym"] = df["year"].astype(str)+"-"+df["month"].astype(str).str.zfill(2)
    # Aggregate per bulan per kategori — hindari duplikat titik di linechart
    agg_cols = {k:"sum" for k in ["total_sales","total_profit","num_orders"] if k in df.columns}
    df = df.groupby(["category","ym"], as_index=False).agg(agg_cols)
    cats = VALID_CATEGORIES if cat_opt=="Semua" else [cat_opt]
    for cat in cats:
        d = df[df["category"]==cat].sort_values("ym")
        fig.add_trace(go.Scatter(
            x=d["ym"], y=d[metric_col], name=cat,
            line=dict(color=CAT_COLORS[cat], width=2.5),
            mode="lines+markers",
            marker=dict(size=7, symbol="circle",
                        line=dict(width=1.5, color=CAT_COLORS[cat])),
        ))
    if metric_opt=="Profit":
        fig.add_hline(y=0, line_dash="dash", line_color="#9CA3AF", line_width=1)

fig.update_layout(
    height=320, hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02,
                font=dict(size=12, color=t["text"])),
    xaxis=dict(showgrid=False, tickfont=dict(size=11, color=t["tick"])),
    yaxis=dict(showgrid=True, gridcolor=t["grid"], tickformat=",.0f",
               tickfont=dict(size=11, color=t["tick"])),
    plot_bgcolor=t["plot_bg"], paper_bgcolor=t["plot_paper"],
    margin=dict(l=10,r=10,t=40,b=10),
    font=dict(family="DM Sans", color=t["text"]),
)
st.plotly_chart(fig, use_container_width=True)
st.divider()

# ── Distribusi per Kategori ───────────────────────────────────────────────
st.markdown(section_label("Distribusi per Kategori", t), unsafe_allow_html=True)
try:
    df_cat = pd.DataFrame(fetch_sales_by_category()["data"])
except Exception as e:
    api_err(e)

cl, cr = st.columns(2)

with cl:
    colors_list = [CAT_COLORS.get(c,"#6B7280") for c in df_cat["category"]]
    fig_pie = go.Figure(go.Pie(
        labels=df_cat["category"], values=df_cat["total_sales"],
        marker=dict(colors=colors_list, line=dict(color=t["plot_bg"], width=3)),
        hole=0.52, textinfo="label+percent",
        textfont=dict(size=12, family="DM Sans"),
        insidetextfont=dict(color="#FFFFFF"),
        outsidetextfont=dict(color=t["text"]),
    ))
    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent",
        insidetextorientation="radial",
    )
    fig_pie.update_layout(
        title=dict(text="Distribusi Sales", font=dict(size=13,family="Syne",color=t["text"]),x=0),
        height=300, showlegend=True,
        legend=dict(font=dict(color=t["text"],size=11), orientation="h", y=-0.15,
                    xanchor="center", x=0.5),
        margin=dict(l=60,r=60,t=40,b=70),
        paper_bgcolor=t["plot_paper"],
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with cr:
    fig_sc = go.Figure()
    for _, row in df_cat.iterrows():
        cat   = row["category"]
        color = CAT_COLORS.get(cat,"#6B7280")
        fig_sc.add_trace(go.Scatter(
            x=[row["total_sales"]], y=[row["total_profit"]],
            mode="markers", name=cat,
            marker=dict(size=20, color=color, opacity=0.9,
                        line=dict(width=2, color=t["plot_bg"])),
            hovertemplate=f"<b>{cat}</b><br>Sales: %{{x:,.0f}}<br>Profit: %{{y:,.0f}}<extra></extra>",
        ))
    # Tambah anotasi nama kategori manual — tidak duplikat di legend
    annotations = []
    for _, row in df_cat.iterrows():
        annotations.append(dict(
            x=row["total_sales"], y=row["total_profit"],
            text=row["category"],
            showarrow=False,
            yshift=18,
            font=dict(size=11, color=t["text"], family="DM Sans"),
        ))
    fig_sc.update_layout(
        title=dict(text="Sales vs Profit per Kategori",
                   font=dict(size=13,family="Syne",color=t["text"]),x=0),
        height=300,
        plot_bgcolor=t["plot_bg"], paper_bgcolor=t["plot_paper"],
        xaxis=dict(title="Total Sales", tickformat=",.0f", showgrid=True,
                   gridcolor=t["grid"], tickfont=dict(size=10,color=t["tick"]),
                   title_font=dict(color=t["tick"])),
        yaxis=dict(title="Total Profit", tickformat=",.0f", showgrid=True,
                   gridcolor=t["grid"], tickfont=dict(size=10,color=t["tick"]),
                   title_font=dict(color=t["tick"])),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top", y=-0.22,
            xanchor="center", x=0.5,
            font=dict(size=10, color=t["text"]),
            itemsizing="constant",
            tracegroupgap=0,
        ),
        annotations=annotations,
        margin=dict(l=10, r=10, t=45, b=70),
        font=dict(family="DM Sans",color=t["text"]),
    )
    st.plotly_chart(fig_sc, use_container_width=True)

st.divider()

# ── Insight Bisnis ────────────────────────────────────────────────────────
st.markdown(section_label("Insight Bisnis", t), unsafe_allow_html=True)
i1,i2 = st.columns(2)
insights = [
    (i1, "#DC2626", "Sub-kategori dengan Kerugian Terbesar",
     "<b>Tables</b> mencatat 83% bulan merugi dengan rata-rata margin –14.8%. "
     "<b>Bookcases</b> (56.5% bulan rugi, margin –12.7%) dan <b>Binders</b> "
     "(margin –20.3%) menyusul sebagai sub-kategori paling tidak menguntungkan."),
    (i2, "#D97706", "Ambang Batas Diskon Kritis",
     "Diskon ≥ 30% pada <b>Tables</b> menyebabkan 93–100% transaksi merugi. "
     "<b>Binders</b> dengan diskon 70–80% menghasilkan kerugian di 100% transaksi. "
     "Rata-rata diskon transaksi merugi (0.37) vs menguntungkan (0.08)."),
]
for col, clr, title, body in insights:
    with col:
        st.markdown(card_wrap(
            f'<div style="font-size:0.8rem;font-weight:600;color:{clr};margin-bottom:0.5rem;">{title}</div>'
            f'<div style="font-size:0.8rem;color:{t["muted"]};line-height:1.6;">{body}</div>',
            t, border_color=clr
        ), unsafe_allow_html=True)

st.markdown("<div style='margin-top:0.75rem;'></div>", unsafe_allow_html=True)
i3,i4 = st.columns(2)
insights2 = [
    (i3, "#059669", "Sub-kategori Paling Stabil",
     "Art, Labels, Envelopes, Accessories, Paper, Copiers, dan Fasteners tidak pernah "
     "mencatat bulan merugi sepanjang 2014–2017. Sub-kategori ini dapat diandalkan "
     "sebagai sumber pendapatan stabil."),
    (i4, "#6366F1", "Rekomendasi Strategis",
     "Batasi diskon Tables dan Bookcases maks 20%. Tinjau strategi diskon Binders. "
     "Prioritaskan promosi pada <b>Technology</b> (margin +15.6%) dan <b>Copiers</b> "
     "dengan margin tertinggi +37.8%."),
]
for col, clr, title, body in insights2:
    with col:
        st.markdown(card_wrap(
            f'<div style="font-size:0.8rem;font-weight:600;color:{clr};margin-bottom:0.5rem;">{title}</div>'
            f'<div style="font-size:0.8rem;color:{t["muted"]};line-height:1.6;">{body}</div>',
            t, border_color=clr
        ), unsafe_allow_html=True)