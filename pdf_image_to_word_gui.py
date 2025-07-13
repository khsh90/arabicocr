import tkinter as tk
from tkinter import filedialog, messagebox
from docx import Document
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

# Helper function to extract text from PDF or image

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == ".pdf":
        images = convert_from_path(file_path)
        for i, img in enumerate(images):
            page_text = pytesseract.image_to_string(img, lang="ara")
            text += f"\n--- Page {i+1} ---\n" + page_text
    elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img, lang="ara")
    else:
        raise ValueError("Unsupported file type.")
    return text

# GUI Application

def run_app():
    def select_file():
        file_path = filedialog.askopenfilename(
            title="Select PDF or Image",
            filetypes=[("PDF and Images", "*.pdf *.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

    def select_output():
        file_path = filedialog.asksaveasfilename(
            title="Save Word File As",
            defaultextension=".docx",
            filetypes=[("Word Document", "*.docx")]
        )
        entry_output.delete(0, tk.END)
        entry_output.insert(0, file_path)

    def process():
        input_path = entry_file.get()
        output_path = entry_output.get()
        if not input_path or not output_path:
            messagebox.showerror("Error", "Please select both input and output files.")
            return
        try:
            text = extract_text(input_path)
            doc = Document()
            doc.add_paragraph(text)
            doc.save(output_path)
            messagebox.showinfo("Success", f"Text extracted and saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("PDF/Image to Word (Arabic OCR)")
    root.geometry("500x200")

    tk.Label(root, text="Select PDF or Image file:").pack(pady=5)
    entry_file = tk.Entry(root, width=50)
    entry_file.pack()
    tk.Button(root, text="Browse", command=select_file).pack(pady=2)

    tk.Label(root, text="Select output Word file:").pack(pady=5)
    entry_output = tk.Entry(root, width=50)
    entry_output.pack()
    tk.Button(root, text="Browse", command=select_output).pack(pady=2)

    tk.Button(root, text="Convert and Save", command=process, bg="#4CAF50", fg="white").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_app()
