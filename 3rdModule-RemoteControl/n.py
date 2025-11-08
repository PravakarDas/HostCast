"""
HostCast Module 3 - Remote Desktop Control
Full screen sharing + audio + remote control (mouse & keyboard)
"""
import base64
import io
import time
import threading
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from PIL import Image
import mss
import numpy as np
import pyaudiowpatch as pyaudio
import pyautogui
from pynput import mouse, keyboard as pynput_keyboard

# Flask + SocketIO setup
app = Flask(__name__)
socketio = SocketIO(
    app, 
    cors_allowed_origins="*", 
    async_mode="threading",
    ping_timeout=60,
    ping_interval=25,
    max_http_buffer_size=10**8,
    logger=False,
    engineio_logger=False
)

# Configuration
TARGET_WIDTH = 1280
AUDIO_CHUNK = 2048
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_RATE = 48000

# Global state
is_streaming = False
audio_lock = threading.Lock()
connected_clients = 0
control_enabled = {}
screen_dimensions = {'width': 1920, 'height': 1080}

# PyAutoGUI settings for faster response
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
pyautogui.MINIMUM_DURATION = 0

# Mouse and keyboard controllers
mouse_controller = mouse.Controller()
keyboard_controller = pynput_keyboard.Controller()

# Keyboard key mapping
KEY_MAP = {
    'Backspace': pynput_keyboard.Key.backspace,
    'Tab': pynput_keyboard.Key.tab,
    'Enter': pynput_keyboard.Key.enter,
    'Shift': pynput_keyboard.Key.shift,
    'Control': pynput_keyboard.Key.ctrl,
    'Alt': pynput_keyboard.Key.alt,
    'Pause': pynput_keyboard.Key.pause,
    'CapsLock': pynput_keyboard.Key.caps_lock,
    'Escape': pynput_keyboard.Key.esc,
    ' ': pynput_keyboard.Key.space,
    'PageUp': pynput_keyboard.Key.page_up,
    'PageDown': pynput_keyboard.Key.page_down,
    'End': pynput_keyboard.Key.end,
    'Home': pynput_keyboard.Key.home,
    'ArrowLeft': pynput_keyboard.Key.left,
    'ArrowUp': pynput_keyboard.Key.up,
    'ArrowRight': pynput_keyboard.Key.right,
    'ArrowDown': pynput_keyboard.Key.down,
    'Insert': pynput_keyboard.Key.insert,
    'Delete': pynput_keyboard.Key.delete,
    'Meta': pynput_keyboard.Key.cmd,
    'ContextMenu': pynput_keyboard.Key.menu,
    'F1': pynput_keyboard.Key.f1,
    'F2': pynput_keyboard.Key.f2,
    'F3': pynput_keyboard.Key.f3,
    'F4': pynput_keyboard.Key.f4,
    'F5': pynput_keyboard.Key.f5,
    'F6': pynput_keyboard.Key.f6,
    'F7': pynput_keyboard.Key.f7,
    'F8': pynput_keyboard.Key.f8,
    'F9': pynput_keyboard.Key.f9,
    'F10': pynput_keyboard.Key.f10,
    'F11': pynput_keyboard.Key.f11,
    'F12': pynput_keyboard.Key.f12,
    'NumLock': pynput_keyboard.Key.num_lock,
    'ScrollLock': pynput_keyboard.Key.scroll_lock,
}

@app.route('/')
def index():
    return render_template("index.html")

def get_loopback_device(p):
    """Get WASAPI loopback device"""
    try:
        wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        
        if not default_speakers["isLoopbackDevice"]:
            for loopback in p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    print(f"🎤 Loopback: {loopback['name']}")
                    return loopback
        return default_speakers
    except Exception as e:
        print(f"❌ Loopback error: {e}")
        return None

