import pytesseract
from pdf2image import convert_from_path

pdf_path = "ilovepdf_merged.pdf"

# Convert PDF pages to images
images = convert_from_path(pdf_path)

# Extract text from each image using Tesseract OCR (Arabic)
text = ""
for i, img in enumerate(images):
    page_text = pytesseract.image_to_string(img, lang="ara")
    text += f"\n--- Page {i+1} ---\n" + page_text

# Save the extracted text to result.txt
with open("result.txt", "w", encoding="utf-8") as f:
    f.write(text)

# Print the first 2000 characters for preview
print(text[:2000])
