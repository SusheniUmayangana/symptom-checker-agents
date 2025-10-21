import streamlit as st

def apply_styles():
    """Injects all custom CSS for the application."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
            html, body, [class*="st-"] { font-family: 'Poppins', sans-serif; }
            .stApp { background-color: #F0F2F6; }
            .hero { padding: 1rem 0 2rem 0; text-align: center; }
            .hero h1 { font-size: 2.8em; font-weight: 700; color: #0D9488; }
            .hero p { font-size: 1.1em; color: #64748B; }
            .report-card { background-color: #FFFFFF; border-radius: 12px; padding: 25px; margin-bottom: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border-left: 5px solid #6C63FF; }
            .report-card h4 { font-size: 1.4em; font-weight: 600; color: #262730; margin-bottom: 0.8rem; }
            .report-card p { font-size: 1.05em; color: #4A4A4A; line-height: 1.6; }
            .footer { text-align: center; padding: 2rem 0; color: #888; font-size: 0.9em; }
            .footer strong { font-weight: 600; }
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
    st.markdown("<hr style='border:1px solid #E0E0E0;'>", unsafe_allow_html=True)
    st.markdown("""
        <div class="footer">
            Built by <strong>Susheni ❤️</strong> • Powered by Streamlit & Gemini
        </div>
    """, unsafe_allow_html=True)