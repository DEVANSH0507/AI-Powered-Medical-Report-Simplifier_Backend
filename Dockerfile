# ---------- Base Python image ----------
FROM python:3.10-slim

# ---------- Install system dependencies ----------
# Tesseract OCR + Poppler for PDFs + OpenCV dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ---------- Set working directory ----------
WORKDIR /app

# ---------- Copy requirements first (for faster Docker caching) ----------
COPY requirements.txt .

# ---------- Install Python dependencies ----------
# ✅ Add opencv-python-headless here to ensure cv2 works
RUN pip install --no-cache-dir -r requirements.txt opencv-python-headless

# ---------- Copy all source code ----------
COPY . .

# ---------- Expose API port ----------
EXPOSE 8000

# ---------- Run FastAPI app ----------
# Modify "app.main:app" if your entry point differs
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
