# api/ml_loader.py
import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, 'models')

MODEL_MAP = {
    "Furniture"      : "final_omp_furniture.pkl",
    "Office Supplies": "final_arima_office_supplies.pkl",
    "Technology"     : "final_theta_technology.pkl"
}

FORECAST_MAP = {
    "Furniture"      : os.path.join("forecast", "forecast_omp_furniture.pkl"),
    "Office Supplies": os.path.join("forecast", "forecast_arima_office_supplies.pkl"),
    "Technology"     : os.path.join("forecast", "forecast_theta_technology.pkl")
}

def load_model_data(category: str) -> dict:
    if category not in MODEL_MAP:
        raise ValueError(f"Kategori '{category}' tidak valid")
    filepath = os.path.join(MODEL_DIR, MODEL_MAP[category])
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File tidak ditemukan: {filepath}")
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def load_forecast_data(category: str) -> dict:
    if category not in FORECAST_MAP:
        raise ValueError(f"Kategori '{category}' tidak valid")
    filepath = os.path.join(MODEL_DIR, FORECAST_MAP[category])
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File tidak ditemukan: {filepath}")
    with open(filepath, 'rb') as f:
        return pickle.load(f)