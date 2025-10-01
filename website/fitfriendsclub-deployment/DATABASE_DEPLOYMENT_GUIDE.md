# Database Schema Deployment Guide for FitFriendsClubs

## Quick Start 🚀

**Option 1: Automated Script (Recommended)**
```bash
# Set your database URL
export DATABASE_URL="postgresql://user:password@host:port/database"

# Run deployment script
./deploy-database.sh
```

**Option 2: Node.js Script**
```bash
# Install dependencies
npm install

# Set environment variable and deploy
export DATABASE_URL="your-database-url"
npm run db:deploy
```

**Option 3: Python Script**
```bash
# Install dependencies
pip install psycopg2-binary

# Deploy
export DATABASE_URL="your-database-url"
python deploy-database.py
```

## Overview
This guide explains how to deploy the complete database schema for your FitFriendsClubs platform, including base tables, fitness clubs, virtual trails, and live streaming functionality.

## Prerequisites
- PostgreSQL database (Supabase, Neon, or self-hosted)
- Database connection credentials
- One of: `psql`, Node.js, or Python

## Schema Files
1. `fitness-clubs-schema.sql` - Core fitness clubs, equipment, and group sessions
2. `streaming-schema.sql` - Live video streaming and chat functionality

## Deployment Methods

### Method 1: Using Database Provider Dashboard (Recommended for beginners)

#### Supabase
1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Create a new query
4. Copy and paste the complete schema (see `complete-schema.sql`)
5. Click **Run** to execute

#### Neon
1. Go to your Neon console
2. Navigate to **SQL Editor**
3. Paste the schema content
4. Execute the queries

#### Other PostgreSQL providers
Most providers offer a SQL console or query interface where you can paste and execute the schema.

### Method 2: Using psql Command Line

```bash
# Connect to your database
psql "postgresql://username:password@host:port/database"

# Or if you have environment variables set
psql $DATABASE_URL

# Execute schema files
\i fitness-clubs-schema.sql
\i streaming-schema.sql

# Or execute all at once
\i complete-schema.sql
```

### Method 3: Using Node.js/JavaScript

```javascript
const { Client } = require('pg');
const fs = require('fs');

const client = new Client({
  connectionString: process.env.DATABASE_URL,
});

async function deploySchema() {
  await client.connect();
  
  const schema = fs.readFileSync('complete-schema.sql', 'utf8');
  await client.query(schema);
  
  console.log('Schema deployed successfully!');
  await client.end();
}

deploySchema().catch(console.error);
```

### Method 4: Using Python

```python
import psycopg2
import os

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cursor = conn.cursor()

with open('complete-schema.sql', 'r') as f:
    schema = f.read()
    
cursor.execute(schema)
conn.commit()
conn.close()

print("Schema deployed successfully!")
```

## Environment Variables

Make sure your Cloudflare Worker has these environment variables configured:

```toml
# In wrangler.toml
[vars]
DATABASE_API_URL = "https://your-db-host.com/api"
DATABASE_API_KEY = "your-api-key"
TURN_SERVER_SECRET = "your-turn-server-secret"
```

## Verification

After deployment, verify your tables exist:

```sql
-- List all tables
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Check table structure
\d users
\d fitness_clubs
\d streaming_sessions
```

## Expected Tables

After successful deployment, you should have these tables:
- `users` (base user accounts)
- `workouts` (individual workouts)
- `social_posts` (social media features)
- `fitness_clubs` (fitness clubs)
- `club_members` (club membership)
- `group_sessions` (group workout sessions)
- `group_session_participants` (session participants)
- `user_equipment` (connected fitness equipment)
- `equipment_workout_data` (workout metrics from equipment)
- `session_leaderboard` (group session rankings)
- `virtual_trails` (virtual running/cycling trails)
- `trail_sessions` (virtual trail workouts)
- `streaming_sessions` (live video streams)
- `stream_viewers` (stream viewership)
- `chat_messages` (live chat during streams)
- `stream_analytics` (streaming metrics)
- `notifications` (user notifications)
- `user_preferences` (streaming and notification preferences)

## Troubleshooting

### Common Issues

1. **Permission denied**: Ensure your database user has CREATE table permissions
2. **Table already exists**: Use `CREATE TABLE IF NOT EXISTS` or drop existing tables first
3. **Foreign key constraints**: Deploy tables in the correct order (users first, then dependent tables)
4. **Connection timeout**: For large schemas, increase connection timeout

### Rollback

If you need to remove the schema:

```sql
-- Drop tables in reverse order (due to foreign keys)
DROP TABLE IF EXISTS stream_analytics CASCADE;
DROP TABLE IF EXISTS chat_messages CASCADE;
DROP TABLE IF EXISTS stream_viewers CASCADE;
DROP TABLE IF EXISTS streaming_sessions CASCADE;
-- ... continue for all tables
```

## Next Steps

1. Deploy the schema using your preferred method
2. Update your Cloudflare Workers environment variables
3. Test API endpoints to ensure database connectivity
4. Configure your streaming infrastructure (RTMP server, WebSocket server)
5. Set up your domain DNS records for streaming endpoints

## Support

If you encounter issues:
1. Check your database logs
2. Verify connection credentials
3. Ensure your database supports PostgreSQL features (JSONB, UUID, etc.)
4. Test with a simple query first: `SELECT NOW();`