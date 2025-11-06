// Socket.IO
const socket = io();

// Dark/Light mode persistence
const toggle = document.getElementById("theme-toggle");
const savedTheme = localStorage.getItem("theme");
if (savedTheme) {
  document.documentElement.setAttribute("data-theme", savedTheme);
  toggle.textContent = savedTheme === "light" ? "🌙" : "☀️";
}

toggle.addEventListener("click", () => {
  const html = document.documentElement;
  const current = html.getAttribute("data-theme");
  const newTheme = current === "light" ? "dark" : "light";
  html.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme);
  toggle.textContent = newTheme === "light" ? "🌙" : "☀️";
});

// Handle new files
socket.on("new_file", (data) => {
  const tbody = document.querySelector("#file-table tbody");
  const row = document.createElement("tr");
  row.dataset.filename = data.filename;
  row.innerHTML = `
    <td>${data.filename}</td>
    <td>${data.meta.device_name}</td>
    <td>${data.meta.ip}</td>
    <td>${data.meta.size}</td>
    <td>${data.meta.upload_time}</td>
    <td><a href="/preview/${data.filename}" target="_blank">👁️</a></td>
    <td><a href="/download/${data.filename}">⬇️</a></td>
    <td>${data.meta.ip === '{{ request.remote_addr }}' ? `<button class="delete-btn" data-filename="${data.filename}">🗑️Delete</button>` : ''}</td>
  `;
  tbody.prepend(row);
  attachDeleteEvents();
});

// Handle deletion
socket.on("delete_file", (data) => {
  const row = document.querySelector(`tr[data-filename="${data.filename}"]`);
  if (row) row.remove();
});

// Delete button events
function attachDeleteEvents() {
  document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.onclick = async () => {
      const filename = btn.dataset.filename;
      const res = await fetch(`/delete/${filename}`, { method: "POST" });
      const result = await res.json();
      if (result.success) btn.closest("tr").remove();
      else alert(result.error);
    };
  });
}
attachDeleteEvents();

// Table search/filter
const searchBox = document.getElementById("searchBox");
searchBox.addEventListener("input", () => {
  const val = searchBox.value.toLowerCase();
  document.querySelectorAll("#file-table tbody tr").forEach(row => {
    row.style.display = [...row.children].some(td => td.textContent.toLowerCase().includes(val)) ? "" : "none";
  });
});

// Table sorting
document.querySelectorAll("#file-table th[data-column]").forEach(header => {
  header.style.cursor = "pointer";
  header.onclick = () => {
    const table = header.closest("table");
    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));
    const col = header.dataset.column;
    const asc = !header.asc;
    header.asc = asc;

    rows.sort((a, b) => {
      const aText = a.querySelector(`td:nth-child(${header.cellIndex+1})`).textContent;
      const bText = b.querySelector(`td:nth-child(${header.cellIndex+1})`).textContent;
      return asc ? aText.localeCompare(bText) : bText.localeCompare(aText);
    });

    rows.forEach(r => tbody.appendChild(r));
  };
});
// Keep device name persistent
const deviceInput = document.querySelector('input[name="device_name"]');

// Load from localStorage
if(localStorage.getItem("device_name")){
  deviceInput.value = localStorage.getItem("device_name");
}

// Save on change
deviceInput.addEventListener("input", () => {
  localStorage.setItem("device_name", deviceInput.value);
});

const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
// const deviceInput = document.getElementById("deviceNameInput");
const progressContainer = document.getElementById("progressContainer");
const progressBar = document.getElementById("progressBar");
const progressText = document.getElementById("progressText");

uploadForm.addEventListener("submit", (e) => {
  e.preventDefault(); // prevent default form submit

  const file = fileInput.files[0];
  const deviceName = deviceInput.value || "Unknown";

  if (!file) return alert("Select a file!");

  const formData = new FormData();
  formData.append("file", file);
  formData.append("device_name", deviceName);

  const xhr = new XMLHttpRequest();

  xhr.upload.addEventListener("progress", (e) => {
    if (e.lengthComputable) {
      const percent = Math.round((e.loaded / e.total) * 100);
      progressBar.value = percent;
      progressText.textContent = percent + "%";
      progressContainer.style.display = "block";
    }
  });

  xhr.onreadystatechange = () => {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      progressBar.value = 100;
      progressText.textContent = "Upload complete!";
      fileInput.value = ""; // clear input
      setTimeout(() => {
        progressContainer.style.display = "none";
        progressBar.value = 0;
        progressText.textContent = "0%";
      }, 1500);
    }
  };

  xhr.open("POST", "/", true);
  xhr.send(formData);
});
