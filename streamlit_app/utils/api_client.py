"""
utils/api_client.py
Komunikasi ke FastAPI backend.
Base URL: http://localhost:8000
"""

import requests
import streamlit as st

API_BASE = "http://localhost:8000"
VALID_CATEGORIES = ["Furniture", "Office Supplies", "Technology"]


def check_health() -> bool:
    try:
        r = requests.get(f"{API_BASE}/dashboard/summary", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


@st.cache_data(ttl=300)
def fetch_summary() -> dict:
    r = requests.get(f"{API_BASE}/dashboard/summary", timeout=10)
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=300)
def fetch_sales_monthly(category: str = None, year: int = None) -> dict:
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
    params = {}
    if year:
        params["year"] = year
    r = requests.get(f"{API_BASE}/dashboard/sales-by-category", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=300)
def fetch_top_products(limit: int = 10, category: str = None) -> dict:
    params = {"limit": limit}
    if category:
        params["category"] = category
    r = requests.get(f"{API_BASE}/dashboard/top-products", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def predict_sales_next(category: str) -> dict:
    r = requests.post(
        f"{API_BASE}/predict/predict-sales",
        json={"category": category},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=300)
def fetch_forecast(category: str) -> dict:
    # Encode spasi → %20 otomatis oleh requests
    r = requests.get(
        f"{API_BASE}/predict/forecast/{category}",
        timeout=30
    )
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=300)
def fetch_metrics(category: str) -> dict:
    r = requests.get(f"{API_BASE}/predict/metrics/{category}", timeout=10)
    r.raise_for_status()
    return r.json()
