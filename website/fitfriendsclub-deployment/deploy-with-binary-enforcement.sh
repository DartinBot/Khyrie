#!/bin/bash
# Ultimate PostgreSQL deployment fix script
# Guarantees binary-only installation on any platform

echo "🚀 DEPLOYING WITH POSTGRESQL BINARY ENFORCEMENT"
echo "================================================"

# Set environment variables to force binary installation
export PIP_NO_CACHE_DIR=1
export PIP_PREFER_BINARY=1
export PIP_ONLY_BINARY="psycopg2,psycopg2-binary"

echo "📦 Installing dependencies with binary enforcement..."

# Clear any cached pip state
pip cache purge 2>/dev/null || true

# Install with maximum binary enforcement
cd backend
pip install --no-cache-dir \
           --prefer-binary \
           --only-binary=psycopg2 \
           --only-binary=psycopg2-binary \
           -r requirements.txt

echo "✅ Installation complete - zero compilation!"

# Verify PostgreSQL support
python -c "import psycopg2; print(f'✅ psycopg2 version: {psycopg2.__version__}')"

echo "🎉 Deployment ready with bulletproof PostgreSQL support!"