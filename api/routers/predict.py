# api/routers/predict.py
from fastapi import APIRouter, HTTPException
from api.ml_loader import load_model_data, load_forecast_data
from api.schemas import PredictRequest, PredictResponse
import numpy as np
import traceback

router = APIRouter(
    prefix="/predict",
    tags=["Forecasting"]
)

VALID_CATEGORIES = ["Furniture", "Office Supplies", "Technology"]


# ════════════════════════════════
#   LOGIC PREDICT PER MODEL TYPE
# ════════════════════════════════

def predict_omp(model_data: dict) -> float:
    """Prediksi untuk Furniture menggunakan OMP"""
    model_tuple = model_data['model']
    omp_model   = model_tuple[0]   # OrthogonalMatchingPursuit
    scaler      = model_tuple[1]   # StandardScaler
    lag_values  = model_tuple[2]   # array nilai historis
    n_lags      = model_data['params']['n_lags']

    last_lags = lag_values[-n_lags:].reshape(1, -1)
    X_scaled  = scaler.transform(last_lags)
    result    = omp_model.predict(X_scaled)
    return float(result[0])


def predict_arima(model_data: dict) -> float:
    """Prediksi untuk Office Supplies menggunakan ARIMA"""
    arima_result = model_data['model']
    forecast     = arima_result.forecast(steps=1)
    return float(forecast.iloc[0])


def predict_theta(model_data: dict) -> float:
    """Prediksi untuk Technology menggunakan Theta"""
    theta_result = model_data['model']
    forecast     = theta_result.forecast(steps=1)
    if hasattr(forecast, 'iloc'):
        return float(forecast.iloc[0])
    return float(forecast[0])


# ════════════════════════════════
#   ENDPOINT: PREDICT SALES
# ════════════════════════════════

@router.post(
    "/predict-sales",
    response_model=PredictResponse,
    summary="Predict Sales",
    description="Prediksi penjualan berdasarkan kategori produk"
)
async def predict_sales(data: PredictRequest):
    if data.category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=404,
            detail=f"Kategori tidak valid. Pilih salah satu: {VALID_CATEGORIES}"
        )
    try:
        model_data = load_model_data(data.category)
        model_type = model_data.get('type', 'unknown')

        if model_type == 'omp':
            predicted = predict_omp(model_data)
        elif model_type == 'arima':
            predicted = predict_arima(model_data)
        elif model_type == 'theta':
            predicted = predict_theta(model_data)
        else:
            raise ValueError(f"Tipe model '{model_type}' tidak dikenali")

        return PredictResponse(
            category=data.category,
            predicted_sales=round(predicted, 2),
            model_used=model_type.upper()
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error prediksi: {str(e)}")


# ════════════════════════════════
#   ENDPOINT: FORECAST
# ════════════════════════════════

@router.get(
    "/forecast/{category}",
    summary="Get Forecast",
    description="Ambil hasil forecast per kategori produk"
)
async def get_forecast(category: str):
    if category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=404,
            detail=f"Kategori tidak valid. Pilih: {VALID_CATEGORIES}"
        )
    try:
        data             = load_forecast_data(category)
        forecast_values  = data['forecast_values']
        lower            = data['lower']
        upper            = data['upper']
        periods          = data['forecast_periods']

        result = []
        for i in range(len(forecast_values)):
            result.append({
                "period"        : str(periods[i]),
                "forecast_sales": round(float(forecast_values[i]), 2),
                "lower_bound"   : round(float(lower[i]), 2),
                "upper_bound"   : round(float(upper[i]), 2),
            })

        return {
            "category"     : category,
            "model_used"   : data.get('type', 'unknown').upper(),
            "total_periods": len(result),
            "forecast"     : result
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"ERROR forecast {category}:")
        print(traceback.format_exc()) 
        raise HTTPException(status_code=500, detail=f"Error forecast: {str(e)}")


# ════════════════════════════════
#   ENDPOINT: MODEL METRICS
# ════════════════════════════════

@router.get(
    "/metrics/{category}",
    summary="Get Model Metrics",
    description="Ambil metrik evaluasi model (MAE, RMSE, MAPE, R2)"
)
async def get_metrics(category: str):
    if category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=404,
            detail=f"Kategori tidak valid. Pilih: {VALID_CATEGORIES}"
        )
    try:
        model_data = load_model_data(category)
        return {
            "category"    : category,
            "model_used"  : model_data.get('type', 'unknown').upper(),
            "params"      : model_data.get('params', {}),
            "val_metrics" : model_data.get('val_metrics', {}),
            "test_metrics": model_data.get('test_metrics', {})
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error metrics: {str(e)}")