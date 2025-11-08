/**
 * HostCast - Modern Screen Share Client
 * Professional WebSocket-based screen sharing with audio support
 */

class HostCastClient {
    constructor() {
        // DOM Elements
        this.screenElement = document.getElementById("screen");
        this.loadingState = document.getElementById("loading-state");
        this.connectionStatus = document.getElementById("connection-status");
        this.streamStatus = document.getElementById("stream-status");
        this.fpsValue = document.getElementById("fps-value");
        
        // Stats elements
        this.statVideoFrames = document.getElementById("stat-video-frames");
        this.statAudioPackets = document.getElementById("stat-audio-packets");
        this.statLatency = document.getElementById("stat-latency");
        this.statDataRate = document.getElementById("stat-data-rate");
        
        // State
        this.videoFrameCount = 0;
        this.audioPacketCount = 0;
        this.lastFrameTime = 0;
        this.fps = 0;
        this.fpsFrames = 0;
        this.fpsLastTime = Date.now();
        this.totalDataReceived = 0;
        this.lastDataRateUpdate = Date.now();
        this.audioContext = null;
        this.isPlaying = true;
        
        // Audio buffering for smooth playback
        this.audioQueue = [];
        this.nextPlayTime = 0;
        this.isProcessingAudio = false;
        
        // Initialize
        this.initSocket();
        this.initControls();
        this.startFPSCounter();
        this.startDataRateMonitor();
    }

    initSocket() {
        console.log("Initializing HostCast connection...");
        
        this.socket = io({
            transports: ["websocket", "polling"],
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionAttempts: 10,
            timeout: 20000
        });

        this.socket.on("connect", () => this.onConnect());
        this.socket.on("disconnect", () => this.onDisconnect());
        this.socket.on("connect_error", (error) => this.onConnectionError(error));
        this.socket.on("frame", (data) => this.onFrame(data));
        this.socket.on("audio", (data) => this.onAudio(data));
    }

    onConnect() {
        console.log("Connected to HostCast server");
        this.updateConnectionStatus("connected", "Connected");
        
        // Initialize audio context on user interaction (required by browsers)
        document.addEventListener('click', () => {
            if (!this.audioContext) {
                this.initAudioContext();
            }
        }, { once: true });
    }

    onDisconnect() {
        console.log("Disconnected from server");
        this.updateConnectionStatus("disconnected", "Disconnected");
        this.updateStreamStatus("Reconnecting...", "#fbbf24");
    }

    onConnectionError(error) {
        console.error("Connection error:", error);
        this.updateConnectionStatus("disconnected", "Connection Error");
    }

    onFrame(data) {
        const now = performance.now();
        
        this.screenElement.src = "data:image/jpeg;base64," + data;
        this.screenElement.classList.add("active");
        
        if (this.videoFrameCount === 0) {
            this.loadingState.classList.add("hidden");
            this.updateStreamStatus("Streaming", "#10b981");
            console.log("Stream started");
        }
        
        this.videoFrameCount++;
        this.fpsFrames++;
        this.totalDataReceived += data.length;
        
        if (this.statVideoFrames) {
            this.statVideoFrames.textContent = this.formatNumber(this.videoFrameCount);
        }
        
        if (this.lastFrameTime > 0) {
            const latency = Math.round(now - this.lastFrameTime);
            if (this.statLatency) {
                this.statLatency.textContent = latency + " ms";
            }
        }
        this.lastFrameTime = now;
    }

    onAudio(audioData) {
        if (!this.isPlaying) return;
        
        this.audioPacketCount++;
        this.totalDataReceived += audioData.data.length;
        
        if (this.statAudioPackets) {
            this.statAudioPackets.textContent = this.formatNumber(this.audioPacketCount);
        }
        
        // Initialize audio context if needed
        if (!this.audioContext) {
            this.initAudioContext();
        }
        
        // Always try to resume if suspended
        if (this.audioContext && this.audioContext.state === "suspended") {
            this.audioContext.resume();
        }
        
        // Add to queue for scheduled playback
        if (this.audioContext && this.audioContext.state === "running") {
            this.audioQueue.push(audioData);
            
            // Start processing queue if not already running
            if (!this.isProcessingAudio) {
                this.processAudioQueue();
            }
        } else if (this.audioPacketCount === 1) {
            console.warn("Audio context not running. Click anywhere to enable audio.");
        }
    }

