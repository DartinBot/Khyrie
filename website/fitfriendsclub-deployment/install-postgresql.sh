#!/bin/bash
# Install PostgreSQL support for FitFriendsClub

echo "🐘 Installing PostgreSQL support for FitFriendsClub..."
echo "=================================================="

# Activate virtual environment
source .venv/bin/activate

echo ""
echo "� Checking for pg_config in PATH..."
echo "------------------------------------"

# Common PostgreSQL installation paths on macOS
PG_PATHS=(
    "/opt/homebrew/bin"
    "/usr/local/bin" 
    "/usr/local/pgsql/bin"
    "/Applications/Postgres.app/Contents/Versions/*/bin"
    "/Library/PostgreSQL/*/bin"
)

# Check if pg_config is already in PATH
if command -v pg_config >/dev/null 2>&1; then
    PG_CONFIG_PATH=$(which pg_config)
    echo "✅ pg_config found in PATH: $PG_CONFIG_PATH"
    PG_VERSION=$(pg_config --version 2>/dev/null || echo "unknown")
    echo "   PostgreSQL version: $PG_VERSION"
    USE_BINARY=false
else
    echo "⚠️  pg_config not found in current PATH"
    
    # Search for pg_config in common locations
    echo "🔍 Searching for pg_config in common locations..."
    FOUND_PG_CONFIG=""
    
    for path in "${PG_PATHS[@]}"; do
        if [ -f "$path/pg_config" ]; then
            FOUND_PG_CONFIG="$path/pg_config"
            echo "✅ Found pg_config at: $FOUND_PG_CONFIG"
            break
        elif ls $path/pg_config 2>/dev/null; then
            FOUND_PG_CONFIG=$(ls $path/pg_config | head -1)
            echo "✅ Found pg_config at: $FOUND_PG_CONFIG"
            break
        fi
    done
    
    if [ -n "$FOUND_PG_CONFIG" ]; then
        # Add to PATH for this session
        PG_DIR=$(dirname "$FOUND_PG_CONFIG")
        export PATH="$PG_DIR:$PATH"
        echo "📍 Added $PG_DIR to PATH for this session"
        USE_BINARY=false
    else
        echo "❌ pg_config not found in common locations"
        echo "💡 Will use binary wheel installation instead"
        USE_BINARY=true
    fi
fi

echo ""
echo "📦 Installing psycopg2..."
echo "-------------------------"

if [ "$USE_BINARY" = true ]; then
    # Install using binary wheel to avoid pg_config issues
    echo "🔄 Installing psycopg2-binary (recommended for deployment)..."
    if pip install --only-binary=psycopg2-binary psycopg2-binary; then
        echo "✅ psycopg2-binary installed successfully!"
    else
        echo "❌ Failed to install psycopg2-binary"
        echo "💡 Try installing PostgreSQL development libraries first:"
        echo "   macOS: brew install postgresql"
        echo "   Ubuntu: sudo apt-get install postgresql-dev"
        exit 1
    fi
else
    # Try to install from source with pg_config available
    echo "🔄 Installing psycopg2 from source (pg_config available)..."
    if pip install psycopg2>=2.9.0; then
        echo "✅ psycopg2 installed successfully from source!"
    else
        echo "⚠️  Source installation failed, falling back to binary..."
        if pip install --only-binary=psycopg2-binary psycopg2-binary; then
            echo "✅ psycopg2-binary installed as fallback!"
        else
            echo "❌ Both source and binary installation failed"
            exit 1
        fi
    fi
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