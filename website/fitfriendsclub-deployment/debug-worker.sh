#!/bin/bash
# Debug Cloudflare Worker Deployment
# Use this script to test your worker endpoint and diagnose issues

echo "🔍 FitFriendsClubs Worker Diagnostics"
echo "=================================="
echo ""

# Check if URL is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide your Cloudflare Worker URL"
    echo "Usage: $0 <worker-url>"
    echo "Example: $0 https://fitfriendsclubs-api.your-subdomain.workers.dev"
    exit 1
fi

WORKER_URL="$1"
echo "🎯 Testing Worker URL: $WORKER_URL"
echo ""

# Test 1: Basic connectivity
echo "📡 Test 1: Basic Connectivity"
echo "-----------------------------"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$WORKER_URL")
echo "HTTP Status Code: $HTTP_CODE"

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Worker is responding"
elif [ "$HTTP_CODE" = "404" ]; then
    echo "❌ Worker not found - check deployment"
elif [ "$HTTP_CODE" = "500" ]; then
    echo "⚠️ Worker error - check code"
else
    echo "⚠️ Unexpected status: $HTTP_CODE"
fi
echo ""

# Test 2: Response headers
echo "📋 Test 2: Response Headers"
echo "---------------------------"
curl -s -I "$WORKER_URL" | head -10
echo ""

# Test 3: Response content
echo "📄 Test 3: Response Content"
echo "---------------------------"
RESPONSE=$(curl -s "$WORKER_URL")
echo "Response preview (first 200 chars):"
echo "$RESPONSE" | head -c 200
echo ""
echo ""

# Test 4: Check if it's JSON
echo "🔍 Test 4: Content Type Analysis"
echo "--------------------------------"
CONTENT_TYPE=$(curl -s -I "$WORKER_URL" | grep -i "content-type" | cut -d' ' -f2- | tr -d '\r')
echo "Content-Type: $CONTENT_TYPE"

if [[ "$CONTENT_TYPE" == *"application/json"* ]]; then
    echo "✅ Correct JSON response"
    echo "📊 Formatted JSON response:"
    curl -s "$WORKER_URL" | jq . 2>/dev/null || echo "Response is not valid JSON"
elif [[ "$CONTENT_TYPE" == *"text/html"* ]]; then
    echo "❌ Getting HTML instead of JSON - likely an error page"
    echo "🔍 Checking if it's a Cloudflare error page..."
    if curl -s "$WORKER_URL" | grep -q "cloudflare"; then
        echo "⚠️ This appears to be a Cloudflare error page"
        echo "💡 Possible causes:"
        echo "   - Worker not deployed correctly"
        echo "   - Worker has runtime errors"
        echo "   - Wrong URL or route"
    fi
else
    echo "❓ Unexpected content type: $CONTENT_TYPE"
fi
echo ""

# Test 5: Test specific endpoints
echo "🎯 Test 5: Endpoint Tests"
echo "-------------------------"
ENDPOINTS=("/" "/health" "/test/database" "/test/clubs")

for endpoint in "${ENDPOINTS[@]}"; do
    echo "Testing: $WORKER_URL$endpoint"
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$WORKER_URL$endpoint")
    if [ "$STATUS" = "200" ]; then
        echo "  ✅ $endpoint - OK ($STATUS)"
    else
        echo "  ❌ $endpoint - Failed ($STATUS)"
    fi
done
echo ""

# Test 6: Check for CORS
echo "🌐 Test 6: CORS Headers"
echo "----------------------"
curl -s -H "Origin: https://example.com" -I "$WORKER_URL" | grep -i "access-control" || echo "No CORS headers found"
echo ""

echo "🏁 Diagnosis Complete!"
echo "====================="
echo ""
echo "💡 Next Steps:"
echo "1. If getting HTML responses, check your worker deployment in Cloudflare Dashboard"
echo "2. If status is 404, verify the worker URL and routing"
echo "3. If status is 500, check worker code for syntax errors"
echo "4. Use Cloudflare Dashboard → Workers → Your Worker → Logs for detailed errors"
echo ""
echo "🔗 Useful Links:"
echo "- Cloudflare Dashboard: https://dash.cloudflare.com/"
echo "- Worker Logs: https://dash.cloudflare.com/ → Workers & Pages → Your Worker → Logs"