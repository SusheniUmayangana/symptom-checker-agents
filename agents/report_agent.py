from crewai import Agent

# Define the Crew AI agent
report_agent = Agent(
    role="Report Compiler",
    goal="Create a final health report",
    backstory="Expert in formatting health advice and matched conditions into a clear, readable summary for users.",
    verbose=True
)

# Define the report generation logic
class ReportAgent:
    def generate_report(self, symptoms: list, conditions: list, advice: str) -> str:
        symptom_str = ", ".join(symptoms) if symptoms else "None specified"
        condition_str = ", ".join(conditions) if conditions else "No conditions matched"

        report = (
            f"🩺 **Health Report**\n\n"
            f"**Identified Symptoms:** {symptom_str}\n"
            f"**Matched Conditions:** {condition_str}\n\n"
            f"**Advice:**\n{advice.strip()}"
        )
        return report