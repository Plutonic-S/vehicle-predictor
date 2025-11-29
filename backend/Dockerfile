FROM python:3.9-slim

WORKDIR /app

# Install dependencies (including huggingface_hub for model download)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt huggingface_hub

# Copy application code (not models - they'll be downloaded)
COPY app.py model_handler.py ./

# Download models from Hugging Face
RUN mkdir -p /app/models && \
    python -c "from huggingface_hub import hf_hub_download; \
    import shutil; \
    files = ['classification_model.pkl', 'regression_model.pkl', 'scaler_clf.pkl', 'scaler_reg.pkl', 'label_encoders.pkl', 'condition_encoder.pkl']; \
    for f in files: \
        downloaded_path = hf_hub_download(repo_id='Aleph-7/vehicle-predictor-models', filename=f); \
        shutil.copy(downloaded_path, f'/app/models/{f}'); \
    print('✅ Models downloaded and copied')"

# Verify models are present
RUN ls -la /app/models && echo "Model files:" && ls -lh /app/models/*.pkl

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run with gunicorn for production
# Use shell form to allow PORT environment variable substitution
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120 --chdir /app app:app
