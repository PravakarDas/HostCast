# 🎯 HostCast

<div align="center">

![HostCast Banner](https://img.shields.io/badge/HostCast-Local_Network_Toolkit-blueviolet?style=for-the-badge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)

**A powerful, lightweight local-network solution for seamless file sharing and real-time screen mirroring with audio streaming across multiple devices.**

[Features](#-features) • [Quick Start](#-quick-start) • [Modules](#-modules) • [Documentation](#-documentation) • [Contact](#-contact)

</div>

---

## 📖 Overview

**HostCast** is a comprehensive local network collaboration tool designed for Windows environments that enables effortless file sharing and real-time screen mirroring with synchronized audio streaming. Built with Flask and SocketIO, HostCast provides a professional, web-based interface accessible from any device on your LAN - perfect for presentations, remote assistance, media sharing, and collaborative work environments.

### ✨ What Makes HostCast Special?

- 🌐 **No Internet Required** - Works entirely on your local network (LAN/WiFi)
- 🚀 **Real-Time Performance** - 15+ FPS screen streaming with synchronized audio
- 💻 **Cross-Device Compatible** - Access from any device with a web browser
- 🎨 **Modern UI/UX** - Professional neon-themed glassmorphism design
- 🔒 **Privacy First** - All data stays on your local network
- ⚡ **Lightweight** - Minimal resource usage with efficient streaming algorithms

---

## 🎁 Features

### 🗂️ Module 1: File Sharing Platform
- 📊 **Real-Time Updates** - Live file list updates via WebSocket
- 🔍 **Search & Sort** - Quickly find files with search and sortable columns
- 👁️ **File Preview** - In-browser preview for images, videos, PDFs, and more
- 📥 **One-Click Download** - Fast file downloads to any connected device
- 🗑️ **Delete Control** - Only uploaders can delete their own files
- 📱 **Device Tracking** - See which device uploaded each file
- 📈 **Metadata Management** - Track upload time, file size, and IP addresses

### 🖥️ Module 2: Screen Mirroring & Audio Streaming
- 🎥 **Real-Time Screen Capture** - Smooth 15+ FPS screen streaming with adaptive resolution
- 🔊 **System Audio Streaming** - Synchronized audio via Windows WASAPI loopback
- 🎛️ **Interactive Controls** - Volume control, mute, play/pause, fullscreen mode
- 📊 **Live Statistics** - FPS counter, quality indicators, bandwidth monitoring
- 🌈 **Modern UI** - Neon-themed design with glassmorphism effects
- 🔄 **Auto-Reconnect** - Intelligent connection management with automatic recovery
- 📱 **Multi-Client Support** - Multiple devices can view simultaneously
- ⚙️ **Smart Buffering** - Optimized audio chunks for smooth playback

---

## 🚀 Quick Start

### Prerequisites

- **Operating System**: Windows 10/11 (for screen sharing audio features)
- **Python**: Version 3.9 or higher and Version 3.12 or lower
- **Network**: All devices connected to the same LAN/WiFi
- **Browser**: Modern browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/PravakarDas/HostCast.git
   cd HostCast
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Find Your Host IP Address**
   ```bash
   ipconfig  # Windows
   ```
   Look for `IPv4 Address` under your active network adapter (e.g., `192.168.1.x`)

### Running Module 1: File Sharing

```bash
cd module1_file_share
python file_server.py
```

🌐 **Access from any device**: `http://<host-ip>:8080`

### Running Module 2: Screen Mirroring

```bash
cd mod2_screenshare
python screenshare_audio.py
```

🌐 **Access from any device**: `http://<host-ip>:5000`

> 💡 **Tip**: Click anywhere on the viewing page to enable audio playback (browser requirement)

---

## 📦 Modules

### 📁 Module 1: File Sharing Platform

A sophisticated file sharing system with real-time synchronization and intuitive web interface.

**Key Features:**
- WebSocket-based live updates
- Device identification and IP tracking
- Secure delete permissions (only uploader can delete)
- File preview for multiple formats
- Search and sort capabilities

**Technology Stack:**
- Flask (Web Framework)
- Flask-SocketIO (Real-time Communication)
- HTML/CSS/JavaScript (Frontend)

[📘 View Module 1 Documentation](./module1_file_share/README.md)

**Screenshots Placeholder:**
```
[Screenshot 1: File Upload Interface]
[Screenshot 2: File List with Search and Preview]
```

---

### 🖥️ Module 2: Screen Mirroring & Audio Streaming

Professional-grade screen mirroring solution with synchronized audio streaming and modern UI.

**Key Features:**
- MSS-based screen capture (30+ FPS)
- PyAudioWPatch WASAPI audio capture
- Adaptive video compression (JPEG, quality 70%)
- Professional neon-themed UI
- Real-time performance metrics

**Technology Stack:**
- Flask + Flask-SocketIO (Backend)
- MSS (Screen Capture)
- PyAudioWPatch (Audio Capture)
- PIL/Pillow (Image Processing)
- Modern JavaScript ES6 (Frontend)

[📘 View Module 2 Documentation](./mod2_screenshare/README.md)

**Screenshots Placeholder:**
```
[Screenshot 1: Screen Mirroring Interface with Controls]
[Screenshot 2: Fullscreen Mode with Stats Panel]
```

---

## 📚 Documentation

### Project Structure

```
HostCast/
├── module1_file_share/          # File sharing module
│   ├── file_server.py           # Flask server with SocketIO
│   ├── static/                  # CSS and JavaScript assets
│   │   ├── css/style.css
│   │   └── js/script.js
│   ├── templates/               # HTML templates
│   │   ├── base.html
│   │   └── index.html
│   ├── uploads/                 # File storage directory
│   │   └── metadata.json        # File metadata database
│   └── README.md                # Module documentation
│
├── mod2_screenshare/            # Screen mirroring module
│   ├── screenshare_audio.py     # Main server application
│   ├── static/                  # Frontend assets
│   │   ├── css/style.css        # Modern UI styles
│   │   └── js/script.js         # WebSocket client
│   ├── templates/
│   │   └── index.html           # Viewer interface
│   ├── MODERNIZATION_COMPLETE.md
│   ├── README_UI.md
│   └── README.md                # Module documentation
│
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
└── README.md                    # This file
```

### System Requirements

**Module 1 (File Sharing):**
- Python 3.9+
- Flask 3.0.3
- Flask-SocketIO 5.3.6
- Any modern web browser

**Module 2 (Screen Mirroring):**
- Windows 10/11 (for audio capture)
- Python 3.8+
- All Module 1 requirements plus:
  - MSS 9.0.1 (Screen capture)
  - Pillow 11.0.0 (Image processing)
  - PyAudioWPatch 0.2.12.5+ (Audio capture)
  - NumPy 1.26.4 (Array processing)

---

## 🐛 Known Issues & Limitations

### Module 1: File Sharing
- ⚠️ **Large File Performance**: Files over 1GB may take time to upload (dependent on network speed)
- ⚠️ **Concurrent Uploads**: Multiple simultaneous uploads may cause UI lag
- ⚠️ **Browser Limits**: Some browsers limit file preview size (e.g., video files)

### Module 2: Screen Mirroring
- ⚠️ **Windows Only Audio**: Audio streaming requires Windows WASAPI (pyaudiowpatch)
- ⚠️ **Network Bandwidth**: Requires stable LAN connection (recommended: 10+ Mbps)
- ⚠️ **Browser Autoplay**: Audio requires user interaction (click/tap) to start (browser security)
- ⚠️ **Multi-Monitor**: Currently captures primary monitor only
- ⚠️ **Latency**: Typical latency 100-300ms (dependent on network and hardware)

### General
- 🔧 **Network Firewall**: May require firewall exceptions for ports 5000 and 8080
- 🔧 **Same Network Required**: All devices must be on the same LAN/WiFi network

---

## 🔧 Troubleshooting

### Cannot Access from Other Devices?
1. Check firewall settings - allow Python through Windows Firewall
2. Ensure all devices are on the same network
3. Verify the correct IP address (use `ipconfig`)
4. Try accessing from host machine first (`http://localhost:8080` or `:5000`)

### No Audio in Screen Mirroring?
1. Click anywhere on the viewer page (browser requires user interaction)
2. Check system audio is playing on host
3. Verify pyaudiowpatch is installed correctly
4. Ensure Windows audio output device is enabled

### Screen Not Updating?
1. Check browser console for errors (F12)
2. Refresh the page
3. Verify host server is running without errors
4. Check network stability

### File Upload Fails?
1. Check available disk space on host
2. Verify write permissions in `uploads/` folder
3. Try smaller files first
4. Check browser console for errors

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs** - Open an issue with detailed description
2. **Suggest Features** - Share your ideas for improvements
3. **Submit Pull Requests** - Fix bugs or add features
4. **Improve Documentation** - Help make docs clearer

### Development Setup

```bash
# Clone and setup
git clone https://github.com/PravakarDas/HostCast.git
cd HostCast
pip install -r requirements.txt

# Create a new branch
git checkout -b feature/your-feature-name

# Make changes and test
# Submit pull request
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR**: You are free to use, modify, and distribute this software for personal or commercial purposes.

---

## 👨‍💻 Contact & Support

<div align="center">

### Pravakar Das

[![Portfolio](https://img.shields.io/badge/Portfolio-pdfolio--rho.vercel.app-blue?style=for-the-badge&logo=vercel)](https://pdfolio-rho.vercel.app/)
[![GitHub](https://img.shields.io/badge/GitHub-PravakarDas-181717?style=for-the-badge&logo=github)](https://github.com/PravakarDas)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-pravakarda-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/pravakarda)
[![Email](https://img.shields.io/badge/Email-pravakar459@gmail.com-EA4335?style=for-the-badge&logo=gmail)](mailto:pravakar459@gmail.com)

**Found this useful? Give it a ⭐ on GitHub!**

</div>

---

## 🙏 Acknowledgements

- **Flask Team** - For the excellent web framework
- **MSS** - For efficient screen capture capabilities
- **PyAudioWPatch** - For Windows audio loopback support
- **Open Source Community** - For inspiration and resources

---

<div align="center">

**Made with ❤️ by Pravakar Das**

*Last Updated: November 2025*

</div>
