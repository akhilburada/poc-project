# Real-World Client Project Guide for ML/AI Engineers (2 Years Experience)

## Healthcare + Fine-tuning Focused Projects (Step-by-Step)

This guide covers realistic healthcare client projects with fine-tuning that a 2-year experience ML/AI engineer typically works on. Each project has detailed step-by-step implementation to help you understand and learn.

---

# PROJECT 1: Medical Report Summarization using Fine-tuned LLM

## Client Information
- **Client**: Apollo Hospitals Group (Large Hospital Chain)
- **Industry**: Healthcare
- **Location**: India/US
- **Duration**: 6 months

---

## STEP 1: Understanding the Business Problem

### What was the problem?
```
BEFORE (Manual Process):
┌─────────────────────────────────────────────────────────────┐
│  Doctor writes 5-10 page discharge summary                  │
│           ↓                                                 │
│  Patient doesn't understand medical terms                   │
│           ↓                                                 │
│  Patient asks questions to nurse (wastes time)              │
│           ↓                                                 │
│  Patient confused about medications, follow-ups             │
│           ↓                                                 │
│  Poor treatment adherence, readmissions                     │
└─────────────────────────────────────────────────────────────┘

Problems:
- Discharge summaries are 5-10 pages of medical jargon
- Patients can't understand complex medical terminology
- Doctors spend 30-45 minutes writing each summary
- Poor patient understanding → medication errors → readmissions
- Hospital readmission costs: $15,000+ per patient
```

### What client wanted?
```
AFTER (AI Solution):
┌─────────────────────────────────────────────────────────────┐
│  Doctor speaks/writes discharge notes                       │
│           ↓                                                 │
│  AI generates structured, patient-friendly summary          │
│           ↓                                                 │
│  Summary in simple language patient understands             │
│           ↓                                                 │
│  Better adherence, fewer readmissions                       │
└─────────────────────────────────────────────────────────────┘

Goals:
- Convert complex medical reports → simple patient summaries
- Reduce doctor's documentation time by 50%
- Improve patient understanding score from 45% to 85%
- Reduce readmission rate by 20%
```

---

## STEP 2: Data Collection & Understanding

### What data did we have?

```
Data Source 1: Discharge Summaries (Structured)
├── Patient Demographics
│   ├── Age, Gender, Blood Group
│   └── Medical Record Number
├── Admission Details
│   ├── Admission Date, Discharge Date
│   ├── Admitting Diagnosis
│   └── Ward/ICU details
├── Clinical Summary
│   ├── Chief Complaints
│   ├── History of Present Illness
│   ├── Past Medical History
│   ├── Examination Findings
│   └── Investigation Results (Lab, Imaging)
├── Treatment Given
│   ├── Medications administered
│   ├── Procedures performed
│   └── Surgeries (if any)
└── Discharge Information
    ├── Discharge Medications
    ├── Follow-up Instructions
    ├── Diet/Lifestyle advice
    └── Warning Signs to watch

Data Source 2: Doctor's Voice Notes (Unstructured)
├── Dictated notes during rounds
└── Post-procedure summaries

Total Data: 50,000 discharge summaries (3 years)
```

### Sample Input Document
```
DISCHARGE SUMMARY
Patient: Mr. Rajesh Kumar, 58/M
MRN: APL20231234

DIAGNOSIS: Acute Inferior Wall Myocardial Infarction (STEMI)

CHIEF COMPLAINTS: Patient presented with severe retrosternal 
chest pain radiating to left arm, associated with diaphoresis 
and nausea for 3 hours duration.

HISTORY: Known case of Type 2 Diabetes Mellitus on OHA for 
10 years. Hypertensive for 5 years on Amlodipine 5mg. 
Smoker - 20 pack years. No h/o CAD, CVA, CKD.

INVESTIGATIONS:
- ECG: ST elevation in II, III, aVF with reciprocal changes
- Trop I: 15.2 ng/ml (elevated)
- 2D Echo: RWMA in inferior wall, EF 45%
- Lipid Profile: TC 245, LDL 165, HDL 35, TG 220

TREATMENT:
Primary PCI done to RCA - Drug eluting stent (3.0 x 28mm) 
deployed with TIMI 3 flow achieved.
Dual antiplatelet therapy initiated.

DISCHARGE MEDICATIONS:
1. Tab Aspirin 75mg OD
2. Tab Clopidogrel 75mg OD  
3. Tab Atorvastatin 40mg HS
4. Tab Metoprolol 25mg BD
5. Tab Ramipril 2.5mg OD
... (continues for 2 more pages)
```

### Sample Output (Patient-Friendly Summary)
```
SIMPLE SUMMARY FOR: Mr. Rajesh Kumar

WHAT HAPPENED TO YOU:
You had a heart attack. A blood vessel in your heart got 
blocked, which stopped blood flow to part of your heart muscle.

WHAT WE DID:
We did an emergency procedure called "angioplasty" where we 
opened the blocked blood vessel and placed a small metal tube 
(stent) to keep it open. The procedure was successful.

YOUR MEDICATIONS (Take Daily):
┌─────────────────────────────────────────────────────────┐
│ Morning (After Breakfast):                               │
│   • Aspirin (small white tablet) - prevents blood clots │
│   • Clopidogrel (pink tablet) - prevents clots on stent │
│   • Metoprolol (white tablet) - protects your heart     │
│   • Ramipril (small pink) - protects heart & kidneys    │
│                                                          │
│ Night (After Dinner):                                    │
│   • Atorvastatin (white tablet) - lowers cholesterol    │
│   • Metoprolol (white tablet) - same as morning         │
└─────────────────────────────────────────────────────────┘

IMPORTANT - GO TO HOSPITAL IMMEDIATELY IF:
⚠️ Chest pain that doesn't go away in 5 minutes
⚠️ Difficulty breathing
⚠️ Excessive sweating without reason
⚠️ Pain spreading to jaw, arm, or back

LIFESTYLE CHANGES:
✓ STOP smoking completely
✓ Walk 30 minutes daily (start slow)
✓ Eat less salt and oil
✓ Take medicines every day - DON'T SKIP

NEXT APPOINTMENT: Dr. Sharma, Cardiology - 15 Jan 2024
```

---

## STEP 3: Why Fine-tuning? Why not GPT-4 directly?

### Comparison Table

| Factor | GPT-4 API | Fine-tuned Llama-2 |
|--------|-----------|-------------------|
| Cost per summary | $0.50 | $0.02 |
| Monthly cost (10K summaries) | $5,000 | $200 |
| Data Privacy | Data goes to OpenAI | Stays on-premise |
| HIPAA Compliance | Complex | Full control |
| Latency | 3-5 seconds | 1-2 seconds |
| Customization | Limited | Full control |
| Medical Accuracy | Good but generic | Trained on our data |

### Decision: Fine-tune Llama-2-7B with QLoRA
```
Reasons:
1. Patient data (PHI) cannot leave hospital servers → HIPAA
2. Volume: 10,000+ summaries/month → API costs too high
3. Need consistent medical terminology → domain fine-tuning
4. Hospital wants to own the model → no vendor lock-in
```

---

## STEP 4: Data Preparation (Most Important Step!)

### Step 4.1: Data Collection
```python
# How we collected training data

import pandas as pd
from sqlalchemy import create_engine

# Connect to Hospital EMR Database
engine = create_engine('postgresql://user:pass@emr-db:5432/hospital')

# Query discharge summaries
query = """
SELECT 
    patient_id,
    admission_date,
    discharge_date,
    discharge_summary_text,
    department,
    primary_diagnosis,
    icd_code
FROM discharge_summaries
WHERE discharge_date >= '2021-01-01'
AND department IN ('Cardiology', 'Neurology', 'Pulmonology')
AND LENGTH(discharge_summary_text) > 1000
"""

df = pd.read_sql(query, engine)
print(f"Total records: {len(df)}")  # 50,000 records
```

### Step 4.2: Data Cleaning
```python
# Remove PHI (Protected Health Information) for training

import re

def remove_phi(text):
    """Remove patient identifiable information"""
    
    # Remove names (using pattern matching)
    text = re.sub(r'Patient:\s*[A-Za-z\s]+,', 'Patient: [NAME],', text)
    
    # Remove MRN numbers
    text = re.sub(r'MRN:\s*\w+', 'MRN: [REDACTED]', text)
    
    # Remove phone numbers
    text = re.sub(r'\b\d{10}\b', '[PHONE]', text)
    
    # Remove dates (keep relative)
    text = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4}', '[DATE]', text)
    
    # Remove addresses
    text = re.sub(r'\d+\s+[\w\s]+(?:Street|Road|Lane|Ave)', '[ADDRESS]', text)
    
    return text

# Apply to all records
df['clean_summary'] = df['discharge_summary_text'].apply(remove_phi)
```

