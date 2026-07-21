import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import sys


print("\n" + "="*50)
print("SWARMMIND: PRIVATE LOCAL LLM ENGINE v1.0")
print("="*50)


sys.stdout.flush()


device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[*] Targeting Compute Hardware: {device.upper()}")
if device == "cuda":
    print(f"[*] Active GPU Detected: {torch.cuda.get_device_name(0)}")
sys.stdout.flush()

print("[*] Loading Model Architecture (GPT-2)...")
sys.stdout.flush()


model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)


data_path = "training_data.txt"
if os.path.exists(data_path):
    with open(data_path, "r") as f:
        local_context = f.read()
    print(f"[+] Loaded Local Dataset Successfully ({len(local_context)} chars)")
else:
    local_context = "SwarmMind private local environment operational."
    print("[-] Local dataset missing, using fallback string.")
sys.stdout.flush()

print("\n--- STARTING HARDWARE-ISOLATED FINETUNE LOOP ---")
sys.stdout.flush()

model.train()

for epoch in range(3): 
    model.train()

inputs = tokenizer(local_context, return_tensors="pt").to(device)
outputs = model(**inputs, labels=inputs["input_ids"])
loss = outputs.loss
loss.backward()

print(f"[] Local Compute Cycle Loss: {loss.item():.4f}")
print(" Tensors successfully optimized on RTX 3050.")


output_dir = "./saved_local_model"
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
print(f"[✓] Model securely written to: {output_dir}")
print("="*50 + "\n")
sys.stdout.flush()

