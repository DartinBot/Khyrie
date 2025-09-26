"""
Minimal Khyrie Subscription Demo Server
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime

app = FastAPI(title="Khyrie Subscription Demo")

# Demo data
demo_data = {"current_tier": "free"}

@app.get("/")
async def root():
    return {"message": "Khyrie Subscription Demo API", "status": "running"}

@app.get("/api/subscriptions/plans")
async def get_plans():
    plans = [
        {
            "tier": "free",
            "name": "Khyrie Free", 
            "price_monthly": 0,
            "features": ["Basic workout tracking", "Exercise library (50)", "Family group (3 members)"]
        },
        {
            "tier": "premium",
            "name": "Khyrie Premium",
            "price_monthly": 9.99,
            "features": ["AI workout generation", "Advanced analytics", "Unlimited family"]
        },
        {
            "tier": "pro", 
            "name": "Khyrie Pro",
            "price_monthly": 19.99,
            "features": ["Real-time form analysis", "Injury prediction", "Advanced AI coaching"]
        },
        {
            "tier": "elite",
            "name": "Khyrie Elite", 
            "price_monthly": 39.99,
            "features": ["AI voice coaching", "AR workouts", "Personal trainer sessions"]
        }
    ]
    return {"plans": plans}

@app.post("/api/subscriptions/create")
async def create_subscription(data: dict):
    tier = data.get("tier")
    if tier not in ["premium", "pro", "elite"]:
        raise HTTPException(status_code=400, detail="Invalid tier")
    
    demo_data["current_tier"] = tier
    return {
        "success": True,
        "tier": tier,
        "message": f"Successfully upgraded to {tier.title()}!"
    }

@app.get("/api/subscriptions/status")
async def get_status():
    return {
        "tier": demo_data["current_tier"],
        "status": "active",
        "features_available": demo_data["current_tier"] != "free"
    }

@app.post("/api/subscriptions/ai/generate-workout")
async def generate_workout():
    if demo_data["current_tier"] == "free":
        raise HTTPException(status_code=403, detail="Premium subscription required")
    
    return {
        "workout": {
            "name": "AI-Generated Upper Body",
            "exercises": ["Push-ups", "Dumbbell Rows", "Shoulder Press"],
            "duration": 35,
            "calories": 285
        }
    }

if __name__ == "__main__":
    print("🚀 Starting Khyrie Subscription Demo...")
    print("🔗 Demo URL: http://localhost:8080")
    print("💰 Tiers: Free ($0) | Premium ($9.99) | Pro ($19.99) | Elite ($39.99)")
    uvicorn.run(app, host="127.0.0.1", port=8080)