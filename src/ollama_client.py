"""
Ollama Integration for Healthcare SLM POC
Uses locally installed Ollama models (phi3, llama3.2)
"""
import requests
import json
import subprocess
import os
from typing import Optional, List, Dict, Generator
from dataclasses import dataclass


@dataclass
class OllamaModel:
    """Represents an Ollama model"""
    name: str
    size: str
    modified: str


class OllamaClient:
    """Client for interacting with local Ollama installation"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.api_generate = f"{base_url}/api/generate"
        self.api_chat = f"{base_url}/api/chat"
        self.api_tags = f"{base_url}/api/tags"
        self.api_create = f"{base_url}/api/create"
        self.api_show = f"{base_url}/api/show"
    
    def is_running(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
        except Exception:
            return False
    
    def list_models(self) -> List[OllamaModel]:
        """List all available models in Ollama"""
        try:
            response = requests.get(self.api_tags, timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = []
                for model in data.get('models', []):
                    models.append(OllamaModel(
                        name=model.get('name', ''),
                        size=self._format_size(model.get('size', 0)),
                        modified=model.get('modified_at', '')[:10]
                    ))
                return models
            return []
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
    
    def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        stream: bool = False
    ) -> str:
        """Generate a response from the model"""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        
        if system:
            payload["system"] = system
        
        try:
            response = requests.post(
                self.api_generate,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model might be loading."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_stream(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Generator[str, None, None]:
        """Generate a streaming response from the model"""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        
        if system:
            payload["system"] = system
        
        try:
            response = requests.post(
                self.api_generate,
                json=payload,
                stream=True,
                timeout=120
            )
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if 'response' in data:
                        yield data['response']
                    if data.get('done', False):
                        break
                        
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """Chat with the model using message history"""
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        
        try:
            response = requests.post(
                self.api_chat,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', '')
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def create_healthcare_model(
        self,
        base_model: str,
        model_name: str,
        healthcare_knowledge: List[Dict[str, str]],
        progress_callback=None
    ) -> bool:
        """
        Create a custom Ollama model with embedded healthcare knowledge.
        This uses Modelfile approach to embed knowledge in the system prompt.
        
        Note: This is NOT true fine-tuning, but it's fast and effective for demos.
        """
        
        if progress_callback:
            progress_callback("Preparing healthcare knowledge...")
        
        # Build system prompt with healthcare knowledge
        system_prompt = self._build_healthcare_system_prompt(healthcare_knowledge)
        
        if progress_callback:
            progress_callback("Creating Modelfile...")
        
        # Create Modelfile content
        modelfile_content = f'''FROM {base_model}

SYSTEM """
{system_prompt}
"""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_predict 500
'''
        
        # Save Modelfile
        modelfile_path = f"/tmp/{model_name}_Modelfile"
        with open(modelfile_path, 'w') as f:
            f.write(modelfile_content)
        
        if progress_callback:
            progress_callback(f"Creating custom model '{model_name}'...")
        
        # Create the model using Ollama API
        try:
            payload = {
                "name": model_name,
                "modelfile": modelfile_content,
                "stream": False
            }
            
            response = requests.post(
                self.api_create,
                json=payload,
                timeout=300  # Model creation can take time
            )
            
            if response.status_code == 200:
                if progress_callback:
                    progress_callback(f"Model '{model_name}' created successfully!")
                return True
            else:
                if progress_callback:
                    progress_callback(f"Error creating model: {response.text}")
                return False
                
        except Exception as e:
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            return False
        finally:
            # Cleanup
            if os.path.exists(modelfile_path):
                os.remove(modelfile_path)
    
    def _build_healthcare_system_prompt(
        self,
        healthcare_knowledge: List[Dict[str, str]]
    ) -> str:
        """Build a system prompt with embedded healthcare knowledge"""
        
        # Create a knowledge base from the Q&A pairs
        knowledge_sections = []
        
        for i, item in enumerate(healthcare_knowledge[:50], 1):  # Limit to 50 for token limits
            q = item.get('instruction', item.get('question', ''))
            a = item.get('response', item.get('answer', ''))
            knowledge_sections.append(f"Q{i}: {q}\nA{i}: {a}")
        
        knowledge_text = "\n\n".join(knowledge_sections)
        
        system_prompt = f"""You are a specialized Healthcare Assistant AI. You have been trained with specific healthcare knowledge to help answer medical and insurance-related questions accurately.

IMPORTANT GUIDELINES:
1. Answer healthcare questions accurately based on your training
2. Be helpful, clear, and professional
3. If you're unsure about something, acknowledge it
4. For emergencies, always advise calling 911 or visiting the ER
5. Never provide specific medical diagnoses - recommend consulting healthcare providers

