# Patient Engagement AI - Interview Preparation Guide

## Your Role Summary (2 Years Experience)

**Your Responsibilities:**
1. Fine-tuning the LLM (Llama-2-7B) using QLoRA
2. Evaluating model performance
3. Deployment support

---

# PART 1: FINE-TUNING THE MODEL

## 1.1 What is Fine-Tuning? (Simple Explanation)

```
ANALOGY FOR INTERVIEWS:

Think of Llama-2 as a medical graduate who knows general medicine.
Fine-tuning is like giving them specialized training for THIS hospital.

Before Fine-tuning: "I know about medicines in general"
After Fine-tuning:  "I know exactly how to talk to Max Healthcare patients,
                     in their language, about their specific concerns"
```

## 1.2 Why QLoRA? (Interview Answer)

```
Q: "Why did you use QLoRA instead of full fine-tuning?"

A: "Three reasons:

1. MEMORY: Full fine-tuning needs 28GB+ GPU memory.
   QLoRA needs only 4-6GB. We could use cheaper GPUs.

2. COST: Full fine-tuning = ₹50,000+ for compute
   QLoRA = ₹500 for same result

3. SPEED: Full fine-tuning = days
   QLoRA = 4 hours

The 'Q' means Quantization (compress model to 4-bit).
The 'LoRA' means we only train small adapter layers (0.06% of parameters)."
```

## 1.3 Step-by-Step Fine-Tuning Process

### Step 1: Environment Setup

```bash
# What you actually ran on AWS EC2 g5.xlarge

# Create conda environment
conda create -n patient-ai python=3.10 -y
conda activate patient-ai

# Install PyTorch with CUDA support
pip install torch==2.1.0 --index-url https://download.pytorch.org/whl/cu118

# Install training libraries
pip install transformers==4.36.0    # Hugging Face library
pip install peft==0.7.0             # For LoRA adapters
pip install bitsandbytes==0.41.0    # For 4-bit quantization
pip install trl==0.7.0              # Training utilities
pip install datasets==2.15.0       # Dataset handling
pip install accelerate==0.25.0     # Training acceleration
pip install wandb                   # Experiment tracking
```

### Step 2: Load Model with 4-bit Quantization

```python
# File: load_model.py
# This is what you wrote to load the base model

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# ============================================
# QUANTIZATION CONFIG
# ============================================
# This compresses the model from 14GB to 4GB
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,              # Use 4-bit precision (key setting!)
    bnb_4bit_quant_type="nf4",      # NormalFloat4 - best quality for LLMs
    bnb_4bit_compute_dtype=torch.float16,  # Compute in fp16 for speed
    bnb_4bit_use_double_quant=True  # Extra compression layer
)

# ============================================
# LOAD TOKENIZER
# ============================================
# Tokenizer converts text to numbers (tokens)
model_name = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # Set padding token
tokenizer.padding_side = "right"            # Pad on right side

# ============================================
# LOAD MODEL
# ============================================
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,  # Apply 4-bit quantization
    device_map="auto"                # Automatically use GPU
)

print(f"Model loaded!")
print(f"GPU Memory Used: {torch.cuda.memory_allocated()/1e9:.2f} GB")
# Output: ~4.2 GB (instead of 14GB without quantization)
```

**Interview Explanation:**
```
"First, I loaded the base Llama-2-7B model with 4-bit quantization.
This reduced memory from 14GB to 4GB, allowing us to train on a
single A10G GPU (24GB). The key was using BitsAndBytesConfig with
NF4 quantization type, which preserves model quality while compressing."
```

### Step 3: Configure LoRA Adapters

