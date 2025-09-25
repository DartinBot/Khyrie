#!/usr/bin/env python3
"""
Khyrie PWA Test Server
Complete integration test server for mobile PWA functionality
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Khyrie PWA Test Server",
    description="Mobile-first PWA test environment",
    version="1.2.0"
)

# Enable CORS for PWA functionality
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files configuration
static_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Icons directory for PWA manifest
icons_dir = os.path.join(static_dir, "icons")
if os.path.exists(icons_dir):
    app.mount("/icons", StaticFiles(directory=icons_dir), name="icons")

# Serve CSS files
@app.get("/mobile-app.css")
async def mobile_css():
    """Serve mobile app CSS"""
    try:
        css_path = os.path.join(static_dir, "mobile-app.css")
        with open(css_path, "r") as f:
            content = f.read()
        return Response(content=content, media_type="text/css")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSS file not found")

# Mock data for testing
mock_users = {
    "family_1": {
        "id": "family_1",
        "name": "Smith Family",
        "members": [
            {"id": "user_1", "name": "John Smith", "role": "parent", "workouts_this_week": 5},
            {"id": "user_2", "name": "Jane Smith", "role": "parent", "workouts_this_week": 3},
            {"id": "user_3", "name": "Sarah Smith", "role": "child", "workouts_this_week": 2},
        ]
    }
}

mock_workouts = [
    {
        "id": "workout_1",
        "name": "Upper Body Strength Focus",
        "duration": 35,
        "difficulty": "intermediate",
        "exercises": ["Push-ups", "Dumbbell Press", "Pull-ups"],
        "calories": 280,
        "ai_generated": True
    },
    {
        "id": "workout_2",
        "name": "Core Blast",
        "duration": 25,
        "difficulty": "beginner",
        "exercises": ["Planks", "Crunches", "Russian Twists"],
        "calories": 180,
        "ai_generated": True
    }
]

mock_trainers = [
    {
        "id": "trainer_1",
        "name": "Mike Johnson",
        "specialty": "Strength Training",
        "rating": 4.8,
        "hourly_rate": 75,
        "available_slots": ["9:00 AM", "2:00 PM", "5:00 PM"]
    },
    {
        "id": "trainer_2",
        "name": "Sarah Davis",
        "specialty": "Yoga & Flexibility",
        "rating": 4.9,
        "hourly_rate": 65,
        "available_slots": ["8:00 AM", "12:00 PM", "6:00 PM"]
    }
]

# Root route - serve mobile PWA
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the mobile PWA homepage"""
    try:
        with open(os.path.join(static_dir, "mobile.html"), "r") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Khyrie PWA Test</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <h1>🚀 Khyrie PWA Test Server</h1>
            <p>Mobile-index.html not found. Please ensure all PWA files are in place.</p>
            <p>✅ Server is running successfully!</p>
            <p>🔗 API endpoints available at /api/</p>
        </body>
        </html>
        """)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check for PWA"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.2.0",
        "features": {
            "pwa": True,
            "offline": True,
            "push_notifications": True,
            "camera": True,
            "health_integration": True,
            "family_features": True,
            "trainer_marketplace": True
        }
    }

# API Routes for PWA functionality
@app.get("/api/user/profile")
async def get_user_profile():
    """Get current user profile"""
    return {
        "id": "user_1",
        "name": "John Smith",
        "email": "john@example.com",
        "family_id": "family_1",
        "workouts_this_week": 5,
        "total_workouts": 127,
        "streak": 12,
        "goals": {
            "weekly_workouts": 7,
            "weekly_calories": 1200
        }
    }

@app.get("/api/workouts")
async def get_workouts():
    """Get available workouts"""
    return {
        "workouts": mock_workouts,
        "total": len(mock_workouts),
        "ai_recommendations": [
            {
                "workout_id": "workout_1",
                "reason": "Based on your recent strength training progress",
                "confidence": 0.85
            }
        ]
    }

@app.post("/api/workouts/generate")
async def generate_ai_workout(request: Request):
    """Generate AI workout"""
    body = await request.json()
    preferences = body.get("preferences", {})
    
    # Simulate AI workout generation
    generated_workout = {
        "id": f"ai_workout_{datetime.now().timestamp()}",
        "name": f"{preferences.get('focus', 'Full Body')} AI Workout",
        "duration": preferences.get("duration", 30),
        "difficulty": preferences.get("difficulty", "intermediate"),
        "exercises": [
            "AI-selected Exercise 1",
            "AI-selected Exercise 2", 
            "AI-selected Exercise 3",
            "AI-selected Exercise 4"
        ],
        "ai_generated": True,
        "personalized": True
    }
    
    return {
        "workout": generated_workout,
        "generation_time": 2.5,
        "confidence": 0.92
    }

@app.get("/api/family")
async def get_family_data():
    """Get family workout data"""
    family = mock_users["family_1"]
    
    # Add recent activity
    family["recent_activity"] = [
        {
            "user_id": "user_1",
            "user_name": "Dad",
            "action": "completed workout",
            "workout": "Core Blast",
            "timestamp": "2 hours ago",
            "emoji": "🔥"
        },
        {
            "user_id": "user_2", 
            "user_name": "Mom",
            "action": "set new squat PR",
            "details": "150 lbs",
            "timestamp": "5 hours ago",
            "emoji": "🎉"
        },
        {
            "user_id": "user_3",
            "user_name": "Sarah",
            "action": "completed yoga session",
            "duration": "30 minutes",
            "timestamp": "Yesterday",
            "emoji": "🧘‍♀️"
        }
    ]
    
    return family

@app.get("/api/trainers")
async def get_trainers():
    """Get available personal trainers"""
    return {
        "trainers": mock_trainers,
        "total": len(mock_trainers),
        "featured": mock_trainers[0]["id"]
    }

@app.post("/api/trainers/{trainer_id}/book")
async def book_trainer(trainer_id: str, request: Request):
    """Book a training session"""
    body = await request.json()
    
    return {
        "booking_id": f"booking_{datetime.now().timestamp()}",
        "trainer_id": trainer_id,
        "scheduled_time": body.get("time"),
        "duration": body.get("duration", 60),
        "cost": 75,
        "status": "confirmed",
        "meeting_link": "https://meet.khyrie.app/session123"
    }

@app.get("/api/health-data")
async def get_health_data():
    """Get health integration data"""
    return {
        "steps_today": 8342,
        "calories_burned": 456,
        "heart_rate_avg": 72,
        "sleep_hours": 7.5,
        "integration_status": {
            "apple_health": True,
            "google_fit": True,
            "last_sync": datetime.now().isoformat()
        },
        "weekly_summary": {
            "total_workouts": 5,
            "total_calories": 1890,
            "avg_heart_rate": 75,
            "goal_completion": 0.71
        }
    }

@app.post("/api/camera/analyze")
async def analyze_form(request: Request):
    """Analyze workout form from camera"""
    # Simulate form analysis
    return {
        "analysis_id": f"analysis_{datetime.now().timestamp()}",
        "exercise": "Push-up",
        "score": 85,
        "feedback": [
            {
                "type": "positive",
                "message": "Good arm positioning and core engagement"
            },
            {
                "type": "improvement", 
                "message": "Try to lower your chest closer to the ground"
            }
        ],
        "recommendations": [
            "Focus on slower controlled movement",
            "Engage core throughout the movement"
        ],
        "processed_in": 1.2
    }

@app.post("/api/offline-sync")
async def sync_offline_data(request: Request):
    """Sync offline data when back online"""
    body = await request.json()
    
    return {
        "synced_items": len(body.get("data", [])),
        "conflicts": 0,
        "sync_timestamp": datetime.now().isoformat(),
        "status": "success"
    }

# PWA specific endpoints
@app.get("/api/pwa/install-prompt")
async def get_install_prompt_data():
    """Get data for PWA install prompt"""
    return {
        "should_prompt": True,
        "install_message": "Install Khyrie for the best mobile experience!",
        "benefits": [
            "🚀 Faster loading",
            "📱 Native-like experience", 
            "🔄 Offline functionality",
            "🔔 Push notifications"
        ]
    }

@app.post("/api/notifications/subscribe")
async def subscribe_notifications(request: Request):
    """Subscribe to push notifications"""
    body = await request.json()
    
    return {
        "subscription_id": f"sub_{datetime.now().timestamp()}",
        "endpoint": body.get("endpoint"),
        "status": "subscribed",
        "notification_types": [
            "workout_reminders",
            "family_activity", 
            "trainer_messages",
            "achievement_alerts"
        ]
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler for PWA"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "pwa_fallback": True
        }
    )

@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    """Custom 500 handler for PWA"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error", 
            "message": "Something went wrong on our end",
            "offline_mode": True
        }
    )

