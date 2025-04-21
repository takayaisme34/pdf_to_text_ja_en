from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from PIL import Image
import pytesseract
from tqdm import tqdm
import os

absPath = os.path.abspath(__file__)
parentDirectory = os.path.dirname(absPath)
TESSERACT_PATH = os.path.join(parentDirectory, "Tesseract-OCR/tesseract.exe")
POPPLER_PATH = os.path.join(parentDirectory, "poppler-23.01.0/Library/bin")

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def pypdf_pdf_to_text(pdfPath):
    reader = PdfReader(pdfPath)
    page = reader.pages
    fullText = ""
    for page in reader.pages:
        text = page.extract_text()
        fullText += " " + text
    return fullText

def ocr_pdf_to_text(pdfPath, language):
    reader = PdfReader(pdfPath)
    
    fullText = ""
    pageNumber = len(reader.pages)
    with tqdm(total=pageNumber, desc="extracting text...")as pbar:

        for page in reader.pages:
            tempPdfWriter = PdfWriter()
            tempPdfWriter.add_page(page)
            
            with BytesIO() as buffer:
                tempPdfWriter.write(buffer)
                pdfBytes = buffer.getvalue()

            images = convert_from_bytes(pdfBytes, poppler_path=POPPLER_PATH)
            for image in images:
                text = pytesseract.image_to_string(image, lang=language)
                fullText += f"{text}\n"

            pbar.update(1)
        
    return fullText

def pdf_to_text(pdfPath, lang="eng", ocr_default=False):
    fullText = pypdf_pdf_to_text(pdfPath)
    if len(fullText) < 500 or ocr_default:
        fullText = ocr_pdf_to_text(pdfPath, lang)
    return fullText

