import sys
from docx import Document

# Usage: python txt_to_docx.py input.txt output.docx
def main():
    if len(sys.argv) != 3:
        print("Usage: python txt_to_docx.py <input_txt_file> <output_docx_file>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{input_path}': {e}")
        sys.exit(1)
    try:
        doc = Document()
        doc.add_paragraph(text)
        doc.save(output_path)
        print(f"Text has been saved to {output_path}")
    except Exception as e:
        print(f"Error writing '{output_path}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
