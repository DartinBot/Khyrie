#!/bin/bash

# FitFriendsClubs Database Deployment Script
# This script deploys the complete database schema to your PostgreSQL database

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🏋️  FitFriendsClubs Database Deployment Script${NC}"
echo -e "${BLUE}===============================================${NC}"
echo ""

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}❌ ERROR: DATABASE_URL environment variable is not set${NC}"
    echo ""
    echo "Please set your DATABASE_URL. Examples:"
    echo ""
    echo "  # Supabase"
    echo "  export DATABASE_URL='postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres'"
    echo ""
    echo "  # Neon"
    echo "  export DATABASE_URL='postgresql://[user]:[password]@[endpoint]/[dbname]'"
    echo ""
    echo "  # Local PostgreSQL"
    echo "  export DATABASE_URL='postgresql://username:password@localhost:5432/fitfriendsclubs'"
    echo ""
    echo "Then run this script again:"
    echo "  ./deploy-database.sh"
    exit 1
fi

echo -e "${YELLOW}📊 Database Connection:${NC}"
echo "  URL: $(echo $DATABASE_URL | sed 's/:[^:]*@/:****@/')"  # Hide password
echo ""

# Test database connection
echo -e "${YELLOW}🔌 Testing database connection...${NC}"
if ! psql "$DATABASE_URL" -c "SELECT NOW() as current_time;" > /dev/null 2>&1; then
    echo -e "${RED}❌ ERROR: Cannot connect to database${NC}"
    echo ""
    echo "Please check:"
    echo "  1. DATABASE_URL is correct"
    echo "  2. Database server is running"
    echo "  3. Network connectivity"
    echo "  4. Username/password are correct"
    echo ""
    echo "Test connection manually:"
    echo "  psql \"\$DATABASE_URL\" -c \"SELECT NOW();\""
    exit 1
fi

echo -e "${GREEN}✅ Database connection successful${NC}"
echo ""

# Check if psql is available
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ ERROR: psql command not found${NC}"
    echo ""
    echo "Please install PostgreSQL client:"
    echo ""
    echo "  # macOS with Homebrew"
    echo "  brew install postgresql"
    echo ""
    echo "  # Ubuntu/Debian"
    echo "  sudo apt-get install postgresql-client"
    echo ""
    echo "  # CentOS/RHEL"
    echo "  sudo yum install postgresql"
    exit 1
fi

# Check if schema file exists
SCHEMA_FILE="complete-schema.sql"
if [ ! -f "$SCHEMA_FILE" ]; then
    echo -e "${RED}❌ ERROR: Schema file '$SCHEMA_FILE' not found${NC}"
    echo ""
    echo "Make sure you're running this script from the correct directory."
    echo "Expected files:"
    echo "  - complete-schema.sql"
    echo "  - deploy-database.sh (this script)"
    exit 1
fi

echo -e "${YELLOW}📁 Schema file found: $SCHEMA_FILE${NC}"
echo ""

# Show what will be deployed
echo -e "${YELLOW}📋 Schema Overview:${NC}"
echo "  This will create the following table groups:"
echo "  • Core Tables: users, workouts, social_posts"
echo "  • Fitness Clubs: fitness_clubs, club_members, group_sessions"
echo "  • Equipment: user_equipment, equipment_workout_data"
echo "  • Virtual Trails: virtual_trails, trail_sessions, trail_achievements"
echo "  • Live Streaming: streaming_sessions, stream_viewers, chat_messages"
echo "  • Notifications: notifications, user_preferences"
echo "  • Sample Data: Demo clubs, trails, and test user"
echo ""

# Confirmation prompt
echo -e "${YELLOW}⚠️  IMPORTANT: This will create/modify tables in your database${NC}"
read -p "Do you want to continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}❌ Deployment cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}🚀 Starting database deployment...${NC}"
echo ""

# Deploy schema
echo -e "${YELLOW}📊 Executing SQL schema...${NC}"

# Run the schema with verbose output
if psql "$DATABASE_URL" -f "$SCHEMA_FILE" -v ON_ERROR_STOP=1; then
    echo ""
    echo -e "${GREEN}✅ Database schema deployed successfully!${NC}"
    echo ""
    
    # Verify deployment by counting tables
    echo -e "${YELLOW}🔍 Verifying deployment...${NC}"
    
    TABLE_COUNT=$(psql "$DATABASE_URL" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
    
    echo "  Tables created: $TABLE_COUNT"
    
    # List all tables
    echo ""
    echo -e "${YELLOW}📋 Created Tables:${NC}"
    psql "$DATABASE_URL" -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE' ORDER BY table_name;"
    
    echo ""
    echo -e "${GREEN}🎉 Deployment Complete!${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "  1. 📝 Update Cloudflare Workers environment variables:"
    echo "     - DATABASE_API_URL: Your database API endpoint"
    echo "     - DATABASE_API_KEY: Your database API key"
    echo "     - TURN_SERVER_SECRET: WebRTC TURN server secret"
    echo ""
    echo "  2. 🌐 Configure DNS records (see DNS_RECORDS.md)"
    echo ""
    echo "  3. 🧪 Test API endpoints:"
    echo "     curl https://api.fitfriendsclubs.com/api/health"
    echo ""
    echo "  4. 📱 Set up streaming infrastructure:"
    echo "     - RTMP server for live video"
    echo "     - WebSocket server for real-time chat"
    echo "     - TURN/STUN servers for WebRTC"
    echo ""
    echo -e "${GREEN}Your FitFriendsClubs platform is ready to deploy! 🏋️‍♀️${NC}"
    
else
    echo ""
    echo -e "${RED}❌ Schema deployment failed${NC}"
    echo ""
    echo "Common issues:"
    echo "  • Permission denied: Your user needs CREATE table permissions"
    echo "  • Connection timeout: Database might be slow or overloaded"
    echo "  • Syntax error: Check PostgreSQL version compatibility"
    echo ""
    echo "To debug:"
    echo "  1. Test basic connection: psql \"\$DATABASE_URL\" -c \"SELECT NOW();\""
    echo "  2. Check permissions: psql \"\$DATABASE_URL\" -c \"SELECT current_user;\""
    echo "  3. Try manual deployment: psql \"\$DATABASE_URL\" -f complete-schema.sql"
    exit 1
fi