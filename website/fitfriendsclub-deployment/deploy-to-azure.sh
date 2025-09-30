#!/bin/bash
# Azure deployment helper script
# Simplifies Azure App Service deployment with PostgreSQL protection

echo "🚀 Azure App Service Deployment Helper"
echo "======================================"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found. Please install it first:"
    echo "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

echo "✅ Azure CLI found"

# Check if logged in
if ! az account show &> /dev/null; then
    echo "🔐 Please login to Azure first:"
    az login
fi

echo "✅ Azure authentication verified"

# Configuration
APP_NAME="fitfriendsclub-app"
RESOURCE_GROUP="fitfriendsclub-rg" 
LOCATION="East US"
PLAN_NAME="fitfriendsclub-plan"

echo ""
echo "📋 Deployment Configuration:"
echo "   App Name: $APP_NAME"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   Location: $LOCATION"
echo ""

read -p "🤔 Continue with deployment? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo "🏗️  Creating Azure resources..."

# Create resource group
echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location "$LOCATION" --output table

# Create app service plan
echo "Creating App Service plan..."
az appservice plan create \
    --name $PLAN_NAME \
    --resource-group $RESOURCE_GROUP \
    --sku B1 \
    --is-linux \
    --output table

# Create web app
echo "Creating Web App..."
az webapp create \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --plan $PLAN_NAME \
    --runtime "PYTHON|3.9" \
    --output table

# Configure app settings for PostgreSQL binary enforcement
echo "Configuring app settings for pg_config protection..."
az webapp config appsettings set \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings \
        PIP_NO_CACHE_DIR=1 \
        PIP_PREFER_BINARY=1 \
        PIP_ONLY_BINARY="psycopg2,psycopg2-binary" \
        PYTHONDONTWRITEBYTECODE=1 \
        SCM_DO_BUILD_DURING_DEPLOYMENT=true \
    --output table

# Set startup command
echo "Setting startup command..."
az webapp config set \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --startup-file "./startup.sh" \
    --output table

# Configure Git deployment
echo "Setting up Git deployment..."
az webapp deployment source config-local-git \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --output table

# Get Git URL
GIT_URL=$(az webapp deployment source config-local-git \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query url -o tsv)

echo ""
echo "🎉 Azure resources created successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Add Azure as Git remote:"
echo "   git remote add azure $GIT_URL"
echo ""
echo "2. Deploy your application:"
echo "   git push azure main"
echo ""
echo "3. Your app will be available at:"
echo "   https://$APP_NAME.azurewebsites.net"
echo ""
echo "🛡️  PostgreSQL pg_config protection is enabled automatically!"