### Step 4.3: Create Training Pairs (Input-Output)
```python
# We needed doctors to create simplified versions
# This was the most time-consuming part

"""
Process:
1. Selected 5,000 discharge summaries
2. Hired 5 doctors (part-time) for annotation
3. Each doctor simplified 1,000 summaries
4. Quality check by senior physician
5. Took 2 months to create dataset
"""

# Training data format
training_example = {
    "instruction": "Convert this medical discharge summary into a simple, patient-friendly summary that a non-medical person can understand.",
    
    "input": """DISCHARGE SUMMARY
Patient: [NAME], 58/M
DIAGNOSIS: Acute Inferior Wall Myocardial Infarction
CHIEF COMPLAINTS: Severe retrosternal chest pain radiating 
to left arm with diaphoresis for 3 hours...
[Full medical text]""",
    
    "output": """SIMPLE SUMMARY FOR YOU

WHAT HAPPENED:
You had a heart attack. This means a blood vessel in your 
heart got blocked...
[Patient-friendly version]"""
}
```

### Step 4.4: Dataset Statistics
```
Final Training Dataset:
├── Total Examples: 5,000
├── Training Set: 4,000 (80%)
├── Validation Set: 500 (10%)
├── Test Set: 500 (10%)
│
├── By Department:
│   ├── Cardiology: 2,000
│   ├── Neurology: 1,500
│   ├── Pulmonology: 1,000
│   └── General Medicine: 500
│
├── Average Input Length: 2,500 tokens
├── Average Output Length: 800 tokens
└── Total Tokens: ~16.5 million
```

---

## STEP 5: Fine-tuning Implementation

### Step 5.1: Environment Setup
```bash
# On AWS SageMaker ml.g5.2xlarge instance (1x A10G GPU, 24GB)

# Create conda environment
conda create -n medical-llm python=3.10
conda activate medical-llm

# Install dependencies
pip install torch==2.1.0
pip install transformers==4.36.0
pip install peft==0.7.0
pip install bitsandbytes==0.41.0
pip install trl==0.7.0
pip install datasets==2.15.0
pip install accelerate==0.25.0
pip install wandb  # for tracking
```

### Step 5.2: Load Base Model with Quantization
```python
# File: train_medical_llm.py

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig
)

# Step 5.2.1: Configure 4-bit quantization
# This reduces memory from 14GB to 4GB
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,              # Load model in 4-bit
    bnb_4bit_quant_type="nf4",      # NormalFloat4 quantization
    bnb_4bit_compute_dtype=torch.float16,  # Compute in fp16
    bnb_4bit_use_double_quant=True  # Nested quantization
)

# Step 5.2.2: Load tokenizer
model_name = "meta-llama/Llama-2-7b-hf"  # Base model

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # Required for Llama
tokenizer.padding_side = "right"

# Step 5.2.3: Load model with quantization
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",  # Automatically place on GPU
    trust_remote_code=True
)

print(f"Model loaded! Memory used: {torch.cuda.memory_allocated()/1e9:.2f} GB")
# Output: Model loaded! Memory used: 4.2 GB
```

### Step 5.3: Configure LoRA
```python
# LoRA = Low-Rank Adaptation
# Instead of training all 7B parameters, we train only ~8M parameters

from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# Step 5.3.1: Prepare model for training
model = prepare_model_for_kbit_training(model)

# Step 5.3.2: LoRA Configuration
lora_config = LoraConfig(
    r=64,                    # Rank - higher = more capacity, more memory
    lora_alpha=16,           # Scaling factor
    target_modules=[         # Which layers to adapt
        "q_proj",            # Query projection
        "k_proj",            # Key projection
        "v_proj",            # Value projection
        "o_proj",            # Output projection
        "gate_proj",         # MLP gate
        "up_proj",           # MLP up
        "down_proj"          # MLP down
    ],
    lora_dropout=0.1,        # Dropout for regularization
    bias="none",             # Don't train biases
    task_type="CAUSAL_LM"    # Language modeling task
)

# Step 5.3.3: Apply LoRA to model
model = get_peft_model(model, lora_config)

# Check trainable parameters
model.print_trainable_parameters()
# Output: trainable params: 8,388,608 || all params: 6,746,804,224 || trainable%: 0.124%
```

### Step 5.4: Prepare Dataset
```python
from datasets import Dataset
import json

# Step 5.4.1: Load your annotated data
with open('training_data.json', 'r') as f:
    data = json.load(f)

# Step 5.4.2: Format into prompt template
def format_prompt(example):
    """Convert to instruction format"""
    prompt = f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""
    return {"text": prompt}

# Step 5.4.3: Create dataset
dataset = Dataset.from_list(data)
dataset = dataset.map(format_prompt)

# Step 5.4.4: Split into train/eval
dataset = dataset.train_test_split(test_size=0.1)
train_dataset = dataset['train']
eval_dataset = dataset['test']

print(f"Training examples: {len(train_dataset)}")
print(f"Evaluation examples: {len(eval_dataset)}")
```

### Step 5.5: Training Configuration
```python
from transformers import TrainingArguments
from trl import SFTTrainer

# Step 5.5.1: Training arguments
training_args = TrainingArguments(
    output_dir="./medical-llm-checkpoints",
    
    # Training hyperparameters
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=4,  # Effective batch = 4 * 4 = 16
    
    # Learning rate
    learning_rate=2e-4,
    weight_decay=0.01,
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    
    # Optimization
    optim="paged_adamw_32bit",  # Memory efficient optimizer
    fp16=True,                   # Mixed precision
    
    # Logging
    logging_steps=10,
    logging_dir="./logs",
    
    # Saving
    save_strategy="epoch",
    save_total_limit=3,
    
    # Evaluation
    evaluation_strategy="epoch",
    
    # Other
    max_grad_norm=0.3,
    group_by_length=True,  # Group similar lengths for efficiency
    report_to="wandb"      # Track on Weights & Biases
)

# Step 5.5.2: Create trainer
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    args=training_args,
    dataset_text_field="text",
    max_seq_length=2048,
    packing=False  # Don't pack multiple examples
)
```

### Step 5.6: Start Training
```python
# Step 5.6.1: Train the model
print("Starting training...")
trainer.train()

# Training output:
"""
Epoch 1/3:
  Step 100/750: loss=1.856, lr=0.000180
  Step 200/750: loss=1.234, lr=0.000195
  Step 300/750: loss=0.987, lr=0.000200
  ...
  Epoch 1 completed. Eval loss: 1.012

Epoch 2/3:
  Step 100/750: loss=0.876, lr=0.000185
  ...
  Epoch 2 completed. Eval loss: 0.856

Epoch 3/3:
  Step 100/750: loss=0.654, lr=0.000120
  ...
  Epoch 3 completed. Eval loss: 0.723

Training completed in 4 hours 32 minutes.
"""

# Step 5.6.2: Save the trained adapter
trainer.save_model("./medical-llm-final")
```

### Step 5.7: Merge and Export
```python
# Step 5.7.1: Merge LoRA weights with base model
from peft import PeftModel

# Load base model (full precision for merging)
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Load and merge adapter
model = PeftModel.from_pretrained(base_model, "./medical-llm-final")
model = model.merge_and_unload()

# Step 5.7.2: Save merged model
model.save_pretrained("./medical-llm-merged")
tokenizer.save_pretrained("./medical-llm-merged")

print("Model merged and saved!")
```

---

## STEP 6: Evaluation

### Step 6.1: Automated Metrics
```python
# Evaluate on test set

from rouge_score import rouge_scorer
import numpy as np

def evaluate_model(model, tokenizer, test_data):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])
    
    results = {
        'rouge1': [], 'rouge2': [], 'rougeL': [],
        'medical_accuracy': [], 'readability': []
    }
    
    for example in test_data:
        # Generate summary
        input_text = format_input(example['input'])
        inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
        
        outputs = model.generate(
            **inputs,
            max_new_tokens=1024,
            temperature=0.3,
            do_sample=True
        )
        
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        reference = example['output']
        
        # ROUGE scores
        scores = scorer.score(reference, generated)
        results['rouge1'].append(scores['rouge1'].fmeasure)
        results['rouge2'].append(scores['rouge2'].fmeasure)
        results['rougeL'].append(scores['rougeL'].fmeasure)
        
        # Medical accuracy (checked by rules)
        results['medical_accuracy'].append(
            check_medical_accuracy(example['input'], generated)
        )
        
        # Readability score
        results['readability'].append(
            calculate_readability(generated)
        )
    
    return {k: np.mean(v) for k, v in results.items()}

# Results
"""
Evaluation Results:
├── ROUGE-1: 0.72
├── ROUGE-2: 0.58
├── ROUGE-L: 0.69
├── Medical Accuracy: 94.5%
├── Readability Score: 8.2 (Grade level)
└── Average Generation Time: 1.8 seconds
"""
```

