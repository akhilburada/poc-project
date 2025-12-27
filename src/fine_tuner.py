"""
Fine-tuning module for CPU-based SLM training
Uses LoRA (Low-Rank Adaptation) for efficient fine-tuning
"""
import os
import time
import torch
from typing import List, Dict, Callable, Optional
from dataclasses import dataclass
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    TrainerCallback
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset
import json


@dataclass
class TrainingMetrics:
    """Container for training metrics"""
    epoch: float
    step: int
    loss: float
    learning_rate: float
    timestamp: float


class MetricsCallback(TrainerCallback):
    """Custom callback to capture training metrics in real-time"""
    
    def __init__(self, metrics_handler: Callable[[TrainingMetrics], None]):
        self.metrics_handler = metrics_handler
        self.start_time = None
    
    def on_train_begin(self, args, state, control, **kwargs):
        self.start_time = time.time()
    
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs and 'loss' in logs:
            metrics = TrainingMetrics(
                epoch=state.epoch or 0,
                step=state.global_step,
                loss=logs.get('loss', 0),
                learning_rate=logs.get('learning_rate', 0),
                timestamp=time.time() - self.start_time if self.start_time else 0
            )
            self.metrics_handler(metrics)


class HealthcareSLMFineTuner:
    """Fine-tuner for healthcare domain SLM"""
    
    def __init__(
        self,
        model_name: str = "distilgpt2",
        output_dir: str = "trained_models",
        use_lora: bool = True
    ):
        self.model_name = model_name
        self.output_dir = output_dir
        self.use_lora = use_lora
        self.model = None
        self.tokenizer = None
        self.training_history: List[TrainingMetrics] = []
        self.is_trained = False
        
    def load_model(self, progress_callback: Optional[Callable] = None):
        """Load the base model and tokenizer"""
        if progress_callback:
            progress_callback("Loading tokenizer...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # Set padding token if not exists
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        if progress_callback:
            progress_callback("Loading model...")
        
        # Load model with CPU optimization
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,  # CPU uses float32
            low_cpu_mem_usage=True
        )
        
        if self.use_lora:
            if progress_callback:
                progress_callback("Applying LoRA configuration...")
            
            # Configure LoRA for efficient fine-tuning
            lora_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                r=8,
                lora_alpha=32,
                lora_dropout=0.1,
                target_modules=["c_attn", "c_proj"],  # GPT-2 specific
                bias="none"
            )
            
            self.model = get_peft_model(self.model, lora_config)
            
            # Print trainable parameters
            trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
            total_params = sum(p.numel() for p in self.model.parameters())
            
            if progress_callback:
                progress_callback(
                    f"LoRA applied: {trainable_params:,} trainable / {total_params:,} total "
                    f"({100 * trainable_params / total_params:.2f}%)"
                )
        
        return self
    
    def prepare_dataset(
        self,
        conversations: List[Dict[str, str]],
        max_length: int = 256
    ) -> Dataset:
        """Prepare dataset for training"""
        
        def format_conversation(item):
            """Format as instruction-following prompt"""
            return f"### Instruction:\n{item['instruction']}\n\n### Response:\n{item['response']}"
        
        # Format all conversations
        formatted_texts = [format_conversation(conv) for conv in conversations]
        
        # Tokenize
        def tokenize_function(examples):
            tokenized = self.tokenizer(
                examples['text'],
                truncation=True,
                padding='max_length',
                max_length=max_length,
                return_tensors=None
            )
            tokenized['labels'] = tokenized['input_ids'].copy()
            return tokenized
        
        dataset = Dataset.from_dict({'text': formatted_texts})
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=['text']
        )
        
        return tokenized_dataset
    
    def train(
        self,
        conversations: List[Dict[str, str]],
        num_epochs: int = 3,
        batch_size: int = 4,
        learning_rate: float = 5e-5,
        max_steps: int = -1,
        metrics_callback: Optional[Callable[[TrainingMetrics], None]] = None,
        progress_callback: Optional[Callable] = None
    ):
        """Fine-tune the model on healthcare data"""
        
        if self.model is None:
            self.load_model(progress_callback)
        
        if progress_callback:
            progress_callback("Preparing dataset...")
        
        # Prepare dataset
        train_dataset = self.prepare_dataset(conversations)
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False  # Causal LM, not masked LM
        )
        
        # Training arguments optimized for CPU
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=2,
            learning_rate=learning_rate,
            weight_decay=0.01,
            warmup_steps=50,
            logging_steps=5,
            save_steps=100,
            save_total_limit=2,
            max_steps=max_steps if max_steps > 0 else -1,
            no_cuda=True,  # Force CPU
            dataloader_num_workers=0,  # Avoid multiprocessing issues
            fp16=False,  # CPU doesn't support fp16
            report_to="none",  # Disable wandb, etc.
            logging_first_step=True,
        )
        
        # Create callbacks list
        callbacks = []
        if metrics_callback:
            callbacks.append(MetricsCallback(metrics_callback))
        
        if progress_callback:
            progress_callback("Starting training...")
        
        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            data_collator=data_collator,
            callbacks=callbacks
        )
        
        # Train
        self.training_history = []
        train_result = trainer.train()
        
        self.is_trained = True
        
        if progress_callback:
            progress_callback("Training complete! Saving model...")
        
        # Save the model
        self.save_model()
        
        return train_result
    
    def save_model(self, path: Optional[str] = None):
        """Save the fine-tuned model"""
        save_path = path or os.path.join(self.output_dir, "healthcare_slm")
        
        if self.use_lora:
            # Save only LoRA weights
            self.model.save_pretrained(save_path)
        else:
            self.model.save_pretrained(save_path)
        
        self.tokenizer.save_pretrained(save_path)
        
        # Save training history
        history_path = os.path.join(save_path, "training_history.json")
        with open(history_path, 'w') as f:
            json.dump(
                [{'epoch': m.epoch, 'step': m.step, 'loss': m.loss, 
                  'lr': m.learning_rate, 'time': m.timestamp} 
                 for m in self.training_history],
                f
            )
    
    def generate_response(
        self,
        instruction: str,
        max_new_tokens: int = 150,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """Generate a response for the given instruction"""
        
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Format the prompt
        prompt = f"### Instruction:\n{instruction}\n\n### Response:\n"
        
        # Tokenize
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=256
        )
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the response part
        if "### Response:" in full_response:
            response = full_response.split("### Response:")[-1].strip()
        else:
            response = full_response[len(prompt):].strip()
        
        return response


class BaselineModel:
    """Baseline model without fine-tuning for comparison"""
    
    def __init__(self, model_name: str = "distilgpt2"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
    
    def load(self):
        """Load the baseline model"""
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        self.model.eval()
        return self
    
    def generate(self, instruction: str, max_new_tokens: int = 150) -> str:
        """Generate response without fine-tuning"""
        if self.model is None:
            self.load()
        
        prompt = f"### Instruction:\n{instruction}\n\n### Response:\n"
        
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=256
        )
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_new_tokens=max_new_tokens,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
        
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if "### Response:" in full_response:
            response = full_response.split("### Response:")[-1].strip()
        else:
            response = full_response[len(prompt):].strip()
        
        return response
