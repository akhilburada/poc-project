# Fine-tuning Phi-3 Mini for Text Rewriting Tasks

This repository contains code and resources for fine-tuning Microsoft's Phi-3 Mini model on a custom text rewriting dataset using QLoRA (Quantized Low-Rank Adaptation).

## 📁 Files

| File | Description |
|------|-------------|
| `phi3_mini_finetuning.ipynb` | Complete Google Colab notebook with step-by-step instructions |
| `finetune_phi3.py` | Standalone Python script for command-line training |
| `training_data.json` | Sample dataset with 47 text rewriting examples |

## 🚀 Quick Start (Google Colab)

1. **Open in Colab**: Upload `phi3_mini_finetuning.ipynb` to [Google Colab](https://colab.research.google.com/)

2. **Enable GPU**: Go to `Runtime` → `Change runtime type` → Select `T4 GPU` (free) or `A100` (Colab Pro)

3. **Run all cells**: The notebook will:
   - Install required packages
   - Load and format your dataset
   - Load Phi-3 Mini with 4-bit quantization
   - Apply LoRA adapters for efficient training
   - Train the model (~10-15 minutes on T4)
   - Test and save the fine-tuned model

## 💻 Quick Start (Local/Script)

```bash
# Install dependencies
pip install transformers>=4.40.0 peft>=0.10.0 bitsandbytes>=0.43.0
pip install trl>=0.8.0 accelerate>=0.28.0 datasets>=2.18.0

# Run fine-tuning
python finetune_phi3.py --data training_data.json --output ./phi3-finetuned --epochs 3
```

## 📊 Dataset Format

Your training data should be a JSON file with this structure:

```json
[
  {"input": "Rewrite to be friendlier: 'Send me the report by EOD.'", "output": "Could you please send me the report by end of day? Thanks!"},
  {"input": "Make more professional: 'Your app is broken.'", "output": "The application isn't working as expected. Could you investigate?"},
  ...
]
```

### Task Types in Sample Dataset

- **Tone rewriting**: Make friendlier, more professional, polite, confident
- **Length modification**: Shorten, simplify, expand for cover letter
- **Format conversion**: Bullets, email subjects, JSON, SMS
- **Summarization**: TL;DR, action lists, bullet summaries
- **Data extraction**: Dates, names, emails, numbers
- **Grammar fixes**: Correct grammar, remove passive voice

## 🔧 Configuration Options

### Training Arguments

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--epochs` | 3 | Number of training epochs |
| `--batch-size` | 2 | Batch size per GPU |
| `--lr` | 2e-4 | Learning rate |
| `--output` | `./phi3-text-rewriter` | Output directory |

### LoRA Configuration (in code)

```python
LoraConfig(
    r=16,                    # Rank of low-rank matrices
    lora_alpha=32,           # Scaling factor
    lora_dropout=0.05,       # Dropout for regularization
    target_modules=[         # Layers to apply LoRA
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
)
```

## 📈 Tips for Better Results

1. **More data**: The sample has 47 examples; aim for 100-1000+ for production use
2. **Consistent format**: Keep input instructions consistent (e.g., always start with action verb)
3. **Diverse examples**: Include edge cases and variations
4. **Longer training**: Try 5-10 epochs for small datasets
5. **Data quality**: High-quality outputs are crucial for model learning

## 💾 Loading the Fine-tuned Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import torch

# Configuration
model_id = "microsoft/Phi-3-mini-4k-instruct"
adapter_path = "./phi3-text-rewriter-final"

# Load with quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# Load base model + adapters
base_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)
model = PeftModel.from_pretrained(base_model, adapter_path)
tokenizer = AutoTokenizer.from_pretrained(adapter_path)
```

## 🧪 Inference Example

```python
def generate_response(prompt):
    formatted = f"""<|system|>
You are a helpful text rewriting assistant. Transform the input text as instructed.<|end|>
<|user|>
{prompt}<|end|>
<|assistant|>
"""
    inputs = tokenizer(formatted, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=128,
            temperature=0.7,
            top_p=0.9,
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    return response.split("<|assistant|>")[-1].replace("<|end|>", "").strip()

# Usage
result = generate_response("Rewrite to be more polite: 'Send it now.'")
print(result)  # "Could you please send it when you get a chance?"
```

## 📋 Requirements

- Python 3.8+
- CUDA-compatible GPU (8GB+ VRAM recommended)
- PyTorch 2.0+

### Package Versions

```
transformers>=4.40.0
peft>=0.10.0
bitsandbytes>=0.43.0
trl>=0.8.0
accelerate>=0.28.0
datasets>=2.18.0
```

## 🙋 Troubleshooting

### Out of Memory (OOM)
- Reduce `per_device_train_batch_size` to 1
- Enable `gradient_checkpointing=True`
- Use `max_seq_length=256` instead of 512

### Slow Training
- Use Google Colab Pro for A100 GPU
- Reduce number of epochs
- Use smaller LoRA rank (`r=8`)

### Poor Results
- Add more training examples
- Increase epochs (5-10)
- Check data quality and consistency
- Try different learning rates (1e-4 to 5e-4)

## 📚 References

- [Phi-3 Technical Report](https://arxiv.org/abs/2404.14219)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [Hugging Face PEFT](https://huggingface.co/docs/peft)
- [TRL Library](https://huggingface.co/docs/trl)

## 📄 License

This code is provided for educational purposes. Please check the [Phi-3 License](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) for model usage terms.
