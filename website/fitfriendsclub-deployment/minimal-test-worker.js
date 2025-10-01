// Ultra-simple test worker to verify deployment
export default {
  async fetch(request, env, ctx) {
    return new Response(JSON.stringify({
      status: "success",
      message: "FitFriendsClubs Worker is working! 🎉",
      timestamp: new Date().toISOString(),
      url: request.url,
      method: request.method
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }
};