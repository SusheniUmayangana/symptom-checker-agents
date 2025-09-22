from openai import OpenAI

def generate_advice(chunks, query):
    context = "\n".join(chunks)
    prompt = f"Based on the following health guidelines:\n{context}\n\nWhat advice would you give for: {query}"
    
    # Replace with your OpenAI or LLM call
    return "AI-generated advice based on retrieved context"