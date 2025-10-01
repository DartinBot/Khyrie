# Wix Frontend + Cloudflare Workers Backend

## 🌐 Why This Combo is Powerful

### Cloudflare Workers Advantages
✅ **Lightning Fast** - Runs on 300+ edge locations worldwide
✅ **Serverless** - No cold starts, instant scaling  
✅ **Cost Effective** - 100k requests/day FREE
✅ **Built-in CORS** - Easy Wix integration
✅ **Global CDN** - Ultra-low latency everywhere

### Architecture Overview
```
Wix Website (Frontend) 
    ↓ HTTPS API Calls
Cloudflare Workers (Your Flask API)
    ↓ Database Queries  
PostgreSQL Database (Supabase/Neon)
```

## 🚀 Converting Your Flask App to Cloudflare Workers

### Option 1: Direct Port (Recommended)
Convert Flask routes to Cloudflare Worker functions:

```javascript
// worker.js - Main Cloudflare Worker
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    // CORS headers for Wix
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*', // Or your Wix domain
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };
    
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    try {
      let response;
      
      // Route handling (convert your Flask routes)
      switch (true) {
        case path.startsWith('/api/workouts'):
          response = await handleWorkouts(request, env);
          break;
        case path.startsWith('/api/users'):
          response = await handleUsers(request, env);
          break;
        case path.startsWith('/api/social'):
          response = await handleSocial(request, env);
          break;
        default:
          response = new Response('Not Found', { status: 404 });
      }
      
      // Add CORS headers to response
      Object.entries(corsHeaders).forEach(([key, value]) => {
        response.headers.set(key, value);
      });
      
      return response;
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', ...corsHeaders }
      });
    }
  }
};

// Workouts API (converted from your Flask route)
async function handleWorkouts(request, env) {
  const method = request.method;
  
  if (method === 'GET') {
    // Get workouts from database
    const workouts = await getWorkoutsFromDB(env.DATABASE_URL);
    return new Response(JSON.stringify(workouts), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  if (method === 'POST') {
    const workout = await request.json();
    const result = await createWorkoutInDB(workout, env.DATABASE_URL);
    return new Response(JSON.stringify(result), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Database functions using PostgreSQL
async function getWorkoutsFromDB(databaseUrl) {
  // Use a PostgreSQL client compatible with Workers
  const client = new PostgresClient(databaseUrl);
  const result = await client.query('SELECT * FROM workouts ORDER BY created_at DESC');
  return result.rows;
}
```

### Option 2: Hono Framework (Modern & Fast)
Use Hono framework - designed for Cloudflare Workers:

```javascript
// worker-hono.js
import { Hono } from 'hono';
import { cors } from 'hono/cors';

const app = new Hono();

// Enable CORS for Wix
app.use('*', cors({
  origin: ['https://yoursite.wix.com', 'https://www.yoursite.com'],
  allowHeaders: ['Content-Type', 'Authorization'],
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
}));

// Convert your Flask routes
app.get('/api/workouts', async (c) => {
  const workouts = await getWorkouts(c.env.DATABASE_URL);
  return c.json(workouts);
});

app.post('/api/workouts', async (c) => {
  const workout = await c.req.json();
  const result = await createWorkout(workout, c.env.DATABASE_URL);
  return c.json(result);
});

app.get('/api/users/:id', async (c) => {
  const userId = c.req.param('id');
  const user = await getUser(userId, c.env.DATABASE_URL);
  return c.json(user);
});

export default app;
```

## 📊 Database Integration Options

### 1. Supabase (Recommended)
```javascript
import { createClient } from '@supabase/supabase-js';

async function initSupabase(env) {
  return createClient(
    env.SUPABASE_URL,
    env.SUPABASE_ANON_KEY
  );
}

async function getWorkouts(env) {
  const supabase = await initSupabase(env);
  const { data, error } = await supabase
    .from('workouts')
    .select('*')
    .order('created_at', { ascending: false });
  
  if (error) throw error;
  return data;
}
```

### 2. Neon PostgreSQL
```javascript
import { Pool } from '@neondatabase/serverless';

async function queryDatabase(sql, params, env) {
  const pool = new Pool({ connectionString: env.DATABASE_URL });
  const client = await pool.connect();
  
  try {
    const result = await client.query(sql, params);
    return result.rows;
  } finally {
    client.release();
  }
}
```

