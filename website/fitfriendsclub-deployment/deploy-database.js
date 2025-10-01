#!/usr/bin/env node

/**
 * FitFriendsClubs Database Deployment Script (Node.js)
 * Alternative deployment method using Node.js and pg library
 */

const fs = require('fs');
const path = require('path');

// Check if pg module is available
let Client;
try {
  Client = require('pg').Client;
} catch (error) {
  console.error('❌ PostgreSQL module not found. Install it with:');
  console.error('   npm install pg');
  console.error('   # or');
  console.error('   yarn add pg');
  process.exit(1);
}

// Colors for console output
const colors = {
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

function log(message, color = 'reset') {
  console.log(colors[color] + message + colors.reset);
}

async function deployDatabase() {
  log('🏋️  FitFriendsClubs Database Deployment (Node.js)', 'blue');
  log('===================================================', 'blue');
  console.log('');

  // Check environment variables
  const databaseUrl = process.env.DATABASE_URL;
  if (!databaseUrl) {
    log('❌ ERROR: DATABASE_URL environment variable is not set', 'red');
    console.log('');
    console.log('Please set your DATABASE_URL. Examples:');
    console.log('');
    console.log('  # Supabase');
    console.log('  export DATABASE_URL="postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres"');
    console.log('');
    console.log('  # Neon');
    console.log('  export DATABASE_URL="postgresql://[user]:[password]@[endpoint]/[dbname]"');
    console.log('');
    console.log('  # Local PostgreSQL');
    console.log('  export DATABASE_URL="postgresql://username:password@localhost:5432/fitfriendsclubs"');
    console.log('');
    console.log('Then run this script again:');
    console.log('  node deploy-database.js');
    process.exit(1);
  }

  // Hide password in log
  const safeUrl = databaseUrl.replace(/:([^:]*?)@/, ':****@');
  log('📊 Database Connection:', 'yellow');
  console.log('  URL:', safeUrl);
  console.log('');

  // Check if schema file exists
  const schemaPath = path.join(__dirname, 'complete-schema.sql');
  if (!fs.existsSync(schemaPath)) {
    log('❌ ERROR: Schema file "complete-schema.sql" not found', 'red');
    console.log('');
    console.log('Make sure you\'re running this script from the correct directory.');
    process.exit(1);
  }

  // Read schema file
  let schemaContent;
  try {
    schemaContent = fs.readFileSync(schemaPath, 'utf8');
  } catch (error) {
    log('❌ ERROR: Could not read schema file', 'red');
    console.error(error.message);
    process.exit(1);
  }

  log('📁 Schema file loaded: complete-schema.sql', 'yellow');
  console.log('');

  // Create database client
  const client = new Client({
    connectionString: databaseUrl,
    ssl: databaseUrl.includes('supabase.co') || databaseUrl.includes('neon.tech') ? { rejectUnauthorized: false } : false
  });

  try {
    // Test connection
    log('🔌 Testing database connection...', 'yellow');
    await client.connect();
    
    const result = await client.query('SELECT NOW() as current_time');
    log('✅ Database connection successful', 'green');
    log(`   Server time: ${result.rows[0].current_time}`, 'green');
    console.log('');

    // Show deployment overview
    log('📋 Schema Overview:', 'yellow');
    console.log('  This will create the following table groups:');
    console.log('  • Core Tables: users, workouts, social_posts');
    console.log('  • Fitness Clubs: fitness_clubs, club_members, group_sessions');
    console.log('  • Equipment: user_equipment, equipment_workout_data');
    console.log('  • Virtual Trails: virtual_trails, trail_sessions, trail_achievements');
    console.log('  • Live Streaming: streaming_sessions, stream_viewers, chat_messages');
    console.log('  • Notifications: notifications, user_preferences');
    console.log('  • Sample Data: Demo clubs, trails, and test user');
    console.log('');

    // Confirmation (in production, you might want to skip this)
    log('⚠️  IMPORTANT: This will create/modify tables in your database', 'yellow');
    
    // Auto-deploy (comment out if you want manual confirmation)
    log('🚀 Starting database deployment...', 'blue');
    console.log('');

    // Execute schema
    log('📊 Executing SQL schema...', 'yellow');
    await client.query(schemaContent);

    log('✅ Database schema deployed successfully!', 'green');
    console.log('');

    // Verify deployment
    log('🔍 Verifying deployment...', 'yellow');
    
    const tableCountResult = await client.query(`
      SELECT COUNT(*) as count 
      FROM information_schema.tables 
      WHERE table_schema = 'public' 
      AND table_type = 'BASE TABLE'
    `);
    
    const tableCount = tableCountResult.rows[0].count;
    console.log(`  Tables created: ${tableCount}`);
    
    // List tables
    const tablesResult = await client.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public' 
      AND table_type = 'BASE TABLE' 
      ORDER BY table_name
    `);
    
    console.log('');
    log('📋 Created Tables:', 'yellow');
    tablesResult.rows.forEach(row => {
      console.log(`  • ${row.table_name}`);
    });

    console.log('');
    log('🎉 Deployment Complete!', 'green');
    console.log('');
    log('Next Steps:', 'blue');
    console.log('  1. 📝 Update Cloudflare Workers environment variables:');
    console.log('     - DATABASE_API_URL: Your database API endpoint');
    console.log('     - DATABASE_API_KEY: Your database API key');
    console.log('     - TURN_SERVER_SECRET: WebRTC TURN server secret');
    console.log('');
    console.log('  2. 🌐 Configure DNS records (see DNS_RECORDS.md)');
    console.log('');
    console.log('  3. 🧪 Test API endpoints:');
    console.log('     curl https://api.fitfriendsclubs.com/api/health');
    console.log('');
    console.log('  4. 📱 Set up streaming infrastructure:');
    console.log('     - RTMP server for live video');
    console.log('     - WebSocket server for real-time chat');
    console.log('     - TURN/STUN servers for WebRTC');
    console.log('');
    log('Your FitFriendsClubs platform is ready to deploy! 🏋️‍♀️', 'green');

  } catch (error) {
    log('❌ Schema deployment failed', 'red');
    console.log('');
    console.error('Error details:', error.message);
    console.log('');
    console.log('Common issues:');
    console.log('  • Permission denied: Your user needs CREATE table permissions');
    console.log('  • Connection timeout: Database might be slow or overloaded');
    console.log('  • Syntax error: Check PostgreSQL version compatibility');
    console.log('');
    console.log('To debug:');
    console.log('  1. Check connection string format');
    console.log('  2. Verify database permissions');
    console.log('  3. Test with a simple query first');
    
    process.exit(1);
  } finally {
    await client.end();
  }
}

// Run deployment
deployDatabase().catch(error => {
  console.error('Deployment script failed:', error);
  process.exit(1);
});