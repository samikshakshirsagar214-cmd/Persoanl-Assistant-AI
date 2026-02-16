import os
from langchain_ollama import ChatOllama

def get_llm():
    # Switches between Docker (ollama:11434) and Local (localhost:11434)
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    return ChatOllama(
        model="gemma:2b",
        base_url=base_url,
        temperature=0.1
    )
