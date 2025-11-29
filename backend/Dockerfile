FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (not models - they'll be downloaded)
COPY app.py model_handler.py download_models.py ./

# Download models from Hugging Face
RUN python download_models.py

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run with gunicorn for production
# Render provides PORT environment variable, default to 10000 for compatibility
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app
