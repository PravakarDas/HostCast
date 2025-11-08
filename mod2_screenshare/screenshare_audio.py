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
socketio = SocketIO(
    app, 
    cors_allowed_origins="*", 
    async_mode="threading",
    ping_timeout=60,
    ping_interval=25,
    max_http_buffer_size=10**8,
    logger=True,
    engineio_logger=True
)

# Configuration
TARGET_WIDTH = 1280
AUDIO_CHUNK = 2048  # Larger chunks = more stable
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_RATE = 48000  # Match your system's native rate

# Global flags
is_streaming = False
audio_lock = threading.Lock()
connected_clients = 0

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/test')
def test():
    return render_template("test.html")

def get_loopback_device(p):
    """Get the WASAPI loopback device for system audio capture"""
    try:
        wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        
        if not default_speakers["isLoopbackDevice"]:
            for loopback in p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    print(f"🎤 Found loopback: {loopback['name']}")
                    return loopback
        return default_speakers
    except Exception as e:
        print(f"❌ Error getting loopback device: {e}")
        return None

def capture_audio():
    """Capture system audio using WASAPI loopback - Non-blocking"""
    global is_streaming
    p = pyaudio.PyAudio()
    stream = None
    
    try:
        loopback = get_loopback_device(p)
        if not loopback:
            print("❌ No loopback device found!")
            return
        
        # Use system's native sample rate
        rate = int(loopback["defaultSampleRate"])
        channels = int(loopback["maxInputChannels"])
        
        print(f"🎵 Audio config: {rate}Hz, {channels}ch, chunk={AUDIO_CHUNK}")
        
        # Open audio stream with error handling
        stream = p.open(
            format=AUDIO_FORMAT,
            channels=channels,
            rate=rate,
            input=True,
            input_device_index=loopback["index"],
            frames_per_buffer=AUDIO_CHUNK,
            stream_callback=None  # Use blocking mode for stability
        )
        
        stream.start_stream()
        print("✅ Audio capture started")
        
        consecutive_errors = 0
        max_errors = 10
        
        while is_streaming and consecutive_errors < max_errors:
            try:
                # Non-blocking read with timeout
                if stream.is_active():
                    data = stream.read(AUDIO_CHUNK, exception_on_overflow=False)
                    
                    # Only encode and send if we have data
                    if data and len(data) > 0:
                        audio_b64 = base64.b64encode(data).decode('utf-8')
                        
                        # Emit in a thread-safe way
                        with audio_lock:
                            socketio.emit("audio", {
                                "data": audio_b64,
                                "rate": rate,
                                "channels": channels
                            }, namespace='/')
                        
                        consecutive_errors = 0  # Reset on success
                    
                    # Small sleep to prevent CPU spinning
                    time.sleep(0.001)
                else:
                    print("⚠️ Audio stream not active")
                    break
                    
            except IOError as e:
                consecutive_errors += 1
                print(f"⚠️ Audio IO error ({consecutive_errors}/{max_errors}): {e}")
                time.sleep(0.01)
            except Exception as e:
                consecutive_errors += 1
                print(f"⚠️ Audio error ({consecutive_errors}/{max_errors}): {e}")
                time.sleep(0.01)
                
    except Exception as e:
        print(f"❌ Audio initialization error: {e}")
    finally:
        print("🛑 Stopping audio capture...")
        if stream:
            try:
                stream.stop_stream()
                stream.close()
            except:
                pass
        p.terminate()
        print("✅ Audio capture stopped")

def stream_screen():
    """Capture and stream screen - Non-blocking"""
    global is_streaming
    
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            print(f"📺 Screen capture started: {monitor['width']}x{monitor['height']}")
            
            frame_count = 0
            fps_time = time.time()
            target_frame_time = 1.0 / 30  # 30 FPS target
            
            while is_streaming:
                frame_start = time.time()
                
                try:
                    # Capture screen
                    frame = sct.grab(monitor)
                    img_np = np.array(frame)
                    img_np = img_np[:, :, :3][:, :, ::-1]  # BGRA -> RGB
                    
                    img = Image.fromarray(img_np)
                    
                    # Resize if needed
                    if TARGET_WIDTH and img.width > TARGET_WIDTH:
                        ratio = TARGET_WIDTH / img.width
                        target_height = int(img.height * ratio)
                        img = img.resize((TARGET_WIDTH, target_height), Image.LANCZOS)
                    
                    # Encode JPEG
                    buffer = io.BytesIO()
                    img.save(buffer, format="JPEG", quality=70, optimize=True)
                    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                    
                    # Emit to clients
                    socketio.emit("frame", img_b64, namespace='/')
                    
                    frame_count += 1
                    
                    # FPS counter every 5 seconds
                    if frame_count % 150 == 0:
                        elapsed = time.time() - fps_time
                        fps = 150 / elapsed
                        print(f"📊 Screen FPS: {fps:.1f}")
                        fps_time = time.time()
                    
                    # Frame timing
                    elapsed = time.time() - frame_start
                    sleep_time = max(0, target_frame_time - elapsed)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                    
                except Exception as e:
                    print(f"⚠️ Screen capture error: {e}")
                    time.sleep(0.1)
                    
    except Exception as e:
        print(f"❌ Screen streaming error: {e}")
    finally:
        print("✅ Screen capture stopped")

# Connection handlers
@socketio.on("connect")
def on_connect():
    global is_streaming, connected_clients
    connected_clients += 1
    print(f"✅ Client connected (Total: {connected_clients})")
    
    if not is_streaming:
        is_streaming = True
        
        # Start screen streaming in thread
        screen_thread = threading.Thread(target=stream_screen, daemon=True)
        screen_thread.start()
        
        # Start audio streaming in separate thread
        audio_thread = threading.Thread(target=capture_audio, daemon=True)
        audio_thread.start()
        
        print("🚀 Streaming started")

@socketio.on("disconnect")
def on_disconnect():
    global connected_clients, is_streaming
    connected_clients -= 1
    print(f"❌ Client disconnected (Remaining: {connected_clients})")
    
    if connected_clients <= 0:
        is_streaming = False
        connected_clients = 0
        print("🛑 All clients disconnected, stopping streams")

@socketio.on("ping")
def handle_ping():
    """Keep connection alive"""
    socketio.emit("pong", namespace='/')

if __name__ == "__main__":
    print("=" * 60)
    print("⚡ HostCast - Screen + Audio Share")
    print("=" * 60)
    print("📡 Server: http://0.0.0.0:5000")
    print("🌐 LAN: http://192.168.1.32:5000")
    print("=" * 60)
    
    try:
        socketio.run(
            app, 
            host="0.0.0.0", 
            port=5000, 
            debug=False,
            use_reloader=False,
            log_output=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        is_streaming = False