import streamlit as st

def render_header():
    st.set_page_config(page_title="Symptom Checker", page_icon="🩺", layout="centered")
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🩺 Symptom Checker</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>An agent-based health assistant powered by Crew AI</p>", unsafe_allow_html=True)
    st.markdown("---")

def render_footer():
    st.markdown("---")
    st.markdown("<p style='text-align: center; font-size: 12px;'>Solo IRWA adaptation by Susheni • Powered by Python & Crew AI</p>", unsafe_allow_html=True)