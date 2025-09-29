# 🚀 FitFriendsClub Deployment Guide

## 📦 Dependency Management

### Production Requirements
```bash
pip install -r backend/requirements.txt
```

### Development Requirements (Optional)
```bash
pip install -r backend/requirements-dev.txt
```

### PostgreSQL Support (Optional)
```bash
./install-postgresql.sh
```

## 🔧 Deployment Solutions for Common Issues

### 1. Build Failures During Dependency Installation

**Problem:** Non-zero exit code during pip install
**Solution:** Use fixed version requirements.txt

✅ **Fixed Issues:**
- Pinned all package versions for consistency
- Removed development tools from production requirements
- Added explicit setuptools for build stability
- Specified Python runtime version

### 2. PostgreSQL PATH Configuration

**If you need pg_config in your build environment:**

#### Automatic Setup
```bash
./setup-postgresql-path.sh  # Interactive PATH configuration
```

#### Manual Setup
Add PostgreSQL to your PATH in shell configuration:

**For Homebrew PostgreSQL:**
```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**For Postgres.app:**
```bash
echo 'export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Verify Configuration
```bash
which pg_config
pg_config --version
```

### 3. Platform-Specific Deployments

#### Railway
```bash
# Uses requirements.txt and runtime.txt automatically
# Set environment variables in Railway dashboard
# PostgreSQL: Uses psycopg2-binary (no pg_config needed)
```

#### Heroku
```bash
# Add Procfile (already configured):
# web: cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
# PostgreSQL: Uses psycopg2-binary (no pg_config needed)
```

#### Render
```bash
# Build Command: pip install -r backend/requirements.txt
# Start Command: gunicorn --chdir backend app:app
# PostgreSQL: Uses psycopg2-binary (no pg_config needed)
```

#### Docker
```dockerfile
FROM python:3.8.19-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ ./backend/
CMD ["gunicorn", "--chdir", "backend", "app:app"]
```

### 3. Environment Variables

Required for production:
```bash
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:port/dbname  # Optional
```

### 4. Database Configuration

**SQLite (Default):**
- No setup required
- Automatically creates fitfriendsclub.db

**PostgreSQL (Production):**
- Set DATABASE_URL environment variable
- Run `./install-postgresql.sh` if needed

## 🧪 Verification Steps

1. **Test Requirements:**
```bash
pip install -r backend/requirements.txt
python -c "from backend.app import app; print('✅ Success')"
```

2. **Run Full Verification:**
```bash
./verify-dependencies.sh
```

3. **Test Production Server:**
```bash
gunicorn --chdir backend app:app
```

## 📋 Troubleshooting

### Common Deployment Errors:

1. **"Package not found"**
   - Check requirements.txt syntax
   - Verify Python version compatibility

2. **"pg_config not found"**
   - Use `./install-postgresql.sh`
   - Or comment out psycopg2-binary in requirements.txt

3. **"Build failed"**
   - Use the fixed requirements.txt with pinned versions
   - Ensure runtime.txt specifies Python 3.8.19

4. **"Import errors"**
   - Check PYTHONPATH includes backend/
   - Verify all dependencies installed correctly

## 🎯 Production Checklist

- [ ] requirements.txt uses pinned versions ✅
- [ ] runtime.txt specifies Python version ✅  
- [ ] Environment variables configured
- [ ] Database connection tested
- [ ] Gunicorn production server working
- [ ] All dependencies verified

## 🔄 Update Dependencies

```bash
# Check for updates
pip list --outdated

# Update specific packages (test thoroughly)
pip install --upgrade package-name

# Update requirements.txt
pip freeze > backend/requirements.txt
```

---

Your FitFriendsClub backend is now deployment-ready! 🎉