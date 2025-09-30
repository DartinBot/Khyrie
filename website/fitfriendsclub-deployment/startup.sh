# Azure App Service startup configuration for FitFriendsClub
# This ensures the Flask app starts correctly

# Change to backend directory and start gunicorn
cd backend
exec gunicorn app:app --bind 0.0.0.0:8000 --timeout 600 --workers 1