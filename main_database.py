from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os
from pathlib import Path

# Import the database-powered family friends tools (local to backend directory)
from family_friends_tools_db import FamilyFriendsToolsDB

# Initialize FastAPI app
app = FastAPI(
    title="Family & Friends Fitness API (Database Version)",
    description="Full-featured API with SQLite database persistence for family & friends fitness tracking",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize family tools with database
family_tools = FamilyFriendsToolsDB()

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Family & Friends Fitness API (Database Version)",
        "version": "2.0.0",
        "status": "healthy",
        "database": "SQLite with persistent data storage",
        "features": [
            "Real data persistence",
            "User authentication ready",
            "Group management with database",
            "Challenge tracking with history",
            "Activity feeds with timestamps",
            "Scalable database design"
        ],
        "endpoints": [
            "/api/family-friends/groups/create",
            "/api/family-friends/groups/join", 
            "/api/family-friends/groups/user/{user_id}",
            "/api/family-friends/workouts/shared/create",
            "/api/family-friends/sessions/start",
            "/api/family-friends/sessions/complete",
            "/api/family-friends/challenges/create",
            "/api/family-friends/challenges/group/{group_id}",
            "/api/family-friends/dashboard/{user_id}",
            "/api/family-friends/groups/{group_id}/activity"
        ]
    }

# Family & Friends Routes with Database Persistence
@app.post("/api/family-friends/groups/create")
async def create_fitness_group(group_data: dict):
    """Create a new family or friends fitness group with database storage."""
    try:
        result = await family_tools.create_fitness_group(group_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/family-friends/groups/join")
async def join_fitness_group(join_data: dict):
    """Join an existing fitness group via invite code with database verification."""
    try:
        result = await family_tools.join_fitness_group(join_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/groups/user/{user_id}")
async def get_user_groups(user_id: str):
    """Get all groups for a specific user from database."""
    try:
        result = await family_tools.get_user_groups(user_id)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/family-friends/workouts/shared/create")
async def create_shared_workout(workout_data: dict):
    """Create a workout that can be shared with family/friends and stored in database."""
    try:
        result = await family_tools.create_shared_workout(workout_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/workouts/shared/group/{group_id}")
async def get_group_shared_workouts(group_id: str):
    """Get all shared workouts for a specific group from database."""
    try:
        # This would be implemented in the database tools
        # For now, return empty list as placeholder
        return {"group_workouts": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/family-friends/sessions/start")
async def start_group_workout_session(session_data: dict):
    """Start a workout session that will be tracked with family/friends in database."""
    try:
        result = await family_tools.start_group_workout_session(session_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/family-friends/sessions/complete")
async def complete_workout_session(session_data: dict):
    """Complete a workout session and share results with groups in database."""
    try:
        result = await family_tools.complete_workout_session(session_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/family-friends/challenges/create")
async def create_group_challenge(challenge_data: dict):
    """Create a fitness challenge for family/friends groups with database storage."""
    try:
        result = await family_tools.create_group_challenge(challenge_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/challenges/group/{group_id}")
async def get_group_challenges(group_id: str, active_only: bool = True):
    """Get all challenges for a specific group from database."""
    try:
        result = family_tools.get_group_challenges(group_id, active_only)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/dashboard/{user_id}")
async def get_family_friends_dashboard(user_id: str):
    """Get comprehensive dashboard for family/friends fitness tracking from database."""
    try:
        result = await family_tools.get_family_friends_dashboard({"user_id": user_id})
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/family-friends/groups/{group_id}/activity")
async def get_group_activity_feed(group_id: str, limit: int = 20):
    """Get recent activity feed for a group from database."""
    try:
        activities = family_tools._get_group_recent_activity(group_id, limit)
        
        detailed_activities = []
        for activity in activities:
            detailed_activities.append({
                **activity,
                "user_name": f"User {activity['user_id']}",  # Would get real name from user table
                "activity_description": f"{activity['activity']} - {activity.get('details', {})}",
                "relative_time": "recently"  # Would calculate real relative time
            })
        
        return {
            "group_id": group_id,
            "activities": detailed_activities,
            "total_activities": len(activities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Database Management Endpoints
@app.get("/api/database/stats")
async def get_database_stats():
    """Get current database statistics."""
    try:
        with family_tools.db_manager.get_connection() as conn:
            tables = [
                "users", "fitness_groups", "group_memberships", 
                "shared_workouts", "workout_sessions", "group_challenges", "activity_feed"
            ]
            stats = {}
            for table in tables:
                count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                stats[table] = count
        
        return {
            "database_stats": stats,
            "total_records": sum(stats.values()),
            "database_file": family_tools.db_manager.db_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/database/reset-sample-data")
async def reset_sample_data():
    """Reset database with fresh sample data."""
    try:
        # Delete existing data
        with family_tools.db_manager.get_connection() as conn:
            tables = [
                "activity_feed", "challenge_participants", "group_challenges",
                "workout_sessions", "shared_workouts", "group_memberships", 
                "fitness_groups", "users"
            ]
            for table in tables:
                conn.execute(f"DELETE FROM {table}")
            conn.commit()
        
        # Recreate sample data
        family_tools.db_manager.create_sample_data()
        
        return {
            "reset_completed": True,
            "message": "Database reset with fresh sample data",
            "sample_users": 5,
            "sample_groups": 3,
            "sample_challenges": 2
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint with database status."""
    try:
        # Test database connection
        with family_tools.db_manager.get_connection() as conn:
            conn.execute("SELECT 1").fetchone()
        
        return {
            "status": "healthy", 
            "service": "family-friends-api-database",
            "database": "connected",
            "version": "2.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "family-friends-api-database", 
            "database": "disconnected",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Family & Friends Fitness API with Database")
    print("📊 Database: SQLite with persistent storage")
    print("🌐 Server: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("📈 Database Stats: http://localhost:8000/api/database/stats")
    uvicorn.run(app, host="0.0.0.0", port=8000)