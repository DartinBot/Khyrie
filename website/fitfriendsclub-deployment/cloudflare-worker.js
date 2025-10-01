// Cloudflare Worker - Direct conversion of your Flask FitFriendsClubs API
// This converts your existing Flask routes to Cloudflare Workers

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;
    
    // CORS headers for Wix integration
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*', // Configure for your Wix domain: https://yoursite.wix.com
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
        case path === '/api/clubs' && method === 'GET':
          response = await getFitnessClubs(request, env);
          break;
        case path === '/api/clubs' && method === 'POST':
          response = await createFitnessClub(request, env);
          break;
        case path.startsWith('/api/clubs/') && path.endsWith('/join') && method === 'POST':
          const clubId = path.split('/')[3];
          response = await joinFitnessClub(clubId, request, env);
          break;
        case path.startsWith('/api/clubs/') && path.endsWith('/leave') && method === 'POST':
          const leaveClubId = path.split('/')[3];
          response = await leaveFitnessClub(leaveClubId, request, env);
          break;
        case path === '/api/clubs/sessions' && method === 'GET':
          response = await getGroupSessions(request, env);
          break;
        case path === '/api/clubs/sessions' && method === 'POST':
          response = await createGroupSession(request, env);
          break;
        case path.startsWith('/api/clubs/sessions/') && path.endsWith('/join') && method === 'POST':
          const sessionId = path.split('/')[4];
          response = await joinGroupSession(sessionId, request, env);
          break;
        case path.startsWith('/api/clubs/') && path.endsWith('/members') && method === 'GET':
          const membersClubId = path.split('/')[3];
          response = await getClubMembers(membersClubId, request, env);
          break;
        case path === '/api/equipment/connect' && method === 'POST':
          response = await connectEquipment(request, env);
          break;
        case path === '/api/equipment/sync' && method === 'POST':
          response = await syncEquipmentData(request, env);
          break;
        case path === '/api/trails' && method === 'GET':
          response = await getVirtualTrails(request, env);
          break;
        case path.startsWith('/api/trails/') && method === 'GET':
          const trailId = path.split('/')[3];
          response = await getTrailDetails(trailId, request, env);
          break;
        case path === '/api/trails/sessions' && method === 'POST':
          response = await createTrailSession(request, env);
          break;
        case path.startsWith('/api/trails/') && path.endsWith('/sessions') && method === 'GET':
          const trailSessionId = path.split('/')[3];
          response = await getTrailSessions(trailSessionId, request, env);
          break;
        case path === '/api/trails/leaderboard' && method === 'GET':
          response = await getTrailLeaderboard(request, env);
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
    
    const imageUrl = `https://api.fitfriendsclubs.com/images/${fileName}`;
    
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

// ===== FITNESS CLUBS & EQUIPMENT INTEGRATION =====

