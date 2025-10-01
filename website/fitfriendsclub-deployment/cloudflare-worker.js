// Cloudflare Worker - Direct conversion of your Flask FitFriendsClub API
// This converts your existing Flask routes to Cloudflare Workers

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;
    
    // CORS headers for Wix integration
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*', // Configure for your Wix domain
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Max-Age': '86400',
    };
    
    // Handle CORS preflight requests
    if (method === 'OPTIONS') {
      return new Response(null, {
        status: 200,
        headers: corsHeaders
      });
    }
    
    try {
      let response;
      
      // Route your existing Flask endpoints
      switch (true) {
        case path === '/api/register':
          response = await handleRegister(request, env);
          break;
        case path === '/api/login':
          response = await handleLogin(request, env);
          break;
        case path === '/api/workouts' && method === 'GET':
          response = await getWorkouts(request, env);
          break;
        case path === '/api/workouts' && method === 'POST':
          response = await createWorkout(request, env);
          break;
        case path.startsWith('/api/workouts/') && method === 'DELETE':
          const workoutId = path.split('/')[3];
          response = await deleteWorkout(workoutId, request, env);
          break;
        case path === '/api/social/posts' && method === 'GET':
          response = await getSocialPosts(request, env);
          break;
        case path === '/api/social/posts' && method === 'POST':
          response = await createSocialPost(request, env);
          break;
        case path.startsWith('/api/social/posts/') && path.endsWith('/like'):
          const postId = path.split('/')[4];
          response = await likeSocialPost(postId, request, env);
          break;
        case path === '/api/user/profile':
          response = await getUserProfile(request, env);
          break;
        case path === '/api/user/profile' && method === 'PUT':
          response = await updateUserProfile(request, env);
          break;
        case path === '/api/upload':
          response = await handleImageUpload(request, env);
          break;
        case path === '/api/health':
          response = new Response(JSON.stringify({ 
            status: 'healthy', 
            timestamp: new Date().toISOString(),
            platform: 'Cloudflare Workers'
          }), {
            headers: { 'Content-Type': 'application/json' }
          });
          break;
        default:
          response = new Response('Not Found', { status: 404 });
      }
      
      // Add CORS headers to all responses
      Object.entries(corsHeaders).forEach(([key, value]) => {
        response.headers.set(key, value);
      });
      
      return response;
      
    } catch (error) {
      console.error('Worker Error:', error);
      return new Response(JSON.stringify({ 
        error: error.message,
        timestamp: new Date().toISOString()
      }), {
        status: 500,
        headers: { 
          'Content-Type': 'application/json',
          ...corsHeaders
        }
      });
    }
  }
};

// Helper function to get user from JWT token
async function getUserFromToken(request, env) {
  const authHeader = request.headers.get('Authorization');
  if (!authHeader?.startsWith('Bearer ')) {
    throw new Error('No valid authorization token');
  }
  
  const token = authHeader.substring(7);
  
  try {
    // In Cloudflare Workers, you'd use Web Crypto API for JWT verification
    // For simplicity, this example uses a basic decode (implement proper verification)
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.user_id;
  } catch (error) {
    throw new Error('Invalid token');
  }
}

