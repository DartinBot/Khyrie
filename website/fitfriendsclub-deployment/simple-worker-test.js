// Simple FitFriendsClubs Test Worker
// Use this minimal version to test deployment before deploying the full worker

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Content-Type': 'application/json'
    };
    
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 200, headers: corsHeaders });
    }
    
    try {
      // Test endpoints
      switch (path) {
        case '/':
        case '/health':
          return new Response(JSON.stringify({
            status: 'success',
            message: 'FitFriendsClubs API is running! 🏋️‍♀️',
            timestamp: new Date().toISOString(),
            environment: env.ENVIRONMENT || 'development',
            version: '1.0.0'
          }), { status: 200, headers: corsHeaders });
          
        case '/test/database':
          return await testDatabaseConnection(env, corsHeaders);
          
        case '/test/clubs':
          return await testClubsEndpoint(env, corsHeaders);
          
        case '/test/trails':
          return await testTrailsEndpoint(env, corsHeaders);
          
        case '/test/all':
          return await runAllTests(env, corsHeaders);
          
        default:
          return new Response(JSON.stringify({
            error: 'Not Found',
            message: `Endpoint ${path} not found`,
            availableEndpoints: [
              '/ - Health check',
              '/health - Health check',
              '/test/database - Test database connection',
              '/test/clubs - Test fitness clubs data',
              '/test/trails - Test virtual trails data',
              '/test/all - Run all tests'
            ]
          }), { status: 404, headers: corsHeaders });
      }
    } catch (error) {
      return new Response(JSON.stringify({
        error: 'Internal Server Error',
        message: error.message,
        timestamp: new Date().toISOString()
      }), { status: 500, headers: corsHeaders });
    }
  }
};

// Test database connection
async function testDatabaseConnection(env, corsHeaders) {
  try {
    const supabaseUrl = env.SUPABASE_URL || 'https://bkaebhccbzpwiyxmpyln.supabase.co';
    const supabaseKey = env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrYWViaGNjYnpwd2l5eG1weWxuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzMjk2NDQsImV4cCI6MjA3NDkwNTY0NH0.n_PZ5YsBxjF6jDPM3HPZ5Vl3ilgKfHiHRVoiLM1h5nY';
    
    const startTime = Date.now();
    
    // Simple test - just select a few user records to verify connection
    const response = await fetch(`${supabaseUrl}/rest/v1/users?select=id,username&limit=3`, {
      headers: {
        'apikey': supabaseKey,
        'Authorization': `Bearer ${supabaseKey}`,
        'Content-Type': 'application/json'
      }
    });
    
    const endTime = Date.now();
    const responseTime = endTime - startTime;
    
    if (response.ok) {
      const data = await response.json();
      return new Response(JSON.stringify({
        status: 'success',
        message: 'Database connection successful! ✅',
        data: {
          connected: true,
          userCount: data.length,
          responseTime: `${responseTime}ms`,
          supabaseUrl: supabaseUrl,
          sampleUsers: data.map(u => u.username || 'unnamed'),
          httpStatus: response.status
        }
      }), { status: 200, headers: corsHeaders });
    } else {
      const errorText = await response.text().catch(() => 'Unknown error');
      throw new Error(`Database connection failed: ${response.status} - ${errorText}`);
    }
  } catch (error) {
    return new Response(JSON.stringify({
      status: 'error',
      message: 'Database connection failed ❌',
      error: error.message,
      troubleshooting: {
        possibleCauses: [
          'Supabase URL or API key incorrect',
          'Network connectivity issue',
          'Table permissions not set correctly',
          'API rate limiting'
        ]
      }
    }), { status: 500, headers: corsHeaders });
  }
}

