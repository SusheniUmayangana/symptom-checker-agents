import pandas as pd
import streamlit as st
import re
from datetime import datetime

# --- Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Import your utility and agent modules
from utils.firebase_config import initialize_firebase
from utils.auth import sign_up, sign_in
from utils.firestore_utils import (
    save_report_to_history,
    get_user_history,
    delete_history_item,
    get_user_profile,
    update_user_profile,
    analyze_history_trends
)
from agents.symptom_classifier import SymptomClassifierAgent, SymptomAgent
from agents.condition_matcher import ConditionMatcherAgent
from agents.advice_agent import AdviceAgent
from ui.layout import apply_styles, render_header_content, render_footer
from ui.pdf_export import generate_pdf

# Apply the custom CSS styles to the app
apply_styles()

# --- Initialize Firebase and Session State ---
firebase = initialize_firebase()

if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if "report_data" not in st.session_state:
    st.session_state.report_data = {}
if 'selected_report' not in st.session_state:
    st.session_state.selected_report = None

# --- Callback Functions ---
def set_page(page_name):
    st.session_state.page = page_name

def clear_report():
    if 'report_data' in st.session_state:
        del st.session_state.report_data
    st.session_state.selected_report = None

def select_report(report):
    st.session_state.selected_report = report

# --- Page Navigation and Display Logic ---

if not st.session_state.user:
    # --- AUTHENTICATION PAGES ---
    if st.session_state.page == 'login':
        st.title("Welcome Back!")
        st.subheader("Please log in to continue.")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            if submitted and sign_in(email, password):
                set_page('app')
                st.rerun()
        st.markdown("---")
        st.write("Don't have an account?")
        if st.button("Go to Sign Up", use_container_width=True):
            set_page('signup')
            st.rerun()

    elif st.session_state.page == 'signup':
        st.title("Create a New Account")
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            if submitted and sign_up(email, password, name):
                st.success("Account created! Please proceed to login.")
                set_page('login')
                st.rerun()
        st.markdown("---")
        st.write("Already have an account?")
        if st.button("Go to Login", use_container_width=True):
            set_page('login')
            st.rerun()

