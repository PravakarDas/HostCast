// Socket.io setup
const socket = io();
const img = document.getElementById("screen");
let lastFrame = 0;

// Receive frames
socket.on("frame", (data) => {
  const now = Date.now();
  if (now - lastFrame > 25) { // limit ~40 FPS
    img.src = "data:image/jpeg;base64," + data;
    lastFrame = now;
  }
});

// Fullscreen button
const btnFullscreen = document.getElementById("btn-fullscreen");
btnFullscreen.addEventListener("click", () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
});

// Stop button (just for demo)
const btnStop = document.getElementById("btn-stop");
btnStop.addEventListener("click", () => {
  img.src = ""; // clear screen
});
