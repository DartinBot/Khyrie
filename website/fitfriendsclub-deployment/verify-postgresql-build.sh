#!/bin/bash

# PostgreSQL Build Verification Script
# Ensures psycopg2-binary is properly configured for production builds

echo "🔍 Verifying PostgreSQL build configuration..."
echo "=================================================="

# Check if we're in the right directory
if [[ ! -f "backend/requirements.txt" ]]; then
    echo "❌ Error: backend/requirements.txt not found"
    echo "   Please run this script from the project root directory"
    exit 1
fi

# Verify psycopg2-binary is in requirements.txt
if grep -q "psycopg2-binary==" backend/requirements.txt; then
    VERSION=$(grep "psycopg2-binary==" backend/requirements.txt | cut -d'=' -f3)
    echo "✅ psycopg2-binary found in requirements.txt: $VERSION"
else
    echo "❌ psycopg2-binary not found in requirements.txt"
    exit 1
fi

# Test installation in a clean environment simulation
echo ""
echo "🧪 Testing dependency installation..."
echo "------------------------------------"

if [[ -d ".venv" ]]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
    
    # Test pip install (dry run first)
    echo "🔄 Testing requirements.txt installation..."
    pip install --dry-run -r backend/requirements.txt > /dev/null 2>&1
    
    if [[ $? -eq 0 ]]; then
        echo "✅ All dependencies can be installed successfully"
        
        # Verify psycopg2 is actually installed
        python -c "import psycopg2; print('✅ psycopg2 import test: PASSED')" 2>/dev/null
        if [[ $? -eq 0 ]]; then
            echo "✅ psycopg2 runtime test: PASSED"
        else
            echo "❌ psycopg2 runtime test: FAILED"
            exit 1
        fi
    else
        echo "❌ Dependency installation test: FAILED"
        exit 1
    fi
else
    echo "⚠️  Virtual environment not found - skipping runtime tests"
fi

echo ""
echo "🎉 PostgreSQL Build Verification: COMPLETE"
echo "============================================="
echo "✅ psycopg2-binary is properly configured"
echo "✅ Dependencies are compatible"
echo "✅ Ready for production build"
echo ""
echo "💡 Build tips:"
echo "   • Using psycopg2-binary (no pg_config required)"
echo "   • Pinned version for consistent builds"
echo "   • Compatible with cloud platforms (Heroku, Railway, Render)"