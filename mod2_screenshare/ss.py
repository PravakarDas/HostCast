import base64
import io
import time
from flask import Flask, render_template
from flask_socketio import SocketIO
from PIL import Image
import mss
import numpy as np

# Flask + SocketIO setup
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Optional: Target width for streaming (smaller = faster)
TARGET_WIDTH = 1600  # adjust to balance quality & speed

@app.route('/')
def index():
    return render_template("index.html")  # keep your templates/index.html

def stream_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # primary monitor
        while True:
            start = time.time()

            # Capture screen
            frame = sct.grab(monitor)
            # Convert BGRA -> RGB properly
            img_np = np.array(frame)
            img_np = img_np[:, :, :3][:, :, ::-1]  # BGRA -> RGB

            img = Image.fromarray(img_np)

            # Optional: resize for performance while keeping aspect ratio
            if TARGET_WIDTH and img.width > TARGET_WIDTH:
                ratio = TARGET_WIDTH / img.width
                target_height = int(img.height * ratio)
                img = img.resize((TARGET_WIDTH, target_height), Image.LANCZOS)

            # Encode JPEG
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=60, optimize=True)
            img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            # Emit to clients
            socketio.emit("frame", img_b64)

            # Maintain ~40 FPS
            elapsed = time.time() - start
            socketio.sleep(max(0.02 - elapsed, 0))

# Start streaming when first client connects
@socketio.on("connect")
def on_connect():
    print("Client connected")
    if not hasattr(socketio, "streaming_started"):
        socketio.start_background_task(stream_screen)
        socketio.streaming_started = True

@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected")

if __name__ == "__main__":
    print("⚡ Starting optimized low-latency screen share at http://localhost:5000")
    socketio.run(app, host="0.0.0.0", port=5000)
