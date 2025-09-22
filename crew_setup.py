from agents.symptom_classifier import SymptomClassifierAgent
from agents.condition_matcher import ConditionMatcherAgent
from agents.advice_agent import AdviceAgent
from agents.report_agent import ReportAgent

def run_symptom_checker(user_input):
    classifier = SymptomClassifierAgent()
    matcher = ConditionMatcherAgent()
    advisor = AdviceAgent()
    reporter = ReportAgent()

    symptoms = classifier.classify(user_input)
    conditions = matcher.match(symptoms)
    advice = advisor.advise(conditions)
    report = reporter.generate_report(symptoms, conditions, advice)

    return report