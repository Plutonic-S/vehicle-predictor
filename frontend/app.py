"""
Streamlit Frontend for Vehicle Price and Condition Prediction
Interactive UI for ML model predictions
"""
import streamlit as st
import requests
import json

# ==================== CONFIGURATION ====================

st.set_page_config(
    page_title="Vehicle Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration - use environment variable for production
import os
API_URL = os.getenv("BACKEND_URL") or st.secrets.get("BACKEND_URL", "http://localhost:5000")

# ==================== HELPER FUNCTIONS ====================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_supported_values():
    """Fetch supported categorical values from API"""
    try:
        response = requests.get(f"{API_URL}/supported-values", timeout=60)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Could not fetch supported values: {e}")
        return None

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

# ==================== CUSTOM CSS ====================

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ==================== MAIN APP ====================

# Header
st.markdown('<p class="main-header">🚗 Vehicle Price & Condition Predictor</p>', unsafe_allow_html=True)
st.markdown("### Powered by Machine Learning 🤖")

# Sidebar - API Status
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Health Check
    api_status = check_api_health()
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
    custom_api = st.text_input("API URL", value=API_URL)
    if custom_api != API_URL:
        API_URL = custom_api

# Fetch supported values
supported_data = fetch_supported_values()

# Default values if API is not available
default_manufacturers = ["toyota", "ford", "honda", "chevrolet", "nissan", "bmw", "mercedes-benz", "volkswagen"]
default_fuels = ["gas", "diesel", "electric", "hybrid", "other"]
default_transmissions = ["automatic", "manual", "other"]
default_drives = ["fwd", "rwd", "4wd", "awd"]
default_title_status = ["clean", "rebuilt", "salvage", "lien", "missing"]
default_sizes = ["compact", "mid-size", "full-size", "sub-compact"]
default_types = ["sedan", "suv", "truck", "coupe", "wagon", "convertible", "hatchback", "van", "pickup"]
default_colors = ["white", "black", "silver", "gray", "blue", "red", "brown", "green", "orange", "yellow"]
default_conditions = ["excellent", "good", "fair", "like new", "new", "salvage"]
default_states = ["ca", "ny", "tx", "fl", "pa", "il", "oh", "ga", "nc", "mi"]

# Extract supported values from API response
if supported_data and supported_data.get('success'):
    valid_cats = supported_data.get('valid_categories', {})
    manufacturers = valid_cats.get('manufacturer', default_manufacturers)
    fuels = valid_cats.get('fuel', default_fuels)
    transmissions = valid_cats.get('transmission', default_transmissions)
    drives = valid_cats.get('drive', default_drives)
    title_statuses = valid_cats.get('title_status', default_title_status)
    sizes = valid_cats.get('size', default_sizes)
    types = valid_cats.get('type', default_types)
    colors = valid_cats.get('paint_color', default_colors)
    conditions = valid_cats.get('condition', default_conditions)
    states = valid_cats.get('state', default_states)
else:
    manufacturers = default_manufacturers
    fuels = default_fuels
    transmissions = default_transmissions
    drives = default_drives
    title_statuses = default_title_status
    sizes = default_sizes
    types = default_types
    colors = default_colors
    conditions = default_conditions
    states = default_states

# ==================== TABS ====================

tab1, tab2, tab3 = st.tabs(["💰 Price Prediction", "🔧 Condition Prediction", "📖 API Documentation"])

# ==================== TAB 1: PRICE PREDICTION ====================

with tab1:
    st.header("Predict Vehicle Price")
    st.markdown("Fill in the vehicle details below to get a price prediction")
    
    with st.form("price_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📅 Basic Info")
            year = st.number_input("Year", min_value=1990, max_value=2025, value=2015, step=1)
            odometer = st.number_input("Odometer (miles)", min_value=0, max_value=500000, value=50000, step=1000)
            manufacturer = st.selectbox("Manufacturer", options=sorted(manufacturers), index=0)
            condition = st.selectbox("Condition", options=sorted(conditions), index=1)
        
        with col2:
            st.subheader("🔧 Technical Details")
            fuel = st.selectbox("Fuel Type", options=sorted(fuels), index=0)
            transmission = st.selectbox("Transmission", options=sorted(transmissions), index=0)
            drive = st.selectbox("Drive Type", options=sorted(drives), index=0)
            title_status = st.selectbox("Title Status", options=sorted(title_statuses), index=0)
        
        with col3:
            st.subheader("🎨 Appearance & Location")
            vehicle_type = st.selectbox("Vehicle Type", options=sorted(types), index=0)
            size = st.selectbox("Size", options=sorted(sizes), index=1)
            paint_color = st.selectbox("Paint Color", options=sorted(colors), index=0)
            state = st.selectbox("State", options=sorted(states), index=0)
        
        # Additional fields (hidden in expander for cleaner UI)
        with st.expander("🗺️ Location Details (Optional)"):
            col_lat, col_long = st.columns(2)
            with col_lat:
                lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=33.7490, format="%.4f")
            with col_long:
                long = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=-84.3880, format="%.4f")
            region = st.text_input("Region", value="los angeles")
        
        # Submit button
        submitted = st.form_submit_button("🔮 Predict Price", use_container_width=True)
        
        if submitted:
            if not api_status:
                st.error("⚠️ API is not running. Please start the Flask backend first.")
            else:
                with st.spinner("🤖 Analyzing vehicle data..."):
                    data = {
                        "year": int(year),
                        "odometer": int(odometer),
                        "lat": float(lat),
                        "long": float(long),
                        "manufacturer": manufacturer,
                        "fuel": fuel,
                        "title_status": title_status,
                        "transmission": transmission,
                        "drive": drive,
                        "size": size,
                        "type": vehicle_type,
                        "paint_color": paint_color,
                        "state": state,
                        "region": region,
                        "condition": condition
                    }
                    
                    try:
                        response = requests.post(f"{API_URL}/predict/price", json=data, timeout=10)
                        result = response.json()
                        
                        if result.get('success'):
                            predicted_price = result['prediction']['predicted_price']
                            
                            # Display prediction in a beautiful box
                            st.markdown(f"""
                            <div class="prediction-box">
                                💵 Predicted Price: ${predicted_price:,.2f}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show confidence metrics if available
                            if 'confidence' in result['prediction']:
                                st.metric("Confidence Score", f"{result['prediction']['confidence']:.2%}")
                            
                            # Show input summary
                            with st.expander("📋 Input Summary"):
                                st.json(data)
                        else:
                            st.error(f"❌ Prediction Error: {result.get('error', 'Unknown error')}")
                    
                    except requests.exceptions.Timeout:
                        st.error("⏱️ Request timed out. Please try again.")
                    except requests.exceptions.ConnectionError:
                        st.error("🔌 Cannot connect to API. Is the Flask server running?")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

# ==================== TAB 2: CONDITION PREDICTION ====================

with tab2:
    st.header("Predict Vehicle Condition")
    st.markdown("Enter vehicle details to predict its condition")
    
    with st.form("condition_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("💰 Price & Basic")
            price = st.number_input("Price ($)", min_value=0, max_value=200000, value=15000, step=500)
            year_c = st.number_input("Year", min_value=1990, max_value=2025, value=2015, step=1, key="year_c")
            odometer_c = st.number_input("Odometer (miles)", min_value=0, max_value=500000, value=50000, step=1000, key="odo_c")
        
        with col2:
            st.subheader("🔧 Technical Details")
            manufacturer_c = st.selectbox("Manufacturer", options=sorted(manufacturers), index=0, key="man_c")
            fuel_c = st.selectbox("Fuel Type", options=sorted(fuels), index=0, key="fuel_c")
            transmission_c = st.selectbox("Transmission", options=sorted(transmissions), index=0, key="trans_c")
        
        with col3:
            st.subheader("🎨 Appearance")
            drive_c = st.selectbox("Drive Type", options=sorted(drives), index=0, key="drive_c")
            vehicle_type_c = st.selectbox("Vehicle Type", options=sorted(types), index=0, key="type_c")
            size_c = st.selectbox("Size", options=sorted(sizes), index=1, key="size_c")
        
        # Additional fields
        with st.expander("🗺️ Additional Details (Optional)"):
            col_lat_c, col_long_c = st.columns(2)
            with col_lat_c:
                lat_c = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=33.7490, format="%.4f", key="lat_c")
                title_status_c = st.selectbox("Title Status", options=sorted(title_statuses), index=0, key="title_c")
            with col_long_c:
                long_c = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=-84.3880, format="%.4f", key="long_c")
                paint_color_c = st.selectbox("Paint Color", options=sorted(colors), index=0, key="color_c")
            
            state_c = st.selectbox("State", options=sorted(states), index=0, key="state_c")
            region_c = st.text_input("Region", value="los angeles", key="region_c")
        
        # Submit button
        submitted_c = st.form_submit_button("🔮 Predict Condition", use_container_width=True)
        
        if submitted_c:
            if not api_status:
                st.error("⚠️ API is not running. Please start the Flask backend first.")
            else:
                with st.spinner("🤖 Analyzing vehicle condition..."):
                    data = {
                        "price": int(price),
                        "year": int(year_c),
                        "odometer": int(odometer_c),
                        "lat": float(lat_c),
                        "long": float(long_c),
                        "manufacturer": manufacturer_c,
                        "fuel": fuel_c,
                        "title_status": title_status_c,
                        "transmission": transmission_c,
                        "drive": drive_c,
                        "size": size_c,
                        "type": vehicle_type_c,
                        "paint_color": paint_color_c,
                        "state": state_c,
                        "region": region_c
                    }
                    
                    try:
                        response = requests.post(f"{API_URL}/predict/condition", json=data, timeout=10)
                        result = response.json()
                        
                        if result.get('success'):
                            predicted_condition = result['prediction']['predicted_condition']
                            
                            # Display prediction
                            st.markdown(f"""
                            <div class="prediction-box">
                                🔧 Predicted Condition: {predicted_condition.upper()}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show probability distribution if available
                            if 'probabilities' in result['prediction']:
                                st.subheader("📊 Probability Distribution")
                                probs = result['prediction']['probabilities']
                                st.bar_chart(probs)
                            
                            # Show input summary
                            with st.expander("📋 Input Summary"):
                                st.json(data)
                        else:
                            st.error(f"❌ Prediction Error: {result.get('error', 'Unknown error')}")
                    
                    except requests.exceptions.Timeout:
                        st.error("⏱️ Request timed out. Please try again.")
                    except requests.exceptions.ConnectionError:
                        st.error("🔌 Cannot connect to API. Is the Flask server running?")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

# ==================== TAB 3: API DOCUMENTATION ====================

with tab3:
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
    cd frontend && streamlit run app.py
    """, language="bash")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    Made with ❤️ using Streamlit & Flask | Vehicle Prediction ML System
</div>
""", unsafe_allow_html=True)
