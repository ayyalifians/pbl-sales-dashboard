import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 1. Deteksi otomatis lokasi file .env berdasarkan direktori projek
current_dir = Path(__file__).resolve().parent  # direktori folder 'database'
project_root = current_dir.parent             # direktori utama projek
env_path = project_root / '.env'

print(f"🔍 Mencari file .env di lokasi: {env_path}")

if not env_path.exists():
    print("❌ ERROR: File .env tidak ditemukan di lokasi tersebut! Pastikan nama file Anda sudah benar '.env' (menggunakan titik di depan, bukan env atau env.txt).")
else:
    print("✅ File .env ditemukan. Mencoba membaca isi data...")
    load_dotenv(dotenv_path=env_path)

# 2. Ambil nilai dari .env
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# 3. Print isi untuk debugging (Aman, password disensor sebagian)
print("\n--- Hasil Pembacaan .env ---")
print(f"DB_USER: {db_user}")
print(f"DB_PASSWORD: {'*** Terisi ***' if db_password else '❌ KOSONG'}")
print(f"DB_HOST: {db_host}")
print(f"DB_PORT: '{db_port}' (Tipe data: {type(db_port)})")
print(f"DB_NAME: {db_name}")
print("----------------------------\n")

# 4. Solusi paksa jika dari file .env masih terbaca kosong atau None
if not db_port or db_port.strip() == "":
    print("⚠️ Peringatan: DB_PORT di .env kosong atau tidak terbaca. Memaksa menggunakan port fallback '6543'.")
    db_port = 6543
else:
    db_port = int(db_port)

# 5. Buat connection string dan jalankan engine (Versi Perbaikan Argumen)
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

try:
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "connect_timeout": 30,
            "options": "-c prepare_threshold=0"  # Cara paling aman menonaktifkan prepared statement di psycopg2
        }
    )
    with engine.connect() as conn:
        print("🎉 BERHASIL! Koneksi ke Supabase sukses dan stabil!")
except Exception as e:
    print(f"❌ Terjadi kesalahan saat membuat engine atau koneksi: {e}")
