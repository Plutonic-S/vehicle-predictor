# 🚗 Vehicle Price & Condition Predictor

A full-stack machine learning application for predicting vehicle prices and conditions using Flask (backend) and Streamlit (frontend).

## 🌟 Features

- **💰 Price Prediction**: Predict vehicle price based on multiple features
- **🔧 Condition Prediction**: Predict vehicle condition (excellent, good, fair, etc.)
- **🎨 Beautiful UI**: Modern, responsive interface built with Streamlit
- **🔄 Real-time API**: RESTful API with Flask backend
- **📊 Interactive**: Dynamic forms with validation and error handling

## 📋 Prerequisites

- Python 3.8+
- Virtual environment (included as `flask_env/`)

## 📁 Project Structure

```
Vehicle_Price_and__Condition_final/
├── backend/                        # Flask API Backend
│   ├── app.py                      # Flask application & API routes
│   ├── model_handler.py            # ML model handling logic
│   ├── requirements.txt            # Backend dependencies
│   └── models/                     # Trained ML models
│       ├── regression_model.pkl
│       ├── classification_model.pkl
│       ├── scaler_reg.pkl
│       ├── scaler_clf.pkl
│       ├── label_encoders.pkl
│       └── condition_encoder.pkl
│
├── frontend/                       # Streamlit Frontend
│   ├── app.py                      # Streamlit application
│   └── requirements.txt            # Frontend dependencies
│
├── flask_env/                      # Python virtual environment
├── vehicles.csv                    # Dataset
├── Vehicle_Price_and_Condition.ipynb  # Model training notebook
├── run_backend.sh                  # Script to run backend
├── run_frontend.sh                 # Script to run frontend
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Activate Virtual Environment

```bash
source flask_env/bin/activate
```

### 2. Start Flask Backend (Terminal 1)

```bash
# Option 1: Using the run script
./run_backend.sh

# Option 2: Manual
cd backend
python app.py
```

The API will be available at: `http://localhost:5000`

### 3. Start Streamlit Frontend (Terminal 2)

```bash
# Activate the same virtual environment in a new terminal
source flask_env/bin/activate

# Option 1: Using the run script
./run_frontend.sh

# Option 2: Manual
cd frontend
streamlit run app.py
```

The web UI will automatically open at: `http://localhost:8501`

## 🔌 API Endpoints

### GET `/`
API information and available endpoints

### GET `/health`
Health check endpoint

### POST `/predict/price`
Predict vehicle price

**Request:**
```json
{
  "year": 2015,
  "odometer": 50000,
  "manufacturer": "toyota",
  "fuel": "gas",
  "transmission": "automatic",
  "drive": "fwd",
  "size": "mid-size",
  "type": "sedan",
  "paint_color": "white",
  "condition": "good",
  "title_status": "clean",
  "state": "ca",
  "region": "los angeles",
  "lat": 33.7490,
  "long": -84.3880
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "predicted_price": 15000.50,
    "model_used": "RandomForestRegressor",
    "currency": "USD"
  }
}
```

### POST `/predict/condition`
Predict vehicle condition

**Request:**
```json
{
  "price": 15000,
  "year": 2015,
  "odometer": 50000,
  "manufacturer": "toyota",
  "fuel": "gas",
  "transmission": "automatic",
  "drive": "fwd",
  "size": "mid-size",
  "type": "sedan",
  "paint_color": "white",
  "title_status": "clean",
  "state": "ca",
  "region": "los angeles",
  "lat": 33.7490,
  "long": -84.3880
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "predicted_condition": "good",
    "model_used": "RandomForestClassifier",
    "probabilities": {
      "excellent": 0.15,
      "good": 0.65,
      "fair": 0.12,
      "like new": 0.05,
      "new": 0.02,
      "salvage": 0.01
    }
  }
}
```

### GET `/supported-values`
Get all supported categorical values for inputs

## 🛠️ Development

### Install Dependencies

```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

# Frontend dependencies
cd ../frontend
pip install -r requirements.txt
```

### Re-train Models

1. Open `Vehicle_Price_and_Condition.ipynb` in Jupyter
2. Run all cells to train new models
3. Models will be exported to `models/` directory
4. Copy the models to `backend/models/`

## 📊 Model Details

- **Price Prediction**: Random Forest Regressor
- **Condition Prediction**: Random Forest Classifier
- **Feature Encoding**: LabelEncoder for categorical features
- **Training Year**: 2021 (used for vehicle age calculation)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is for educational purposes.

---
Made with ❤️ using Flask, Streamlit & Scikit-learn
