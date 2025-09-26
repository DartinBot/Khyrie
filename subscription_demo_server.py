"""
Khyrie Subscription Demo Server
FastAPI server to demonstrate the complete subscription system
"""

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
import uvicorn
import os

# Import our subscription components
from subscription_api import subscription_router
from subscription_models import get_db, User, create_tables, create_sample_data

# Create FastAPI app
app = FastAPI(title="Khyrie Subscription Demo", version="1.0.0")

# Include subscription routes
app.include_router(subscription_router)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    print("🚀 Initializing Khyrie Subscription Demo Server...")
    try:
        create_tables()
        create_sample_data()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Database initialization: {str(e)}")

# Serve static files (HTML, CSS, JS)
@app.get("/")
async def root():
    """Serve the main subscription demo page"""
    return FileResponse("subscription_demo.html")

@app.get("/subscription")
@app.get("/subscribe")
async def subscription_page():
    """Serve the subscription demo page"""
    return FileResponse("subscription_demo.html")

# Demo API endpoints
@app.get("/api/demo/status")
async def demo_status():
    """Get demo system status"""
    return {
        "status": "active",
        "message": "Khyrie Subscription Demo is running!",
        "features": {
            "stripe_integration": True,
            "premium_ai": True,
            "subscription_tiers": 4,
            "database": True
        }
    }

@app.get("/api/demo/features")
async def demo_features():
    """Get available features for demo"""
    return {
        "free": [
            "Basic workout tracking",
            "Exercise library (50 exercises)",
            "Family group (3 members)",
            "Basic progress charts"
        ],
        "premium": [
            "AI workout generation",
            "Advanced progress analytics", 
            "Unlimited family members",
            "Custom meal plans",
            "Priority support"
        ],
        "pro": [
            "Everything in Premium +",
            "Real-time form analysis",
            "Injury risk prediction",
            "Advanced AI coaching",
            "Wearable device integration"
        ],
        "elite": [
            "Everything in Pro +",
            "AI voice coaching",
            "AR workout experiences",
            "Personal trainer sessions (2/month)",
            "24/7 AI health monitoring"
        ]
    }

@app.post("/api/demo/simulate-upgrade")
async def simulate_upgrade(request: dict):
    """Simulate subscription upgrade for demo"""
    tier = request.get("tier", "premium")
    
    # Simulate processing time
    import time
    time.sleep(1)
    
    prices = {
        "premium": 9.99,
        "pro": 19.99,
        "elite": 39.99
    }
    
    return {
        "success": True,
        "message": f"Successfully upgraded to {tier.upper()} plan!",
        "tier": tier,
        "price": prices.get(tier, 0),
        "features_unlocked": await demo_features()
    }

@app.get("/api/demo/ai-workout")
async def demo_ai_workout():
    """Demo AI workout generation"""
    return {
        "workout": {
            "name": "AI-Powered Upper Body Strength",
            "duration": 35,
            "difficulty": "intermediate",
            "exercises": [
                {
                    "name": "Push-ups",
                    "sets": 3,
                    "reps": "12-15",
                    "rest": 60,
                    "form_tips": ["Keep core tight", "Full range of motion"]
                },
                {
                    "name": "Pull-ups", 
                    "sets": 3,
                    "reps": "8-12",
                    "rest": 90,
                    "form_tips": ["Control the descent", "Pull to chest level"]
                },
                {
                    "name": "Shoulder Press",
                    "sets": 3,
                    "reps": "10-15",
                    "rest": 60,
                    "form_tips": ["Press overhead", "Keep core engaged"]
                }
            ],
            "ai_notes": [
                "Focus on proper form over speed",
                "Increase weight if completing all reps easily"
            ],
            "estimated_calories": 285
        },
        "tier_required": "premium"
    }

@app.get("/api/demo/form-analysis")
async def demo_form_analysis():
    """Demo form analysis feature"""
    return {
        "analysis": {
            "exercise": "Squat",
            "form_score": 87,
            "injury_risk": 15,
            "breakdown": {
                "knee_alignment": "Excellent (95%)",
                "depth": "Good (85%)",
                "core_stability": "Needs improvement (75%)"
            },
            "recommendations": [
                "Engage core more throughout movement",
                "Maintain consistent descent speed",
                "Focus on driving through heels"
            ],
            "next_session_focus": "Core stability exercises"
        },
        "tier_required": "pro"
    }

@app.get("/api/demo/voice-coaching")
async def demo_voice_coaching():
    """Demo AI voice coaching"""
    return {
        "coaching_session": {
            "session_name": "Motivational Push-Up Challenge",
            "duration": 300,
            "voice_cues": [
                {
                    "time": 0,
                    "message": "Let's start with perfect form! Hands shoulder-width apart."
                },
                {
                    "time": 30,
                    "message": "Great job! Feel that strength building with each rep!"
                },
                {
                    "time": 60, 
                    "message": "Halfway there! Keep your core tight and breathe steady."
                }
            ],
            "adaptive_feedback": "Based on your performance, I'm adjusting the pace to match your strength level.",
            "motivation_style": "encouraging"
        },
        "tier_required": "elite"
    }

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Khyrie Subscription Demo",
        "timestamp": "2025-09-25T12:00:00Z"
    }

if __name__ == "__main__":
    print("🚀 Starting Khyrie Subscription Demo Server...")
    print("📱 Features:")
    print("   - Subscription pricing demo")
    print("   - Premium AI feature testing")
    print("   - Stripe integration simulation")
    print("   - Interactive payment flow")
    print()
    print("🔗 Access at: http://localhost:8080")
    print("📋 API docs: http://localhost:8080/docs")
    
    uvicorn.run(app, host="127.0.0.1", port=8080)