```python
# File: setup_lora.py
# This is how you configured the trainable layers

from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# ============================================
# PREPARE MODEL FOR TRAINING
# ============================================
# This enables gradient computation for quantized model
model = prepare_model_for_kbit_training(model)

# ============================================
# LORA CONFIGURATION
# ============================================
lora_config = LoraConfig(
    r=32,                    # Rank - controls capacity (higher = more learning)
    lora_alpha=64,           # Scaling factor (usually 2x rank)
    target_modules=[         # Which layers to train
        "q_proj",            # Query projection (attention)
        "k_proj",            # Key projection (attention)
        "v_proj",            # Value projection (attention)
        "o_proj",            # Output projection (attention)
    ],
    lora_dropout=0.1,        # Dropout for regularization
    bias="none",             # Don't train biases
    task_type="CAUSAL_LM"    # Task type: language modeling
)

# ============================================
# APPLY LORA TO MODEL
# ============================================
model = get_peft_model(model, lora_config)

# Check what we're training
model.print_trainable_parameters()
# Output: trainable params: 4,194,304 || all params: 6,738,415,616 
#         || trainable%: 0.06%
```

**Interview Explanation:**
```
"LoRA adds small adapter matrices to the attention layers. Instead of
training all 7 billion parameters, we only train 4 million parameters
(0.06%). I chose r=32 as the rank - this controls how much the model
can learn. Higher rank means more capacity but more memory. We targeted
the attention layers (q, k, v, o projections) because that's where the
model learns relationships between words."
```

### Step 4: Prepare Training Data

```python
# File: prepare_data.py
# This is how you formatted the training data

import json
from datasets import Dataset

# ============================================
# LOAD RAW DATA
# ============================================
with open("training_data.json", "r") as f:
    raw_data = json.load(f)

# Sample of what the raw data looks like:
# {
#     "question": "When should I take Metformin?",
#     "answer": "Take Metformin with meals, morning and evening...",
#     "category": "MEDICATION",
#     "patient_context": "Diabetic patient, post-discharge"
# }

# ============================================
# FORMAT INTO LLAMA-2 CHAT TEMPLATE
# ============================================
def format_for_training(example):
    """Convert Q&A pair into Llama-2 chat format"""
    
    # Llama-2 uses special tokens: [INST], <<SYS>>, etc.
    formatted = f"""<s>[INST] <<SYS>>
You are a caring health assistant for a hospital. Answer patient questions 
in simple, easy-to-understand language. Be warm and supportive. If you 
detect an emergency, tell the patient to go to the hospital immediately.
<</SYS>>

Patient Question: {example['question']}
Patient Context: {example.get('patient_context', 'General patient')}
[/INST] {example['answer']} </s>"""
    
    return {"text": formatted}

# ============================================
# CREATE DATASET
# ============================================
dataset = Dataset.from_list(raw_data)
dataset = dataset.map(format_for_training)

# Split into training and validation
dataset = dataset.train_test_split(test_size=0.1, seed=42)

print(f"Training examples: {len(dataset['train'])}")    # 22,500
print(f"Validation examples: {len(dataset['test'])}")   # 2,500
```

**Interview Explanation:**
```
"I formatted the training data into Llama-2's chat template. This template
uses special tokens like [INST] for instructions and <<SYS>> for system
prompts. Getting this format right is crucial - if the format doesn't match
what Llama-2 expects, the model won't learn properly. I also included a
system prompt that defines the assistant's personality and guidelines."
```

### Step 5: Training Configuration

```python
# File: train.py
# The actual training script you ran

from transformers import TrainingArguments
from trl import SFTTrainer

# ============================================
# TRAINING ARGUMENTS
# ============================================
training_args = TrainingArguments(
    # Output directory for checkpoints
    output_dir="./patient-ai-checkpoints",
    
    # Training duration
    num_train_epochs=3,              # Train for 3 passes over data
    
    # Batch size configuration
    per_device_train_batch_size=4,   # 4 examples per GPU at a time
    gradient_accumulation_steps=4,    # Accumulate 4 batches before update
    # Effective batch size = 4 * 4 = 16
    
    # Learning rate settings
    learning_rate=2e-4,              # 0.0002 - standard for LoRA
    warmup_steps=100,                # Gradually increase LR at start
    
    # Optimization
    fp16=True,                       # Use mixed precision (faster)
    optim="paged_adamw_32bit",       # Memory-efficient optimizer
    
    # Evaluation and saving
    evaluation_strategy="epoch",     # Evaluate after each epoch
    save_strategy="epoch",           # Save checkpoint after each epoch
    logging_steps=50,                # Log every 50 steps
    
    # Other settings
    max_grad_norm=0.3,              # Gradient clipping (prevents exploding)
    weight_decay=0.001,             # Regularization
)

# ============================================
# CREATE TRAINER
# ============================================
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset['train'],
    eval_dataset=dataset['test'],
    args=training_args,
    dataset_text_field="text",       # Column name with formatted text
    max_seq_length=1024,             # Maximum tokens per example
    packing=False,                   # Don't pack multiple examples
)

# ============================================
# START TRAINING
# ============================================
print("Starting training...")
trainer.train()

# Training takes ~4 hours on g5.xlarge
```

