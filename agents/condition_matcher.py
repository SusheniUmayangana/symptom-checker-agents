from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    verbose=True,
    temperature=0.1
)

class ConditionMatcherAgent:
    def __init__(self):
        self.agent = Agent(
            role="Condition Matcher",
            goal="Match symptoms to known conditions",
            backstory="Uses structured rules and JSON mappings to identify likely health conditions based on user symptoms.",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    def execute(self, symptoms: list) -> dict:
        symptom_map = {
            "fever": ["flu", "dengue"],
            "cough": ["cold", "flu"],
            "headache": ["migraine", "flu"],
            "rash": ["allergy", "dengue"],
            "joint pain": ["dengue", "arthritis"],
            "sore throat": ["cold", "flu"],
            "nausea": ["food poisoning", "dengue"],
            "vomiting": ["food poisoning", "dengue"],
            "bleeding": ["dengue"],
            "itching": ["allergy"]
        }

        condition_scores = {}
        for symptom in symptoms:
            matches = symptom_map.get(symptom.lower(), [])
            for condition in matches:
                condition_scores[condition] = condition_scores.get(condition, 0) + 1

        total = sum(condition_scores.values())
        if total == 0:
            return {"unknown": 1.0}

        return {cond: round(score / total, 2) for cond, score in condition_scores.items()}