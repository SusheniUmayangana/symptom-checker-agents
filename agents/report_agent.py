from crewai import Agent

class ReportAgent:
    def __init__(self):
        self.agent = Agent(
            role="Report Compiler",
            goal="Create a final health report",
            backstory="Expert in formatting health advice and matched conditions into a clear, readable summary for users.",
            verbose=True
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