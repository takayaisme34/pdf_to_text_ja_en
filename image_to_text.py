from PIL import Image
import pytesseract

# Specify the path to the Tesseract executable (replace with your path)
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Open the image using PIL
image_path = f"./photos/image_1.png"
image = Image.open(image_path)

# Use pytesseract to extract text from the image
text = pytesseract.image_to_string(image)

# Print the extracted text
print("Extracted Text:")
print(text)
