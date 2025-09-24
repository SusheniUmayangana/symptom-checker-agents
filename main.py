# main.py
import os
from agents.symptom_classifier import SymptomClassifierAgent, SymptomAgent
from agents.condition_matcher import ConditionMatcherAgent
from agents.advice_agent import AdviceAgent
from agents.report_agent import ReportAgent  

def run_basic_pipeline(user_input: str) -> str:
    agent = SymptomAgent()
    return agent.analyze(user_input)

def run_full_pipeline(user_input: str) -> str:
    classifier = SymptomClassifierAgent()
    matcher = ConditionMatcherAgent()
    advisor = AdviceAgent()
    reporter = ReportAgent()

    symptoms = classifier.execute(user_input)
    condition_scores = matcher.execute(symptoms)
    advice = advisor.execute(user_input)
    report = reporter.execute(symptoms, list(condition_scores.keys()), advice)
    return report

if __name__ == "__main__":
    user_input = input("Describe your symptoms: ")
    print("\n🩺 Gemini Response:")
    print(run_basic_pipeline(user_input))

    print("\n📄 Full CrewAI Report:")
    print(run_full_pipeline(user_input))
    
