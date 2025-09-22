from rag.loader import load_text
from rag.chunker import chunk_by_heading
from rag.retriever import retrieve_chunks
from rag.generator import generate_advice
from crewai import Agent

# Define the Crew AI agent
advice_agent = Agent(
    role="Advice Generator",
    goal="Provide health advice based on guidelines",
    backstory="Uses a RAG pipeline to retrieve relevant health guideline chunks and generate personalized advice using a language model.",
    verbose=True
)

# Define the advice generation logic
class AdviceAgent:
    def __init__(self, guideline_path="health_guidelines.txt"):
        self.guideline_path = guideline_path

    def advise(self, query: str) -> str:
        try:
            text = load_text(self.guideline_path)
            chunks = chunk_by_heading(text)
            relevant_chunks = retrieve_chunks(chunks, query)
            advice = generate_advice(relevant_chunks, query)
            return advice.strip()
        except Exception as e:
            return f"⚠️ Error generating advice: {str(e)}"