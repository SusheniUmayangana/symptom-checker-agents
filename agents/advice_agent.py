from crewai import Agent
from rag.loader import load_text
from rag.chunker import chunk_by_heading
from rag.retriever import retrieve_chunks
from rag.generator import generate_advice

class AdviceAgent:
    def __init__(self, guideline_path="docs/health_guidelines.txt"):
        self.agent = Agent(
            role="Advice Generator",
            goal="Provide health advice based on guidelines",
            backstory="Uses a RAG pipeline to retrieve relevant health guideline chunks and generate personalized advice.",
            verbose=True
        )
        self.guideline_path = guideline_path

    def execute(self, query: str) -> str:
        try:
            text = load_text(self.guideline_path)
            chunks = chunk_by_heading(text)
            relevant_chunks = retrieve_chunks(chunks, query)
            advice = generate_advice(relevant_chunks, query)
            return advice.strip()
        except Exception as e:
            return f"⚠️ Error generating advice: {str(e)}"