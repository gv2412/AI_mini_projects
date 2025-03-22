from flask import Flask, render_template, request, send_file, url_for
import qrcode
import os
import base64
from io import BytesIO
import socket

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    # Save the file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Generate QR code with download link using local IP
    local_ip = get_local_ip()
    download_url = f"http://{local_ip}:5000{url_for('download_file', filename=file.filename)}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(download_url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Convert QR code to base64 for displaying in HTML
    buffered = BytesIO()
    qr_image.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return render_template('result.html', qr_code=qr_base64, filename=file.filename)

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)