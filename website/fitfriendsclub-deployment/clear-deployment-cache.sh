#!/bin/bash
# Universal Cache Clearing Script
# Clears caches for all major deployment platforms

echo "🧹 CLEARING DEPLOYMENT CACHES"
echo "============================="

# Local pip cache clearing
echo "1. 🏠 Clearing local pip cache..."
pip cache purge 2>/dev/null || echo "   No pip cache to clear"
rm -rf ~/.cache/pip 2>/dev/null || true
rm -rf /tmp/pip* 2>/dev/null || true
echo "   ✅ Local pip cache cleared"

# Platform-specific cache clearing commands
echo ""
echo "2. 🌐 Platform-specific cache clearing commands:"
echo ""

echo "📦 HEROKU:"
echo "   heroku builds:cache:purge -a YOUR_APP_NAME"
echo "   heroku restart -a YOUR_APP_NAME"
echo ""

echo "🚄 RAILWAY:"
echo "   Go to Railway dashboard → Your service → Settings → Clear Build Cache"
echo "   Or redeploy with 'Force rebuild' option"
echo ""

echo "🎨 RENDER:"
echo "   Go to Render dashboard → Your service → Manual Deploy → Clear build cache"
echo "   Or use 'Clear build cache' in service settings"
echo ""

echo "🔷 NETLIFY (for functions):"
echo "   Go to Site settings → Build & deploy → Clear cache"
echo "   Or use: netlify build:clear-cache"
echo ""

echo "▲ VERCEL:"
echo "   vercel --force"
echo "   Or go to dashboard → Deployments → Clear cache"
echo ""

echo "🐳 DOCKER:"
echo "   docker builder prune -af"
echo "   docker system prune -af"
echo ""

# Local environment reset
echo "3. 🔄 Local environment reset (if needed)..."
if [ -d ".venv" ]; then
    echo "   Virtual environment found. To reset completely:"
    echo "   rm -rf .venv"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r backend/requirements-binary-only.txt"
else
    echo "   No virtual environment found"
fi

echo ""
echo "4. 🎯 After clearing cache, redeploy with:"
echo "   - Use requirements-binary-only.txt"
echo "   - Or run ./deploy-with-binary-enforcement.sh"
echo ""
echo "✅ Cache clearing guide complete!"