### Step 6.2: Human Evaluation
```
Human Evaluation Process:
1. Selected 100 random test summaries
2. 3 evaluators: Doctor, Nurse, Patient representative
3. Rated each summary on 1-5 scale

Results:
┌─────────────────────────────────────────┐
│ Metric                      │ Score     │
├─────────────────────────────────────────┤
│ Medical Accuracy            │ 4.6/5     │
│ Completeness                │ 4.4/5     │
│ Patient Understandability   │ 4.7/5     │
│ Actionability               │ 4.5/5     │
│ Overall Quality             │ 4.5/5     │
└─────────────────────────────────────────┘
```

---

## STEP 7: Deployment on AWS

### Step 7.1: Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                     Hospital Network (VPC)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │   EMR        │     │   API        │     │   Model      │    │
│  │   System     │────▶│   Gateway    │────▶│   Server     │    │
│  │              │     │   (FastAPI)  │     │   (vLLM)     │    │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
│        │                     │                    │             │
│        │                     │                    │             │
│        ▼                     ▼                    ▼             │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │   Patient    │     │   Logging    │     │   GPU        │    │
│  │   Portal     │     │   (CloudWatch)│    │   (g5.2xlarge)│   │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Step 7.2: Deploy Model with vLLM
```python
# File: deploy_model.py
# vLLM provides 3-5x faster inference than HuggingFace

from vllm import LLM, SamplingParams

# Load model with vLLM
llm = LLM(
    model="./medical-llm-merged",
    tensor_parallel_size=1,  # 1 GPU
    gpu_memory_utilization=0.9,
    max_model_len=4096
)

# Sampling parameters
sampling_params = SamplingParams(
    temperature=0.3,
    top_p=0.9,
    max_tokens=1024,
    stop=["### Input:", "### Instruction:"]
)

def generate_summary(discharge_text: str) -> str:
    prompt = f"""### Instruction:
Convert this medical discharge summary into a simple, patient-friendly 
summary that a non-medical person can understand.

### Input:
{discharge_text}

### Response:
"""
    
    outputs = llm.generate([prompt], sampling_params)
    return outputs[0].outputs[0].text
```

### Step 7.3: FastAPI Server
```python
# File: api_server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Medical Summary API")

class SummaryRequest(BaseModel):
    discharge_summary: str
    patient_language: str = "english"

class SummaryResponse(BaseModel):
    patient_summary: str
    processing_time: float
    word_count: int

@app.post("/generate-summary", response_model=SummaryResponse)
async def generate_patient_summary(request: SummaryRequest):
    import time
    start = time.time()
    
    try:
        summary = generate_summary(request.discharge_summary)
        
        return SummaryResponse(
            patient_summary=summary,
            processing_time=time.time() - start,
            word_count=len(summary.split())
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## STEP 8: Results & Business Impact

### Metrics Achieved
```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT RESULTS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TECHNICAL METRICS:                                              │
│  ├── Model Accuracy: 94.5%                                       │
│  ├── Generation Time: 1.8 seconds average                        │
│  ├── Throughput: 1000 summaries/hour                            │
│  └── Uptime: 99.9%                                               │
│                                                                  │
│  BUSINESS METRICS:                                               │
│  ├── Doctor Time Saved: 25 min/patient → 5 min (80% reduction)  │
│  ├── Patient Understanding: 45% → 87% (+42%)                    │
│  ├── Readmission Rate: 15% → 11% (27% reduction)                │
│  └── Annual Cost Savings: $2.1M                                  │
│                                                                  │
│  COST BREAKDOWN:                                                 │
│  ├── Development: $150,000 (6 months, 3 engineers)              │
│  ├── Infrastructure: $3,000/month (GPU + storage)               │
│  ├── Maintenance: $2,000/month                                   │
│  └── Total First Year: $210,000                                  │
│                                                                  │
│  ROI: 10x (Saved $2.1M, Cost $210K)                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Your Role Summary (For Interview)

```
"I worked on a medical report summarization project for a large 
hospital chain. My responsibilities included:

1. DATA PREPARATION (2 months):
   - Worked with EMR team to extract 50,000 discharge summaries
   - Implemented PHI removal pipeline for HIPAA compliance
   - Coordinated with doctors to create 5,000 training pairs

2. MODEL DEVELOPMENT (2 months):
   - Implemented QLoRA fine-tuning pipeline for Llama-2-7B
   - Optimized hyperparameters using Weights & Biases
   - Achieved 94.5% medical accuracy on test set

3. DEPLOYMENT (1 month):
   - Deployed model using vLLM for optimized inference
   - Built FastAPI service with <2 second response time
   - Set up monitoring with CloudWatch

4. RESULTS:
   - Reduced doctor documentation time by 80%
   - Improved patient understanding scores from 45% to 87%
   - Saved hospital $2.1M annually in reduced readmissions"
```

---

## Interview Questions & Answers

### Q1: Why did you choose QLoRA over full fine-tuning?
```
Answer:
"We chose QLoRA for three main reasons:

1. MEMORY: Full fine-tuning Llama-2-7B needs 56GB+ GPU memory.
   QLoRA reduces this to 8GB, allowing us to use a single A10G GPU.

2. COST: Full fine-tuning would require 4x A100 GPUs (~$30/hour).
   QLoRA on single A10G cost us ~$2/hour. 10x cheaper.

3. PERFORMANCE: Research shows QLoRA achieves 97% of full 
   fine-tuning performance. Our evaluation confirmed this.

Trade-off: QLoRA inference is slightly slower due to quantization
overhead, but vLLM optimizations minimized this."
```

### Q2: How did you handle HIPAA compliance?
```
Answer:
"We implemented multiple layers of PHI protection:

1. DATA LAYER:
   - Removed all 18 HIPAA identifiers using regex + NER
   - Used date shifting (random offset) instead of removal
   - Stored data in encrypted S3 buckets

2. MODEL LAYER:
   - Trained on de-identified data only
   - Model runs on hospital's private VPC
   - No data sent to external APIs

3. DEPLOYMENT LAYER:
   - All traffic encrypted (TLS 1.3)
   - API authentication with hospital SSO
   - Audit logs for all requests

4. PROCESS LAYER:
   - Signed BAA with AWS
   - Regular security audits
   - Staff training on PHI handling"
```

### Q3: How did you evaluate medical accuracy?
```
Answer:
"We used a three-tier evaluation approach:

1. AUTOMATED CHECKS:
   - Entity extraction: Did output mention all medications?
   - Dosage matching: Are dosages correct?
   - Warning signs: Are critical symptoms included?

2. DOCTOR REVIEW:
   - 100 random samples reviewed by cardiologist
   - Scored on accuracy, completeness, safety
   - Average score: 4.6/5

3. PATIENT TESTING:
   - 50 patients read AI summaries
   - Comprehension quiz after reading
   - 87% scored above 80% on quiz

We also implemented a feedback loop where doctors could flag
incorrect summaries, which were added to training data."
```

### Q4: What was the most challenging part?
```
Answer:
"The most challenging part was creating high-quality training data.

CHALLENGE:
- Needed 5,000 input-output pairs
- Each pair required a doctor to write patient-friendly version
- Doctors are expensive and busy

SOLUTION:
1. Started with 500 examples, trained initial model
2. Used model to generate draft summaries
3. Doctors only had to EDIT, not write from scratch
4. This reduced annotation time by 60%

We also created detailed annotation guidelines with examples,
which improved consistency across different doctors."
```

---

# PROJECT 2: Clinical Notes NER and Diagnosis Coding (ICD-10)

## Client Information
- **Client**: United Healthcare (Insurance Company)
- **Industry**: Healthcare Insurance
- **Duration**: 8 months

---

## STEP 1: Business Problem

