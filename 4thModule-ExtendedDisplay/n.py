"""
HostCast Module 4 - Extended Display
Extends host display to client devices as virtual monitors
Client becomes an extended screen that host can drag windows to
"""
import base64
import io
import time
import threading
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from PIL import Image, ImageDraw, ImageFont
import mss
import numpy as np
import pyaudiowpatch as pyaudio
from pynput import mouse, keyboard as pynput_keyboard
import ctypes
import win32api
import win32con

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
connected_clients = {}
screen_dimensions = {'width': 1920, 'height': 1080}
keyboard_controller = pynput_keyboard.Controller()

# Key mapping
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
    'F1': pynput_keyboard.Key.f1, 'F2': pynput_keyboard.Key.f2,
    'F3': pynput_keyboard.Key.f3, 'F4': pynput_keyboard.Key.f4,
    'F5': pynput_keyboard.Key.f5, 'F6': pynput_keyboard.Key.f6,
    'F7': pynput_keyboard.Key.f7, 'F8': pynput_keyboard.Key.f8,
    'F9': pynput_keyboard.Key.f9, 'F10': pynput_keyboard.Key.f10,
    'F11': pynput_keyboard.Key.f11, 'F12': pynput_keyboard.Key.f12,
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
                    return loopback
        return default_speakers
    except Exception as e:
        print(f"❌ Loopback error: {e}")
        return None

