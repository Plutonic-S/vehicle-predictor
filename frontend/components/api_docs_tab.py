"""
API documentation tab component
"""
import streamlit as st


def render_api_docs_tab():
    """Render the API documentation tab"""
    st.header("📖 API Documentation")
    
    st.subheader("🔗 API Endpoints")
    
    st.markdown("#### `GET /`")
    st.code("""
    Response:
    {
        "message": "Vehicle Price and Condition Prediction API",
        "version": "1.0.0",
        "models_loaded": true,
        "endpoints": {...}
    }
    """, language="json")
    
    st.markdown("#### `POST /predict/price`")
    st.markdown("Predict vehicle price based on features")
    st.code("""
    Request Body:
    {
        "year": 2015,
        "odometer": 50000,
        "lat": 33.7490,
        "long": -84.3880,
        "manufacturer": "toyota",
        "fuel": "gas",
        "title_status": "clean",
        "transmission": "automatic",
        "drive": "fwd",
        "size": "mid-size",
        "type": "sedan",
        "paint_color": "white",
        "state": "ca",
        "region": "los angeles",
        "condition": "good"
    }
    
    Response:
    {
        "success": true,
        "prediction": {
            "predicted_price": 15000.50
        }
    }
    """, language="json")
    
    st.markdown("#### `POST /predict/condition`")
    st.markdown("Predict vehicle condition based on features")
    st.code("""
    Request Body:
    {
        "price": 15000,
        "year": 2015,
        "odometer": 50000,
        "lat": 33.7490,
        "long": -84.3880,
        "manufacturer": "toyota",
        "fuel": "gas",
        "title_status": "clean",
        "transmission": "automatic",
        "drive": "fwd",
        "size": "mid-size",
        "type": "sedan",
        "paint_color": "white",
        "state": "ca",
        "region": "los angeles"
    }
    
    Response:
    {
        "success": true,
        "prediction": {
            "predicted_condition": "good"
        }
    }
    """, language="json")
    
    st.markdown("#### `GET /supported-values`")
    st.markdown("Get all supported categorical values")
    st.code("""
    Response:
    {
        "success": true,
        "valid_categories": {
            "manufacturer": ["toyota", "ford", ...],
            "fuel": ["gas", "diesel", ...],
            ...
        }
    }
    """, language="json")
    
    st.divider()
    
    st.subheader("🛠️ Quick Start")
    st.code("""
    # Start Flask Backend (from project root)
    cd backend && python app.py
    
    # Start Streamlit Frontend (in another terminal, from project root)
    streamlit run frontend/app.py
    """, language="bash")