### What was the problem?
```
CURRENT PROCESS:
┌─────────────────────────────────────────────────────────────────┐
│  Hospital submits claim with clinical notes                      │
│           ↓                                                      │
│  Human coder reads notes (10-15 minutes)                        │
│           ↓                                                      │
│  Assigns ICD-10 codes manually                                   │
│           ↓                                                      │
│  Error rate: 15-20%                                              │
│           ↓                                                      │
│  Claim denials, appeals, delays                                  │
│           ↓                                                      │
│  Processing cost: $25/claim                                      │
└─────────────────────────────────────────────────────────────────┘

Problems:
- 5 million claims/month to process
- Human coders expensive ($50K-80K/year)
- 15% error rate causing claim denials
- Appeals process costs $100+ per denied claim
- Total annual cost: $150M+
```

### What client wanted?
```
AI SOLUTION:
┌─────────────────────────────────────────────────────────────────┐
│  Clinical notes submitted                                        │
│           ↓                                                      │
│  AI extracts: Diagnoses, Procedures, Medications                │
│           ↓                                                      │
│  AI suggests ICD-10 codes with confidence                       │
│           ↓                                                      │
│  High confidence (>95%): Auto-approve                           │
│  Low confidence (<95%): Human review                            │
│           ↓                                                      │
│  Target: 70% automation, 5% error rate                          │
└─────────────────────────────────────────────────────────────────┘

Goals:
- Automate 70% of claims coding
- Reduce error rate to <5%
- Reduce processing cost to $5/claim
- Annual savings target: $100M
```

---

## STEP 2: Understanding the Task

### What is ICD-10 Coding?
```
ICD-10 = International Classification of Diseases, 10th Revision

Example Clinical Note:
"58-year-old male with Type 2 Diabetes Mellitus presenting with 
diabetic foot ulcer on right heel. Patient also has hypertension 
and chronic kidney disease stage 3."

ICD-10 Codes to Assign:
├── E11.621 - Type 2 diabetes with foot ulcer
├── L97.419 - Ulcer of right heel, unspecified severity  
├── I10 - Essential hypertension
└── N18.3 - Chronic kidney disease, stage 3

Why it's hard:
- 70,000+ possible ICD-10 codes
- Subtle differences matter (E11.621 vs E11.622)
- Context dependent (primary vs secondary diagnosis)
- Requires medical knowledge
```

### Task Breakdown
```
Our AI System does 3 things:

TASK 1: Named Entity Recognition (NER)
Input: "Patient has Type 2 Diabetes with foot ulcer"
Output: 
  - [Type 2 Diabetes] → DIAGNOSIS
  - [foot ulcer] → DIAGNOSIS
  - [Patient] → not relevant

TASK 2: Entity Linking to ICD-10
Input: "Type 2 Diabetes with foot ulcer"
Output: E11.621 (specific code for this combination)

TASK 3: Code Ranking
Input: Multiple possible codes
Output: Ranked by confidence with explanations
```

---

## STEP 3: Data Preparation

### Step 3.1: Data Sources
```
Data Available:
├── Historical Claims Data
│   ├── 10 million claims (5 years)
│   ├── Clinical notes + assigned codes
│   └── Quality: Mixed (some errors)
│
├── MIMIC-III Dataset (Public)
│   ├── ICU clinical notes
│   ├── Professionally coded
│   └── Quality: High
│
└── ICD-10 Reference Database
    ├── All 70,000+ codes
    ├── Code descriptions
    └── Coding guidelines
```

### Step 3.2: Creating NER Training Data
```python
# We used a combination of:
# 1. Rule-based pre-labeling
# 2. Human annotation
# 3. Active learning

# Step 1: Rule-based pre-labeling
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_sci_lg")  # Medical NLP model

# Load medical dictionaries
diagnoses = load_umls_diagnoses()  # 100,000+ terms
procedures = load_cpt_codes()
medications = load_rxnorm()

# Create matchers
diagnosis_matcher = PhraseMatcher(nlp.vocab)
diagnosis_patterns = [nlp.make_doc(text) for text in diagnoses]
diagnosis_matcher.add("DIAGNOSIS", diagnosis_patterns)

def prelabel_document(text):
    doc = nlp(text)
    entities = []
    
    # Find diagnosis mentions
    matches = diagnosis_matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        entities.append({
            "start": span.start_char,
            "end": span.end_char,
            "text": span.text,
            "label": "DIAGNOSIS"
        })
    
    return entities

# Step 2: Human annotation using Label Studio
"""
Process:
1. Pre-labeled 50,000 notes using rules
2. Medical coders reviewed and corrected
3. Each note took 2-3 minutes to review
4. Total annotation time: 2,500 hours
5. Cost: $75,000 (annotators at $30/hour)
"""
```

### Step 3.3: Training Data Format
```python
# NER Training Data Format (BIO tagging)

training_example = {
    "text": "Patient is a 58 year old male with Type 2 Diabetes Mellitus presenting with diabetic foot ulcer",
    "entities": [
        {"start": 35, "end": 59, "label": "DIAGNOSIS"},  # Type 2 Diabetes Mellitus
        {"start": 77, "end": 95, "label": "DIAGNOSIS"}   # diabetic foot ulcer
    ]
}

# Convert to token-level labels
"""
Token          | Label
---------------|-------
Patient        | O
is             | O
a              | O
58             | O
year           | O
old            | O
male           | O
with           | O
Type           | B-DIAGNOSIS
2              | I-DIAGNOSIS
Diabetes       | I-DIAGNOSIS
Mellitus       | I-DIAGNOSIS
presenting     | O
with           | O
diabetic       | B-DIAGNOSIS
foot           | I-DIAGNOSIS
ulcer          | I-DIAGNOSIS
"""
```

### Step 3.4: Dataset Statistics
```
Final Dataset:
├── NER Training Data
│   ├── Documents: 50,000
│   ├── Total Entities: 450,000
│   ├── Entity Types: DIAGNOSIS, PROCEDURE, MEDICATION, LAB_VALUE
│   └── Average entities per doc: 9
│
├── ICD-10 Classification Data
│   ├── Training pairs: 500,000 (diagnosis text → ICD code)
│   ├── Unique ICD codes: 8,500 (most common)
│   └── Average codes per claim: 4.2
│
└── Split
    ├── Training: 80%
    ├── Validation: 10%
    └── Test: 10%
```

---

## STEP 4: Model Architecture

### Two-Stage Pipeline
```
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 1: NER MODEL                            │
│                  (Fine-tuned BioBERT)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: "58 yo male with Type 2 DM and diabetic foot ulcer"     │
│                              ↓                                   │
│  Output: [Type 2 DM] = DIAGNOSIS                                │
│          [diabetic foot ulcer] = DIAGNOSIS                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 2: CODE PREDICTION                      │
│              (Fine-tuned Llama-2 with RAG)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: "Type 2 DM" + "diabetic foot ulcer" + context           │
│                              ↓                                   │
│  RAG: Retrieve similar past cases + ICD guidelines              │
│                              ↓                                   │
│  Output: E11.621 (confidence: 94%)                              │
│          E11.622 (confidence: 3%)                               │
│          E11.620 (confidence: 2%)                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## STEP 5: Stage 1 - NER Model Training

### Step 5.1: Fine-tune BioBERT for NER
```python
# File: train_ner_model.py

from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForTokenClassification
)
from datasets import Dataset
import numpy as np

# Step 5.1.1: Define labels
label_list = [
    "O",           # Outside any entity
    "B-DIAGNOSIS", # Beginning of diagnosis
    "I-DIAGNOSIS", # Inside diagnosis
    "B-PROCEDURE", # Beginning of procedure
    "I-PROCEDURE", # Inside procedure
    "B-MEDICATION",# Beginning of medication
    "I-MEDICATION",# Inside medication
    "B-LAB",       # Beginning of lab value
    "I-LAB"        # Inside lab value
]
label2id = {l: i for i, l in enumerate(label_list)}
id2label = {i: l for i, l in enumerate(label_list)}

# Step 5.1.2: Load BioBERT
model_name = "dmis-lab/biobert-base-cased-v1.2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(
    model_name,
    num_labels=len(label_list),
    id2label=id2label,
    label2id=label2id
)

# Step 5.1.3: Tokenize and align labels
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(
        examples["tokens"],
        truncation=True,
        is_split_into_words=True,
        max_length=512
    )
    
    labels = []
    for i, label in enumerate(examples["ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        label_ids = []
        previous_word_idx = None
        
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)  # Ignore in loss
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])
            else:
                # For subwords, use I- tag if B- tag
                label_ids.append(label[word_idx])
            previous_word_idx = word_idx
        
        labels.append(label_ids)
    
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

# Step 5.1.4: Prepare dataset
train_dataset = Dataset.from_dict(train_data)
train_dataset = train_dataset.map(
    tokenize_and_align_labels,
    batched=True
)

