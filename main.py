from ui.layout import render_header, render_footer
from crew_setup import run_symptom_checker
import streamlit as st
from ui.pdf_export import generate_pdf

render_header()

st.subheader("📝 Describe your symptoms")
user_input = st.text_area("Enter symptoms (e.g., fever, cough, headache):", height=100)

if st.button("🔍 Check Symptoms"):
    with st.spinner("Analyzing symptoms..."):
        report = run_symptom_checker(user_input)

    st.success("✅ Report Generated")
    st.markdown("### 📄 Health Report")
    st.text_area("Report Preview", report, height=300)
    pdf_file = generate_pdf(report_text=report, filename="health_report.pdf")

    with open(pdf_file, "rb") as f:
        st.download_button("⬇️ Download PDF Report", f, file_name="health_report.pdf", mime="application/pdf")

render_footer()