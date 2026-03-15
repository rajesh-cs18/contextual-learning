# Deployment Guide - Streamlit Community Cloud

## Prerequisites
- GitHub account
- Your code pushed to a GitHub repository
- Gemini API key ready

## Step-by-Step Deployment

### 1. Prepare Your Repository

```bash
cd /Users/rajesh/work/pirbhu/contextual-learning

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Theory2Practice AI Bridge"

# Create a new repository on GitHub at: https://github.com/new
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/theory2practice.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Streamlit Community Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Click "Sign in" and authorize with GitHub

2. **Create New App**
   - Click "New app" button
   - Select your repository: `YOUR_USERNAME/theory2practice`
   - Main file path: `app.py`
   - App URL: Choose your subdomain (e.g., `theory2practice.streamlit.app`)

3. **Configure Secrets (IMPORTANT)**
   - Click "Advanced settings" before deploying
   - In the "Secrets" section, add:
     ```toml
     GEMINI_API_KEY = "AIzasdSyAQGNuqzDwyWtebjMdR-fPG_tKukjA5rt"
     ```
   - Click "Save"

4. **Deploy**
   - Click "Deploy!"
   - Wait 2-3 minutes for initial deployment

### 3. Your App is Live! 🎉

Your app will be available at:
```
https://YOUR_SUBDOMAIN.streamlit.app
```

## Updating Your App

Every time you push to GitHub, Streamlit automatically redeploys:

```bash
git add .
git commit -m "Updated feature"
git push
```

Wait ~1 minute and your changes are live!

## Managing Secrets

To update your API key later:

1. Go to your app on Streamlit Cloud
2. Click the hamburger menu (⋮)
3. Click "Settings"
4. Go to "Secrets" tab
5. Edit and save

## Monitoring

- **Logs:** View in Streamlit Cloud dashboard
- **Metrics:** Check app usage and errors
- **Restarts:** Can manually restart from settings

## Benefits of Streamlit Cloud

✅ **Free hosting** for public apps  
✅ **Auto-updates** on git push  
✅ **No DevOps required**  
✅ **Secure secrets management**  
✅ **Custom domain support** (paid plans)  
✅ **Built for Streamlit apps**  

## Troubleshooting

**App won't start?**
- Check logs in Streamlit Cloud dashboard
- Verify `requirements.txt` has all dependencies
- Ensure Python version compatibility (3.10+)

**API key not working?**
- Check secrets syntax (TOML format)
- No quotes around the key if using TOML
- Restart app after updating secrets

**App is slow?**
- Streamlit Cloud free tier is shared
- Consider caching with `@st.cache_data`
- Reduce number of use cases for faster generation

## Alternative: Deploy to Railway

If you prefer Railway:

1. Go to https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Select your repository
4. Add environment variable:
   - Key: `GEMINI_API_KEY`
   - Value: Your API key
5. Railway auto-detects and deploys

## Cost Comparison

| Platform | Free Tier | Best For |
|----------|-----------|----------|
| **Streamlit Cloud** | Unlimited public apps | Streamlit apps (BEST) |
| **Railway** | $5 credit/month | Quick deploys |
| **Render** | 750 hours/month | Python apps |
| **Heroku** | Deprecated free tier | N/A |
| **Google Cloud Run** | Pay-per-use | Production at scale |

---

**Recommendation:** Start with **Streamlit Community Cloud** - it's specifically designed for this and completely free for public apps!
