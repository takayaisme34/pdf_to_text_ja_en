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


class PdfTextExtraction:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.reader = PdfReader(pdf_path)

    def pypdf_text_extraction(self):
        full_text = ""
        for page in self.reader.pages:
            page_text = page.extract_text()
            full_text += page_text
        return full_text
    
    def ocr_text_extraction(self, language):
        fullText = ""
        pageNumber = len(self.reader.pages)
        with tqdm(total=pageNumber, desc="extracting text...")as pbar:

            for page in self.reader.pages:
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

    def pdf_to_text(self, lang="eng", ocr_default=False):
        full_text = self.pypdf_text_extraction()
        if len(full_text) < 500 or ocr_default or self.reader.is_encrypted:
            if self.reader.is_encrypted:
                print("encrypted pdf!")
            full_text = self.ocr_text_extraction(lang)
        return full_text


