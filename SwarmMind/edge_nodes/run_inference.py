import sys
import os
import warnings
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, logging


sys.stdout.reconfigure(encoding='utf-8')
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
warnings.filterwarnings("ignore")
logging.set_verbosity_error()


model_name = "Qwen/Qwen2.5-0.5B-Instruct"

try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype=torch.float16, 
        device_map="auto",
        low_cpu_mem_usage=True,
        offload_folder="offload" 
    )
except Exception as e:
    print(f"CRITICAL MODEL ERROR: {str(e)}")
    sys.exit(1)

def get_expert_response(user_input):
    messages = [
        {"role": "system", "content": "You are a strict, expert AI. For math questions, provide only the step-by-step solution. For coding questions, provide only the highly optimized code without any conversational filler or pleasantries."},
        {"role": "user", "content": user_input}
    ]
    
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
   
    inputs = tokenizer([text], return_tensors="pt").to(model.device) 
    
    with torch.no_grad():
        output_tokens = model.generate(
            **inputs, 
            max_new_tokens=512,  
            temperature=0.1,     
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id 
        )
    
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, output_tokens)]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Prompt nahi mila.")
        sys.exit(1)
    
    try:
        answer = get_expert_response(sys.argv[1])
        print(answer)
    except Exception as e:
        print(f"CRITICAL GENERATION ERROR: {str(e)}")
        sys.exit(1)