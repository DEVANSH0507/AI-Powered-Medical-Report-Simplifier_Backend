🧠 AI-Powered Medical Report Simplifier (Backend)

Developed by: Devansh Gupta
Submission: Problem Statement 7 – AI for Healthcare Simplification

📋 Overview

The AI-Powered Medical Report Simplifier intelligently converts complex medical reports into simple, human-readable summaries.
It uses OCR + Spell Correction + AI Normalization + Hallucination Guardrails to ensure high accuracy and reliability.

✅ Works with both text and scanned image/PDF reports
✅ Fixes OCR typos and formatting
✅ Generates clear, non-diagnostic summaries for patients

⚙️ Architecture

Your backend follows a modular, layered pipeline built with FastAPI and Python 3.10.

1️⃣ Input Layer

Accepts either typed text or uploaded image/PDF files.

Automatically detects the input type and processes accordingly.

📁 app/api/upload.py

2️⃣ OCR & Confidence Engine

Uses Tesseract OCR (and Poppler for PDFs) to extract text.

Calculates average OCR Confidence Score using per-word metadata.

📁 app/services/ocr.py

3️⃣ Spell Correction Layer

Fixes OCR typos using a custom medical dictionary + fuzzy matching.

Example corrections:

“Hemglobin” → “Hemoglobin”

“Hgh” → “High”

“Glocose” → “Glucose”

📁 app/services/spellCorrection.py

4️⃣ Normalization & Guardrails Layer

Extracts structured test data:
name, value, unit, status, and reference range.

Removes unwanted symbols and formats (11,200 → 11200).

Includes Guardrails to reject hallucinated tests not found in user input (via fuzzy matching).

📁 app/services/Normalize.py

5️⃣ AI Summarization Layer

Powered by NVIDIA Phi-4 Mini via OpenAI-compatible API.

Generates easy-to-understand, non-diagnostic explanations for patients.

Adds short notes and explanations for each test result.

📁 app/api/summary.py

6️⃣ Final Workflow
     ┌───────────────────────────────┐
     │      Input (Text/Image)       │
     └──────────────┬────────────────┘
                    │
                    ▼
      OCR Extraction + Confidence (Tesseract)
                    │
                    ▼
     Spell Correction (Fuzzy + Dictionary)
                    │
                    ▼
     Normalization (Regex + Range Mapping)
                    │
                    ▼
     Guardrail Validation (Anti-Hallucination)
                    │
                    ▼
     AI Explanation (NVIDIA Phi-4 Mini)
                    │
                    ▼
         JSON Response with Summary

🧩 Tech Stack
Component	Technology
Language	Python 3.10
Framework	FastAPI
AI Model	NVIDIA Phi-4 Mini (via OpenAI-compatible API)
OCR Engine	Tesseract OCR + Poppler for PDFs
Spell Correction	Regex + Fuzzy Matching
Containerization	Docker
Deployment	Render / Ngrok (for demo)
🚀 Key Features

✅ OCR + Spell Correction – Reads scanned and typed reports accurately
✅ Normalization – Cleans, validates, and structures extracted data
✅ AI Explanation – Converts data into easy-to-understand summaries
✅ Guardrails – Detects and blocks hallucinated test names
✅ Confidence Score – Evaluates OCR text reliability
✅ Dual Input Mode – Works with both file and text form inputs
✅ Dockerized – Fully portable and deployable on any cloud

🏗️ Project Structure
Backend/
│
├── app/
│   ├── api/
│   │   ├── upload.py          # Handles OCR & text upload routes
│   │   └── summary.py         # AI-based summarization logic
│   │
│   ├── services/
│   │   ├── ocr.py             # OCR extraction + confidence calculation
│   │   ├── spellCorrection.py # Cleans OCR typos using fuzzy logic
│   │   ├── Normalize.py       # AI normalization + hallucination guardrail
│   │   └── confidence.py      # Computes average OCR confidence
│   │
│   ├── main.py                # FastAPI app entry point
│   └── __init__.py
│
├── Dockerfile
├── requirements.txt
└── README.md

⚙️ Setup Instructions (Local Run)
🧩 1. Clone the Repository
git clone https://github.com/DEVANSH0507/AI-Powered-Medical-Report-Simplifier_Backend
cd AI-Powered-Medical-Report-Simplifier_Backend

🧩 2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # (Windows)
# or
source venv/bin/activate  # (Linux/Mac)

🧩 3. Install Dependencies
pip install -r requirements.txt

🧩 4. Run FastAPI Server
uvicorn app.main:app --reload

🧩 5. Access API Docs

👉 Open: http://127.0.0.1:8000/docs

🐳 Run with Docker
Step 1 — Build Image
docker build -t medical-report-api .

Step 2 — Run Container
docker run -d -p 8000:8000 medical-report-api

Step 3 — Open Docs

👉 http://localhost:8000/docs

🔍 API Endpoints
Endpoint	Method	Description
/upload/text	POST	Accepts text or image, extracts tests, and returns confidence
/upload/normalize	POST	Normalizes test names and units
/upload/api/analyze	POST	AI generates a patient-friendly summary
🧾 Example
Input:
CBC: Hemglobin 10.2 g/dL (Low)
WBC 11200 /uL (Hgh)

Output:
{
 "tests": [
  {"name":"Hemoglobin","value":10.2,"unit":"g/dL","status":"low","ref_range":{"low":12.0,"high":15.0}},
  {"name":"WBC","value":11200,"unit":"/uL","status":"high","ref_range":{"low":4000,"high":11000}}
 ],
 "summary": "Low hemoglobin and high white blood cell count.",
 "status": "ok"
}

🧠 Prompts Used for AI Normalization

“You are an AI medical text parser.
Extract test names, numeric values, units, and status.
Fix OCR errors (e.g., ‘Hemglobin’ → ‘Hemoglobin’).
Add reference ranges.
Output only valid JSON.
Provide a short, plain-language summary.”

🧩 State Management & Guardrails
Feature	Description
Validation Layer	Regex + Fuzzy Matching (via difflib)
Error Guardrail	Rejects hallucinated tests not found in input
OCR Confidence	Average word confidence (0.0–1.0)
Dual Input Handling	Chooses text or image dynamically
AI Consistency Check	Auto-corrects malformed JSON responses
🧩 Screenshots (Attach Below)
Screenshot	Description

	Example input medical report

	FastAPI Swagger UI

	Sample JSON AI output

(You can upload screenshots directly in GitHub)

⚠️ Known Issues

OCR may slightly misread noisy scans

Poppler path differs on Windows/Linux

AI summaries simplify medical terms intentionally

🚀 Future Improvements

Integrate MongoDB for report history

Add JWT Authentication

Build React Dashboard for visualization

Add custom range dataset for more test types

Enable cloud storage (S3/Render) for uploads

💬 Credits

🧑‍💻 Developed by: Devansh Gupta
🎯 AI-Powered Medical Report Simplifier – Problem Statement 7
📧 Contact: (optional)
