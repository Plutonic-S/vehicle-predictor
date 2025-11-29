"""
Price prediction tab component
"""
import streamlit as st
from api_client import predict_price


def render_price_tab(api_status, categories):
    """
    Render the price prediction tab
    
    Args:
        api_status (bool): Whether the API is connected
        categories (dict): Dictionary of valid categories
    """
    st.header("Predict Vehicle Price")
    st.markdown("Fill in the vehicle details below to get a price prediction")
    
    with st.form("price_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📅 Basic Info")
            year = st.number_input("Year", min_value=1990, max_value=2025, value=2015, step=1)
            odometer = st.number_input("Odometer (miles)", min_value=0, max_value=500000, value=50000, step=1000)
            manufacturer = st.selectbox("Manufacturer", options=sorted(categories['manufacturers']), index=0)
            condition = st.selectbox("Condition", options=sorted(categories['conditions']), index=1)
        
        with col2:
            st.subheader("🔧 Technical Details")
            fuel = st.selectbox("Fuel Type", options=sorted(categories['fuels']), index=0)
            transmission = st.selectbox("Transmission", options=sorted(categories['transmissions']), index=0)
            drive = st.selectbox("Drive Type", options=sorted(categories['drives']), index=0)
            title_status = st.selectbox("Title Status", options=sorted(categories['title_status']), index=0)
        
        with col3:
            st.subheader("🎨 Appearance & Location")
            vehicle_type = st.selectbox("Vehicle Type", options=sorted(categories['types']), index=0)
            size = st.selectbox("Size", options=sorted(categories['sizes']), index=1)
            paint_color = st.selectbox("Paint Color", options=sorted(categories['colors']), index=0)
            state = st.selectbox("State", options=sorted(categories['states']), index=0)
        
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
                    
                    result = predict_price(data)
                    
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
