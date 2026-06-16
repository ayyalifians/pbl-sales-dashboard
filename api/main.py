# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import predict, dashboard   # ← hapus 'data' dulu

app = FastAPI(
    title="Sales Forecasting API - Kelompok 6",
    description="API prediksi penjualan berbasis Machine Learning (PyCaret Time Series)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers — fokus prioritas 1 dulu
app.include_router(predict.router)
app.include_router(dashboard.router)   # ← ini yang penting untuk Aisyah

@app.get("/", tags=["General"])
async def root():
    return {
        "message": "Sales Forecasting API - Kelompok 6",
        "status" : "running",
        "version": "1.0.0",
        "docs"   : "/docs"
    }

@app.get("/health", tags=["General"])
async def health_check():
    return {"status": "healthy"}