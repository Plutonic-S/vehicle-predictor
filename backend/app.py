"""
Flask Backend for Vehicle Price and Condition Prediction API
Exposes ML models through REST endpoints
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from model_handler import ModelHandler

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize model handler
try:
    model_handler = ModelHandler(models_dir='models')
    models_loaded = True
except Exception as e:
    print(f"⚠️  Warning: Could not load models: {e}")
    models_loaded = False

# ==================== ROUTES ====================

@app.route('/', methods=['GET'])
def home():
    """Root endpoint - API information"""
    return jsonify({
        'message': 'Vehicle Price and Condition Prediction API',
        'version': '1.0.0',
        'models_loaded': models_loaded,
        'endpoints': {
            'GET /': 'API information',
            'GET /health': 'Health check',
            'POST /predict/price': 'Predict vehicle price',
            'POST /predict/condition': 'Predict vehicle condition',
            'GET /supported-values': 'Get supported categorical values'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': models_loaded
    })

@app.route('/predict/price', methods=['POST'])
def predict_price():
    """
    Predict vehicle price
    
    Expected JSON body:
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
    """
    if not models_loaded:
        return jsonify({
            'error': 'Models not loaded. Please train and export models first.'
        }), 500
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Validate required fields
        required_fields = ['year', 'odometer', 'manufacturer', 'fuel', 'transmission']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Make prediction
        result = model_handler.predict_price(data)
        
        return jsonify({
            'success': True,
            'prediction': result,
            'input': data
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/predict/condition', methods=['POST'])
def predict_condition():
    """
    Predict vehicle condition
    
    Expected JSON body:
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
    """
    if not models_loaded:
        return jsonify({
            'error': 'Models not loaded. Please train and export models first.'
        }), 500
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Validate required fields
        required_fields = ['price', 'year', 'odometer', 'manufacturer', 'fuel', 'transmission']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Make prediction
        result = model_handler.predict_condition(data)
        
        return jsonify({
            'success': True,
            'prediction': result,
            'input': data
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/supported-values', methods=['GET'])
def get_supported_values():
    """Get all supported categorical values for inputs"""
    if not models_loaded:
        return jsonify({
            'error': 'Models not loaded'
        }), 500
    
    try:
        categories = model_handler.get_valid_categories()
        feature_info = model_handler.get_feature_info()
        return jsonify({
            'success': True,
            'valid_categories': categories,
            'feature_info': feature_info
        })
    except Exception as e:
        return jsonify({
            'error': f'Failed to retrieve supported values: {str(e)}'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== RUN APP ====================

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    # Debug mode off in production
    debug = os.getenv('FLASK_ENV') != 'production' and os.getenv('FLASK_DEBUG', '1') == '1'
    
    print("\n" + "="*60)
    print("🚀 Vehicle Price & Condition Prediction API")
    print("="*60)
    print(f"📍 Running on: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"📦 Models loaded: {models_loaded}")
    print(f"🌍 Environment: {os.getenv('FLASK_ENV', 'development')}")
    print("="*60 + "\n")
    
    app.run(host=host, port=port, debug=debug)
