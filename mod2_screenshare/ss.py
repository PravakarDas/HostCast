import base64
import io
import time
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO
from PIL import Image
import mss
import numpy as np
import pyaudiowpatch as pyaudio

# Flask + SocketIO setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hostcast-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Optional: Target width for streaming (smaller = faster)
TARGET_WIDTH = 1600  # adjust to balance quality & speed

# Audio settings
CHUNK = 1024  # Audio chunk size
FORMAT = pyaudio.paInt16
CHANNELS = 2  # Stereo
RATE = 44100  # Sample rate

# Global flags and tracking
is_streaming = False
streaming_lock = threading.Lock()
connected_clients = set()
audio_stream = None
p = None

@app.route('/')
def index():
    return render_template("index.html")  # keep your templates/index.html

def get_default_wasapi_loopback():
    """Get the default WASAPI loopback device for capturing system audio on Windows"""
    try:
        global p
        p = pyaudio.PyAudio()
        
        # Get default WASAPI info
        wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        
        if not default_speakers["isLoopbackDevice"]:
            for loopback in p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break
        
        return default_speakers
    except Exception as e:
        print(f"Error getting WASAPI loopback device: {e}")
        return None

def stream_audio():
    """Capture and stream system audio to all connected clients"""
    global audio_stream, is_streaming, p
    
    print("🔊 Audio streaming thread started")
    
    try:
        default_speakers = get_default_wasapi_loopback()
        if not default_speakers:
            print("⚠️  Could not find WASAPI loopback device. Audio streaming disabled.")
            return
        
        print(f"🎵 Streaming audio from: {default_speakers['name']}")
        
        # Open audio stream
        audio_stream = p.open(
            format=FORMAT,
            channels=default_speakers["maxInputChannels"],
            rate=int(default_speakers["defaultSampleRate"]),
            frames_per_buffer=CHUNK,
            input=True,
            input_device_index=default_speakers["index"]
        )
        
        while is_streaming:
            try:
                # Read audio data
                audio_data = audio_stream.read(CHUNK, exception_on_overflow=False)
                # Encode as base64
                audio_b64 = base64.b64encode(audio_data).decode('utf-8')
                # Broadcast to ALL clients (no broadcast parameter needed)
                socketio.emit("audio", {
                    "data": audio_b64,
                    "rate": int(default_speakers["defaultSampleRate"]),
                    "channels": default_speakers["maxInputChannels"]
                }, namespace='/')
            except Exception as e:
                print(f"Error reading audio: {e}")
                socketio.sleep(0.01)
                
    except Exception as e:
        print(f"⚠️  Audio streaming error: {e}")
    finally:
        if audio_stream:
            audio_stream.stop_stream()
            audio_stream.close()
        if p:
            p.terminate()
    
    print("🔊 Audio streaming thread stopped")

def stream_screen():
    """Continuously capture and broadcast screen to all connected clients"""
    global is_streaming
    
    print("🎥 Screen streaming thread started")
    frame_count = 0
    
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # primary monitor
        print(f"   Monitor size: {monitor['width']}x{monitor['height']}")
        
        while is_streaming:
            try:
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

                # Broadcast to ALL clients (no broadcast parameter needed)
                socketio.emit("frame", img_b64, namespace='/')
                
                frame_count += 1
                if frame_count % 100 == 0:
                    print(f"   📺 Sent {frame_count} frames to {len(connected_clients)} client(s)")

                # Maintain ~40 FPS
                elapsed = time.time() - start
                socketio.sleep(max(0.025 - elapsed, 0))
                
            except Exception as e:
                print(f"❌ Error in screen capture: {e}")
                import traceback
                traceback.print_exc()
                socketio.sleep(0.1)
    
    print("🎥 Screen streaming thread stopped")

# Start streaming when first client connects
@socketio.on("connect")
def on_connect():
    global is_streaming, connected_clients
    
    from flask import request
    client_id = request.sid
    connected_clients.add(client_id)
    
    print(f"✅ Client connected (SID: {client_id}) - Total clients: {len(connected_clients)}")
    print(f"   Current streaming status: {is_streaming}")
    
    with streaming_lock:
        if not is_streaming:
            print("🎬 Starting streaming threads...")
            is_streaming = True
            try:
                # Start screen streaming
                socketio.start_background_task(stream_screen)
                print("   ✓ Screen thread started")
                # Start audio streaming
                socketio.start_background_task(stream_audio)
                print("   ✓ Audio thread started")
                print("✅ Streaming started for first client")
            except Exception as e:
                print(f"❌ Error starting streaming: {e}")
                is_streaming = False
        else:
            print("📡 New client joined existing stream")

@socketio.on("disconnect")
def on_disconnect():
    global is_streaming, connected_clients
    
    from flask import request
    client_id = request.sid
    connected_clients.discard(client_id)
    
    print(f"❌ Client disconnected (SID: {client_id}) - Remaining clients: {len(connected_clients)}")
    
    # Optional: Stop streaming if no clients (uncomment if desired)
    # with streaming_lock:
    #     if len(connected_clients) == 0:
    #         is_streaming = False
    #         print("⏹️  All clients disconnected - streaming stopped")

if __name__ == "__main__":
    print("=" * 60)
    print("⚡ HostCast Screen + Audio Share Server")
    print("=" * 60)
    print("🎥 Video streaming: ENABLED")
    print("🔊 Audio streaming: ENABLED (Windows WASAPI)")
    print("👥 Multi-client: ENABLED")
    print("=" * 60)
    print("🌐 Server starting at http://0.0.0.0:5000")
    print("📱 Clients can connect from any device on the network")
    print("=" * 60)
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
