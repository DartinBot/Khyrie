# 🚨 pg_config ERROR TROUBLESHOOTING GUIDE

## The Problem
```
Error: pg_config executable not found.
pg_config is required to build psycopg2 from source.
```

This happens when your deployment platform tries to install `psycopg2` (source) instead of `psycopg2-binary` (pre-compiled).

## 🎯 SOLUTIONS (Try in order)

### Solution 1: Clear Deployment Cache
Your platform may have cached the source `psycopg2` package. 
**Clear the deployment cache completely** and redeploy.

### Solution 2: Use Binary-Only Requirements
Replace your requirements.txt with `requirements-binary-only.txt`:
```bash
# In your deployment settings, change the install command to:
pip install -r backend/requirements-binary-only.txt
```

### Solution 3: Use Nuclear Deployment Script
```bash
# Run this in your deployment environment:
./deploy-with-binary-enforcement.sh
```

### Solution 4: Update Procfile
Replace `Procfile` with `Procfile-binary-only`:
```bash
cp Procfile-binary-only Procfile
```

### Solution 5: Platform-Specific Fixes

**Heroku:**
- Use `app.json` (already configured)
- Clear build cache: `heroku builds:cache:purge`

**Railway:**
- Add to environment variables:
  - `PIP_ONLY_BINARY=:all:`
  - `PIP_PREFER_BINARY=1`
  - `PIP_NO_CACHE_DIR=1`

**Render:**
- In Build Command: `pip install --only-binary=:all: -r backend/requirements-binary-only.txt`

### Solution 6: Ultimate Nuclear Option
If all else fails, use the nuclear deployment script which:
- Blocks ALL source compilation with `--only-binary=:all:`
- Uses constraints.txt to prevent psycopg2 source installation
- Clears all caches
- Uses binary-only requirements

## 🛡️ Files Created for You
- ✅ `constraints.txt` - Blocks source psycopg2
- ✅ `requirements-binary-only.txt` - Only binary packages
- ✅ `Procfile-binary-only` - Alternative Procfile
- ✅ `deploy-with-binary-enforcement.sh` - Nuclear option script
- ✅ `app.json` - Heroku configuration with binary enforcement

## 🎯 Why This Happens
1. Platform has cached source `psycopg2`
2. Another dependency requests `psycopg2` instead of `psycopg2-binary`
3. Platform ignores binary-only flags
4. Old configuration cached by platform

## ✅ Expected Result
After applying fixes, you should see:
```
Successfully installed psycopg2-binary-2.9.9
```
Instead of:
```
Error: pg_config executable not found
```