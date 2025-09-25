from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os
from pathlib import Path

# Add the parent directory to Python path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

# Simple mock classes to avoid complex dependencies for testing
class MockTools:
    """Mock implementation for testing family & friends functionality"""
    
    def __init__(self):
        self.groups_database = {
            "group_1": {
                "name": "Family Fitness",
                "group_type": "family",
                "members": [
                    {"user_id": "user123", "role": "admin"},
                    {"user_id": "user456", "role": "member"}
                ],
                "created_date": "2024-01-01"
            }
        }
        self.shared_workouts = {}
        self.group_challenges = {}
        
    async def create_fitness_group(self, data):
        return {
            "group_created": True,
            "group_id": "new_group_123",
            "invite_code": "FAMILY2024",
            "message": "Family fitness group created successfully!"
        }
    
    async def join_fitness_group(self, data):
        return {
            "joined": True,
            "group_name": "Family Fitness",
            "message": "Successfully joined the group!"
        }
    
    async def create_shared_workout(self, data):
        return {
            "workout_created": True,
            "workout_id": "workout_123",
            "message": "Shared workout created!"
        }
    
    async def start_group_workout_session(self, data):
        return {
            "session_started": True,
            "session_id": "session_123",
            "message": "Workout session started!"
        }
    
    async def complete_workout_session(self, data):
        return {
            "session_completed": True,
            "achievements": ["First workout of the week!"],
            "message": "Workout completed!"
        }
    
    async def create_group_challenge(self, data):
        return {
            "challenge_created": True,
            "challenge_id": "challenge_123",
            "message": "Group challenge created!"
        }
    
    async def get_family_friends_dashboard(self, data):
        return {
            "dashboard_data": {
                "user_groups": ["Family Fitness", "Running Buddies"],
                "active_challenges": [
                    {"id": "1", "name": "30-Day Step Challenge", "days_remaining": 12, "participant_count": 15}
                ],
                "recent_workouts": ["Morning Run", "Strength Training"],
                "weekly_stats": {
                    "workouts_completed": 4,
                    "total_minutes": 240,
                    "calories_burned": 1200
                }
            }
        }
    
    def _get_group_recent_activity(self, group_id):
        return [
            {
                "id": "1",
                "user_id": "user456",
                "activity": "workout_completed",
                "details": "Morning Run",
                "timestamp": "2024-01-15T10:00:00"
            },
            {
                "id": "2", 
                "user_id": "user789",
                "activity": "challenge_joined",
                "details": "30-Day Step Challenge",
                "timestamp": "2024-01-15T09:00:00"
            }
        ]

# Initialize FastAPI app
app = FastAPI(
    title="Family & Friends Fitness API (Simple)",
    description="Simplified API for testing family & friends integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize mock family tools
family_tools = MockTools()

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Family & Friends Fitness API (Simple Test Version)",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": [
            "/api/family-friends/groups/create",
            "/api/family-friends/groups/join", 
            "/api/family-friends/groups/user/{user_id}",
            "/api/family-friends/dashboard/{user_id}"
        ]
    }

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
            if any(m["user_id"] == user_id for m in group["members"]):
                user_groups.append({
                    "group_id": group_id,
                    "name": group["name"],
                    "type": group["group_type"],
                    "member_count": len(group["members"]),
                    "role": next(m["role"] for m in group["members"] if m["user_id"] == user_id),
                    "created_date": group["created_date"]
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
        # Mock data for testing
        group_workouts = [
            {
                "workout_id": "workout_1",
                "name": "Family Morning Routine",
                "type": "cardio",
                "difficulty": "beginner",
                "duration": 30,
                "creator_id": "user123",
                "created_date": "2024-01-10",
                "exercise_count": 5
            }
        ]
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
        # Mock challenges data
        group_challenges = [
            {
                "challenge_id": "challenge_1",
                "name": "30-Day Step Challenge",
                "type": "step_count",
                "days_remaining": 12,
                "participant_count": 5,
                "is_active": True,
                "start_date": "2024-01-01",
                "end_date": "2024-01-31"
            }
        ]
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
        activities = family_tools._get_group_recent_activity(group_id)
        
        detailed_activities = []
        for activity in activities[:limit]:
            detailed_activities.append({
                **activity,
                "user_name": f"User {activity['user_id']}",
                "activity_description": f"{activity['activity']} - {activity['details']}",
                "relative_time": "recently"
            })
        
        return {
            "group_id": group_id,
            "activities": detailed_activities,
            "total_activities": len(activities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "family-friends-api-simple"}

if __name__ == "__main__":
    import uvicorn
    print("Starting Family & Friends Fitness API on http://localhost:8000")
    print("API Docs available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)