**Interview Explanation:**
```
"I configured training with:
- 3 epochs (passes through the data)
- Effective batch size of 16 (4 per device × 4 accumulation steps)
- Learning rate of 2e-4 with warmup
- Mixed precision (fp16) for faster training

The key hyperparameters I tuned were:
- Learning rate: Started with 1e-4, found 2e-4 gave faster convergence
- Epochs: 3 was optimal; more caused overfitting
- Batch size: 16 balanced memory usage and training stability"
```

### Step 6: Save the Fine-tuned Model

```python
# File: save_model.py
# After training completes

# ============================================
# MERGE LORA WEIGHTS WITH BASE MODEL
# ============================================
# This combines the trained adapters with the original model
model = model.merge_and_unload()

# ============================================
# SAVE FOR DEPLOYMENT
# ============================================
output_dir = "./patient-ai-final"
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"Model saved to {output_dir}")

# The saved model can now be loaded without LoRA/PEFT libraries
# Just use standard transformers loading
```

## 1.4 Training Monitoring (What You Tracked)

```python
# Using Weights & Biases (wandb) for tracking

import wandb

wandb.init(project="patient-ai", name="qlora-run-1")

# Metrics you monitored:
# 1. Training Loss - should decrease over time
# 2. Validation Loss - should decrease but not go below training loss
# 3. Learning Rate - verify warmup working correctly
# 4. GPU Memory - ensure not running out of memory
```

**Training Log Example:**
```
Epoch 1/3:
  Step 100: loss=1.823, lr=0.00015
  Step 200: loss=1.456, lr=0.00020
  Eval Loss: 1.189

Epoch 2/3:
  Step 400: loss=1.087, lr=0.00020
  Step 500: loss=0.956, lr=0.00020
  Eval Loss: 0.823

Epoch 3/3:
  Step 700: loss=0.756, lr=0.00020
  Step 800: loss=0.689, lr=0.00020
  Eval Loss: 0.598  ← Best model saved here
```

---

# PART 2: MODEL EVALUATION

## 2.1 Evaluation Overview

```
WHAT YOU EVALUATED:

1. ACCURACY - Does the model give correct answers?
2. SAFETY - Does it detect emergencies correctly?
3. QUALITY - Are responses helpful and clear?
4. CONSISTENCY - Does it give same answer to same question?
```

## 2.2 Automated Evaluation Metrics

### Accuracy Evaluation

```python
# File: evaluate_accuracy.py
# How you measured answer correctness

import json
from openai import OpenAI

client = OpenAI()  # GPT-4 as evaluator

def evaluate_response(question, model_answer, ground_truth):
    """Use GPT-4 to judge if model answer is correct"""
    
    prompt = f"""You are evaluating a healthcare AI assistant's response.

Question: {question}

Model's Answer: {model_answer}

Correct Answer: {ground_truth}

Rate the model's answer on these criteria (1-5 scale):
1. ACCURACY: Is the medical information correct?
2. COMPLETENESS: Does it cover all important points?
3. SAFETY: Would following this advice be safe?
4. CLARITY: Is it easy for a patient to understand?

Return JSON: {{"accuracy": X, "completeness": X, "safety": X, "clarity": X}}
"""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

# ============================================
# RUN EVALUATION ON TEST SET
# ============================================
def run_evaluation(test_data, model):
    """Evaluate model on entire test set"""
    
    results = []
    
    for item in test_data:
        # Get model's response
        model_answer = generate_response(model, item['question'])
        
        # Evaluate using GPT-4
        scores = evaluate_response(
            question=item['question'],
            model_answer=model_answer,
            ground_truth=item['answer']
        )
        
        results.append({
            "question": item['question'],
            "category": item['category'],
            "scores": scores
        })
    
    return results

# ============================================
# CALCULATE METRICS BY CATEGORY
# ============================================
def calculate_metrics(results):
    """Calculate accuracy by category"""
    
    categories = {}
    
    for r in results:
        cat = r['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r['scores']['accuracy'])
    
    for cat, scores in categories.items():
        avg = sum(scores) / len(scores)
        print(f"{cat}: {avg:.1%} accuracy")
    
    # Overall
    all_scores = [r['scores']['accuracy'] for r in results]
    print(f"\nOVERALL: {sum(all_scores)/len(all_scores):.1%}")

# Results:
# MEDICATION: 96.2% accuracy
# SYMPTOMS: 91.5% accuracy
# DIET: 94.8% accuracy
# GENERAL: 93.1% accuracy
# OVERALL: 93.9% accuracy
```

