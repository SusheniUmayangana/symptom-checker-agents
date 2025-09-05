from crewai import Agent

report_generator = Agent(
    role="AI Report Generator",
    goal="Generate comprehensive reports on AI systems",
    backstory="Skilled in technical writing and data analysis",
    tools=[retriever_tool],
    verbose=True
)