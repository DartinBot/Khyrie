#!/bin/bash
# VERSION COMPATIBLE PostgreSQL Deployment
# Tries multiple psycopg2-binary versions until one works

echo "🔧 VERSION-COMPATIBLE PostgreSQL DEPLOYMENT"
echo "==========================================="

# Set binary-only environment
export PIP_NO_CACHE_DIR=1
export PIP_PREFER_BINARY=1
export PIP_ONLY_BINARY=":all:"

cd backend

echo "📦 Trying different psycopg2-binary versions..."

# Version priority list (newest to oldest)
VERSIONS=("2.9.9" "2.9.8" "2.9.7" "2.9.6" "2.9.5")

for version in "${VERSIONS[@]}"; do
    echo "   🔄 Trying psycopg2-binary==$version..."
    
    # Create temporary requirements with this version
    sed "s/psycopg2-binary==.*/psycopg2-binary==$version/" requirements.txt > temp-requirements.txt
    
    # Try to install
    if pip install --no-cache-dir --prefer-binary --only-binary=:all: -r temp-requirements.txt; then
        echo "   ✅ SUCCESS with psycopg2-binary==$version"
        
        # Update the actual requirements file with working version
        sed -i.bak "s/psycopg2-binary==.*/psycopg2-binary==$version/" requirements.txt
        echo "   📝 Updated requirements.txt to use version $version"
        
        # Verify installation
        python -c "import psycopg2; print(f'✅ PostgreSQL ready: {psycopg2.__version__}')"
        
        # Cleanup
        rm temp-requirements.txt requirements.txt.bak 2>/dev/null || true
        
        echo "🎉 DEPLOYMENT READY with compatible PostgreSQL version!"
        exit 0
    else
        echo "   ❌ Version $version not available"
        rm temp-requirements.txt 2>/dev/null || true
    fi
done

# If all specific versions fail, try flexible version
echo "🔄 Trying flexible version range..."
if pip install --no-cache-dir --prefer-binary --only-binary=:all: -r ../backend/requirements-flexible.txt; then
    echo "✅ SUCCESS with flexible version range"
    echo "📝 Consider using requirements-flexible.txt for deployment"
    echo "🎉 DEPLOYMENT READY with flexible PostgreSQL version!"
else
    echo "❌ All PostgreSQL versions failed"
    echo "💡 Try manually updating requirements.txt with an older version"
    exit 1
fi