def capture_audio():
    """Capture system audio"""
    global is_streaming
    p = pyaudio.PyAudio()
    stream = None
    
    try:
        loopback = get_loopback_device(p)
        if not loopback:
            print("❌ No loopback device!")
            return
        
        rate = int(loopback["defaultSampleRate"])
        channels = int(loopback["maxInputChannels"])
        
        print(f"🎵 Audio: {rate}Hz, {channels}ch")
        
        stream = p.open(
            format=AUDIO_FORMAT,
            channels=channels,
            rate=rate,
            input=True,
            input_device_index=loopback["index"],
            frames_per_buffer=AUDIO_CHUNK,
            stream_callback=None
        )
        
        stream.start_stream()
        print("✅ Audio started")
        
        consecutive_errors = 0
        max_errors = 10
        
        while is_streaming and consecutive_errors < max_errors:
            try:
                if stream.is_active():
                    data = stream.read(AUDIO_CHUNK, exception_on_overflow=False)
                    
                    if data and len(data) > 0:
                        audio_b64 = base64.b64encode(data).decode('utf-8')
                        
                        with audio_lock:
                            socketio.emit("audio", {
                                "data": audio_b64,
                                "rate": rate,
                                "channels": channels
                            }, namespace='/')
                        
                        consecutive_errors = 0
                    
                    time.sleep(0.001)
                else:
                    break
                    
            except IOError:
                consecutive_errors += 1
                time.sleep(0.01)
            except Exception:
                consecutive_errors += 1
                time.sleep(0.01)
                
    except Exception as e:
        print(f"❌ Audio init error: {e}")
    finally:
        print("🛑 Audio stopped")
        if stream:
            try:
                stream.stop_stream()
                stream.close()
            except:
                pass
        p.terminate()

def stream_screen():
    """Capture and stream screen"""
    global is_streaming, screen_dimensions
    
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screen_dimensions = {
                'width': monitor['width'],
                'height': monitor['height']
            }
            
            print(f"📺 Screen: {monitor['width']}x{monitor['height']}")
            
            # Send screen dimensions to all clients
            socketio.emit("screen_info", screen_dimensions, namespace='/')
            
            frame_count = 0
            fps_time = time.time()
            target_frame_time = 1.0 / 30
            
            while is_streaming:
                frame_start = time.time()
                
                try:
                    frame = sct.grab(monitor)
                    img_np = np.array(frame)
                    img_np = img_np[:, :, :3][:, :, ::-1]
                    
                    img = Image.fromarray(img_np)
                    
                    if TARGET_WIDTH and img.width > TARGET_WIDTH:
                        ratio = TARGET_WIDTH / img.width
                        target_height = int(img.height * ratio)
                        img = img.resize((TARGET_WIDTH, target_height), Image.LANCZOS)
                    
                    buffer = io.BytesIO()
                    img.save(buffer, format="JPEG", quality=70, optimize=True)
                    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                    
                    socketio.emit("frame", img_b64, namespace='/')
                    
                    frame_count += 1
                    
                    if frame_count % 150 == 0:
                        elapsed = time.time() - fps_time
                        fps = 150 / elapsed
                        print(f"📊 FPS: {fps:.1f}")
                        fps_time = time.time()
                    
                    elapsed = time.time() - frame_start
                    sleep_time = max(0, target_frame_time - elapsed)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                    
                except Exception as e:
                    print(f"⚠️ Screen error: {e}")
                    time.sleep(0.1)
                    
    except Exception as e:
        print(f"❌ Screen error: {e}")
    finally:
        print("✅ Screen stopped")

# Mouse control handlers
@socketio.on("mouse_move")
def handle_mouse_move(data):
    """Handle mouse movement from client"""
    sid = request.sid
    if not control_enabled.get(sid, False):
        return
    
    try:
        # Convert relative coordinates (0-1) to absolute screen coordinates
        x = int(data['x'] * screen_dimensions['width'])
        y = int(data['y'] * screen_dimensions['height'])
        
        # Clamp to screen bounds
        x = max(0, min(x, screen_dimensions['width'] - 1))
        y = max(0, min(y, screen_dimensions['height'] - 1))
        
        # Move mouse using pynput for better compatibility
        mouse_controller.position = (x, y)
        
    except Exception as e:
        print(f"❌ Mouse move error: {e}")

