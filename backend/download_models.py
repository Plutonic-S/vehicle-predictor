"""
Download model files from Hugging Face Hub
"""
from huggingface_hub import hf_hub_download
import shutil
import os

# Create models directory
os.makedirs('/app/models', exist_ok=True)

# List of model files to download
files = [
    'classification_model.pkl',
    'regression_model.pkl',
    'scaler_clf.pkl',
    'scaler_reg.pkl',
    'label_encoders.pkl',
    'condition_encoder.pkl'
]

# Download each file
print("Downloading models from Hugging Face...")
for filename in files:
    print(f"Downloading {filename}...")
    downloaded_path = hf_hub_download(
        repo_id='Aleph-7/vehicle-predictor-models',
        filename=filename
    )
    target_path = f'/app/models/{filename}'
    shutil.copy(downloaded_path, target_path)
    print(f"✓ Copied {filename} to {target_path}")

print("\n✅ All models downloaded and copied successfully!")
print("\nModel files:")
for filename in os.listdir('/app/models'):
    filepath = f'/app/models/{filename}'
    size = os.path.getsize(filepath)
    print(f"  {filename}: {size:,} bytes")
