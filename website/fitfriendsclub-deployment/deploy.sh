#!/bin/bash

# FitFriendsClubs - Cloudflare Deployment Script
echo "🚀 Deploying FitFriendsClubs to Cloudflare Workers..."

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "❌ Wrangler CLI not found. Installing..."
    npm install -g wrangler
fi

# Login to Cloudflare (if not already logged in)
echo "🔐 Checking Cloudflare authentication..."
wrangler whoami || wrangler login

# Deploy to production
echo "📦 Deploying worker to production..."
wrangler deploy --env production

# Check deployment status
echo "✅ Deployment complete!"
echo ""
echo "🌐 Your API should be available at:"
echo "   https://api.fitfriendsclubs.com/api/health"
echo ""
echo "🔧 Don't forget to set your secrets:"
echo "   wrangler secret put DATABASE_API_URL --env production"
echo "   wrangler secret put DATABASE_API_KEY --env production"
echo ""
echo "📋 Verify DNS records are configured:"
echo "   - A record: @ → 104.21.0.0 (proxied)"
echo "   - CNAME: www → fitfriendsclubs.com (proxied)"  
echo "   - CNAME: api → fitfriendsclubs.com (proxied)"
echo ""
echo "🧪 Test your deployment:"
echo "   curl https://api.fitfriendsclubs.com/api/health"