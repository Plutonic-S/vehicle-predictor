# Vehicle Price & Condition Predictor - Setup & Running Guide

A machine learning application that predicts vehicle prices and conditions using Flask backend and Streamlit frontend.

## 📋 Prerequisites

- Python 3.9+ installed
- Git installed
- Virtual environment already set up (`flask_env/`)

## 🚀 Quick Start (2 Steps)

### Step 1: Start the Flask Backend (Terminal 1)

```bash
# Navigate to project directory
cd Vehicle_Price_and__Condition_final

# Activate virtual environment
source flask_env/bin/activate

# Start backend
cd backend
python app.py
```

**Expected output:**
```
✅ All models loaded successfully!
🚀 Vehicle Price & Condition Prediction API
📍 Running on: http://127.0.0.1:5000
```

### Step 2: Start the Streamlit Frontend (Terminal 2)

```bash
# In a NEW terminal, navigate to project directory
cd /Vehicle_Price_and__Condition_final

# Activate virtual environment
source flask_env/bin/activate

# Start frontend
streamlit run frontend/main.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

---

## 📱 Access the Application

Open your browser and visit: **http://localhost:8501**

You should see:
- ✅ API Connected (green indicator in sidebar)
- 💰 Price Prediction tab
- 🔧 Condition Prediction tab
- 📖 API Documentation tab

---

## 🔧 Available Endpoints

### Health Check
```bash
curl http://localhost:5000/health
```

### Get Supported Values
```bash
curl http://localhost:5000/supported-values
```

### Predict Price
```bash
curl -X POST http://localhost:5000/predict/price \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### Predict Condition
```bash
curl -X POST http://localhost:5000/predict/condition \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## 📁 Project Structure

```
Vehicle_Price_and__Condition_final/
├── backend/
│   ├── app.py                 # Flask API routes
│   ├── model_handler.py       # ML model loading & predictions
│   ├── models/                # Trained ML models (.pkl files)
│   └── requirements.txt
│
├── frontend/
│   ├── main.py               # Entry point (run this!)
│   ├── app.py                # Original version (still works)
│   ├── config.py             # Configuration settings
│   ├── api_client.py         # API communication
│   ├── styles.py             # CSS & HTML templates
│   ├── utils.py              # Helper functions
│   └── components/
│       ├── sidebar.py        # Sidebar UI
│       ├── price_tab.py      # Price prediction UI
│       ├── condition_tab.py  # Condition prediction UI
│       └── api_docs_tab.py   # API documentation
│
├── flask_env/                # Virtual environment
├── SETUP.md                  # This file
└── README.md
```

---

## 🎯 Features

### 💰 Price Prediction
- Input: Vehicle details (year, mileage, manufacturer, fuel type, etc.)
- Output: Predicted price in USD

### 🔧 Condition Prediction
- Input: Vehicle details (price, year, mileage, etc.)
- Output: Predicted condition (new, like new, excellent, good, fair, salvage)

### 📊 Interactive UI
- Beautiful gradient design with responsive layout
- Real-time API health checks
- Detailed input summaries for debugging

---

## ⚙️ Configuration

**Backend Configuration** (`backend/app.py`):
- Host: 0.0.0.0
- Port: 5000 (or via `PORT` environment variable)
- Debug: ON (development mode)

**Frontend Configuration** (`frontend/config.py`):
- API URL: http://localhost:5000
- Cache TTL: 300 seconds (5 minutes)
- Request timeouts: 5-10 seconds

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill process on port 5000 if needed
lsof -ti:5000 | xargs kill -9
```

### Frontend can't connect to backend
1. Verify backend is running: `curl http://localhost:5000/health`
2. Make sure both are using the same virtual environment
3. Check firewall settings if on remote machine

### Models not loading
- Ensure `backend/models/` directory exists with all `.pkl` files
- Models should include:
  - `regression_model.pkl` (255MB)
  - `classification_model.pkl` (212MB)
  - `scaler_reg.pkl`
  - `scaler_clf.pkl`
  - `label_encoders.pkl`
  - `condition_encoder.pkl`

---

## 📝 Notes

- Backend runs in debug mode with hot-reload
- Models are cached after first load
- Predictions use LabelEncoder for categorical features
- Tree-based models (RandomForest) don't require scaling

---

## 🤝 Support

For issues or questions, check:
- Backend logs in Terminal 1
- Frontend logs in Terminal 2
- API documentation tab in the Streamlit app

---

**Happy predicting! 🚗**
