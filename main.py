#!/usr/bin/env python3
"""
Khyrie Fitness Platform - Main API Server
Copyright (C) 2025 Darnell Roy

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
import os
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.production' if os.getenv('ENVIRONMENT') == 'production' else '.env')

# Production settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Configure logging for production
if ENVIRONMENT == "production":
    logging.basicConfig(
        level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
else:
    logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Import local tools and modules
from fitness_tools import (
    create_server, ExerciseTools, SprintTools, CalisthenicsTools, 
    StrengthTools, WearableTools, NutritionTools, RecoveryTools, 
    PhysicalTherapyTools, SocialTools, AILangChainTools
)

# Import family & friends tools (local)
from family_friends_tools import FamilyFriendsTools

# Import advanced components
from advanced_workout_tools import AdvancedWorkoutTools
from comprehensive_fitness_models import ComprehensiveFitnessDatabase

# Initialize FastAPI app with production settings
app = FastAPI(
    title="Khyrie Fitness Platform",
    description="AI-Powered Family Fitness Platform",
    version="1.0.0",
    docs_url="/docs" if DEBUG else None,  # Hide docs in production
    redoc_url="/redoc" if DEBUG else None
)

# Production CORS settings
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
logger.info(f"Configuring CORS for origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Add security headers middleware for production
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    
    if ENVIRONMENT == "production":
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    return response

# Health check endpoint for monitoring
@app.get("/health")
async def health_check():
    """Health check endpoint for production monitoring."""
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "version": "1.0.0",
        "debug": DEBUG
    }



# Initialize MCP tool classes
exercise_tools = ExerciseTools()
sprint_tools = SprintTools()
calisthenics_tools = CalisthenicsTools()
strength_tools = StrengthTools()
wearable_tools = WearableTools()
nutrition_tools = NutritionTools()
recovery_tools = RecoveryTools()
pt_tools = PhysicalTherapyTools()
social_tools = SocialTools()
ai_tools = AILangChainTools()
family_tools = FamilyFriendsTools()

# Initialize advanced components
try:
    from database_migration import DatabaseMigrator
    migrator = DatabaseMigrator()
    migration_status = migrator.get_migration_status()
    
    if not migration_status["migration_complete"]:
        logger.info("Running database migration...")
        migrator.migrate_from_simple_db()
    
    advanced_workout_tools = AdvancedWorkoutTools()
    comprehensive_db = ComprehensiveFitnessDatabase()
    logger.info("Advanced components initialized successfully")
except Exception as e:
    logger.error(f"Error initializing advanced components: {e}")
    # Fallback to basic functionality
    advanced_workout_tools = None
    comprehensive_db = None

# Include subscription routes
try:
    from subscription_routes import router as subscription_router
    app.include_router(subscription_router)
    logger.info("Subscription routes loaded successfully")
except ImportError as e:
    logger.warning(f"Subscription routes not available: {e}")
except Exception as e:
    logger.error(f"Error loading subscription routes: {e}")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Fitness Web App API",
        "version": "1.0.0",
        "tools_available": 45,
        "domains": [
            "exercise_library",
            "sprint_training", 
            "calisthenics",
            "strength_training",
            "wearable_devices",
            "nutrition",
            "recovery",
            "physical_therapy",
            "social_features",
            "ai_recommendations"
        ]
    }

# Mount static files for PWA assets
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
if os.path.exists("icons"):
    app.mount("/icons", StaticFiles(directory="icons"), name="icons")

# PWA Routes for Mobile App
@app.get("/mobile")
async def mobile_app():
    """Serve mobile PWA landing page."""
    return FileResponse("mobile.html", media_type="text/html")

@app.get("/manifest.json")
async def pwa_manifest():
    """Serve PWA manifest with proper headers."""
    return FileResponse(
        "manifest.json", 
        media_type="application/manifest+json",
        headers={"Cache-Control": "no-cache"}
    )

@app.get("/sw.js")
async def service_worker():
    """Serve service worker with proper MIME type."""
    return FileResponse(
        "sw.js",
        media_type="application/javascript",
        headers={
            "Cache-Control": "no-cache",
            "Service-Worker-Allowed": "/"
        }
    )

@app.get("/ai_dashboard.html")
async def ai_dashboard():
    """Serve AI Dashboard with PWA support."""
    return FileResponse("ai_dashboard.html", media_type="text/html")

@app.get("/test_frontend.html")
async def test_frontend():
    """Serve test frontend with PWA support."""
    return FileResponse("test_frontend.html", media_type="text/html")

@app.get("/dashboard")
async def dashboard_shortcut():
    """Shortcut to AI Dashboard."""
    return FileResponse("ai_dashboard.html", media_type="text/html")

@app.get("/test")
async def test_shortcut():
    """Shortcut to test frontend."""
    return FileResponse("test_frontend.html", media_type="text/html")

# Exercise & Workout Routes
@app.get("/api/exercises")
async def get_exercises(category: str = None, muscle_group: str = None):
    """Get exercise library with optional filtering."""
    try:
        result = await exercise_tools.get_exercises(category, muscle_group)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/exercises/{exercise_id}")
async def get_exercise(exercise_id: str):
    """Get specific exercise details."""
    try:
        result = await exercise_tools.get_exercise(exercise_id)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Exercise not found")

@app.post("/api/workouts/sprint")
async def create_sprint_workout(workout_data: dict):
    """Create custom sprint workout."""
    try:
        result = await sprint_tools.create_sprint_workout(workout_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workouts/calisthenics")
async def generate_calisthenics_workout(workout_data: dict):
    """Generate calisthenics workout."""
    try:
        result = await calisthenics_tools.generate_calisthenics_workout(workout_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Strength Training Routes
@app.post("/api/strength/1rm-calculator")
async def calculate_1rm(calculation_data: dict):
    """Calculate estimated 1RM from submaximal lifts."""
    try:
        result = await strength_tools.calculate_1rm(calculation_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/strength/program")
async def create_strength_program(program_data: dict):
    """Create comprehensive strength training program."""
    try:
        result = await strength_tools.create_strength_program(program_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/strength/periodization")
async def generate_periodization_plan(plan_data: dict):
    """Generate periodized training plan."""
    try:
        result = await strength_tools.generate_periodization_plan(plan_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/strength/progress")
async def track_strength_progress(user_id: str, exercise: str = "back_squat", time_period: str = "12_weeks"):
    """Track and analyze strength training progress."""
    try:
        result = await strength_tools.track_strength_progress({
            "user_id": user_id,
            "exercise": exercise,
            "time_period": time_period
        })
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/strength/exercises")
async def get_strength_exercise_library(category: str = None, muscle_group: str = None, difficulty: str = None):
    """Get comprehensive strength exercise library."""
    try:
        result = await strength_tools.get_exercise_library({
            "category": category,
            "muscle_group": muscle_group,
            "difficulty": difficulty
        })
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Recovery Routes
@app.get("/api/recovery/assessment")
async def get_recovery_assessment(user_id: str):
    """Get recovery readiness assessment."""
    try:
        result = await recovery_tools.assess_recovery_readiness({
            "user_id": user_id,
            "include_recommendations": True
        })
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recovery/workout")
async def generate_recovery_workout(workout_request: dict):
    """Generate active recovery workout."""
    try:
        result = await recovery_tools.generate_active_recovery_workout(workout_request)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recovery/protocols")
async def get_recovery_protocols():
    """Get evidence-based recovery protocols."""
    try:
        result = await recovery_tools.get_recovery_protocols({})
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Wearable Device Routes
@app.get("/api/wearables/connections")
async def get_wearable_connections(user_id: str):
    """Get user's wearable device connections."""
    try:
        result = await wearable_tools.get_wearable_connections({"user_id": user_id})
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/wearables/sync")
async def sync_wearable_data(sync_request: dict):
    """Sync data from wearable devices."""
    try:
        result = await wearable_tools.sync_wearable_data(sync_request)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/wearables/data/{data_type}")
