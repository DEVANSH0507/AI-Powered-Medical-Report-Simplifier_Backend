from app.services.spellCorrection import clean_ocr_text
from openai import OpenAI
import json, re, logging
import difflib

# open ai client call
client = OpenAI(
    api_key="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",
    base_url="https://integrate.api.nvidia.com/v1"
)


def normalize(input_text):
    # Defining prompt for AI
    prompt = (
        "You are an AI medical text parser.\n"
        "Your job is to analyze raw medical test text and return only valid JSON.\n"
        "Instructions:\n"
        "1. Extract each test with name, numeric value, unit, and status (Low/Normal/High).\n"
        "2. Normalize spellings and units.\n"
        "3. Correct any likely OCR or typing mistakes in test names or units. For example:\n"
        "   - 'Hemglobin' → 'Hemoglobin'\n"
        "   - 'Glocose' → 'Glucose'\n"
        "   - 'Cholestrol' → 'Cholesterol'\n"
        "   - 'Hgh' → 'High'\n"
        "4. Add reference range for common tests.\n"
        "5. Add a simple plain-language summary and short explanations.\n"
        "6. Do not add any extra commentary or text outside the JSON.\n"
        "7. Keep numeric values **exactly as in input** — do NOT scale (e.g., keep 11200, not 11.2).\n"
        "8. Output ONLY JSON. No prefixes, suffixes, or markdown.\n\n"
        "JSON format:\n"
        "{\n"
        " \"tests\": [\n"
        "   {\"name\": \"\", \"value\": 0, \"unit\": \"\", \"status\": \"\", \"ref_range\": {\"low\": 0, \"high\": 0}}\n"
        " ],\n"
        " \"summary\": \"\",\n"
        " \"explanations\": [],\n"
        " \"status\": \"ok\"\n"
        "}\n\n"
        f"Now process this input:\n{input_text}"
    )

    # calling ai
    response = client.chat.completions.create(
        model="microsoft/phi-4-mini-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=700,
    )

    ai_output = (response.choices[0].message.content or "").strip()

    # to repair invalid json response like if ai return some extra content
    try:
        result = json.loads(ai_output)
    except json.JSONDecodeError as e:
        logging.warning(f"AI JSON decode failed: {e} | Raw: {ai_output[:500]}")
        cleaned = re.sub(r"```(?:json)?|```", "", ai_output)
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                result = json.loads(match.group(0))
            except json.JSONDecodeError:
                result = {"status": "unprocessed", "reason": f"Invalid JSON after repair: {e}"}
        else:
            result = {"status": "unprocessed", "reason": f"Invalid JSON from AI: {e}"}
    
    # compare Ai result with input test to prevent hallucination
    # hence if test is noot in input return invalid tests
    raw_names = [t.lower() for t in re.findall(r"[A-Za-z]+", input_text)]

    for t in result.get("tests", []):
        if isinstance(t, dict) and "name" in t:
            ai_name = t["name"].lower()
           
            if ai_name not in raw_names and not difflib.get_close_matches(ai_name, raw_names, n=1, cutoff=0.75):
                return result
                result = {
                    "status": "unprocessed",
                    "reason": f"hallucinated test '{t['name']}' not found in input"
                }
                break

    return result
