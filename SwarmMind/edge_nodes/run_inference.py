import sys
import os
import torch
from huggingface_hub import login
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(token=hf_token)

model_name = "google/gemma-3-4b-it"

try:
    print("DEBUG: Loading model...", file=sys.stderr)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True
        
    )
    
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        low_cpu_mem_usage=True
        
    )
    print("DEBUG: Model loaded successfully!", file=sys.stderr)

except Exception as e:
    print(f"ASLI ERROR YE HAI: {e}", file=sys.stderr)
    sys.exit(1)

def get_expert_response(user_input):
   
    system_content = "You are a concise AI assistant. Provide direct answers. Do not repeat previous conversations."
    
   
    prompt = f"System: {system_content}\nUser: {user_input}\nAssistant:"
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        output_tokens = model.generate(
            **inputs,
            max_new_tokens=100, 
            temperature=0.2,    
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.5 
        )
    
    input_length = inputs['input_ids'].shape[-1]
    response = tokenizer.decode(output_tokens[0][input_length:], skip_special_tokens=True)
    
    return response.split("\n")[0].strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    print(get_expert_response(sys.argv[1]))