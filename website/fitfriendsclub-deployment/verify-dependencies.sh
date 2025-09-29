#!/bin/bash
# FitFriendsClub Dependency Verification Script

echo "🔍 Verifying FitFriendsClub Dependencies..."
echo "=============================================="

# Activate virtual environment
source .venv/bin/activate

echo ""
echo "📦 Core Dependencies Status:"
echo "----------------------------"

# Check each critical dependency
dependencies=(
    "flask:Flask web framework"
    "flask-cors:CORS support"
    "python-jose:JWT authentication"
    "pillow:Image processing"
    "python-multipart:File upload handling"
    "gunicorn:Production WSGI server"
    "black:Code formatting"
    "wheel:Package building tool"
)

for dep in "${dependencies[@]}"; do
    package=$(echo $dep | cut -d: -f1)
    description=$(echo $dep | cut -d: -f2)
    
    if pip show "$package" &>/dev/null; then
        version=$(pip show "$package" | grep Version | cut -d' ' -f2)
        echo "✅ $package ($version) - $description"
    else
        echo "❌ $package - MISSING - $description"
    fi
done

echo ""
echo "🗄️  Database Support:"
echo "---------------------"
if pip show psycopg2-binary &>/dev/null; then
    version=$(pip show psycopg2-binary | grep Version | cut -d' ' -f2)
    echo "✅ psycopg2-binary ($version) - PostgreSQL support"
else
    echo "⚠️  psycopg2-binary - Optional PostgreSQL support (SQLite will be used)"
fi

echo ""
echo "🧪 Application Test:"
echo "--------------------"
cd backend
if python -c "from app import app; print('✅ Flask application imports successfully')" 2>/dev/null; then
    echo "✅ All imports successful"
    echo "✅ Ready for development/production"
else
    echo "❌ Application import failed"
    echo "❌ Check dependencies and fix issues"
fi

echo ""
echo "📋 Installation Commands:"
echo "-------------------------"
echo "Main dependencies:     pip install -r requirements.txt"
echo "PostgreSQL support:    pip install -r requirements-postgres.txt"
echo "Format code:          ./format-code.sh"
echo ""
echo "🚀 Ready to launch FitFriendsClub!"