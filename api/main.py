# api/main.py
import logging
import sys

# ---------------------------------------------------------------------------
# Logging — setup PERTAMA sebelum import apapun agar semua log tertangkap
# ---------------------------------------------------------------------------
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

logger.info(">>> [1/7] Logging initialized")

# ---------------------------------------------------------------------------
# Import FastAPI core
# ---------------------------------------------------------------------------
logger.info(">>> [2/7] Importing FastAPI core...")
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
logger.info(">>> [2/7] FastAPI core imported OK")

# ---------------------------------------------------------------------------
# Import database module
# ---------------------------------------------------------------------------
logger.info(">>> [3/7] Importing database.connection...")
from database.connection import check_db_connection
logger.info(">>> [3/7] database.connection imported OK")

# ---------------------------------------------------------------------------
# Import routers
# ---------------------------------------------------------------------------
logger.info(">>> [4/7] Importing router: predict...")
from api.routers import predict
logger.info(">>> [4/7] Router predict imported OK")

logger.info(">>> [5/7] Importing router: dashboard...")
from api.routers import dashboard
logger.info(">>> [5/7] Router dashboard imported OK")


# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------
logger.info(">>> [6/7] Creating FastAPI app instance...")
app = FastAPI(
    title="Sales Forecasting API - Kelompok 6",
    description="API prediksi penjualan berbasis Machine Learning (PyCaret Time Series)",
    version="1.0.0",
)
logger.info(">>> [6/7] FastAPI app instance created OK")


# ---------------------------------------------------------------------------
# Startup + shutdown event handlers
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("=== Application starting up ===")
    logger.info(">>> Checking database connection...")
    db_status = check_db_connection()
    if db_status["status"] == "connected":
        logger.info(">>> Database connection: OK")
    else:
        logger.warning(
            ">>> Database connection: %s — %s",
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
# NOTE: Routers di-comment out sementara untuk isolasi masalah.
#       Jika aplikasi respond normal tanpa routers, masalah ada di salah satu router.
#       Uncomment satu per satu untuk menemukan router yang bermasalah.
# ---------------------------------------------------------------------------
logger.info(">>> [7/7] Registering routers...")

# --- ROUTER PREDICT (comment out untuk isolasi) ---
app.include_router(predict.router)
logger.info(">>> [7/7] predict router registered OK")

# --- ROUTER DASHBOARD (comment out untuk isolasi) ---
app.include_router(dashboard.router)
logger.info(">>> [7/7] dashboard router registered OK")

logger.info(">>> [7/7] All routers registered. App is ready.")


# ---------------------------------------------------------------------------
# General endpoints — selalu aktif, tidak butuh database
# ---------------------------------------------------------------------------
@app.get("/", tags=["General"])
async def root():
    logger.debug("GET / called")
    return {
        "message": "Sales Forecasting API - Kelompok 6",
        "status" : "running",
        "version": "1.0.0",
        "docs"   : "/docs",
        "debug"  : "routers=predict+dashboard",
    }


@app.get("/health", tags=["General"])
async def health_check():
    """
    Health check endpoint — selalu mengembalikan HTTP 200.
    Menyertakan status database sebagai informasi tambahan,
    tapi TIDAK gagal meski database tidak tersedia.
    """
    logger.debug("GET /health called")
    db_status = check_db_connection()
    return {
        "status"  : "ok",
        "version" : "1.0.0",
        "database": db_status,
    }