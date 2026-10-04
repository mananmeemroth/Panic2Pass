# 🚨 Panic2Pass - The Pre-Exam Emergency AI Cramming Engine

> **Turn chaotic PDFs, lecture slides, and confusing syllabi into high-yield 30-minute exam triage plans in seconds.**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20(Llama%203.2)-blueviolet.svg)](https://ollama.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Overview

**Panic2Pass** is built for students facing last-minute exam pressure. It takes your uploaded syllabus or lecture notes and synthesizes laser-focused exam rescue materials.

### 🎯 Emergency Rescue Modes

1. ⚡ **30-Min Crash Plan**: Strict triage breakdown (10 mins for formulas/definitions, 15 mins for core mechanisms, 5 mins for hall-door memory checklist).
2. 🆘 **I'm Lost (ELI5 Concept Clarifier)**: De-jargonizes complex topics with intuitive real-world analogies, step-by-step logic, and common misconceptions.
3. 📝 **Quiz Me (High-Yield Active Recall)**: Simulates 3 high-probability exam questions with scoring criteria and hidden model answers.
4. 📋 **Rapid Cheat Sheet**: Dense markdown matrix of definitions, algorithm steps, and trap checklists.

---

## 🚀 Quickstart (Local Development)

### 1. Ensure Ollama is Running
```bash
ollama serve
ollama pull llama3.2:3b
```

### 2. Install Dependencies & Run
```bash
pip install -r requirements.txt
python app.py
```
Open **http://localhost:7860** in your browser.

---

## ☁️ Deploying to Render (Step-by-Step)

You can deploy Panic2Pass to **[Render](https://render.com)** in 2 minutes:

### Step 1: Create a Free Groq API Key (Recommended for Cloud)
Render is a cloud container and does not run local Ollama by default. Getting a free Groq API key allows your Render deployment to run ultra-fast Llama 3.3 for free:
- Go to [console.groq.com](https://console.groq.com) and create a free key (starts with `gsk_...`).

### Step 2: Deploy on Render
1. Go to your [Render Dashboard](https://dashboard.render.com/) and click **New + > Web Service**.
2. Connect your GitHub repository: `https://github.com/mananmeemroth/Panic2Pass`.
3. Configure the following settings:
   - **Name**: `panic2pass`
   - **Language / Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Under **Environment Variables**, add:
   - `GROQ_API_KEY`: *(Paste your `gsk_...` key)*
   *(Or if using a self-hosted Ollama server, set `OLLAMA_BASE_URL` to your server's URL)*
5. Click **Deploy Web Service**!

---

## 🔒 Privacy & Zero Cloud Leakage
When running locally, Panic2Pass runs 100% on your local machine using Ollama. No notes, slides, or questions ever leave your device.

---

## 📄 License
MIT License. Built for students everywhere.
