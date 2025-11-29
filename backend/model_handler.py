"""
Model Handler for Vehicle Price and Condition Prediction
Loads trained models and handles predictions using LabelEncoder (same as notebook)
"""
import pickle
import numpy as np
import pandas as pd
from pathlib import Path

class ModelHandler:
    def __init__(self, models_dir='models'):
        """Initialize and load all models and encoders"""
        self.models_dir = Path(models_dir)
        self.current_year = 2021  # Same as training
        self.load_models()
        
    def load_models(self):
        """Load all saved models and encoders"""
        try:
            # Load regression model
            with open(self.models_dir / 'regression_model.pkl', 'rb') as f:
                self.regression_model = pickle.load(f)
            print("✓ Regression model loaded")
            
            # Load classification model
            with open(self.models_dir / 'classification_model.pkl', 'rb') as f:
                self.classification_model = pickle.load(f)
            print("✓ Classification model loaded")
            
            # Load scalers
            with open(self.models_dir / 'scaler_reg.pkl', 'rb') as f:
                self.scaler_reg = pickle.load(f)
            print("✓ Regression scaler loaded")
            
            with open(self.models_dir / 'scaler_clf.pkl', 'rb') as f:
                self.scaler_clf = pickle.load(f)
            print("✓ Classification scaler loaded")
            
            # Load label encoders for categorical features (same as notebook)
            with open(self.models_dir / 'label_encoders.pkl', 'rb') as f:
                self.label_encoders = pickle.load(f)
            print("✓ Label encoders loaded")
            
            # Load condition encoder
            with open(self.models_dir / 'condition_encoder.pkl', 'rb') as f:
                self.condition_encoder = pickle.load(f)
            print("✓ Condition encoder loaded")
            
            print("\n✅ All models loaded successfully!")
            print(f"Label encoders for {len(self.label_encoders)} categorical features")
            
        except FileNotFoundError as e:
            raise Exception(f"Model files not found. Please train and export models first: {e}")
    
    def encode_categorical(self, data):
        """
        Encode categorical features using LabelEncoder (same as notebook)
        
        Args:
            data (dict): Input features
            
        Returns:
            dict: Encoded features
        """
        encoded_data = data.copy()
        
        # Calculate vehicle_age if not provided
        if 'vehicle_age' not in encoded_data and 'year' in encoded_data:
            encoded_data['vehicle_age'] = self.current_year - encoded_data['year']
        
        # Apply label encoding to categorical features
        for feature, encoder in self.label_encoders.items():
            if feature in encoded_data:
                try:
                    # Convert to string to handle any numpy string types
                    value = str(encoded_data[feature])
                    # Transform using the trained encoder
                    encoded_data[feature] = encoder.transform([value])[0]
                except ValueError as e:
                    # Handle unknown categories
                    print(f"⚠️ Unknown value '{encoded_data[feature]}' for {feature}, using most common")
                    encoded_data[feature] = 0  # Default to first encoded value
        
        return encoded_data
    
    def predict_price(self, data):
        """
        Predict vehicle price
        
        Args:
            data (dict): Input features including:
                - year, odometer, lat, long
                - manufacturer, fuel, title_status, transmission, drive
                - size, type, paint_color, state, region, condition
                
        Returns:
            dict: Prediction result with price
        """
        # Encode categorical features using LabelEncoder
        encoded_data = self.encode_categorical(data)
        
        # Encode condition separately using condition_encoder
        if 'condition' in encoded_data:
            try:
                value = str(encoded_data['condition'])
                encoded_data['condition'] = self.condition_encoder.transform([value])[0]
            except ValueError:
                print(f"⚠️ Unknown condition '{encoded_data['condition']}', using default")
                encoded_data['condition'] = 0
        
        # Feature order for regression (16 features): 
        # year, vehicle_age, odometer, lat, long, + 11 encoded categorical
        feature_order = [
            'year', 'vehicle_age', 'odometer', 'lat', 'long',
            'manufacturer', 'fuel', 'title_status', 'transmission', 'drive',
            'size', 'type', 'paint_color', 'state', 'region', 'condition'
        ]
        
        # Create feature array in correct order
        X = np.array([[encoded_data[feature] for feature in feature_order]])
        
        # Make prediction (tree-based models don't need scaling)
        predicted_price = self.regression_model.predict(X)[0]
        
        model_name = type(self.regression_model).__name__
        
        return {
            'predicted_price': float(predicted_price),
            'model_used': model_name,
            'currency': 'USD'
        }
    
    def predict_condition(self, data):
        """
        Predict vehicle condition
        
        Args:
            data (dict): Input features including:
                - price, year, odometer, lat, long
                - manufacturer, fuel, title_status, transmission, drive
                - size, type, paint_color, state, region
                
        Returns:
            dict: Prediction result with condition
        """
        # Encode categorical features using LabelEncoder
        encoded_data = self.encode_categorical(data)
        
        # Feature order for classification (16 features, no condition):
        # price, year, vehicle_age, odometer, lat, long, + 10 encoded categorical
        feature_order = [
            'price', 'year', 'vehicle_age', 'odometer', 'lat', 'long',
            'manufacturer', 'fuel', 'title_status', 'transmission', 'drive',
            'size', 'type', 'paint_color', 'state', 'region'
        ]
        
        # Create feature array in correct order
        X = np.array([[encoded_data[feature] for feature in feature_order]])
        
        # Make prediction (tree-based models don't need scaling)
        predicted_encoded = self.classification_model.predict(X)[0]
        predicted_condition = self.condition_encoder.inverse_transform([predicted_encoded])[0]
        
        # Get probability if available
        probabilities = None
        if hasattr(self.classification_model, 'predict_proba'):
            probs = self.classification_model.predict_proba(X)[0]
            probabilities = {
                condition: float(prob) 
                for condition, prob in zip(self.condition_encoder.classes_, probs)
            }
        
        model_name = type(self.classification_model).__name__
        
        result = {
            'predicted_condition': predicted_condition,
            'model_used': model_name
        }
        
        if probabilities:
            result['probabilities'] = probabilities
        
        return result
    
    def get_supported_values(self):
        """Get all supported categorical values for inputs"""
        # Return example values or common categories
        supported = {
            'manufacturer': ['toyota', 'ford', 'chevrolet', 'honda', 'nissan', 'jeep', 'ram', 'gmc'],
            'fuel': ['gas', 'diesel', 'hybrid', 'electric', 'other'],
            'title_status': ['clean', 'rebuilt', 'lien', 'salvage', 'missing', 'parts only'],
            'transmission': ['automatic', 'manual', 'other'],
            'drive': ['fwd', 'rwd', '4wd', 'awd'],
            'size': ['compact', 'mid-size', 'full-size', 'sub-compact'],
            'type': ['sedan', 'suv', 'truck', 'coupe', 'wagon', 'van', 'convertible', 'hatchback', 'pickup'],
            'paint_color': ['white', 'black', 'silver', 'grey', 'blue', 'red', 'brown', 'green', 'yellow', 'orange'],
            'state': ['ca', 'tx', 'fl', 'ny', 'pa', 'il', 'oh', 'ga', 'nc', 'mi'],
            'condition': ['excellent', 'good', 'fair', 'like new', 'new', 'salvage']
        }
        return supported
    
    def get_valid_categories(self):
        """
        Get valid categories from the trained label encoders
        
        Returns:
            dict: Dictionary of feature names and their valid values
        """
        categories = {}
        
        # Get categories from label encoders
        for feature, encoder in self.label_encoders.items():
            categories[feature] = list(encoder.classes_)
        
        # Add condition categories from condition encoder
        categories['condition'] = list(self.condition_encoder.classes_)
        
        return categories
    
    def get_feature_info(self):
        """
        Get feature information for API documentation
        
        Returns:
            dict: Feature descriptions and requirements
        """
        return {
            'regression_features': {
                'required': ['year', 'odometer', 'lat', 'long', 'manufacturer', 'fuel', 
                           'title_status', 'transmission', 'drive', 'size', 'type', 
                           'paint_color', 'state', 'region', 'condition'],
                'description': 'Features needed for price prediction (16 total)'
            },
            'classification_features': {
                'required': ['price', 'year', 'odometer', 'lat', 'long', 'manufacturer', 
                           'fuel', 'title_status', 'transmission', 'drive', 'size', 
                           'type', 'paint_color', 'state', 'region'],
                'description': 'Features needed for condition prediction (16 total, excluding condition)'
            },
            'encoding_method': 'LabelEncoder (same as training notebook)',
            'current_year': self.current_year
        }