# Step 5.1.5: Training arguments
training_args = TrainingArguments(
    output_dir="./ner-model",
    num_train_epochs=5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    learning_rate=5e-5,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="f1"
)

# Step 5.1.6: Compute metrics
from seqeval.metrics import f1_score, precision_score, recall_score

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=2)
    
    true_labels = [
        [id2label[l] for l in label if l != -100]
        for label in labels
    ]
    true_predictions = [
        [id2label[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    
    return {
        "precision": precision_score(true_labels, true_predictions),
        "recall": recall_score(true_labels, true_predictions),
        "f1": f1_score(true_labels, true_predictions)
    }

# Step 5.1.7: Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForTokenClassification(tokenizer),
    compute_metrics=compute_metrics
)

trainer.train()

# Results:
"""
NER Model Results:
├── Precision: 92.3%
├── Recall: 89.7%
├── F1 Score: 91.0%
│
├── By Entity Type:
│   ├── DIAGNOSIS: F1 = 93.2%
│   ├── PROCEDURE: F1 = 90.1%
│   ├── MEDICATION: F1 = 94.5%
│   └── LAB_VALUE: F1 = 86.2%
"""
```

---

## STEP 6: Stage 2 - ICD-10 Code Prediction

### Step 6.1: Build RAG System for ICD Guidelines
```python
# File: build_icd_rag.py

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Step 6.1.1: Load ICD-10 guidelines and descriptions
icd_documents = []

# Load official ICD-10 guidelines (700+ pages)
with open("icd10_guidelines.txt", "r") as f:
    guidelines = f.read()

# Load code descriptions
import pandas as pd
icd_codes = pd.read_csv("icd10_codes.csv")

for _, row in icd_codes.iterrows():
    doc = f"""
    ICD-10 Code: {row['code']}
    Description: {row['description']}
    Category: {row['category']}
    Guidelines: {row['coding_notes']}
    Examples: {row['examples']}
    """
    icd_documents.append(doc)

# Step 6.1.2: Chunk and embed
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = text_splitter.split_text("\n".join(icd_documents))

# Use medical embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="pritamdeka/S-PubMedBert-MS-MARCO"
)

# Create vector store
vectorstore = FAISS.from_texts(chunks, embeddings)
vectorstore.save_local("./icd_vectorstore")

print(f"Created vector store with {len(chunks)} chunks")
```

### Step 6.2: Fine-tune Llama-2 for Code Prediction
```python
# File: train_icd_model.py

# Training data format
training_example = {
    "instruction": """You are a medical coding expert. Given the extracted 
diagnoses and clinical context, predict the most appropriate ICD-10 codes.
Use the provided reference guidelines.""",
    
    "input": """
EXTRACTED ENTITIES:
- Type 2 Diabetes Mellitus [DIAGNOSIS]
- Diabetic foot ulcer [DIAGNOSIS]
- Right heel [BODY_LOCATION]

CLINICAL CONTEXT:
58-year-old male with history of Type 2 DM presenting with non-healing 
ulcer on right heel for 2 weeks. No signs of infection.

RELEVANT GUIDELINES:
[Retrieved from RAG]
E11.621 - Type 2 diabetes mellitus with foot ulcer
- Use when patient has type 2 DM with documented foot ulcer
- Additional code for site of ulcer (L97.4-)
""",
    
    "output": """
PRIMARY DIAGNOSIS:
E11.621 - Type 2 diabetes mellitus with foot ulcer
Confidence: 95%
Reasoning: Patient has documented Type 2 DM with foot ulcer, matching criteria.

SECONDARY DIAGNOSIS:
L97.419 - Non-pressure chronic ulcer of right heel, unspecified severity
Confidence: 88%
Reasoning: Ulcer location specified as right heel, severity not documented.

CODING NOTES:
- E11.621 should be sequenced first as the underlying condition
- L97.419 provides specificity for ulcer location
- Consider E11.65 if hyperglycemia documented
"""
}

# Fine-tuning follows same process as Project 1
# Using QLoRA with following specific changes:

lora_config = LoraConfig(
    r=32,              # Lower rank for classification task
    lora_alpha=64,
    target_modules=["q_proj", "v_proj"],  # Fewer modules
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Training for 5 epochs with early stopping
# Best model at epoch 3 with validation accuracy 87%
```

---

## STEP 7: Integration Pipeline

### Step 7.1: Complete Pipeline Code
```python
# File: icd_coding_pipeline.py

import torch
from transformers import pipeline
from langchain.vectorstores import FAISS
from vllm import LLM, SamplingParams

class ICDCodingPipeline:
    def __init__(self):
        # Load NER model
        self.ner_model = pipeline(
            "ner",
            model="./ner-model",
            tokenizer="./ner-model",
            aggregation_strategy="simple"
        )
        
        # Load RAG vector store
        self.vectorstore = FAISS.load_local(
            "./icd_vectorstore",
            embeddings
        )
        
        # Load fine-tuned LLM
        self.llm = LLM(model="./icd-llm-merged")
        self.sampling_params = SamplingParams(
            temperature=0.1,
            max_tokens=512
        )
    
    def extract_entities(self, clinical_text: str) -> list:
        """Stage 1: Extract medical entities"""
        entities = self.ner_model(clinical_text)
        
        # Group and deduplicate
        grouped = {}
        for ent in entities:
            key = ent['word'].lower()
            if key not in grouped:
                grouped[key] = {
                    'text': ent['word'],
                    'type': ent['entity_group'],
                    'score': ent['score']
                }
            else:
                # Keep highest confidence
                if ent['score'] > grouped[key]['score']:
                    grouped[key]['score'] = ent['score']
        
        return list(grouped.values())
    
    def retrieve_guidelines(self, entities: list) -> str:
        """Retrieve relevant ICD guidelines using RAG"""
        query = " ".join([e['text'] for e in entities if e['type'] == 'DIAGNOSIS'])
        
        docs = self.vectorstore.similarity_search(query, k=5)
        return "\n".join([doc.page_content for doc in docs])
    
    def predict_codes(self, entities: list, context: str, guidelines: str) -> dict:
        """Stage 2: Predict ICD-10 codes"""
        
        # Format entities
        entity_str = "\n".join([
            f"- {e['text']} [{e['type']}]" for e in entities
        ])
        
        prompt = f"""### Instruction:
You are a medical coding expert. Predict ICD-10 codes for the given diagnoses.

### Input:
EXTRACTED ENTITIES:
{entity_str}

CLINICAL CONTEXT:
{context}

RELEVANT GUIDELINES:
{guidelines}

### Response:
"""
        
        outputs = self.llm.generate([prompt], self.sampling_params)
        return self.parse_output(outputs[0].outputs[0].text)
    
    def parse_output(self, text: str) -> dict:
        """Parse LLM output into structured format"""
        codes = []
        
        # Extract codes using regex
        import re
        pattern = r'([A-Z]\d{2}\.?\d{0,4})\s*-\s*(.+?)(?:Confidence:\s*(\d+)%)?'
        
        for match in re.finditer(pattern, text):
            codes.append({
                'code': match.group(1),
                'description': match.group(2).strip(),
                'confidence': int(match.group(3)) if match.group(3) else 80
            })
        
        return {
            'codes': codes,
            'raw_output': text
        }
    
    def process_claim(self, clinical_text: str) -> dict:
        """Full pipeline"""
        # Step 1: Extract entities
        entities = self.extract_entities(clinical_text)
        
        # Step 2: Retrieve guidelines
        guidelines = self.retrieve_guidelines(entities)
        
        # Step 3: Predict codes
        result = self.predict_codes(entities, clinical_text, guidelines)
        
        # Step 4: Apply routing logic
        high_confidence = [c for c in result['codes'] if c['confidence'] >= 95]
        needs_review = [c for c in result['codes'] if c['confidence'] < 95]
        
        return {
            'entities': entities,
            'predicted_codes': result['codes'],
            'auto_approved': high_confidence,
            'needs_human_review': needs_review,
            'routing': 'auto' if len(needs_review) == 0 else 'human_review'
        }

# Usage
pipeline = ICDCodingPipeline()

clinical_note = """
58-year-old male with Type 2 Diabetes Mellitus presenting with 
diabetic foot ulcer on right heel. Patient also has hypertension 
and chronic kidney disease stage 3. No signs of infection.
"""

result = pipeline.process_claim(clinical_note)
print(result)

# Output:
"""
{
    'entities': [
        {'text': 'Type 2 Diabetes Mellitus', 'type': 'DIAGNOSIS', 'score': 0.98},
        {'text': 'diabetic foot ulcer', 'type': 'DIAGNOSIS', 'score': 0.96},
        {'text': 'hypertension', 'type': 'DIAGNOSIS', 'score': 0.97},
        {'text': 'chronic kidney disease stage 3', 'type': 'DIAGNOSIS', 'score': 0.94}
    ],
    'predicted_codes': [
        {'code': 'E11.621', 'description': 'Type 2 DM with foot ulcer', 'confidence': 96},
        {'code': 'L97.419', 'description': 'Ulcer of right heel', 'confidence': 89},
        {'code': 'I10', 'description': 'Essential hypertension', 'confidence': 98},
        {'code': 'N18.3', 'description': 'CKD stage 3', 'confidence': 95}
    ],
    'auto_approved': [
        {'code': 'E11.621', ...},
        {'code': 'I10', ...},
        {'code': 'N18.3', ...}
    ],
    'needs_human_review': [
        {'code': 'L97.419', ...}
    ],
    'routing': 'human_review'
}
"""
```

---

## STEP 8: Results & Metrics

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT RESULTS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TECHNICAL METRICS:                                              │
│  ├── NER F1 Score: 91.0%                                        │
│  ├── Code Prediction Accuracy: 87.5%                            │
│  ├── Top-3 Code Accuracy: 94.2%                                 │
│  ├── Processing Time: 2.5 seconds/claim                         │
│  └── Throughput: 1,500 claims/hour                              │
│                                                                  │
│  BUSINESS METRICS:                                               │
│  ├── Automation Rate: 68% (claims auto-processed)               │
│  ├── Error Rate: 4.2% (vs 15% manual)                           │
│  ├── Cost per Claim: $7 (vs $25 manual)                         │
│  ├── Monthly Claims Processed: 5 million                        │
│  └── Annual Savings: $90M                                        │
│                                                                  │
│  QUALITY IMPROVEMENTS:                                           │
│  ├── Claim Denial Rate: 12% → 6%                                │
│  ├── Appeals Reduced: 50%                                        │
│  └── Processing Time: 48 hours → 4 hours                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Your Role Summary (For Interview)

```
"I worked on a clinical NER and ICD-10 coding project for a major 
health insurance company. My responsibilities included:

1. NER MODEL DEVELOPMENT:
   - Fine-tuned BioBERT for medical entity extraction
   - Achieved 91% F1 score on diagnosis extraction
   - Implemented rule-based pre-labeling to reduce annotation costs

2. RAG SYSTEM FOR ICD GUIDELINES:
   - Built vector database with 70,000+ ICD-10 codes
   - Implemented semantic search for guideline retrieval
   - Integrated with LLM for context-aware coding

3. LLM FINE-TUNING:
   - Fine-tuned Llama-2-7B for code prediction
   - Used QLoRA to train on 500K coding examples
   - Achieved 87.5% accuracy on code prediction

4. DEPLOYMENT:
   - Built end-to-end pipeline with 2.5s latency
   - Implemented confidence-based routing
   - 68% of claims processed automatically

5. RESULTS:
   - Reduced coding errors from 15% to 4.2%
   - Saved $90M annually in operational costs
   - Reduced claim denials by 50%"
```

---

# PROJECT 3: AI-Powered Radiology Report Assistant

## Client Information
- **Client**: RadNet (Diagnostic Imaging Centers)
- **Industry**: Healthcare / Radiology
- **Duration**: 7 months

---

## STEP 1: Business Problem

```
CURRENT WORKFLOW:
┌─────────────────────────────────────────────────────────────────┐
│  Patient gets CT/MRI scan                                        │
│           ↓                                                      │
│  Images stored in PACS system                                    │
│           ↓                                                      │
│  Radiologist reviews images (15-20 min)                         │
│           ↓                                                      │
│  Radiologist dictates report (10-15 min)                        │
│           ↓                                                      │
│  Transcriptionist types report (20-30 min)                      │
│           ↓                                                      │
│  Radiologist reviews and signs (5 min)                          │
│           ↓                                                      │
│  Total time: 50-70 minutes per study                            │
│  Turnaround: 24-48 hours                                         │
└─────────────────────────────────────────────────────────────────┘

Problems:
- Radiologist shortage (30% vacancy rate)
- 1,000+ studies/day backlog
- High turnaround time affects patient care
- Inconsistent report quality
```

### AI Solution
```
AI-ASSISTED WORKFLOW:
┌─────────────────────────────────────────────────────────────────┐
│  Patient gets CT/MRI scan                                        │
│           ↓                                                      │
│  Images stored in PACS                                           │
│           ↓                                                      │
│  AI generates preliminary findings (30 seconds)                  │
│           ↓                                                      │
│  AI generates structured report draft (30 seconds)               │
│           ↓                                                      │
│  Radiologist reviews AI draft + images (10-15 min)              │
│           ↓                                                      │
│  Radiologist edits and signs (5 min)                            │
│           ↓                                                      │
│  Total time: 15-20 minutes per study                            │
│  Turnaround: 2-4 hours                                           │
└─────────────────────────────────────────────────────────────────┘

Goals:
- Generate structured report drafts from radiologist's voice notes
- Auto-suggest findings from prior reports
- Reduce report turnaround from 48 hrs to 4 hrs
- Maintain 95%+ clinical accuracy
```

---

## STEP 2: System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    RADIOLOGY AI ASSISTANT                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐                                                │
│  │  Voice Input │ ─────────┐                                    │
│  │  (Whisper)   │          │                                    │
│  └──────────────┘          │                                    │
│                            ▼                                    │
│                   ┌─────────────────┐                           │
│  ┌──────────────┐ │   RAG System    │                           │
│  │ Prior Reports│─▶│  (Patient      │                           │
│  │ (Vector DB)  │ │   History)      │                           │
│  └──────────────┘ └────────┬────────┘                           │
│                            │                                    │
│                            ▼                                    │
│  ┌──────────────┐ ┌─────────────────┐ ┌──────────────┐         │
│  │  Templates   │─▶│ Fine-tuned LLM │─▶│  Structured  │         │
│  │  (By Modality)│ │  (Report Gen)  │ │  Report      │         │
│  └──────────────┘ └─────────────────┘ └──────────────┘         │
│                            │                                    │
│                            ▼                                    │
│                   ┌─────────────────┐                           │
│                   │ Quality Checks  │                           │
│                   │ - Critical finds│                           │
│                   │ - Completeness  │                           │
│                   │ - Consistency   │                           │
│                   └─────────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## STEP 3: Data Preparation

### Step 3.1: Report Structure Analysis
```
Standard Radiology Report Sections:

CT CHEST REPORT:
├── CLINICAL HISTORY
│   └── Why the scan was ordered
├── TECHNIQUE  
│   └── How the scan was performed
├── COMPARISON
│   └── Prior studies for comparison
├── FINDINGS
│   ├── Lungs
│   ├── Pleura
│   ├── Mediastinum
│   ├── Heart
│   ├── Bones
│   └── Other
├── IMPRESSION
│   └── Summary of key findings
└── RECOMMENDATIONS
    └── Follow-up suggestions
```

### Step 3.2: Training Data Collection
```python
# Collected 100,000 radiology reports from PACS

data_structure = {
    "study_type": "CT Chest",
    "voice_dictation": "This is a CT chest with contrast...",
    "structured_report": {
        "clinical_history": "...",
        "technique": "...",
        "findings": {
            "lungs": "...",
            "pleura": "...",
            # ... other sections
        },
        "impression": "...",
        "recommendations": "..."
    },
    "prior_reports": ["report_id_1", "report_id_2"],
    "critical_findings": ["pulmonary embolism"],
    "icd_codes": ["I26.99"]
}

# Dataset split
"""
├── CT Reports: 40,000
├── MRI Reports: 30,000
├── X-Ray Reports: 20,000
└── Ultrasound Reports: 10,000
"""
```

### Step 3.3: Voice-to-Text Preprocessing
```python
# Using OpenAI Whisper for transcription

import whisper

model = whisper.load_model("large-v2")

def transcribe_dictation(audio_path: str) -> str:
    """Transcribe radiologist's voice dictation"""
    result = model.transcribe(
        audio_path,
        language="en",
        task="transcribe",
        initial_prompt="Radiology report dictation. Medical terminology."
    )
    return result["text"]

# Example dictation
"""
Input Audio: "Lungs are clear. No focal consolidation, 
pleural effusion or pneumothorax. Heart size is normal. 
No mediastinal lymphadenopathy..."

Output Text: "Lungs are clear. No focal consolidation, 
pleural effusion or pneumothorax. Heart size is normal. 
No mediastinal lymphadenopathy..."
"""
```

---

## STEP 4: Fine-tuning for Report Generation

### Step 4.1: Training Data Format
```python
training_example = {
    "instruction": """Generate a structured radiology report from the 
following dictation. Follow the standard report format and include 
all relevant sections.""",
    
    "input": """
STUDY TYPE: CT Chest with contrast
PATIENT CONTEXT: 65-year-old male, history of lung cancer, 
follow-up scan.

PRIOR REPORT (3 months ago):
"Known 2.3 cm right upper lobe nodule. No metastatic disease."

DICTATION:
"CT chest with contrast. Comparison made to prior CT from 3 months 
ago. Right upper lobe nodule now measures 2.8 cm, previously 2.3 cm, 
representing interval growth. No new pulmonary nodules. No pleural 
effusion. Mediastinal lymph nodes are stable. No osseous lesions."
""",
    
    "output": """
CT CHEST WITH CONTRAST

CLINICAL HISTORY:
65-year-old male with history of lung cancer, follow-up imaging.

TECHNIQUE:
CT of the chest was performed with intravenous contrast.

COMPARISON:
CT chest dated [3 months prior].

FINDINGS:

Lungs:
- Right upper lobe: Spiculated nodule measures 2.8 cm (previously 
  2.3 cm), representing interval growth of 5 mm.
- No new pulmonary nodules or masses.
- Airways are patent.

Pleura:
- No pleural effusion or pneumothorax.

Mediastinum:
- No significant mediastinal or hilar lymphadenopathy.
- Lymph nodes are stable compared to prior.

Heart:
- Heart size is normal.
- No pericardial effusion.

Bones:
- No aggressive osseous lesions.

IMPRESSION:
1. Interval growth of right upper lobe nodule (2.3 cm → 2.8 cm), 
   concerning for disease progression.
2. No new metastatic disease identified.

RECOMMENDATION:
Recommend PET-CT for further evaluation and oncology consultation.

CRITICAL FINDING: ⚠️ Interval growth of known malignancy - 
attending physician notified.
"""
}
```

### Step 4.2: Fine-tuning Code
```python
# Similar to Project 1, with specific modifications for radiology

# Custom loss weighting for critical findings
class RadiologyTrainer(SFTTrainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        outputs = model(**inputs)
        loss = outputs.loss
        
        # Extra weight for critical findings sections
        if self.is_critical_finding_batch(inputs):
            loss = loss * 1.5  # 50% higher weight
        
        return (loss, outputs) if return_outputs else loss
    
    def is_critical_finding_batch(self, inputs):
        # Check if batch contains critical findings
        decoded = self.tokenizer.batch_decode(inputs['input_ids'])
        critical_terms = ['tumor growth', 'pulmonary embolism', 
                         'aortic dissection', 'pneumothorax']
        return any(term in text.lower() for text in decoded 
                   for term in critical_terms)

# Training with domain-specific evaluation
def evaluate_radiology_report(generated: str, reference: str) -> dict:
    return {
        'rouge_l': compute_rouge(generated, reference),
        'section_completeness': check_all_sections(generated),
        'critical_finding_detected': check_critical_findings(generated),
        'measurement_accuracy': check_measurements(generated, reference),
        'recommendation_present': has_recommendations(generated)
    }
```

---

## STEP 5: RAG for Patient History

```python
# Build patient history retrieval system

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

class PatientHistoryRAG:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="pritamdeka/S-PubMedBert-MS-MARCO"
        )
        self.vectorstore = Chroma(
            persist_directory="./patient_reports_db",
            embedding_function=self.embeddings
        )
    
    def get_prior_reports(self, patient_id: str, study_type: str, 
                          current_findings: str, k: int = 3) -> list:
        """Retrieve relevant prior reports for comparison"""
        
        # Search within patient's reports
        results = self.vectorstore.similarity_search(
            query=current_findings,
            k=k,
            filter={"patient_id": patient_id}
        )
        
        # Sort by date (most recent first)
        results = sorted(results, 
                        key=lambda x: x.metadata['study_date'],
                        reverse=True)
        
        return [
            {
                'date': r.metadata['study_date'],
                'study_type': r.metadata['study_type'],
                'impression': r.page_content,
                'key_measurements': r.metadata.get('measurements', {})
            }
            for r in results
        ]
    
    def format_comparison_context(self, prior_reports: list) -> str:
        """Format prior reports for LLM context"""
        if not prior_reports:
            return "No prior imaging available for comparison."
        
        context = "PRIOR IMAGING FOR COMPARISON:\n\n"
        for report in prior_reports:
            context += f"Study Date: {report['date']}\n"
            context += f"Type: {report['study_type']}\n"
            context += f"Impression: {report['impression']}\n"
            if report['key_measurements']:
                context += f"Key Measurements: {report['key_measurements']}\n"
            context += "\n---\n\n"
        
        return context
```

---

## STEP 6: Critical Finding Detection

```python
# Safety layer for critical findings

CRITICAL_FINDINGS = {
    'CT_CHEST': [
        {'finding': 'pulmonary embolism', 'urgency': 'STAT'},
        {'finding': 'aortic dissection', 'urgency': 'STAT'},
        {'finding': 'tension pneumothorax', 'urgency': 'STAT'},
        {'finding': 'new lung mass', 'urgency': 'URGENT'},
        {'finding': 'tumor progression', 'urgency': 'URGENT'}
    ],
    'CT_HEAD': [
        {'finding': 'acute hemorrhage', 'urgency': 'STAT'},
        {'finding': 'acute stroke', 'urgency': 'STAT'},
        {'finding': 'mass effect', 'urgency': 'STAT'},
        {'finding': 'new brain mass', 'urgency': 'URGENT'}
    ]
}

class CriticalFindingDetector:
    def __init__(self):
        # Fine-tuned classifier for critical findings
        self.classifier = pipeline(
            "text-classification",
            model="./critical-findings-classifier",
            top_k=None
        )
    
    def check_report(self, report_text: str, study_type: str) -> dict:
        # Get predictions
        predictions = self.classifier(report_text)
        
        critical_findings = []
        for pred in predictions:
            if pred['score'] > 0.8:  # High confidence threshold
                finding_info = self.get_finding_info(pred['label'], study_type)
                if finding_info:
                    critical_findings.append({
                        'finding': pred['label'],
                        'confidence': pred['score'],
                        'urgency': finding_info['urgency'],
                        'action_required': self.get_action(finding_info['urgency'])
                    })
        
        return {
            'has_critical_findings': len(critical_findings) > 0,
            'findings': critical_findings,
            'notification_required': any(f['urgency'] == 'STAT' for f in critical_findings)
        }
    
    def get_action(self, urgency: str) -> str:
        actions = {
            'STAT': 'Immediately notify referring physician and document communication',
            'URGENT': 'Notify referring physician within 1 hour',
            'ROUTINE': 'Include in report, no immediate notification required'
        }
        return actions.get(urgency, 'Review required')
```

---

## STEP 7: Complete Pipeline

```python
# File: radiology_assistant.py

class RadiologyAssistant:
    def __init__(self):
        # Voice transcription
        self.whisper = whisper.load_model("large-v2")
        
        # Report generation LLM
        self.llm = LLM(model="./radiology-llm-merged")
        
        # Patient history RAG
        self.history_rag = PatientHistoryRAG()
        
        # Critical finding detector
        self.critical_detector = CriticalFindingDetector()
        
        # Report templates
        self.templates = load_report_templates()
    
    def process_study(self, 
                      audio_path: str, 
                      patient_id: str,
                      study_type: str,
                      clinical_history: str) -> dict:
        """Complete pipeline for radiology report generation"""
        
        # Step 1: Transcribe voice dictation
        dictation = self.whisper.transcribe(audio_path)['text']
        
        # Step 2: Get prior reports for comparison
        prior_reports = self.history_rag.get_prior_reports(
            patient_id=patient_id,
            study_type=study_type,
            current_findings=dictation
        )
        comparison_context = self.history_rag.format_comparison_context(prior_reports)
        
        # Step 3: Generate structured report
        template = self.templates[study_type]
        prompt = self.build_prompt(
            dictation=dictation,
            clinical_history=clinical_history,
            comparison=comparison_context,
            template=template
        )
        
        report = self.generate_report(prompt)
        
        # Step 4: Check for critical findings
        critical_check = self.critical_detector.check_report(report, study_type)
        
        # Step 5: Add critical finding alerts if needed
        if critical_check['has_critical_findings']:
            report = self.add_critical_alerts(report, critical_check)
        
        return {
            'draft_report': report,
            'transcription': dictation,
            'critical_findings': critical_check,
            'prior_comparisons': len(prior_reports),
            'requires_stat_notification': critical_check['notification_required']
        }
    
    def generate_report(self, prompt: str) -> str:
        sampling_params = SamplingParams(
            temperature=0.2,  # Low temperature for consistency
            max_tokens=2048
        )
        outputs = self.llm.generate([prompt], sampling_params)
        return outputs[0].outputs[0].text

# Usage
assistant = RadiologyAssistant()

result = assistant.process_study(
    audio_path="dictation_001.wav",
    patient_id="PT12345",
    study_type="CT_CHEST",
    clinical_history="65-year-old male, lung cancer follow-up"
)

print(result['draft_report'])
```

---

## STEP 8: Results

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT RESULTS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TECHNICAL METRICS:                                              │
│  ├── Report Generation Accuracy: 94.2%                          │
│  ├── Critical Finding Detection: 99.1% sensitivity              │
│  ├── Section Completeness: 97.5%                                │
│  ├── Measurement Accuracy: 98.3%                                │
│  └── Average Generation Time: 45 seconds                        │
│                                                                  │
│  WORKFLOW METRICS:                                               │
│  ├── Radiologist Time per Study: 60 min → 18 min (70% reduction)│
│  ├── Report Turnaround: 48 hours → 3.5 hours (93% reduction)   │
│  ├── Reports per Radiologist/Day: 25 → 65 (160% increase)       │
│  └── Transcription Cost Savings: $500K/year                     │
│                                                                  │
│  QUALITY METRICS:                                                │
│  ├── Report Revision Rate: 8% → 3%                              │
│  ├── Critical Finding Miss Rate: 0.5% → 0.05%                   │
│  └── Radiologist Satisfaction: 4.5/5                            │
│                                                                  │
│  BUSINESS IMPACT:                                                │
│  ├── Annual Revenue Increase: $3.2M (more studies processed)    │
│  ├── Cost Savings: $1.8M (reduced transcription + efficiency)   │
│  └── Total Value: $5M annually                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Your Role Summary (For Interview)

```
"I worked on an AI-powered radiology report assistant that helps 
radiologists generate reports faster. My responsibilities:

1. VOICE-TO-REPORT PIPELINE:
   - Integrated Whisper for medical dictation transcription
   - Built RAG system for patient history retrieval
   - Fine-tuned Llama-2 for structured report generation

2. FINE-TUNING:
   - Created training dataset from 100K radiology reports
   - Used QLoRA to fine-tune on domain-specific format
   - Achieved 94.2% accuracy on report generation

3. SAFETY LAYER:
   - Built critical finding detection classifier
   - 99.1% sensitivity on critical findings
   - Implemented automatic notification workflow

4. RESULTS:
   - Reduced report turnaround from 48 hrs to 3.5 hrs
   - Radiologists now process 160% more studies
   - Saved $1.8M annually in operational costs"
```

---

# Common Interview Q&A for All Projects

## Technical Questions

### Q: Why fine-tuning instead of prompt engineering?
```
Answer:
"We evaluated both approaches:

PROMPT ENGINEERING:
- Pros: Quick to implement, no training needed
- Cons: Inconsistent output format, higher latency (long prompts), 
  higher API costs, limited domain knowledge

FINE-TUNING:
- Pros: Consistent output, lower latency, lower cost, 
  better domain understanding
- Cons: Requires training data, upfront development time

For our use case (high volume, specific format, domain expertise),
fine-tuning was clearly better. We saw:
- 40% improvement in output consistency
- 60% reduction in inference cost
- 3x faster response time"
```

### Q: How do you handle model hallucinations in healthcare?
```
Answer:
"Hallucinations in healthcare are dangerous, so we implemented 
multiple safeguards:

1. RETRIEVAL AUGMENTATION (RAG):
   - Model must cite sources from our knowledge base
   - Reduces hallucination by grounding in facts

2. CONSTRAINED GENERATION:
   - Structured output format
   - Validation against known values (ICD codes, drug names)

3. CONFIDENCE SCORING:
   - Model outputs confidence for each prediction
   - Low confidence → human review

4. POST-PROCESSING VALIDATION:
   - Rule-based checks for medical accuracy
   - Cross-reference with patient history

5. HUMAN-IN-THE-LOOP:
   - Doctors always review before final use
   - Feedback loop for continuous improvement"
```

### Q: How do you evaluate healthcare AI models?
```
Answer:
"We use a multi-level evaluation approach:

LEVEL 1 - AUTOMATED METRICS:
- ROUGE scores for summarization
- F1/Precision/Recall for NER/classification
- Exact match for code prediction

LEVEL 2 - DOMAIN-SPECIFIC METRICS:
- Medical accuracy (correct entities, codes)
- Completeness (all required fields present)
- Consistency (same input → same output)

LEVEL 3 - HUMAN EVALUATION:
- Doctor review of random samples
- Likert scale ratings (1-5)
- Error categorization

LEVEL 4 - CLINICAL VALIDATION:
- Prospective study with real patients
- Compare AI vs human performance
- Track downstream outcomes

We don't deploy until all 4 levels show acceptable results."
```

### Q: What's your experience with LoRA hyperparameters?
```
Answer:
"Key hyperparameters and my learnings:

RANK (r):
- Higher rank = more capacity but more memory
- For domain adaptation: r=32-64 works well
- For task-specific: r=8-16 often sufficient
- We used r=64 for medical terminology

ALPHA:
- Controls learning rate scaling (alpha/r)
- Typically alpha = 2*r works well
- We used alpha=128 with r=64

TARGET MODULES:
- Attention layers (q,k,v,o) are essential
- MLP layers (gate, up, down) help for domain adaptation
- We targeted all 7 modules for best results

DROPOUT:
- 0.05-0.1 for regularization
- Higher dropout if overfitting
- We used 0.1 due to limited data

These were tuned through systematic experimentation using 
Weights & Biases for tracking."
```

---

## How to Explain Projects in Interview

### STAR Method Example
```
SITUATION:
"At [Company], we had a client - a large hospital chain - struggling 
with discharge summary documentation. Doctors were spending 30+ 
minutes per patient on paperwork, and patients couldn't understand 
the medical jargon."

TASK:
"My task was to build an AI system that could convert complex 
medical discharge summaries into simple, patient-friendly language 
while maintaining medical accuracy."

ACTION:
"I led the ML development:
1. First, I worked with the EMR team to extract 50,000 historical 
   discharge summaries, implementing PHI removal for HIPAA compliance.
2. I coordinated with 5 doctors to create 5,000 training pairs of 
   medical-to-simple text conversions.
3. I implemented a QLoRA fine-tuning pipeline for Llama-2-7B, 
   achieving 94.5% accuracy on our medical accuracy benchmark.
4. I deployed the model using vLLM on AWS within the hospital's 
   private VPC for data privacy.
5. I built monitoring dashboards to track model performance and 
   collect feedback for improvement."

RESULT:
"The system reduced doctor documentation time by 80%, improved 
patient understanding scores from 45% to 87%, and contributed to 
a 27% reduction in readmission rates. The hospital estimated 
annual savings of $2.1M."
```

---

## Quick Reference: Key Numbers to Remember

```
PROJECT 1 - Medical Report Summarization:
├── Training data: 5,000 examples
├── Model: Llama-2-7B with QLoRA
├── Accuracy: 94.5%
├── Latency: 1.8 seconds
├── Time saved: 80% (30 min → 5 min)
└── Annual savings: $2.1M

PROJECT 2 - ICD-10 Coding:
├── NER F1: 91.0%
├── Code accuracy: 87.5%
├── Automation rate: 68%
├── Error reduction: 15% → 4.2%
└── Annual savings: $90M

PROJECT 3 - Radiology Assistant:
├── Report accuracy: 94.2%
├── Critical finding detection: 99.1%
├── Turnaround reduction: 48 hrs → 3.5 hrs
├── Productivity increase: 160%
└── Annual value: $5M
```

---

## Study Checklist

- [ ] Understand business problem for each project
- [ ] Know the data pipeline and preprocessing steps
- [ ] Understand fine-tuning process (QLoRA, LoRA, hyperparameters)
- [ ] Know evaluation metrics and results
- [ ] Understand deployment architecture
- [ ] Practice explaining your role using STAR method
- [ ] Prepare for technical deep-dive questions
- [ ] Know the challenges and solutions
- [ ] Remember key metrics and numbers
- [ ] Prepare questions to ask the interviewer
