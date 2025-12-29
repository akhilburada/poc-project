# 🏥 Healthcare SLM Fine-tuning POC

A **Proof of Concept** for customizing Small Language Models (SLMs) on healthcare data using **local Ollama models** (Phi3, Llama 3.2).

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local-green.svg)

---

## 🎯 What This POC Does

```
┌─────────────────────────────────────────────────────────────────┐
│                         POC WORKFLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. UPLOAD DATA ──► Healthcare Q&A dataset (JSON/CSV)           │
│                                                                  │
│  2. BEFORE ──────► Ask question to BASE model                   │
│                    (Generic response, no healthcare knowledge)   │
│                                                                  │
│  3. TRAIN ───────► Embed healthcare knowledge into model        │
│                    (< 5 minutes, real-time visualization)        │
│                                                                  │
│  4. AFTER ───────► Ask SAME question to TRAINED model           │
│                    (Accurate, domain-specific response)          │
│                                                                  │
│  5. COMPARE ─────► Side-by-side Before vs After                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+**
2. **Ollama** installed and running with models:
   - `phi3:mini` (recommended for fast demos)
   - `llama3.2:1b` (alternative option)

### Step 1: Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download
```

### Step 2: Pull Models

```bash
# Start Ollama server
ollama serve

# In another terminal, pull models
ollama pull phi3:mini
ollama pull llama3.2:1b
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📖 Usage Guide

### Tab 1: Data Upload

1. Upload your healthcare Q&A dataset (or use sample data)
2. Supported formats: **CSV**, **JSON**, **JSONL**, **TXT**
3. Preview your data before training

**Sample JSON Format:**
```json
{
  "instruction": "What are the symptoms of diabetes?",
  "response": "Common symptoms include increased thirst, frequent urination..."
}
```

### Tab 2: Training

1. Select your base model (phi3:mini or llama3.2:1b)
2. Click **"Start Training"**
3. Watch real-time loss curves
4. Training completes in < 5 minutes

### Tab 3: Chatbot

1. Ask healthcare questions
2. See **Before** (base model) and **After** (trained model) responses
3. Compare the improvement side-by-side

---

## 📁 Project Structure

```
/workspace/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── src/
│   ├── __init__.py
│   ├── config.py             # Configuration settings
│   ├── data_processor.py     # Data processing utilities
│   ├── fine_tuner.py         # HuggingFace fine-tuner (optional)
│   └── ollama_client.py      # Ollama integration
├── sample_data/
│   ├── healthcare_qa.json    # Sample healthcare Q&A
│   └── healthcare_qa.csv     # Alternative format
└── docs/
    ├── SLM_vs_LLM_Analysis.md
    └── SLM_Sales_Presentation.md
```

---

## 🔧 How Training Works

This POC uses **Ollama's Modelfile approach** to embed healthcare knowledge:

```
Base Model (phi3:mini)
        │
        ▼
┌───────────────────┐
│  Healthcare Q&A   │
│  Data Processing  │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Create Custom    │
│  Modelfile with   │
│  System Prompt    │
└───────────────────┘
        │
        ▼
Trained Model (healthcare-assistant)
```

**Note:** This is knowledge embedding via system prompts, not traditional weight-based fine-tuning. For true fine-tuning, you would need tools like llama.cpp or Unsloth.

---

## 💡 Key Features

| Feature | Description |
|---------|-------------|
| 🦙 **Local Ollama** | Uses your installed Ollama models |
| 📁 **File Upload** | CSV, JSON, JSONL, TXT support |
| ⚡ **Fast Training** | < 5 minutes for POC demo |
| 📊 **Real-time Charts** | Live loss and learning rate visualization |
| 🔄 **Before/After** | Side-by-side response comparison |
| 🔒 **Privacy** | All data stays local |

---

## ❓ Troubleshooting

### Ollama Not Running

```bash
# Start Ollama server
ollama serve

# Check if running
ollama list
```

### No Models Found

```bash
ollama pull phi3:mini
ollama pull llama3.2:1b
```

### Slow First Response

The first query loads the model into memory. Subsequent queries are faster.

### Out of Memory

- Use smaller model (`phi3:mini` instead of larger models)
- Close other applications
- Reduce "Max Knowledge Items" in sidebar

---

## 📊 Expected Performance

| Model | Size | First Response | Subsequent | RAM Usage |
|-------|------|----------------|------------|-----------|
| phi3:mini | 2.3GB | 5-10s | 1-3s | ~4GB |
| llama3.2:1b | 1.3GB | 3-7s | 1-2s | ~3GB |

---

## 🎬 Demo Script (5 Minutes)

1. **[0:00]** Show Ollama status (green = running)
2. **[0:30]** Upload sample healthcare data
3. **[1:00]** Ask question BEFORE training → show generic response
4. **[1:30]** Start training → watch loss curves
5. **[3:30]** Training complete
6. **[4:00]** Ask SAME question AFTER training → show improved response
7. **[4:30]** Side-by-side comparison
8. **[5:00]** Q&A

---

## 📝 License

This project is for demonstration purposes only. Ensure compliance with healthcare regulations (HIPAA, etc.) before production use.

---

**Built for Healthcare AI Innovation 🏥**
