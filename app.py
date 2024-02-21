from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from pdf2docx import Converter

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})

    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})

    if file and file.filename.lower().endswith('.pdf'):
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Perform the PDF to Word conversion
            word_file = os.path.splitext(file.filename)[0] + '.docx'
            word_path = os.path.join(app.config['UPLOAD_FOLDER'], word_file)

            cv = Converter(file_path)
            cv.convert(word_path, start=0, end=None)
            cv.close()

            return jsonify({'success': True, 'url': f'/uploads/{word_file}'})

        except Exception as e:
            return jsonify({'success': False, 'message': f'Error during conversion: {str(e)}'})

    return jsonify({'success': False, 'message': 'Invalid file format'})

@app.route('/uploads/<filename>')
def download_word_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)