async def get_wearable_data(data_type: str, user_id: str, days: int = 7):
    """Get historical wearable data."""
    try:
        result = await wearable_tools.get_wearable_data({
            "user_id": user_id,
            "data_type": data_type,
            "days": days
        })
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Nutrition Routes
@app.get("/api/nutrition/meals")
async def get_meal_plans(user_id: str):
    """Get personalized meal plans."""
    try:
        result = await nutrition_tools.get_meal_plans({"user_id": user_id})
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/nutrition/log")
async def log_meal(meal_data: dict):
    """Log a meal entry."""
    try:
        result = await nutrition_tools.log_meal(meal_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nutrition/analytics/{user_id}")
async def get_nutrition_analytics(user_id: str, period: str = "week"):
    """Get nutrition analytics and trends."""
    try:
        result = await nutrition_tools.get_nutrition_analytics({
            "user_id": user_id,
            "period": period
        })
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Physical Therapy Routes
@app.post("/api/pt/assessment")
async def create_pt_assessment(assessment_data: dict):
    """Create physical therapy assessment."""
    try:
        result = await pt_tools.create_pt_assessment(assessment_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pt/session")
async def log_pt_session(session_data: dict):
    """Log physical therapy session."""
    try:
        result = await pt_tools.log_pt_session(session_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Social Routes
@app.get("/api/social/feed/{user_id}")
async def get_social_feed(user_id: str):
    """Get user's social feed."""
    try:
        result = await social_tools.get_social_feed({"user_id": user_id})
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/social/post")
async def create_social_post(post_data: dict):
    """Create social media post."""
    try:
        result = await social_tools.create_social_post(post_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI Recommendation Routes
@app.post("/api/ai/workout-recommendation")
async def get_workout_recommendation(user_profile: dict):
    """Get AI-powered workout recommendation."""
    try:
        result = await ai_tools.get_workout_recommendation(user_profile)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/training-analysis") 
async def analyze_training_data(analysis_request: dict):
    """Analyze training data with AI insights."""
    try:
        result = await ai_tools.analyze_training_data(analysis_request)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Family & Friends Routes
@app.post("/api/family-friends/groups/create")
async def create_fitness_group(group_data: dict):
    """Create a new family or friends fitness group."""
    try:
        result = await family_tools.create_fitness_group(group_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/family-friends/groups/join")
async def join_fitness_group(join_data: dict):
    """Join an existing fitness group via invite code."""
    try:
        result = await family_tools.join_fitness_group(join_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/groups/user/{user_id}")
async def get_user_groups(user_id: str):
    """Get all groups for a specific user."""
    try:
        user_groups = []
        for group_id, group in family_tools.groups_database.items():
            if any(m["user_id"] == user_id for m in group.members):
                user_groups.append({
                    "group_id": group_id,
                    "name": group.name,
                    "type": group.group_type,
                    "member_count": len(group.members),
                    "role": next(m["role"] for m in group.members if m["user_id"] == user_id),
                    "created_date": group.created_date
                })
        return {"user_groups": user_groups}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/family-friends/workouts/shared/create")
async def create_shared_workout(workout_data: dict):
    """Create a workout that can be shared with family/friends."""
    try:
        result = await family_tools.create_shared_workout(workout_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/workouts/shared/group/{group_id}")
async def get_group_shared_workouts(group_id: str):
    """Get all shared workouts for a specific group."""
    try:
        group_workouts = []
        for workout_id, workout in family_tools.shared_workouts.items():
            if group_id in workout.group_ids:
                group_workouts.append({
                    "workout_id": workout_id,
                    "name": workout.name,
                    "type": workout.workout_type,
                    "difficulty": workout.difficulty_level,
                    "duration": workout.estimated_duration,
                    "creator_id": workout.creator_id,
                    "created_date": workout.created_date,
                    "exercise_count": len(workout.exercises)
                })
        return {"group_workouts": group_workouts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/family-friends/sessions/start")
async def start_group_workout_session(session_data: dict):
    """Start a workout session that will be tracked with family/friends."""
    try:
        result = await family_tools.start_group_workout_session(session_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/family-friends/sessions/complete")
async def complete_workout_session(session_data: dict):
    """Complete a workout session and share results with groups."""
    try:
        result = await family_tools.complete_workout_session(session_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/family-friends/challenges/create")
async def create_group_challenge(challenge_data: dict):
    """Create a fitness challenge for family/friends groups."""
    try:
        result = await family_tools.create_group_challenge(challenge_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/challenges/group/{group_id}")
async def get_group_challenges(group_id: str, active_only: bool = True):
    """Get all challenges for a specific group."""
    try:
        group_challenges = []
        for challenge_id, challenge in family_tools.group_challenges.items():
            if challenge.group_id == group_id:
                if not active_only or challenge.is_active:
                    from datetime import datetime
                    end_date = datetime.fromisoformat(challenge.end_date)
                    days_remaining = max(0, (end_date - datetime.now()).days)
                    
                    group_challenges.append({
                        "challenge_id": challenge_id,
                        "name": challenge.name,
                        "type": challenge.challenge_type,
                        "days_remaining": days_remaining,
                        "participant_count": len(challenge.participants),
                        "is_active": challenge.is_active,
                        "start_date": challenge.start_date,
                        "end_date": challenge.end_date
                    })
        return {"group_challenges": group_challenges}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/dashboard/{user_id}")
async def get_family_friends_dashboard(user_id: str):
    """Get comprehensive dashboard for family/friends fitness tracking."""
    try:
        result = await family_tools.get_family_friends_dashboard({"user_id": user_id})
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/groups/{group_id}/activity")
async def get_group_activity_feed(group_id: str, limit: int = 20):
    """Get recent activity feed for a group."""
    try:
        if group_id not in family_tools.groups_database:
            raise HTTPException(status_code=404, detail="Group not found")
        
        activities = family_tools._get_group_recent_activity(group_id)
        
        detailed_activities = []
        for activity in activities[:limit]:
            detailed_activities.append({
                **activity,
                "user_name": f"User {activity['user_id']}",
                "activity_description": activity.get("activity", "activity"),
                "relative_time": "recently"
            })
        
        return {
            "group_id": group_id,
            "activities": detailed_activities,
            "total_activities": len(activities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# FITNESS TOOL API ENDPOINTS - Integrated from external main.py
# =============================================================================

# Exercise Routes
@app.post("/api/exercises/suggestions")
async def get_exercise_suggestions(request_data: dict):
    """Get exercise suggestions based on criteria."""
    try:
        result = exercise_tools.get_exercise_suggestions(
            request_data.get("muscle_group", "all"),
            request_data.get("equipment", "any")
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/exercises/workout")
async def create_custom_workout(workout_data: dict):
    """Create custom workout based on preferences."""
    try:
        # Use placeholder implementation from fitness_tools
        result = {
            "workout_id": f"workout_{int(datetime.utcnow().timestamp())}",
            "name": workout_data.get("name", "Custom Workout"),
            "exercises": exercise_tools.get_exercise_suggestions()["exercises"],
            "duration": workout_data.get("duration", 45),
            "difficulty": workout_data.get("difficulty", "intermediate")
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sprint Training Routes
@app.post("/api/workouts/sprint")
async def create_sprint_workout(workout_data: dict):
    """Create sprint workout based on fitness level."""
    try:
        result = sprint_tools.get_sprint_workout(workout_data.get("level", "beginner"))
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Calisthenics Routes
@app.post("/api/workouts/calisthenics")
async def generate_calisthenics_workout(workout_data: dict):
    """Generate calisthenics workout."""
    try:
        result = calisthenics_tools.get_bodyweight_routine(workout_data.get("difficulty", "intermediate"))
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Strength Training Routes
@app.post("/api/strength/1rm-calculator")
async def calculate_1rm(calculation_data: dict):
    """Calculate estimated 1RM from submaximal lifts."""
    try:
        weight = calculation_data.get("weight", 100)
        reps = calculation_data.get("reps", 5)
        
        # Epley formula: 1RM = weight × (1 + reps/30)
        estimated_1rm = weight * (1 + reps / 30)
        
        result = {
            "weight_used": weight,
            "reps_performed": reps,
            "estimated_1rm": round(estimated_1rm, 1),
            "formula_used": "Epley",
            "confidence": "high" if reps <= 10 else "moderate"
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/strength/program")
async def create_strength_program(program_data: dict):
    """Create comprehensive strength training program."""
    try:
        result = {
            "program_id": f"strength_{int(datetime.utcnow().timestamp())}",
            "name": program_data.get("name", "Strength Program"),
            "duration_weeks": program_data.get("weeks", 12),
            "frequency": program_data.get("frequency", 3),
            "focus": program_data.get("focus", "general_strength"),
            "exercises": [
                {"name": "Squat", "sets": 3, "reps": "5-8", "intensity": "80-85%"},
                {"name": "Bench Press", "sets": 3, "reps": "5-8", "intensity": "80-85%"},
                {"name": "Deadlift", "sets": 3, "reps": "3-5", "intensity": "85-90%"},
                {"name": "Overhead Press", "sets": 3, "reps": "6-10", "intensity": "75-80%"}
            ]
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/strength/exercises")
async def get_strength_exercise_library(category: str = None, muscle_group: str = None, difficulty: str = None):
    """Get comprehensive strength exercise library."""
    try:
        exercises = [
            {"name": "Back Squat", "category": "compound", "muscle_group": "legs", "difficulty": "intermediate"},
            {"name": "Bench Press", "category": "compound", "muscle_group": "chest", "difficulty": "beginner"},
            {"name": "Deadlift", "category": "compound", "muscle_group": "back", "difficulty": "advanced"},
            {"name": "Pull-up", "category": "compound", "muscle_group": "back", "difficulty": "intermediate"},
            {"name": "Push-up", "category": "bodyweight", "muscle_group": "chest", "difficulty": "beginner"}
        ]
        
        # Filter exercises based on parameters
        filtered_exercises = exercises
        if category:
            filtered_exercises = [e for e in filtered_exercises if e["category"] == category]
        if muscle_group:
            filtered_exercises = [e for e in filtered_exercises if e["muscle_group"] == muscle_group]
        if difficulty:
            filtered_exercises = [e for e in filtered_exercises if e["difficulty"] == difficulty]
        
        result = {
            "exercises": filtered_exercises,
            "total": len(filtered_exercises),
            "filters": {"category": category, "muscle_group": muscle_group, "difficulty": difficulty}
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Recovery Routes
@app.get("/api/recovery/assessment")
async def get_recovery_assessment(user_id: str):
    """Get recovery readiness assessment."""
    try:
        result = {
            "user_id": user_id,
            "recovery_score": 7.5,
            "sleep_quality": 8.0,
            "heart_rate_variability": 42,
            "perceived_exertion": 6,
            "recommendations": [
                "Good recovery status - ready for moderate intensity training",
                "Consider light stretching or mobility work",
                "Maintain current sleep schedule"
            ],
            "assessment_date": datetime.utcnow().isoformat()
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recovery/workout")
async def generate_recovery_workout(workout_request: dict):
    """Generate active recovery workout."""
    try:
        intensity = workout_request.get("intensity", "low")
        duration = workout_request.get("duration", 30)
        
        result = {
            "workout_type": "active_recovery",
            "intensity": intensity,
            "duration_minutes": duration,
            "exercises": [
                {"name": "Light walking", "duration": "10 min", "intensity": "low"},
                {"name": "Dynamic stretching", "duration": "10 min", "intensity": "low"},
                {"name": "Foam rolling", "duration": "10 min", "intensity": "light pressure"}
            ],
            "notes": "Focus on movement quality and relaxation"
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recovery/protocols")
async def get_recovery_protocols():
    """Get evidence-based recovery protocols."""
    try:
        result = {
            "protocols": [
                {
                    "name": "Sleep Optimization",
                    "description": "7-9 hours of quality sleep",
                    "evidence": "Grade A",
                    "implementation": ["Consistent sleep schedule", "Cool room temperature", "Limit screens before bed"]
                },
                {
                    "name": "Active Recovery",
                    "description": "Light movement on rest days",
                    "evidence": "Grade B",
                    "implementation": ["20-30 min walks", "Gentle yoga", "Swimming at easy pace"]
                },
                {
                    "name": "Nutrition Timing",
                    "description": "Post-workout nutrition within 2 hours",
                    "evidence": "Grade A",
                    "implementation": ["Protein + carbs combo", "Adequate hydration", "Anti-inflammatory foods"]
                }
            ]
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Nutrition Routes
@app.post("/api/nutrition/meal-plan")
async def create_nutrition_plan(nutrition_data: dict):
    """Create personalized nutrition plan."""
    try:
        goals = nutrition_data.get("goals", ["general_health"])
        calories = nutrition_data.get("target_calories", 2000)
        
        result = {
            "plan_id": f"nutrition_{int(datetime.utcnow().timestamp())}",
            "daily_calories": calories,
            "macros": {
                "protein": f"{int(calories * 0.25 / 4)}g (25%)",
                "carbs": f"{int(calories * 0.45 / 4)}g (45%)",
                "fats": f"{int(calories * 0.30 / 9)}g (30%)"
            },
            "meal_suggestions": [
                {"meal": "Breakfast", "calories": int(calories * 0.25)},
                {"meal": "Lunch", "calories": int(calories * 0.35)},
                {"meal": "Dinner", "calories": int(calories * 0.30)},
                {"meal": "Snacks", "calories": int(calories * 0.10)}
            ],
            "goals": goals
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Wearable Device Routes
@app.get("/api/wearables/connections")
async def get_wearable_connections(user_id: str):
    """Get connected wearable devices."""
    try:
        result = {
            "user_id": user_id,
            "connected_devices": [
                {"device": "Apple Watch", "status": "connected", "last_sync": "2024-01-15T10:30:00Z"},
                {"device": "Fitbit", "status": "disconnected", "last_sync": "2024-01-10T08:15:00Z"}
            ],
            "available_integrations": ["Apple Health", "Google Fit", "Garmin Connect", "Strava"]
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Physical Therapy Routes
@app.post("/api/physical-therapy/assessment")
async def create_pt_assessment(assessment_data: dict):
    """Create physical therapy assessment."""
    try:
        pain_areas = assessment_data.get("pain_areas", [])
        pain_level = assessment_data.get("pain_level", 0)
        
        result = {
            "assessment_id": f"pt_{int(datetime.utcnow().timestamp())}",
            "pain_areas": pain_areas,
            "pain_level": pain_level,
            "recommendations": [
                "Consult with healthcare provider for persistent pain",
                "Focus on mobility and gentle movement",
                "Avoid exercises that increase pain"
            ],
            "exercises": [
                {"name": "Gentle range of motion", "sets": 2, "reps": 10},
                {"name": "Isometric holds", "sets": 3, "duration": "10 seconds"}
            ]
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Social & AI Routes
@app.get("/api/social/leaderboard")
async def get_social_leaderboard(category: str = "steps", period: str = "week"):
    """Get social fitness leaderboard."""
    try:
        result = {
            "category": category,
            "period": period,
            "leaderboard": [
                {"rank": 1, "user": "FitnessFan123", "value": 85420, "unit": "steps"},
                {"rank": 2, "user": "RunnerGirl", "value": 78350, "unit": "steps"},
                {"rank": 3, "user": "StrengthSeeker", "value": 72100, "unit": "steps"}
            ],
            "user_rank": 15,
            "user_value": 65200
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===============================
# FAMILY & FRIENDS SOCIAL ROUTES
# ===============================

@app.post("/api/family-friends/groups/create")
async def create_fitness_group(group_data: dict):
    """Create a new family or friends fitness group."""
    try:
        result = family_tools.create_fitness_group(group_data)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error creating fitness group: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/family-friends/groups/join")
async def join_fitness_group(join_data: dict):
    """Join an existing fitness group via invite code."""
    try:
        result = family_tools.join_fitness_group(join_data)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error joining fitness group: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/groups/user/{user_id}")
async def get_user_groups(user_id: str):
    """Get all groups for a specific user."""
    try:
        user_groups = []
        for group_id, group in family_tools.groups_database.items():
            if any(m["user_id"] == user_id for m in group.members):
                user_groups.append({
                    "group_id": group_id,
                    "name": group.name,
                    "type": group.group_type,
                    "member_count": len(group.members),
                    "role": next(m["role"] for m in group.members if m["user_id"] == user_id),
                    "created_date": group.created_date,
                    "invite_code": group.invite_code
                })
        return {"user_groups": user_groups}
    except Exception as e:
        logger.error(f"Error getting user groups: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/family-friends/challenges/create")
async def create_group_challenge(challenge_data: dict):
    """Create a fitness challenge for family/friends groups."""
    try:
        result = family_tools.create_group_challenge(challenge_data)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error creating group challenge: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/challenges/group/{group_id}")
async def get_group_challenges(group_id: str, active_only: bool = True):
    """Get all challenges for a specific group."""
    try:
        group_challenges = []
        for challenge_id, challenge in family_tools.group_challenges.items():
            if challenge.group_id == group_id:
                if not active_only or challenge.is_active:
                    from datetime import datetime
                    end_date = datetime.fromisoformat(challenge.end_date)
                    days_remaining = max(0, (end_date - datetime.now()).days)
                    
                    group_challenges.append({
                        "challenge_id": challenge_id,
                        "name": challenge.name,
                        "type": challenge.challenge_type,
                        "days_remaining": days_remaining,
                        "participant_count": len(challenge.participants),
                        "is_active": challenge.is_active,
                        "start_date": challenge.start_date,
                        "end_date": challenge.end_date
                    })
        return {"group_challenges": group_challenges}
    except Exception as e:
        logger.error(f"Error getting group challenges: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/dashboard/{user_id}")
async def get_family_friends_dashboard(user_id: str):
    """Get comprehensive dashboard for family/friends fitness tracking."""
    try:
        result = family_tools.get_family_friends_dashboard({"user_id": user_id})
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error getting family friends dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/groups/{group_id}/activity")
async def get_group_activity_feed(group_id: str, limit: int = 20):
    """Get recent activity feed for a group."""
    try:
        if group_id not in family_tools.groups_database:
            raise HTTPException(status_code=404, detail="Group not found")
        
        activities = family_tools._get_group_recent_activity(group_id)
        
        detailed_activities = []
        for activity in activities[:limit]:
            detailed_activities.append({
                **activity,
                "user_name": f"User {activity['user_id']}",
                "activity_description": activity.get("activity", "activity"),
                "relative_time": "recently"
            })
        
        return {
            "group_id": group_id,
            "activities": detailed_activities,
            "total_activities": len(activities)
        }
    except Exception as e:
        logger.error(f"Error getting group activity feed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/recommendations")
async def get_ai_recommendations(request_data: dict):
    """Get AI-powered fitness recommendations."""
    try:
        user_id = request_data.get("user_id")
        preferences = request_data.get("preferences", {})
        
        result = {
            "user_id": user_id,
            "recommendations": [
                {
                    "type": "workout",
                    "title": "Upper Body Strength Focus",
                    "description": "Based on your recent lower body sessions, consider upper body work",
                    "confidence": 0.85
                },
                {
                    "type": "recovery",
                    "title": "Active Recovery Recommended",
                    "description": "Your intensity has been high - consider a light day",
                    "confidence": 0.92
                }
            ],
            "personalization_factors": ["workout_history", "recovery_metrics", "stated_goals"]
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===============================
# ADVANCED WORKOUT ENDPOINTS
# ===============================

@app.post("/api/advanced/programs/create")
async def create_workout_program(request_data: dict):
    """Create a comprehensive workout program."""
    if not advanced_workout_tools:
        raise HTTPException(status_code=503, detail="Advanced workout tools not available")
    try:
        result = advanced_workout_tools.create_workout_program(
            creator_id=request_data.get("creator_id"),
            name=request_data.get("name"),
            description=request_data.get("description"),
            duration_weeks=request_data.get("duration_weeks", 8),
            frequency_per_week=request_data.get("frequency_per_week", 3),
            difficulty_level=request_data.get("difficulty_level", "intermediate"),
            goals=request_data.get("goals", ["strength"]),
            exercises=request_data.get("exercises", []),
            progression_scheme=request_data.get("progression_scheme", {})
        )
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error creating workout program: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/advanced/programs/generate")
async def generate_adaptive_program(request_data: dict):
    """Generate AI-powered adaptive workout program."""
    try:
        result = advanced_workout_tools.generate_adaptive_program(
            user_id=request_data.get("user_id"),
            goals=request_data.get("goals", ["strength"]),
            available_days=request_data.get("available_days", 3),
            session_length=request_data.get("session_length", 60)
        )
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error generating adaptive program: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/advanced/strength/standards/{user_id}/{exercise_id}")
async def get_strength_standards(user_id: str, exercise_id: str):
    """Calculate strength standards and percentiles."""
    try:
        result = advanced_workout_tools.calculate_strength_standards(user_id, exercise_id)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error calculating strength standards: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/advanced/analytics/trends/{user_id}")
async def get_workout_trends(user_id: str, days: int = 90):
    """Get comprehensive workout trend analysis."""
    try:
        result = advanced_workout_tools.analyze_workout_trends(user_id, days)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error analyzing workout trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/advanced/ai/recommendations/{user_id}")
async def get_ai_workout_recommendations(user_id: str):
    """Get AI-powered workout recommendations."""
    try:
        result = advanced_workout_tools.generate_ai_workout_recommendation(user_id)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error generating AI recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/advanced/injury/risk/{user_id}")
async def get_injury_risk_assessment(user_id: str):
    """Get AI-powered injury risk prediction."""
    try:
        result = advanced_workout_tools.predict_injury_risk(user_id)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error predicting injury risk: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/advanced/analytics/user/{user_id}")
async def get_comprehensive_user_analytics(user_id: str, days: int = 30):
    """Get comprehensive user analytics from advanced database."""
    try:
        result = comprehensive_db.get_user_analytics(user_id, days)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error getting user analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===============================
# DATABASE MANAGEMENT ENDPOINTS
# ===============================

@app.get("/api/database/status")
async def get_database_status():
    """Get current database status and migration information."""
    try:
        if 'migrator' in globals():
            status = migrator.get_migration_status()
            return JSONResponse(content=status)
        else:
            return JSONResponse(content={
                "error": "Database migrator not available",
                "basic_functionality": True
            })
    except Exception as e:
        logger.error(f"Error getting database status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/database/migrate")
async def run_database_migration():
    """Manually trigger database migration."""
    try:
        if 'migrator' not in globals():
            raise HTTPException(status_code=503, detail="Database migrator not available")
        
        migrator.migrate_from_simple_db()
        status = migrator.get_migration_status()
        
        return JSONResponse(content={
            "migration_completed": True,
            "status": status
        })
    except Exception as e:
        logger.error(f"Error running database migration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/database/initialize")
async def initialize_fresh_database():
    """Initialize fresh database with sample data."""
    try:
        if 'migrator' not in globals():
            raise HTTPException(status_code=503, detail="Database migrator not available")
        
        migrator.initialize_fresh_database()
        status = migrator.get_migration_status()
        
        return JSONResponse(content={
            "initialization_completed": True,
            "status": status
        })
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Subscription page endpoint
@app.get("/subscription")
async def subscription_page():
    """Serve subscription pricing page."""
    return FileResponse("subscription.html")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "fitness-web-app-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)