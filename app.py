import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename

load_dotenv()  # Load environment variables from a .env file if present

from utils.pdf_utils import extract_text_from_pdf
from utils.summarizer import summarize_text
from utils.visualizer import generate_visual
from utils.doc_utils import save_markdown, save_docx

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOCS_FOLDER'] = 'docs'
app.config['IMAGE_FOLDER'] = 'static/images'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOCS_FOLDER'], exist_ok=True)
os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            return 'No file part', 400
        file = request.files['pdf']
        if file.filename == '':
            return 'No selected file', 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        text = extract_text_from_pdf(filepath)
        summary = summarize_text(text)

        base = os.path.splitext(filename)[0]
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        md_name = f"{base}_{timestamp}.md"
        docx_name = f"{base}_{timestamp}.docx"
        img_name = f"{base}_{timestamp}.png"

        md_path = os.path.join(app.config['DOCS_FOLDER'], md_name)
        docx_path = os.path.join(app.config['DOCS_FOLDER'], docx_name)
        save_markdown(summary, md_path)
        save_docx(summary, docx_path)

        image_path = os.path.join(app.config['IMAGE_FOLDER'], img_name)
        generate_visual(summary, image_path)

        return render_template(
            'result.html',
            summary=summary.split('\n'),
            image_url=url_for('static', filename=f'images/{img_name}'),
            md_file=md_name,
            docx_file=docx_name,
        )
    return render_template('upload.html')


@app.route('/docs/<path:filename>')
def download_file(filename: str):
    """Provide access to generated documents."""
    return send_from_directory(app.config['DOCS_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
