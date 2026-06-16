#!/usr/bin/env python3
"""
validate_env.py — Cek environment variables sebelum aplikasi start.

Cara pakai:
  python validate_env.py            # exit 0 jika OK, exit 1 jika ada yang hilang
  python validate_env.py --warn     # selalu exit 0, hanya print warning (mode Railway)

Di Dockerfile, tambahkan sebelum CMD uvicorn:
  RUN python validate_env.py --warn
  atau
  CMD ["sh", "-c", "python validate_env.py --warn && uvicorn api.main:app --host 0.0.0.0 --port 8000"]
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = {
    "DB_USER"    : "Username database PostgreSQL",
    "DB_PASSWORD": "Password database PostgreSQL",
    "DB_HOST"    : "Host database PostgreSQL (misal: db.xxx.supabase.co)",
    "DB_NAME"    : "Nama database PostgreSQL",
}

OPTIONAL_VARS = {
    "DB_PORT": "Port database (default: 6543 untuk Supabase Transaction Pooler)",
}

warn_only = "--warn" in sys.argv

print("=" * 60)
print("  validate_env.py — Pengecekan Environment Variables")
print("=" * 60)

missing  = []
present  = []

for var, description in REQUIRED_VARS.items():
    value = os.getenv(var)
    if value:
        # Sensor nilai agar tidak bocor ke log
        masked = value[:2] + "*" * (len(value) - 2) if len(value) > 2 else "**"
        present.append((var, masked))
        print(f"  [OK]      {var:<15} = {masked}  ({description})")
    else:
        missing.append(var)
        print(f"  [MISSING] {var:<15}   ({description})")

print()
for var, description in OPTIONAL_VARS.items():
    value = os.getenv(var, "(tidak di-set, pakai default)")
    print(f"  [OPT]     {var:<15} = {value}  ({description})")

print("=" * 60)

if missing:
    print(f"\n  ⚠  {len(missing)} variable wajib tidak di-set: {missing}")
    if warn_only:
        print("  Mode --warn: aplikasi tetap akan dijalankan.")
        print("  Endpoint yang membutuhkan database akan mengembalikan HTTP 503.")
        print("=" * 60)
        sys.exit(0)
    else:
        print("  Tambahkan variable di atas ke Railway → Variables.")
        print("=" * 60)
        sys.exit(1)
else:
    print(f"\n  ✓  Semua {len(REQUIRED_VARS)} variable wajib tersedia.")
    print("=" * 60)
    sys.exit(0)
