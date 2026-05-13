import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
from sqlalchemy import create_engine, text
from pycaret.time_series import TSForecastingExperiment

# ── Inisialisasi app ──
app = FastAPI(
    title="Sales Forecasting API - Kelompok 6",
    description="API prediksi penjualan berbasis Machine Learning (PyCaret Time Series)",
    version="1.0.0"
)

# ── Koneksi database ──
engine = create_engine(
    "postgresql+psycopg2://postgres:mabaPENS24@localhost:5432/superstore_db"
)

# ── Load semua model saat server pertama kali nyala ──
exp = TSForecastingExperiment()
models = {
    "Furniture":       exp.load_model("model_furniture"),
    "Office Supplies": exp.load_model("model_office_supplies"),
    "Technology":      exp.load_model("model_technology"),
}
print("Semua model berhasil dimuat!")

# ── Schema request & response ──
class ForecastRequest(BaseModel):
    category: Literal["Furniture", "Office Supplies", "Technology"]
    periods: Optional[int] = 6

class ForecastResponse(BaseModel):
    category: str
    periods: int
    forecast: list

# ── Endpoint 1: Health check ──
@app.get("/", tags=["General"])
async def root():
    return {"status": "running", "message": "Sales Forecasting API aktif"}

# ── Endpoint 2: Prediksi penjualan ──
@app.post("/predict", tags=["Forecasting"], response_model=ForecastResponse)
async def predict_sales(request: ForecastRequest):
    """
    Prediksi penjualan ke depan berdasarkan kategori produk.
    - **category**: Furniture | Office Supplies | Technology
    - **periods**: jumlah bulan yang ingin diprediksi (default 6)
    """
    if request.periods < 1 or request.periods > 24:
        raise HTTPException(status_code=400,
                            detail="periods harus antara 1 sampai 24")

    model = models[request.category]
    forecast_df = exp.predict_model(model, fh=request.periods)

    result = forecast_df.reset_index()
    result.columns = ["period", "predicted_sales"]
    result["period"] = result["period"].astype(str)
    result["predicted_sales"] = result["predicted_sales"].round(2)

    return {
        "category": request.category,
        "periods": request.periods,
        "forecast": result.to_dict(orient="records")
    }

# ── Endpoint 3: Data historis dari database ──
@app.get("/sales/history", tags=["Data"])
async def get_sales_history(category: Optional[str] = None):
    """
    Ambil data penjualan historis bulanan dari database.
    Bisa difilter by category.
    """
    if category:
        query = text("""
            SELECT year, month, category, sub_category,
                   total_sales, total_profit, num_orders
            FROM ts_sales_monthly
            WHERE category = :cat
            ORDER BY year, month
        """)
        df = pd.read_sql(query, engine, params={"cat": category})
    else:
        query = text("""
            SELECT year, month, category,
                   SUM(total_sales) as total_sales,
                   SUM(total_profit) as total_profit,
                   SUM(num_orders) as num_orders
            FROM ts_sales_monthly
            GROUP BY year, month, category
            ORDER BY year, month, category
        """)
        df = pd.read_sql(query, engine)

    return {"data": df.to_dict(orient="records")}

# ── Endpoint 4: Ambil hasil prediksi yang tersimpan di DB ──
@app.get("/predictions/saved", tags=["Data"])
async def get_saved_predictions(category: Optional[str] = None):
    """
    Ambil prediksi yang sudah tersimpan di tabel ml_predictions.
    """
    if category:
        query = text("""
            SELECT * FROM ml_predictions
            WHERE category = :cat
            ORDER BY target_year, target_month
        """)
        df = pd.read_sql(query, engine, params={"cat": category})
    else:
        df = pd.read_sql(
            "SELECT * FROM ml_predictions ORDER BY category, target_year, target_month",
            engine
        )
    return {"data": df.to_dict(orient="records")}

# ── Jalankan server ──
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)