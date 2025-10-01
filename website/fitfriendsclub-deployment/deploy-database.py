#!/usr/bin/env python3
"""
FitFriendsClubs Database Deployment Script (Python)
Alternative deployment method using Python and psycopg2
"""

import os
import sys
from pathlib import Path

# Check if psycopg2 is available
try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    print("❌ psycopg2 module not found. Install it with:")
    print("   pip install psycopg2-binary")
    print("   # or")
    print("   conda install psycopg2")
    sys.exit(1)

def log(message, color=None):
    """Print colored log messages"""
    colors = {
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'reset': '\033[0m'
    }
    
    if color:
        print(f"{colors.get(color, '')}{message}{colors['reset']}")
    else:
        print(message)

def deploy_database():
    """Main deployment function"""
    log('🏋️  FitFriendsClubs Database Deployment (Python)', 'blue')
    log('=================================================', 'blue')
    print()

    # Check environment variables
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        log('❌ ERROR: DATABASE_URL environment variable is not set', 'red')
        print()
        print('Please set your DATABASE_URL. Examples:')
        print()
        print('  # Supabase')
        print('  export DATABASE_URL="postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres"')
        print()
        print('  # Neon')
        print('  export DATABASE_URL="postgresql://[user]:[password]@[endpoint]/[dbname]"')
        print()
        print('  # Local PostgreSQL')
        print('  export DATABASE_URL="postgresql://username:password@localhost:5432/fitfriendsclubs"')
        print()
        print('Then run this script again:')
        print('  python deploy-database.py')
        sys.exit(1)

    # Hide password in log
    safe_url = database_url
    if '://' in database_url and '@' in database_url:
        parts = database_url.split('@')
        if len(parts) == 2:
            prefix = parts[0].split('://')
            if len(prefix) == 2 and ':' in prefix[1]:
                user_pass = prefix[1].split(':')
                safe_url = f"{prefix[0]}://{user_pass[0]}:****@{parts[1]}"

    log('📊 Database Connection:', 'yellow')
    print(f'  URL: {safe_url}')
    print()

    # Check if schema file exists
    schema_path = Path(__file__).parent / 'complete-schema.sql'
    if not schema_path.exists():
        log('❌ ERROR: Schema file "complete-schema.sql" not found', 'red')
        print()
        print("Make sure you're running this script from the correct directory.")
        sys.exit(1)

    # Read schema file
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_content = f.read()
    except Exception as e:
        log('❌ ERROR: Could not read schema file', 'red')
        print(f'Error: {e}')
        sys.exit(1)

    log('📁 Schema file loaded: complete-schema.sql', 'yellow')
    print()

    # Connect to database
    try:
        log('🔌 Testing database connection...', 'yellow')
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Test connection
        cursor.execute('SELECT NOW() as current_time')
        result = cursor.fetchone()
        
        log('✅ Database connection successful', 'green')
        log(f'   Server time: {result[0]}', 'green')
        print()

        # Show deployment overview
        log('📋 Schema Overview:', 'yellow')
        print('  This will create the following table groups:')
        print('  • Core Tables: users, workouts, social_posts')
        print('  • Fitness Clubs: fitness_clubs, club_members, group_sessions')
        print('  • Equipment: user_equipment, equipment_workout_data')
        print('  • Virtual Trails: virtual_trails, trail_sessions, trail_achievements')
        print('  • Live Streaming: streaming_sessions, stream_viewers, chat_messages')
        print('  • Notifications: notifications, user_preferences')
        print('  • Sample Data: Demo clubs, trails, and test user')
        print()

        # Confirmation
        log('⚠️  IMPORTANT: This will create/modify tables in your database', 'yellow')
        
        # Auto-deploy (in production, you might want manual confirmation)
        log('🚀 Starting database deployment...', 'blue')
        print()

        # Execute schema
        log('📊 Executing SQL schema...', 'yellow')
        cursor.execute(schema_content)
        conn.commit()

        log('✅ Database schema deployed successfully!', 'green')
        print()

        # Verify deployment
        log('🔍 Verifying deployment...', 'yellow')
        
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
        """)
        
        table_count = cursor.fetchone()[0]
        print(f'  Tables created: {table_count}')
        
        # List tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE' 
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        
        print()
        log('📋 Created Tables:', 'yellow')
        for table in tables:
            print(f'  • {table[0]}')

        print()
        log('🎉 Deployment Complete!', 'green')
        print()
        log('Next Steps:', 'blue')
        print('  1. 📝 Update Cloudflare Workers environment variables:')
        print('     - DATABASE_API_URL: Your database API endpoint')
        print('     - DATABASE_API_KEY: Your database API key')
        print('     - TURN_SERVER_SECRET: WebRTC TURN server secret')
        print()
        print('  2. 🌐 Configure DNS records (see DNS_RECORDS.md)')
        print()
        print('  3. 🧪 Test API endpoints:')
        print('     curl https://api.fitfriendsclubs.com/api/health')
        print()
        print('  4. 📱 Set up streaming infrastructure:')
        print('     - RTMP server for live video')
        print('     - WebSocket server for real-time chat')
        print('     - TURN/STUN servers for WebRTC')
        print()
        log('Your FitFriendsClubs platform is ready to deploy! 🏋️‍♀️', 'green')

    except psycopg2.Error as e:
        log('❌ Database deployment failed', 'red')
        print()
        print(f'Database error: {e}')
        print()
        print('Common issues:')
        print('  • Permission denied: Your user needs CREATE table permissions')
        print('  • Connection timeout: Database might be slow or overloaded')
        print('  • Invalid connection string: Check DATABASE_URL format')
        print('  • SSL certificate issues: For cloud databases, check SSL settings')
        print()
        print('To debug:')
        print('  1. Test connection: psql "$DATABASE_URL" -c "SELECT NOW();"')
        print('  2. Check permissions and database existence')
        print('  3. Verify SSL requirements for cloud databases')
        
        sys.exit(1)

    except Exception as e:
        log('❌ Unexpected error occurred', 'red')
        print(f'Error: {e}')
        sys.exit(1)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    deploy_database()