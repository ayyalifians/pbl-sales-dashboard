# test_db.py
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os

load_dotenv()

host     = os.getenv('DB_HOST')
user     = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port     = os.getenv('DB_PORT', '5432')
name     = os.getenv('DB_NAME')

print("=== CEK ENV VARIABLES ===")
print(f"DB_HOST     : {host}")
print(f"DB_USER     : {user}")
print(f"DB_PASSWORD : {'*' * len(password) if password else 'KOSONG!'}")
print(f"DB_PORT     : {port}")
print(f"DB_NAME     : {name}")

# Cek apakah ada yang kosong
missing = []
if not host:     missing.append('DB_HOST')
if not user:     missing.append('DB_USER')
if not password: missing.append('DB_PASSWORD')
if not name:     missing.append('DB_NAME')

if missing:
    print(f"\n❌ ENV VARIABLE KOSONG: {missing}")
    print("Pastikan .env sudah diisi dengan benar!")
else:
    print("\n✅ Semua env variable terisi")
    print("\n=== TEST KONEKSI DB ===")

    url = f"postgresql://{user}:{password}@{host}:{port}/{name}"

    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            # Test 1: koneksi basic
            conn.execute(text("SELECT 1"))
            print("✅ Koneksi berhasil!")

            # Test 2: cek tabel yang dibutuhkan
            tables = [
                'orders',
                'products',
                'customers',
                'ts_sales_monthly',
            ]
            print("\n=== CEK TABEL ===")
            for table in tables:
                try:
                    r = conn.execute(
                        text(f"SELECT COUNT(*) FROM {table}")
                    )
                    count = r.fetchone()[0]
                    print(f"✅ {table:<25} : {count:>6} rows")
                except Exception as e:
                    print(f"❌ {table:<25} : TIDAK ADA ({e})")

    except Exception as e:
        print(f"❌ Koneksi gagal: {e}")
        print("\nKemungkinan penyebab:")
        print("  1. Password salah")
        print("  2. Host salah")
        print("  3. IP belum diwhitelist di Supabase")