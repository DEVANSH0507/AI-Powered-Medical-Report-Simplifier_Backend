import re, difflib

#To correct spell we make dictionary for map then correct near text
#manually check each word and try to correct 

def clean_ocr_text(raw_text: str):
   
    # dictionary
    direct_map = {
        "Hemglobin": "Hemoglobin",
        "Hemgoblin": "Hemoglobin",
        "Hgh": "High",
        "Lo": "Low",
        "Nomal": "Normal",
        "Glocose": "Glucose",
        "Cholestrol": "Cholesterol"
    }

    for wrong, right in direct_map.items():
        raw_text = re.sub(rf"\b{wrong}\b", right, raw_text, flags=re.IGNORECASE)

    # Known Matches
    known_terms = [
        "Hemoglobin", "WBC", "RBC", "Platelets", "Glucose",
        "Cholesterol", "Triglycerides", "Urea", "Creatinine"
    ]

    words = raw_text.split()
    corrected_words = []

    for w in words:
        match = difflib.get_close_matches(w, known_terms, n=1, cutoff=0.80)
        if match:
            corrected_words.append(match[0])
        else:
            corrected_words.append(w)

    corrected_text = " ".join(corrected_words)
    return corrected_text