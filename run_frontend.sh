#!/bin/bash
# Run Frontend Server

cd "$(dirname "$0")/frontend"
echo "🎨 Starting Streamlit Frontend..."
echo "================================="

# Check if virtual environment exists
if [ -d "../flask_env" ]; then
    source ../flask_env/bin/activate
    echo "✓ Virtual environment activated"
fi

streamlit run app.py
