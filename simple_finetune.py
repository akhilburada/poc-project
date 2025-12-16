# Simple Phi-3 Mini Fine-tuning Script
# Run in Google Colab with GPU enabled

# Step 1: Install packages (run this first in Colab)
# !pip install -q transformers peft bitsandbytes trl accelerate datasets

import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

# Step 2: Your training data
data = [
    {"input": "Rewrite to be friendlier: 'Send me the report by EOD.'", "output": "Could you please send me the report by end of day? Thanks!"},
    {"input": "Make more professional: 'Your app is broken. Fix it.'", "output": "It looks like the application isn't working as expected. Could you investigate and provide a fix?"},
    {"input": "Simplify: 'Subsequent to our prior correspondence, I am following up.'", "output": "I'm following up on our previous message."},
    {"input": "Rewrite as a short SMS: 'I will be 10 minutes late due to traffic.'", "output": "Running ~10 mins late—traffic. See you soon."},
    {"input": "Fix grammar: 'Me and Alex were going to the store yesterday.'", "output": "Alex and I went to the store yesterday."},
    {"input": "Make less harsh: 'This is wrong. Do it again.'", "output": "I think there's an issue with this—could you revise it and try again?"},
    {"input": "Shorten: 'At this point in time we are unable to proceed.'", "output": "We can't proceed right now."},
    {"input": "Rewrite to sound confident: 'I think I can do this project.'", "output": "I'm confident I can deliver this project successfully."},
    {"input": "Make concise: 'Please be advised that your request has been received.'", "output": "We received your request."},
    {"input": "Summarize: 'We paused the rollout after error rates rose. We are investigating.'", "output": "Rollout paused due to errors; investigating now."},
]

# Step 3: Format data for Phi-3
def format_prompt(sample):
    return f"""<|user|>
{sample['input']}<|end|>
<|assistant|>
{sample['output']}<|end|>"""

dataset = Dataset.from_list([{"text": format_prompt(s)} for s in data])

# Step 4: Load model (4-bit to save memory)
model_id = "microsoft/Phi-3-mini-4k-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16),
    device_map="auto",
    trust_remote_code=True,
)

# Step 5: Add LoRA adapters
model = get_peft_model(model, LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    task_type="CAUSAL_LM",
))

# Step 6: Train
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=256,
    args=TrainingArguments(
        output_dir="./model",
        num_train_epochs=3,
        per_device_train_batch_size=1,
        learning_rate=2e-4,
        bf16=True,
        logging_steps=5,
        save_strategy="no",
    ),
)

trainer.train()

# Step 7: Save
trainer.save_model("./my-phi3-model")
tokenizer.save_pretrained("./my-phi3-model")
print("Done! Model saved to ./my-phi3-model")

# Step 8: Test
def ask(prompt):
    inputs = tokenizer(f"<|user|>\n{prompt}<|end|>\n<|assistant|>\n", return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=50, do_sample=False)
    return tokenizer.decode(output[0], skip_special_tokens=True).split("<|assistant|>")[-1].strip()

print("\nTest:")
print(ask("Make friendlier: 'Do this now.'"))
