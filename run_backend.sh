#!/bin/bash
# Run Backend Server

cd "$(dirname "$0")/backend"
echo "🚀 Starting Flask Backend Server..."
echo "=================================="

# Check if virtual environment exists
if [ -d "../flask_env" ]; then
    source ../flask_env/bin/activate
    echo "✓ Virtual environment activated"
fi

python app.py
