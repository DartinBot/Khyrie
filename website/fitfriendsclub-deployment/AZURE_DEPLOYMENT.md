# 🚀 Azure App Service Deployment Guide for FitFriendsClub

## 📋 Prerequisites
1. Azure account with active subscription
2. Azure CLI installed: `az login`
3. Resource group created in Azure

## 🔧 Azure App Service Setup

### Step 1: Create Azure App Service
```bash
# Login to Azure
az login

# Create resource group (if needed)
az group create --name fitfriendsclub-rg --location "East US"

# Create App Service Plan
az appservice plan create \
  --name fitfriendsclub-plan \
  --resource-group fitfriendsclub-rg \
  --sku B1 \
  --is-linux

# Create Web App with Python runtime
az webapp create \
  --name fitfriendsclub-app \
  --resource-group fitfriendsclub-rg \
  --plan fitfriendsclub-plan \
  --runtime "PYTHON|3.9"
```

### Step 2: Configure App Settings
```bash
# Set environment variables for PostgreSQL binary enforcement
az webapp config appsettings set \
  --name fitfriendsclub-app \
  --resource-group fitfriendsclub-rg \
  --settings \
    PIP_NO_CACHE_DIR=1 \
    PIP_PREFER_BINARY=1 \
    PIP_ONLY_BINARY="psycopg2,psycopg2-binary" \
    PYTHONDONTWRITEBYTECODE=1 \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true

# Set startup command
az webapp config set \
  --name fitfriendsclub-app \
  --resource-group fitfriendsclub-rg \
  --startup-file "cd backend && gunicorn app:app --bind 0.0.0.0:8000"
```

### Step 3: Deploy via Git
```bash
# Configure local Git deployment
az webapp deployment source config-local-git \
  --name fitfriendsclub-app \
  --resource-group fitfriendsclub-rg

# Get deployment credentials
az webapp deployment list-publishing-credentials \
  --name fitfriendsclub-app \
  --resource-group fitfriendsclub-rg

# Add Azure remote (replace with your actual URL)
git remote add azure https://fitfriendsclub-app.scm.azurewebsites.net/fitfriendsclub-app.git

# Deploy to Azure
git push azure main
```

## 🎯 Alternative: Deploy via Azure CLI
```bash
# Deploy from local directory
az webapp up \
  --name fitfriendsclub-app \
  --resource-group fitfriendsclub-rg \
  --runtime "PYTHON:3.9" \
  --sku B1
```

## 📦 PostgreSQL Configuration

### Option 1: Azure Database for PostgreSQL
```bash
# Create Azure PostgreSQL server
az postgres server create \
  --name fitfriendsclub-postgres \
  --resource-group fitfriendsclub-rg \
  --location "East US" \
  --admin-user fitadmin \
  --admin-password YourSecurePassword123! \
  --sku-name B_Gen5_1

# Create database
az postgres db create \
  --name fitfriendsclub_db \
  --server-name fitfriendsclub-postgres \
  --resource-group fitfriendsclub-rg

# Set connection string
az webapp config connection-string set \
  --name fitfriendsclub-app \
  --resource-group fitfriendsclub-rg \
  --connection-string-type PostgreSQL \
  --settings DATABASE_URL="postgresql://fitadmin:YourSecurePassword123!@fitfriendsclub-postgres.postgres.database.azure.com:5432/fitfriendsclub_db"
```

### Option 2: Use SQLite (Default)
No additional configuration needed - your app will use SQLite automatically.

## 🚨 Troubleshooting pg_config Errors

### Built-in Protection
Your deployment includes automatic pg_config error prevention:
- ✅ Uses `requirements-flexible.txt` with version range
- ✅ Forces binary installation via environment variables
- ✅ Custom deployment script with PostgreSQL enforcement

### If Issues Persist
1. **Check deployment logs:**
   ```bash
   az webapp log tail --name fitfriendsclub-app --resource-group fitfriendsclub-rg
   ```

2. **Restart app:**
   ```bash
   az webapp restart --name fitfriendsclub-app --resource-group fitfriendsclub-rg
   ```

3. **Use specific psycopg2 version:**
   - Update to use `requirements-binary-only.txt` with fixed version

## 🌐 Access Your App
After deployment, your app will be available at:
`https://fitfriendsclub-app.azurewebsites.net`

## 📁 Files Created for Azure Deployment
- ✅ `deploy.cmd` - Custom deployment script with pg_config protection
- ✅ `.deployment` - Azure deployment configuration
- ✅ `azure-app-service.toml` - App Service settings
- ✅ All requirements files optimized for binary installation

## 🎉 Expected Result
- ✅ No pg_config errors during deployment
- ✅ PostgreSQL support working correctly
- ✅ Flask app running on Azure App Service
- ✅ Automatic scaling and management via Azure