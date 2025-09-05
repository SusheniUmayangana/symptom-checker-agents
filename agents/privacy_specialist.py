from crewai import Agent

privacy_specialist = Agent(
    role="AI Privacy Specialist",
    goal="Ensure AI systems comply with data privacy regulations",
    backstory="Expert in data privacy laws and ethical AI practices",
    tools=[retriever_tool],
    verbose=True
)