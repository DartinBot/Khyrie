#!/bin/bash

# Supabase Deployment Script for FitFriendsClubs
# This script helps you deploy and configure Supabase with Cloudflare Workers

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🏋️  FitFriendsClubs Supabase + Cloudflare Setup${NC}"
echo -e "${BLUE}==============================================${NC}"
echo ""

# Check if required files exist
if [ ! -f "complete-schema.sql" ]; then
    echo -e "${RED}❌ complete-schema.sql not found${NC}"
    exit 1
fi

if [ ! -f "wrangler.toml" ]; then
    echo -e "${RED}❌ wrangler.toml not found${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Setup Checklist:${NC}"
echo "  1. 🗄️  Deploy database schema to Supabase"
echo "  2. 🔑 Configure Cloudflare Worker secrets"
echo "  3. 🌐 Test API connection"
echo "  4. 🚀 Deploy to production"
echo ""

# Step 1: Database Schema Deployment
echo -e "${BLUE}Step 1: Database Schema Deployment${NC}"
echo ""
echo "Choose your deployment method:"
echo "  a) Supabase Dashboard (SQL Editor)"
echo "  b) Command line (psql)"
echo "  c) Skip (already deployed)"
echo ""

read -p "Select option (a/b/c): " -n 1 -r DEPLOY_CHOICE
echo ""

case $DEPLOY_CHOICE in
    [Aa]* )
        echo ""
        echo -e "${YELLOW}📋 Manual Supabase Dashboard Deployment:${NC}"
        echo "  1. Go to your Supabase project dashboard"
        echo "  2. Navigate to SQL Editor"
        echo "  3. Copy contents of complete-schema.sql"
        echo "  4. Paste into SQL Editor"
        echo "  5. Click 'Run' to execute"
        echo ""
        read -p "Press Enter when schema is deployed..."
        ;;
    [Bb]* )
        if [ -z "$DATABASE_URL" ]; then
            echo ""
            echo -e "${YELLOW}Enter your Supabase DATABASE_URL:${NC}"
            echo "Format: postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres"
            read -p "DATABASE_URL: " DATABASE_URL
            export DATABASE_URL
        fi
        
        echo ""
        echo -e "${YELLOW}🚀 Deploying schema via command line...${NC}"
        
        if command -v psql &> /dev/null; then
            psql "$DATABASE_URL" -f complete-schema.sql
            echo -e "${GREEN}✅ Schema deployed successfully${NC}"
        else
            echo -e "${YELLOW}psql not found. Using Node.js deployment script...${NC}"
            node deploy-database.js
        fi
        ;;
    [Cc]* )
        echo -e "${GREEN}✅ Skipping schema deployment${NC}"
        ;;
    * )
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo ""

# Step 2: Supabase Configuration
echo -e "${BLUE}Step 2: Supabase Configuration${NC}"
echo ""
echo "We need your Supabase project details:"
echo ""

# Get Supabase URL
if [ -z "$SUPABASE_URL" ]; then
    read -p "Supabase Project URL (https://[project].supabase.co): " SUPABASE_URL
fi

# Get anon key
if [ -z "$SUPABASE_ANON_KEY" ]; then
    read -p "Supabase anon public key (eyJ...): " SUPABASE_ANON_KEY
fi

