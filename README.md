🧠 AI-Powered Medical Report Simplifier (Backend)

An intelligent FastAPI-based backend that extracts, cleans, and simplifies medical reports into easy-to-understand summaries for patients — using OCR, Spell Correction, AI Normalization, and Hallucination Guardrails.

Built using Tesseract OCR, NVIDIA Phi-4 Mini LLM, and Python FastAPI, it supports both text and image inputs, ensuring accurate structured medical data with plain-language explanations.

📖 Table of Contents

Overview

Prompts Used and Refinements

Architecture

State Management Choices

Setup Instructions

API Routes and Usage

Example Workflow

Screenshots

Known Issues

Potential Improvements

Tech Stack

Author

🧠 Overview

The backend intelligently processes medical test reports (text or images) and converts them into structured, human-readable summaries.

It ensures:

Clean OCR extraction

Corrected test spellings

Standardized medical units

Realistic AI explanations

No hallucinated (fake) data in outputs

💡 Core Goals

Extract accurate tests and values from real medical reports

Fix OCR typos contextually (Hemglobin → Hemoglobin)

Normalize numeric units and detect “High/Low” flags

Produce safe, factual JSON + summary text

🧾 Sample Input & Output
Input:
CBC: Hemglobin 10.2 g/dL (Low), WBC 11200 /uL (Hgh)

Output:
{
 "tests": [
  {"name":"Hemoglobin","value":10.2,"unit":"g/dL","status":"low","ref_range":{"low":12.0,"high":15.0}},
  {"name":"WBC","value":11200,"unit":"/uL","status":"high","ref_range":{"low":4000,"high":11000}}
 ],
 "summary": "Low hemoglobin and high white blood cell count.",
 "status": "ok"
}

🧱 Architecture
🧩 Flow
Input (Text or Image)
        ↓
Step 1: OCR Extraction (Tesseract)
        ↓
Step 2: Spell Correction (Custom Dictionary + Fuzzy Match)
        ↓
Step 3: AI Normalization (Phi-4 Mini)
        ↓
Step 4: Hallucination Guardrails (Regex + difflib)
        ↓
Step 5: Final Structured JSON + Summary

📂 Folder Structure
app/
├── api/
│   ├── upload.py          # Handles OCR + text routes
│   └── summary.py         # AI summarization logic
│
├── services/
│   ├── ocr.py             # OCR extraction + confidence
│   ├── spellCorrection.py # Fuzzy spell correction
│   ├── Normalize.py       # AI normalization & validation
│   ├── confidence.py      # Average OCR confidence
│
├── main.py                # FastAPI entry point
├── Dockerfile
└── requirements.txt

🧩 State Management Choices

Even though FastAPI is stateless, each step logically maintains “state” between transformations.

Component	Responsibility
ocr.py	Extracts text + calculates confidence
spellCorrection.py	Fixes OCR misspellings
Normalize.py	Normalizes and validates tests
summary.py	Generates plain-language AI explanations
confidence.py	Scores OCR accuracy
⚙️ Setup Instructions
🧩 Prerequisites

Python 3.10+

Tesseract OCR installed (Docker handles this automatically)

NVIDIA API key (for Phi-4 Mini)

FastAPI & Uvicorn installed

🧩 Installation
git clone https://github.com/DEVANSH0507/AI-Powered-Medical-Report-Simplifier_Backend
cd AI-Powered-Medical-Report-Simplifier_Backend

python -m venv venv
venv\Scripts\activate     # Windows
# or
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt

🧩 Run Locally
uvicorn app.main:app --reload


Access: 👉 http://127.0.0.1:8000/docs

🐳 Docker Setup
Step 1 — Build Image
docker build -t medical-simplifier-backend .

Step 2 — Run Container
docker run -d -p 8000:8000 medical-simplifier-backend


Access: 👉 http://localhost:8000/docs

🌐 API Routes and Usage
Step	Endpoint	Input Type	Description
1️⃣	/upload/text	Text / Image	Extracts medical tests + confidence
2️⃣	/upload/normalize	Text	Normalizes and validates test data
3️⃣	/upload/api/analyze	Text	AI-generated patient summary
🧪 Example Workflow
Step 1 – OCR Extraction

POST /upload/text

{
  "tests_raw": ["Hemoglobin 10.2 g/dL (Low)", "WBC 11200 /uL (High)"],
  "confidence": 0.92
}

Step 2 – Normalization

POST /upload/normalize

{
  "tests": [
    {"name": "Hemoglobin", "value": 10.2, "unit": "g/dL", "status": "low"},
    {"name": "WBC", "value": 11200, "unit": "/uL", "status": "high"}
  ]
}

Step 3 – AI Analysis

POST /upload/api/analyze

{
  "summary": "Low hemoglobin and high white blood cell count.",
  "explanations": ["Hemoglobin indicates anemia", "WBC high suggests infection"],
  "status": "ok"
}

🧩 Prompts Used and Refinements

Prompt (AI Normalization Layer):
"You are an AI medical text parser. Extract tests, normalize spellings, fix OCR mistakes, include ref ranges, and provide JSON + plain summary. Output only valid JSON."

✅ Refinements made:

Prevented hallucinations via fuzzy comparison

Forced numeric preservation (11200 stays as 11200)

Added guardrail for missing test names

Optimized token parsing for mixed-format reports

📸 Screenshots
Screenshot	Description

	Example input report

	FastAPI Swagger interface

	Normalized JSON output

	AI summary example
⚠️ Known Issues
Issue	Description
OCR on noisy scans	May drop symbols or units
Poppler path	Differs for Windows/Linux
AI simplifications	May overly generalize results
🔮 Potential Improvements

Add database (MongoDB/Postgres) for history

JWT authentication for secure access

Enhanced test reference datasets

Cloud file storage (AWS S3 / Render)

Add frontend dashboard (React or Next.js)

⚙️ Tech Stack
Component	Technology
Backend	Python + FastAPI
AI Model	NVIDIA Phi-4 Mini (OpenAI-compatible)
OCR	Tesseract OCR + Poppler
Spell Correction	Regex + Fuzzy Matching
Containerization	Docker
Deployment	Render / Ngrok
Validation	difflib-based hallucination guardrail
👨‍💻 Author

Devansh Gupta
Backend Developer | AI Systems & OCR Automation
📧 [Optional Email]
🧩 Project: AI-Powered Medical Report Simplifier – Problem Statement 7
