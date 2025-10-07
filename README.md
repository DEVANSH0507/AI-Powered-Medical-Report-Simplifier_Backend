🧠 AI-Powered Medical Report Simplifier (Backend)

Built by Devansh Gupta (Problem Statement 7 Submission)

📋 Overview

This backend project simplifies complex medical reports into easy-to-understand summaries for patients.
It uses OCR + AI-based text normalization + plain-language explanation, ensuring no hallucinated or fake medical data is generated.

The system can handle both typed and scanned medical reports (images or PDFs), extract test data accurately, normalize them, and provide a friendly explanation of the findings.

⚙️ Architecture
                ┌──────────────────────────┐
                │        Frontend UI       │
                │ (Future / Optional)      │
                └────────────┬─────────────┘
                             │  (HTTP POST)
                             ▼
               ┌───────────────────────────┐
               │     FastAPI Backend       │
               │───────────────────────────│
               │ /upload/text              │  →  Extracts tests (OCR/Text)
               │ /upload/normalize         │  →  Normalizes & validates data
               │ /upload/api/analyze       │  →  AI explanation & summary
               └────────────┬──────────────┘
                            │
           ┌────────────────┴────────────────┐
           │                                 │
┌────────────────────────┐     ┌────────────────────────┐
│  Tesseract OCR Engine  │     │ NVIDIA Phi-4 Mini LLM │
│ (Text/Image Extraction)│     │ (Medical Explanation)  │
└────────────────────────┘     └────────────────────────┘

🧩 Tech Stack
Component	Technology
Language	Python 3.10
Framework	FastAPI
AI Model	NVIDIA Phi-4 Mini (OpenAI-compatible API)
OCR Engine	Tesseract OCR + Poppler for PDFs
Spell Correction	Fuzzy Matching + Manual Mapping
Containerization	Docker
Deployment	Render / Ngrok (for local testing)
🚀 Key Features

📄 OCR + Spell Correction → Reads both scanned and typed medical reports.

🧮 Normalization → Standardizes test names, units, and reference ranges.

🧠 AI Explanation → Converts complex results into easy-to-understand summaries.

🧰 Guardrails → Detects hallucinated or non-existent tests using regex + fuzzy logic.

🔄 Flexible Input → Supports both text and image uploads.

⚡ Dockerized → Fully portable and cloud-deployable.

🏗️ Project Structure
Backend/
│
├── app/
│   ├── api/
│   │   ├── upload.py          # Handles OCR & text upload routes
│   │   └── summary.py         # AI analysis & summarization logic
│   │
│   ├── services/
│   │   ├── ocr.py             # Tesseract OCR + confidence calculation
│   │   ├── spellCorrection.py # Manual + fuzzy spelling correction
│   │   ├── Normalize.py       # AI normalization + hallucination guardrail
│   │   └── confidence.py      # Average OCR confidence calculator
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

🧩 5. Access the API

Open http://127.0.0.1:8000/docs

🐳 Run with Docker
Step 1 — Build the image
docker build -t medical-report-api .

Step 2 — Run the container
docker run -d -p 8000:8000 medical-report-api

Step 3 — Test it

Open: http://localhost:8000/docs

🔍 API Endpoints
Endpoint	Method	Description
/upload/text	POST	Accepts image or text. Extracts tests + returns confidence.
/upload/normalize	POST	Normalizes medical tests and units.
/upload/api/analyze	POST	AI generates a patient-friendly summary.
📡 Sample Input / Output
🧾 Input:
CBC: Hemglobin 10.2 g/dL (Low)
WBC 11200 /uL (Hgh)

🔍 Output:
{
 "tests": [
  {"name":"Hemoglobin","value":10.2,"unit":"g/dL","status":"low","ref_range":{"low":12.0,"high":15.0}},
  {"name":"WBC","value":11200,"unit":"/uL","status":"high","ref_range":{"low":4000,"high":11000}}
 ],
 "summary": "Low hemoglobin and high white blood cell count.",
 "status": "ok"
}

🧠 Prompts Used

The AI model was prompted with structured, rule-based instructions:

You are an AI medical text parser.
1. Extract tests with name, value, unit, status.
2. Normalize names and fix OCR spellings.
3. Add reference ranges.
4. Provide plain-language summary.
5. Output only valid JSON without commentary.


Refinements were made iteratively to handle OCR errors, misspellings, and numerical mismatches (e.g., 11,200 → 11200).

🧩 State Management Choices

Validation Layer → Regex + Fuzzy Matching (difflib)

Error Guardrail → Rejects hallucinated AI outputs not found in input

OCR Confidence Score → Averaged from Tesseract’s per-word data

Dual Input Mode → Chooses between text or image dynamically

🧩 Screenshots (Attach Below)

🖼️ You can drag & drop images here in GitHub after upload.

Screenshot	Description

	Example of input image report

	FastAPI Swagger interface

	Sample AI JSON response
⚠️ Known Issues

Minor OCR inaccuracies for very noisy scans.

Some AI-generated summaries may simplify complex test results.

Poppler path for PDF may differ on Windows & Docker.

🚀 Potential Improvements

Add database logging (MongoDB or PostgreSQL).

Integrate authentication (JWT).

Add frontend dashboard for visualization.

Improve test reference range dataset.

Add cloud storage for uploaded reports.

💬 Credits

Developed by Devansh Gupta
Under AI-Powered Medical Report Simplifier – Problem Statement 7
📧 Contact: [your email if you want to include]
