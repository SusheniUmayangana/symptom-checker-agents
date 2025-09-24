import streamlit as st
from agents.symptom_classifier import SymptomClassifierAgent, SymptomAgent
from agents.condition_matcher import ConditionMatcherAgent
from agents.advice_agent import AdviceAgent
from agents.report_agent import ReportAgent
from ui.layout import render_header, render_footer
from ui.pdf_export import generate_pdf
from datetime import datetime

# Initialize agents
classifier = SymptomClassifierAgent()
matcher = ConditionMatcherAgent()
advisor = AdviceAgent()
reporter = ReportAgent()
agent = SymptomAgent()

# Render header
render_header()

# Main input section
st.subheader("Describe your symptoms:")
user_input = st.text_area("Enter your symptoms below", height=100)

# Session state setup
if "report" not in st.session_state:
    st.session_state.report = ""
if "gemini_response" not in st.session_state:
    st.session_state.gemini_response = ""

# Run agents on button click
if st.button("🔍 Check Symptoms") and user_input.strip():
    with st.spinner("Getting advice from AI agents..."):
        gemini_response = agent.analyze(user_input)
        symptoms = classifier.execute(user_input)
        condition_scores = matcher.execute(symptoms)
        advice = advisor.execute(user_input)

        combined_advice = f"{advice}\n\nGemini says:\n{gemini_response}"
        report = (
            "Identified Symptoms:\n"
            + ", ".join(symptoms)
            + "\n\nMatched Conditions:\n"
            + ", ".join(condition_scores.keys())
            + "\n\nAdvice:\n"
            + combined_advice
        )

        st.session_state.report = report
        st.session_state.gemini_response = gemini_response

# ✅ Show Report if Available
if st.session_state.report:
    st.success("✅ Health Report Generated")

    # Split report into sections
    sections = {
        "Identified Symptoms": "",
        "Matched Conditions": "",
        "Advice": ""
    }

    current_section = None
    for line in st.session_state.report.split("\n"):
        line = line.strip().rstrip(":")
        if line in sections:
            current_section = line
        elif current_section:
            sections[current_section] += line + "\n"

    # Render each section with Markdown
    st.markdown("### 🩺 Your Health Summary")
    for title, body in sections.items():
        if body.strip():
            st.markdown(f"#### {title}")
            st.markdown(
                f"<div style='background-color:#f9f9f9; padding:10px; border-radius:6px; font-size:15px;'>{body.strip()}</div>",
                unsafe_allow_html=True
            )

    # 📄 PDF Export
    filename = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_file = generate_pdf(report_text=st.session_state.report, filename=filename)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="⬇️ Download PDF Report",
            data=f,
            file_name=filename,
            mime="application/pdf"
        )

# Render footer
render_footer()