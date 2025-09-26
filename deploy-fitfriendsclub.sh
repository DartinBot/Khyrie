#!/bin/bash

# FitFriendsClub Deployment Script
# Automated deployment to fitfriendsclub.com via Netlify

set -e  # Exit on any error

echo "🚀 FitFriendsClub Deployment Script"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SITE_NAME="fitfriendsclub"
DOMAIN="fitfriendsclub.com"
BUILD_DIR="website"
REPO_URL="https://github.com/DartinBot/Khyrie"

echo -e "${BLUE}📋 Deployment Configuration${NC}"
echo "Site Name: $SITE_NAME"
echo "Domain: $DOMAIN"
echo "Build Directory: $BUILD_DIR"
echo "Repository: $REPO_URL"
echo ""

# Check if we're in the right directory
if [ ! -f "website/index.html" ]; then
    echo -e "${RED}❌ Error: website/index.html not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo -e "${GREEN}✅ Project files found${NC}"

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo -e "${YELLOW}⚠️  Netlify CLI not found. Installing...${NC}"
    npm install -g netlify-cli
fi

echo -e "${GREEN}✅ Netlify CLI ready${NC}"

# Login to Netlify (if not already logged in)
echo -e "${BLUE}🔐 Checking Netlify authentication...${NC}"
if ! netlify status &> /dev/null; then
    echo -e "${YELLOW}Please login to Netlify:${NC}"
    netlify login
fi

echo -e "${GREEN}✅ Netlify authentication confirmed${NC}"

# Check if site exists
echo -e "${BLUE}🌐 Checking site status...${NC}"
if netlify sites:list | grep -q "$SITE_NAME"; then
    echo -e "${GREEN}✅ Site '$SITE_NAME' found${NC}"
    SITE_ID=$(netlify sites:list --json | jq -r ".[] | select(.name==\"$SITE_NAME\") | .id")
    echo "Site ID: $SITE_ID"
else
    echo -e "${YELLOW}⚠️  Site '$SITE_NAME' not found. Creating new site...${NC}"
    netlify sites:create --name "$SITE_NAME"
    SITE_ID=$(netlify sites:list --json | jq -r ".[] | select(.name==\"$SITE_NAME\") | .id")
    echo -e "${GREEN}✅ Site created with ID: $SITE_ID${NC}"
fi

# Deploy to Netlify
echo -e "${BLUE}📦 Deploying to Netlify...${NC}"
netlify deploy --dir="$BUILD_DIR" --site="$SITE_ID"

echo -e "${GREEN}✅ Draft deployment successful${NC}"
echo ""

# Ask for production deployment confirmation
echo -e "${YELLOW}🤔 Ready to deploy to production?${NC}"
echo "This will make the site live at $DOMAIN"
read -p "Deploy to production? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}🚀 Deploying to production...${NC}"
    netlify deploy --prod --dir="$BUILD_DIR" --site="$SITE_ID"
    
    echo ""
    echo -e "${GREEN}🎉 DEPLOYMENT SUCCESSFUL!${NC}"
    echo "================================"
    echo -e "🌐 Live Site: ${GREEN}https://$DOMAIN${NC}"
    echo -e "📊 Admin Panel: ${BLUE}https://app.netlify.com/sites/$SITE_NAME${NC}"
    echo ""
    
    # Display next steps
    echo -e "${BLUE}📋 Next Steps:${NC}"
    echo "1. Configure custom domain (if not done already)"
    echo "2. Set up email forwarding: hello@fitfriendsclub.com"
    echo "3. Configure form notifications"
    echo "4. Set up analytics (Google Analytics recommended)"
    echo "5. Test all functionality on live site"
    echo ""
    
    # Test the deployment
    echo -e "${BLUE}🧪 Testing deployment...${NC}"
    if curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN" | grep -q "200"; then
        echo -e "${GREEN}✅ Site is responding correctly${NC}"
    else
        echo -e "${YELLOW}⚠️  Site may still be propagating. Check again in a few minutes.${NC}"
    fi
    
else
    echo -e "${YELLOW}⏸️  Production deployment skipped${NC}"
    echo "You can deploy to production later with:"
    echo "netlify deploy --prod --dir=$BUILD_DIR --site=$SITE_ID"
fi

echo ""
echo -e "${GREEN}✨ Deployment script completed!${NC}"