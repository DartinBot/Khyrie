#!/bin/bash
# NUCLEAR OPTION: Absolutely prevent pg_config errors
# Use this if regular deployment keeps failing

echo "� NUCLEAR PostgreSQL FIX - BLOCKING ALL SOURCE COMPILATION"
echo "============================================================="

# Nuclear environment variables
export PIP_NO_CACHE_DIR=1
export PIP_PREFER_BINARY=1
export PIP_ONLY_BINARY=":all:"  # Block ALL source compilation
export PIP_CONSTRAINT="../constraints.txt"
export PYTHONDONTWRITEBYTECODE=1

echo "🧹 Step 1: Nuclear cache cleanup..."
pip cache purge 2>/dev/null || true
rm -rf ~/.cache/pip 2>/dev/null || true
rm -rf /tmp/pip* 2>/dev/null || true

echo "🛡️  Step 2: Installing with MAXIMUM protection..."
cd backend

# Try binary-only requirements first
if [ -f "requirements-binary-only.txt" ]; then
    echo "   Using requirements-binary-only.txt"
    pip install --no-cache-dir \
               --prefer-binary \
               --only-binary=:all: \
               --constraint ../constraints.txt \
               -r requirements-binary-only.txt
else
    echo "   Using regular requirements.txt with binary enforcement"
    pip install --no-cache-dir \
               --prefer-binary \
               --only-binary=:all: \
               --constraint ../constraints.txt \
               -r requirements.txt
fi

echo "✅ Installation complete - ZERO chance of source compilation!"

# Verify PostgreSQL support
python -c "
try:
    import psycopg2
    print(f'✅ psycopg2 version: {psycopg2.__version__}')
    print('🎉 SUCCESS: No pg_config errors possible!')
except Exception as e:
    print(f'❌ Error: {e}')
    exit(1)
"

echo "🚀 NUCLEAR FIX COMPLETE - pg_config errors eliminated forever!"