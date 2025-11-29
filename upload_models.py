#!/usr/bin/env python3
"""
Upload model files to Hugging Face Hub
Run this script to upload your trained models for deployment
"""

from huggingface_hub import HfApi, login
import os

# Login to Hugging Face (will prompt for token)
print("🔐 Logging into Hugging Face...")
print("Get your token from: https://huggingface.co/settings/tokens")
print("Make sure to create a token with WRITE permissions!")
print("\nEnter your NEW token (paste and press Enter):")
token = input().strip()
login(token=token)

# Initialize API
api = HfApi()

# Repository details
repo_id = "Aleph-7/vehicle-predictor-models"
repo_type = "model"

# Create repository if it doesn't exist
print(f"\n📦 Creating repository: {repo_id}")
try:
    api.create_repo(repo_id=repo_id, repo_type=repo_type, exist_ok=True, private=False)
    print("✅ Repository created/verified")
except Exception as e:
    print(f"⚠️  Repository issue: {e}")
    print("   Continuing with upload attempt...")

# Upload model files from backend/models directory
models_dir = "backend/models"
model_files = [
    "classification_model.pkl",
    "regression_model.pkl",
    "scaler_clf.pkl",
    "scaler_reg.pkl",
    "label_encoders.pkl",
    "condition_encoder.pkl"
]

print("\n📤 Uploading model files...")
for model_file in model_files:
    file_path = os.path.join(models_dir, model_file)
    if os.path.exists(file_path):
        print(f"  Uploading {model_file}...")
        try:
            api.upload_file(
                path_or_fileobj=file_path,
                path_in_repo=model_file,
                repo_id=repo_id,
                repo_type=repo_type,
            )
            print(f"  ✅ {model_file} uploaded")
        except Exception as e:
            print(f"  ❌ Failed to upload {model_file}: {e}")
    else:
        print(f"  ⚠️  {model_file} not found at {file_path}")

print("\n✅ Upload complete!")
print(f"🌐 Models available at: https://huggingface.co/{repo_id}")
print("\nNext step: Update Dockerfile to download these models during build")
