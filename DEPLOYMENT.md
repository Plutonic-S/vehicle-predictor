# 🚀 Deploying to Render

This guide will help you deploy your Vehicle Price & Condition Predictor to Render.

## Prerequisites

1. Create a [GitHub](https://github.com) account (if you don't have one)
2. Create a [Render](https://render.com) account (free tier available)
3. Push your code to GitHub

## Step 1: Push Code to GitHub

```bash
# Initialize git (if not already done)
cd /home/pluto/Documents/trashuni/workshop/Vehicle_Price_and__Condition_final
git init

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
flask_env/
env/
venv/
.env
.vscode/
.idea/
*.log
.DS_Store
EOF

# Add files
git add backend/ frontend/ .dockerignore README.md
git commit -m "Initial commit - Vehicle Price Predictor"

# Create repository on GitHub and push
# (Follow GitHub instructions to create repo and add remote)
git remote add origin https://github.com/YOUR_USERNAME/vehicle-predictor.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy Backend to Render

1. **Go to Render Dashboard**: https://dashboard.render.com

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Click "Connect" next to your repository

3. **Configure Backend Service**:
   ```
   Name: vehicle-predictor-api
   Region: Choose closest to you
   Branch: main
   Root Directory: backend
   Runtime: Docker
   Instance Type: Free
   ```

4. **Environment Variables** (Optional):
   ```
   FLASK_ENV=production
   ```

5. Click **"Create Web Service"**

6. Wait for deployment (5-10 minutes)

7. **Copy your backend URL**: `https://vehicle-predictor-api.onrender.com`

## Step 3: Deploy Frontend to Render

1. **Create Another Web Service**:
   - Click "New +" → "Web Service"
   - Select same repository

2. **Configure Frontend Service**:
   ```
   Name: vehicle-predictor-frontend
   Region: Same as backend
   Branch: main
   Root Directory: frontend
   Runtime: Docker
   Instance Type: Free
   ```

3. **Environment Variables** (IMPORTANT):
   ```
   BACKEND_URL=https://vehicle-predictor-api.onrender.com
   ```
   (Use the backend URL from Step 2)

4. Click **"Create Web Service"**

5. Wait for deployment (5-10 minutes)

## Step 4: Test Your Deployment

1. Open your frontend URL: `https://vehicle-predictor-frontend.onrender.com`

2. Check API connection status in the sidebar

3. Try making a prediction!

## Important Notes

### Free Tier Limitations
- Services spin down after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (enough for one service running 24/7)

### Cold Starts
If you get a timeout on first request:
1. Wait 30-60 seconds for backend to wake up
2. Refresh the page
3. Try prediction again

### Troubleshooting

**Backend not loading models?**
- Check that `backend/models/` directory is in your git repository
- Verify all `.pkl` files are committed

**Frontend can't connect to backend?**
- Verify `BACKEND_URL` environment variable is set correctly
- Check backend service is running in Render dashboard
- Make sure CORS is enabled (already configured in `app.py`)

**Deployment failed?**
- Check deployment logs in Render dashboard
- Verify Dockerfile syntax
- Ensure all dependencies are in `requirements.txt`

## Monitoring

- View logs in Render dashboard
- Monitor service health
- Check deployment history

## Upgrade to Paid Plan

For production use, consider upgrading to avoid cold starts:
- **Starter**: $7/month per service (no sleeping)
- **Standard**: $25/month per service (more resources)

## Alternative: Deploy Both in Same Service

If you want to save on free tier hours, you can deploy both backend and frontend in one service using a custom startup script. Let me know if you want instructions for this approach!

---

## Next Steps

After deployment:
1. Test all functionality
2. Share your deployed URL with others
3. Consider adding authentication for production use
4. Set up monitoring and error tracking
5. Add a custom domain (optional)

Congratulations! 🎉 Your ML application is now live!
