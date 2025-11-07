from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pyautogui
import io
import base64

app = Flask(__name__, static_folder='static', template_folder='templates')
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('request_screenshot')
def handle_request_screenshot():
    screenshot = pyautogui.screenshot()
    buffer = io.BytesIO()
    screenshot.save(buffer, format="JPEG", quality=90)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    emit('screenshot', {'image': img_str})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
