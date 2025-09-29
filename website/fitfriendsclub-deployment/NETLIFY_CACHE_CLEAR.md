# Netlify Cache Clearing Guide for FitFriendsClub

## 🧹 Clear Netlify Deployment Cache

### Method 1: Netlify Dashboard (Recommended)
1. **Go to your Netlify dashboard**: https://app.netlify.com
2. **Select your FitFriendsClub site**
3. **Go to Site settings → Build & deploy**
4. **Click "Clear cache"** or **"Clear cache and retry deploy"**
5. **Trigger a new deployment**

### Method 2: Netlify CLI (if installed)
```bash
# Install Netlify CLI (if not already installed)
npm install -g netlify-cli

# Login to Netlify
netlify login

# Clear build cache
netlify build:clear-cache

# Trigger new deployment
netlify deploy --prod
```

### Method 3: Force New Build
1. **In Netlify dashboard → Deploys**
2. **Click "Trigger deploy"**
3. **Select "Clear cache and deploy site"**

## 🎯 After Clearing Cache

### Option A: Use Binary-Only Requirements
Update your Netlify build settings to use:
```bash
# Build command:
cd backend && pip install -r requirements-binary-only.txt

# Or with our nuclear option:
./deploy-with-binary-enforcement.sh
```

### Option B: Environment Variables
Add these environment variables in Netlify:
- `PIP_NO_CACHE_DIR=1`
- `PIP_PREFER_BINARY=1` 
- `PIP_ONLY_BINARY=psycopg2,psycopg2-binary`

## 🚨 Important for Your pg_config Error
Since you're getting `pg_config executable not found`, make sure to:

1. ✅ Clear Netlify cache (steps above)
2. ✅ Use `requirements-binary-only.txt` 
3. ✅ Set environment variables to force binary installation
4. ✅ Redeploy

This will prevent Netlify from trying to compile `psycopg2` from source.