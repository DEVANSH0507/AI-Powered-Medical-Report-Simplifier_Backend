from fastapi import APIRouter, UploadFile, File, Form,HTTPException
from app.services.spellCorrection import clean_ocr_text
from app.services.confidence import CalConfidence
from app.api.summary import analyze
from app.services.Normalize import normalize
from typing import Optional
from PIL import Image
import pytesseract
import io
import re

router = APIRouter()

# Reusable function to extract Text and confidence from image

async def extract(file: UploadFile):
    
    #read the file
    contents = await file.read()

    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # call confidence func to get it from services
    confidence = CalConfidence(contents)

    try:
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail="failed on extract")

    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found")

    return text.strip(), confidence




@router.post("/text",
            description="When sending only text input ensure in file  UNTICK send empty value")
async def process_text(
    text_input: str = Form(None),
    file: UploadFile = File(None),
    ):
    
    #invalid input 
    if not text_input and not file:
        raise HTTPException(status_code=400, detail="No input")

    # file provided
    if file and not text_input:
        input_text, confidence = await extract(file)

    # text provided
    else:
        input_text = text_input.strip()
        confidence = 0.95  

 
    cleaned_text = clean_ocr_text(input_text)
    cleaned_text = re.sub(r'(?<=\d),(?=\d{3}\b)', '', cleaned_text)
    #To seprate according to new lines
    cleaned_text = re.sub(r'[;]+', '\n', cleaned_text)
    cleaned_text = re.sub(r'[\r\t ]*\n[\r\t ]*', '\n', cleaned_text).strip()
    # split on comma
    tests = [line.strip() for line in cleaned_text.split("\n") if line.strip()]

    return {
        "tests_raw": tests,
        "confidence": confidence
    }


@router.post("/normalize",
            description="When sending only text input ensure in file input UNTICK send empty value")
async def process_normalize(    
    text_input: str = Form(None),
    file: UploadFile = File(None)):

    # check for no input
    if not text_input and not file:
        raise HTTPException(status_code=400, detail="invalid input")

    #when file given
    if file and not text_input:
       text_input, confidence = await extract(file)

    # text given
    else:
        text_input = text_input.strip()
        confidence = 0.95 
    
    #spell check then normalize
    text_input=clean_ocr_text(text_input)
    data=normalize(text_input)
    tests = data.get("tests", [])

    return {
        "tests_raw": tests,
        "confidence": confidence
    }

@router.post("/api/analyze",
             description="When sending only text input ensure in file input  UNTICK send empty input")
async def analyze_medical_text(
    text_input: str = Form(None),
    file: UploadFile = File(None)):
    

    # no input
    if not text_input and not file:
        raise HTTPException(status_code=400, detail="invalid input")

    # file given
    if file and not text_input:
        input_text, confidence = await extract(file)

    # text given
    else:
        input_text = text_input.strip()
        confidence = 0.95 

      #spell correct then normalize then analyze  
    input_text = clean_ocr_text(input_text)
    result = normalize(input_text)
    data=analyze(result)
    return data




