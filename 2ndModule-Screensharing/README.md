# 🖥️ HostCast Module 2: Screen Mirroring & Audio Streaming

<div align="center">

![Module 2 Banner](https://img.shields.io/badge/Module_2-Screen_Mirroring-blueviolet?style=for-the-badge)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![MSS](https://img.shields.io/badge/MSS-9.0.1-orange?style=flat-square)](https://python-mss.readthedocs.io/)
[![PyAudioWPatch](https://img.shields.io/badge/PyAudioWPatch-0.2.12.5-red?style=flat-square)](https://github.com/s0d3s/PyAudioWPatch)

**Professional real-time screen sharing with synchronized audio streaming and modern neon-themed UI.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Technical Details](#-technical-details) • [Troubleshooting](#-troubleshooting)

</div>

---

## 📖 Overview

Module 2 is a cutting-edge screen mirroring solution that streams your Windows desktop and system audio in real-time to multiple devices over your local network. Built with modern web technologies and featuring a stunning neon-themed glassmorphism UI, it's perfect for presentations, remote assistance, media streaming, and collaborative viewing.

### ✨ Key Highlights

- 🎥 **30+ FPS Screen Streaming** - Smooth, real-time screen capture with adaptive resolution
- 🔊 **Synchronized Audio** - Windows WASAPI loopback for perfect audio-video sync
- 🎨 **Modern Neon UI** - Professional glassmorphism design with animated effects
- 📊 **Live Statistics** - Real-time FPS, quality, and bandwidth monitoring
- 🎛️ **Interactive Controls** - Volume, mute, play/pause, fullscreen
- 🔄 **Smart Reconnection** - Automatic recovery from connection drops
- 📱 **Multi-Device Support** - Stream to unlimited clients simultaneously

---

## 🎁 Features

### Video Streaming

#### 📺 Screen Capture
- **MSS Technology**: Ultra-fast screen capture using Python-MSS library
- **Adaptive Resolution**: Automatic scaling to 1280px width (configurable)
- **High Frame Rate**: 30+ FPS for smooth viewing experience
- **Primary Monitor**: Captures main display (monitor 1)
- **Quality Optimization**: JPEG compression at 70% quality for optimal balance

#### 🎬 Video Processing
- **NumPy Array Processing**: Efficient pixel manipulation
- **PIL/Pillow Encoding**: Fast JPEG encoding with optimization
- **Base64 Transmission**: Reliable data transmission over WebSocket
- **Frame Buffering**: Smart buffering prevents frame drops
- **Latency Optimization**: 100-300ms typical latency

### Audio Streaming

#### 🎵 Audio Capture
- **WASAPI Loopback**: Windows Audio Session API for system audio
- **Multi-Channel Support**: Stereo and mono audio streams
- **Native Sample Rate**: Matches system audio settings (typically 48kHz)
- **Large Chunks**: 4096 sample chunks for smooth playback
- **Error Recovery**: Automatic handling of buffer overflows/underflows

#### 🔊 Audio Processing
- **16-bit PCM**: High-quality audio format (paInt16)
- **Base64 Encoding**: Efficient transmission encoding
- **Synchronized Streaming**: Audio-video sync within 50ms
- **Smart Buffering**: Prevents crackling and skipping
- **Auto-Detection**: Automatically finds default audio output device

### User Interface

#### 🎨 Design Elements
- **Neon Color Scheme**: Cyan (#00f2ff), Purple (#7b2ff7), Pink (#ff00ff)
- **Glassmorphism**: Frosted glass effects with backdrop blur
- **Animated Background**: Three floating neon orbs for ambient effect
- **Gradient Accents**: Smooth color transitions throughout
- **Responsive Layout**: Adapts to desktop, tablet, and mobile

#### 🎛️ Control Panel
- **Play/Pause Button**: Control stream playback
- **Volume Control**: Slider with visual feedback
- **Mute Toggle**: One-click audio muting
- **Fullscreen Mode**: Immersive viewing experience
- **Interactive Tooltips**: Helpful hover information

#### 📊 Statistics Panel
- **FPS Counter**: Real-time frame rate display
- **Quality Indicator**: Visual quality meter
- **Connection Status**: Live connection state with color coding
- **Stream Status**: Current stream state indicator
- **Bandwidth Monitor**: Data transfer visualization

#### ⚡ Status Indicators
- **Connection Dot**: Red (disconnected), Yellow (connecting), Green (connected)
- **Stream State**: Waiting, Buffering, Streaming, Error states
- **Visual Feedback**: Instant state change notifications
- **Loading Animation**: Professional spinner during initialization

---

## 🚀 Installation

### Prerequisites

- **Operating System**: Windows 10/11 (required for audio streaming)
- **Python**: 3.8 or higher
- **pip**: Python package manager
- **Network**: LAN or WiFi connection
- **Audio Device**: Windows audio output device enabled

### Step-by-Step Setup

1. **Navigate to Module Directory**
   ```bash
   cd HostCast/mod2_screenshare
   ```

2. **Install Dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```
   
   **Core Dependencies:**
   ```
   Flask==3.0.3                 # Web framework
   Flask-SocketIO==5.3.6        # Real-time communication
   python-socketio==5.11.3      # SocketIO client
   python-engineio==4.9.1       # Engine.IO implementation
   mss==9.0.1                   # Screen capture
   Pillow==11.0.0               # Image processing
   numpy==1.26.4                # Array processing
   pyaudiowpatch>=0.2.12.5      # Windows audio capture
   ```

3. **Verify Installation**
   ```bash
   python -c "import flask, flask_socketio, mss, PIL, numpy, pyaudiowpatch; print('All dependencies installed!')"
   ```

### PyAudioWPatch Installation Notes

**Important**: PyAudioWPatch is Windows-specific and required for audio streaming.

If you encounter installation issues:

```bash
# Update pip and setuptools
python -m pip install --upgrade pip setuptools

# Install wheel package
pip install wheel

# Install PyAudioWPatch
pip install pyaudiowpatch

# Verify installation
python -c "import pyaudiowpatch; print('PyAudioWPatch installed successfully!')"
```

---

## 📱 Usage

### Starting the Server

1. **Run the Application**
   ```bash
   python screenshare_audio.py
   ```

2. **Expected Console Output**
   ```
   ============================================================
   ⚡ HostCast - Screen + Audio Share
   ============================================================
   📡 Server: http://0.0.0.0:5000
   🌐 LAN: http://192.168.1.32:5000
   ============================================================
   ```

3. **Server is Ready** when you see:
   ```
   * Running on http://0.0.0.0:5000
   ```

### Accessing the Viewer

**From Host Machine:**
```
http://localhost:5000
```

**From Other Devices (same network):**
```
http://<host-ip>:5000
```
Example: `http://192.168.1.100:5000`

### Using the Interface

#### Initial Connection

1. **Open URL** in any modern browser
2. **Wait for Connection**: Status indicator turns green
3. **Click Anywhere**: Required to enable audio (browser security)
4. **Start Viewing**: Screen and audio begin streaming

#### Control Panel

**Play/Pause Button** (▶️/⏸️)
- **Function**: Control stream playback
- **Shortcut**: Spacebar
- **State**: Toggles between play and pause

**Volume Control** (🔊)
- **Function**: Adjust audio volume (0-100%)
- **Default**: 50%
- **Interaction**: Drag slider or click position
- **Visual**: Real-time volume bar indicator

**Mute Button** (🔇)
- **Function**: Toggle audio on/off
- **Shortcut**: M key
- **Visual**: Button changes color when muted
- **State**: Preserves volume level

**Fullscreen Button** (⛶)
- **Function**: Toggle fullscreen mode
- **Shortcut**: F key or F11
- **Exit**: ESC key or click button again
- **Benefits**: Immersive viewing, hides UI clutter

#### Statistics Panel

**FPS Counter**
- **Display**: Current frames per second
- **Target**: 30 FPS
- **Color Coding**:
  - Green: 25-30+ FPS (Excellent)
  - Yellow: 15-25 FPS (Good)
  - Red: <15 FPS (Poor)

**Quality Indicator**
- **Visual**: Circular progress meter
- **Range**: 0-100%
- **Factors**: FPS, bandwidth, latency
- **Real-time**: Updates every second

**Connection Status**
- **States**:
  - 🔴 Disconnected (Red)
  - 🟡 Connecting (Yellow)
  - 🟢 Connected (Green)
- **Auto-reconnect**: Attempts every 3 seconds on disconnect

### Advanced Features

#### Fullscreen Mode

**Activate**:
- Click fullscreen button
- Press F key
- Press F11 (browser fullscreen)

**Features in Fullscreen**:
- Statistics panel hidden by default
- Control panel auto-hides after 3 seconds
- Move mouse to show controls
- Cleaner viewing experience

**Exit**:
- Press ESC key
- Click fullscreen button
- Press F11

#### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Space** | Play/Pause stream |
| **M** | Mute/Unmute audio |
| **F** | Toggle fullscreen |
| **F11** | Browser fullscreen |
| **ESC** | Exit fullscreen |
| **+** / **-** | Volume up/down (if implemented) |

---

## 🛠️ Technical Details

### Architecture

```
┌─────────────────────────────────────────────────────┐
│           Windows Host Machine                      │
│                                                     │
│  ┌──────────────┐         ┌──────────────────┐    │
│  │ MSS Screen   │         │ PyAudioWPatch    │    │
│  │ Capture      │         │ WASAPI Loopback  │    │
│  │              │         │                  │    │
│  │ • Primary    │         │ • System Audio   │    │
│  │   Monitor    │         │ • 48kHz 16-bit   │    │
│  │ • 30+ FPS    │         │ • 4096 chunks    │    │
│  │ • Adaptive   │         │ • Stereo/Mono    │    │
│  │   Resolution │         │                  │    │
│  └──────┬───────┘         └────────┬─────────┘    │
│         │                          │               │
│         └──────────┬───────────────┘               │
│                    │                               │
│         ┌──────────▼──────────┐                    │
│         │ Image Processing    │                    │
│         │ • NumPy arrays      │                    │
│         │ • PIL/Pillow JPEG   │                    │
│         │ • Base64 encoding   │                    │
│         └──────────┬──────────┘                    │
│                    │                               │
│         ┌──────────▼──────────┐                    │
│         │ Flask + SocketIO    │                    │
│         │ Port 5000           │                    │
│         │                     │                    │
│         │ Events:             │                    │
│         │ • frame             │                    │
│         │ • audio             │                    │
│         │ • connect           │                    │
│         │ • disconnect        │                    │
│         └──────────┬──────────┘                    │
└────────────────────┼────────────────────────────────┘
                     │
          WebSocket over LAN
                     │
┌────────────────────┼────────────────────────────────┐
│                    ▼                                │
│         ┌─────────────────────┐                    │
│         │   Client Browser    │                    │
│         │                     │                    │
│         │ JavaScript ES6      │                    │
│         │ • Socket.IO client  │                    │
│         │ • Web Audio API     │                    │
│         │ • Canvas rendering  │                    │
│         │ • Event handlers    │                    │
│         └──────────┬──────────┘                    │
│                    │                               │
│         ┌──────────▼──────────┐                    │
│         │ UI Components       │                    │
│         │                     │                    │
│         │ • Screen display    │                    │
│         │ • Control panel     │                    │
│         │ • Stats panel       │                    │
│         │ • Status indicators │                    │
│         └─────────────────────┘                    │
│                                                     │
│     Supports: Chrome, Firefox, Edge, Safari        │
└─────────────────────────────────────────────────────┘
```

### File Structure

```
mod2_screenshare/
├── screenshare_audio.py        # Main Flask application
├── templates/
│   └── index.html              # Modern UI template
├── static/
│   ├── css/
│   │   └── style.css          # Neon glassmorphism styles (700+ lines)
│   ├── js/
│   │   └── script.js          # ES6 client logic (500+ lines)
│   └── assets/                # (Empty - for future assets)
├── MODERNIZATION_COMPLETE.md   # UI modernization notes
├── README_UI.md                # UI design documentation
└── README.md                   # This file
```

### Backend Components

#### Main Server (`screenshare_audio.py`)

**Configuration**:
```python
TARGET_WIDTH = 1280           # Video width in pixels
AUDIO_CHUNK = 4096            # Audio samples per chunk
AUDIO_FORMAT = pyaudio.paInt16  # 16-bit PCM
AUDIO_RATE = 48000            # Sample rate in Hz
```

**Threading Model**:
- **Main Thread**: Flask application and SocketIO event loop
- **Screen Thread**: Continuous screen capture (daemon)
- **Audio Thread**: Continuous audio capture (daemon)
- **Thread Safety**: Locks for shared resources

**SocketIO Events**:

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `connect` | Client → Server | None | Client connection established |
| `disconnect` | Client → Server | None | Client disconnection |
| `frame` | Server → Client | Base64 JPEG | Video frame data |
| `audio` | Server → Client | Base64 PCM + metadata | Audio chunk with rate/channels |
| `ping` | Client → Server | None | Keep-alive ping |
| `pong` | Server → Client | None | Keep-alive response |

#### Screen Capture Function

```python
def stream_screen():
    """Captures screen at 30 FPS and broadcasts via WebSocket"""
    - Captures using MSS (native OS calls)
    - Converts BGRA to RGB using NumPy
    - Resizes to TARGET_WIDTH maintaining aspect ratio
    - Encodes as JPEG (quality 70%)
    - Base64 encodes for transmission
    - Emits via SocketIO to all clients
    - Frame timing: ~33ms per frame (30 FPS)
```

#### Audio Capture Function

```python
def capture_audio():
    """Captures system audio using WASAPI loopback"""
    - Finds default audio output device
    - Creates loopback device for capture
    - Opens audio stream (48kHz, 16-bit, stereo)
    - Reads 4096 sample chunks
    - Base64 encodes audio data
    - Emits with sample rate and channel info
    - Error recovery for buffer issues
    - Precise timing to prevent underruns
```

### Frontend Components

#### JavaScript Client (`script.js`)

**HostCastViewer Class**:
```javascript
class HostCastViewer {
    constructor() {
        // Initialize Socket.IO connection
        // Setup Web Audio API context
        // Create audio buffer queue
        // Initialize UI event handlers
        // Setup statistics tracking
    }
    
    // Key methods:
    connectSocket()          // Establish WebSocket connection
    handleFrame(data)        // Process and display video frames
    handleAudio(data)        // Decode and play audio
    toggleFullscreen()       // Fullscreen mode management
    updateStats()            // Real-time statistics update
    handleReconnect()        // Auto-reconnection logic
}
```

**Web Audio API Setup**:
```javascript
// Audio context initialization
this.audioContext = new (window.AudioContext || window.webkitAudioContext)();

// Audio buffer queue for smooth playback
this.audioQueue = [];
this.isPlaying = false;

// Process incoming audio chunks
playAudioChunk(pcmData, sampleRate, channels)
```

#### CSS Styling (`style.css`)

**CSS Custom Properties**:
```css
:root {
    /* Neon Colors */
    --neon-cyan: #00f2ff;
    --neon-purple: #7b2ff7;
    --neon-pink: #ff00ff;
    
    /* Glass Effects */
    --glass-bg: rgba(255, 255, 255, 0.05);
    --glass-border: rgba(255, 255, 255, 0.1);
    
    /* Animations */
    --transition-speed: 0.3s;
    --glow-intensity: 0 0 20px;
}
```

**Key Features**:
- Glassmorphism with `backdrop-filter: blur(20px)`
- CSS Grid and Flexbox layouts
- Keyframe animations for loading states
- Media queries for responsive design
- CSS transforms for smooth interactions
- Box shadows for depth and glow effects

---

## 🔧 Configuration

### Video Settings

**Resolution**:
```python
TARGET_WIDTH = 1280  # Change to adjust stream resolution
# Options: 1920 (1080p), 1280 (720p), 854 (480p), 640 (360p)
```

**Frame Rate**:
```python
target_frame_time = 1.0 / 30  # 30 FPS
# Options: 1/60 (60 FPS), 1/30 (30 FPS), 1/15 (15 FPS)
```

**JPEG Quality**:
```python
img.save(buffer, format="JPEG", quality=70, optimize=True)
# Quality range: 10-100 (higher = better quality, larger file)
```

### Audio Settings

**Sample Rate**:
```python
AUDIO_RATE = 48000  # Match your system's native rate
# Common rates: 48000, 44100, 32000, 16000
```

**Chunk Size**:
```python
AUDIO_CHUNK = 4096  # Larger = smoother, more latency
# Options: 2048, 4096, 8192
```

**Audio Format**:
```python
AUDIO_FORMAT = pyaudio.paInt16  # 16-bit PCM
# Other options: paInt24, paInt32 (higher quality, more bandwidth)
```

### Server Settings

**Port**:
```python
socketio.run(app, host="0.0.0.0", port=5000, debug=False)
# Change port=5000 to your desired port
```

**Debug Mode**:
```python
debug=False  # Set to True for development
# Debug mode enables auto-reload and verbose logging
```

**SocketIO Timeouts**:
```python
socketio = SocketIO(
    app,
    ping_timeout=60,      # Seconds before timeout
    ping_interval=25,     # Seconds between pings
    max_http_buffer_size=10**8  # Max message size
)
```

---

## 🐛 Known Issues & Limitations

### Critical Issues

1. **Windows-Only Audio Streaming**
   - **Issue**: PyAudioWPatch requires Windows WASAPI
   - **Impact**: Audio won't work on Linux/macOS
   - **Workaround**: Video-only mode on non-Windows systems
   - **Status**: 🔴 Platform limitation

2. **Browser Audio Autoplay Restriction**
   - **Issue**: Browsers block audio until user interaction
   - **Impact**: Must click page before audio plays
   - **Workaround**: Clear "Click to Enable Audio" message
   - **Status**: 🟡 Browser security policy

3. **Primary Monitor Only**
   - **Issue**: Only captures primary display (monitor 1)
   - **Impact**: Cannot stream secondary monitors
   - **Workaround**: Set desired monitor as primary
   - **Status**: 🔴 Feature not implemented

### Performance Issues

4. **Network Latency**
   - **Issue**: 100-300ms delay typical, up to 500ms on WiFi
   - **Impact**: Not suitable for real-time gaming/typing
   - **Workaround**: Use wired Ethernet connection
   - **Status**: 🟡 Network dependent

5. **High CPU Usage**
   - **Issue**: 15-30% CPU on modern systems
   - **Impact**: May slow down other applications
   - **Workaround**: Lower resolution or frame rate
   - **Status**: 🟡 Expected for real-time encoding

6. **Bandwidth Requirements**
   - **Issue**: Requires 10+ Mbps for smooth streaming
   - **Impact**: May stutter on slow networks
   - **Workaround**: Reduce video quality settings
   - **Status**: 🟡 Expected for video streaming

### UI/UX Issues

7. **Fullscreen Control Auto-hide**
   - **Issue**: Controls disappear after 3 seconds in fullscreen
   - **Impact**: May be confusing initially
   - **Workaround**: Move mouse to reveal controls
   - **Status**: 🟢 By design (immersive mode)

8. **Mobile Browser Limitations**
   - **Issue**: Smaller screens, touch controls less precise
   - **Impact**: Not ideal for mobile viewing
   - **Workaround**: Use tablet or desktop
   - **Status**: 🟡 Responsive design limitations

### Audio Issues

9. **Audio Crackling on Weak Networks**
   - **Issue**: Occasional audio crackling/skipping
   - **Impact**: Degraded audio quality
   - **Workaround**: Improve network stability, reduce chunk size
   - **Status**: 🟡 Network dependent

10. **Audio Desynchronization**
    - **Issue**: Audio may drift from video after hours of streaming
    - **Impact**: A/V sync degrades over time
    - **Workaround**: Refresh page periodically
    - **Status**: 🟡 Rare edge case

### Technical Limitations

11. **No Multi-Monitor Support**
    - **Status**: 🔴 Not implemented

12. **No Screen Region Selection**
    - **Status**: 🔴 Not implemented

13. **No Recording Capability**
    - **Status**: 🔴 Not implemented

14. **No Password Protection**
    - **Status**: 🔴 Not implemented

15. **No Encryption**
    - **Issue**: Data transmitted unencrypted on LAN
    - **Impact**: Vulnerable on untrusted networks
    - **Status**: 🔴 Security limitation

---

## 🔧 Troubleshooting

### Server Issues

#### Server Won't Start

**Error**: `OSError: [WinError 10048] Only one usage of each socket address`

**Solution**:
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Or change port in screenshare_audio.py
```

**Error**: `ModuleNotFoundError: No module named 'pyaudiowpatch'`

**Solution**:
```bash
pip install pyaudiowpatch>=0.2.12.5
```

**Error**: `ImportError: DLL load failed while importing _portaudio`

**Solution**:
```bash
# Reinstall PyAudioWPatch
pip uninstall pyaudiowpatch
pip install pyaudiowpatch --no-cache-dir

# Install Microsoft Visual C++ Redistributable
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
```

#### Audio Not Capturing

**Check 1**: Audio device enabled
```powershell
# Open Sound Settings
control mmsys.cpl

# Ensure default playback device is enabled
```

**Check 2**: PyAudioWPatch installation
```python
# Test in Python console
import pyaudiowpatch as pyaudio
p = pyaudio.PyAudio()
print(p.get_default_output_device_info())
```

**Check 3**: Console output
```
# Look for error messages like:
❌ Error getting loopback device: ...
❌ Audio initialization error: ...
```

**Solution**:
1. Verify audio is playing on host (play music)
2. Check Windows audio settings
3. Try different audio device
4. Reinstall PyAudioWPatch

#### Screen Capture Fails

**Error**: `ScreenShotError`

**Solution**:
```python
# Check if MSS can capture
from mss import mss
with mss() as sct:
    print(sct.monitors)  # Should show monitor list
```

**Issue**: Black screen captured

**Solution**:
1. Check if app has screen recording permissions
2. Disable hardware acceleration in applications
3. Update graphics drivers

### Client Issues

#### Cannot Connect to Server

**Check 1**: Server running
```bash
# Should see server output
# ⚡ HostCast - Screen + Audio Share
```

**Check 2**: IP address correct
```powershell
ipconfig
# Use IPv4 Address from active network adapter
```

**Check 3**: Firewall
```powershell
# Allow Python through firewall
netsh advfirewall firewall add rule name="HostCast Screen Share" dir=in action=allow protocol=TCP localport=5000
```

**Check 4**: Same network
```powershell
# From client device, ping host
ping <host-ip>
```

#### No Video Showing

**Symptom**: Loading spinner persists

**Check 1**: Browser console (F12)
```javascript
// Look for errors:
// Failed to connect to ws://...
// Error loading image: ...
```

**Check 2**: Network tab
```
// Check if WebSocket connected
// Status should be 101 Switching Protocols
```

**Solution**:
1. Refresh page (Ctrl+R)
2. Clear browser cache (Ctrl+Shift+Delete)
3. Try different browser
4. Check server console for errors

#### No Audio Playing

**Symptom**: Video works but no audio

**Check 1**: Click interaction
```
// Ensure you clicked page at least once
// Browsers require user interaction for audio
```

**Check 2**: Browser console
```javascript
// Look for:
// AudioContext state: suspended
// Audio permission denied
```

**Check 3**: Volume settings
```
// Check:
// - Browser tab not muted
// - Volume slider not at 0
// - Mute button not active
// - System volume not muted
```

**Solution**:
1. Click page to enable audio
2. Check volume slider (middle of control panel)
3. Unmute if needed
4. Verify host audio is playing

#### Poor Video Quality

**Symptom**: Pixelated or blurry image

**Solutions**:
1. **Increase JPEG quality** in `screenshare_audio.py`:
   ```python
   img.save(buffer, format="JPEG", quality=85, optimize=True)  # Increase from 70
   ```

2. **Increase resolution**:
   ```python
   TARGET_WIDTH = 1920  # Increase from 1280
   ```

3. **Check network speed**:
   ```powershell
   # Test bandwidth
   # Should have 10+ Mbps available
   ```

#### Audio Crackling/Skipping

**Symptom**: Audio stutters or crackles

**Solutions**:
1. **Increase chunk size** in `screenshare_audio.py`:
   ```python
   AUDIO_CHUNK = 8192  # Increase from 4096
   ```

2. **Check CPU usage**:
   ```powershell
   # Task Manager → Performance
   # CPU should be below 80%
   ```

3. **Improve network**:
   - Use Ethernet instead of WiFi
   - Reduce network congestion
   - Close bandwidth-heavy applications

4. **Lower video quality**:
   ```python
   TARGET_WIDTH = 854  # Reduce to 480p
   ```

#### High Latency

**Symptom**: 500ms+ delay between host and viewer

**Solutions**:
1. **Use wired connection**: Switch from WiFi to Ethernet
2. **Reduce frame rate**: Lower FPS to reduce bandwidth
3. **Optimize network**: Close other streaming applications
4. **Check ping**:
   ```powershell
   ping <host-ip>
   # Should be <10ms on LAN
   ```

### Browser-Specific Issues

#### Chrome/Edge

**Issue**: High CPU usage

**Solution**:
```
chrome://flags
# Disable hardware acceleration if needed
```

#### Firefox

**Issue**: Audio sync issues

**Solution**:
```
about:config
media.autoplay.default = 0  # Allow autoplay
```

#### Safari

**Issue**: WebSocket connection drops

**Solution**:
1. Update to latest Safari version
2. Check Safari privacy settings
3. Disable "Prevent cross-site tracking"

---

## 📊 Performance Optimization

### Host Machine Optimization

1. **Close Unnecessary Applications**
   - Free up CPU and RAM
   - Close browser tabs
   - Stop background updates

2. **Graphics Settings**
   ```
   Windows Settings → System → Display
   • Set refresh rate to 60Hz
   • Disable transparency effects
   • Reduce animations
   ```

3. **Power Settings**
   ```
   Control Panel → Power Options
   • Set to High Performance mode
   • Prevent sleep during streaming
   ```

4. **Network Priority**
   ```powershell
   # Set Python process to high priority
   Get-Process python | Select-Object -First 1 | Set-ProcessPriority -Priority High
   ```

### Client Device Optimization

1. **Browser Settings**
   - Enable hardware acceleration
   - Clear cache and cookies
   - Disable unnecessary extensions
   - Use Incognito/Private mode

2. **Display Settings**
   - Match client display resolution to stream
   - Use fullscreen mode for better performance
   - Disable browser UI for cleaner view

3. **Network Settings**
   - Connect via Ethernet if possible
   - Disable VPN/proxy
   - Close other streaming services
   - Set router QoS priority for streaming

### Network Optimization

1. **Wired Connection**
   ```
   WiFi: 50-100ms latency, packet loss possible
   Ethernet: <10ms latency, no packet loss
   ```

2. **Router Settings**
   ```
   • Enable QoS (Quality of Service)
   • Prioritize host and client IPs
   • Use 5GHz WiFi if available
   • Update router firmware
   ```

3. **Bandwidth Management**
   ```
   Required bandwidth:
   • 1280x720 @ 30fps = ~5-10 Mbps
   • Audio @ 48kHz = ~1.5 Mbps
   • Total recommended: 15+ Mbps
   ```

---

## 🎯 Use Cases

### 1. Presentations & Demos
- Present slides to multiple devices
- Demo software to team members
- Share screen during meetings
- Training sessions

### 2. Media Streaming
- Watch movies/videos on other devices
- Share music playback across rooms
- Stream gameplay to viewers
- Display photo slideshows

### 3. Remote Assistance
- Help family/friends troubleshoot
- Guide users through software
- Monitor other computers
- Tech support sessions

### 4. Education
- Virtual classroom screen sharing
- Tutorial recording setups
- Student presentation viewing
- Multi-room learning

### 5. Entertainment
- Watch PC content on TV browser
- Stream to tablets while cooking
- Share gaming sessions
- Multi-room music sync

---

## 🔮 Future Enhancements

### Planned Features

- [ ] **Multi-monitor support** - Select which monitor to stream
- [ ] **Screen region selection** - Capture specific area
- [ ] **Recording capability** - Save streams to file
- [ ] **Password protection** - Secure access
- [ ] **SSL/TLS encryption** - Encrypted streaming
- [ ] **Bitrate control** - Manual quality adjustment
- [ ] **Audio input switching** - Choose audio source
- [ ] **Client-side recording** - Record on viewer device
- [ ] **Picture-in-Picture mode** - Floating window viewer
- [ ] **Multiple quality presets** - Quick quality switching
- [ ] **Mobile app** - Dedicated mobile viewers
- [ ] **Chromecast support** - Cast to TV devices
- [ ] **Chat feature** - Text communication
- [ ] **File transfer** - Send files during streaming
- [ ] **Virtual pointer** - Highlight areas on screen

### Potential Improvements

- [ ] Linux/macOS audio support (via PulseAudio/CoreAudio)
- [ ] Hardware-accelerated encoding (H.264/H.265)
- [ ] WebRTC for lower latency
- [ ] Adaptive bitrate streaming
- [ ] Better error recovery
- [ ] Stream recording history
- [ ] Usage statistics dashboard
- [ ] Multi-language support
- [ ] Dark/Light theme toggle
- [ ] Customizable UI colors
- [ ] Gesture controls for mobile
- [ ] Voice commands
- [ ] AI-powered quality optimization

---

## 📸 Screenshots

### Main Viewer Interface
```
[Screenshot Placeholder: Neon UI with screen streaming]
- Animated background with floating orbs
- Glassmorphism header with status indicators
- Main screen display area
- Control panel with volume, mute, fullscreen buttons
- Statistics panel showing FPS and quality
- Modern neon color scheme (cyan, purple, pink)
```

### Fullscreen Mode
```
[Screenshot Placeholder: Immersive fullscreen view]
- Clean fullscreen display
- Auto-hiding controls
- Minimal UI distractions
- Statistics panel toggle
- High-quality video rendering
```

---

## 🤝 Contributing

### Areas for Contribution

1. **Platform Support**: Linux/macOS audio capture
2. **Performance**: Hardware encoding, WebRTC implementation
3. **Features**: Multi-monitor, recording, encryption
4. **UI/UX**: Additional themes, mobile optimization
5. **Documentation**: More examples, tutorials, translations

### Development Guidelines

```bash
# Setup development environment
git clone https://github.com/PravakarDas/HostCast.git
cd HostCast/mod2_screenshare
pip install -r ../requirements.txt

# Test your changes
python screenshare_audio.py

# Submit pull request
```

---

## 📄 License

This module is part of HostCast and is licensed under the **MIT License**.

See the root [LICENSE](../LICENSE) file for details.

---

## 👨‍💻 Developer

<div align="center">

### Pravakar Das

[![Portfolio](https://img.shields.io/badge/Portfolio-pdfolio--rho.vercel.app-blue?style=flat-square&logo=vercel)](https://pdfolio-rho.vercel.app/)
[![GitHub](https://img.shields.io/badge/GitHub-PravakarDas-181717?style=flat-square&logo=github)](https://github.com/PravakarDas)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-pravakarda-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/pravakarda)
[![Email](https://img.shields.io/badge/Email-pravakar459@gmail.com-EA4335?style=flat-square&logo=gmail)](mailto:pravakar459@gmail.com)

</div>

---

## 📚 Additional Resources

### Documentation
- [MSS Documentation](https://python-mss.readthedocs.io/)
- [PyAudioWPatch GitHub](https://github.com/s0d3s/PyAudioWPatch)
- [Flask-SocketIO Docs](https://flask-socketio.readthedocs.io/)
- [Web Audio API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

### Related Projects
- [HostCast Main Documentation](../README.md)
- [Module 1: File Sharing](../module1_file_share/README.md)
- [UI Design Notes](./README_UI.md)
- [Modernization Complete](./MODERNIZATION_COMPLETE.md)

### Support
- [GitHub Issues](https://github.com/PravakarDas/HostCast/issues)
- [Email Support](mailto:pravakar459@gmail.com)

---

<div align="center">

**Part of the HostCast Project**

[Back to Main README](../README.md) | [Module 1 Documentation](../module1_file_share/README.md)

*Last Updated: November 2025*

</div>
