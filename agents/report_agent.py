from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    verbose=True,
    temperature=0.1
)

class ReportAgent:
    def __init__(self):
        self.agent = Agent(
            role="Report Compiler",
            goal="Create a final health report",
            backstory="Expert in formatting health advice and matched conditions into a clear, readable summary for users.",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    def execute(self, symptoms: list, conditions: list, advice: str) -> str:
        symptom_str = ", ".join(symptoms) if symptoms else "None specified"
        condition_str = ", ".join(conditions) if conditions else "No conditions matched"

        return (
            f"Health Report\n\n"
            f"Identified Symptoms: {symptom_str}\n"
            f"Matched Conditions: {condition_str}\n\n"
            f"Advice:\n{advice.strip()}"
        )