else:
    # --- LOGGED-IN USER SECTION ---
    user_id = st.session_state.user['uid']
    id_token = st.session_state.user['idToken']
    user_profile = get_user_profile(user_id, id_token)
    is_pro = user_profile.get('plan') == 'pro'

    st.sidebar.title(f"Welcome, {st.session_state.user['name']}")
    st.sidebar.markdown("---")

    # --- PAGE DISPLAY LOGIC (with specific sidebars for each page) ---
    if st.session_state.page == 'upgrade':
        # --- UPGRADE PAGE SIDEBAR ---
        if st.sidebar.button("← Back to App"):
            set_page('app')
            st.rerun()

        # --- Upgrade Page Content ---
        st.title("🚀 Upgrade to Symptom Checker Pro")
        st.markdown("Unlock powerful features and get unlimited access.")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Pro Plan Features:")
            st.markdown("""
            * **Unlimited Scenarios:** Analyze symptoms as often as you need.
            * **Deeper AI Analysis:** Access our most advanced AI model.
            * **Full History Access:** View and manage your complete history.
            * **Trend Analysis:** Get insights on recurring symptoms over time.
            """)
        with col2:
            st.subheader("Simulated Payment")
            st.info("**This is a demo.** Please do **not** enter real credit card information.", icon="⚠️")
            with st.form("payment_form"):
                card_number = st.text_input("Card Number", placeholder="0000 0000 0000 0000")
                exp_date = st.text_input("Expiration Date (MM/YY)", placeholder="MM/YY")
                cvc = st.text_input("CVC", placeholder="123", type="password", max_chars=4)
                name_on_card = st.text_input("Name on Card", placeholder="Your Name")
                submitted = st.form_submit_button("Pay $10 and Upgrade", use_container_width=True)
                if submitted:
                    if not all([card_number, exp_date, cvc, name_on_card]):
                        st.error("Please fill in all payment fields.")
                    elif len(re.sub(r'\s+', '', card_number)) != 16 or not card_number.replace(' ', '').isdigit():
                        st.error("Please enter a valid 16-digit card number.")
                    elif not re.match(r'^(0[1-9]|1[0-2])\/([0-9]{2})$', exp_date):
                        st.error("Please enter the expiration date in MM/YY format.")
                    elif not (len(cvc) in [3, 4] and cvc.isdigit()):
                        st.error("Please enter a valid 3 or 4-digit CVC.")
                    else:
                        if update_user_profile(user_id, id_token, {"plan": "pro"}):
                            st.success("Upgrade Successful! Welcome to Pro!")
                            st.balloons()
                            set_page('app')
                            st.rerun()
                        else:
                            st.error("Upgrade failed. Please try again.")

    # This is the main application page for logged in users
    elif st.session_state.page == 'app':

        # --- MAIN APP SIDEBAR ---
        if is_pro:
            st.sidebar.markdown(
                """<div style="background-color:#FFD700;color:black;padding:2px 8px;border-radius:12px;font-size:12px;font-weight:bold;text-align:center;margin-top:-10px;margin-bottom:10px;">
                PRO
                </div>""", unsafe_allow_html=True
            )

        if not is_pro:
            st.sidebar.subheader("Upgrade to Pro!")
            if st.sidebar.button("🚀 Go Pro"):
                set_page('upgrade')
                st.rerun()

        st.sidebar.markdown("---")
        if st.sidebar.button("Sign Out"):
            st.session_state.user = None
            set_page('login')
            st.rerun()

        # --- MAIN CONTENT ---
        @st.cache_resource
        def load_agents():
            return SymptomClassifierAgent(), ConditionMatcherAgent(), AdviceAgent(), SymptomAgent()
        classifier, matcher, advisor, agent = load_agents()

        
        main_tab, history_tab = st.tabs(["Symptom Checker", "My History"])

        with main_tab:
            render_header_content()

            st.subheader("How are you feeling today?")
            user_input = st.text_input(
                "Describe your symptoms in detail.",
                placeholder="e.g., 'I have a high fever, a sore throat...'"
            )
            if st.button("🔍 Analyze My Symptoms", use_container_width=True) and user_input.strip():
                user_profile = get_user_profile(user_id, id_token)
                scenarios_used = user_profile.get('scenarios_used', 0)
                if not is_pro and scenarios_used >= 10:
                    st.warning("You've reached your free limit. Please upgrade to Pro.")
                    if st.button("Upgrade to Pro Now"):
                        set_page('upgrade')
                        st.rerun()
                else:
                    clear_report()
                    with st.spinner("Our AI agents are analyzing your symptoms..."):
                        symptoms = classifier.execute(user_input)
                        condition_scores = matcher.execute(symptoms)
                        advice = advisor.execute(user_input)
                        gemini_response = agent.analyze(user_input, is_pro=is_pro)
                        st.session_state.report_data = {
                            "Identified Symptoms": ", ".join(symptoms) if symptoms else "No specific symptoms identified.",
                            "Potential Conditions": ", ".join(condition_scores.keys()) if condition_scores else "No matching conditions found.",
                            "Personalized Advice": advice,
                            "Additional Insights": gemini_response
                        }
                        save_report_to_history(user_id, id_token, st.session_state.report_data)
                        if not is_pro:
                            update_user_profile(user_id, id_token, {'scenarios_used': scenarios_used + 1})
            
            if st.session_state.report_data:
                st.success("✅ Your health analysis is complete!")
                report_icons = {
                    "Identified Symptoms": "🩺", "Potential Conditions": "🧬",
                    "Personalized Advice": "💡", "Additional Insights": "🤖"
                }
                for title, body in st.session_state.report_data.items():
                    if body and body.strip():
                        icon = report_icons.get(title, "📄")

                        html_body = body.strip().replace("\n", "<br>")
                        html_body = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_body) # Bold
                        html_body = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_body)       # Italic
                        
                        st.markdown(f"""
                            <div class="report-card">
                                <h4>{icon} {title}</h4>
                                <p>{html_body}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""<div class="report-card"><h4>{icon} {title}</h4><p>{body.strip().replace("\n", "<br>")}</p></div>""", unsafe_allow_html=True)
                st.markdown("---")
                col1, col2 = st.columns([4, 2])
                with col2:
                    st.button("Start New Scenario", on_click=clear_report, use_container_width=True)
                try:
                    pdf_file = generate_pdf(report_data=st.session_state.report_data, filename="health_report.pdf", is_pro=is_pro)
                    with open(pdf_file, "rb") as f:
                        st.download_button(label="⬇️ Download PDF Report", data=f, file_name="health_report.pdf", mime="application/pdf", use_container_width=True)
                except Exception as e:
                    st.error(f"Failed to generate PDF. Error: {e}")

        with history_tab:
            st.title("Your Past Analyses")
            if is_pro:
                st.subheader("📈 Your Symptom Trends")
                with st.container(border=True):
                    full_history = get_user_history(user_id, id_token, is_pro=True)
                    trends, symptom_counts = analyze_history_trends(full_history)
                    if symptom_counts:
                        st.markdown("##### Symptom Frequency")
                        df_symptoms = pd.DataFrame(symptom_counts.items(), columns=['Symptom', 'Count'])
                        st.bar_chart(df_symptoms.set_index('Symptom'))
                        st.markdown("---")
                    st.markdown("##### Key Insights")
                    for trend in trends:
                        st.info(trend)
                st.markdown("---")

            col1, col2 = st.columns([1, 2])
                
            with col1:
                st.subheader("Reports")
                history_list = get_user_history(user_id, id_token, is_pro=is_pro)
                if not history_list:
                    st.info("No past reports.")
                else:
                    for report in history_list:
                        report_id = report.get('timestamp', 'N/A')
                        symptoms = report.get('Identified Symptoms', 'No symptoms')
                        st.button(
                            f"**{report_id.split(' ')[0]}** - {symptoms}", 
                            key=f"btn_{report.get('unique_id')}", 
                            on_click=select_report, args=[report], 
                            use_container_width=True
                            )

            with col2:
                st.subheader("Report Details")
                selected = st.session_state.selected_report
               
                if selected:
                    with st.container(border=True):                            
                        st.markdown(f"**Report from:** {selected.get('timestamp')}")
                        st.markdown("---")
                        st.markdown(f"**🩺 Identified Symptoms:** {selected.get('Identified Symptoms', 'N/A')}")
                        st.markdown(f"**🧬 Potential Conditions:** {selected.get('Potential Conditions', 'N/A')}")
                        st.markdown("---")
                        st.markdown("#### Personalized Advice")
                        st.markdown(selected.get("Personalized Advice", "No advice available."))
                        st.markdown("#### 🤖 Additional Insights")
                        st.markdown(selected.get("Additional Insights", "No additional insights."))
                            
                        st.markdown("---")
                        unique_id = selected.get('unique_id')
                        if st.button("Delete this Report", key=f"del_btn_{unique_id}", type="primary"):
                           if unique_id:
                                delete_history_item(user_id, id_token, unique_id)
                                st.session_state.selected_report = None # Clear selection
                                st.rerun()
                else:
                    st.info("Select a report from the list on the left to view its details.")
        
        # Render Footer
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="footer">Built by Susheni ❤️ • Powered by Streamlit & Gemini</div>', unsafe_allow_html=True)