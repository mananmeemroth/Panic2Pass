/**
 * Panic2Pass - Client-Side Controller
 */

let currentPdfText = "";
let currentRawOutput = "";
let isGenerating = false;

document.addEventListener("DOMContentLoaded", () => {
    initCacheStatus();
    initDropzone();
    initNotesTextListener();
});

// 1. Check & Warm up Ollama Model Cache
async function initCacheStatus() {
    const statusPill = document.getElementById("cacheStatusPill");
    const statusText = document.getElementById("cacheStatusText");

    try {
        const res = await fetch("/api/status");
        const data = await res.json();
        if (data.is_cached) {
            statusText.textContent = `🟢 Ollama: ${data.model} (Cached)`;
            statusPill.style.background = "rgba(16, 185, 129, 0.12)";
            statusPill.style.borderColor = "rgba(16, 185, 129, 0.3)";
            statusPill.style.color = "#047857";
        } else {
            statusText.textContent = `⏳ Pre-warming ${data.model}...`;
            // Poll again after 3 seconds
            setTimeout(initCacheStatus, 3000);
        }
    } catch (e) {
        statusText.textContent = "⚠️ Ollama Offline";
        statusPill.style.background = "rgba(239, 68, 68, 0.12)";
        statusPill.style.color = "#dc2626";
    }
}

// 2. Drag & Drop and PDF Extraction
function initDropzone() {
    const dropzone = document.getElementById("pdfDropzone");
    const fileInput = document.getElementById("pdfFileInput");

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.style.borderColor = "#2563eb";
            dropzone.style.background = "rgba(37, 99, 235, 0.05)";
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.style.borderColor = "#cbd5e1";
            dropzone.style.background = "#f8fafc";
        }, false);
    });

    dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
}

async function handleFileUpload(file) {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
        alert("Please upload a valid PDF document.");
        return;
    }

    const headline = document.getElementById("uploadHeadline");
    const subheadline = document.getElementById("uploadSubheadline");
    headline.textContent = `⏳ Parsing "${file.name}"...`;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("/api/parse-pdf", {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        if (data.success) {
            currentPdfText = data.text;
            headline.textContent = `✅ ${file.name}`;
            subheadline.textContent = `Parsed ${data.pages} pages (${data.char_count} characters ready)`;
            updateCharCount(data.char_count);
        } else {
            headline.textContent = "⚠️ Error Reading PDF";
            subheadline.textContent = data.error || "Could not extract text from this PDF.";
        }
    } catch (e) {
        headline.textContent = "⚠️ Upload Failed";
        subheadline.textContent = e.message;
    }
}

// 3. Tab Switching
function switchInputTab(tab) {
    const pdfBtn = document.getElementById("tabPdfBtn");
    const textBtn = document.getElementById("tabTextBtn");
    const pdfContent = document.getElementById("tabPdfContent");
    const textContent = document.getElementById("tabTextContent");

    if (tab === 'pdf') {
        pdfBtn.classList.add("active");
        textBtn.classList.remove("active");
        pdfContent.classList.remove("hidden");
        textContent.classList.add("hidden");
    } else {
        textBtn.classList.add("active");
        pdfBtn.classList.remove("active");
        textContent.classList.remove("hidden");
        pdfContent.classList.add("hidden");
    }
}

function initNotesTextListener() {
    const notesInput = document.getElementById("notesTextInput");
    notesInput.addEventListener("input", () => {
        const len = notesInput.value.length;
        if (!currentPdfText) {
            updateCharCount(len);
        }
    });
}

function updateCharCount(count) {
    document.getElementById("studioWordCount").textContent = `${count} chars loaded`;
}

function setTopic(topic) {
    document.getElementById("weakTopicInput").value = topic;
}

function selectModeAndScroll(modeName) {
    const studio = document.getElementById("studio");
    studio.scrollIntoView({ behavior: 'smooth' });
    triggerPanic(modeName);
}

// 4. Trigger Real-Time Panic Stream
async function triggerPanic(modeName) {
    if (isGenerating) return;

    const notesText = document.getElementById("notesTextInput").value;
    const weakTopic = document.getElementById("weakTopicInput").value;
    const outputDisplay = document.getElementById("outputDisplay");
    const outputDot = document.getElementById("outputDot");
    const outputStatus = document.getElementById("outputStatusLabel");

    const effectiveText = currentPdfText.trim() || notesText.trim();
    if (!effectiveText) {
        alert("⚠️ Please upload a PDF syllabus or paste study notes first!");
        return;
    }

    isGenerating = true;
    currentRawOutput = "";
    outputDot.className = "status-indicator-dot active";
    outputStatus.textContent = `Streaming ${modeName}...`;
    outputDisplay.innerHTML = `<div style="color: #64748b; font-style: italic;">⚡ Contacting cached Ollama engine for ${modeName}...</div>`;

    try {
        const response = await fetch("/api/stream-rescue", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                context: effectiveText,
                weak_topic: weakTopic,
                mode: modeName
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            currentRawOutput += chunk;
            renderMarkdown(currentRawOutput);
            outputDisplay.scrollTop = outputDisplay.scrollHeight;
        }

        outputDot.className = "status-indicator-dot";
        outputStatus.textContent = `✅ Completed ${modeName}`;
    } catch (e) {
        outputDot.className = "status-indicator-dot error";
        outputStatus.textContent = "Error generating plan";
        outputDisplay.innerHTML = `<div style="color: #ef4444; font-weight: 600;">❌ Error: ${e.message}</div>`;
    } finally {
        isGenerating = false;
    }
}

// 5. Markdown Rendering with Highlight.js
function renderMarkdown(rawMd) {
    const outputDisplay = document.getElementById("outputDisplay");
    if (typeof marked !== "undefined") {
        outputDisplay.innerHTML = marked.parse(rawMd);
        outputDisplay.querySelectorAll("pre code").forEach((el) => {
            if (typeof hljs !== "undefined") {
                hljs.highlightElement(el);
            }
        });
    } else {
        outputDisplay.textContent = rawMd;
    }
}

// 6. Action Tools (Copy & Download)
function copyOutput() {
    if (!currentRawOutput.trim()) return;
    navigator.clipboard.writeText(currentRawOutput).then(() => {
        const copyBtn = document.getElementById("copyBtn");
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = "<span>✅ Copied!</span>";
        setTimeout(() => { copyBtn.innerHTML = originalText; }, 2000);
    });
}

function downloadOutput() {
    if (!currentRawOutput.trim()) return;
    const blob = new Blob([currentRawOutput], { type: "text/markdown;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Panic2Pass_Rescue_Plan.md";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function clearOutput() {
    currentRawOutput = "";
    document.getElementById("outputDisplay").innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">⚡</div>
            <h3>Your rescue plan will stream live here.</h3>
            <p>Select your PDF notes on the left and choose a panic action to generate your exam prep strategy instantly.</p>
        </div>
    `;
    document.getElementById("outputStatusLabel").textContent = "Ready to generate";
    document.getElementById("outputDot").className = "status-indicator-dot";
}
