// Fixed FitFriendsClubs Test Worker
// This version properly handles environment variables and has better error handling

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
            version: '1.0.1',
            availableEndpoints: [
              '/ - Health check',
              '/test/database - Database connection test',
              '/test/clubs - Fitness clubs data test',
              '/test/trails - Virtual trails data test',
              '/test/all - Run complete test suite',
              '/debug/env - Check environment variables'
            ]
          }), { status: 200, headers: corsHeaders });
          
        case '/debug/env':
          return new Response(JSON.stringify({
            status: 'success',
            message: 'Environment variables debug info',
            environment: {
              SUPABASE_URL: env.SUPABASE_URL ? '✅ Set' : '❌ Missing',
              SUPABASE_ANON_KEY: env.SUPABASE_ANON_KEY ? '✅ Set (length: ' + env.SUPABASE_ANON_KEY.length + ')' : '❌ Missing',
              SUPABASE_SERVICE_KEY: env.SUPABASE_SERVICE_KEY ? '✅ Set' : '❌ Missing',
              DATABASE_URL: env.DATABASE_URL ? '✅ Set' : '❌ Missing',
              ENVIRONMENT: env.ENVIRONMENT || 'not set'
            },
            fallbackValues: {
              usingFallbackUrl: !env.SUPABASE_URL,
              usingFallbackKey: !env.SUPABASE_ANON_KEY
            }
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
              '/test/database - Test database connection',
              '/test/clubs - Test fitness clubs data',
              '/test/trails - Test virtual trails data',
              '/test/all - Run all tests',
              '/debug/env - Check environment variables'
            ]
          }), { status: 404, headers: corsHeaders });
      }
    } catch (error) {
      return new Response(JSON.stringify({
        error: 'Internal Server Error',
        message: error.message,
        timestamp: new Date().toISOString(),
        stack: error.stack
      }), { status: 500, headers: corsHeaders });
    }
  }
};

// Test database connection with better error handling
async function testDatabaseConnection(env, corsHeaders) {
  try {
    // Use environment variables with fallbacks
    const supabaseUrl = env.SUPABASE_URL || 'https://bkaebhccbzpwiyxmpyln.supabase.co';
    const supabaseKey = env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrYWViaGNjYnpwd2l5eG1weWxuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzMjk2NDQsImV4cCI6MjA3NDkwNTY0NH0.n_PZ5YsBxjF6jDPM3HPZ5Vl3ilgKfHiHRVoiLM1h5nY';
    
    const startTime = Date.now();
    
    // Test with a simple users query
    const response = await fetch(`${supabaseUrl}/rest/v1/users?select=id,username&limit=3`, {
      method: 'GET',
      headers: {
        'apikey': supabaseKey,
        'Authorization': `Bearer ${supabaseKey}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
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
          sampleUsers: data.map(u => u.username || `ID: ${u.id}`),
          httpStatus: response.status,
          usingEnvVars: {
            url: !!env.SUPABASE_URL,
            key: !!env.SUPABASE_ANON_KEY
          }
        }
      }), { status: 200, headers: corsHeaders });
    } else {
      const errorText = await response.text().catch(() => 'Could not read error response');
      return new Response(JSON.stringify({
        status: 'error',
        message: 'Database connection failed ❌',
        error: `HTTP ${response.status}: ${errorText}`,
        debug: {
          url: `${supabaseUrl}/rest/v1/users?select=id,username&limit=3`,
          status: response.status,
          statusText: response.statusText,
          responseTime: `${responseTime}ms`
        }
      }), { status: 500, headers: corsHeaders });
    }
  } catch (error) {
    return new Response(JSON.stringify({
      status: 'error',
      message: 'Database connection failed ❌',
      error: error.message,
      errorType: error.name,
      troubleshooting: {
        possibleCauses: [
          'Network connectivity issue',
          'Supabase API key expired or invalid',
          'CORS policy blocking the request',
          'Supabase service temporarily unavailable'
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
        'Authorization': `Bearer ${supabaseKey}`,
        'Content-Type': 'application/json'
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
          sampleClub: clubs[0] || null,
          httpStatus: response.status
        }
      }), { status: 200, headers: corsHeaders });
    } else {
      const errorText = await response.text().catch(() => 'Unknown error');
      throw new Error(`HTTP ${response.status}: ${errorText}`);
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
        'Authorization': `Bearer ${supabaseKey}`,
        'Content-Type': 'application/json'
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
          featuredTrail: trails.find(t => t.name === 'Central Park Loop') || trails[0],
          httpStatus: response.status
        }
      }), { status: 200, headers: corsHeaders });
    } else {
      const errorText = await response.text().catch(() => 'Unknown error');
      throw new Error(`HTTP ${response.status}: ${errorText}`);
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
  const startTime = Date.now();
  
  try {
    // Test 1: Database connection
    const dbTest = await testDatabaseConnection(env, corsHeaders);
    const dbResult = await dbTest.json();
    tests.push({
      name: 'Database Connection',
      status: dbResult.status,
      message: dbResult.message,
      responseTime: dbResult.data?.responseTime || 'unknown'
    });
    
    // Test 2: Clubs endpoint (only if database works)
    if (dbResult.status === 'success') {
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
    } else {
      tests.push({
        name: 'Fitness Clubs',
        status: 'skipped',
        message: 'Skipped due to database connection failure'
      });
      tests.push({
        name: 'Virtual Trails',
        status: 'skipped',
        message: 'Skipped due to database connection failure'
      });
    }
    
    const endTime = Date.now();
    const allPassed = tests.every(test => test.status === 'success');
    
    return new Response(JSON.stringify({
      status: allPassed ? 'success' : tests.some(t => t.status === 'success') ? 'partial' : 'failed',
      message: allPassed ? 'All tests passed! 🎉' : 'Some tests failed ⚠️',
      timestamp: new Date().toISOString(),
      totalTime: `${endTime - startTime}ms`,
      results: tests,
      summary: {
        total: tests.length,
        passed: tests.filter(t => t.status === 'success').length,
        failed: tests.filter(t => t.status === 'error').length,
        skipped: tests.filter(t => t.status === 'skipped').length
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