#!/usr/bin/env python3
"""
Fine-tune Phi-3 Mini for Text Rewriting Tasks using QLoRA

This script fine-tunes Microsoft's Phi-3 Mini model on a custom text rewriting
dataset using QLoRA (4-bit quantization + LoRA) for memory efficiency.

Usage:
    python finetune_phi3.py --data training_data.json --output ./phi3-finetuned

Requirements:
    pip install transformers>=4.40.0 peft>=0.10.0 bitsandbytes>=0.43.0
    pip install trl>=0.8.0 accelerate>=0.28.0 datasets>=2.18.0
"""

import argparse
import json
import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer


def load_data(data_path: str) -> list:
    """Load training data from JSON file."""
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✅ Loaded {len(data)} training examples from {data_path}")
    return data


def format_instruction(sample: dict) -> str:
    """Format a single example into Phi-3's chat format."""
    system_message = "You are a helpful text rewriting assistant. Transform the input text as instructed."
    
    formatted = f"""<|system|>
{system_message}<|end|>
<|user|>
{sample['input']}<|end|>
<|assistant|>
{sample['output']}<|end|>"""
    
    return formatted


def create_dataset(data: list) -> Dataset:
    """Create a HuggingFace Dataset from the training data."""
    formatted_data = [{"text": format_instruction(sample)} for sample in data]
    dataset = Dataset.from_list(formatted_data)
    print(f"✅ Created dataset with {len(dataset)} examples")
    return dataset


def load_model_and_tokenizer(model_id: str):
    """Load the model and tokenizer with 4-bit quantization."""
    print(f"🚀 Loading model: {model_id}")
    
    # 4-bit quantization config
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        trust_remote_code=True,
        use_fast=True
    )
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    
    # Load model with quantization
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        attn_implementation="eager",
    )
    
    model.config.use_cache = False
    model.config.pretraining_tp = 1
    
    print(f"✅ Model loaded! Memory: ~{model.get_memory_footprint() / 1e9:.2f} GB")
    
    return model, tokenizer


def setup_lora(model):
    """Configure and apply LoRA adapters to the model."""
    model = prepare_model_for_kbit_training(model)
    
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    return model


def create_trainer(
    model,
    tokenizer,
    dataset: Dataset,
    output_dir: str,
    epochs: int = 3,
    batch_size: int = 2,
    learning_rate: float = 2e-4,
):
    """Create the SFTTrainer with training arguments."""
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=4,
        learning_rate=learning_rate,
        weight_decay=0.01,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        optim="paged_adamw_8bit",
        fp16=False,
        bf16=True,
        gradient_checkpointing=True,
        max_grad_norm=0.3,
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=2,
        report_to="none",
        seed=42,
    )
    
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        dataset_text_field="text",
        max_seq_length=512,
        packing=False,
    )
    
    return trainer


def generate_response(model, tokenizer, prompt: str, max_new_tokens: int = 128) -> str:
    """Generate a response using the fine-tuned model."""
    system_message = "You are a helpful text rewriting assistant. Transform the input text as instructed."
    
    formatted_prompt = f"""<|system|>
{system_message}<|end|>
<|user|>
{prompt}<|end|>
<|assistant|>
"""
    
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id,
        )
    
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    response = full_response.split("<|assistant|>")[-1].replace("<|end|>", "").strip()
    
    return response


def main():
    parser = argparse.ArgumentParser(description="Fine-tune Phi-3 Mini for text rewriting")
    parser.add_argument("--data", type=str, default="training_data.json", help="Path to training data JSON")
    parser.add_argument("--output", type=str, default="./phi3-text-rewriter", help="Output directory")
    parser.add_argument("--model", type=str, default="microsoft/Phi-3-mini-4k-instruct", help="Base model ID")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=2, help="Batch size per device")
    parser.add_argument("--lr", type=float, default=2e-4, help="Learning rate")
    parser.add_argument("--test-only", action="store_true", help="Skip training, only test")
    
    args = parser.parse_args()
    
    # Check GPU
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️ No GPU detected! Training will be slow.")
    
    # Load data
    data = load_data(args.data)
    dataset = create_dataset(data)
    
    # Load model
    model, tokenizer = load_model_and_tokenizer(args.model)
    
    if not args.test_only:
        # Setup LoRA
        model = setup_lora(model)
        
        # Create trainer
        trainer = create_trainer(
            model=model,
            tokenizer=tokenizer,
            dataset=dataset,
            output_dir=args.output,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.lr,
        )
        
        # Train
        print("\n🎯 Starting fine-tuning...")
        print("=" * 50)
        torch.cuda.empty_cache()
        trainer.train()
        print("=" * 50)
        print("✅ Training complete!")
        
        # Save
        trainer.save_model(f"{args.output}-final")
        tokenizer.save_pretrained(f"{args.output}-final")
        print(f"✅ Model saved to: {args.output}-final")
    
    # Test
    print("\n📝 Testing the model:")
    print("=" * 50)
    
    test_prompts = [
        "Rewrite to be friendlier: 'Get this done now.'",
        "Simplify: 'In accordance with the aforementioned guidelines...'",
        "Make more professional: 'This looks bad.'",
    ]
    
    for prompt in test_prompts:
        print(f"\n📥 Input: {prompt}")
        response = generate_response(model, tokenizer, prompt)
        print(f"📤 Output: {response}")
        print("-" * 50)


if __name__ == "__main__":
    main()
