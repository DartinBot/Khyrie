#!/bin/bash
# Install PostgreSQL support for FitFriendsClub

echo "🐘 Installing PostgreSQL support for FitFriendsClub..."
echo "=================================================="

# Activate virtual environment
source .venv/bin/activate

echo ""
echo "📦 Installing psycopg2-binary..."
echo "--------------------------------"

# Install using binary wheel to avoid pg_config issues
if pip install --only-binary=psycopg2-binary psycopg2-binary; then
    echo "✅ psycopg2-binary installed successfully!"
else
    echo "❌ Failed to install psycopg2-binary"
    echo "💡 Try installing PostgreSQL development libraries first:"
    echo "   macOS: brew install postgresql"
    echo "   Ubuntu: sudo apt-get install postgresql-dev"
    exit 1
fi

echo ""
echo "🧪 Testing PostgreSQL support..."
echo "--------------------------------"

# Test the installation
python -c "
import psycopg2
print('✅ PostgreSQL support is working!')
print(f'   psycopg2 version: {psycopg2.__version__}')
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 PostgreSQL Support Successfully Installed!"
    echo "============================================"
    echo ""
    echo "📋 Your FitFriendsClub backend now supports:"
    echo "   ✅ SQLite (development/small production)"
    echo "   ✅ PostgreSQL (production databases)"
    echo ""
    echo "🚀 Set DATABASE_URL environment variable to use PostgreSQL:"
    echo "   export DATABASE_URL='postgresql://user:pass@host:port/dbname'"
else
    echo "❌ Installation verification failed"
    exit 1
fi