"""
Simple Khyrie Subscription Demo Server
Standalone demo without complex dependencies
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
import json
from datetime import datetime

# Create FastAPI app
app = FastAPI(title="Khyrie Subscription Demo", version="1.0.0")

# Store demo data
demo_data = {
    "current_tier": "free",
    "plans": {
        "free": {"price": 0, "name": "Free"},
        "premium": {"price": 9.99, "name": "Premium"},  
        "pro": {"price": 19.99, "name": "Pro"},
        "elite": {"price": 39.99, "name": "Elite"}
    }
}

@app.get("/")
async def root():
    """Serve the main subscription demo page"""
    return FileResponse("subscription_demo.html")

@app.get("/api/subscriptions/plans")
async def get_subscription_plans():
    """Get all available subscription plans"""
    plans = [
        {
            "tier": "free",
            "name": "Khyrie Free",
            "price_monthly": 0,
            "features": [
                "Basic workout tracking",
                "Exercise library (50 exercises)",
                "Family group (3 members)",
                "Basic progress charts",
                "Community features"
            ],
            "recommended": False
        },
        {
            "tier": "premium", 
            "name": "Khyrie Premium",
            "price_monthly": 9.99,
            "features": [
                "AI-powered workout recommendations",
                "Advanced progress analytics",
                "Unlimited family members", 
                "Full exercise library (500+ exercises)",
                "Custom meal plans",
                "Priority support",
                "Workout form analysis",
                "Progress predictions"
            ],
            "recommended": True
        },
        {
            "tier": "pro",
            "name": "Khyrie Pro", 
            "price_monthly": 19.99,
            "features": [
                "Everything in Premium +",
                "Real-time form analysis",
                "Predictive injury prevention",
                "Advanced AI coaching",
                "Wearable device integration",
                "API access for developers",
                "Custom workout AI generation",
                "Biometric trend analysis",
                "Nutrition AI recommendations"
            ],
            "recommended": False
        },
        {
            "tier": "elite",
            "name": "Khyrie Elite",
            "price_monthly": 39.99,
            "features": [
                "Everything in Pro +",
                "Personal AI coach with voice guidance", 
                "AR/VR workout experiences",
                "One-on-one trainer sessions (2/month)",
                "Advanced biometric tracking",
                "White-label licensing",
                "Priority feature requests",
                "24/7 AI health monitoring",
                "Custom app branding"
            ],
            "recommended": False
        }
    ]
    
    return {"plans": plans}

@app.post("/api/subscriptions/create")
async def create_subscription(request: dict):
    """Simulate subscription creation"""
    tier = request.get("tier")
    
    if not tier or tier not in ["premium", "pro", "elite"]:
        raise HTTPException(status_code=400, detail="Invalid subscription tier")
    
    # Simulate successful subscription
    demo_data["current_tier"] = tier
    
    return {
        "success": True,
        "subscription_id": f"sub_demo_{tier}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "client_secret": "pi_demo_client_secret", 
        "message": f"Successfully upgraded to {tier.title()} plan!"
    }

@app.get("/api/subscriptions/status") 
async def get_subscription_status():
    """Get current subscription status"""
    current_tier = demo_data["current_tier"]
    plan_info = demo_data["plans"][current_tier]
    
    features_by_tier = {
        "free": ["Basic workout tracking", "Exercise library (50)", "Family group (3 members)"],
        "premium": ["AI workout generation", "Advanced analytics", "Unlimited family", "Custom meal plans"],
        "pro": ["Real-time form analysis", "Injury prediction", "Advanced AI coaching", "Wearable integration"], 
        "elite": ["AI voice coaching", "AR workouts", "Personal trainer sessions", "24/7 monitoring"]
    }
    
    # Get all features up to current tier
    all_features = []
    tier_order = ["free", "premium", "pro", "elite"]
    current_index = tier_order.index(current_tier)
    
    for i in range(current_index + 1):
        all_features.extend(features_by_tier[tier_order[i]])
    
    return {
        "user_id": "demo_user_123",
        "tier": current_tier,
        "status": "active",
        "started": "2025-09-25T00:00:00Z",
        "ends": "2025-10-25T00:00:00Z",
        "features": all_features
    }

# Demo AI feature endpoints

@app.post("/api/subscriptions/ai/generate-workout")
async def generate_ai_workout():
    """Demo AI workout generation"""
    if demo_data["current_tier"] == "free":
        raise HTTPException(status_code=403, detail="This feature requires a Premium subscription or higher")
    
    return {
        "workout": {
            "id": "ai_workout_demo_001",
            "name": "AI-Powered Intermediate Upper Body",
            "estimated_duration": 35,
            "difficulty": "intermediate", 
            "equipment_needed": ["dumbbells", "bodyweight"],
            "exercises": [
                {
                    "name": "Push-ups",
                    "sets": 3,
                    "reps": "12-15",
                    "rest_seconds": 60,
                    "form_tips": ["Keep core tight", "Full range of motion", "Control the descent"]
                },
                {
                    "name": "Dumbbell Rows", 
                    "sets": 3,
                    "reps": "10-12",
                    "rest_seconds": 60,
                    "form_tips": ["Squeeze shoulder blades", "Keep back straight", "Control the weight"]
                },
                {
                    "name": "Shoulder Press",
                    "sets": 3, 
                    "reps": "10-15",
                    "rest_seconds": 60,
                    "form_tips": ["Press straight up", "Keep core engaged", "Don't arch back"]
                }
            ],
            "ai_notes": [
                "Focus on controlled movements rather than speed",
                "Increase weight if completing all reps easily",
                "Rest 2-3 minutes between different exercises"
            ],
            "estimated_calories": 285
        },
        "tier_required": "premium"
    }

@app.post("/api/subscriptions/ai/analyze-progress")
async def analyze_progress():
    """Demo progress analysis"""
    if demo_data["current_tier"] == "free":
        raise HTTPException(status_code=403, detail="This feature requires a Premium subscription or higher")
    
    return {
        "analysis": {
            "total_workouts": 23,
            "avg_workout_duration": 32.4,
            "avg_calories_burned": 298.5,
            "recent_improvement": 12.3,
            "consistency_score": 87.5,
            "insights": [
                "Great progress! Your workout duration has increased by 12.3% recently.",
                "Excellent consistency! You complete 87% of your planned workouts."
            ],
            "recommendations": [
                "Consider adding more challenging exercises to continue progressing.",
                "Your consistency is excellent - maintain this momentum!"
            ]
        },
        "tier_required": "premium"
    }

@app.post("/api/subscriptions/ai/form-analysis")
async def analyze_workout_form():
    """Demo form analysis"""
    if demo_data["current_tier"] not in ["pro", "elite"]:
        raise HTTPException(status_code=403, detail="This feature requires a Pro subscription or higher")
    
    return {
        "analysis": {
            "form_score": 87,
            "injury_risk": 0.15,
            "recommendations": [
                "Focus on slower, controlled movements for Squats",
                "Keep your core engaged throughout the movement"
            ],
            "improvements": [
                "Work on hip mobility and ankle flexibility",
                "Practice the movement without weight first"
            ],
            "next_workout": {
                "focus_area": "form_improvement",
                "suggested_exercises": ["Squats"],
                "modifications": ["Work on hip mobility", "Practice bodyweight squats"]
            }
        },
        "tier_required": "pro"
    }

@app.post("/api/subscriptions/ai/voice-coaching")
async def create_voice_coaching():
    """Demo voice coaching"""
    if demo_data["current_tier"] != "elite":
        raise HTTPException(status_code=403, detail="This feature requires an Elite subscription")
    
    return {
        "coaching_session": {
            "session_id": "voice_coach_demo_001",
            "workout_name": "AI Coached Push-Up Challenge", 
            "total_duration": 300,
            "voice_cues": [
                {
                    "time_seconds": 0,
                    "message": "Starting Push-ups. Remember to focus on proper form.",
                    "type": "instruction"
                },
                {
                    "time_seconds": 30,
                    "message": "Great job! Keep your core engaged and maintain steady breathing.",
                    "type": "motivation"
                },
                {
                    "time_seconds": 60,
                    "message": "Excellent work! Take a 30-second rest.",
                    "type": "completion"
                }
            ],
            "motivation_messages": [
                "You're doing amazing! Every rep counts!",
                "Feel that strength building with each movement!",
                "Your dedication is paying off!"
            ]
        },
        "tier_required": "elite"
    }

# Demo upgrade endpoint
@app.post("/api/demo/simulate-upgrade")
async def simulate_upgrade(request: dict):
    """Simulate subscription upgrade"""
    tier = request.get("tier", "premium")
    
    if tier not in ["premium", "pro", "elite"]:
        raise HTTPException(status_code=400, detail="Invalid tier")
    
    demo_data["current_tier"] = tier
    price = demo_data["plans"][tier]["price"]
    
    return {
        "success": True,
        "message": f"Successfully upgraded to {tier.upper()} plan!",
        "tier": tier,
        "price": price,
        "effective_date": datetime.now().isoformat()
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Khyrie Subscription Demo",
        "timestamp": datetime.now().isoformat(),
        "current_tier": demo_data["current_tier"]
    }

if __name__ == "__main__":
    print("🚀 Starting Khyrie Subscription Demo Server...")
    print("💳 Features Available:")
    print("   - Interactive subscription pricing")
    print("   - Premium AI feature demos")
    print("   - Tier-based access control")
    print("   - Simulated payment flow")
    print()
    print("🔗 Demo URL: http://localhost:8080")
    print("📚 API Docs: http://localhost:8080/docs")
    print()
    print("💰 Subscription Tiers:")
    print("   🆓 Free: $0/month")
    print("   ⭐ Premium: $9.99/month")
    print("   🚀 Pro: $19.99/month")
    print("   🏆 Elite: $39.99/month")
    
    uvicorn.run(app, host="127.0.0.1", port=8080)