// Test fitness clubs endpoint
async function testClubsEndpoint(env, corsHeaders) {
  try {
    const supabaseUrl = env.SUPABASE_URL || 'https://bkaebhccbzpwiyxmpyln.supabase.co';
    const supabaseKey = env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrYWViaGNjYnpwd2l5eG1weWxuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzMjk2NDQsImV4cCI6MjA3NDkwNTY0NH0.n_PZ5YsBxjF6jDPM3HPZ5Vl3ilgKfHiHRVoiLM1h5nY';
    
    const response = await fetch(`${supabaseUrl}/rest/v1/fitness_clubs?select=id,name,category,equipment_type&limit=5`, {
      headers: {
        'apikey': supabaseKey,
        'Authorization': `Bearer ${supabaseKey}`
      }
    });
    
    if (response.ok) {
      const clubs = await response.json();
      return new Response(JSON.stringify({
        status: 'success',
        message: 'Fitness clubs data retrieved! 🏃‍♀️',
        data: {
          totalClubs: clubs.length,
          clubs: clubs,
          sampleClub: clubs[0] || null
        }
      }), { status: 200, headers: corsHeaders });
    } else {
      throw new Error(`Failed to fetch clubs: ${response.status}`);
    }
  } catch (error) {
    return new Response(JSON.stringify({
      status: 'error',
      message: 'Failed to retrieve fitness clubs ❌',
      error: error.message
    }), { status: 500, headers: corsHeaders });
  }
}

// Test virtual trails endpoint
async function testTrailsEndpoint(env, corsHeaders) {
  try {
    const supabaseUrl = env.SUPABASE_URL || 'https://bkaebhccbzpwiyxmpyln.supabase.co';
    const supabaseKey = env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrYWViaGNjYnpwd2l5eG1weWxuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzMjk2NDQsImV4cCI6MjA3NDkwNTY0NH0.n_PZ5YsBxjF6jDPM3HPZ5Vl3ilgKfHiHRVoiLM1h5nY';
    
    const response = await fetch(`${supabaseUrl}/rest/v1/virtual_trails?select=id,name,location,difficulty,distance_km&limit=5`, {
      headers: {
        'apikey': supabaseKey,
        'Authorization': `Bearer ${supabaseKey}`
      }
    });
    
    if (response.ok) {
      const trails = await response.json();
      return new Response(JSON.stringify({
        status: 'success',
        message: 'Virtual trails data retrieved! 🗺️',
        data: {
          totalTrails: trails.length,
          trails: trails,
          featuredTrail: trails.find(t => t.name === 'Central Park Loop') || trails[0]
        }
      }), { status: 200, headers: corsHeaders });
    } else {
      throw new Error(`Failed to fetch trails: ${response.status}`);
    }
  } catch (error) {
    return new Response(JSON.stringify({
      status: 'error',
      message: 'Failed to retrieve virtual trails ❌',
      error: error.message
    }), { status: 500, headers: corsHeaders });
  }
}

// Run all tests
async function runAllTests(env, corsHeaders) {
  const tests = [];
  
  try {
    // Test 1: Database connection
    const dbTest = await testDatabaseConnection(env, corsHeaders);
    const dbResult = await dbTest.json();
    tests.push({
      name: 'Database Connection',
      status: dbResult.status,
      message: dbResult.message
    });
    
    // Test 2: Clubs endpoint
    const clubsTest = await testClubsEndpoint(env, corsHeaders);
    const clubsResult = await clubsTest.json();
    tests.push({
      name: 'Fitness Clubs',
      status: clubsResult.status,
      message: clubsResult.message,
      dataCount: clubsResult.data?.totalClubs || 0
    });
    
    // Test 3: Trails endpoint
    const trailsTest = await testTrailsEndpoint(env, corsHeaders);
    const trailsResult = await trailsTest.json();
    tests.push({
      name: 'Virtual Trails',
      status: trailsResult.status,
      message: trailsResult.message,
      dataCount: trailsResult.data?.totalTrails || 0
    });
    
    const allPassed = tests.every(test => test.status === 'success');
    
    return new Response(JSON.stringify({
      status: allPassed ? 'success' : 'partial',
      message: allPassed ? 'All tests passed! 🎉' : 'Some tests failed ⚠️',
      timestamp: new Date().toISOString(),
      results: tests,
      summary: {
        total: tests.length,
        passed: tests.filter(t => t.status === 'success').length,
        failed: tests.filter(t => t.status === 'error').length
      }
    }), { status: 200, headers: corsHeaders });
    
  } catch (error) {
    return new Response(JSON.stringify({
      status: 'error',
      message: 'Test suite failed to run',
      error: error.message,
      completedTests: tests
    }), { status: 500, headers: corsHeaders });
  }
}