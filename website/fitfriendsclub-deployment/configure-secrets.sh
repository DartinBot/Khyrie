#!/bin/bash

# Cloudflare Workers Secrets Configuration Script
# Run this script to set all required secrets for FitFriendsClubs

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔑 Cloudflare Workers Secrets Configuration${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "❌ Wrangler CLI not found. Install it with:"
    echo "   npm install -g wrangler"
    exit 1
fi

# Choose environment
echo "Select environment:"
echo "  1) Production"
echo "  2) Development"
echo "  3) Both"
echo ""

read -p "Choose (1/2/3): " -n 1 -r ENV_CHOICE
echo ""

case $ENV_CHOICE in
    1) ENVIRONMENTS=("production") ;;
    2) ENVIRONMENTS=("development") ;;
    3) ENVIRONMENTS=("production" "development") ;;
    *) echo "Invalid choice"; exit 1 ;;
esac

# Collect secret values
echo ""
echo -e "${YELLOW}Enter your secret values:${NC}"
echo ""

# Supabase Service Role Key
echo "1. Supabase Service Role Key (starts with eyJ...):"
read -s -p "   SUPABASE_SERVICE_KEY: " SUPABASE_SERVICE_KEY
echo ""

# Database URL
echo ""
echo "2. Database URL (postgresql://...):"
read -s -p "   DATABASE_URL: " DATABASE_URL
echo ""

# TURN Server Secret (optional)
echo ""
echo "3. TURN Server Secret for WebRTC (optional, press Enter to skip):"
read -s -p "   TURN_SERVER_SECRET: " TURN_SERVER_SECRET
echo ""

# JWT Secret (optional)
echo ""
echo "4. JWT Secret for authentication (optional, press Enter to skip):"
read -s -p "   JWT_SECRET: " JWT_SECRET
echo ""

# Set secrets for each environment
for ENV in "${ENVIRONMENTS[@]}"; do
    echo ""
    echo -e "${YELLOW}Setting secrets for $ENV environment...${NC}"
    
    # Required secrets
    echo "$SUPABASE_SERVICE_KEY" | wrangler secret put SUPABASE_SERVICE_KEY --env $ENV
    echo "$DATABASE_URL" | wrangler secret put DATABASE_URL --env $ENV
    
    # Optional secrets
    if [ -n "$TURN_SERVER_SECRET" ]; then
        echo "$TURN_SERVER_SECRET" | wrangler secret put TURN_SERVER_SECRET --env $ENV
    fi
    
    if [ -n "$JWT_SECRET" ]; then
        echo "$JWT_SECRET" | wrangler secret put JWT_SECRET --env $ENV
    fi
    
    echo -e "${GREEN}✅ Secrets set for $ENV environment${NC}"
done

echo ""
echo -e "${GREEN}🎉 All secrets configured successfully!${NC}"
echo ""
echo -e "${BLUE}Verify your secrets:${NC}"
for ENV in "${ENVIRONMENTS[@]}"; do
    echo "  wrangler secret list --env $ENV"
done

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Deploy your worker: wrangler publish --env production"
echo "  2. Test your API: curl https://api.fitfriendsclubs.com/api/health"