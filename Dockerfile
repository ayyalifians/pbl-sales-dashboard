# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements dulu (layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --default-timeout=1000 -r requirements.txt

# Copy semua file project
COPY . .

# Expose port
EXPOSE 8000

# Jalankan validate_env dulu (--warn: tidak crash jika ada var hilang, hanya log),
# lalu start Uvicorn. Output validate_env akan terlihat di Railway deploy logs.
CMD ["sh", "-c", "python validate_env.py --warn && uvicorn api.main:app --host 0.0.0.0 --port 8000 --log-level debug"]