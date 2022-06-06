from PIL import Image

import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

print(pytesseract.image_to_string(Image.open('capture_csv.png'), lang='fra'))