# database/connection.py
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from fastapi import HTTPException
import logging
import sys
import os

load_dotenv()

logger = logging.getLogger(__name__)

logger.info("[db/connection] Module loading...")

DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = os.getenv("DB_PORT", "6543")
DB_NAME     = os.getenv("DB_NAME")

logger.info(
    "[db/connection] Env vars — DB_HOST=%s DB_PORT=%s DB_NAME=%s DB_USER=%s DB_PASSWORD=%s",
    DB_HOST or "MISSING",
    DB_PORT,
    DB_NAME or "MISSING",
    DB_USER or "MISSING",
    "SET" if DB_PASSWORD else "MISSING",
)

Base = declarative_base()

# Check which vars are missing and warn — but do NOT raise at import time.
_missing_vars = [
    k for k, v in {
        "DB_USER"    : DB_USER,
        "DB_PASSWORD": DB_PASSWORD,
        "DB_HOST"    : DB_HOST,
        "DB_NAME"    : DB_NAME,
    }.items() if not v
]

if _missing_vars:
    logger.warning(
        "[db/connection] Database environment variables tidak lengkap: %s. "
        "Endpoint yang membutuhkan database akan mengembalikan HTTP 503.",
        _missing_vars,
    )
    print(
        f"[database/connection.py] WARNING: env vars tidak lengkap: {_missing_vars}. "
        "DB engine tidak dibuat.",
        file=sys.stderr,
        flush=True,
    )
    engine       = None
    SessionLocal = None
else:
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    # Log URL tanpa password untuk debugging
    _safe_url = f"postgresql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    logger.info("[db/connection] Creating engine: %s", _safe_url)

    try:
        engine = create_engine(
            DATABASE_URL,
            connect_args={
                "connect_timeout": 5,               # turun dari 10 → 5 detik agar cepat fail
                "options": "-c prepare_threshold=0" # wajib untuk Transaction Pooler Supabase
            },
            pool_pre_ping=True,   # validasi koneksi sebelum dipakai
            pool_timeout=10,      # turun dari 20 → 10 detik
            pool_recycle=300,
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info(
            "[db/connection] Engine created OK (host=%s, port=%s, db=%s).",
            DB_HOST, DB_PORT, DB_NAME,
        )
    except Exception as exc:
        print(
            f"[database/connection.py] ERROR: Gagal membuat database engine: {exc}",
            file=sys.stderr,
            flush=True,
        )
        logger.error("[db/connection] Gagal membuat database engine: %s", exc, exc_info=True)
        engine       = None
        SessionLocal = None

logger.info("[db/connection] Module loaded. engine=%s", "OK" if engine else "None")


def get_db():
    """
    FastAPI dependency yang menyediakan sesi database.
    Mengembalikan HTTP 503 jika engine tidak tersedia,
    sehingga aplikasi tetap bisa start meski DB belum siap.
    """
    if SessionLocal is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Database tidak tersedia. "
                "Periksa environment variables (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME) "
                "dan pastikan database dapat diakses."
            )
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> dict:
    """
    Cek koneksi database secara aktif.
    Dipakai oleh /health endpoint — tidak pernah raise exception.
    """
    logger.info("[db/connection] check_db_connection() called")
    if engine is None:
        logger.warning("[db/connection] check_db_connection: engine is None, missing=%s", _missing_vars)
        return {
            "status" : "unavailable",
            "detail" : f"Engine tidak dibuat. Env vars hilang: {_missing_vars}"
        }
    try:
        logger.info("[db/connection] Attempting SELECT 1 test query...")
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("[db/connection] SELECT 1 OK — database is reachable")
        return {"status": "connected"}
    except Exception as exc:
        logger.error("[db/connection] SELECT 1 FAILED: %s", exc, exc_info=True)
        return {"status": "error", "detail": str(exc)}
