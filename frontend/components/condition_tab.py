"""
Condition prediction tab component
"""
import streamlit as st
from api_client import predict_condition


def render_condition_tab(api_status, categories):
    """
    Render the condition prediction tab
    
    Args:
        api_status (bool): Whether the API is connected
        categories (dict): Dictionary of valid categories
    """
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
            manufacturer_c = st.selectbox("Manufacturer", options=sorted(categories['manufacturers']), index=0, key="man_c")
            fuel_c = st.selectbox("Fuel Type", options=sorted(categories['fuels']), index=0, key="fuel_c")
            transmission_c = st.selectbox("Transmission", options=sorted(categories['transmissions']), index=0, key="trans_c")
        
        with col3:
            st.subheader("🎨 Appearance")
            drive_c = st.selectbox("Drive Type", options=sorted(categories['drives']), index=0, key="drive_c")
            vehicle_type_c = st.selectbox("Vehicle Type", options=sorted(categories['types']), index=0, key="type_c")
            size_c = st.selectbox("Size", options=sorted(categories['sizes']), index=1, key="size_c")
        
        # Additional fields
        with st.expander("🗺️ Additional Details (Optional)"):
            col_lat_c, col_long_c = st.columns(2)
            with col_lat_c:
                lat_c = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=33.7490, format="%.4f", key="lat_c")
                title_status_c = st.selectbox("Title Status", options=sorted(categories['title_status']), index=0, key="title_c")
            with col_long_c:
                long_c = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=-84.3880, format="%.4f", key="long_c")
                paint_color_c = st.selectbox("Paint Color", options=sorted(categories['colors']), index=0, key="color_c")
            
            state_c = st.selectbox("State", options=sorted(categories['states']), index=0, key="state_c")
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
                    
                    result = predict_condition(data)
                    
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
