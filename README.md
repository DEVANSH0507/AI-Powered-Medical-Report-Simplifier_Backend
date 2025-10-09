# 🧠 AI-Powered Medical Report Simplifier (Backend)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent **FastAPI-based backend** that extracts, cleans, and simplifies **medical reports** into easy-to-understand summaries for patients — powered by **OCR, Spell Correction, AI Normalization**, and **Hallucination Guardrails**.

Built with **Tesseract OCR**, **NVIDIA Phi-4 Mini LLM**, and **Python FastAPI**, it supports both **text and image inputs**, ensuring accurate structured medical data with factual, plain-language explanations.

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Core Goals](#-core-goals)
- [Sample Input & Output](#-sample-input--output)
- [Architecture](#-architecture)
- [Folder Structure](#-folder-structure)
- [State Management Choices](#-state-management-choices)
- [Setup Instructions](#-setup-instructions)
- [Run Locally](#-run-locally)
- [Docker Setup](#-docker-setup)
- [API Routes and Usage](#-api-routes-and-usage)
- [Example Workflow](#-example-workflow)
- [Prompts Used and Refinements](#-prompts-used-and-refinements)
- [Screenshots](#-screenshots)
- [Known Issues](#-known-issues)
- [Potential Improvements](#-potential-improvements)
- [Tech Stack](#-tech-stack)
- [Author](#-author)

---

## 🧠 Overview

The backend processes **medical test reports** (from text or scanned images) and converts them into **structured, human-readable summaries**.

### It ensures:
- ✅ Clean OCR extraction  
- ✅ Corrected test spellings  
- ✅ Standardized medical units  
- ✅ Realistic, medically factual AI explanations  
- ✅ No hallucinated or fake data in outputs  

---

## 💡 Core Goals

- Extract accurate test names and values from reports  
- Fix OCR typos contextually (`Hemglobin → Hemoglobin`)  
- Normalize numeric units and detect “High/Low” flags  
- Produce safe, validated JSON + readable summary text  

---

## 🧾 Sample Input & Output

**Input:**
CBC: Hemglobin 10.2 g/dL (Low), WBC 11200 /uL (Hgh)


**Output:**
```json
{
 "tests": [
  {"name":"Hemoglobin","value":10.2,"unit":"g/dL","status":"low","ref_range":{"low":12.0,"high":15.0}},
  {"name":"WBC","value":11200,"unit":"/uL","status":"high","ref_range":{"low":4000,"high":11000}}
 ],
 "summary": "Low hemoglobin and high white blood cell count.",
 "status": "ok"
}
  ```
## 🧱 Architecture

🧩 Processing Flow

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
Step 5: Final Structured JSON + AI Summary

## 📂 Folder Structure

<img width="755" height="441" alt="image" src="https://github.com/user-attachments/assets/0d061e81-9d49-48e3-864f-b9c190381a17" />

## ⚙️ Setup Instructions
🧩 Prerequisites

Python 3.10+

Tesseract OCR installed (Docker image includes it automatically)

NVIDIA API key (for Phi-4 Mini)

FastAPI & Uvicorn installed

## 🧩 Installation
```
' Clone the repository
git clone https://github.com/DEVANSH0507/AI-Powered-Medical-Report-Simplifier_Backend

' Navigate into the project directory
cd AI-Powered-Medical-Report-Simplifier_Backend

' Create a virtual environment
python -m venv venv

' Activate the virtual environment
' Windows:
venv\Scripts\activate
' Mac/Linux:
source venv/bin/activate

' Install project dependencies
pip install -r requirements.txt


## ▶️ Run Locally

uvicorn app.main:app --reload

Access Swagger UI: 👉 http://127.0.0.1:8000/docs


## 🐳 Docker Setup

Step 1 — Build Image: 
**docker build -t medical-simplifier-backend .**

Step 2 — Run Container:
**docker run -d -p 8000:8000 medical-simplifier-backend**


Access: 👉 http://localhost:8000/docs
```

##  🌐 API Routes and Usage

| Step | Endpoint              | Input Type   | Description                             |
| ---- | --------------------- | ------------ | --------------------------------------- |
| 1️⃣  | `/upload/text`        | Text / Image | Extracts medical tests + OCR confidence |
| 2️⃣  | `/upload/normalize`   | Text         | Normalizes and validates test data      |
| 3️⃣  | `/upload/api/analyze` | Text         | AI-generated patient summary            |


## 🧪 Example Workflow
🩺 Step 1 – OCR Extraction

POST /upload/text
```
{
  "tests_raw": ["Hemoglobin 10.2 g/dL (Low)", "WBC 11200 /uL (High)"],
  "confidence": 0.92
}
```

## ⚙️ Step 2 – Normalization

POST /upload/normalize
```
{
  "tests": [
    {"name": "Hemoglobin", "value": 10.2, "unit": "g/dL", "status": "low"},
    {"name": "WBC", "value": 11200, "unit": "/uL", "status": "high"}
  ]
}
```

## 💬 Step 3 – AI Analysis

POST /upload/api/analyze

```
{
  "summary": "Low hemoglobin and high white blood cell count.",
  "explanations": ["Hemoglobin indicates anemia", "WBC high suggests infection"],
  "status": "ok"
}
```
## 🧩 Prompts Used and Refinements
AI Normalization Prompt:

 “You are an AI medical text parser. Extract tests, normalize spellings, fix OCR mistakes, include ref ranges, and provide JSON + plain summary. Output only valid JSON.” 

 
## ✅ Refinements

Prevented hallucinations via fuzzy comparison

Enforced numeric preservation (11200 stays 11200)

Added guardrail for missing test names

Optimized token parsing for mixed-format reports
reports

## 📸 Screenshots


1.	/upload/text — Extract Tests

curl -X POST "http://localhost:8000/upload/text" \
  -F "text_input=CBC: Hemglobin 10.2 g/dL (Low), WBC 11200 /uL (Hgh)"

 <img width="616" height="262" alt="image" src="https://github.com/user-attachments/assets/99806ddc-b0a7-4529-bc05-85ea8dae69a6" />

2.	/upload/normalize — Normalize Tests

curl -X POST "http://localhost:8000/upload/normalize" \
  -F "text_input=Hemoglobin 10.2 g/dL (Low), WBC 11200 /uL (High)"


  <img width="604" height="480" alt="image" src="https://github.com/user-attachments/assets/0eaea31e-98ad-4d20-aba1-738cb083e4d1" />


3.	/upload/api/analyze — AI-Based Summary

<img width="940" height="450" alt="image" src="https://github.com/user-attachments/assets/dba0d4b3-ca64-434d-91c4-497fc982dcd7" />

## ⚠️ Known Issues

| Issue              | Description                        |
| ------------------ | ---------------------------------- |
| OCR on noisy scans | May drop symbols or units          |
| Poppler path       | Differs for Windows/Linux          |
| AI simplifications | May overly generalize some results |

## 🔮 Potential Improvements

🗃️ Add database (MongoDB/Postgres) for report history

🔐 JWT authentication for secure access

📚 Enhance medical reference datasets

☁️ Cloud file storage (AWS S3 / Render)

🖥️ Add frontend dashboard (React / Next.js)

## ⚙️ Tech Stack

| Component            | Technology                            |
| -------------------- | ------------------------------------- |
| **Backend**          | Python + FastAPI                      |
| **AI Model**         | NVIDIA Phi-4 Mini (OpenAI-compatible) |
| **OCR**              | Tesseract OCR + Poppler               |
| **Spell Correction** | Regex + Fuzzy Matching                |
| **Containerization** | Docker                                |
| **Deployment**       | Render / Ngrok                        |
| **Validation**       | difflib-based hallucination guardrail |

👨‍💻 Author

Devansh Gupta
Backend Developer | AI Systems & OCR Automation

📧 [Optional Email]
🧩 Project: AI-Powered Medical Report Simplifier – Problem Statement 7



 







