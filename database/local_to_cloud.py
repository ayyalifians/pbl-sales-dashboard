import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text

# 1. Load file .env
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# ==========================================
# KONFIGURASI ENGINE 1: POSTGRES LOKAL
# ==========================================
# Silakan sesuaikan isian di bawah ini dengan pgAdmin lokal Anda jika berbeda
LOCAL_USER = "postgres"
LOCAL_PASSWORD = "mabaPENS24"  # <-- Ganti dengan password pgAdmin Anda
LOCAL_HOST = "localhost"
LOCAL_PORT = "5432"
LOCAL_DB_NAME = "superstore_db"    # <-- Ganti dengan nama database di pgAdmin

local_url = f"postgresql://{LOCAL_USER}:{LOCAL_PASSWORD}@{LOCAL_HOST}:{LOCAL_PORT}/{LOCAL_DB_NAME}"
engine_lokal = create_engine(local_url)

# ==========================================
# KONFIGURASI ENGINE 2: SUPABASE CLOUD (Dari .env yang sudah sukses)
# ==========================================
supabase_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine_supabase = create_engine(
    supabase_url,
    connect_args={
        "connect_timeout": 30,
        "options": "-c prepare_threshold=0"
    }
)

# ==========================================
# PROSES MIGRASI DATA LANGSUNG
# ==========================================
# Tuliskan nama-nama tabel di pgAdmin lokal Anda yang ingin dipindahkan ke Supabase
# Contoh: ["sales", "products", "customers"]
TABEL_YANG_INGIN_DIPINDAHKAN = [
    "users",
    "ts_sales_monthly",
    "locations",
    "customers",
    "products",
    "shipments",
    "orders",
    "ml_predictions"
]

print("🚀 Memulai proses migrasi data dari Lokal ke Supabase...")

try:
    # Tes koneksi ke kedua database terlebih dahulu
    with engine_lokal.connect() as conn_lokal, engine_supabase.connect() as conn_supa:
        print("✅ Kedua database berhasil terhubung!")
        
        for nama_tabel in TABEL_YANG_INGIN_DIPINDAHKAN:
            print(f"\n⏳ Memproses tabel '{nama_tabel}'...")
            
            # 1. Baca data dari lokal ke dalam Pandas DataFrame
            df = pd.read_sql_query(f"SELECT * FROM {nama_tabel}", engine_lokal)
            print(f"   -> Berhasil membaca {len(df)} baris data dari database lokal.")
            
            # 2. Upload langsung data tersebut ke Supabase
            # 'if_exists=replace' akan otomatis membuat tabel baru di Supabase jika belum ada
            df.to_sql(nama_tabel, engine_supabase, if_exists='replace', index=False)
            print(f"   -> 🎉 Sukses meng-upload tabel '{nama_tabel}' ke Supabase Cloud!")
            
    print("\n🌟 SEMUA DATA BERHASIL DIPINDAHKAN KE SUPABASE!")

except Exception as e:
    print(f"\n❌ Terjadi kesalahan saat migrasi data: {e}")