### Emergency Detection Evaluation

```python
# File: evaluate_emergency.py
# How you tested the emergency detection

def evaluate_emergency_detection(test_cases):
    """Test emergency detection accuracy"""
    
    # Metrics we need:
    # - True Positive (TP): Correctly identified emergency
    # - False Positive (FP): Normal case flagged as emergency
    # - True Negative (TN): Correctly identified as normal
    # - False Negative (FN): Emergency missed (DANGEROUS!)
    
    tp = fp = tn = fn = 0
    
    for case in test_cases:
        prediction = detector.check_message(case['message'])
        actual = case['is_emergency']
        
        if prediction['is_emergency'] and actual:
            tp += 1
        elif prediction['is_emergency'] and not actual:
            fp += 1
        elif not prediction['is_emergency'] and not actual:
            tn += 1
        else:  # not prediction and actual = MISSED EMERGENCY
            fn += 1
            print(f"⚠️ MISSED: {case['message']}")  # Flag for review
    
    # Calculate metrics
    sensitivity = tp / (tp + fn)  # How many emergencies we catch
    specificity = tn / (tn + fp)  # How many normals we correctly identify
    precision = tp / (tp + fp)    # Of flagged cases, how many are real
    
    print(f"Sensitivity (Recall): {sensitivity:.1%}")  # 98.5%
    print(f"Specificity: {specificity:.1%}")           # 97.9%
    print(f"Precision: {precision:.1%}")               # 95.2%
    print(f"False Negative Rate: {fn/(tp+fn):.1%}")    # 1.5%

# Example test cases:
emergency_test_cases = [
    {"message": "I have severe chest pain right now", "is_emergency": True},
    {"message": "Can't breathe, feeling dizzy", "is_emergency": True},
    {"message": "I had mild chest pain last week", "is_emergency": False},
    {"message": "What time should I take my medicine?", "is_emergency": False},
]
```

**Interview Explanation:**
```
"For emergency detection, we prioritized SENSITIVITY over precision.
Missing an emergency (false negative) could be fatal, while a false
alarm just means unnecessary escalation. We achieved 98.5% sensitivity,
meaning we catch 98.5% of all emergencies. The 1.5% we miss are edge
cases we're continuously improving."
```

### Response Consistency Evaluation

```python
# File: evaluate_consistency.py
# Test if model gives same answer to same question

def test_consistency(model, test_questions, num_runs=5):
    """Check if model gives consistent answers"""
    
    consistency_scores = []
    
    for question in test_questions:
        responses = []
        
        # Ask same question multiple times
        for _ in range(num_runs):
            response = generate_response(model, question)
            responses.append(response)
        
        # Compare responses using embedding similarity
        embeddings = [get_embedding(r) for r in responses]
        similarities = calculate_pairwise_similarity(embeddings)
        avg_similarity = sum(similarities) / len(similarities)
        
        consistency_scores.append(avg_similarity)
    
    print(f"Consistency Score: {sum(consistency_scores)/len(consistency_scores):.1%}")
    # Result: 95.3% consistency
```

## 2.3 Human Evaluation

