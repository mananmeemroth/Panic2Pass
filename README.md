# 🚨 Panic2Pass - The Pre-Exam Emergency AI Cramming Engine

> **Turn chaotic PDFs, lecture slides, and confusing syllabi into high-yield 30-minute exam triage plans in seconds — 100% locally & privately with Ollama.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20(Llama%203.2)-blueviolet.svg)](https://ollama.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Overview

**Panic2Pass** is built for students facing last-minute exam pressure. Powered directly and exclusively by **Ollama** (`llama3.2:3b`), it takes your uploaded syllabus or lecture notes and synthesizes laser-focused exam rescue materials with zero cloud data leakage.

### 🎯 Emergency Rescue Modes

1. ⚡ **30-Min Crash Plan**: Strict triage breakdown (10 mins for formulas/definitions, 15 mins for core mechanisms, 5 mins for hall-door memory checklist).
2. 🆘 **I'm Lost (ELI5 Concept Clarifier)**: De-jargonizes complex topics with intuitive real-world analogies, step-by-step logic, and common misconceptions.
3. 📝 **Quiz Me (High-Yield Active Recall)**: Simulates 3 high-probability exam questions with scoring criteria and hidden model answers.
4. 📋 **Rapid Cheat Sheet**: Dense markdown matrix of definitions, algorithm steps, and trap checklists.

---

## 🏗️ Architecture

```
Panic2Pass/
├── backend/
│   ├── config.py              # Server settings, Ollama endpoints, context limits
│   ├── model_cache.py         # Ollama model preloader & memory cache manager
│   ├── extractor.py           # Fast PDF text parser and character chunking
│   ├── prompts.py             # Focused exam triage prompts
│   └── engine.py              # Streaming execution engine
├── static/
│   ├── css/style.css          # Modern SaaS styling & responsive design
│   ├── js/main.js             # Real-time token streaming & drag-and-drop controller
│   └── images/                # 3D illustration assets
├── templates/
│   └── index.html             # Full-page landing page & interactive studio
├── app.py                     # FastAPI application & server launcher
├── requirements.txt           # Production Python dependencies
├── Procfile                   # Process file for cloud deployment
├── .gitignore                 # Git ignore rules
└── README.md                  # Documentation
```

---

## 🚀 Quickstart

### 1. Ensure Ollama is Running
```bash
ollama serve
ollama pull llama3.2:3b
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Panic2Pass
```bash
python app.py
```
Open **http://localhost:7860** in your browser.

---

## 🔒 Privacy & Zero Cloud Leakage
Panic2Pass runs 100% on your local machine using Ollama. No notes, slides, or questions ever leave your device.

---

## 📄 License
MIT License. Built for students everywhere.
