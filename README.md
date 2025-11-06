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
2. Install Python dependencies:

    ```pip install -r requirements.txt```
3. Launch the application (example):

    ```python main.py```

>_(Adapt the command according to the actual entry‑point)_
### Usage

1. On the host device, launch the server or application for **HostCast**.  
2. On other devices connected to the same network, open the client (browser or app) and connect to the host’s local IP address and port as prompted.  
3. Through the UI you can:
   - Share files between devices.  
   - Mirror or extend your screen to another device.  
4. For screen extension: select the **“Extend”** mode so the secondary device acts as an extra display (instead of just mirroring).  
5. For file sharing: on one device choose **“Send”**, on the receiving device open **“Receive”**, then follow the UI prompts.

> _Specific UI details, ports, and other options should be found in the source code or the in‑app help guide._
## How it Works

At a high level:

- A server listens on the local network and advertises itself (via broadcast/mDNS or manual IP).  
- Clients connect to the server via WebSocket / HTTP.  
- File transfers occur via chunked upload/download across the local network.  
- Screen capture (on the host) and streaming (to client) uses OS screen‑capture APIs + WebRTC / WebSocket.  
- The “extend screen” mode treats the client device as an additional display, sending the extra region of the host’s desktop to the client.

_(Implementation details may vary. Refer to the source modules for exact behaviour.)_

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
