# Jalankan di Cell paling awal notebook, sebelum insert apapun
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg2://postgres:mabaPENS24@localhost:5432/superstore_db")

# Lihat struktur semua tabel sekaligus
query = """
SELECT table_name, column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
"""
print(pd.read_sql(query, engine).to_string())

# # Menghapus semua data yang terlanjur menumpuk agar bersih kembali
# with engine.connect() as conn:
#     conn.execute(text("""
#         TRUNCATE TABLE 
#             orders, customers, shipments, products, locations, ts_sales_monthly 
#         RESTART IDENTITY CASCADE;
#     """))
#     conn.commit()
# print("Database berhasil dikosongkan!")