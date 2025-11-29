"""
API client for communicating with the Flask backend
"""
import requests
import streamlit as st
from config import API_URL, TIMEOUT_HEALTH, TIMEOUT_SUPPORTED_VALUES, TIMEOUT_PREDICTION, CACHE_TTL


@st.cache_data(ttl=CACHE_TTL)
def fetch_supported_values():
    """Fetch supported categorical values from API"""
    try:
        response = requests.get(f"{API_URL}/supported-values", timeout=TIMEOUT_SUPPORTED_VALUES)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Could not fetch supported values: {e}")
        return None


def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=TIMEOUT_HEALTH)
        return response.status_code == 200
    except:
        return False


def predict_price(data):
    """
    Send price prediction request to API
    
    Args:
        data (dict): Vehicle features
        
    Returns:
        dict: API response with prediction
    """
    try:
        response = requests.post(
            f"{API_URL}/predict/price",
            json=data,
            timeout=TIMEOUT_PREDICTION
        )
        return response.json()
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to API. Is the Flask server running?"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def predict_condition(data):
    """
    Send condition prediction request to API
    
    Args:
        data (dict): Vehicle features
        
    Returns:
        dict: API response with prediction
    """
    try:
        response = requests.post(
            f"{API_URL}/predict/condition",
            json=data,
            timeout=TIMEOUT_PREDICTION
        )
        return response.json()
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to API. Is the Flask server running?"}
    except Exception as e:
        return {"success": False, "error": str(e)}