    initAudioContext() {
        if (this.audioContext) return;
        
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.nextPlayTime = this.audioContext.currentTime;
            console.log("Audio context initialized - State:", this.audioContext.state);
            
            // Force resume if suspended
            if (this.audioContext.state === "suspended") {
                this.audioContext.resume().then(() => {
                    console.log("Audio context resumed");
                });
            }
        } catch (error) {
            console.error("Failed to initialize audio:", error);
        }
    }

    processAudioQueue() {
        if (this.audioQueue.length === 0) {
            this.isProcessingAudio = false;
            return;
        }
        
        this.isProcessingAudio = true;
        const audioData = this.audioQueue.shift();
        
        try {
            // Decode base64 to binary
            const binaryString = atob(audioData.data);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }
            
            // Convert Int16 to Float32
            const int16Array = new Int16Array(bytes.buffer);
            const float32Array = new Float32Array(int16Array.length);
            for (let i = 0; i < int16Array.length; i++) {
                float32Array[i] = int16Array[i] / 32768.0;
            }
            
            // Create audio buffer
            const numFrames = float32Array.length / audioData.channels;
            const audioBuffer = this.audioContext.createBuffer(
                audioData.channels,
                numFrames,
                audioData.rate
            );
            
            // Fill audio buffer (interleaved to planar)
            for (let channel = 0; channel < audioData.channels; channel++) {
                const channelData = audioBuffer.getChannelData(channel);
                for (let i = 0; i < numFrames; i++) {
                    channelData[i] = float32Array[i * audioData.channels + channel];
                }
            }
            
            // Calculate when to play this chunk
            const currentTime = this.audioContext.currentTime;
            
            // If we're behind, catch up
            if (this.nextPlayTime < currentTime) {
                this.nextPlayTime = currentTime;
            }
            
            // Schedule playback
            const source = this.audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(this.audioContext.destination);
            source.start(this.nextPlayTime);
            
            // Update next play time
            const chunkDuration = audioBuffer.duration;
            this.nextPlayTime += chunkDuration;
            
            // Schedule next chunk
            source.onended = () => {
                this.processAudioQueue();
            };
            
        } catch (error) {
            if (this.audioPacketCount < 5) {
                console.warn("Audio playback error:", error);
            }
            // Continue processing queue even on error
            setTimeout(() => this.processAudioQueue(), 10);
        }
    }

    updateConnectionStatus(status, text) {
        const statusDot = this.connectionStatus.querySelector(".status-dot");
        const statusText = this.connectionStatus.querySelector(".status-text");
        
        statusDot.className = "status-dot";
        
        if (status === "connected") {
            statusDot.classList.add("status-connected");
            statusText.textContent = text;
        } else if (status === "disconnected") {
            statusDot.classList.add("status-disconnected");
            statusText.textContent = text;
        } else {
            statusDot.classList.add("status-connecting");
            statusText.textContent = text;
        }
    }

    updateStreamStatus(text, color = null) {
        const statusText = this.streamStatus.querySelector(".status-text");
        statusText.textContent = text;
        if (color) {
            statusText.style.color = color;
        }
    }

    startFPSCounter() {
        setInterval(() => {
            const now = Date.now();
            const elapsed = now - this.fpsLastTime;
            
            if (elapsed >= 1000) {
                this.fps = Math.round((this.fpsFrames * 1000) / elapsed);
                this.fpsValue.textContent = this.fps;
                this.fpsFrames = 0;
                this.fpsLastTime = now;
            }
        }, 100);
    }

    startDataRateMonitor() {
        setInterval(() => {
            const now = Date.now();
            const elapsed = now - this.lastDataRateUpdate;
            
            if (elapsed >= 1000 && this.statDataRate) {
                const bytesPerSecond = (this.totalDataReceived * 1000) / elapsed;
                const kbPerSecond = bytesPerSecond / 1024;
                this.statDataRate.textContent = kbPerSecond.toFixed(1) + " KB/s";
                this.totalDataReceived = 0;
                this.lastDataRateUpdate = now;
            }
        }, 1000);
    }

    initControls() {
        const btnPlay = document.getElementById("btn-play");
        if (btnPlay) {
            btnPlay.addEventListener("click", () => {
                this.isPlaying = !this.isPlaying;
                const path = btnPlay.querySelector("path");
                if (this.isPlaying) {
                    path.setAttribute("d", "M6 4L14 10L6 16V4Z");
                    btnPlay.setAttribute("data-tooltip", "Pause");
                } else {
                    path.setAttribute("d", "M6 4H8V16H6V4Z M12 4H14V16H12V4Z");
                    btnPlay.setAttribute("data-tooltip", "Play");
                }
                console.log(this.isPlaying ? "Playback resumed" : "Playback paused");
            });
        }

        const btnVolume = document.getElementById("btn-volume");
        if (btnVolume) {
            btnVolume.addEventListener("click", () => {
                if (this.audioContext) {
                    if (this.audioContext.state === "suspended") {
                        this.audioContext.resume();
                        console.log("Audio unmuted");
                    } else {
                        this.audioContext.suspend();
                        console.log("Audio muted");
                    }
                } else {
                    this.initAudioContext();
                }
            });
        }

        const btnFullscreen = document.getElementById("btn-fullscreen");
        if (btnFullscreen) {
            btnFullscreen.addEventListener("click", () => {
                const screenContainer = document.getElementById("screen-container");
                
                if (!document.fullscreenElement) {
                    // Enter fullscreen on the screen container only
                    if (screenContainer.requestFullscreen) {
                        screenContainer.requestFullscreen();
                    } else if (screenContainer.webkitRequestFullscreen) {
                        screenContainer.webkitRequestFullscreen();
                    } else if (screenContainer.msRequestFullscreen) {
                        screenContainer.msRequestFullscreen();
                    }
                    console.log("Entered fullscreen");
                } else {
                    // Exit fullscreen
                    if (document.exitFullscreen) {
                        document.exitFullscreen();
                    } else if (document.webkitExitFullscreen) {
                        document.webkitExitFullscreen();
                    } else if (document.msExitFullscreen) {
                        document.msExitFullscreen();
                    }
                    console.log("Exited fullscreen");
                }
            });
        }

        const btnSettings = document.getElementById("btn-settings");
        if (btnSettings) {
            btnSettings.addEventListener("click", () => {
                console.log("Settings clicked");
                alert("Settings panel coming soon!");
            });
        }

        const btnShare = document.getElementById("btn-share");
        if (btnShare) {
            btnShare.addEventListener("click", () => {
                const url = window.location.href;
                if (navigator.share) {
                    navigator.share({
                        title: "HostCast Stream",
                        text: "Join my screen share session",
                        url: url
                    });
                } else {
                    navigator.clipboard.writeText(url);
                    alert("Stream URL copied to clipboard!");
                }
                console.log("Share clicked");
            });
        }

        const statsToggle = document.getElementById("stats-toggle");
        const statsContent = document.getElementById("stats-content");
        if (statsToggle && statsContent) {
            let statsVisible = true;
            statsToggle.addEventListener("click", () => {
                statsVisible = !statsVisible;
                statsContent.style.display = statsVisible ? "flex" : "none";
            });
        }
    }

    formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
        window.hostcast = new HostCastClient();
    });
} else {
    window.hostcast = new HostCastClient();
}

console.log("%cHostCast v2.0", "color: #00f2ff; font-size: 20px; font-weight: bold;");
console.log("%cModern Screen Sharing Platform", "color: #7b2ff7; font-size: 12px;");
