import streamlit as st
from ui.layout import render_header, render_footer
from ui.pdf_export import generate_pdf
from agents.symptom_classifier import symptom_classifier
from agents.condition_matcher import condition_matcher
from agents.advice_agent import advice_agent
from agents.report_agent import report_agent
from crewai import Crew, Task

# 🧠 UI Header
render_header()

# 📝 User Input
st.subheader("📝 Describe your symptoms")
user_input = st.text_area("Enter symptoms (e.g., fever, cough, headache):", height=100)

# 🔍 Run Crew AI
if st.button("🔍 Check Symptoms") and user_input.strip():
    with st.spinner("Getting advice from AI agents..."):

        # 🧩 Define tasks dynamically with user input
        task1 = Task(
            description=f"Classify symptoms from user input: '{user_input}'",
            agent=symptom_classifier,
            expected_output="List of symptoms"
        )

        task2 = Task(
            description="Match the classified symptoms to known conditions",
            agent=condition_matcher,
            expected_output="Likely conditions"
        )

        task3 = Task(
            description="Generate health advice based on the matched conditions and symptoms",
            agent=advice_agent,
            expected_output="Health advice"
        )

        task4 = Task(
            description="Compile a health report using the symptoms, conditions, and advice",
            agent=report_agent,
            expected_output="Final report with advice and matched conditions"
        )

        # 🧠 Assemble and run the Crew
        crew = Crew(
            agents=[symptom_classifier, condition_matcher, advice_agent, report_agent],
            tasks=[task1, task2, task3, task4]
        )

        report = crew.kickoff()

    # ✅ Show Results
    st.success("✅ Report Generated")
    st.text_area("📄 Health Report", report, height=300)

    # 📄 PDF Export
    pdf_file = generate_pdf(report_text=report, filename="health_report.pdf")
    with open(pdf_file, "rb") as f:
        st.download_button("⬇️ Download PDF Report", f, file_name="health_report.pdf", mime="application/pdf")

# 🧠 UI Footer
render_footer()