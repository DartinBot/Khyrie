#!/bin/bash

# 🚀 Deploy FitFriendsClub to Cloudflare Workers + Wix Frontend
# This script deploys your Flask API to Cloudflare Workers

echo "🌐 Deploying FitFriendsClub to Cloudflare Workers..."

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "📦 Installing Wrangler CLI..."
    npm install -g wrangler
fi

# Login to Cloudflare (if not already logged in)
echo "🔐 Checking Cloudflare authentication..."
if ! wrangler whoami &> /dev/null; then
    echo "Please login to Cloudflare:"
    wrangler login
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Set up secrets (you'll need to add these manually)
echo "🔑 Setting up environment secrets..."
echo "You need to add these secrets manually:"
echo "  wrangler secret put DATABASE_URL"
echo "  wrangler secret put DATABASE_API_KEY" 
echo "  wrangler secret put JWT_SECRET"

# Deploy to Cloudflare Workers
echo "🚀 Deploying to Cloudflare Workers..."
wrangler publish

# Get deployment URL
WORKER_URL=$(wrangler subdomain 2>/dev/null | grep -o "https://.*workers.dev" || echo "https://fitfriendsclub-api.your-subdomain.workers.dev")

echo ""
echo "✅ Deployment Complete!"
echo "🌐 API URL: $WORKER_URL"
echo ""
echo "📋 Next Steps for Wix Integration:"
echo "1. Copy your API URL: $WORKER_URL"
echo "2. In Wix Code, use this URL for API calls"
echo "3. Update CORS settings if needed"
echo ""
echo "🧪 Test your API:"
echo "curl $WORKER_URL/api/health"
echo ""
echo "📚 Documentation: https://developers.cloudflare.com/workers/"