## 🎨 Wix Frontend Integration

### 1. API Service in Wix
```javascript
// wix-code/api-service.js
import { fetch } from 'wix-fetch';

const API_BASE = 'https://your-worker.your-subdomain.workers.dev';

export class FitnessAPI {
  static async createWorkout(workoutData) {
    const response = await fetch(`${API_BASE}/api/workouts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(workoutData)
    });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    
    return response.json();
  }
  
  static async getWorkouts(userId) {
    const response = await fetch(`${API_BASE}/api/workouts?userId=${userId}`);
    return response.json();
  }
  
  static async getUserProfile(userId) {
    const response = await fetch(`${API_BASE}/api/users/${userId}`);
    return response.json();
  }
}
```

### 2. Wix Page Implementation
```javascript
// Wix Page Code
import { FitnessAPI } from 'backend/api-service.js';
import wixUsers from 'wix-users';

$w.onReady(function () {
  loadUserWorkouts();
  
  // Create workout form
  $w('#createWorkoutBtn').onClick(async () => {
    const workoutData = {
      title: $w('#workoutTitle').value,
      description: $w('#workoutDesc').value,
      duration: parseInt($w('#duration').value),
      intensity: $w('#intensity').value,
      userId: wixUsers.currentUser.id
    };
    
    try {
      $w('#loadingIcon').show();
      await FitnessAPI.createWorkout(workoutData);
      
      // Refresh workout list
      await loadUserWorkouts();
      
      // Clear form
      $w('#workoutForm').reset();
      $w('#successMessage').show();
      
    } catch (error) {
      console.error('Error creating workout:', error);
      $w('#errorMessage').text = 'Failed to create workout';
      $w('#errorMessage').show();
    } finally {
      $w('#loadingIcon').hide();
    }
  });
});

async function loadUserWorkouts() {
  try {
    const user = wixUsers.currentUser;
    if (!user.loggedIn) return;
    
    const workouts = await FitnessAPI.getWorkouts(user.id);
    
    // Display workouts in repeater
    $w('#workoutsRepeater').data = workouts;
    
  } catch (error) {
    console.error('Error loading workouts:', error);
  }
}
```

## 🚀 Deployment Steps

### 1. Setup Cloudflare Worker
```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create new worker
wrangler generate fitness-api

# Configure wrangler.toml
```

### 2. Configure Environment Variables
```toml
# wrangler.toml
name = "fitness-api"
main = "src/worker.js"
compatibility_date = "2023-12-01"

[vars]
ENVIRONMENT = "production"

[[env.production.vars]]
DATABASE_URL = "your-database-connection-string"
SUPABASE_URL = "your-supabase-url"
SUPABASE_ANON_KEY = "your-supabase-key"
```

### 3. Deploy to Cloudflare
```bash
# Deploy worker
wrangler publish

# Your API will be available at:
# https://fitness-api.your-subdomain.workers.dev
```

## 💰 Cost Breakdown

| Service | Free Tier | Monthly Cost |
|---------|-----------|--------------|
| Cloudflare Workers | 100k requests/day | $5/10M requests |
| Wix Premium | - | $16-35/month |
| Supabase Database | 500MB, 2 projects | $25/month |
| **Total** | **~100k requests/day FREE** | **$41-60/month** |

## 🏆 Why This Setup Rocks

### Performance Benefits
- ⚡ **Sub-50ms response times** globally
- 🌍 **Edge computing** - API runs close to users
- 🚀 **No cold starts** - Always ready
- 📱 **Mobile optimized** - Fast on all devices

### Developer Experience  
- 🔧 **Keep existing logic** - Port Flask routes easily
- 🎯 **Modern tooling** - TypeScript support
- 📊 **Built-in analytics** - Request monitoring
- 🔄 **Hot reloading** - Fast development

### Scalability
- 📈 **Automatic scaling** - Handle traffic spikes
- 🌐 **Global distribution** - 300+ locations
- 💾 **Edge caching** - Ultra-fast responses
- 🛡️ **DDoS protection** - Built-in security

**This combination gives you the best of both worlds: Wix's easy frontend building + Cloudflare's enterprise-grade backend infrastructure!**

Would you like me to help convert your specific Flask routes to Cloudflare Workers?