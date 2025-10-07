from fastapi import APIRouter, Form
from app.services.spellCorrection import clean_ocr_text
from app.services.Normalize import normalize
from fastapi.responses import JSONResponse
import json, re, logging

router = APIRouter()

def analyze(result):
    #to change result acc to required format
    try:
        final_output = {
            "tests": [],
            "summary": result.get("summary", ""),
            "status": result.get("status", "ok")
        }

    # Lets take all parameter from ai response
    #convert acc to json

        if "tests" in result:
            for test in result["tests"]:
                if isinstance(test, dict):
                    fixed = {
                        "name": test.get("name", "").strip(),
                        "value": test.get("value"),
                        "unit": (
                            "/" + test["unit"].replace("/", "").strip()
                            if test.get("unit") and not test["unit"].startswith("/")
                            else test.get("unit", "")
                        ),
                        "status": test.get("status", "").lower(),
                        "ref_range": test.get("ref_range", {})
                    }
                    final_output["tests"].append(fixed)

        return JSONResponse(content=final_output)

    except Exception as e:
        logging.error(f"Error in /api/analyze: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
