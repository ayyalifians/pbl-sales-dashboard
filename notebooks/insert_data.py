import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. Load variabel dari file .env
load_dotenv()

# Ambil kedua URL Database dari file .env
OLD_DB_URL = os.getenv("OLD_DATABASE_URL")
NEW_DB_URL = os.getenv("NEW_DATABASE_URL")

if not OLD_DB_URL or not NEW_DB_URL:
    print("❌ Error: Pastikan OLD_DATABASE_URL dan NEW_DATABASE_URL ada di file .env!")
    exit()

# 2. Buat "Mesin" Koneksi untuk kedua project
engine_old = create_engine(OLD_DB_URL)
engine_new = create_engine(NEW_DB_URL)

print("✅ Koneksi ke kedua database berhasil dibuat.")
print("-" * 50)

# Daftar tabel yang akan dimigrasikan (Urutan penting: Master dulu, baru Transaksi)
tables_to_migrate = [
    'users', 
    'locations', 
    'customers', 
    'products', 
    'shipments', 
    'orders', 
    'ts_sales_monthly', 
    'ml_predictions'
]

# 3. Proses looping untuk memindahkan data per tabel
for idx, table_name in enumerate(tables_to_migrate, start=1):
    print(f"[{idx}/8] Memproses tabel '{table_name}'...")
    
    try:
        # Sedot data dari project LAMA
        print(f"   -> Mengambil data dari project lama...")
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine_old)
        
        # Cek apakah tabel kosong
        if df.empty:
            print(f"   ⚠️ Tabel '{table_name}' kosong di project lama, dilewati.")
            continue
            
        # Tembak data ke project BARU
        print(f"   -> Memasukkan {len(df)} baris ke project baru...")
        df.to_sql(table_name, engine_new, if_exists='append', index=False)
        print(f"   ✅ Sukses!")
        
    except Exception as e:
        print(f"   ❌ GAGAL memproses tabel '{table_name}'. Detail error: {e}")

print("-" * 50)
print("🎉 PROSES MIGRASI SELESAI!")