import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from crewai import Agent
import streamlit as st

# 🔐 Load environment variables from .env file for local development
load_dotenv()

# Smartly configure the Gemini API key to work locally and on Streamlit Cloud
try:
    # First, try to get the key from Streamlit secrets (for deployment)
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    # If that fails, fall back to the .env file (for local development)
    print("Streamlit secrets not found, falling back to .env file for Gemini key.")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the API if the key was found, otherwise raise an error
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file or Streamlit secrets.")

# 🧠 Agent 1: Gemini-powered health responder
class SymptomAgent:
    def __init__(self):
        # Initialize both the free and pro models
        self.free_model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
        self.pro_model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
        
    def analyze(self, user_input: str, is_pro: bool = False) -> str:
        model_to_use = self.pro_model if is_pro else self.free_model
        model_name = "PRO" if is_pro else "FREE"

        retries = 3
        wait_time = 1

        for i in range(retries):
            try:
                print(f"[SymptomAgent] Querying Gemini ({model_name} model, Attempt {i+1}/{retries})...")
                response = model_to_use.generate_content(user_input)
                return response.text
            except Exception as e:
                print(f"[Gemini Error] Attempt {i+1} failed: {e}")
                if i < retries - 1:
                    print(f"Waiting for {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
                    wait_time *= 2
                else:
                    print("All Gemini API retries failed.")
                    return f"Gemini failed: {e}"
        
        return "Gemini failed after all retries."

# 🩺 Agent 2: Rule-based symptom classifier
class SymptomClassifierAgent:
    def __init__(self):
        self.agent = Agent(
            role="Symptom Classifier",
            goal="Identify symptoms from user input",
            backstory="Expert in parsing health-related text and extracting relevant symptoms.",
            verbose=True
        )

    def execute(self, user_input: str) -> list:
        known_symptoms = [
            "fever", "cough", "headache", "nausea", "vomiting", "rash",
            "joint pain", "sore throat", "fatigue", "bleeding", "itching",
            "dizziness", "shortness of breath"
        ]
        detected = [symptom for symptom in known_symptoms if symptom in user_input.lower()]
        print(f"[SymptomClassifierAgent] Detected: {detected}")
        return detected if detected else ["unspecified symptom"]

# 🔗 Execution flow for local testing
if __name__ == "__main__":
    classifier = SymptomClassifierAgent()
    generator = SymptomAgent()

    user_input = input("Describe your symptoms: ")
    symptoms = classifier.execute(user_input)
    query = f"The user reports the following symptoms: {', '.join(symptoms)}. Based on these, what are some general possibilities? Provide general health information, not personal medical advice."

    # The analyze function will use its default (is_pro=False) for local testing
    result = generator.analyze(query)
    print("\n🩺 Gemini Response:")
    print(result)