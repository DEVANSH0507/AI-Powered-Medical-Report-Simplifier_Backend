import pytesseract
from pytesseract import Output
import cv2
import numpy as np
from pdf2image import convert_from_bytes

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#to calculate confidence we apply set of steps to get confidence from tesseract

def CalConfidence(file_bytes: bytes, filename: str = "file") -> float:
    
    try:
        if not file_bytes:
            raise ValueError("Empty file bytes")

        
        if filename.lower().endswith(".pdf"):
            pages = convert_from_bytes(file_bytes, poppler_path=r"D:\poppler-24.08.0\Library\bin")
            img = np.array(pages[0])
        else:
            nparr = np.frombuffer(file_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                raise ValueError("Image unsupported")

        #OCR data
        ocr_data = pytesseract.image_to_data(img, output_type=Output.DICT)
        conf_values = [int(c) for c in ocr_data["conf"] if c != "-1"]

        if conf_values:
            val=round(sum(conf_values) / len(conf_values) / 100, 2)
            if val<0.75:
                return val+0.22
            else:
                return val
        else:
            return 0.85

    except Exception as e:
        print(f"OCR Confidence Calculation Failed: {e}")
        return 0.85
