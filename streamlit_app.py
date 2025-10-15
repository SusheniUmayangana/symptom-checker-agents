# streamlit_app.py

import streamlit as st
from agents.symptom_classifier import SymptomClassifierAgent, SymptomAgent
from agents.condition_matcher import ConditionMatcherAgent
from agents.advice_agent import AdviceAgent
from agents.report_agent import ReportAgent
from ui.layout import render_header, render_footer # We remove render_section
from ui.pdf_export import generate_pdf
from datetime import datetime
import re

# --- Agent Initialization ---
# It's good practice to cache heavy objects to improve performance
@st.cache_resource
def load_agents():
    classifier = SymptomClassifierAgent()
    matcher = ConditionMatcherAgent()
    advisor = AdviceAgent()
    reporter = ReportAgent()
    agent = SymptomAgent()
    return classifier, matcher, advisor, reporter, agent

classifier, matcher, advisor, reporter, agent = load_agents()

# --- Page Rendering ---
render_header()

# --- Main Input Section ---
st.subheader("How are you feeling today?")
user_input = st.text_area(
    "Describe your symptoms in detail. For example: 'I have a high fever, a sore throat, and a persistent headache.'",
    height=120,
    placeholder="Enter your symptoms here..."
)

# --- Session State Management ---
if "report_data" not in st.session_state:
    st.session_state.report_data = {}

# --- Logic on Button Click ---
if st.button("🔍 Analyze My Symptoms") and user_input.strip():
    with st.spinner("Our AI agents are analyzing your symptoms... Please wait."):
        # Run agents to get data
        symptoms = classifier.execute(user_input)
        condition_scores = matcher.execute(symptoms)
        advice = advisor.execute(user_input)
        gemini_response = agent.analyze(user_input) # Assuming this gives additional advice

        # Store structured data in session state instead of a single string
        st.session_state.report_data = {
            "Identified Symptoms": ", ".join(symptoms) if symptoms else "No specific symptoms identified.",
            "Potential Conditions": ", ".join(condition_scores.keys()) if condition_scores else "No matching conditions found based on input.",
            "Personalized Advice": advice,
            "Additional Insights": gemini_response
        }
        
# --- Report Display ---
if st.session_state.report_data:
    st.success("✅ Your health analysis is complete!")
    
    # Define icons for each section
    icons = {
        "Identified Symptoms": "🩺",
        "Potential Conditions": "🧬",
        "Personalized Advice": "💡",
        "Additional Insights": "🤖"
    }

    # Generate the text for the PDF report
    report_text_for_pdf = ""

    for title, body in st.session_state.report_data.items():
        if body.strip():
            # Format for display
            icon = icons.get(title, "📄")

            # Convert basic markdown to HTML for consistent rendering in the card
            html_body = body.strip().replace("\n", "<br>")
            html_body = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_body) # Bold
            html_body = html_body.replace("•", "•&nbsp;") # Ensure space after bullet

            st.markdown(f"""
                <div class="report-card">
                    <h4>{icon} {title}</h4>
                    <p>{body.strip()}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Format for PDF
            report_text_for_pdf += f"{title}:\n{body.strip()}\n\n"
    
    # --- PDF Export Section (Your new, improved code) ---
    st.markdown("---")
    col1, col2, col3 = st.columns([1.5, 2, 1]) # Create columns for centering
    with col2:
        filename = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        try:
            pdf_file = generate_pdf(report_data=st.session_state.report_data, filename=filename)

            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=f,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Failed to generate PDF. Error: {e}")

# --- Footer ---
render_footer()