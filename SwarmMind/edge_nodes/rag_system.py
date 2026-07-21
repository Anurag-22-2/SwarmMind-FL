# rag_system.py
import sys
import json
import chromadb
from chromadb.utils import embedding_functions
from ddgs import DDGS

# --- Setup ChromaDB (Persistent) ---
chroma_client = chromadb.PersistentClient(path="./vector_store")
# Ye default embedding hai, koi heavy DLL load nahi karta
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

knowledge_collection = chroma_client.get_or_create_collection(
    name="swarmmind_knowledge",
    embedding_function=embedding_fn
)

memory_collection = chroma_client.get_or_create_collection(
    name="swarmmind_memory",
    embedding_function=embedding_fn
)

# --- Helper Functions ---
def chunk_text(text, chunk_size=150, overlap=30):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunks.append(" ".join(words[start:start + chunk_size]))
        start += chunk_size - overlap
    return chunks

def index_knowledge_base(path="knowledge_base.txt"):
    try:
        with open(path, encoding="utf-8") as f:
            raw_text = f.read()
        all_chunks = []
        for paragraph in raw_text.split("\n\n"):
            if paragraph.strip():
                all_chunks.extend(chunk_text(paragraph.strip()))
        
        if all_chunks:
            already_indexed = knowledge_collection.count()
            knowledge_collection.add(
                documents=all_chunks,
                ids=[f"chunk_{already_indexed + i}" for i in range(len(all_chunks))]
            )
            print(f"Indexed {len(all_chunks)} chunks", file=sys.stderr)
    except FileNotFoundError:
        print("knowledge_base.txt not found", file=sys.stderr)

def retrieve_context(query, top_k=2, max_distance=0.8):
    if knowledge_collection.count() == 0:
        return None
    results = knowledge_collection.query(query_texts=[query], n_results=top_k)
    docs = results["documents"][0]
    distances = results["distances"][0]
    relevant = [d for d, dist in zip(docs, distances) if dist < max_distance]
    return "\n\n".join(relevant) if relevant else None

def save_to_memory(prompt, response, turn_id):
    memory_collection.add(
        documents=[f"User asked: {prompt}\nAnswer given: {response}"],
        ids=[f"memory_{turn_id}"]
    )

def recall_relevant_memory(query, top_k=1, max_distance=0.8):
    if memory_collection.count() == 0:
        return None
    results = memory_collection.query(query_texts=[query], n_results=top_k)
    docs, distances = results["documents"][0], results["distances"][0]
    relevant = [d for d, dist in zip(docs, distances) if dist < max_distance]
    return "\n\n".join(relevant) if relevant else None

def web_search(query, max_results=3):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return None
        return "\n\n".join(f"{r['title']}: {r['body']}" for r in results)
    except Exception as e:
        print(f"Web search failed: {e}", file=sys.stderr)
        return None

# --- Main Agent Logic ---
# Note: You need to import your actual generate function from run_inference.py
# For now, this is a placeholder structure based on your guide.
def agent_respond(user_prompt, conversation_history, generate_func, model, tokenizer, gen_config):
    # 1. Check Local Knowledge First
    context = retrieve_context(user_prompt)
    
    # 2. Check Memory
    memory = recall_relevant_memory(user_prompt)
    
    system_instruction = "You are a helpful assistant. Use the provided context to answer."
    if context:
        system_instruction += f"\n\nRelevant Context:\n{context}"
    if memory:
        system_instruction += f"\n\nPast Memory:\n{memory}"

    # Simple fallback: If no context found, try Web Search (Optional based on Part 3)
    if not context and not memory:
        # web_result = web_search(user_prompt) # Uncomment if you want auto web search
        # if web_result: system_instruction += f"\n\nWeb Info:\n{web_result}"
        pass

    # Call your existing inference function
    # Assuming your run_inference.py has a function called 'generate'
    final_prompt = f"{system_instruction}\n\nUser: {user_prompt}\nAssistant:"
    
    # IMPORTANT: Replace this line with your actual model call from run_inference.py
    # answer = generate(model, tokenizer, final_prompt, gen_config) 
    answer = "Model generation logic needs to be linked here from run_inference.py"
    
    return answer