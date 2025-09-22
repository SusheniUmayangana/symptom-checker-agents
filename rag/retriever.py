from difflib import get_close_matches

def retrieve_chunks(chunks, query):
    return [chunk for chunk in chunks if any(symptom in chunk.lower() for symptom in query.lower().split())]