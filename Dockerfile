# ---------- Base Python image ----------
FROM python:3.10-slim

# ---------- Install system dependencies ----------
# (Tesseract OCR + Poppler + OpenCV runtime libraries)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# ---------- Set working directory ----------
WORKDIR /app

# ---------- Copy requirements first (for better build caching) ----------
COPY requirements.txt .

# ---------- Install Python dependencies ----------
# Important: install dependencies exactly as defined in requirements.txt
# Do not append packages directly on this line — it can break pip caching.
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy the complete source code ----------
COPY . .

# ---------- Expose API port ----------
EXPOSE 8000

# ---------- Start FastAPI application ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
