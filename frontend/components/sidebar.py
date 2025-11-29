"""
Sidebar component with API status and settings
"""
import streamlit as st
from config import API_URL


def render_sidebar(api_status):
    """
    Render the sidebar with API status and information
    
    Args:
        api_status (bool): Whether the API is connected
    """
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Health Check
        if api_status:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Offline")
            st.warning("Please start the Flask backend:\n```bash\ncd backend && python app.py\n```")
        
        st.divider()
        
        st.header("📊 About")
        st.info("""
        This application uses machine learning models to:
        - 💰 Predict vehicle prices
        - 🔧 Predict vehicle conditions
        
        Built with:
        - Flask (Backend)
        - Streamlit (Frontend)
        - Scikit-learn (ML Models)
        """)
        
        st.divider()
        
        # API URL Configuration
        st.text_input("API URL", value=API_URL, disabled=True)
