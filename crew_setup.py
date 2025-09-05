from crewai import Crew, Task
from agents.risk_analyst import risk_analyst
from agents.compliance_researcher import compliance_researcher
from agents.report_generator import report_generator
from agents.privacy_specialist import privacy_specialist


task1 = Task(agent=risk_analyst, description="Analyze model risks")
task2 = Task(agent=compliance_researcher, description="Extract AI Act obligations")
task3 = Task(agent=report_generator, description="Generate risk assessment report")
task4 = Task(agent=privacy_specialist, description="Review data privacy compliance")

crew = Crew(tasks=[task1, task2, task3, task4])