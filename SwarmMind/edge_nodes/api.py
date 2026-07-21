from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

import rag_system  # Import RAG system

app = FastAPI()

# Global variables for model
model = None
tokenizer = None

@app.on_event("startup")
async def startup_event():
    global model, tokenizer
    
    # Initialize RAG (only once at startup)
    rag_system.index_knowledge_base()
    
    print("🔄 Loading Model into VRAM... Please wait.")
    model_name = "google/gemma-3-4b-it"

    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        quantization_config=bnb_config, 
        device_map="auto"
    )
    print("✅ Model Successfully Loaded! API is ready on port 8000.")

class Query(BaseModel):
    prompt: str

@app.post("/generate")
def generate_text(query: Query):
    try:
        # --- RAG: Get relevant context ---
        context = rag_system.retrieve_context(query.prompt)
        
        # --- Build prompt with context ---
        if context:
            system_instruction = f"System: You are a helpful AI assistant. Use the following context if relevant:\n{context}\n"
        else:
            system_instruction = "System: You are a helpful AI assistant."
        
        full_prompt = f"{system_instruction}\nUser: {query.prompt}\nAssistant:"
        
        # --- Generate response ---
        inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            output_tokens = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.2
            )
        
        input_length = inputs['input_ids'].shape[-1]
        response = tokenizer.decode(output_tokens[0][input_length:], skip_special_tokens=True)
        
        return {"response": response.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)