# 📁 HostCast Module 1: File Sharing Platform

<div align="center">

![Module 1 Banner](https://img.shields.io/badge/Module_1-File_Sharing-success?style=for-the-badge)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![SocketIO](https://img.shields.io/badge/SocketIO-5.3.6-blue?style=flat-square)](https://socket.io/)

**A real-time, web-based file sharing platform for seamless file transfer across devices on your local network.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Technical Details](#-technical-details) • [Troubleshooting](#-troubleshooting)

</div>

---

## 📖 Overview

Module 1 is a lightweight yet powerful file sharing platform that enables effortless file transfer between devices on the same local network. With real-time updates via WebSocket, intuitive search and sort functionality, and secure delete controls, it provides a professional solution for local file collaboration.

### ✨ Key Highlights

- 🚀 **Real-Time Synchronization** - Instant file list updates across all connected devices
- 🔒 **Secure Access Control** - Only uploaders can delete their files
- 📱 **Device Identification** - Track which device uploaded each file
- 👁️ **Universal Preview** - Preview images, videos, PDFs, and text files in-browser
- 🔍 **Advanced Search** - Quickly find files with live search functionality
- 📊 **Smart Sorting** - Sort by filename, size, upload time, or device

---

## 🎁 Features

### Core Functionality

#### 📤 File Upload
- **Simple Interface**: Click or drag-and-drop to upload files
- **Device Naming**: Tag uploads with custom device names
- **Progress Tracking**: Real-time upload progress indicators
- **Multi-Format Support**: Upload any file type without restrictions
- **Automatic Metadata**: Captures upload time, file size, IP address, and device name

#### 📥 File Download
- **One-Click Download**: Direct download from any connected device
- **Original Filename**: Preserves original file names
- **Fast Transfer**: Optimized for LAN speeds

#### 👁️ File Preview
- **In-Browser Viewing**: Preview without downloading
- **Supported Formats**:
  - Images: JPG, PNG, GIF, WebP, SVG
  - Videos: MP4, WebM, OGG
  - Documents: PDF, TXT
  - Audio: MP3, WAV, OGG

#### 🗑️ File Management
- **Secure Delete**: Only the uploader's IP can delete their files
- **Instant Updates**: Deletions sync across all connected devices
- **Metadata Cleanup**: Automatic cleanup of file metadata

#### 🔍 Search & Filter
- **Live Search**: Filter files as you type
- **Multi-Column Sort**: Sort by any column (filename, device, IP, size, time)
- **Ascending/Descending**: Toggle sort order with one click

#### 📊 Metadata Tracking
- **Device Name**: Custom identifier for each upload
- **IP Address**: Track which device uploaded each file
- **Upload Time**: Precise timestamp for each upload
- **File Size**: Display file size in bytes

### Real-Time Features

- **WebSocket Connection**: Bi-directional real-time communication
- **Live File List**: New uploads appear instantly on all devices
- **Delete Notifications**: Removed files disappear in real-time
- **Connection Status**: Visual indicators for connection state

---

## 🚀 Installation

### Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager
- **Network**: LAN or WiFi connection

### Step-by-Step Setup

1. **Navigate to Module Directory**
   ```bash
   cd HostCast/module1_file_share
   ```

2. **Install Dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```
   
   **Core Dependencies:**
   - `Flask==3.0.3` - Web framework
   - `Flask-SocketIO==5.3.6` - Real-time communication
   - `python-socketio==5.11.3` - SocketIO client
   - `python-engineio==4.9.1` - Engine.IO implementation

3. **Verify Installation**
   ```bash
   python -c "import flask, flask_socketio; print('Dependencies installed successfully!')"
   ```

---

## 📱 Usage

### Starting the Server

1. **Run the Server**
   ```bash
   python file_server.py
   ```

2. **Expected Output**
   ```
   * Serving Flask app 'file_server'
   * Debug mode: on
   WARNING: This is a development server. Do not use it in a production deployment.
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:8080
   * Running on http://192.168.1.x:8080
   ```

3. **Find Your IP Address**
   ```powershell
   ipconfig
   ```
   Look for `IPv4 Address` under your active network adapter.

### Accessing the Interface

**From Host Machine:**
```
http://localhost:8080
```

**From Other Devices (same network):**
```
http://<host-ip>:8080
```
Example: `http://192.168.1.100:8080`

### Using the Platform

#### Uploading Files

1. **Enter Device Name**: Type a recognizable name for your device
2. **Select File**: Click "Choose File" or drag-and-drop
3. **Upload**: Click "Upload File" button
4. **Confirmation**: File appears in the list instantly

#### Downloading Files

1. **Locate File**: Use search or scroll through the list
2. **Click Download Icon**: Click ⬇️ icon in the Download column
3. **Save**: File downloads to your default downloads folder

#### Previewing Files

1. **Click Preview Icon**: Click 👁️ icon in the Preview column
2. **View in Browser**: File opens in a new tab
3. **Close Tab**: Close when done viewing

#### Deleting Files

> ⚠️ **Note**: Only the device that uploaded a file can delete it

1. **Find Your Upload**: Look for files with your IP address
2. **Click Delete Icon**: Click 🗑️ icon in the Delete column
3. **Confirmation**: File is deleted instantly from all devices

#### Searching Files

1. **Use Search Box**: Type filename, device name, or IP
2. **Live Filtering**: Results update as you type
3. **Clear Search**: Delete search text to show all files

#### Sorting Files

1. **Click Column Header**: Click any column name (Filename, Device, Size, etc.)
2. **Toggle Sort**: Click again to reverse sort order
3. **Visual Indicator**: Arrow shows current sort column and direction

---

## 🛠️ Technical Details

### Architecture

```
┌─────────────────────────────────────────┐
│         Flask Application               │
│                                         │
│  ┌──────────────┐  ┌─────────────────┐ │
│  │   Routes     │  │  SocketIO Events│ │
│  │              │  │                 │ │
│  │ • /          │  │ • connect       │ │
│  │ • /download  │  │ • new_file      │ │
│  │ • /preview   │  │ • delete_file   │ │
│  │ • /delete    │  │                 │ │
│  └──────────────┘  └─────────────────┘ │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │     File Storage Layer          │   │
│  │                                 │   │
│  │  uploads/                       │   │
│  │  ├── file1.jpg                  │   │
│  │  ├── file2.pdf                  │   │
│  │  └── metadata.json              │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
                    │
           WebSocket (Port 8080)
                    │
┌───────────────────┴──────────────────────┐
│                                          │
│  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ Client 1 │  │ Client 2 │  │Client 3│ │
│  │ Browser  │  │ Browser  │  │Browser │ │
│  └──────────┘  └──────────┘  └────────┘ │
└──────────────────────────────────────────┘
```

### File Structure

```
module1_file_share/
├── file_server.py          # Main Flask application
├── static/                 # Frontend assets
│   ├── css/
│   │   └── style.css      # Styling
│   └── js/
│       └── script.js      # Client-side logic
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   └── index.html         # Main interface
└── uploads/                # File storage (auto-created)
    └── metadata.json      # File metadata database
```

### Backend Components

#### Flask Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET, POST | Main page & file upload handler |
| `/download/<filename>` | GET | File download endpoint |
| `/preview/<filename>` | GET | File preview endpoint |
| `/delete/<filename>` | POST | File deletion endpoint |

#### SocketIO Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Client → Server | New client connection |
| `connected` | Server → Client | Connection confirmation |
| `new_file` | Server → All Clients | New file uploaded notification |
| `delete_file` | Server → All Clients | File deleted notification |

#### Metadata Schema

```json
{
  "example.jpg": {
    "device_name": "My Laptop",
    "ip": "192.168.1.100",
    "upload_time": "2025-11-08 14:30:45",
    "size": 1048576
  }
}
```

### Frontend Components

#### JavaScript Functionality

- **WebSocket Client**: Real-time communication via Socket.IO
- **Event Handlers**: Upload, delete, search, sort interactions
- **Dynamic Updates**: Live DOM manipulation for file list
- **AJAX Requests**: Asynchronous file operations

#### CSS Features

- **Responsive Design**: Mobile, tablet, and desktop layouts
- **Table Styling**: Clean, modern file list presentation
- **Interactive Elements**: Hover effects, button styles
- **Loading States**: Visual feedback during operations

---

## 🔧 Configuration

### Port Configuration

**Default Port**: 8080

To change the port, edit `file_server.py`:

```python
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)  # Change port here
```

### Upload Folder

**Default Location**: `./uploads`

To change the upload directory:

```python
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Change 'uploads' to your desired folder
```

### CORS Settings

**Default**: All origins allowed (`*`)

To restrict origins:

```python
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
# Change "*" to specific origins like ["http://192.168.1.100:8080"]
```

---

## 🐛 Known Issues & Limitations

### Current Limitations

1. **Large File Uploads**
   - **Issue**: Files over 1GB may cause timeouts or memory issues
   - **Workaround**: Use smaller files or increase server timeout
   - **Status**: 🔴 Known limitation

2. **Concurrent Upload Performance**
   - **Issue**: Multiple simultaneous uploads may slow down the interface
   - **Impact**: UI may lag with 5+ concurrent uploads
   - **Status**: 🔴 Known issue

3. **Browser File Preview Limits**
   - **Issue**: Large videos or PDFs may not preview in all browsers
   - **Workaround**: Download file instead of previewing
   - **Status**: 🟡 Browser-dependent

4. **No User Authentication**
   - **Issue**: Anyone on the network can access and upload files
   - **Impact**: Security concern for public networks
   - **Status**: 🔴 Feature not implemented

5. **Storage Management**
   - **Issue**: No automatic cleanup of old files
   - **Workaround**: Manually delete files from `uploads/` folder
   - **Status**: 🔴 Feature not implemented

6. **Delete Permission Check**
   - **Issue**: IP-based deletion can be spoofed
   - **Impact**: Security concern in untrusted networks
   - **Status**: 🟡 Basic protection only

### Browser Compatibility

| Browser | Upload | Download | Preview | WebSocket | Status |
|---------|--------|----------|---------|-----------|--------|
| Chrome 90+ | ✅ | ✅ | ✅ | ✅ | Fully supported |
| Firefox 88+ | ✅ | ✅ | ✅ | ✅ | Fully supported |
| Edge 90+ | ✅ | ✅ | ✅ | ✅ | Fully supported |
| Safari 14+ | ✅ | ✅ | ⚠️ | ✅ | Preview limited |
| Mobile Chrome | ✅ | ✅ | ⚠️ | ✅ | Preview limited |
| Mobile Safari | ✅ | ✅ | ⚠️ | ✅ | Preview limited |

---

## 🔧 Troubleshooting

### Server Issues

#### Server Won't Start

**Error**: `Address already in use`

**Solution**:
```powershell
# Find process using port 8080
netstat -ano | findstr :8080

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
pip install -r ../requirements.txt
```

#### Cannot Access from Other Devices

**Check 1**: Firewall settings
```powershell
# Add firewall rule for Python
netsh advfirewall firewall add rule name="Python File Server" dir=in action=allow protocol=TCP localport=8080
```

**Check 2**: Network connectivity
```powershell
# Verify devices can ping each other
ping <device-ip>
```

**Check 3**: IP address
```powershell
# Verify correct IP address
ipconfig
# Use the IPv4 Address from your active network adapter
```

### Upload Issues

#### Upload Fails Silently

**Possible Causes**:
1. File too large (check available disk space)
2. No write permissions to `uploads/` folder
3. Network timeout

**Solutions**:
```powershell
# Check disk space
Get-PSDrive C | Select-Object Used,Free

# Check folder permissions
icacls uploads
```

#### Upload Progress Not Showing

**Cause**: JavaScript error or browser compatibility

**Solution**:
1. Open browser console (F12)
2. Check for JavaScript errors
3. Try different browser
4. Clear browser cache

### Download Issues

#### Download Not Starting

**Solution**:
1. Check browser download settings
2. Verify file still exists on server
3. Try preview first, then right-click → Save As

#### Downloaded File Corrupted

**Cause**: Network interruption during transfer

**Solution**:
1. Delete corrupted file
2. Re-download from server
3. Check network stability

### Preview Issues

#### Preview Not Loading

**Solutions**:
1. Check file format compatibility
2. Try downloading instead
3. Verify file isn't corrupted
4. Check browser console for errors

#### Video/PDF Preview Freezes Browser

**Cause**: File too large for in-browser rendering

**Solution**:
1. Download file instead of previewing
2. Use external viewer application

### WebSocket Issues

#### Real-Time Updates Not Working

**Check 1**: WebSocket connection
```javascript
// Open browser console (F12) and check for:
// "Client connected" message
```

**Check 2**: Firewall/proxy blocking WebSocket

**Solution**:
1. Check firewall settings
2. Try disabling VPN
3. Verify network allows WebSocket connections

#### Multiple Connections from Same Device

**Cause**: Browser tabs not properly disconnecting

**Solution**:
1. Close all tabs
2. Clear browser cache
3. Restart browser

---

## 📊 Performance Tips

### Optimizing Upload Speed

1. **Use Wired Connection**: Ethernet provides more stable transfer
2. **Close Unnecessary Apps**: Free up bandwidth
3. **Upload During Off-Peak**: Less network congestion
4. **Compress Large Files**: Reduce file size before uploading

### Server Optimization

1. **Increase Upload Limit** (if needed):
   ```python
   app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB limit
   ```

2. **Use Production Server** (for heavy use):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8080 file_server:app
   ```

---

## 🔮 Future Enhancements

### Planned Features

- [ ] User authentication system
- [ ] File organization with folders
- [ ] Bulk file operations (multi-select, bulk download)
- [ ] File compression/decompression
- [ ] Upload resume capability
- [ ] Advanced file search (by type, date range, size)
- [ ] Storage quota management
- [ ] Thumbnail generation for images/videos
- [ ] File sharing links with expiration
- [ ] Activity logging and audit trail

---

## 📸 Screenshots

### Main Interface
```
[Screenshot Placeholder: Upload interface with file list table]
- File upload form with device name input
- File selection button
- Upload progress bar
```

### File List with Actions
```
[Screenshot Placeholder: File list with search and actions]
- Search bar at the top
- Sortable columns (Filename, Device, IP, Size, Time)
- Action buttons (Preview, Download, Delete)
- Real-time file list updates
```

---

## 🤝 Contributing

Found a bug or have a feature request? Contributions are welcome!

### Reporting Issues

1. Check existing issues first
2. Provide detailed description
3. Include error messages/screenshots
4. Specify your environment (OS, Python version, browser)

### Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

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

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [Socket.IO Client API](https://socket.io/docs/v4/client-api/)
- [HostCast Main Documentation](../README.md)

---

<div align="center">

**Part of the HostCast Project**

[Back to Main README](../README.md) | [Module 2 Documentation](../mod2_screenshare/README.md)

*Last Updated: November 2025*

</div>
