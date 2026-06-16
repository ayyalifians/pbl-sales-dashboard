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

DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = os.getenv("DB_PORT", "6543")
DB_NAME     = os.getenv("DB_NAME")

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
        "Database environment variables tidak lengkap: %s. "
        "Endpoint yang membutuhkan database akan mengembalikan HTTP 503.",
        _missing_vars,
    )
    print(
        f"[database/connection.py] WARNING: env vars tidak lengkap: {_missing_vars}. "
        "DB engine tidak dibuat.",
        file=sys.stderr
    )
    engine       = None
    SessionLocal = None
else:
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    try:
        engine = create_engine(
            DATABASE_URL,
            connect_args={
                "connect_timeout": 10,              # cepat gagal agar startup tidak hang
                "options": "-c prepare_threshold=0" # wajib untuk Transaction Pooler Supabase
            },
            pool_pre_ping=True,   # validasi koneksi sebelum dipakai
            pool_timeout=20,
            pool_recycle=300,
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("Database engine berhasil dibuat (host=%s, port=%s, db=%s).",
                    DB_HOST, DB_PORT, DB_NAME)
    except Exception as exc:
        print(
            f"[database/connection.py] ERROR: Gagal membuat database engine: {exc}",
            file=sys.stderr
        )
        logger.error("Gagal membuat database engine: %s", exc, exc_info=True)
        engine       = None
        SessionLocal = None


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
    if engine is None:
        return {
            "status" : "unavailable",
            "detail" : f"Engine tidak dibuat. Env vars hilang: {_missing_vars}"
        }
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "connected"}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}
