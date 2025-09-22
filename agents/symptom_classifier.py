from crewai import Agent

class SymptomClassifierAgent:
    def __init__(self):
        self.agent = Agent(
            role="Symptom Classifier",
            goal="Identify symptoms from user input",
            backstory="Expert in parsing health-related text and extracting relevant symptoms for downstream agents.",
            verbose=True
        )

    def execute(self, user_input: str) -> list:
        known_symptoms = [
            "fever", "cough", "headache", "nausea", "vomiting", "rash",
            "joint pain", "sore throat", "fatigue", "bleeding", "itching"
        ]
        detected = [symptom for symptom in known_symptoms if symptom in user_input.lower()]
        return detected if detected else ["unspecified symptom"]