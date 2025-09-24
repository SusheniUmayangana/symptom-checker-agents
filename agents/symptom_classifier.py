import os
from dotenv import load_dotenv
import google.generativeai as genai
from crewai import Agent

# 🔐 Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 🧠 Agent 1: Gemini-powered health responder
class SymptomAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(model_name="models/gemini-2.0-flash-001")

    def analyze(self, user_input: str) -> str:
        try:
            print(f"[SymptomAgent] Query: {user_input}")
            response = self.model.generate_content(user_input)
            print(f"[Gemini Raw Response] {response}")
            return response.text
        except Exception as e:
            print(f"[Gemini Error] {e}")
            return f"Gemini failed: {e}"
        
# 🩺 Agent 2: Rule-based symptom classifier
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
        print(f"[SymptomClassifierAgent] Detected: {detected}")
        return detected if detected else ["unspecified symptom"]

# 🔗 Execution flow
if __name__ == "__main__":
    classifier = SymptomClassifierAgent()
    generator = SymptomAgent()

    user_input = input("Describe your symptoms: ")
    symptoms = classifier.execute(user_input)
    query = f"The user reports: {', '.join(symptoms)}. What could this indicate?"

    result = generator.analyze(query)
    print("\n🩺 Gemini Response:")
    print(result)