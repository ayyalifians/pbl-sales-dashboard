# PBL Sales Dashboard — Kelompok 6
**Sistem Web Service Dashboard Monitoring dan Prediksi Penjualan Berbasis Machine Learning**

MLOps | Teknologi Web Service | Data Mining

---

## Tech Stack
- **Backend**  : FastAPI (Railway) + Python
- **Frontend** : Streamlit
- **Database** : Supabase (PostgreSQL)
- **ML Models**: ARIMA, OMP, Theta (statsmodels + sklearn)
- **Container**: Docker + DockerHub

---

## Cara Menjalankan dengan Docker

### Prerequisites
- Docker Desktop sudah terinstall
- File `.env` sudah dikonfigurasi

### 1. Clone Repository
git clone https://github.com/ayyalifians/pbl-sales-dashboard.git
cd pbl-sales-dashboard
git checkout main

### 2. Setup Environment
cp .env.example .env
# Edit .env dengan kredensial database yang benar

### 3. Pull dan Jalankan Docker
docker pull [username]/pbl-ml-model:latest
docker pull [username]/pbl-web:latest
docker compose up -d

### 4. Akses Aplikasi
- FastAPI Docs : http://localhost:8000/docs
- Streamlit UI : http://localhost:8501
- API Health   : http://localhost:8000/health

---

## Docker Images
- ML Model API : https://hub.docker.com/r/ayyalifians/pbl-ml-model
- Web Dashboard: https://hub.docker.com/r/ayyalifians/pbl-web

---

## Struktur Project
pbl-sales-dashboard/
├── api/                → FastAPI endpoints
├── database/           → Koneksi database
├── models/             → File model (.pkl)
├── notebooks/          → Jupyter notebooks (EDA + Modeling)
├── streamlit_app/      → Streamlit UI
├── data/               → Dataset
├── Dockerfile          → Container ML Model
├── Dockerfile.streamlit→ Container Web
└── docker-compose.yml  → Orchestration