// Get all fitness clubs
async function getFitnessClubs(request, env) {
  try {
    const url = new URL(request.url);
    const category = url.searchParams.get('category'); // run, cycle, pilates, yoga, strength, etc.
    
    let query = `
      SELECT c.*, COUNT(m.user_id) as member_count,
             u.username as creator_name
      FROM fitness_clubs c 
      LEFT JOIN club_members m ON c.id = m.club_id 
      JOIN users u ON c.creator_id = u.id
    `;
    
    const params = [];
    if (category) {
      query += ' WHERE c.category = $1';
      params.push(category);
    }
    
    query += ' GROUP BY c.id, u.username ORDER BY member_count DESC, c.created_at DESC';
    
    const result = await queryDatabase(query, params, env);
    
    return new Response(JSON.stringify(result.rows), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to get fitness clubs' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Create a new fitness club
async function createFitnessClub(request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    const { name, description, category, equipment_type, max_members } = await request.json();
    
    // Validate required fields
    if (!name || !category) {
      return new Response(JSON.stringify({ 
        error: 'Club name and category are required' 
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Valid categories for fitness clubs
    const validCategories = ['run', 'cycle', 'pilates', 'yoga', 'strength', 'crossfit', 'hiit', 'dance', 'swimming'];
    if (!validCategories.includes(category.toLowerCase())) {
      return new Response(JSON.stringify({ 
        error: 'Invalid category. Valid options: ' + validCategories.join(', ') 
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    const result = await queryDatabase(
      `INSERT INTO fitness_clubs (creator_id, name, description, category, equipment_type, max_members, created_at) 
       VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *`,
      [userId, name, description, category.toLowerCase(), equipment_type, max_members || 100, new Date().toISOString()],
      env
    );
    
    // Automatically join creator to the club
    await queryDatabase(
      'INSERT INTO club_members (club_id, user_id, role, joined_at) VALUES ($1, $2, $3, $4)',
      [result.rows[0].id, userId, 'admin', new Date().toISOString()],
      env
    );
    
    return new Response(JSON.stringify({
      success: true,
      club: result.rows[0]
    }), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to create fitness club' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Join a fitness club
async function joinFitnessClub(clubId, request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    
    // Check if club exists and has space
    const clubResult = await queryDatabase(
      'SELECT * FROM fitness_clubs WHERE id = $1',
      [clubId],
      env
    );
    
    if (clubResult.rows.length === 0) {
      return new Response(JSON.stringify({ 
        error: 'Club not found' 
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Check if already a member
    const memberCheck = await queryDatabase(
      'SELECT id FROM club_members WHERE club_id = $1 AND user_id = $2',
      [clubId, userId],
      env
    );
    
    if (memberCheck.rows.length > 0) {
      return new Response(JSON.stringify({ 
        error: 'Already a member of this club' 
      }), {
        status: 409,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Check member count vs max_members
    const memberCount = await queryDatabase(
      'SELECT COUNT(*) as count FROM club_members WHERE club_id = $1',
      [clubId],
      env
    );
    
    const club = clubResult.rows[0];
    if (memberCount.rows[0].count >= club.max_members) {
      return new Response(JSON.stringify({ 
        error: 'Club is at maximum capacity' 
      }), {
        status: 409,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Join the club
    await queryDatabase(
      'INSERT INTO club_members (club_id, user_id, role, joined_at) VALUES ($1, $2, $3, $4)',
      [clubId, userId, 'member', new Date().toISOString()],
      env
    );
    
    return new Response(JSON.stringify({
      success: true,
      message: 'Successfully joined the club'
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to join club' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Leave a fitness club
async function leaveFitnessClub(clubId, request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    
    const result = await queryDatabase(
      'DELETE FROM club_members WHERE club_id = $1 AND user_id = $2 RETURNING id',
      [clubId, userId],
      env
    );
    
    if (result.rows.length === 0) {
      return new Response(JSON.stringify({ 
        error: 'Not a member of this club' 
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return new Response(JSON.stringify({
      success: true,
      message: 'Successfully left the club'
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to leave club' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Get club members
async function getClubMembers(clubId, request, env) {
  try {
    await getUserFromToken(request, env); // Verify authentication
    
    const result = await queryDatabase(
      `SELECT u.id, u.username, u.profile_picture, cm.role, cm.joined_at 
       FROM club_members cm 
       JOIN users u ON cm.user_id = u.id 
       WHERE cm.club_id = $1 
       ORDER BY cm.joined_at ASC`,
      [clubId],
      env
    );
    
    return new Response(JSON.stringify(result.rows), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to get club members' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Get group workout sessions
async function getGroupSessions(request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    const url = new URL(request.url);
    const clubId = url.searchParams.get('club_id');
    const upcoming = url.searchParams.get('upcoming') === 'true';
    
    let query = `
      SELECT gs.*, fc.name as club_name, fc.category, fc.equipment_type,
             u.username as instructor_name,
             COUNT(gsp.user_id) as participant_count
      FROM group_sessions gs
      JOIN fitness_clubs fc ON gs.club_id = fc.id
      JOIN users u ON gs.instructor_id = u.id
      LEFT JOIN group_session_participants gsp ON gs.id = gsp.session_id
    `;
    
    const params = [];
    const conditions = [];
    
    if (clubId) {
      conditions.push('gs.club_id = $' + (params.length + 1));
      params.push(clubId);
    }
    
    if (upcoming) {
      conditions.push('gs.start_time > $' + (params.length + 1));
      params.push(new Date().toISOString());
    }
    
    // Only show sessions for clubs the user is a member of
    conditions.push(`EXISTS (
      SELECT 1 FROM club_members cm 
      WHERE cm.club_id = gs.club_id AND cm.user_id = $${params.length + 1}
    )`);
    params.push(userId);
    
    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }
    
    query += ' GROUP BY gs.id, fc.name, fc.category, fc.equipment_type, u.username ORDER BY gs.start_time ASC';
    
    const result = await queryDatabase(query, params, env);
    
    return new Response(JSON.stringify(result.rows), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to get group sessions' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Create a group workout session
async function createGroupSession(request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    const { club_id, title, description, start_time, duration_minutes, max_participants, equipment_settings } = await request.json();
    
    // Verify user is admin/moderator of the club
    const memberCheck = await queryDatabase(
      'SELECT role FROM club_members WHERE club_id = $1 AND user_id = $2',
      [club_id, userId],
      env
    );
    
    if (memberCheck.rows.length === 0 || !['admin', 'moderator'].includes(memberCheck.rows[0].role)) {
      return new Response(JSON.stringify({ 
        error: 'Only club admins and moderators can create sessions' 
      }), {
        status: 403,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    const result = await queryDatabase(
      `INSERT INTO group_sessions (club_id, instructor_id, title, description, start_time, duration_minutes, max_participants, equipment_settings, created_at) 
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING *`,
      [club_id, userId, title, description, start_time, duration_minutes, max_participants || 50, JSON.stringify(equipment_settings), new Date().toISOString()],
      env
    );
    
    return new Response(JSON.stringify({
      success: true,
      session: result.rows[0]
    }), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to create group session' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Join a group workout session
async function joinGroupSession(sessionId, request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    
    // Check if session exists and user is club member
    const sessionResult = await queryDatabase(
      `SELECT gs.*, cm.user_id as is_member 
       FROM group_sessions gs
       LEFT JOIN club_members cm ON gs.club_id = cm.club_id AND cm.user_id = $1
       WHERE gs.id = $2`,
      [userId, sessionId],
      env
    );
    
    if (sessionResult.rows.length === 0) {
      return new Response(JSON.stringify({ 
        error: 'Session not found' 
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    const session = sessionResult.rows[0];
    if (!session.is_member) {
      return new Response(JSON.stringify({ 
        error: 'Must be a club member to join sessions' 
      }), {
        status: 403,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Check if already joined
    const participantCheck = await queryDatabase(
      'SELECT id FROM group_session_participants WHERE session_id = $1 AND user_id = $2',
      [sessionId, userId],
      env
    );
    
    if (participantCheck.rows.length > 0) {
      return new Response(JSON.stringify({ 
        error: 'Already joined this session' 
      }), {
        status: 409,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Check capacity
    const participantCount = await queryDatabase(
      'SELECT COUNT(*) as count FROM group_session_participants WHERE session_id = $1',
      [sessionId],
      env
    );
    
    if (participantCount.rows[0].count >= session.max_participants) {
      return new Response(JSON.stringify({ 
        error: 'Session is at maximum capacity' 
      }), {
        status: 409,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Join the session
    await queryDatabase(
      'INSERT INTO group_session_participants (session_id, user_id, joined_at) VALUES ($1, $2, $3)',
      [sessionId, userId, new Date().toISOString()],
      env
    );
    
    return new Response(JSON.stringify({
      success: true,
      message: 'Successfully joined the session'
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to join session' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Connect fitness equipment (treadmill, bike, etc.)
async function connectEquipment(request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    const { equipment_type, equipment_id, brand, model, connection_data } = await request.json();
    
    // Valid equipment types
    const validTypes = ['treadmill', 'stationary_bike', 'elliptical', 'rowing_machine', 'smart_trainer'];
    if (!validTypes.includes(equipment_type)) {
      return new Response(JSON.stringify({ 
        error: 'Invalid equipment type. Valid options: ' + validTypes.join(', ')
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Store equipment connection
    const result = await queryDatabase(
      `INSERT INTO user_equipment (user_id, equipment_type, equipment_id, brand, model, connection_data, connected_at, is_active) 
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING *`,
      [userId, equipment_type, equipment_id, brand, model, JSON.stringify(connection_data), new Date().toISOString(), true],
      env
    );
    
    return new Response(JSON.stringify({
      success: true,
      equipment: result.rows[0],
      message: 'Equipment connected successfully'
    }), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to connect equipment' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Sync equipment data during workouts
async function syncEquipmentData(request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    const { session_id, equipment_id, workout_data } = await request.json();
    
    // Validate workout data structure
    const { 
      duration_seconds, 
      distance, 
      calories_burned, 
      avg_heart_rate, 
      max_heart_rate,
      speed_data, // Array of speed measurements over time
      resistance_data, // Array of resistance levels over time
      timestamps // Array of timestamps for data points
    } = workout_data;
    
    // Store workout metrics
    const result = await queryDatabase(
      `INSERT INTO equipment_workout_data 
       (user_id, session_id, equipment_id, duration_seconds, distance, calories_burned, 
        avg_heart_rate, max_heart_rate, speed_data, resistance_data, timestamps, synced_at) 
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12) RETURNING *`,
      [
        userId, session_id, equipment_id, duration_seconds, distance, calories_burned,
        avg_heart_rate, max_heart_rate, JSON.stringify(speed_data), 
        JSON.stringify(resistance_data), JSON.stringify(timestamps), new Date().toISOString()
      ],
      env
    );
    
    // If this is part of a group session, update leaderboard
    if (session_id) {
      await updateSessionLeaderboard(session_id, userId, workout_data, env);
    }
    
    return new Response(JSON.stringify({
      success: true,
      data: result.rows[0],
      message: 'Workout data synced successfully'
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to sync equipment data' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Helper function to update session leaderboard
async function updateSessionLeaderboard(sessionId, userId, workoutData, env) {
  try {
    // Calculate score based on workout type and metrics
    let score = 0;
    if (workoutData.distance) score += workoutData.distance * 10; // 10 points per unit distance
    if (workoutData.calories_burned) score += workoutData.calories_burned; // 1 point per calorie
    if (workoutData.duration_seconds) score += Math.floor(workoutData.duration_seconds / 60) * 5; // 5 points per minute
    
    await queryDatabase(
      `INSERT INTO session_leaderboard (session_id, user_id, score, distance, duration_seconds, calories_burned, updated_at)
       VALUES ($1, $2, $3, $4, $5, $6, $7)
       ON CONFLICT (session_id, user_id) 
       DO UPDATE SET score = $3, distance = $4, duration_seconds = $5, calories_burned = $6, updated_at = $7`,
      [sessionId, userId, score, workoutData.distance, workoutData.duration_seconds, workoutData.calories_burned, new Date().toISOString()],
      env
    );
  } catch (error) {
    console.error('Failed to update leaderboard:', error);
  }
}

// ===== VIRTUAL TRAILS SYSTEM =====

// Get virtual trails with filtering options
async function getVirtualTrails(request, env) {
  try {
    const url = new URL(request.url);
    const activity_type = url.searchParams.get('activity_type'); // run, cycle, both
    const difficulty = url.searchParams.get('difficulty'); // easy, moderate, hard, expert
    const location = url.searchParams.get('location'); // city, country, or region
    const distance_min = url.searchParams.get('distance_min');
    const distance_max = url.searchParams.get('distance_max');
    const featured = url.searchParams.get('featured') === 'true';
    
    let query = `
      SELECT vt.*, 
             COUNT(DISTINCT ts.id) as total_sessions,
             COUNT(DISTINCT ts.user_id) as total_participants,
             AVG(ts.completion_time_seconds) as avg_completion_time,
             MIN(ts.completion_time_seconds) as best_time
      FROM virtual_trails vt
      LEFT JOIN trail_sessions ts ON vt.id = ts.trail_id AND ts.completed = true
    `;
    
    const conditions = [];
    const params = [];
    
    if (activity_type && activity_type !== 'both') {
      conditions.push(`(vt.activity_type = $${params.length + 1} OR vt.activity_type = 'both')`);
      params.push(activity_type);
    }
    
    if (difficulty) {
      conditions.push(`vt.difficulty = $${params.length + 1}`);
      params.push(difficulty);
    }
    
    if (location) {
      conditions.push(`(LOWER(vt.location) LIKE $${params.length + 1} OR LOWER(vt.country) LIKE $${params.length + 1})`);
      params.push(`%${location.toLowerCase()}%`);
      params.push(`%${location.toLowerCase()}%`);
    }
    
    if (distance_min) {
      conditions.push(`vt.distance_km >= $${params.length + 1}`);
      params.push(parseFloat(distance_min));
    }
    
    if (distance_max) {
      conditions.push(`vt.distance_km <= $${params.length + 1}`);
      params.push(parseFloat(distance_max));
    }
    
    if (featured) {
      conditions.push(`vt.is_featured = true`);
    }
    
    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }
    
    query += ` 
      GROUP BY vt.id 
      ORDER BY vt.is_featured DESC, total_participants DESC, vt.name ASC
    `;
    
    const result = await queryDatabase(query, params, env);
    
    return new Response(JSON.stringify({
      trails: result.rows,
      total_count: result.rows.length
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to get virtual trails' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Get detailed information about a specific trail
async function getTrailDetails(trailId, request, env) {
  try {
    await getUserFromToken(request, env); // Verify authentication
    
    // Get trail details with statistics
    const trailResult = await queryDatabase(
      `SELECT vt.*,
              COUNT(DISTINCT ts.id) as total_sessions,
              COUNT(DISTINCT ts.user_id) as total_participants,
              AVG(ts.completion_time_seconds) as avg_completion_time,
              MIN(ts.completion_time_seconds) as best_time,
              MAX(ts.completion_time_seconds) as slowest_time
       FROM virtual_trails vt
       LEFT JOIN trail_sessions ts ON vt.id = ts.trail_id AND ts.completed = true
       WHERE vt.id = $1
       GROUP BY vt.id`,
      [trailId],
      env
    );
    
    if (trailResult.rows.length === 0) {
      return new Response(JSON.stringify({ 
        error: 'Trail not found' 
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Get recent sessions and leaderboard
    const recentSessions = await queryDatabase(
      `SELECT ts.*, u.username, u.profile_picture
       FROM trail_sessions ts
       JOIN users u ON ts.user_id = u.id
       WHERE ts.trail_id = $1 AND ts.completed = true
       ORDER BY ts.completed_at DESC
       LIMIT 10`,
      [trailId],
      env
    );
    
    // Get top performers (leaderboard)
    const leaderboard = await queryDatabase(
      `SELECT ts.*, u.username, u.profile_picture,
              RANK() OVER (ORDER BY ts.completion_time_seconds ASC) as rank
       FROM trail_sessions ts
       JOIN users u ON ts.user_id = u.id
       WHERE ts.trail_id = $1 AND ts.completed = true
       ORDER BY ts.completion_time_seconds ASC
       LIMIT 10`,
      [trailId],
      env
    );
    
    const trail = trailResult.rows[0];
    
    return new Response(JSON.stringify({
      trail,
      recent_sessions: recentSessions.rows,
      leaderboard: leaderboard.rows,
      statistics: {
        total_sessions: trail.total_sessions,
        total_participants: trail.total_participants,
        avg_completion_time: trail.avg_completion_time,
        best_time: trail.best_time,
        slowest_time: trail.slowest_time
      }
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to get trail details' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Create a trail session (start a virtual trail workout)
async function createTrailSession(request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    const { trail_id, equipment_id, session_mode } = await request.json();
    
    // Validate trail exists
    const trailResult = await queryDatabase(
      'SELECT * FROM virtual_trails WHERE id = $1',
      [trail_id],
      env
    );
    
    if (trailResult.rows.length === 0) {
      return new Response(JSON.stringify({ 
        error: 'Trail not found' 
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    const trail = trailResult.rows[0];
    
    // Create trail session
    const result = await queryDatabase(
      `INSERT INTO trail_sessions 
       (user_id, trail_id, equipment_id, session_mode, started_at, target_distance_km, target_elevation_gain_m, status)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING *`,
      [
        userId, trail_id, equipment_id, session_mode || 'solo',
        new Date().toISOString(), trail.distance_km, trail.elevation_gain_m, 'active'
      ],
      env
    );
    
    // Load trail route data for equipment configuration
    const routeData = JSON.parse(trail.route_data);
    
    return new Response(JSON.stringify({
      success: true,
      session: result.rows[0],
      trail_info: {
        name: trail.name,
        description: trail.description,
        distance_km: trail.distance_km,
        elevation_gain_m: trail.elevation_gain_m,
        difficulty: trail.difficulty,
        route_data: routeData
      },
      equipment_config: {
        incline_profile: routeData.elevation_profile,
        resistance_profile: routeData.resistance_profile,
        scenery_checkpoints: routeData.scenery_points,
        audio_cues: routeData.audio_cues
      }
    }), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to create trail session' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Get trail sessions for a specific trail
async function getTrailSessions(trailId, request, env) {
  try {
    const userId = await getUserFromToken(request, env);
    const url = new URL(request.url);
    const status = url.searchParams.get('status'); // 'active', 'completed', 'paused'
    const user_sessions_only = url.searchParams.get('user_only') === 'true';
    
    let query = `
      SELECT ts.*, u.username, u.profile_picture, vt.name as trail_name
      FROM trail_sessions ts
      JOIN users u ON ts.user_id = u.id
      JOIN virtual_trails vt ON ts.trail_id = vt.id
      WHERE ts.trail_id = $1
    `;
    
    const params = [trailId];
    
    if (status) {
      query += ` AND ts.status = $${params.length + 1}`;
      params.push(status);
    }
    
    if (user_sessions_only) {
      query += ` AND ts.user_id = $${params.length + 1}`;
      params.push(userId);
    }
    
    query += ' ORDER BY ts.started_at DESC LIMIT 50';
    
    const result = await queryDatabase(query, params, env);
    
    return new Response(JSON.stringify(result.rows), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to get trail sessions' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Get global trail leaderboard
async function getTrailLeaderboard(request, env) {
  try {
    await getUserFromToken(request, env); // Verify authentication
    
    const url = new URL(request.url);
    const trail_id = url.searchParams.get('trail_id');
    const activity_type = url.searchParams.get('activity_type');
    const time_period = url.searchParams.get('period') || 'all_time'; // 'week', 'month', 'year', 'all_time'
    
    let query = `
      SELECT ts.*, u.username, u.profile_picture, vt.name as trail_name,
             vt.location, vt.country, vt.distance_km,
             RANK() OVER (`;
    
    if (trail_id) {
      query += `PARTITION BY ts.trail_id ORDER BY ts.completion_time_seconds ASC`;
    } else {
      query += `ORDER BY ts.completion_time_seconds ASC`;
    }
    
    query += `) as rank
      FROM trail_sessions ts
      JOIN users u ON ts.user_id = u.id
      JOIN virtual_trails vt ON ts.trail_id = vt.id
      WHERE ts.completed = true`;
    
    const params = [];
    
    if (trail_id) {
      query += ` AND ts.trail_id = $${params.length + 1}`;
      params.push(trail_id);
    }
    
    if (activity_type) {
      query += ` AND vt.activity_type IN ($${params.length + 1}, 'both')`;
      params.push(activity_type);
    }
    
    // Time period filtering
    if (time_period !== 'all_time') {
      let interval;
      switch (time_period) {
        case 'week': interval = '7 days'; break;
        case 'month': interval = '30 days'; break;
        case 'year': interval = '365 days'; break;
        default: interval = '30 days';
      }
      query += ` AND ts.completed_at >= NOW() - INTERVAL '${interval}'`;
    }
    
    query += ` ORDER BY ts.completion_time_seconds ASC LIMIT 100`;
    
    const result = await queryDatabase(query, params, env);
    
    return new Response(JSON.stringify({
      leaderboard: result.rows,
      filters: {
        trail_id,
        activity_type,
        time_period
      }
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ 
      error: 'Failed to get trail leaderboard' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}