# Static file serving for PWA assets
@app.get("/manifest.json")
async def serve_manifest():
    """Serve PWA manifest"""
    try:
        with open(os.path.join(static_dir, "manifest.json"), "r") as f:
            return JSONResponse(json.load(f))
    except FileNotFoundError:
        return JSONResponse({
            "name": "Khyrie Fitness",
            "short_name": "Khyrie",
            "start_url": "/",
            "display": "standalone",
            "theme_color": "#667eea",
            "background_color": "#ffffff"
        })

@app.get("/sw.js")
async def serve_service_worker():
    """Serve service worker"""
    try:
        with open(os.path.join(static_dir, "sw.js"), "r") as f:
            return HTMLResponse(f.read(), media_type="application/javascript")
    except FileNotFoundError:
        return HTMLResponse("// Service worker not found", media_type="application/javascript")

def main():
    """Run the PWA test server"""
    print("🚀 Starting Khyrie PWA Test Server...")
    print("📱 Mobile-optimized Progressive Web App")
    print("🔗 Server will be available at: http://localhost:8000")
    print("📲 Test PWA installation and offline functionality")
    print("🔄 Background sync, push notifications, and camera features enabled")
    print("\n✨ Features to test:")
    print("   - 📱 PWA installation prompt")
    print("   - 🔄 Offline workout capability") 
    print("   - 🔔 Push notifications")
    print("   - 📸 Camera integration")
    print("   - 👨‍👩‍👧‍👦 Family features")
    print("   - 🏥 Health platform integration")
    print("   - 👨‍🏫 Trainer marketplace")
    print("\n🎯 Open http://localhost:8000 on mobile or desktop")
    print("💡 Use Chrome DevTools > Application > Service Workers to test PWA features")
    
    uvicorn.run(
        "pwa_test_server:app",
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()