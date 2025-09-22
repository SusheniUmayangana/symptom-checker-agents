import streamlit as st
from ui.layout import render_header, render_footer
from ui.pdf_export import generate_pdf
from agents.symptom_classifier import SymptomClassifierAgent
from agents.condition_matcher import ConditionMatcherAgent
from agents.advice_agent import AdviceAgent
from agents.report_agent import ReportAgent

# Initialize agents
classifier = SymptomClassifierAgent()
matcher = ConditionMatcherAgent()
advisor = AdviceAgent()
reporter = ReportAgent()

# 🧠 UI Header
render_header()

# 📝 User Input
st.subheader("📝 Describe your symptoms")
user_input = st.text_area("Enter symptoms (e.g., fever, cough, headache):", height=100)

# 🔍 Run Crew AI
if st.button("🔍 Check Symptoms") and user_input.strip():
    with st.spinner("Getting advice from AI agents..."):
        symptoms = classifier.execute(user_input)
        condition_scores = matcher.execute(symptoms)
        advice = advisor.execute(user_input)
        report = reporter.execute(symptoms, list(condition_scores.keys()), advice)

    # ✅ Show Results
    st.success("✅ Report Generated")
    st.text_area("📄 Health Report", report, height=300)

    # 📄 PDF Export
    pdf_file = generate_pdf(report_text=report, filename="health_report.pdf")
    with open(pdf_file, "rb") as f:
        st.download_button("⬇️ Download PDF Report", f, file_name="health_report.pdf", mime="application/pdf")

# 🧠 UI Footer
render_footer()