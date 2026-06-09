# api/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.routers import predict, dashboard
from database.connection import check_db_connection
import logging
import sys

# ---------------------------------------------------------------------------
# Logging — tulis ke stdout agar Railway menangkap semua output
# ---------------------------------------------------------------------------
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Sales Forecasting API - Kelompok 6",
    description="API prediksi penjualan berbasis Machine Learning (PyCaret Time Series)",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Startup + shutdown event handlers
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("=== Application starting up ===")
    db_status = check_db_connection()
    if db_status["status"] == "connected":
        logger.info("Database connection: OK")
    else:
        logger.warning(
            "Database connection: %s — %s",
            db_status["status"],
            db_status.get("detail", ""),
        )
        logger.warning(
            "Aplikasi tetap berjalan. Endpoint DB akan mengembalikan HTTP 503 "
            "sampai database tersedia."
        )
    logger.info("=== Application started successfully ===")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("=== Application shutting down ===")


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Global exception handler — tangkap semua error yang tidak ter-handle
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception on %s %s: %s",
        request.method,
        request.url.path,
        exc,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error"  : "Internal server error",
            "detail" : str(exc),
            "path"   : request.url.path,
        },
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(predict.router)
app.include_router(dashboard.router)


# ---------------------------------------------------------------------------
# General endpoints
# ---------------------------------------------------------------------------
@app.get("/", tags=["General"])
async def root():
    return {
        "message": "Sales Forecasting API - Kelompok 6",
        "status" : "running",
        "version": "1.0.0",
        "docs"   : "/docs",
    }


@app.get("/health", tags=["General"])
async def health_check():
    """
    Health check endpoint — selalu mengembalikan HTTP 200.
    Menyertakan status database sebagai informasi tambahan,
    tapi TIDAK gagal meski database tidak tersedia.
    """
    db_status = check_db_connection()
    return {
        "status"  : "ok",
        "version" : "1.0.0",
        "database": db_status,
    }