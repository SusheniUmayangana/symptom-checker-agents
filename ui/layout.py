import streamlit as st

def apply_styles():
    """Injects all custom CSS for the application."""
    st.markdown("""
        <style>
            /* Base container with full width */
            div[data-testid="stAppViewContainer"] {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: #1A202C;
                background-color: #F7FAFC;
                width: 100%; /* Full page width */
                max-width: 1800px; /* Cap for ultra-wide screens */
                margin: 0 auto;
                padding: 1rem;
                box-sizing: border-box;
            }
            /* Hero section with healthcare theme */
            div.hero {
                padding: 2.5rem 2rem;
                text-align: center;
                background: linear-gradient(135deg, #14B8A6 0%, #3B82F6 100%); /* Teal to blue gradient */
                border-radius: 12px;
                margin-bottom: 2rem;
                border: 1px solid #E5E7EB;
                animation: fadeIn 0.5s ease-in;
                width: 100%;
            }
            div.hero h1 {
                font-size: 3.2rem;
                font-weight: 800;
                color: #FFFFFF;
                margin-bottom: 0.75rem;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
            }
            div.hero p {
                font-size: 1.3rem;
                color: #F7FAFC;
                font-weight: 500;
            }
            /* Report card styling with animation */
            div.report-card {
                background-color: #FFFFFF;
                border-radius: 12px;
                padding: 2rem;
                margin-bottom: 2rem;
                border-left: 6px solid #14B8A6; /* Teal accent */
                box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                animation: fadeIn 0.5s ease-in;
                width: 100%;
            }
            div.report-card h4 {
                font-size: 1.6rem;
                font-weight: 700;
                color: #1A202C;
                margin-bottom: 1rem;
            }
            div.report-card p {
                font-size: 1.2rem;
                color: #4A5568;
                line-height: 1.7;
            }
            /* Button styling with teal theme */
            button[data-testid="stButton"] {
                background-color: #14B8A6 !important;
                color: #FFFFFF !important;
                border-radius: 8px !important;
                padding: 0.85rem 1.5rem !important;
                font-weight: 600 !important;
                width: 100% !important;
                font-size: 1.1rem !important;
                box-shadow: 0 4px 6px rgba(20, 184, 166, 0.2) !important;
                transition: all 0.3s ease !important;
            }
            button[data-testid="stButton"]:hover {
                background-color: #0F766E !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 12px rgba(20, 184, 166, 0.3) !important;
            }
            /* Input styling */
            div[data-testid="stTextInput"] input {
                border: 2px solid #CBD5E0 !important;
                border-radius: 8px !important;
                padding: 0.85rem !important;
                font-size: 1.1rem !important;
                width: 100% !important;
                transition: border-color 0.3s ease !important;
            }
            div[data-testid="stTextInput"] input:focus {
                border-color: #14B8A6 !important;
                box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.2) !important;
            }
            /* Footer styling */
            div.footer {
                text-align: center;
                padding: 2rem 2rem;
                color: #718096;
                font-size: 1rem;
                background-color: #FFFFFF;
                border-top: 2px solid #E2E8F0;
                margin-top: 2.5rem;
                width: 100%;
            }
            div.footer strong {
                font-weight: 700;
                color: #14B8A6;
            }
            /* Debug element to confirm CSS loading */
            .css-debug {
                background-color: #10B981;
                color: #FFFFFF;
                padding: 0.5rem;
                font-size: 0.9rem;
                text-align: center;
                margin-bottom: 1rem;
                animation: fadeIn 0.5s ease-in;
            }
            /* Animations */
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            /* Responsive adjustments */
            @media (max-width: 768px) {
                div[data-testid="stAppViewContainer"] {
                    padding: 0.5rem;
                }
                div.hero {
                    padding: 1.5rem 1rem;
                }
                div.hero h1 {
                    font-size: 2.2rem;
                }
                div.hero p {
                    font-size: 1rem;
                }
                div.report-card {
                    padding: 1.5rem 1rem;
                }
                div.report-card h4 {
                    font-size: 1.4rem;
                }
                div.report-card p {
                    font-size: 1.1rem;
                }
                button[data-testid="stButton"] {
                    font-size: 1rem !important;
                }
            }
            @media (max-width: 480px) {
                div.hero h1 {
                    font-size: 1.8rem;
                }
                div.hero p {
                    font-size: 0.9rem;
                }
                div.report-card {
                    padding: 1rem 0.5rem;
                }
                div.report-card h4 {
                    font-size: 1.2rem;
                }
                div.report-card p {
                    font-size: 1rem;
                }
            }
        </style>
    """, unsafe_allow_html=True)

def render_header_content():
    """Renders the HTML and image for the header."""
    st.markdown("""
        <div class="hero">
            <h1>Symptom Checker ✨</h1>
            <p>Your intelligent partner for preliminary symptom analysis.</p>
        </div>
    """, unsafe_allow_html=True)
    st.image("https://images.pexels.com/photos/4021775/pexels-photo-4021775.jpeg", use_container_width=True)

def render_footer():
    """Renders the HTML for the footer."""
    st.markdown("<hr style='border:1px solid #E2E8F0;'>", unsafe_allow_html=True)
    st.markdown("""
        <div class="footer">
            Built by <strong>Susheni ❤️</strong> • Powered by Streamlit & Gemini
        </div>
    """, unsafe_allow_html=True)