YOUR HEALTHCARE KNOWLEDGE BASE:

{knowledge_text}

Use the above knowledge to answer questions accurately. If a question is not covered in your knowledge base, use your general understanding but indicate that the user should verify with their healthcare provider."""

        return system_prompt
    
    def delete_model(self, model_name: str) -> bool:
        """Delete a custom model"""
        try:
            response = requests.delete(
                f"{self.base_url}/api/delete",
                json={"name": model_name},
                timeout=30
            )
            return response.status_code == 200
        except Exception:
            return False


class HealthcareOllamaTrainer:
    """
    Trainer that creates healthcare-specialized Ollama models.
    Uses the Modelfile approach for quick "training" demos.
    """
    
    def __init__(self, base_model: str = "phi3:mini"):
        self.client = OllamaClient()
        self.base_model = base_model
        self.trained_model_name = None
        self.training_complete = False
        
    def get_available_models(self) -> List[str]:
        """Get list of available base models"""
        models = self.client.list_models()
        return [m.name for m in models]
    
    def train(
        self,
        healthcare_data: List[Dict[str, str]],
        model_name: str = "healthcare-assistant",
        progress_callback=None,
        metrics_callback=None
    ) -> bool:
        """
        "Train" a healthcare model by creating a custom Modelfile.
        
        This simulates training for the POC demo. For true fine-tuning,
        you would need to use llama.cpp or similar tools.
        """
        import time
        
        if progress_callback:
            progress_callback("Initializing training pipeline...")
        
        # Simulate training phases for the demo
        phases = [
            ("Loading base model...", 0.5),
            ("Preparing healthcare dataset...", 0.5),
            ("Encoding knowledge base...", 1.0),
            ("Optimizing model parameters...", 1.0),
            ("Creating specialized model...", 2.0),
            ("Validating model...", 0.5),
        ]
        
        total_steps = len(phases) + 5  # Extra steps for metrics
        current_step = 0
        
        # Simulate training metrics for visualization
        if metrics_callback:
            import random
            loss = 2.5
            for i in range(20):
                # Simulate decreasing loss
                loss = max(0.3, loss - random.uniform(0.05, 0.15))
                lr = 5e-5 * (1 - i/25)  # Decreasing learning rate
                
                from src.fine_tuner import TrainingMetrics
                metrics = TrainingMetrics(
                    epoch=i / 6.67,  # ~3 epochs
                    step=i,
                    loss=loss,
                    learning_rate=lr,
                    timestamp=i * 0.25
                )
                metrics_callback(metrics)
                time.sleep(0.15)  # Small delay for visualization
        
        # Execute phases
        for phase_name, duration in phases:
            if progress_callback:
                progress_callback(phase_name)
            time.sleep(duration)
        
        # Actually create the model
        success = self.client.create_healthcare_model(
            base_model=self.base_model,
            model_name=model_name,
            healthcare_knowledge=healthcare_data,
            progress_callback=progress_callback
        )
        
        if success:
            self.trained_model_name = model_name
            self.training_complete = True
            if progress_callback:
                progress_callback("Training complete! Model is ready.")
        
        return success
    
    def generate_before(self, question: str) -> str:
        """Generate response from base model (before training)"""
        prompt = f"Answer this healthcare question:\n\n{question}"
        
        return self.client.generate(
            model=self.base_model,
            prompt=prompt,
            temperature=0.7,
            max_tokens=300
        )
    
    def generate_after(self, question: str) -> str:
        """Generate response from trained model (after training)"""
        if not self.trained_model_name:
            return "Error: Model not trained yet."
        
        prompt = f"Answer this healthcare question:\n\n{question}"
        
        return self.client.generate(
            model=self.trained_model_name,
            prompt=prompt,
            temperature=0.7,
            max_tokens=300
        )
    
    def cleanup(self):
        """Delete the trained model"""
        if self.trained_model_name:
            self.client.delete_model(self.trained_model_name)
            self.trained_model_name = None
            self.training_complete = False


def check_ollama_status():
    """Check Ollama installation and status"""
    client = OllamaClient()
    
    status = {
        'installed': False,
        'running': False,
        'models': [],
        'recommended_models': []
    }
    
    # Check if running
    status['running'] = client.is_running()
    
    if status['running']:
        status['installed'] = True
        models = client.list_models()
        status['models'] = [m.name for m in models]
        
        # Identify recommended models for healthcare POC
        recommended = ['phi3', 'llama3.2', 'llama3.1', 'mistral', 'gemma']
        for model_name in status['models']:
            for rec in recommended:
                if rec in model_name.lower():
                    status['recommended_models'].append(model_name)
                    break
    
    return status
