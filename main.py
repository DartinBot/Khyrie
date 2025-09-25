from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import local tools and modules
from fitness_tools import (
    create_server, ExerciseTools, SprintTools, CalisthenicsTools, 
    StrengthTools, WearableTools, NutritionTools, RecoveryTools, 
    PhysicalTherapyTools, SocialTools, AILangChainTools
)

# Import family & friends tools (local)
from family_friends_tools import FamilyFriendsTools

# Initialize FastAPI app
app = FastAPI(
    title="Fitness Web App API",
    description="REST API wrapper for 40 fitness MCP tools",
    version="1.0.0"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "fitness-web-app-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)