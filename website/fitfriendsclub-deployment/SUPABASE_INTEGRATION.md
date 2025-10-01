# Supabase + Cloudflare Workers Integration Guide

## Overview
This guide shows you how to connect your FitFriendsClubs Cloudflare Worker to Supabase for database operations.

## Step 1: Deploy Database Schema to Supabase

### Option A: Using Supabase Dashboard
1. Go to your **Supabase project dashboard**
2. Navigate to **SQL Editor**
3. Copy the contents of `complete-schema.sql`
4. Paste into the SQL Editor
5. Click **Run** to execute the schema

### Option B: Using Command Line
```bash
# Set your Supabase database URL
export DATABASE_URL="postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres"

# Deploy schema using our script
./deploy-database.sh
```

## Step 2: Get Supabase Connection Details

1. **Go to Supabase Dashboard** → Settings → Database
2. **Copy these values:**
   ```
   Host: db.[project].supabase.co
   Database: postgres
   Port: 5432
   User: postgres
   Password: [your-password]
   ```

3. **Go to Settings → API**
4. **Copy these values:**
   ```
   Project URL: https://[project].supabase.co
   anon public key: eyJ...
   service_role secret: eyJ...
   ```

## Step 3: Configure Cloudflare Worker Secrets

Set your Supabase credentials as Cloudflare Worker secrets:

```bash
# Set Supabase service role key (for server-side operations)
wrangler secret put SUPABASE_SERVICE_KEY --env production

# Set database URL (for direct PostgreSQL if needed)
wrangler secret put DATABASE_URL --env production

# Set streaming server secret
wrangler secret put TURN_SERVER_SECRET --env production
```

**Example values:**
```bash
# Supabase Service Role Key (secret - do not expose in client)
wrangler secret put SUPABASE_SERVICE_KEY
# Enter: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Database URL (direct PostgreSQL connection)
wrangler secret put DATABASE_URL
# Enter: postgresql://postgres:password@db.project.supabase.co:5432/postgres

# TURN server secret for WebRTC streaming
wrangler secret put TURN_SERVER_SECRET
# Enter: your-turn-server-secret-key
```

## Step 4: Update Wrangler.toml (Public Variables)

Update your `wrangler.toml` with public Supabase configuration:

```toml
[env.production.vars]
ENVIRONMENT = "production"
API_VERSION = "1.0"
# Supabase public configuration
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Step 5: Database Connection Methods

Your Cloudflare Worker now supports multiple connection methods:

### Method 1: Supabase REST API (Recommended)
- Uses Supabase's REST endpoints
- Better for simple CRUD operations
- Automatic connection pooling
- Built-in security features

### Method 2: Direct PostgreSQL
- Uses direct database connection
- Better for complex SQL queries
- Requires connection string
- More control over queries

## Step 6: Test Your Connection

### Test API Health
```bash
curl https://api.fitfriendsclubs.com/api/health
```

### Test Database Connection
```bash
# Test user registration
curl -X POST https://api.fitfriendsclubs.com/api/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### Test Fitness Clubs
```bash
# Get fitness clubs
curl https://api.fitfriendsclubs.com/api/clubs
```

## Step 7: Supabase-Specific Features

### Row Level Security (RLS)
Enable RLS for better security:

```sql
-- Enable RLS on tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE fitness_clubs ENABLE ROW LEVEL SECURITY;
ALTER TABLE group_sessions ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own data" ON users
  FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update own profile" ON users
  FOR UPDATE USING (auth.uid()::text = id::text);
```

### Real-time Subscriptions
Enable real-time for live features:

```sql
-- Enable real-time for chat messages
ALTER PUBLICATION supabase_realtime ADD TABLE chat_messages;
ALTER PUBLICATION supabase_realtime ADD TABLE stream_viewers;
ALTER PUBLICATION supabase_realtime ADD TABLE notifications;
```

### Storage for Images
Configure Supabase Storage:

1. Go to **Storage** in Supabase Dashboard
2. Create bucket: `fitness-images`
3. Set up storage policies
4. Update your Worker to use Supabase Storage instead of R2

## Step 8: Environment-Specific Configuration

### Development Environment
```bash
# Set development secrets
wrangler secret put SUPABASE_SERVICE_KEY --env development
wrangler secret put DATABASE_URL --env development
```

### Production Environment
```bash
# Set production secrets
wrangler secret put SUPABASE_SERVICE_KEY --env production
wrangler secret put DATABASE_URL --env production
```

## Troubleshooting

### Common Issues

1. **Connection Failed**: Check DATABASE_URL format
2. **Permission Denied**: Verify SUPABASE_SERVICE_KEY
3. **CORS Errors**: Update CORS settings in Supabase
4. **SSL Errors**: Ensure SSL is configured in connection string

### Debug Commands
```bash
# Test secrets are set
wrangler secret list --env production

# Check logs
wrangler tail --env production

# Test deployment
wrangler dev
```

### Supabase-Specific Debugging
```sql
-- Check table exists
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Test sample query
SELECT * FROM users LIMIT 1;

-- Check RLS policies
SELECT * FROM pg_policies WHERE tablename = 'users';
```

## Security Best Practices

1. **Never expose `service_role` key in client-side code**
2. **Use `anon` key for client-side operations**
3. **Enable Row Level Security (RLS)**
4. **Set up proper CORS configuration**
5. **Use environment-specific secrets**
6. **Regularly rotate API keys**

## Next Steps

1. ✅ Deploy database schema to Supabase
2. ✅ Configure Cloudflare Worker secrets
3. ✅ Test API endpoints
4. 🔄 Set up Supabase Storage for images
5. 🔄 Configure real-time subscriptions
6. 🔄 Enable Row Level Security
7. 🔄 Set up monitoring and logging

Your FitFriendsClubs platform is now connected to Supabase with full fitness club, virtual trails, and live streaming capabilities! 🏋️‍♀️