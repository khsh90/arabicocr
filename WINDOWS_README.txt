# Windows Build & Run Instructions for PDF/Image to Word (Arabic OCR) App

## 1. Install Python (3.10 or 3.11 recommended)
- Download from https://www.python.org/downloads/windows/
- Add Python to PATH during installation.

## 2. Install Tesseract OCR for Windows
- Download from https://github.com/tesseract-ocr/tesseract
- Install and add the Tesseract install directory (e.g., `C:\Program Files\Tesseract-OCR`) to your PATH.
- Make sure to select Arabic language data during installation, or download `ara.traineddata` and place it in the `tessdata` folder.

## 3. Install Poppler for Windows
- Download from http://blog.alivate.com.au/poppler-windows/
- Extract and add the `bin` folder to your PATH.

## 4. Install Python dependencies
Open Command Prompt in your project directory and run:
```
pip install -r requirements.txt
```

## 5. Build the .exe
```
pyinstaller --onefile --noconsole pdf_image_to_word_gui.py
```
- The `.exe` will be in the `dist` folder.

## 6. Run the App
- Double-click the `.exe` in `dist` or run from Command Prompt.

## Notes
- The app supports PDF and image files as input.
- Output is a Word file (`.docx`) with extracted Arabic text.
- Tesseract and Poppler must be in PATH for the app to work.