def create_virtual_screen(width, height, display_name, mouse_x=None, mouse_y=None):
    """Create a virtual extended screen image with host cursor"""
    img = Image.new('RGB', (width, height), color=(15, 15, 25))
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([0, 0, width-1, height-1], outline=(0, 255, 0), width=5)
    
    # Draw grid
    grid_spacing = 80
    for x in range(0, width, grid_spacing):
        draw.line([(x, 0), (x, height)], fill=(35, 35, 45), width=1)
    for y in range(0, height, grid_spacing):
        draw.line([(0, y), (width, y)], fill=(35, 35, 45), width=1)
    
    # Draw center crosshair
    center_x, center_y = width // 2, height // 2
    draw.line([(center_x - 50, center_y), (center_x + 50, center_y)], fill=(0, 255, 0), width=2)
    draw.line([(center_x, center_y - 50), (center_x, center_y + 50)], fill=(0, 255, 0), width=2)
    
    # Draw text
    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    text = f"Extended Display"
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, height // 2 - 100), text, fill=(0, 255, 0), font=font_large)
    
    text2 = f"{display_name}"
    bbox2 = draw.textbbox((0, 0), text2, font=font_small)
    text_width2 = bbox2[2] - bbox2[0]
    draw.text(((width - text_width2) // 2, height // 2), text2, fill=(100, 255, 100), font=font_small)
    
    text3 = f"{width}x{height}"
    bbox3 = draw.textbbox((0, 0), text3, font=font_small)
    text_width3 = bbox3[2] - bbox3[0]
    draw.text(((width - text_width3) // 2, height // 2 + 50), text3, fill=(100, 255, 100), font=font_small)
    
    # Draw host cursor if provided
    if mouse_x is not None and mouse_y is not None:
        cursor_x = int(mouse_x * width)
        cursor_y = int(mouse_y * height)
        
        # Draw cursor circle
        cursor_size = 20
        draw.ellipse(
            [cursor_x - cursor_size, cursor_y - cursor_size, 
             cursor_x + cursor_size, cursor_y + cursor_size],
            outline=(255, 0, 255),
            width=4
        )
        
        # Draw crosshair on cursor
        draw.line([(cursor_x - cursor_size - 10, cursor_y), (cursor_x + cursor_size + 10, cursor_y)], 
                  fill=(255, 0, 255), width=3)
        draw.line([(cursor_x, cursor_y - cursor_size - 10), (cursor_x, cursor_y + cursor_size + 10)], 
                  fill=(255, 0, 255), width=3)
    
    return img

def capture_audio():
    """Capture system audio"""
    global is_streaming
    p = pyaudio.PyAudio()
    stream = None
    
    try:
        loopback = get_loopback_device(p)
        if not loopback:
            print("⚠️ No loopback device - audio disabled")
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
        
        while is_streaming:
            try:
                if stream.is_active():
                    data = stream.read(AUDIO_CHUNK, exception_on_overflow=False)
                    if data and len(data) > 0:
                        audio_b64 = base64.b64encode(data).decode('utf-8')
                        socketio.emit("audio", {
                            "data": audio_b64,
                            "rate": rate,
                            "channels": channels
                        }, namespace='/')
                    time.sleep(0.001)
                else:
                    break
            except:
                time.sleep(0.01)
                
    except Exception as e:
        print(f"❌ Audio error: {e}")
    finally:
        if stream:
            try:
                stream.stop_stream()
                stream.close()
            except:
                pass
        p.terminate()

def calculate_virtual_bounds(sid):
    """Calculate virtual display bounds"""
    client = connected_clients.get(sid)
    if not client:
        return None
    
    position = client['position']
    res = client['resolution']
    host_w = screen_dimensions['width']
    host_h = screen_dimensions['height']
    
    # Calculate bounds based on position
    if position == 'right':
        return {
            'x_min': host_w,
            'x_max': host_w + res['width'],
            'y_min': 0,
            'y_max': res['height']
        }
    elif position == 'left':
        return {
            'x_min': -res['width'],
            'x_max': 0,
            'y_min': 0,
            'y_max': res['height']
        }
    elif position == 'top':
        return {
            'x_min': 0,
            'x_max': res['width'],
            'y_min': -res['height'],
            'y_max': 0
        }
    elif position == 'bottom':
        return {
            'x_min': 0,
            'x_max': res['width'],
            'y_min': host_h,
            'y_max': host_h + res['height']
        }
    
    return None

def stream_extended_displays():
    """Stream virtual extended displays to clients"""
    global is_streaming
    
    try:
        print("📺 Extended display streaming started")
        
        target_frame_time = 1.0 / 30
        last_mouse_pos = {}
        
        while is_streaming:
            frame_start = time.time()
            
            try:
                # Get current mouse position
                mouse_pos = win32api.GetCursorPos()
                
                # Update each connected client
                for sid, client_info in list(connected_clients.items()):
                    if client_info.get('mode') == 'extended':
                        width = client_info['resolution']['width']
                        height = client_info['resolution']['height']
                        display_name = client_info['display_name']
                        
                        # Calculate if mouse is in this client's virtual area
                        bounds = calculate_virtual_bounds(sid)
                        mouse_x_rel = None
                        mouse_y_rel = None
                        
                        if bounds:
                            if (bounds['x_min'] <= mouse_pos[0] <= bounds['x_max'] and
                                bounds['y_min'] <= mouse_pos[1] <= bounds['y_max']):
                                # Mouse is in this display's area
                                mouse_x_rel = (mouse_pos[0] - bounds['x_min']) / (bounds['x_max'] - bounds['x_min'])
                                mouse_y_rel = (mouse_pos[1] - bounds['y_min']) / (bounds['y_max'] - bounds['y_min'])
                                
                                # Clamp to 0-1
                                mouse_x_rel = max(0, min(1, mouse_x_rel))
                                mouse_y_rel = max(0, min(1, mouse_y_rel))
                        
                        # Only regenerate if mouse moved or first frame
                        if sid not in last_mouse_pos or last_mouse_pos[sid] != (mouse_x_rel, mouse_y_rel):
                            last_mouse_pos[sid] = (mouse_x_rel, mouse_y_rel)
                            
                            # Create virtual screen with cursor
                            img = create_virtual_screen(width, height, display_name, mouse_x_rel, mouse_y_rel)
                            
                            # Resize for streaming
                            if TARGET_WIDTH and img.width > TARGET_WIDTH:
                                ratio = TARGET_WIDTH / img.width
                                target_height = int(img.height * ratio)
                                img = img.resize((TARGET_WIDTH, target_height), Image.LANCZOS)
                            
                            # Encode
                            buffer = io.BytesIO()
                            img.save(buffer, format="JPEG", quality=75, optimize=True)
                            img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                            
                            # Send to specific client
                            socketio.emit("frame", img_b64, room=sid)
                
                # Frame timing
                elapsed = time.time() - frame_start
                sleep_time = max(0, target_frame_time - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
            except Exception as e:
                print(f"⚠️ Stream error: {e}")
                time.sleep(0.1)
                    
    except Exception as e:
        print(f"❌ Display stream error: {e}")

# Client input handlers
@socketio.on("client_mouse_move")
def handle_client_mouse_move(data):
    """Handle mouse movement from client - move host cursor"""
    sid = request.sid
    client = connected_clients.get(sid)
    
    if not client or client.get('mode') != 'extended':
        return
    
    try:
        # Calculate absolute position in virtual space
        bounds = calculate_virtual_bounds(sid)
        if bounds:
            abs_x = int(bounds['x_min'] + data['x'] * (bounds['x_max'] - bounds['x_min']))
            abs_y = int(bounds['y_min'] + data['y'] * (bounds['y_max'] - bounds['y_min']))
            
            # Move cursor
            ctypes.windll.user32.SetCursorPos(abs_x, abs_y)
    except Exception as e:
        print(f"❌ Client mouse error: {e}")

@socketio.on("client_mouse_click")
def handle_client_mouse_click(data):
    """Handle mouse click from client"""
    sid = request.sid
    client = connected_clients.get(sid)
    
    if not client or client.get('mode') != 'extended':
        return
    
    try:
        button_map = {
            'left': (win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP),
            'right': (win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP),
            'middle': (win32con.MOUSEEVENTF_MIDDLEDOWN, win32con.MOUSEEVENTF_MIDDLEUP)
        }
        
        action = data['action']
        button = data['button']
        
        if button in button_map:
            down_event, up_event = button_map[button]
            
            if action == 'down':
                win32api.mouse_event(down_event, 0, 0, 0, 0)
            elif action == 'up':
                win32api.mouse_event(up_event, 0, 0, 0, 0)
            elif action == 'click':
                win32api.mouse_event(down_event, 0, 0, 0, 0)
                time.sleep(0.01)
                win32api.mouse_event(up_event, 0, 0, 0, 0)
        
        print(f"🖱️ Click: {button} {action}")
    except Exception as e:
        print(f"❌ Click error: {e}")

@socketio.on("client_mouse_scroll")
def handle_client_mouse_scroll(data):
    """Handle scroll from client"""
    sid = request.sid
    client = connected_clients.get(sid)
    
    if not client or client.get('mode') != 'extended':
        return
    
    try:
        delta_y = data.get('deltaY', 0)
        if abs(delta_y) > 0:
            scroll_amount = -int(delta_y)
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, scroll_amount, 0)
    except Exception as e:
        print(f"❌ Scroll error: {e}")

@socketio.on("client_key_event")
def handle_client_key_event(data):
    """Handle keyboard from client"""
    sid = request.sid
    client = connected_clients.get(sid)
    
    if not client or client.get('mode') != 'extended':
        return
    
    try:
        key = data['key']
        action = data['action']
        
        if key in KEY_MAP:
            mapped_key = KEY_MAP[key]
        else:
            mapped_key = key
        
        if action == 'down':
            keyboard_controller.press(mapped_key)
        elif action == 'up':
            keyboard_controller.release(mapped_key)
        
        print(f"⌨️ Key: {key} {action}")
    except Exception as e:
        print(f"❌ Key error: {e}")

@socketio.on("set_display_mode")
def handle_set_display_mode(data):
    """Set client display mode and configuration"""
    sid = request.sid
    
    mode = data.get('mode', 'extended')
    position = data.get('position', 'right')
    resolution = data.get('resolution', {'width': 1920, 'height': 1080})
    display_name = data.get('display_name', f'Display-{sid[:8]}')
    
    connected_clients[sid] = {
        'mode': mode,
        'position': position,
        'resolution': resolution,
        'display_name': display_name
    }
    
    bounds = calculate_virtual_bounds(sid)
    
    print(f"📺 Client configured: {display_name}")
    print(f"   Position: {position}")
    print(f"   Resolution: {resolution['width']}x{resolution['height']}")
    print(f"   Virtual bounds: X({bounds['x_min']} to {bounds['x_max']}), Y({bounds['y_min']} to {bounds['y_max']})")
    
    emit("display_configured", {
        'virtual_bounds': bounds,
        'host_screen': screen_dimensions
    })

@socketio.on("connect")
def on_connect():
    global is_streaming
    sid = request.sid
    
    print(f"✅ Client connected: {sid[:8]}")
    
    # Get host screen info
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screen_dimensions['width'] = monitor['width']
        screen_dimensions['height'] = monitor['height']
    
    print(f"   Host screen: {screen_dimensions['width']}x{screen_dimensions['height']}")
    
    emit("screen_info", screen_dimensions)
    
    if not is_streaming:
        is_streaming = True
        
        threading.Thread(target=stream_extended_displays, daemon=True).start()
        threading.Thread(target=capture_audio, daemon=True).start()
        
        print("🚀 Streaming started")

@socketio.on("disconnect")
def on_disconnect():
    global is_streaming
    sid = request.sid
    
    if sid in connected_clients:
        print(f"❌ Client disconnected: {connected_clients[sid]['display_name']}")
        del connected_clients[sid]
    
    if len(connected_clients) == 0:
        is_streaming = False
        print("🛑 All clients disconnected")

@socketio.on("ping")
def handle_ping():
    emit("pong")

if __name__ == "__main__":
    print("=" * 70)
    print("⚡ HostCast Module 4 - Extended Display System")
    print("=" * 70)
    print("📡 Server: http://0.0.0.0:5000")
    print("🖥️  Features: Virtual Extended Display + Audio")
    print("=" * 70)
    print("\n💡 How to use:")
    print("   1. Connect client browser to http://<host-ip>:5000")
    print("   2. Configure display position (left/right/top/bottom)")
    print("   3. Move mouse PAST your screen edge to see it on client")
    print("   4. Client can also control host by moving mouse/typing")
    print("=" * 70)
    print("\n⚠️  IMPORTANT: Run as Administrator!")
    print("=" * 70)
    
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