"""
Configuration settings for the SLM Healthcare POC
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class ModelConfig:
    """Model configuration settings"""
    # Using DistilGPT2 - a lightweight, CPU-friendly model
    # Can be swapped with other models like:
    # - "microsoft/DialoGPT-small" 
    # - "TinyLlama/TinyLlama-1.1B-Chat-v1.0" (if more RAM available)
    # - "facebook/opt-125m"
    model_name: str = "distilgpt2"
    max_length: int = 512
    num_train_epochs: int = 3
    learning_rate: float = 5e-5
    batch_size: int = 4
    warmup_steps: int = 100
    weight_decay: float = 0.01
    gradient_accumulation_steps: int = 2
    
    # LoRA Configuration for efficient fine-tuning
    lora_r: int = 8
    lora_alpha: int = 32
    lora_dropout: float = 0.1
    
    # CPU-specific optimizations
    use_cpu: bool = True
    num_workers: int = 2
    
@dataclass
class AppConfig:
    """Application configuration settings"""
    upload_folder: str = "uploads"
    model_output_dir: str = "trained_models"
    max_file_size_mb: int = 100
    supported_formats: tuple = (".txt", ".csv", ".json", ".pdf", ".docx")
    
    # Training constraints for POC (5 minute target)
    max_training_samples: int = 1000
    max_training_time_seconds: int = 300  # 5 minutes
    
    # Streamlit settings
    page_title: str = "Healthcare SLM Fine-tuning POC"
    page_icon: str = "🏥"


# Create config instances
model_config = ModelConfig()
app_config = AppConfig()

# Create necessary directories
os.makedirs(app_config.upload_folder, exist_ok=True)
os.makedirs(app_config.model_output_dir, exist_ok=True)
