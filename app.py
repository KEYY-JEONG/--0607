import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
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
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        text = extract_text_from_pdf(filepath)
        summary = summarize_text(text)

        md_path = os.path.join(app.config['DOCS_FOLDER'], 'summary.md')
        docx_path = os.path.join(app.config['DOCS_FOLDER'], 'summary.docx')
        save_markdown(summary, md_path)
        save_docx(summary, docx_path)

        image_path = os.path.join(app.config['IMAGE_FOLDER'], 'visual.png')
        generate_visual(summary, image_path)

        return render_template('result.html', summary=summary.split('\n'), image_url=url_for('static', filename='images/visual.png'))
    return render_template('upload.html')


@app.route('/docs/<path:filename>')
def download_file(filename: str):
    """Provide access to generated documents."""
    return send_from_directory(app.config['DOCS_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
