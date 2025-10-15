# ui/layout.py

import streamlit as st

def render_header():
    """
    Renders the header and injects custom CSS for an elegant UI.
    """
    st.set_page_config(page_title="AI Health Assistant", page_icon="🩺", layout="centered")

    # Import Google Fonts and define CSS
    st.markdown("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        
        <style>
            /* --- Global Styles --- */
            html, body, [class*="st-"] {
                font-family: 'Poppins', sans-serif;
                background-color: #F0F2F6; /* Soft gray background */
            }

            /* --- Animations --- */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            /* --- Main App Container --- */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                animation: fadeIn 0.5s ease-out;
            }

            /* --- Header/Hero Section --- */
            .hero {
                padding: 1rem 0 2rem 0;
                text-align: center;
                animation: fadeIn 0.5s ease-out;
            }
            .hero h1 {
                font-size: 2.8em;
                font-weight: 700;
                color: #0D9488; /* Deep Teal */
                margin-bottom: 0.5rem;
            }
            .hero h1 .icon {
                color: #6C63FF; /* Accent color */
            }
            .hero p {
                font-size: 1.1em;
                color: #64748B; /* Softer text color */
                font-weight: 300;
            }
            
            /* --- Input Area --- */
            .stTextArea textarea {
                border-radius: 10px;
                border: 1px solid #D0D0D0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.02);
                font-size: 1em;
            }

            /* --- Button --- */
            .stButton>button {
                border: 2px solid #2563EB; /* Border color matches the theme blue */
                border-radius: 9999px;
                padding: 0.75rem 1.5rem;
                font-weight: 600;
                color: #2563EB; /* Text color is blue */
                background-color: transparent; /* Transparent background */
                transition: all 0.2s ease-in-out;
            }
            .stButton>button:hover {
                background-color: #2563EB; /* Fills with blue on hover */
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }

            /* --- Custom Report Card Styling --- */
            .report-card {
                background-color: #FFFFFF;
                border-radius: 12px;
                padding: 25px;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 20px rgba(0,0,0,0.06);
                border-left: 5px solid #6C63FF; /* Accent border */
                animation: fadeIn 0.7s ease-out;
            }
            .report-card h4 {
                font-size: 1.4em;
                font-weight: 600;
                color: #262730;
                margin-bottom: 0.8rem;
                display: flex;
                align-items: center;
            }
            .report-card p {
                font-size: 1.05em;
                color: #4A4A4A;
                line-height: 1.6;
            }

            /* --- Footer --- */
            .footer {
                text-align: center;
                padding: 2rem 0;
                color: #888;
                font-size: 0.9em;
                font-weight: 300;
            }
            .footer strong {
                font-weight: 600;
            }
        </style>
    """, unsafe_allow_html=True)

    # Render the styled header
    st.markdown("""
        <div class="hero">
            <h1>Symptom Checker<span class="icon">✨</span></h1>
            <p>Your intelligent partner for preliminary symptom analysis.</p>
        </div>
    """, unsafe_allow_html=True)

    # Add a modern header image
    st.image(
        "https://images.pexels.com/photos/4021775/pexels-photo-4021775.jpeg",
        use_container_width=True
    )


def render_footer():
    """ Renders a styled footer """
    st.markdown("<hr style='border:1px solid #E0E0E0;'>", unsafe_allow_html=True)
    st.markdown("""
        <div class="footer">
            Built with Solo IRWA adaptation by <strong>Susheni ❤️</strong> • Powered by Streamlit & CrewAI
        </div>
    """, unsafe_allow_html=True)