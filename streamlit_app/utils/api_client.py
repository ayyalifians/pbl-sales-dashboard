"""
utils/api_client.py
Semua fungsi komunikasi ke FastAPI backend (Alifia).
Base URL: http://localhost:8000  ← FastAPI default port, bukan 5000
"""

import requests
import streamlit as st

API_BASE = "http://localhost:8000"

VALID_CATEGORIES = ["Furniture", "Office Supplies", "Technology"]

# ════════════════════════════════
#   HEALTH CHECK
# ════════════════════════════════

def check_health() -> bool:
    """Cek apakah FastAPI aktif."""
    try:
        r = requests.get(f"{API_BASE}/dashboard/summary", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


# ════════════════════════════════
#   DASHBOARD ENDPOINTS
# ════════════════════════════════

@st.cache_data(ttl=300)
def fetch_summary() -> dict:
    """
    GET /dashboard/summary
    Response:
    {
        "total_sales"    : 2297201.0,
        "total_profit"   : 286397.0,
        "total_orders"   : 9994,
        "total_customers": 793
    }
    """
    r = requests.get(f"{API_BASE}/dashboard/summary", timeout=10)
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=300)
def fetch_sales_monthly(category: str = None, year: int = None) -> dict:
    """
    GET /dashboard/sales-monthly?category=Furniture&year=2017
    Response:
    {
        "total_records": 48,
        "filter": { "category": "Furniture", "year": "All" },
        "data": [
            { "year":2014, "month":1, "category":"Furniture",
              "total_sales":1234.5, "total_profit":200.0, "num_orders":5 },
            ...
        ]
    }
    """
    params = {}
    if category:
        params["category"] = category
    if year:
        params["year"] = year
    r = requests.get(f"{API_BASE}/dashboard/sales-monthly", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=300)
def fetch_sales_by_category(year: int = None) -> dict:
    """
    GET /dashboard/sales-by-category?year=2017
    Response:
    {
        "filter": { "year": "All" },
        "data": [
            { "category":"Technology", "total_sales":836154.0,
              "total_profit":145454.0, "total_orders":1847 },
            ...
        ]
    }
    """
    params = {}
    if year:
        params["year"] = year
    r = requests.get(f"{API_BASE}/dashboard/sales-by-category", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=300)
def fetch_top_products(limit: int = 10, category: str = None) -> dict:
    """
    GET /dashboard/top-products?limit=10&category=Technology
    Response:
    {
        "total_records": 10,
        "data": [
            { "product_name":"...", "category":"...", "sub_category":"...",
              "total_sales":1234.0, "total_profit":200.0, "total_orders":5 },
            ...
        ]
    }
    """
    params = {"limit": limit}
    if category:
        params["category"] = category
    r = requests.get(f"{API_BASE}/dashboard/top-products", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


# ════════════════════════════════
#   PREDICT ENDPOINTS
# ════════════════════════════════

def predict_sales_next(category: str) -> dict:
    """
    POST /predict/predict-sales
    Body    : { "category": "Furniture" }
    Response:
    {
        "category"       : "Furniture",
        "predicted_sales": 12345.67,
        "model_used"     : "OMP"
    }
    """
    r = requests.post(
        f"{API_BASE}/predict/predict-sales",
        json={"category": category},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=300)
def fetch_forecast(category: str) -> dict:
    """
    GET /predict/forecast/{category}
    Response:
    {
        "category"     : "Furniture",
        "model_used"   : "OMP",
        "total_periods": 12,
        "forecast": [
            { "period":"2018-01", "forecast_sales":12345.67,
              "lower_bound":10000.0, "upper_bound":15000.0 },
            ...
        ]
    }
    """
    r = requests.get(f"{API_BASE}/predict/forecast/{category}", timeout=30)
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=300)
def fetch_metrics(category: str) -> dict:
    """
    GET /predict/metrics/{category}
    Response:
    {
        "category"    : "Furniture",
        "model_used"  : "OMP",
        "params"      : { "n_lags": 6 },
        "val_metrics" : { "mae":..., "rmse":..., "mape":..., "r2":... },
        "test_metrics": { "mae":..., "rmse":..., "mape":..., "r2":... }
    }
    """
    r = requests.get(f"{API_BASE}/predict/metrics/{category}", timeout=10)
    r.raise_for_status()
    return r.json()
