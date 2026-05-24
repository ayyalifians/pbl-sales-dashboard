# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import predict, data

app = FastAPI(
    title="Sales Forecasting API - Kelompok 6",
    description="API prediksi penjualan berbasis Machine Learning (PyCaret Time Series)",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──
app.include_router(predict.router)
app.include_router(data.router)

# ── General ──
@app.get("/", tags=["General"])
async def root():
    return {
        "message": "Sales Forecasting API - Kelompok 6",
        "status" : "running",
        "version": "1.0.0",
        "docs"   : "/docs"
    }