```python
# Human evaluation process you helped design

# ============================================
# SAMPLE SELECTION
# ============================================
# Randomly select 500 conversations for human review
# Stratified by category to ensure coverage

# ============================================
# EVALUATION CRITERIA
# ============================================
evaluation_criteria = {
    "accuracy": "Is the medical information correct? (1-5)",
    "safety": "Is the advice safe to follow? (1-5)",
    "empathy": "Is the response caring and supportive? (1-5)",
    "clarity": "Is it easy to understand? (1-5)",
    "completeness": "Does it answer the full question? (1-5)"
}

# ============================================
# EVALUATORS
# ============================================
# 3 doctors reviewed each conversation
# Final score = average of 3 ratings

# Results:
# Accuracy: 4.3/5
# Safety: 4.6/5
# Empathy: 4.1/5
# Clarity: 4.4/5
# Overall: 4.2/5
```

## 2.4 A/B Testing

```
A/B TEST SETUP:

Group A (Control): Patients use call center only
Group B (Test): Patients use AI assistant + call center

METRICS TRACKED:
- Query resolution rate
- Time to get answer
- Patient satisfaction score
- Escalation rate to human

RESULTS (after 1 month):
- Group B resolved 64% queries without human
- Average response time: 2 seconds (vs 15 min wait)
- Satisfaction: 4.4/5 (vs 3.8/5 for call center)
```

## 2.5 Evaluation Metrics Summary (Memorize This)

```
KEY METRICS TO MENTION IN INTERVIEWS:

ACCURACY METRICS:
├── Overall Accuracy: 93.9%
├── Medication Questions: 96.2%
├── Symptom Questions: 91.5%
├── Diet Questions: 94.8%
└── General Questions: 93.1%

EMERGENCY DETECTION:
├── Sensitivity: 98.5% (catches emergencies)
├── Specificity: 97.9%
├── Precision: 95.2%
└── False Negative Rate: 1.5%

QUALITY METRICS:
├── Human Evaluation: 4.2/5
├── Response Consistency: 95.3%
└── User Satisfaction: 4.4/5

PERFORMANCE METRICS:
├── Response Time: 1.8 seconds (avg)
├── 95th Percentile: 2.5 seconds
└── Throughput: 1000+ concurrent users
```

---

# PART 3: DEPLOYMENT

## 3.1 Deployment Architecture

```
YOUR ROLE IN DEPLOYMENT:

1. Model optimization using vLLM
2. API endpoint setup with FastAPI
3. Basic load testing
4. Docker containerization support
```

## 3.2 Model Serving with vLLM

```python
# File: model_server.py
# How you set up efficient model serving

from vllm import LLM, SamplingParams

# ============================================
# LOAD MODEL WITH vLLM
# ============================================
# vLLM is 10-20x faster than basic HuggingFace inference
# Key features: PagedAttention, Continuous batching

llm = LLM(
    model="./patient-ai-final",      # Your fine-tuned model
    tensor_parallel_size=1,          # Number of GPUs (1 for our setup)
    gpu_memory_utilization=0.9,      # Use 90% of GPU memory
    max_model_len=2048,              # Maximum context length
)

# ============================================
# SAMPLING PARAMETERS
# ============================================
sampling_params = SamplingParams(
    temperature=0.3,     # Low = more consistent/deterministic
    max_tokens=512,      # Maximum response length
    top_p=0.9,          # Nucleus sampling
    top_k=50,           # Top-k sampling
)

# ============================================
# GENERATION FUNCTION
# ============================================
def generate_response(prompt):
    """Generate response using vLLM"""
    outputs = llm.generate([prompt], sampling_params)
    return outputs[0].outputs[0].text
```

**Interview Explanation:**
```
"We used vLLM for serving because it's much faster than standard
HuggingFace inference. vLLM uses PagedAttention which manages GPU
memory like virtual memory - this allows efficient batching of requests.
We got 10x throughput improvement compared to basic transformers inference."
```

## 3.3 FastAPI Endpoint

