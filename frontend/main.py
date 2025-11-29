"""
Main Streamlit Application for Vehicle Price and Condition Prediction
Refactored into modular components
"""
import streamlit as st
from config import PAGE_TITLE, PAGE_ICON, LAYOUT
from styles import CUSTOM_CSS, FOOTER_HTML
from api_client import check_api_health, fetch_supported_values
from utils import get_categories
from components import (
    render_sidebar,
    render_price_tab,
    render_condition_tab,
    render_api_docs_tab
)


def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Header
    st.markdown('<p class="main-header">🚗 Vehicle Price & Condition Predictor</p>', unsafe_allow_html=True)
    st.markdown("### Powered by Machine Learning 🤖")
    
    # Check API status
    api_status = check_api_health()
    
    # Render sidebar
    render_sidebar(api_status)
    
    # Fetch supported values
    supported_data = fetch_supported_values()
    categories = get_categories(supported_data)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["💰 Price Prediction", "🔧 Condition Prediction", "📖 API Documentation"])
    
    # Render tabs
    with tab1:
        render_price_tab(api_status, categories)
    
    with tab2:
        render_condition_tab(api_status, categories)
    
    with tab3:
        render_api_docs_tab()
    
    # Footer
    st.divider()
    st.markdown(FOOTER_HTML, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
