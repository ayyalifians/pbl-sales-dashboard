# database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "6543")  # Sudah benar default-nya 6543
DB_NAME = os.getenv("DB_NAME")

# Validasi — tidak ada fallback ke hardcode
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise ValueError(
        "Environment variables DB tidak lengkap. "
        "Pastikan .env sudah diisi dengan benar."
    )

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# --- PERBAIKAN DI BAGIAN INI ---
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "connect_timeout": 30,             # Menghindari timeout jika internet melambat
        "options": "-c prepare_threshold=0" # WAJIB agar tidak bentrok dengan Transaction Pooler Supabase
    }
)
# -------------------------------

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