```python
# File: api_server.py
# The API you helped build

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI(title="Patient Health Assistant API")

# ============================================
# REQUEST/RESPONSE MODELS
# ============================================
class ChatRequest(BaseModel):
    patient_id: str
    message: str
    language: str = "english"

class ChatResponse(BaseModel):
    response: str
    is_emergency: bool
    response_time_ms: int

# ============================================
# MAIN CHAT ENDPOINT
# ============================================
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint for patient queries"""
    
    start_time = time.time()
    
    try:
        # Step 1: Check for emergencies
        emergency_check = warning_detector.check(request.message)
        
        if emergency_check["is_emergency"]:
            # Alert medical team asynchronously
            alert_medical_team(request.patient_id, request.message)
            response_text = get_emergency_response()
            is_emergency = True
        else:
            # Step 2: Get patient context from database
            patient_context = get_patient_context(request.patient_id)
            
            # Step 3: Search knowledge base (RAG)
            relevant_info = knowledge_base.search(request.message)
            
            # Step 4: Build prompt and generate response
            prompt = build_prompt(request.message, patient_context, relevant_info)
            response_text = generate_response(prompt)
            is_emergency = False
        
        # Calculate response time
        response_time = int((time.time() - start_time) * 1000)
        
        return ChatResponse(
            response=response_text,
            is_emergency=is_emergency,
            response_time_ms=response_time
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# HEALTH CHECK ENDPOINT
# ============================================
@app.get("/health")
async def health_check():
    """Health check for load balancer"""
    return {"status": "healthy", "model_loaded": True}
```

## 3.4 Docker Configuration

```dockerfile
# Dockerfile you helped create

FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Install Python
RUN apt-get update && apt-get install -y python3.10 python3-pip

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Copy model files (or download from S3 at startup)
COPY ./patient-ai-final ./patient-ai-final

EXPOSE 8000

# Run with uvicorn
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 3.5 Load Testing

```python
# File: load_test.py
# Basic load testing you performed

import asyncio
import aiohttp
import time

async def send_request(session, url, payload):
    """Send single request and measure time"""
    start = time.time()
    async with session.post(url, json=payload) as response:
        result = await response.json()
        latency = (time.time() - start) * 1000
        return latency, result

async def load_test(num_requests=100, concurrent=10):
    """Run load test with concurrent requests"""
    
    url = "http://localhost:8000/chat"
    payload = {
        "patient_id": "test123",
        "message": "When should I take my blood pressure medicine?"
    }
    
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, url, payload) for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)
    
    latencies = [r[0] for r in results]
    
    print(f"Total Requests: {num_requests}")
    print(f"Concurrent Users: {concurrent}")
    print(f"Average Latency: {sum(latencies)/len(latencies):.0f} ms")
    print(f"P95 Latency: {sorted(latencies)[int(0.95*len(latencies))]:.0f} ms")
    print(f"Max Latency: {max(latencies):.0f} ms")

# Run load test
asyncio.run(load_test(num_requests=100, concurrent=10))

# Results:
# Average Latency: 1800 ms
# P95 Latency: 2500 ms
# Max Latency: 3200 ms
```

---

# PART 4: INTERVIEW Q&A

## Common Questions You'll Be Asked

### Q1: "Walk me through the fine-tuning process"

```
ANSWER TEMPLATE:

"I fine-tuned Llama-2-7B using QLoRA technique. Here's the process:

1. DATA PREPARATION:
   - We had 25,000 patient Q&A pairs from call center transcripts
   - I formatted them into Llama-2's chat template with system prompts
   - Split 80-10-10 for train/validation/test

2. MODEL LOADING:
   - Loaded base model with 4-bit quantization using BitsAndBytes
   - This reduced memory from 14GB to 4GB

3. LORA CONFIGURATION:
   - Added LoRA adapters to attention layers (q, k, v, o projections)
   - Rank=32, Alpha=64
   - Only 0.06% of parameters trainable

4. TRAINING:
   - 3 epochs, batch size 16, learning rate 2e-4
   - Used SFTTrainer from TRL library
   - Monitored loss on validation set

5. RESULT:
   - Training took 4 hours on single A10G GPU
   - Final loss: 0.598
   - Achieved 93.9% accuracy on test set"
```

### Q2: "Why those specific hyperparameters?"

```
ANSWER:

"I chose these based on experimentation and best practices:

RANK = 32:
- Started with 16, accuracy was 91%
- Increased to 32, accuracy improved to 94%
- Tried 64, minimal improvement but 2x memory usage
- 32 was the sweet spot

