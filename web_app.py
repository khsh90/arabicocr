from flask import Flask, request, render_template_string, send_file, jsonify
import os
import time
from werkzeug.utils import secure_filename
from docx import Document
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img, lang='ara') + '\n'
    return text

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang='ara')
    return text

@app.route('/', methods=['GET'])
def index():
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>AI Arabic OCR</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
      <style>
        body { background: #181c24; color: #e0e6f6; }
        .container { max-width: 500px; margin-top: 60px; background: #23283a; border-radius: 18px; box-shadow: 0 0 24px #00ffe7a0; }
        .ai-title { font-size: 2.2rem; font-weight: 700; text-align: center; margin-bottom: 18px; letter-spacing: 1px; text-shadow: 0 0 8px #00ffe7; }
        .logo { display: block; margin: 0 auto 18px auto; max-width: 120px; filter: drop-shadow(0 0 8px #00ffe7); }
        label { color: #00ffe7; font-weight: 500; }
        .form-control, .btn { border-radius: 10px; }
        .btn-primary { background: linear-gradient(90deg, #00ffe7 0%, #007cf0 100%); border: none; color: #181c24; font-weight: 600; box-shadow: 0 0 8px #00ffe7a0; }
        .btn-primary:hover { background: linear-gradient(90deg, #007cf0 0%, #00ffe7 100%); color: #23283a; }
        #loading { display: none; }
        .spinner-border { color: #00ffe7; }
      </style>
    </head>
    <body>
      <div class="container p-4">
        <img src="/static/trismart logo.png" alt="Trismart Logo" class="logo">
        <div class="ai-title">AI Arabic OCR</div>
        <form id="uploadForm" enctype="multipart/form-data">
          <div class="mb-3">
            <label for="file" class="form-label">Choose PDF or Image</label>
            <input class="form-control" type="file" id="file" name="file" accept=".pdf,.png,.jpg,.jpeg" required>
          </div>
          <div class="mb-3">
            <label for="output_filename" class="form-label">Output Word filename</label>
            <input class="form-control" type="text" id="output_filename" name="output_filename" value="result" required>
          </div>
          <button type="submit" class="btn btn-primary w-100">Convert</button>
        </form>
        <div id="loading" class="text-center mt-4">
          <div class="spinner-border" role="status"></div>
          <div class="mt-2">Processing... <span id="timer">0</span> seconds</div>
        </div>
      </div>
      <script>
        const form = document.getElementById('uploadForm');
        const loading = document.getElementById('loading');
        const timerSpan = document.getElementById('timer');
        let timer = 0, interval;
        form.onsubmit = function(e) {
          e.preventDefault();
          loading.style.display = 'block';
          timer = 0;
          timerSpan.textContent = timer;
          interval = setInterval(() => { timer++; timerSpan.textContent = timer; }, 1000);
          const formData = new FormData(form);
          fetch('/convert', {
            method: 'POST',
            body: formData
          })
          .then(response => {
            if (!response.ok) throw new Error('Conversion failed');
            return response.blob();
          })
          .then(blob => {
            clearInterval(interval);
            loading.style.display = 'none';
            const outputName = document.getElementById('output_filename').value || 'result';
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = outputName + '.docx';
            link.click();
          })
          .catch(err => {
            clearInterval(interval);
            loading.style.display = 'none';
            alert('Error: ' + err.message);
          });
        };
      </script>
    </body>
    </html>
    ''')

@app.route('/convert', methods=['POST'])
def convert():
    start_time = time.time()
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    output_filename = request.form.get('output_filename', 'result')
    output_filename = output_filename.rsplit('.', 1)[0]  # Remove any extension
    output_filename += '.docx'
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        ext = filename.rsplit('.', 1)[1].lower()
        if ext == 'pdf':
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_image(file_path)
        doc = Document()
        doc.add_paragraph(text)
        temp_docx_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        doc.save(temp_docx_path)
        elapsed = time.time() - start_time
        print(f"Conversion took {elapsed:.2f} seconds.")
        return send_file(temp_docx_path, as_attachment=True, download_name=output_filename)
    else:
        return 'Invalid file type.', 400

if __name__ == '__main__':
    app.run(debug=True)
