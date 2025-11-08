from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import os
import mimetypes
import json
from datetime import datetime
import socket

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
METADATA_FILE = os.path.join(UPLOAD_FOLDER, 'metadata.json')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load or initialize metadata
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)
else:
    metadata = {}


def save_metadata():
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)


def get_client_ip():
    # get IP from request
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.remote_addr
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        device_name = request.form.get('device_name', 'Unknown')
        client_ip = get_client_ip()
        if file and file.filename:
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(save_path)

            # Save metadata
            metadata[file.filename] = {
                "device_name": device_name,
                "ip": client_ip,
                "upload_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "size": os.path.getsize(save_path)
            }
            save_metadata()
            socketio.emit('new_file', {"filename": file.filename, "meta": metadata[file.filename]})
        return redirect(url_for('index'))

    files = sorted(metadata.items(), key=lambda x: x[1]['upload_time'], reverse=True)
    return render_template('index.html', files=files)


@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/preview/<path:filename>')
def preview(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype=mime_type)


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    client_ip = get_client_ip()
    # Only sender can delete
    if filename in metadata and metadata[filename]["ip"] == client_ip:
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, filename))
            metadata.pop(filename)
            save_metadata()
            socketio.emit('delete_file', {"filename": filename})
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    return jsonify({"success": False, "error": "Not allowed"})


@socketio.on('connect')
def connected():
    emit('connected', {'msg': 'Client connected'})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