LEARNING RATE = 2e-4:
- Standard for LoRA fine-tuning
- Tried 1e-4: slower convergence, similar final accuracy
- Tried 5e-4: faster but less stable

EPOCHS = 3:
- After epoch 3, validation loss started increasing
- Sign of overfitting, so we stopped at 3

BATCH SIZE = 16:
- Limited by GPU memory
- Used gradient accumulation (4 batches × 4 = 16 effective)"
```

### Q3: "How did you evaluate the model?"

```
ANSWER:

"I used multiple evaluation approaches:

1. AUTOMATED EVALUATION:
   - Used GPT-4 as judge to compare model output vs ground truth
   - Scored on accuracy, completeness, safety, clarity (1-5)
   - Category-wise breakdown: Medication 96%, Symptoms 91%, etc.

2. EMERGENCY DETECTION:
   - Created test set of 500 emergency and 500 normal messages
   - Measured sensitivity (98.5%) and specificity (97.9%)
   - Prioritized catching all emergencies (low false negatives)

3. HUMAN EVALUATION:
   - 3 doctors reviewed 500 random conversations
   - Average rating: 4.2/5 across accuracy, safety, empathy

4. CONSISTENCY TESTING:
   - Asked same question 5 times, compared responses
   - 95% semantic similarity - highly consistent

5. PRODUCTION MONITORING:
   - Daily sampling of conversations
   - User feedback collection
   - Alert on anomalous responses"
```

### Q4: "What was the hardest challenge?"

```
ANSWER:

"The hardest challenge was EMERGENCY DETECTION. Missing an emergency
could be life-threatening.

PROBLEM: 
- False negatives (missing emergencies) are unacceptable
- But false positives waste medical team's time

SOLUTION:
1. Two-layer detection: keyword matching + classifier
2. Very low threshold for flagging (0.7 confidence)
3. Human follow-up for ALL flagged cases
4. Continuous improvement based on missed cases

RESULT:
- 98.5% sensitivity (catch 98.5% of emergencies)
- Only 2.1% false positive rate
- 12 lives potentially saved in first 6 months"
```

### Q5: "How did you handle Hindi/Hinglish?"

```
ANSWER:

"We needed to support Hindi because 60% of patients in North India
prefer communicating in Hindi.

APPROACH:
1. Training data included:
   - 60% English (15,000 examples)
   - 30% Hindi (7,500 examples)
   - 10% Hinglish/mixed (2,500 examples)

2. Used actual patient conversations, not translations
   - Translations lose natural phrasing
   - Real conversations capture how patients actually speak

3. Medical terms kept in English
   - 'diabetes', 'blood pressure' understood in both languages
   - Easier for doctors to review

RESULTS:
- English: 95.2% accuracy
- Hindi: 91.8% accuracy  
- Hinglish: 89.5% accuracy

CHALLENGE: Code-switching (mixing languages mid-sentence)
SOLUTION: Training on real Hinglish data improved handling"
```

### Q6: "Why vLLM for deployment?"

```
ANSWER:

"vLLM offers significant performance advantages:

1. PAGED ATTENTION:
   - Manages GPU memory like virtual memory
   - Prevents memory fragmentation
   - Allows serving more concurrent users

2. CONTINUOUS BATCHING:
   - Dynamically batches incoming requests
   - New requests added to batch without waiting
   - 10x throughput vs static batching

3. RESULTS FOR US:
   - Standard inference: ~50 requests/minute
   - vLLM: ~500 requests/minute (10x improvement)
   - Response time: 1.8 seconds average

This was critical because we had 500K+ conversations/month."
```

### Q7: "What would you do differently?"

```
ANSWER:

"Looking back, I would:

1. TRY SMALLER MODELS FIRST:
   - Mistral-7B or Llama-3-8B might work similarly
   - Potentially faster inference and lower cost

2. MORE SYNTHETIC DATA:
   - Getting doctors to annotate was slow
   - Could use GPT-4 to generate more examples
   - Then have doctors verify a sample

3. BETTER EVALUATION PIPELINE:
   - Automated regression tests before each deployment
   - More comprehensive edge case coverage

