import pickle
import os

BASE_DIR = r"C:\Users\user\Documents\SDT B PENS 2024\Semester 4\Praktikum Teknologi Web Service\PBL\pbl-sales-dashboard"

files = {
    "Furniture"      : "models/final_omp_furniture.pkl",
    "Office Supplies": "models/final_arima_office_supplies.pkl",
    "Technology"     : "models/final_theta_technology.pkl"
}

for category, path in files.items():
    filepath = os.path.join(BASE_DIR, path)
    print(f"\n{'='*50}")
    print(f"Kategori : {category}")
    
    with open(filepath, 'rb') as f:
        isi = pickle.load(f)
    
    model_content = isi['model']
    print(f"Tipe model content : {type(model_content)}")
    
    # Kalau tuple, cek tiap elemennya
    if isinstance(model_content, tuple):
        print(f"Jumlah elemen tuple: {len(model_content)}")
        for i, elem in enumerate(model_content):
            print(f"  [{i}] → {type(elem).__name__} : {str(elem)[:80]}")
    
    # Kalau langsung object
    else:
        print(f"Model object : {model_content}")
        print(f"Methods      : {[m for m in dir(model_content) if not m.startswith('_')][:10]}")
    
    # Cek forecast juga
    forecast_files = {
        "Furniture"      : "models/forecast/forecast_omp_furniture.pkl",
        "Office Supplies": "models/forecast/forecast_arima_office_supplies.pkl",
        "Technology"     : "models/forecast/forecast_theta_technology.pkl"
    }
    
    fpath = os.path.join(BASE_DIR, forecast_files[category])
    print(f"\nForecast file:")
    with open(fpath, 'rb') as f:
        forecast = pickle.load(f)
    print(f"  Tipe    : {type(forecast)}")
    if hasattr(forecast, 'shape'):
        print(f"  Shape   : {forecast.shape}")
    if hasattr(forecast, 'keys'):
        print(f"  Keys    : {list(forecast.keys())}")
    if isinstance(forecast, (list, tuple)):
        print(f"  Length  : {len(forecast)}")
        print(f"  Contoh  : {forecast[:3]}")
    if hasattr(forecast, 'head'):
        print(f"  Head    :\n{forecast.head()}")