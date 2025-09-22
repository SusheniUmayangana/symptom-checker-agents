from crewai import Agent

# Define the Crew AI agent
symptom_classifier = Agent(
    role="Symptom Classifier",
    goal="Identify symptoms from user input",
    backstory="Expert in parsing health-related text and extracting relevant symptoms for downstream agents.",
    verbose=True
)

# Define the callable logic for classification
class SymptomClassifierAgent:
    def classify(self, user_input: str) -> list:
        # Basic keyword-based classification (can be replaced with NLP later)
        known_symptoms = [
            "fever", "cough", "headache", "nausea", "vomiting", "rash",
            "joint pain", "sore throat", "fatigue", "bleeding", "itching"
        ]
        detected = [symptom for symptom in known_symptoms if symptom in user_input.lower()]
        return detected if detected else ["unspecified symptom"]