4. VOICE INTERFACE FROM START:
   - Many elderly patients struggle with typing
   - Voice would improve accessibility

5. ACTIVE LEARNING:
   - Automatically flag low-confidence responses
   - Send for human review and add to training set"
```

---

# PART 5: QUICK REFERENCE CARD

## Numbers to Memorize

```
TRAINING:
├── Training Examples: 25,000
├── Model: Llama-2-7B
├── Technique: QLoRA (r=32, alpha=64)
├── Trainable Parameters: 0.06%
├── Training Time: 4 hours
├── Training Cost: ~₹500
└── GPU: AWS g5.xlarge (A10G 24GB)

ACCURACY:
├── Overall: 93.9%
├── Medication: 96.2%
├── Symptoms: 91.5%
├── Diet: 94.8%
└── Emergency Detection: 98.5% sensitivity

PERFORMANCE:
├── Response Time: 1.8 seconds
├── Concurrent Users: 1000+
├── Uptime: 99.9%
└── Monthly Conversations: 500,000

BUSINESS IMPACT:
├── Call Center Reduction: 64%
├── Readmission Reduction: 39%
├── User Satisfaction: 4.4/5
├── Annual Savings: ₹3.3 crores
└── ROI: 394%
```

## Key Technical Terms

```
QLoRA = Quantized Low-Rank Adaptation
├── Quantization: Compress model to 4-bit
└── LoRA: Train only small adapter layers

RAG = Retrieval Augmented Generation
├── Store knowledge in vector database
├── Retrieve relevant info for each query
└── Provide to LLM for accurate answers

vLLM = Fast LLM serving library
├── PagedAttention: Efficient memory management
└── Continuous Batching: Dynamic request batching

FAISS = Facebook AI Similarity Search
└── Vector database for RAG system

SFTTrainer = Supervised Fine-Tuning Trainer
└── From TRL library, simplifies training
```

## Your Role Summary (for resume/interviews)

```
"As an ML Engineer on the Patient Engagement AI project, I:

• Fine-tuned Llama-2-7B using QLoRA, achieving 93.9% accuracy 
  on patient health queries

• Designed and implemented evaluation framework including 
  automated metrics, emergency detection testing (98.5% 
  sensitivity), and human evaluation protocols

• Optimized model serving using vLLM, achieving 1.8s response 
  time and 1000+ concurrent user support

• Contributed to deployment on AWS, including Docker 
  containerization and load testing

Results: 64% call center reduction, 39% readmission reduction,
₹3.3 crore annual savings"
```

---

# PART 6: PRACTICE EXERCISES

## Exercise 1: Explain QLoRA to a Non-Technical Person

```
PRACTICE THIS:

"Imagine you want to teach a doctor to specialize in cardiology.
You don't restart their entire medical education - you add 
specialized training on top of what they already know.

That's what QLoRA does:
- The base model (Llama) already knows language and general knowledge
- We add a small 'specialization layer' for healthcare
- This layer is only 0.06% of the model
- Much faster and cheaper than retraining everything"
```

## Exercise 2: Whiteboard the Architecture

```
PRACTICE DRAWING THIS:

Patient → API Gateway → Load Balancer → GPU Server
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
              Emergency           RAG Knowledge            Patient
              Detector            Base Search              Context
                    │                      │                      │
                    └──────────────────────┼──────────────────────┘
                                           │
                                      LLM (Llama-2)
                                           │
                                      Response
```

## Exercise 3: Debugging Scenario

```
SCENARIO: "Model accuracy dropped from 94% to 85% after 
           deploying a new version. How would you debug?"

YOUR ANSWER:

1. CHECK DATA DRIFT:
   "First, I'd compare recent queries to training data distribution.
    Maybe patients are asking different types of questions."

2. CHECK MODEL WEIGHTS:
   "Verify the correct model version was deployed.
    Compare checksums of model files."

3. SAMPLE FAILING CASES:
   "Look at specific queries where accuracy dropped.
    Are they a new category we didn't train on?"

4. CHECK INFRASTRUCTURE:
   "Verify GPU memory, batch sizes, no resource contention.
    Performance issues can affect quality."

5. ROLLBACK:
   "If critical, rollback to previous version while investigating."
```
