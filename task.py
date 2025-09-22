from crewai import Task

from agents import advice_agent, condition_matcher, report_agent, symptom_classifier

task1 = Task(
    description="Classify symptoms from user input",
    agent=symptom_classifier,
    expected_output="List of symptoms"
)

task2 = Task(
    description="Match symptoms to conditions",
    agent=condition_matcher,
    expected_output="Likely conditions"
)

task3 = Task(
    description="Generate advice based on symptoms and conditions",
    agent=advice_agent,
    expected_output="Health advice"
)

task4 = Task(
    description="Compile a health report",
    agent=report_agent,
    expected_output="Final report with advice and matched conditions"
)