# 🚀 FitFriendsClub Backend Deployment Guide

## 🔧 Fixing PostgreSQL Build Issues

### Problem
If you're getting this error during deployment:
```
Error: pg_config executable not found
```

### ✅ **Solution 1: Use SQLite (Recommended)**

Your backend is already configured to use SQLite by default, which works perfectly for most fitness apps.

**For Railway/Render/Heroku deployment:**
1. Use `requirements.txt` (already configured without PostgreSQL)
2. Your app will automatically use SQLite
3. No additional configuration needed

### ✅ **Solution 2: Enable PostgreSQL (Advanced)**

If you specifically need PostgreSQL:

**Option A: Update requirements.txt**
```bash
# Add this to requirements.txt
psycopg2-binary
```

**Option B: Platform-specific fixes**

**Railway:**
```bash
# Add to railway.toml
[build]
  builder = "nixpacks"

[deploy]
  startCommand = "cd backend && gunicorn app:app --bind 0.0.0.0:$PORT"
```

**Render:**
```bash
# In Build Command field:
cd backend && pip install -r requirements.txt

# In Start Command field:
cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
```

**Heroku:**
```bash
# Create requirements.txt with:
flask==3.0.3
flask-cors==5.0.0
python-dotenv==1.0.1
requests==2.32.4
PyJWT==2.9.0
gunicorn==21.2.0
psycopg2-binary
```

### 🎯 **Recommended Deployment Steps**

1. **Deploy with SQLite first** (zero configuration)
2. **Test your app** to ensure everything works
3. **Upgrade to PostgreSQL later** if needed

### 🔗 **Platform-Specific Deployment**

**Railway (Recommended):**
1. Connect GitHub repo
2. Select `backend` folder as root
3. Deploy automatically

**Render:**
1. Connect GitHub repo  
2. Build Command: `cd backend && pip install -r requirements.txt`
3. Start Command: `cd backend && gunicorn app:app --bind 0.0.0.0:$PORT`

**Heroku:**
1. Use `Procfile` (already created)
2. Set buildpack to Python
3. Deploy from GitHub

### 📊 **Database Migration**

Your app automatically handles both SQLite and PostgreSQL:
- **Development:** SQLite (local file)
- **Production:** PostgreSQL (if DATABASE_URL is set)
- **Fallback:** SQLite (if PostgreSQL unavailable)

### 🛠️ **Environment Variables**

Set these in your deployment platform:

```bash
# Optional: Only if using PostgreSQL
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Required: JWT secret
SECRET_KEY=your-secret-key-here
```

### ✅ **Zero-Config Deployment**

For the easiest deployment, your current setup works out of the box with:
- Railway
- Render  
- Heroku
- Any Python hosting platform

No PostgreSQL configuration needed! 🚀