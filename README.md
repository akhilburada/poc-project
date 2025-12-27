# 🏥 Healthcare SLM Fine-tuning POC

A **Proof of Concept** for fine-tuning Small Language Models (SLMs) on healthcare data using CPU-only infrastructure. This POC demonstrates real-time training visualization, before/after response comparison, and efficient domain adaptation.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Project Overview

This POC addresses the need for **on-premise, cost-effective AI solutions** in healthcare settings where:
- Data privacy and security are paramount
- GPU infrastructure may not be available
- Quick customization to specific domains is required
- Live demonstrations of AI capabilities are needed

### Key Features

| Feature | Description |
|---------|-------------|
| 📁 **File Upload** | Support for CSV, JSON, JSONL, and TXT formats |
| 🚀 **Fast Training** | Optimized for < 5 minute training cycles |
| 📊 **Real-time Visualization** | Live loss curves and learning rate schedules |
| 💬 **Before/After Comparison** | Side-by-side response comparison |
| 🔧 **LoRA Fine-tuning** | Efficient parameter-efficient training |
| 💻 **CPU-Optimized** | No GPU required |

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- 4GB+ RAM recommended
- No GPU required

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd healthcare-slm-poc

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Start the Streamlit app
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Step 1: Upload Data

Upload your healthcare Q&A dataset or use the built-in sample data.

**Supported Formats:**

**JSON/JSONL:**
```json
{
  "instruction": "What are the symptoms of diabetes?",
  "response": "Common symptoms include increased thirst..."
}
```

**CSV:**
```csv
question,answer
"What are diabetes symptoms?","Common symptoms include..."
```

**TXT:**
```
Q: What are diabetes symptoms?
A: Common symptoms include increased thirst, frequent urination...
```

### Step 2: Configure Training

Adjust training parameters in the sidebar:
- **Model**: DistilGPT2 (default), GPT2, OPT-125M
- **Epochs**: 1-5 (recommended: 2-3)
- **Batch Size**: 1-8 (recommended: 4)
- **Learning Rate**: 1e-5 to 2e-4
- **LoRA**: Enable for efficient training

### Step 3: Train & Compare

1. Click "Start Training" to begin fine-tuning
2. Watch real-time loss curves and metrics
3. After training, use the chatbot to compare responses

## 🏗️ Project Structure

```
healthcare-slm-poc/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── src/
│   ├── __init__.py
│   ├── config.py         # Configuration settings
│   ├── data_processor.py # Data processing utilities
│   └── fine_tuner.py     # Fine-tuning pipeline
├── sample_data/
│   ├── healthcare_qa.json
│   └── healthcare_qa.csv
├── docs/
│   └── SLM_vs_LLM_Analysis.md
├── uploads/              # Uploaded files (created at runtime)
└── trained_models/       # Saved models (created at runtime)
```

## 🔧 Technical Details

### Model Architecture

- **Base Model**: DistilGPT2 (82M parameters)
- **Fine-tuning Method**: LoRA (Low-Rank Adaptation)
- **Trainable Parameters**: ~0.5% of total (with LoRA)

### LoRA Configuration

```python
LoraConfig(
    r=8,                    # Rank of update matrices
    lora_alpha=32,          # Scaling factor
    lora_dropout=0.1,       # Dropout probability
    target_modules=["c_attn", "c_proj"]  # GPT-2 attention layers
)
```

### Training Optimizations for CPU

1. **Small Batch Sizes**: Reduced memory footprint
2. **Gradient Accumulation**: Simulates larger batches
3. **Float32 Precision**: CPU-compatible (no FP16)
4. **LoRA**: Reduces trainable parameters by ~99%
5. **Limited Context Length**: 256-512 tokens

## 📊 Performance Expectations

| Dataset Size | Training Time | Memory Usage |
|--------------|---------------|--------------|
| 50 samples   | ~1-2 min      | ~2GB         |
| 100 samples  | ~2-3 min      | ~2.5GB       |
| 500 samples  | ~10-15 min    | ~3GB         |
| 1000 samples | ~20-30 min    | ~3.5GB       |

*Times measured on Intel i7 CPU with 16GB RAM*

## 🩺 Healthcare Use Cases

1. **Patient FAQ Bot**: Answer common health questions
2. **Insurance Query Handler**: Explain coverage and benefits
3. **Appointment Scheduling**: Natural language scheduling
4. **Symptom Checker**: Initial symptom assessment
5. **Medication Information**: Drug interactions and instructions

## ⚠️ Important Limitations

1. **Not for Medical Diagnosis**: This is a POC, not a medical device
2. **Accuracy Varies**: Small models have limited reasoning ability
3. **Training Data Quality**: Output quality depends on input data
4. **Hallucination Risk**: Model may generate inaccurate information
5. **Context Limitations**: Limited context window (256-512 tokens)

## 🔒 Security Considerations

- **On-Premise Deployment**: Data never leaves your infrastructure
- **No External API Calls**: All processing is local
- **Data Isolation**: Uploaded data is not persisted by default
- **Model Isolation**: Fine-tuned models are stored locally

## 📚 Further Reading

- [SLM vs LLM Analysis](docs/SLM_vs_LLM_Analysis.md) - Detailed comparison
- [LoRA Paper](https://arxiv.org/abs/2106.09685) - Original LoRA research
- [Hugging Face PEFT](https://huggingface.co/docs/peft) - PEFT documentation

## 🛠️ Troubleshooting

### Common Issues

**Out of Memory:**
- Reduce batch size to 1-2
- Reduce max sequence length
- Close other applications

**Slow Training:**
- Reduce number of epochs
- Use smaller dataset
- Enable LoRA if disabled

**Poor Results:**
- Increase training epochs
- Use more/better training data
- Adjust learning rate

## 📝 License

This project is for demonstration purposes. Please ensure compliance with healthcare regulations (HIPAA, etc.) before production use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

**Built with ❤️ for Healthcare AI Innovation**