# Get service role key
if [ -z "$SUPABASE_SERVICE_KEY" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Service role key is sensitive - it will be stored as a Cloudflare secret${NC}"
    read -s -p "Supabase service_role secret key (eyJ...): " SUPABASE_SERVICE_KEY
    echo ""
fi

# Get database URL
if [ -z "$DATABASE_URL" ]; then
    echo ""
    read -p "Database URL (postgresql://...): " DATABASE_URL
fi

echo ""

# Step 3: Update wrangler.toml
echo -e "${YELLOW}📝 Updating wrangler.toml...${NC}"

# Create backup
cp wrangler.toml wrangler.toml.backup

# Update public variables in wrangler.toml
sed -i.tmp "s|SUPABASE_URL = \".*\"|SUPABASE_URL = \"$SUPABASE_URL\"|g" wrangler.toml
sed -i.tmp "s|SUPABASE_ANON_KEY = \".*\"|SUPABASE_ANON_KEY = \"$SUPABASE_ANON_KEY\"|g" wrangler.toml

# Clean up temp file
rm -f wrangler.toml.tmp

echo -e "${GREEN}✅ wrangler.toml updated${NC}"
echo ""

# Step 4: Set Cloudflare Secrets
echo -e "${BLUE}Step 3: Setting Cloudflare Worker Secrets${NC}"
echo ""

echo -e "${YELLOW}Setting secrets for production environment...${NC}"

# Set SUPABASE_SERVICE_KEY
echo "$SUPABASE_SERVICE_KEY" | wrangler secret put SUPABASE_SERVICE_KEY --env production

# Set DATABASE_URL
echo "$DATABASE_URL" | wrangler secret put DATABASE_URL --env production

# Set TURN_SERVER_SECRET (prompt if not provided)
if [ -z "$TURN_SERVER_SECRET" ]; then
    echo ""
    echo "TURN server secret for WebRTC streaming (optional, press Enter to skip):"
    read -s -p "TURN_SERVER_SECRET: " TURN_SERVER_SECRET
    echo ""
fi

if [ -n "$TURN_SERVER_SECRET" ]; then
    echo "$TURN_SERVER_SECRET" | wrangler secret put TURN_SERVER_SECRET --env production
fi

echo -e "${GREEN}✅ Secrets configured${NC}"
echo ""

# Step 5: Test Connection
echo -e "${BLUE}Step 4: Testing Connection${NC}"
echo ""

echo -e "${YELLOW}🧪 Starting development server for testing...${NC}"
echo ""

# Start dev server in background
wrangler dev --env production &
DEV_PID=$!

# Wait for server to start
sleep 5

# Test health endpoint
echo "Testing API health endpoint..."
if curl -s http://localhost:8787/api/health > /dev/null; then
    echo -e "${GREEN}✅ Health endpoint working${NC}"
else
    echo -e "${RED}❌ Health endpoint failed${NC}"
fi

# Kill dev server
kill $DEV_PID 2>/dev/null || true

echo ""

# Step 6: Deploy to Production
echo -e "${BLUE}Step 5: Deploy to Production${NC}"
echo ""

read -p "Deploy to production now? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🚀 Deploying to Cloudflare Workers...${NC}"
    
    wrangler publish --env production
    
    echo ""
    echo -e "${GREEN}✅ Deployment complete!${NC}"
    echo ""
    
    # Test production endpoint
    echo -e "${YELLOW}🧪 Testing production endpoint...${NC}"
    
    if curl -s https://api.fitfriendsclubs.com/api/health > /dev/null; then
        echo -e "${GREEN}✅ Production API is live!${NC}"
    else
        echo -e "${YELLOW}⚠️  Production endpoint not responding yet (DNS may still be propagating)${NC}"
    fi
else
    echo -e "${YELLOW}Skipping production deployment${NC}"
    echo ""
    echo "To deploy later, run:"
    echo "  wrangler publish --env production"
fi

echo ""
echo -e "${GREEN}🎉 Supabase + Cloudflare Integration Complete!${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "  1. 🌐 Configure your custom domain DNS records"
echo "  2. 🔒 Enable Row Level Security in Supabase"
echo "  3. 📱 Set up Supabase Storage for images"
echo "  4. 🔴 Configure live streaming infrastructure"
echo "  5. 📊 Set up monitoring and analytics"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo "  Test locally:     wrangler dev"
echo "  View logs:        wrangler tail --env production"
echo "  Update secrets:   wrangler secret put SECRET_NAME --env production"
echo ""
echo -e "${GREEN}Your FitFriendsClubs platform is ready! 🏋️‍♀️${NC}"