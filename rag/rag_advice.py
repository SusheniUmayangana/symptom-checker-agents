from transformers import pipeline

generator = pipeline("text-generation", model="mistralai/Mixtral-8x7B-Instruct-v0.1")

def load_guidelines(path="docs/health_guidelines.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_by_heading(text, delimiter="###"):
    chunks = text.split(delimiter)
    return [f"{delimiter}{chunk.strip()}" for chunk in chunks if chunk.strip()]

def retrieve_chunks(chunks, query):
    return [chunk for chunk in chunks if any(word in chunk.lower() for word in query.lower().split())]

def generate_advice(chunks, query):
    context = "\n".join(chunks)
    prompt = f"Based on the following health guidelines:\n{context}\n\nWhat advice would you give for: {query}"
    response = generator(prompt, max_new_tokens=300, do_sample=True)
    return response[0]["generated_text"]

def get_health_advice(query):
    text = load_guidelines()
    chunks = chunk_by_heading(text)
    relevant = retrieve_chunks(chunks, query)
    return generate_advice(relevant, query)