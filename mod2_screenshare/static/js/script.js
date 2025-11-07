const socket = io();
const canvas = document.getElementById("screenCanvas");
const ctx = canvas.getContext("2d");

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

let streaming = false;
let intervalId = null;

// Request screenshot from server
function requestScreenshot() {
    if (streaming) {
        socket.emit("request_screenshot");
    }
}

// Receive screenshot and draw
socket.on("screenshot", (data) => {
    const img = new Image();
    img.onload = function () {
        // Maintain aspect ratio inside the canvas
        canvas.width = canvas.clientWidth;
        canvas.height = canvas.clientHeight;

        const scale = Math.min(canvas.width / img.width, canvas.height / img.height);
        const x = (canvas.width / 2) - (img.width / 2) * scale;
        const y = (canvas.height / 2) - (img.height / 2) * scale;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
    };
    img.src = `data:image/jpeg;base64,${data.image}`;
});

// Start/Stop streaming
startBtn.addEventListener("click", () => {
    if (!streaming) {
        streaming = true;
        intervalId = setInterval(requestScreenshot, 500); // every 0.5s
        startBtn.disabled = true;
        stopBtn.disabled = false;
    }
});

stopBtn.addEventListener("click", () => {
    streaming = false;
    clearInterval(intervalId);
    startBtn.disabled = false;
    stopBtn.disabled = true;
});
