#!/bin/bash
# FitFriendsClub Backend Production Startup Script

# Set environment variables
export FLASK_ENV=production
export FLASK_DEBUG=False

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Change to backend directory
cd backend

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Initialize database
echo "🗄️  Initializing database..."
python -c "from app import init_database; init_database()"

# Start Gunicorn server
echo "🚀 Starting FitFriendsClub Backend with Gunicorn..."
exec gunicorn \
    --config gunicorn.conf.py \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers ${WORKERS:-4} \
    --timeout ${TIMEOUT:-30} \
    --keep-alive ${KEEPALIVE:-2} \
    --max-requests ${MAX_REQUESTS:-1000} \
    --preload \
    app:app