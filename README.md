# HostCast  
*A lightweight local‑network tool to share files, mirror or extend your screen, and collaborate seamlessly between devices on the same network.*

## Table of Contents  
- [Overview](#overview)  
- [Features](#features)  
- [Getting Started](#getting‑started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
  - [Usage](#usage)  
- [How it Works](#how‑it‑works)  
- [Configuration & Customization](#configuration‑&‑customization)  
- [Project Structure](#project‑structure)  
- [Contributing](#contributing)  
- [License](#license)  
- [Acknowledgements](#acknowledgements)

## Overview  
HostCast is designed to make local‑network collaboration easy. On devices connected to the *same local network* (LAN/WiFi), you can:  
- Share files between devices  
- Mirror or extend your screen to another device  
- Collaborate in real time across devices  

Because everything happens over the local network, it can work even without internet (depending on network setup). The aim is minimal overhead, efficient connectivity, and flexible usage across devices.

## Features  
- **File sharing**: Easily transfer files between devices in the local network.  
- **Screen mirroring / extension**: Mirror or extend your display from one device to another on the same network.  
- **Audio streaming** 🆕: Share system audio from host to all connected clients (Windows supported).
- **Collaboration mode**: Multiple devices can join, share content or screens, enabling collaborative workflows.  
- Cross‑platform (depending on implementation) and lightweight.  
- MIT‑licensed: gives freedom to use, modify and distribute.

## Getting Started  
### Prerequisites  
- Devices connected to the **same local network** (WiFi or LAN).  
- (Depending on the project’s implementation) A modern browser or OS environment supporting web sockets / streaming / screen capture.  
- Python + dependencies (since there is `requirements.txt`).

### Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/PravakarDas/HostCast.git
   cd HostCast
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the application:
   
   **For Screen + Audio Sharing:**
   ```bash
   cd mod2_screenshare
   python ss.py
   ```
   
   **For File Sharing:**
   ```bash
   cd module1_file_share
   python file_server.py
   ```
### Usage

#### Module 1: File Sharing
1. Start the file server:
   ```bash
   cd module1_file_share
   python file_server.py
   ```
2. Access from browser: `http://<host-ip>:8080`
3. Upload and download files between devices

#### Module 2: Screen + Audio Sharing 🆕
1. Start the screen share server:
   ```bash
   cd mod2_screenshare
   python ss.py
   ```
2. Access from any device: `http://<host-ip>:5000`
3. **Click on the page** to enable audio
4. Enjoy live screen and audio streaming!
5. Use controls: volume slider, mute button, fullscreen mode

**Features:**
- 🎥 Real-time screen streaming (~40 FPS)
- 🔊 System audio streaming (Windows WASAPI)
- 🎮 Volume control and mute
- 🖥️ Fullscreen mode
- 📊 Connection status indicators

See `mod2_screenshare/QUICKSTART.md` for detailed instructions.

> _To find your host IP address, run `ipconfig` (Windows) or `ifconfig` (Linux/Mac)_
## How it Works

At a high level:

- A server listens on the local network and advertises itself (via broadcast/mDNS or manual IP).  
- Clients connect to the server via WebSocket / HTTP.  
- File transfers occur via chunked upload/download across the local network.  
- Screen capture (on the host) and streaming (to client) uses OS screen‑capture APIs + WebRTC / WebSocket.  
- **Audio capture** uses Windows WASAPI loopback to stream system audio in real-time.
- Audio and video are transmitted as base64-encoded data via Socket.IO for low latency.
- The "extend screen" mode treats the client device as an additional display, sending the extra region of the host's desktop to the client.

_(Implementation details may vary. Refer to the source modules for exact behaviour.)_

### Architecture

```
┌──────────────────────────────────┐
│   HOST COMPUTER (Windows)        │
│                                  │
│  ┌─────────┐    ┌─────────┐    │
│  │ Screen  │    │  Audio  │    │
│  │Capture  │    │(WASAPI) │    │
│  └────┬────┘    └────┬────┘    │
│       │              │          │
│       └──────┬───────┘          │
│              │                  │
│     ┌────────▼────────┐        │
│     │ Flask+SocketIO  │        │
│     │   Port 5000     │        │
│     └────────┬────────┘        │
└──────────────┼──────────────────┘
               │
    WebSocket (Local Network)
               │
┌──────────────▼──────────────────┐
│   CLIENT DEVICE (Browser)       │
│                                 │
│  ┌──────────┐  ┌─────────────┐ │
│  │  Video   │  │Web Audio API│ │
│  │ Display  │  │  Playback   │ │
│  └──────────┘  └─────────────┘ │
│                                 │
│  Controls: Volume, Mute, etc.  │
└─────────────────────────────────┘
```

## Configuration & Customization

You can customise:

- Ports (change default HTTP/WebSocket ports)  
- Authentication / access control (if needed)  
- UI themes or localisation  
- File transfer limits or chunk‑size thresholds  
- Screen capture quality (resolution / frame rate)  

Look into the configuration files or command‑line arguments in the codebase for options.


## Contributing  
Contributions are very welcome!  

- Please fork the repository, make your feature or bug‑fix, then open a Pull Request.  
- Ensure code style consistency and update documentation accordingly.  
- If adding major new features (e.g., remote internet sharing, multi‑room collaboration), please open an Issue first to discuss design.  
- Report bugs via the Issues tab, including reproduction steps and environment details.  

## License  
This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it, provided you include the original license.  

## Acknowledgements  
- Thanks to the original author, Pravakar Das, for initiating this project.  
- Thanks to open‑source libraries used (see `requirements.txt`).  
- Inspired by other screen‑sharing / mirroring tools and local‑network collaboration platforms.  
