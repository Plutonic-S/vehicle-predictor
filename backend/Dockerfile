FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (not models - they'll be downloaded)
COPY app.py model_handler.py download_models.py ./

# Download models from Hugging Face
RUN python download_models.py

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run with gunicorn for production
# Use shell form to allow PORT environment variable substitution
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120 --chdir /app app:app
