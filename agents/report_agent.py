# agents/report_agent.py

class ReportAgent:
    def __init__(self):
        # The unused crewai.Agent has been removed to fix the error.
        print("Initialized ReportAgent.")

    def execute(self, symptoms: list, conditions: dict, advice: str) -> str:
        """
        This function is not strictly necessary as formatting is handled in the main app,
        but it's here for logical separation.
        """
        symptom_str = ", ".join(symptoms) if symptoms else "None specified"
        condition_str = ", ".join(conditions.keys()) if conditions else "No conditions matched"

        return (
            f"Health Report\n\n"
            f"Identified Symptoms: {symptom_str}\n"
            f"Matched Conditions: {condition_str}\n\n"
            f"Advice:\n{advice.strip()}"
        )