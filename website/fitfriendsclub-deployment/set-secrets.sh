#!/bin/bash

# Quick Cloudflare Secrets Setup for FitFriendsClubs
# Run this script to set all your secrets at once

echo "🔑 Setting up Cloudflare Worker Secrets"
echo "======================================"
echo ""

# Prompt for values
echo "Enter your Supabase details:"
echo ""

read -p "Database URL (postgresql://...): " DATABASE_URL
read -s -p "Service Role Key (eyJ...): " SUPABASE_SERVICE_KEY
echo ""
read -s -p "TURN Server Secret (optional, press Enter to skip): " TURN_SERVER_SECRET
echo ""

echo ""
echo "Setting secrets for production environment..."

# Set the secrets
echo "$DATABASE_URL" | wrangler secret put DATABASE_URL --env production
echo "$SUPABASE_SERVICE_KEY" | wrangler secret put SUPABASE_SERVICE_KEY --env production

if [ -n "$TURN_SERVER_SECRET" ]; then
    echo "$TURN_SERVER_SECRET" | wrangler secret put TURN_SERVER_SECRET --env production
fi

echo ""
echo "✅ Secrets configured successfully!"
echo ""
echo "Next steps:"
echo "1. Update SUPABASE_URL and SUPABASE_ANON_KEY in wrangler.toml"
echo "2. Deploy: wrangler publish --env production"
echo "3. Test: curl https://api.fitfriendsclubs.com/api/health"