// Database helper - works with Supabase, Neon, or any PostgreSQL
async function queryDatabase(sql, params = [], env) {
  const response = await fetch(env.DATABASE_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${env.DATABASE_API_KEY}`
    },
    body: JSON.stringify({ query: sql, params })
  });
  
  if (!response.ok) {
    throw new Error(`Database query failed: ${response.statusText}`);
  }
  
  return response.json();
}

// User Registration - converted from your Flask route
async function handleRegister(request, env) {
  const { username, email, password } = await request.json();
  
  // Validate input
  if (!username || !email || !password) {
    return new Response(JSON.stringify({ 
      error: 'Username, email, and password are required' 
    }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  // Hash password (use Web Crypto API in Workers)
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashedPassword = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  
  try {
    // Check if user exists
    const existingUser = await queryDatabase(
      'SELECT id FROM users WHERE username = $1 OR email = $2',
      [username, email],
      env
    );
    
    if (existingUser.rows.length > 0) {
      return new Response(JSON.stringify({ 
        error: 'Username or email already exists' 
      }), {
        status: 409,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Create user
    const result = await queryDatabase(
      'INSERT INTO users (username, email, password, created_at) VALUES ($1, $2, $3, $4) RETURNING id',
      [username, email, hashedPassword, new Date().toISOString()],
      env
    );
    
    const userId = result.rows[0].id;
    
    // Generate JWT token (simplified - implement proper JWT in production)
    const token = btoa(JSON.stringify({ 
      user_id: userId, 
      exp: Date.now() + 86400000 // 24 hours
    }));
    
    return new Response(JSON.stringify({
      success: true,
      token,
      user: { id: userId, username, email }
    }), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Registration failed' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// User Login - converted from your Flask route
async function handleLogin(request, env) {
  const { username, password } = await request.json();
  
  // Hash password for comparison
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashedPassword = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  
  try {
    const result = await queryDatabase(
      'SELECT id, username, email FROM users WHERE username = $1 AND password = $2',
      [username, hashedPassword],
      env
    );
    
    if (result.rows.length === 0) {
      return new Response(JSON.stringify({ 
        error: 'Invalid credentials' 
      }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    const user = result.rows[0];
    
    // Generate JWT token
    const token = btoa(JSON.stringify({ 
      user_id: user.id, 
      exp: Date.now() + 86400000 // 24 hours
    }));
    
    return new Response(JSON.stringify({
      success: true,
      token,
      user
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Login failed' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Get Workouts - converted from your Flask route
async function getWorkouts(request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    
    const result = await queryDatabase(
      'SELECT * FROM workouts WHERE user_id = $1 ORDER BY created_at DESC',
      [userId],
      env
    );
    
    return new Response(JSON.stringify(result.rows), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to get workouts' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Create Workout - converted from your Flask route
async function createWorkout(request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    const { title, description, duration, intensity } = await request.json();
    
    const result = await queryDatabase(
      'INSERT INTO workouts (user_id, title, description, duration, intensity, created_at) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *',
      [userId, title, description, duration, intensity, new Date().toISOString()],
      env
    );
    
    return new Response(JSON.stringify({
      success: true,
      workout: result.rows[0]
    }), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to create workout' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Delete Workout - converted from your Flask route
async function deleteWorkout(workoutId, request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    
    const result = await queryDatabase(
      'DELETE FROM workouts WHERE id = $1 AND user_id = $2 RETURNING id',
      [workoutId, userId],
      env
    );
    
    if (result.rows.length === 0) {
      return new Response(JSON.stringify({ 
        error: 'Workout not found' 
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return new Response(JSON.stringify({
      success: true,
      message: 'Workout deleted'
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to delete workout' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Get Social Posts - converted from your Flask route
async function getSocialPosts(request, env) {
  try {
    const result = await queryDatabase(`
      SELECT p.*, u.username, u.profile_picture 
      FROM social_posts p 
      JOIN users u ON p.user_id = u.id 
      ORDER BY p.created_at DESC
    `, [], env);
    
    return new Response(JSON.stringify(result.rows), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to get social posts' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Create Social Post - converted from your Flask route
async function createSocialPost(request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    const { content, image_url } = await request.json();
    
    const result = await queryDatabase(
      'INSERT INTO social_posts (user_id, content, image_url, likes, created_at) VALUES ($1, $2, $3, $4, $5) RETURNING *',
      [userId, content, image_url || null, 0, new Date().toISOString()],
      env
    );
    
    return new Response(JSON.stringify({
      success: true,
      post: result.rows[0]
    }), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to create social post' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Like Social Post - converted from your Flask route
async function likeSocialPost(postId, request, env) {
  try {
    await getUserFromToken(request, env); // Verify authentication
    
    const result = await queryDatabase(
      'UPDATE social_posts SET likes = likes + 1 WHERE id = $1 RETURNING likes',
      [postId],
      env
    );
    
    if (result.rows.length === 0) {
      return new Response(JSON.stringify({ 
        error: 'Post not found' 
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return new Response(JSON.stringify({
      success: true,
      likes: result.rows[0].likes
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to like post' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Get User Profile - converted from your Flask route
async function getUserProfile(request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    
    const result = await queryDatabase(
      'SELECT id, username, email, profile_picture, created_at FROM users WHERE id = $1',
      [userId],
      env
    );
    
    if (result.rows.length === 0) {
      return new Response(JSON.stringify({ 
        error: 'User not found' 
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return new Response(JSON.stringify(result.rows[0]), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to get user profile' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Update User Profile - converted from your Flask route
async function updateUserProfile(request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    const { username, email, profile_picture } = await request.json();
    
    const result = await queryDatabase(
      'UPDATE users SET username = $1, email = $2, profile_picture = $3 WHERE id = $4 RETURNING id, username, email, profile_picture',
      [username, email, profile_picture, userId],
      env
    );
    
    return new Response(JSON.stringify({
      success: true,
      user: result.rows[0]
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to update profile' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Image Upload Handler - converted from your Flask route
async function handleImageUpload(request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    
    // Handle multipart form data in Cloudflare Workers
    const formData = await request.formData();
    const file = formData.get('image');
    
    if (!file) {
      return new Response(JSON.stringify({ 
        error: 'No image file provided' 
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Upload to Cloudflare R2 or external service
    const fileId = crypto.randomUUID();
    const fileName = `uploads/${userId}/${fileId}-${file.name}`;
    
    // Store in Cloudflare R2 (if configured)
    await env.IMAGES_BUCKET.put(fileName, file.stream(), {
      httpMetadata: {
        contentType: file.type,
      },
    });
    
    const imageUrl = `https://your-domain.com/images/${fileName}`;
    
    return new Response(JSON.stringify({
      success: true,
      image_url: imageUrl,
      filename: fileName
    }), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to upload image' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}