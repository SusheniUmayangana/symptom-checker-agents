from crewai import Agent

risk_analyst = Agent(
    role="AI Risk Assessment Analyst",
    goal="Identify and score risks in AI systems using AI Act obligations",
    backstory="Expert in AI safety and risk modeling",
    tools=[retriever_tool],
    verbose=True
)