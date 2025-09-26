#!/bin/bash

# 🚀 FitFriendsClub Website Deployment Package
# This script packages your website files for deployment

echo "🏆 Packaging FitFriendsClub Website for Deployment..."
echo ""

# Create deployment directory
DEPLOY_DIR="fitfriendsclub-deployment"
mkdir -p "$DEPLOY_DIR"

# Copy all website files
echo "📁 Copying website files..."
cp index.html "$DEPLOY_DIR/"
cp styles.css "$DEPLOY_DIR/"
cp script.js "$DEPLOY_DIR/"
cp favicon.ico "$DEPLOY_DIR/" 2>/dev/null || echo "⚠️  No favicon found - consider adding one"

echo ""
echo "✅ Deployment package created in: $DEPLOY_DIR/"
echo ""
echo "🚀 READY TO DEPLOY!"
echo ""
echo "Next Steps:"
echo "1. Go to https://netlify.com"
echo "2. Create a FREE account"  
echo "3. Drag the '$DEPLOY_DIR' folder to deploy"
echo "4. Add fitfriendsclub.com as custom domain"
echo "5. Update DNS settings as shown in DEPLOY.md"
echo ""
echo "🌟 Your FitFriendsClub website will be live in minutes!"
echo ""

# List files in deployment package
echo "📦 Deployment Package Contents:"
ls -la "$DEPLOY_DIR"/
echo ""
echo "🎯 Total package size:"
du -sh "$DEPLOY_DIR"

echo ""
echo "💡 Pro Tip: The deployment guide (DEPLOY.md) has complete"
echo "   step-by-step instructions for multiple hosting options!"
echo ""
echo "🏆 Good luck with your FitFriendsClub launch! 💪"