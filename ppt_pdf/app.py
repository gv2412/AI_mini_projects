from flask import Flask, request, send_file, render_template, flash
from file_converter import FileConverter
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = 'your-secret-key-here'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'.pptx', '.ppt', '.docx', '.doc', '.xlsx', '.xls'}

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        flash('No file uploaded')
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return 'No file selected', 400
    
    if not allowed_file(file.filename):
        flash('Invalid file type')
        return 'Invalid file type', 400
    
    try:
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        converter = FileConverter()
        pdf_path = converter.convert_to_pdf(input_path)
        
        if pdf_path.startswith('Error'):
            flash('Conversion failed')
            return pdf_path, 500
        
        return send_file(pdf_path, 
                        as_attachment=True,
                        download_name=os.path.basename(pdf_path))
    
    except Exception as e:
        flash(f'Error: {str(e)}')
        return f'Error: {str(e)}', 500
    
    finally:
        # Clean up uploaded files
        if os.path.exists(input_path):
            try:
                os.remove(input_path)
            except:
                pass

if __name__ == '__main__':
    app.run(debug=True)