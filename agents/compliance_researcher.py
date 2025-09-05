from crewai import Agent

compliance_researcher = Agent(
    role="AI Compliance Researcher",
    goal="Research and summarize AI regulations and standards",
    backstory="Experienced in legal research and AI policy",
    tools=[retriever_tool],
    verbose=True
)