@socketio.on("mouse_click")
def handle_mouse_click(data):
    """Handle mouse clicks from client"""
    sid = request.sid
    if not control_enabled.get(sid, False):
        return
    
    try:
        button_map = {
            'left': mouse.Button.left,
            'right': mouse.Button.right,
            'middle': mouse.Button.middle
        }
        
        button = button_map.get(data['button'], mouse.Button.left)
        action = data['action']
        
        if action == 'down':
            mouse_controller.press(button)
        elif action == 'up':
            mouse_controller.release(button)
        elif action == 'click':
            mouse_controller.click(button, 1)
        elif action == 'double':
            mouse_controller.click(button, 2)
        
        print(f"🖱️ Mouse {action}: {data['button']}")
            
    except Exception as e:
        print(f"❌ Mouse click error: {e}")

@socketio.on("mouse_scroll")
def handle_mouse_scroll(data):
    """Handle mouse scroll from client"""
    sid = request.sid
    if not control_enabled.get(sid, False):
        return
    
    try:
        delta_x = data.get('deltaX', 0)
        delta_y = data.get('deltaY', 0)
        
        # Scroll using pynput (dx, dy)
        if abs(delta_y) > 0:
            scroll_amount = -int(delta_y / 50)
            mouse_controller.scroll(0, scroll_amount)
        
        if abs(delta_x) > 0:
            scroll_amount = int(delta_x / 50)
            mouse_controller.scroll(scroll_amount, 0)
        
        print(f"🖱️ Scroll: dx={delta_x}, dy={delta_y}")
            
    except Exception as e:
        print(f"❌ Mouse scroll error: {e}")

# Keyboard control handlers
@socketio.on("key_event")
def handle_key_event(data):
    """Handle keyboard events from client"""
    sid = request.sid
    if not control_enabled.get(sid, False):
        return
    
    try:
        key = data['key']
        action = data['action']
        
        # Map special keys
        if key in KEY_MAP:
            mapped_key = KEY_MAP[key]
        else:
            # Regular character
            mapped_key = key
        
        if action == 'down':
            keyboard_controller.press(mapped_key)
            print(f"⌨️ Key DOWN: {key}")
        elif action == 'up':
            keyboard_controller.release(mapped_key)
            print(f"⌨️ Key UP: {key}")
            
    except Exception as e:
        print(f"❌ Key event error: {e}")

@socketio.on("enable_control")
def handle_enable_control(data):
    """Enable/disable remote control for a client"""
    sid = request.sid
    enabled = data.get('enabled', False)
    control_enabled[sid] = enabled
    
    if enabled:
        print(f"🎮 Control ENABLED for client {sid[:8]}")
        emit("control_status", {"enabled": True})
    else:
        print(f"🎮 Control DISABLED for client {sid[:8]}")
        emit("control_status", {"enabled": False})

# Connection handlers
@socketio.on("connect")
def on_connect():
    global is_streaming, connected_clients
    connected_clients += 1
    sid = request.sid
    control_enabled[sid] = False
    
    print(f"✅ Client connected: {sid[:8]} (Total: {connected_clients})")
    
    if not is_streaming:
        is_streaming = True
        
        screen_thread = threading.Thread(target=stream_screen, daemon=True)
        screen_thread.start()
        
        audio_thread = threading.Thread(target=capture_audio, daemon=True)
        audio_thread.start()
        
        print("🚀 Streaming started")
    else:
        # Send screen info to new client
        emit("screen_info", screen_dimensions)

@socketio.on("disconnect")
def on_disconnect():
    global connected_clients, is_streaming
    sid = request.sid
    
    if sid in control_enabled:
        del control_enabled[sid]
    
    connected_clients -= 1
    print(f"❌ Client disconnected: {sid[:8]} (Remaining: {connected_clients})")
    
    if connected_clients <= 0:
        is_streaming = False
        connected_clients = 0
        print("🛑 All clients disconnected")

@socketio.on("ping")
def handle_ping():
    emit("pong")

if __name__ == "__main__":
    print("=" * 60)
    print("⚡ HostCast Module 3 - Remote Desktop Control")
    print("=" * 60)
    print("📡 Server: http://0.0.0.0:5000")
    print("🎮 Features: Screen + Audio + Mouse + Keyboard Control")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: Run as Administrator for keyboard control!")
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
        print("\n🛑 Server stopped")
        is_streaming = False

        