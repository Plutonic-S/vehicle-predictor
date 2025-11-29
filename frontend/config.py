"""
Configuration settings for the Streamlit application
"""

# API Configuration
API_URL = "http://localhost:5000"

# Cache settings
CACHE_TTL = 300  # 5 minutes

# Timeout settings (in seconds)
TIMEOUT_HEALTH = 5
TIMEOUT_SUPPORTED_VALUES = 10
TIMEOUT_PREDICTION = 10

# Page configuration
PAGE_TITLE = "Vehicle Predictor"
PAGE_ICON = "🚗"
LAYOUT = "wide"

# Default values for dropdowns
DEFAULT_VALUES = {
    "manufacturers": ["toyota", "ford", "honda", "chevrolet", "nissan", "bmw", "mercedes-benz", "volkswagen"],
    "fuels": ["gas", "diesel", "electric", "hybrid", "other"],
    "transmissions": ["automatic", "manual", "other"],
    "drives": ["fwd", "rwd", "4wd", "awd"],
    "title_status": ["clean", "rebuilt", "salvage", "lien", "missing"],
    "sizes": ["compact", "mid-size", "full-size", "sub-compact"],
    "types": ["sedan", "suv", "truck", "coupe", "wagon", "convertible", "hatchback", "van", "pickup"],
    "colors": ["white", "black", "silver", "gray", "blue", "red", "brown", "green", "orange", "yellow"],
    "conditions": ["excellent", "good", "fair", "like new", "new", "salvage"],
    "states": ["ca", "ny", "tx", "fl", "pa", "il", "oh", "ga", "nc", "mi"]
}
