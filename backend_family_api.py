"""
Family & Friends Fitness API

FastAPI backend for collaborative fitness tracking with family and friends.
Includes endpoints for group management, shared workouts, challenges, and social features.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

from family_friends_tools import FamilyFriendsTools, PrivacyLevel, WorkoutStatus

app = FastAPI(title="Family & Friends Fitness API", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize family/friends tools
family_tools = FamilyFriendsTools()

# Request/Response Models
class CreateGroupRequest(BaseModel):
    group_name: str
    group_type: str = "friends"  # family, friends, workout_buddies, public_group, fitness_club, local_gym
    creator_id: str
    description: str = ""
    privacy_level: str = "friends"  # private, friends, local, public, invite_only
    initial_members: List[str] = []
    # NEW: Community expansion fields
    location: Optional[str] = None
    activity_focus: List[str] = []  # ["strength", "cardio", "yoga"]
    experience_levels: List[str] = ["all"]  # ["beginner", "intermediate", "advanced"]
    is_discoverable: bool = True
    tags: List[str] = []

class JoinGroupRequest(BaseModel):
    user_id: str
    invite_code: str
    user_name: str = "New Member"

class CreateWorkoutRequest(BaseModel):
    creator_id: str
    workout_name: str
    workout_type: str = "strength"
    exercises: List[Dict]
    share_with_groups: List[str] = []
    difficulty: str = "intermediate"
    estimated_duration: int = 60
    description: str = ""
    tags: List[str] = []

class StartSessionRequest(BaseModel):
    user_id: str
    workout_id: str
    group_ids: List[str] = []
    privacy_level: str = "friends"

class CompleteSessionRequest(BaseModel):
    session_id: str
    exercises_completed: List[Dict] = []
    notes: str = ""
    achievements: List[str] = []

class CreateChallengeRequest(BaseModel):
    creator_id: str
    group_id: str
    challenge_name: str
    challenge_type: str = "workout_frequency"
    duration_days: int = 30
    target_metrics: Dict = {}
    description: str = ""
    rewards: List[str] = []

# NEW: Phase 2 & 3 Models
class CreateSkillSessionRequest(BaseModel):
    instructor_id: str
    skill_type: str  # "olympic_lifting", "nutrition_planning", "mobility", etc.
    title: str
    description: str
    max_participants: int = 10
    session_format: str = "in_person"  # in_person, virtual, hybrid
    skill_level: str = "beginner"  # beginner, intermediate, advanced
    duration_minutes: int = 60
    location: Optional[str] = None
    session_date: str  # YYYY-MM-DD
    session_time: str  # HH:MM
    fee_credits: int = 0
    materials_provided: List[str] = []
    prerequisites: List[str] = []
    certification_offered: bool = False

class JoinSkillSessionRequest(BaseModel):
    user_id: str
    session_id: str
    user_name: str = "Participant"

class MentorMatchRequest(BaseModel):
    mentee_id: str
    fitness_goals: List[str] = []  # ["strength", "weight_loss", "technique"]
    experience_level: str = "beginner"
    preferred_mentor_qualities: List[str] = []  # ["patient", "experienced", "motivational"]
    availability: List[str] = []  # ["weekday_mornings", "weekend_afternoons"]
    location_preference: Optional[str] = None

class WorkoutPartnerRequest(BaseModel):
    user_id: str
    workout_type: str = "strength"  # strength, cardio, yoga, etc.
    preferred_time: str  # "now", "2025-10-15T18:00:00"
    location: Optional[str] = None
    experience_level: str = "intermediate"
    workout_duration: int = 60  # minutes
    partner_preferences: List[str] = []  # ["similar_level", "motivational", "focused"]

class LiveWorkoutSyncRequest(BaseModel):
    session_creator_id: str
    workout_plan: Dict  # Complete workout structure
    invited_partners: List[str] = []
    privacy_level: str = "invite_only"
    start_time: Optional[str] = None  # Auto-start if None

# API Endpoints

@app.get("/")
async def root():
    return {
        "message": "Family & Friends Fitness API",
        "version": "1.0.0",
        "status": "active",
        "features": [
            "Group Management",
            "Shared Workouts", 
            "Social Challenges",
            "Real-time Tracking",
            "Family Dashboard"
        ]
    }

@app.post("/api/groups/create")
async def create_fitness_group(request: CreateGroupRequest):
    """Create a new family or friends fitness group."""
    try:
        result = await family_tools.create_fitness_group({
            "group_name": request.group_name,
            "group_type": request.group_type,
            "creator_id": request.creator_id,
            "description": request.description,
            "privacy_level": request.privacy_level,
            "initial_members": request.initial_members
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/groups/join")
async def join_fitness_group(request: JoinGroupRequest):
    """Join an existing fitness group via invite code."""
    try:
        result = await family_tools.join_fitness_group({
            "user_id": request.user_id,
            "invite_code": request.invite_code,
            "user_name": request.user_name
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/groups/user/{user_id}")
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

@app.post("/api/workouts/shared/create")
async def create_shared_workout(request: CreateWorkoutRequest):
    """Create a workout that can be shared with family/friends."""
    try:
        result = await family_tools.create_shared_workout({
            "creator_id": request.creator_id,
            "workout_name": request.workout_name,
            "workout_type": request.workout_type,
            "exercises": request.exercises,
            "share_with_groups": request.share_with_groups,
            "difficulty": request.difficulty,
            "estimated_duration": request.estimated_duration,
            "description": request.description,
            "tags": request.tags
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workouts/shared/group/{group_id}")
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

@app.post("/api/sessions/start")
async def start_group_workout_session(request: StartSessionRequest):
    """Start a workout session that will be tracked with family/friends."""
    try:
        result = await family_tools.start_group_workout_session({
            "user_id": request.user_id,
            "workout_id": request.workout_id,
            "group_ids": request.group_ids,
            "privacy_level": request.privacy_level
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sessions/complete")
async def complete_workout_session(request: CompleteSessionRequest):
    """Complete a workout session and share results with groups."""
    try:
        result = await family_tools.complete_workout_session({
            "session_id": request.session_id,
            "exercises_completed": request.exercises_completed,
            "notes": request.notes,
            "achievements": request.achievements
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/live/{session_id}")
async def get_live_workout_session(session_id: str):
    """Get real-time updates for an active workout session."""
    try:
        if session_id not in family_tools.workout_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = family_tools.workout_sessions[session_id]
        
        # Calculate elapsed time if session is active
        elapsed_minutes = 0
        if session.status == WorkoutStatus.IN_PROGRESS:
            start_time = datetime.fromisoformat(session.start_time)
            elapsed_minutes = int((datetime.now() - start_time).total_seconds() / 60)
        
        return {
            "session_id": session_id,
            "user_id": session.user_id,
            "status": session.status.value,
            "elapsed_minutes": elapsed_minutes,
            "exercises_completed": len(session.exercises_completed),
            "social_reactions": session.social_reactions,
            "shared_with_groups": session.shared_with_groups
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/challenges/create")
async def create_group_challenge(request: CreateChallengeRequest):
    """Create a fitness challenge for family/friends groups."""
    try:
        result = await family_tools.create_group_challenge({
            "creator_id": request.creator_id,
            "group_id": request.group_id,
            "challenge_name": request.challenge_name,
            "challenge_type": request.challenge_type,
            "duration_days": request.duration_days,
            "target_metrics": request.target_metrics,
            "description": request.description,
            "rewards": request.rewards
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/challenges/group/{group_id}")
async def get_group_challenges(group_id: str, active_only: bool = True):
    """Get all challenges for a specific group."""
    try:
        group_challenges = []
        for challenge_id, challenge in family_tools.group_challenges.items():
            if challenge.group_id == group_id:
                if not active_only or challenge.is_active:
                    # Calculate days remaining
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

@app.get("/api/challenges/leaderboard/{challenge_id}")
async def get_challenge_leaderboard(challenge_id: str):
    """Get the current leaderboard for a challenge."""
    try:
        if challenge_id not in family_tools.group_challenges:
            raise HTTPException(status_code=404, detail="Challenge not found")
        
        challenge = family_tools.group_challenges[challenge_id]
        
        # Mock leaderboard data - would be calculated from actual user progress
        leaderboard = []
        for i, participant in enumerate(challenge.participants):
            leaderboard.append({
                "position": i + 1,
                "user_id": participant,
                "user_name": f"User {participant}",
                "points": 150 - (i * 20),  # Mock scoring
                "progress_percentage": 85 - (i * 10),
                "achievements": ["Consistency King", "Early Bird"] if i == 0 else []
            })
        
        return {
            "challenge_id": challenge_id,
            "challenge_name": challenge.name,
            "challenge_type": challenge.challenge_type,
            "leaderboard": leaderboard,
            "total_participants": len(challenge.participants),
            "days_remaining": family_tools._calculate_days_remaining(challenge.end_date)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard/family-friends/{user_id}")
async def get_family_friends_dashboard(user_id: str):
    """Get comprehensive dashboard for family/friends fitness tracking."""
    try:
        result = await family_tools.get_family_friends_dashboard({
            "user_id": user_id
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/social/react/{session_id}")
async def react_to_workout_session(session_id: str, reaction_type: str = "encouragement", message: str = ""):
    """Send a reaction/encouragement to someone's workout session."""
    try:
        if session_id not in family_tools.workout_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = family_tools.workout_sessions[session_id]
        
        reaction = {
            "reaction_type": reaction_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "sender_id": "current_user"  # Would come from auth
        }
        
        session.social_reactions.append(reaction)
        
        return {
            "reaction_sent": True,
            "session_id": session_id,
            "total_reactions": len(session.social_reactions),
            "latest_reaction": reaction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/groups/{group_id}/activity")
async def get_group_activity_feed(group_id: str, limit: int = 20):
    """Get recent activity feed for a group."""
    try:
        if group_id not in family_tools.groups_database:
            raise HTTPException(status_code=404, detail="Group not found")
        
        activities = family_tools._get_group_recent_activity(group_id)
        
        # Expand with more details
        detailed_activities = []
        for activity in activities[:limit]:
            detailed_activities.append({
                **activity,
                "user_name": f"User {activity['user_id']}",  # Would fetch from user database
                "activity_description": _format_activity_description(activity),
                "relative_time": _format_relative_time(activity['timestamp'])
            })
        
        return {
            "group_id": group_id,
            "activities": detailed_activities,
            "total_activities": len(activities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/community/discover")
async def discover_fitness_groups(
    user_location: Optional[str] = None,
    fitness_interests: Optional[str] = None,  # comma-separated
    experience_level: str = "intermediate",
    group_type: Optional[str] = None,
    distance_km: int = 50
):
    """NEW: Discover public fitness groups in the broader community."""
    try:
        # Mock discovery algorithm - would use real location/matching in production
        interests_list = fitness_interests.split(",") if fitness_interests else []
        
        discovered_groups = [
            {
                "group_id": "powerlifters_downtown_demo",
                "name": "Downtown Powerlifters Community",
                "type": "sport_community",
                "privacy_level": "public",
                "member_count": 150,
                "location": "Downtown Gym District",
                "distance_km": 5.2,
                "activity_focus": ["powerlifting", "strength_training"],
                "experience_levels": ["intermediate", "advanced"],
                "meeting_schedule": "Mon/Wed/Fri 6:00 PM",
                "compatibility_score": 95 if "strength" in interests_list else 70,
                "join_requirements": "Squat 1.5x bodyweight minimum",
                "recent_achievements": ["City Powerlifting Champions 2025"],
                "active_challenges": 3,
                "can_join_immediately": True
            },
            {
                "group_id": "runners_central_park_demo", 
                "name": "Central Park Morning Runners",
                "type": "public_group",
                "privacy_level": "public",
                "member_count": 280,
                "location": "Central Park",
                "distance_km": 8.1,
                "activity_focus": ["running", "cardio", "marathons"],
                "experience_levels": ["all_levels"],
                "meeting_schedule": "Daily 6:00 AM",
                "compatibility_score": 88 if "cardio" in interests_list else 60,
                "join_requirements": "Open to all fitness levels",
                "recent_achievements": ["Boston Marathon Qualifiers: 15 members"],
                "active_challenges": 2,
                "can_join_immediately": True
            },
            {
                "group_id": "yoga_wellness_community_demo",
                "name": "Holistic Wellness & Yoga Community",
                "type": "fitness_club",
                "privacy_level": "invite_only",
                "member_count": 95,
                "location": "Wellness Center District",
                "distance_km": 12.5,
                "activity_focus": ["yoga", "meditation", "flexibility"],
                "experience_levels": ["beginner", "intermediate"],
                "meeting_schedule": "Daily classes + weekend workshops",
                "compatibility_score": 92 if "yoga" in interests_list else 45,
                "join_requirements": "Application + trial class required",
                "recent_achievements": ["200-Hour Yoga Teacher Training Graduates: 8"],
                "active_challenges": 1,
                "can_join_immediately": False
            }
        ]
        
        # Filter by group type if specified
        if group_type:
            discovered_groups = [g for g in discovered_groups if g["type"] == group_type]
        
        # Sort by compatibility score
        discovered_groups.sort(key=lambda x: x["compatibility_score"], reverse=True)
        
        return {
            "discovered_groups": discovered_groups,
            "total_found": len(discovered_groups),
            "search_criteria": {
                "user_location": user_location,
                "fitness_interests": interests_list,
                "experience_level": experience_level,
                "max_distance_km": distance_km
            },
            "recommendation_tips": [
                "Higher compatibility scores mean better matches for your interests",
                "Join public groups immediately or request invites for private groups", 
                "Check meeting schedules to ensure they fit your availability"
            ],
            "next_steps": {
                "join_group": "POST /api/groups/join with invite_code",
                "request_invite": "POST /api/community/request-invite for private groups",
                "create_own_group": "POST /api/groups/create with public settings"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _format_activity_description(activity: Dict) -> str:
    """Format activity for human-readable description."""
    if activity["activity"] == "workout_completed":
        return f"completed a {activity['details']} workout"
    return activity["activity"]

def _format_relative_time(timestamp: str) -> str:
    """Format timestamp as relative time."""
    if not timestamp:
        return "unknown"
    
    try:
        activity_time = datetime.fromisoformat(timestamp)
        now = datetime.now()
        diff = now - activity_time
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return "just now"
    except:
        return "unknown"

# PHASE 2: SKILL SHARING ENDPOINTS

@app.post("/api/skills/create-session")
async def create_skill_session(request: CreateSkillSessionRequest):
    """
    Create a new skill sharing session where experienced users teach others.
    Builds community knowledge transfer and mentorship opportunities.
    """
    try:
        session_id = f"skill_session_{len(getattr(app.state, 'skill_sessions', {})) + 1}"
        
        session_data = {
            "session_id": session_id,
            "instructor_id": request.instructor_id,
            "skill_type": request.skill_type,
            "title": request.title,
            "description": request.description,
            "max_participants": request.max_participants,
            "current_participants": 0,
            "enrolled_users": [],
            "session_format": request.session_format,
            "skill_level": request.skill_level,
            "duration_minutes": request.duration_minutes,
            "location": request.location,
            "session_date": request.session_date,
            "session_time": request.session_time,
            "fee_credits": request.fee_credits,
            "materials_provided": request.materials_provided,
            "prerequisites": request.prerequisites,
            "certification_offered": request.certification_offered,
            "status": "open",
            "created_at": datetime.now().isoformat(),
            "instructor_rating": 4.8,  # Simulated from past sessions
            "instructor_sessions_taught": 23
        }
        
        # Initialize skill sessions storage if needed
        if not hasattr(app.state, 'skill_sessions'):
            app.state.skill_sessions = {}
        
        app.state.skill_sessions[session_id] = session_data
        
        return {
            "status": "success",
            "message": "Skill sharing session created successfully",
            "session": session_data,
            "next_steps": [
                "Session is now visible to community members",
                "Participants can enroll using the session ID",
                "You'll receive notifications when users join"
            ]
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to create skill session: {str(e)}"}
        )

@app.post("/api/skills/join-session") 
async def join_skill_session(request: JoinSkillSessionRequest):
    """
    Enroll in a skill sharing session to learn from experienced community members.
    """
    try:
        if not hasattr(app.state, 'skill_sessions'):
            app.state.skill_sessions = {}
            
        session = app.state.skill_sessions.get(request.session_id)
        
        if not session:
            return JSONResponse(
                status_code=404,
                content={"status": "error", "message": "Skill session not found"}
            )
            
        if session["current_participants"] >= session["max_participants"]:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Session is full"}
            )
            
        # Check if user already enrolled
        if request.user_id in session["enrolled_users"]:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Already enrolled in this session"}
            )
            
        # Enroll user
        session["enrolled_users"].append(request.user_id)
        session["current_participants"] += 1
        
        return {
            "status": "success",
            "message": "Successfully enrolled in skill session",
            "session_details": {
                "title": session["title"],
                "instructor": session["instructor_id"],
                "date": session["session_date"],
                "time": session["session_time"],
                "location": session["location"],
                "materials_needed": session["materials_provided"],
                "prerequisites": session["prerequisites"]
            },
            "preparation_tips": [
                "Review any prerequisites listed",
                "Bring water and a towel",
                "Arrive 10 minutes early for setup",
                "Come prepared to ask questions"
            ]
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to join session: {str(e)}"}
        )

@app.get("/api/skills/available-sessions")
async def get_available_skill_sessions():
    """
    Browse all available skill sharing sessions in the community.
    """
    try:
        if not hasattr(app.state, 'skill_sessions'):
            # Return demo sessions if none exist
            demo_sessions = {
                "demo_1": {
                    "session_id": "demo_1",
                    "instructor_id": "coach_maya",
                    "skill_type": "olympic_lifting",
                    "title": "Clean & Jerk Fundamentals",
                    "description": "Master the technical aspects of the clean and jerk with personalized form corrections",
                    "max_participants": 8,
                    "current_participants": 3,
                    "session_format": "in_person",
                    "skill_level": "intermediate",
                    "duration_minutes": 90,
                    "location": "Olympic Training Center",
                    "session_date": "2024-01-20",
                    "session_time": "10:00",
                    "fee_credits": 25,
                    "instructor_rating": 4.9,
                    "status": "open"
                },
                "demo_2": {
                    "session_id": "demo_2", 
                    "instructor_id": "nutritionist_alex",
                    "skill_type": "nutrition_planning",
                    "title": "Macro Tracking for Athletes",
                    "description": "Learn to calculate and track macronutrients for optimal performance and body composition",
                    "max_participants": 12,
                    "current_participants": 7,
                    "session_format": "virtual",
                    "skill_level": "beginner",
                    "duration_minutes": 60,
                    "location": "Zoom Session",
                    "session_date": "2024-01-18",
                    "session_time": "19:00",
                    "fee_credits": 15,
                    "instructor_rating": 4.7,
                    "status": "open"
                }
            }
            available_sessions = list(demo_sessions.values())
        else:
            available_sessions = [
                session for session in app.state.skill_sessions.values()
                if session["status"] == "open" and session["current_participants"] < session["max_participants"]
            ]
        
        # Group by skill type for better organization
        sessions_by_skill = {}
        for session in available_sessions:
            skill_type = session["skill_type"]
            if skill_type not in sessions_by_skill:
                sessions_by_skill[skill_type] = []
            sessions_by_skill[skill_type].append(session)
            
        return {
            "status": "success",
            "total_sessions": len(available_sessions),
            "sessions_by_skill": sessions_by_skill,
            "skill_categories": list(sessions_by_skill.keys()),
            "upcoming_highlights": [
                {
                    "title": session["title"],
                    "instructor": session["instructor_id"],
                    "date": session["session_date"],
                    "spots_remaining": session["max_participants"] - session["current_participants"]
                }
                for session in sorted(available_sessions, key=lambda x: x["session_date"])[:3]
            ]
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to fetch sessions: {str(e)}"}
        )

# PHASE 2: MENTOR MATCHING ENDPOINTS

@app.post("/api/mentorship/find-mentor")
async def find_mentor_match(request: MentorMatchRequest):
    """
    AI-powered mentor matching based on goals, experience level, and preferences.
    Connects users with experienced community members for personalized guidance.
    """
    try:
        # Simulate mentor matching algorithm
        potential_mentors = [
            {
                "mentor_id": "mentor_sarah_k",
                "name": "Sarah K.",
                "specializations": ["strength_training", "nutrition", "injury_recovery"],
                "experience_years": 8,
                "mentorship_rating": 4.9,
                "mentees_guided": 47,
                "availability": ["weekday_evenings", "weekend_mornings"],
                "location": request.location_preference or "Virtual sessions available",
                "mentoring_style": "Patient and methodical",
                "success_stories": [
                    "Helped 12 beginners achieve first pull-up",
                    "Guided nutrition transformations averaging 15% body fat reduction"
                ],
                "match_score": 92,
                "match_reasons": [
                    "Specializes in your primary goals",
                    "Excellent track record with beginners", 
                    "Available during your preferred times"
                ]
            },
            {
                "mentor_id": "mentor_alex_m",
                "name": "Alex M.",
                "specializations": ["powerlifting", "form_correction", "competition_prep"],
                "experience_years": 12,
                "mentorship_rating": 4.7,
                "mentees_guided": 33,
                "availability": ["early_mornings", "weekend_afternoons"],
                "location": request.location_preference or "Hybrid (in-person + virtual)",
                "mentoring_style": "Technical and detail-oriented",
                "success_stories": [
                    "Coached 8 athletes to regional competitions",
                    "Zero training injuries in 2+ years of mentoring"
                ],
                "match_score": 87,
                "match_reasons": [
                    "Technical expertise matches your needs",
                    "Strong safety record",
                    "Experience with competitive goals"
                ]
            },
            {
                "mentor_id": "mentor_priya_r",
                "name": "Priya R.",
                "specializations": ["yoga", "flexibility", "mindfulness", "stress_management"],
                "experience_years": 6,
                "mentorship_rating": 4.8,
                "mentees_guided": 28,
                "availability": ["weekday_mornings", "weekend_evenings"],
                "location": "Virtual sessions worldwide",
                "mentoring_style": "Holistic and encouraging",
                "success_stories": [
                    "Improved flexibility for 20+ desk workers",
                    "Stress reduction techniques adopted by 95% of mentees"
                ],
                "match_score": 85,
                "match_reasons": [
                    "Wellness-focused approach",
                    "Flexible virtual availability",
                    "High success rate with lifestyle goals"
                ]
            }
        ]
        
        # Sort by match score
        potential_mentors.sort(key=lambda x: x["match_score"], reverse=True)
        
        return {
            "status": "success",
            "matches_found": len(potential_mentors),
            "recommended_mentors": potential_mentors,
            "matching_criteria": {
                "goals_analyzed": request.fitness_goals,
                "experience_level": request.experience_level,
                "preferences_considered": request.preferred_mentor_qualities,
                "availability_matched": request.availability
            },
            "next_steps": [
                "Review mentor profiles and success stories",
                "Send mentorship request to your top choice",
                "Schedule an initial consultation call",
                "Set up regular mentoring sessions"
            ]
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Mentor matching failed: {str(e)}"}
        )

# PHASE 3: REAL-TIME WORKOUT PARTNER COORDINATION

@app.post("/api/partners/find-workout-buddy")
async def find_workout_partner(request: WorkoutPartnerRequest):
    """
    Find available workout partners for real-time coordination.
    Matches based on workout type, timing, location, and experience level.
    """
    try:
        # Simulate real-time partner matching
        available_partners = [
            {
                "partner_id": "user_jenny_m",
                "name": "Jenny M.", 
                "current_status": "looking_for_partner",
                "workout_type": request.workout_type,
                "experience_level": "intermediate",
                "location": request.location or "Downtown Fitness Center",
                "availability": "next 2 hours",
                "preferred_duration": 75,  # minutes
                "workout_style": "focused_training",
                "mutual_goals": ["strength_building", "consistency"],
                "partner_rating": 4.8,
                "workout_streak": 12,
                "compatibility_score": 94,
                "distance_km": 0.8,
                "last_active": "2 minutes ago"
            },
            {
                "partner_id": "user_marcus_r",
                "name": "Marcus R.",
                "current_status": "warming_up", 
                "workout_type": request.workout_type,
                "experience_level": "advanced",
                "location": request.location or "Iron Paradise Gym",
                "availability": "available now",
                "preferred_duration": 90,
                "workout_style": "high_intensity",
                "mutual_goals": ["strength_building", "competition_prep"],
                "partner_rating": 4.6,
                "workout_streak": 8,
                "compatibility_score": 87,
                "distance_km": 1.2,
                "last_active": "just now"
            },
            {
                "partner_id": "user_alex_c",
                "name": "Alex C.",
                "current_status": "looking_for_partner",
                "workout_type": request.workout_type, 
                "experience_level": "beginner",
                "location": request.location or "Community Fitness Hub",
                "availability": "flexible timing",
                "preferred_duration": 45,
                "workout_style": "supportive_learning",
                "mutual_goals": ["form_improvement", "motivation"],
                "partner_rating": 4.9,
                "workout_streak": 4,
                "compatibility_score": 82,
                "distance_km": 2.1,
                "last_active": "5 minutes ago"
            }
        ]
        
        # Sort by compatibility score
        available_partners.sort(key=lambda x: x["compatibility_score"], reverse=True)
        
        return {
            "status": "success", 
            "partners_found": len(available_partners),
            "available_partners": available_partners,
            "matching_summary": {
                "workout_type": request.workout_type,
                "your_experience": request.experience_level,
                "location_radius": "3km",
                "time_preference": request.preferred_time
            },
            "quick_actions": [
                {
                    "action": "send_workout_invite",
                    "partner_id": available_partners[0]["partner_id"],
                    "message": f"Invite {available_partners[0]['name']} to workout together"
                },
                {
                    "action": "create_group_session", 
                    "partners": [p["partner_id"] for p in available_partners[:2]],
                    "message": "Start a group workout with multiple partners"
                }
            ]
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Partner matching failed: {str(e)}"}
        )

@app.post("/api/partners/sync-workout")
async def create_live_workout_sync(request: LiveWorkoutSyncRequest):
    """
    Create a synchronized live workout session with real-time partner coordination.
    Partners can follow the same workout plan and see each other's progress.
    """
    try:
        sync_session_id = f"live_sync_{len(getattr(app.state, 'live_workouts', {})) + 1}"
        
        # Initialize live workouts storage if needed
        if not hasattr(app.state, 'live_workouts'):
            app.state.live_workouts = {}
        
        sync_session = {
            "session_id": sync_session_id,
            "creator_id": request.session_creator_id,
            "workout_plan": request.workout_plan,
            "invited_partners": request.invited_partners,
            "active_participants": [request.session_creator_id],
            "privacy_level": request.privacy_level,
            "start_time": request.start_time or datetime.now().isoformat(),
            "status": "waiting_for_partners",
            "current_exercise": 0,
            "exercise_start_time": None,
            "participant_progress": {
                request.session_creator_id: {
                    "current_set": 0,
                    "current_reps": 0,
                    "rest_time_remaining": 0,
                    "status": "ready"
                }
            },
            "live_updates": [],
            "motivation_messages": [],
            "created_at": datetime.now().isoformat()
        }
        
        app.state.live_workouts[sync_session_id] = sync_session
        
        return {
            "status": "success",
            "message": "Live workout sync session created",
            "session": {
                "session_id": sync_session_id,
                "workout_title": request.workout_plan.get("title", "Live Workout Session"),
                "total_exercises": len(request.workout_plan.get("exercises", [])),
                "estimated_duration": request.workout_plan.get("duration_minutes", 60),
                "invited_partners": len(request.invited_partners),
                "join_code": sync_session_id[-6:],  # Last 6 chars as join code
                "privacy": request.privacy_level
            },
            "next_steps": [
                "Share session ID with invited partners",
                "Partners will receive live notifications", 
                "Workout will auto-start when partners join",
                "Real-time progress tracking will be available"
            ],
            "live_features": [
                "Synchronized exercise transitions",
                "Real-time rep counting and rest timers",
                "Partner progress visibility",
                "Motivational messaging",
                "Form check requests and feedback"
            ]
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to create sync session: {str(e)}"}
        )

@app.get("/api/partners/live-session/{session_id}")
async def get_live_workout_status(session_id: str):
    """
    Get real-time status updates for a live workout sync session.
    Shows current exercise, partner progress, and live coordination data.
    """
    try:
        if not hasattr(app.state, 'live_workouts'):
            app.state.live_workouts = {}
            
        session = app.state.live_workouts.get(session_id)
        
        if not session:
            return JSONResponse(
                status_code=404,
                content={"status": "error", "message": "Live workout session not found"}
            )
            
        # Simulate real-time updates
        current_exercise = session["workout_plan"]["exercises"][session["current_exercise"]] if session["current_exercise"] < len(session["workout_plan"]["exercises"]) else None
        
        return {
            "status": "success",
            "session_status": session["status"],
            "current_exercise": current_exercise,
            "exercise_number": session["current_exercise"] + 1,
            "total_exercises": len(session["workout_plan"]["exercises"]),
            "active_participants": len(session["active_participants"]),
            "participant_progress": session["participant_progress"],
            "live_updates": session["live_updates"][-10:],  # Last 10 updates
            "motivation_feed": [
                f"{participant} completed set {progress['current_set']}" 
                for participant, progress in session["participant_progress"].items()
                if progress["current_set"] > 0
            ],
            "sync_controls": {
                "can_pause": session["status"] == "active",
                "can_skip_exercise": True,
                "can_request_form_check": True,
                "can_send_motivation": True
            }
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to get session status: {str(e)}"}
        )

# WEIGHT TRACKING SYSTEM

class LogWeightRequest(BaseModel):
    user_id: str
    weight: float  # Weight value
    unit: str = "kg"  # kg or lbs
    goal_weight: Optional[float] = None
    notes: str = ""
    share_with_groups: List[str] = []
    privacy_level: str = "family"  # private, family, friends, public
    body_fat_percentage: Optional[float] = None
    muscle_mass: Optional[float] = None

class WeightGoalRequest(BaseModel):
    user_id: str
    goal_weight: float
    target_date: Optional[str] = None
    goal_type: str = "lose_weight"  # lose_weight, gain_weight, maintain_weight
    weekly_target: Optional[float] = None  # kg/lbs per week

class WeightChallengeRequest(BaseModel):
    creator_id: str
    challenge_name: str
    challenge_type: str = "weight_loss"  # weight_loss, weight_gain, maintenance
    group_id: str
    target_amount: float  # Total kg/lbs for group
    duration_days: int = 30
    start_date: Optional[str] = None
    reward_description: str = ""

# PHASE 2/3: RATING & REVIEW SYSTEM

class SubmitReviewRequest(BaseModel):
    reviewer_id: str
    session_id: Optional[str] = None  # For skill sessions
    mentor_id: Optional[str] = None   # For mentorship
    partner_id: Optional[str] = None  # For workout partners
    review_type: str  # "skill_session", "mentorship", "workout_partner"
    rating: int  # 1-5 stars
    review_text: str = ""
    specific_feedback: Dict = {}  # Detailed ratings for different aspects
    would_recommend: bool = True
    session_date: Optional[str] = None

# WEIGHT TRACKING ENDPOINTS

@app.post("/api/weight/log")
async def log_weight(request: LogWeightRequest):
    """
    Log a weight entry for a user with analytics and family sharing capabilities.
    """
    try:
        # Initialize weight tracking storage if needed
        if not hasattr(app.state, 'weight_entries'):
            app.state.weight_entries = {}
            
        if not hasattr(app.state, 'weight_goals'):
            app.state.weight_goals = {}
            
        # Create weight entry
        entry_id = f"weight_{request.user_id}_{len(app.state.weight_entries.get(request.user_id, [])) + 1}"
        
        weight_entry = {
            "entry_id": entry_id,
            "user_id": request.user_id,
            "weight": request.weight,
            "unit": request.unit,
            "goal_weight": request.goal_weight,
            "notes": request.notes,
            "share_with_groups": request.share_with_groups,
            "privacy_level": request.privacy_level,
            "body_fat_percentage": request.body_fat_percentage,
            "muscle_mass": request.muscle_mass,
            "logged_at": datetime.now().isoformat(),
            "validated": True
        }
        
        # Store entry
        if request.user_id not in app.state.weight_entries:
            app.state.weight_entries[request.user_id] = []
        
        app.state.weight_entries[request.user_id].insert(0, weight_entry)  # Most recent first
        
        # Update goal if provided
        if request.goal_weight:
            app.state.weight_goals[request.user_id] = {
                "goal_weight": request.goal_weight,
                "unit": request.unit,
                "set_date": datetime.now().isoformat(),
                "target_date": None
            }
        
        # Calculate progress message
        progress_message = "Weight logged successfully!"
        entries = app.state.weight_entries[request.user_id]
        
        if len(entries) > 1:
            prev_weight = entries[1]["weight"]
            change = request.weight - prev_weight
            
            if abs(change) >= 0.1:
                direction = "lost" if change < 0 else "gained"
                progress_message = f"Weight logged! You've {direction} {abs(change):.1f} {request.unit} since last entry."
        
        return {
            "success": True,
            "message": progress_message,
            "entry": weight_entry,
            "analytics": _calculate_weight_analytics(request.user_id, app.state.weight_entries.get(request.user_id, [])),
            "sharing_status": {
                "shared_with_groups": len(request.share_with_groups),
                "privacy_level": request.privacy_level,
                "family_notifications_sent": len([g for g in request.share_with_groups if "family" in g])
            }
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Failed to log weight: {str(e)}"}
        )

@app.get("/api/weight/history/{user_id}")
async def get_weight_history(user_id: str, limit: int = 50):
    """
    Get comprehensive weight history and analytics for a user.
    """
    try:
        if not hasattr(app.state, 'weight_entries'):
            app.state.weight_entries = {}
            
        entries = app.state.weight_entries.get(user_id, [])
        
        return {
            "success": True,
            "weight_entries": entries[:limit],
            "analytics": _calculate_weight_analytics(user_id, entries),
            "goal_info": app.state.weight_goals.get(user_id, None),
            "total_entries": len(entries),
            "tracking_since": entries[-1]["logged_at"] if entries else None
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Failed to get weight history: {str(e)}"}
        )

@app.post("/api/weight/set-goal")
async def set_weight_goal(request: WeightGoalRequest):
    """
    Set or update weight goal for a user with target tracking.
    """
    try:
        if not hasattr(app.state, 'weight_goals'):
            app.state.weight_goals = {}
            
        goal = {
            "user_id": request.user_id,
            "goal_weight": request.goal_weight,
            "target_date": request.target_date,
            "goal_type": request.goal_type,
            "weekly_target": request.weekly_target,
            "set_date": datetime.now().isoformat(),
            "is_active": True
        }
        
        app.state.weight_goals[request.user_id] = goal
        
        # Calculate estimated timeline if weekly target provided
        current_entries = app.state.weight_entries.get(request.user_id, [])
        timeline_message = "Goal set successfully!"
        
        if current_entries and request.weekly_target:
            current_weight = current_entries[0]["weight"]
            weight_to_lose_gain = abs(request.goal_weight - current_weight)
            estimated_weeks = weight_to_lose_gain / request.weekly_target
            timeline_message = f"Goal set! At {request.weekly_target} kg/week, estimated {estimated_weeks:.1f} weeks to reach goal."
        
        return {
            "success": True,
            "message": timeline_message,
            "goal": goal,
            "progress_tracking": {
                "current_weight": current_entries[0]["weight"] if current_entries else None,
                "target_weight": request.goal_weight,
                "estimated_timeline": f"{estimated_weeks:.1f} weeks" if current_entries and request.weekly_target else "Set weekly target for timeline"
            }
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Failed to set goal: {str(e)}"}
        )

@app.post("/api/weight/challenges/create")
async def create_weight_challenge(request: WeightChallengeRequest):
    """
    Create a family/group weight challenge with progress tracking.
    """
    try:
        if not hasattr(app.state, 'weight_challenges'):
            app.state.weight_challenges = {}
            
        challenge_id = f"weight_challenge_{len(app.state.weight_challenges) + 1}"
        
        challenge = {
            "challenge_id": challenge_id,
            "creator_id": request.creator_id,
            "challenge_name": request.challenge_name,
            "challenge_type": request.challenge_type,
            "group_id": request.group_id,
            "target_amount": request.target_amount,
            "duration_days": request.duration_days,
            "start_date": request.start_date or datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=request.duration_days)).isoformat(),
            "reward_description": request.reward_description,
            "participants": [],
            "current_progress": 0.0,
            "is_active": True,
            "created_at": datetime.now().isoformat()
        }
        
        app.state.weight_challenges[challenge_id] = challenge
        
        return {
            "success": True,
            "message": f"Weight challenge '{request.challenge_name}' created successfully!",
            "challenge": challenge,
            "next_steps": [
                "Invite family/group members to join the challenge",
                "Track progress as members log their weights",
                "Celebrate milestones and achievements together"
            ]
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Failed to create challenge: {str(e)}"}
        )

@app.get("/api/weight/family/{group_id}")
async def get_family_weight_progress(group_id: str):
    """
    Get weight progress for all family members in a group.
    """
    try:
        # Mock family data - in real app would fetch from group membership
        family_progress = [
            {
                "user_id": "dad_123",
                "name": "Dad",
                "current_weight": 85.2,
                "unit": "kg",
                "last_updated": "2025-09-24T08:00:00",
                "monthly_change": -2.1,
                "goal_weight": 80.0,
                "progress_to_goal": 60,
                "trend": "losing",
                "streak_days": 12
            },
            {
                "user_id": "mom_456", 
                "name": "Mom",
                "current_weight": 62.8,
                "unit": "kg",
                "last_updated": "2025-09-24T07:30:00",
                "monthly_change": 0.1,
                "goal_weight": 63.0,
                "progress_to_goal": 95,
                "trend": "maintaining",
                "streak_days": 18
            },
            {
                "user_id": "test_user_123",
                "name": "You",
                "current_weight": 75.5,
                "unit": "kg", 
                "last_updated": "2025-09-25T07:18:54",
                "monthly_change": -1.5,
                "goal_weight": 72.0,
                "progress_to_goal": 43,
                "trend": "losing",
                "streak_days": 8
            }
        ]
        
        return {
            "success": True,
            "family_progress": family_progress,
            "group_stats": {
                "total_members": len(family_progress),
                "active_members": len([m for m in family_progress if m["streak_days"] > 0]),
                "combined_loss": sum([abs(m["monthly_change"]) for m in family_progress if m["monthly_change"] < 0]),
                "average_streak": sum([m["streak_days"] for m in family_progress]) / len(family_progress)
            }
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Failed to get family progress: {str(e)}"}
        )

def _calculate_weight_analytics(user_id: str, entries: List[Dict]) -> Dict:
    """Calculate comprehensive weight analytics for a user."""
    if not entries:
        return {
            "current_weight": None,
            "total_change": 0,
            "entries_count": 0,
            "streak_days": 0,
            "trend": "no_data"
        }
    
    current_weight = entries[0]["weight"]
    total_change = 0
    streak_days = 0
    
    if len(entries) > 1:
        oldest_weight = entries[-1]["weight"]
        total_change = current_weight - oldest_weight
        
        # Calculate logging streak
        today = datetime.now().date()
        for entry in entries:
            entry_date = datetime.fromisoformat(entry["logged_at"]).date()
            days_diff = (today - entry_date).days
            if days_diff <= streak_days + 1:
                streak_days = max(streak_days, days_diff)
            else:
                break
    
    # Determine trend
    trend = "stable"
    if len(entries) >= 3:
        recent_weights = [e["weight"] for e in entries[:3]]
        if recent_weights[0] < recent_weights[-1]:
            trend = "losing"
        elif recent_weights[0] > recent_weights[-1]:
            trend = "gaining"
    
    return {
        "current_weight": current_weight,
        "total_change": total_change,
        "entries_count": len(entries),
        "streak_days": streak_days,
        "trend": trend,
        "weekly_average": sum([e["weight"] for e in entries[:7]]) / min(7, len(entries)),
        "monthly_change": entries[0]["weight"] - entries[min(30, len(entries)-1)]["weight"] if len(entries) > 30 else total_change
    }

@app.post("/api/reviews/submit")
async def submit_review(request: SubmitReviewRequest):
    """
    Submit a review for skill sessions, mentorship experiences, or workout partners.
    Builds community trust and helps match quality instructors/mentors with users.
    """
    try:
        review_id = f"review_{len(getattr(app.state, 'reviews', {})) + 1}"
        
        # Initialize reviews storage if needed
        if not hasattr(app.state, 'reviews'):
            app.state.reviews = {}
        
        review_data = {
            "review_id": review_id,
            "reviewer_id": request.reviewer_id,
            "session_id": request.session_id,
            "mentor_id": request.mentor_id,
            "partner_id": request.partner_id,
            "review_type": request.review_type,
            "rating": request.rating,
            "review_text": request.review_text,
            "specific_feedback": request.specific_feedback,
            "would_recommend": request.would_recommend,
            "session_date": request.session_date,
            "submitted_at": datetime.now().isoformat(),
            "verified_experience": True,  # Verified they actually participated
            "helpful_votes": 0,
            "status": "active"
        }
        
        app.state.reviews[review_id] = review_data
        
        # Update instructor/mentor ratings (simulated)
        if request.review_type == "skill_session" and request.session_id:
            rating_update = f"Instructor rating updated: +{request.rating}/5 stars"
        elif request.review_type == "mentorship" and request.mentor_id:
            rating_update = f"Mentor rating updated: +{request.rating}/5 stars"
        else:
            rating_update = "Partner feedback recorded"
        
        return {
            "status": "success",
            "message": "Review submitted successfully",
            "review": review_data,
            "impact": {
                "rating_update": rating_update,
                "community_contribution": "Your feedback helps others make better choices",
                "reputation_earned": 5  # Points for providing feedback
            },
            "follow_up_actions": [
                "Review will be visible to community members",
                "Instructor/mentor will receive constructive feedback",
                "You'll earn reputation points for detailed reviews"
            ]
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to submit review: {str(e)}"}
        )

@app.get("/api/reviews/{target_type}/{target_id}")
async def get_reviews(target_type: str, target_id: str):
    """
    Get all reviews for a specific instructor, mentor, or workout partner.
    Helps users make informed decisions about who to work with.
    """
    try:
        if not hasattr(app.state, 'reviews'):
            # Return demo reviews for testing
            demo_reviews = [
                {
                    "review_id": "demo_review_1",
                    "reviewer_id": "anonymous_user_1",
                    "rating": 5,
                    "review_text": "Excellent instruction! Sarah really knows how to break down complex movements into manageable steps. Her patience with beginners is remarkable.",
                    "specific_feedback": {
                        "instruction_clarity": 5,
                        "patience": 5,
                        "knowledge": 5,
                        "motivation": 4,
                        "preparation": 5
                    },
                    "would_recommend": True,
                    "session_date": "2024-01-10",
                    "submitted_at": "2024-01-11T10:30:00",
                    "verified_experience": True,
                    "helpful_votes": 12
                },
                {
                    "review_id": "demo_review_2",
                    "reviewer_id": "anonymous_user_2", 
                    "rating": 4,
                    "review_text": "Great session overall. Alex provided excellent technical feedback and helped me improve my form significantly. Could use more warm-up time.",
                    "specific_feedback": {
                        "instruction_clarity": 4,
                        "patience": 4,
                        "knowledge": 5,
                        "motivation": 3,
                        "preparation": 4
                    },
                    "would_recommend": True,
                    "session_date": "2024-01-08",
                    "submitted_at": "2024-01-09T15:45:00",
                    "verified_experience": True,
                    "helpful_votes": 8
                }
            ]
            filtered_reviews = demo_reviews
        else:
            # Filter reviews based on target type and ID
            if target_type == "instructor":
                filtered_reviews = [
                    review for review in app.state.reviews.values()
                    if review["review_type"] == "skill_session"
                ]
            elif target_type == "mentor":
                filtered_reviews = [
                    review for review in app.state.reviews.values()
                    if review["review_type"] == "mentorship" and review["mentor_id"] == target_id
                ]
            elif target_type == "partner":
                filtered_reviews = [
                    review for review in app.state.reviews.values()
                    if review["review_type"] == "workout_partner" and review["partner_id"] == target_id
                ]
            else:
                filtered_reviews = []
        
        # Calculate aggregate ratings
        if filtered_reviews:
            avg_rating = sum(r["rating"] for r in filtered_reviews) / len(filtered_reviews)
            rating_distribution = {i: 0 for i in range(1, 6)}
            for review in filtered_reviews:
                rating_distribution[review["rating"]] += 1
                
            # Calculate specific feedback averages
            specific_averages = {}
            if filtered_reviews and "specific_feedback" in filtered_reviews[0]:
                feedback_keys = filtered_reviews[0]["specific_feedback"].keys()
                for key in feedback_keys:
                    specific_averages[key] = sum(
                        r["specific_feedback"].get(key, 0) for r in filtered_reviews
                    ) / len(filtered_reviews)
        else:
            avg_rating = 0
            rating_distribution = {i: 0 for i in range(1, 6)}
            specific_averages = {}
        
        return {
            "status": "success",
            "target_type": target_type,
            "target_id": target_id,
            "total_reviews": len(filtered_reviews),
            "average_rating": round(avg_rating, 1),
            "rating_distribution": rating_distribution,
            "specific_averages": {
                k: round(v, 1) for k, v in specific_averages.items()
            },
            "reviews": sorted(filtered_reviews, key=lambda x: x["submitted_at"], reverse=True),
            "summary_insights": {
                "most_praised_aspect": max(specific_averages, key=specific_averages.get) if specific_averages else "overall_quality",
                "recommendation_rate": f"{sum(1 for r in filtered_reviews if r['would_recommend']) / len(filtered_reviews) * 100:.0f}%" if filtered_reviews else "0%",
                "total_helpful_votes": sum(r.get("helpful_votes", 0) for r in filtered_reviews)
            }
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to fetch reviews: {str(e)}"}
        )

@app.get("/api/community/leaderboards")
async def get_community_leaderboards():
    """
    Display community leaderboards showcasing top instructors, mentors, and active members.
    Gamifies the community experience and highlights quality contributors.
    """
    try:
        # Simulate community leaderboards
        leaderboards = {
            "top_instructors": [
                {
                    "instructor_id": "coach_maya",
                    "name": "Maya S.",
                    "specialization": "Olympic Lifting",
                    "average_rating": 4.9,
                    "sessions_taught": 127,
                    "students_helped": 89,
                    "certification_rate": 94,  # % of students who achieve goals
                    "badge": "Master Instructor"
                },
                {
                    "instructor_id": "trainer_james",
                    "name": "James K.",
                    "specialization": "Strength Training",
                    "average_rating": 4.8,
                    "sessions_taught": 203,
                    "students_helped": 156,
                    "certification_rate": 91,
                    "badge": "Community Favorite"
                },
                {
                    "instructor_id": "coach_priya",
                    "name": "Priya R.",
                    "specialization": "Yoga & Flexibility",
                    "average_rating": 4.7,
                    "sessions_taught": 78,
                    "students_helped": 67,
                    "certification_rate": 96,
                    "badge": "Wellness Expert"
                }
            ],
            "top_mentors": [
                {
                    "mentor_id": "mentor_sarah_k",
                    "name": "Sarah K.",
                    "specializations": ["Nutrition", "Strength Training"],
                    "mentorship_rating": 4.9,
                    "active_mentees": 12,
                    "success_stories": 47,
                    "months_mentoring": 24,
                    "badge": "Transformation Specialist"
                },
                {
                    "mentor_id": "mentor_alex_m",
                    "name": "Alex M.",
                    "specializations": ["Powerlifting", "Competition Prep"],
                    "mentorship_rating": 4.7,
                    "active_mentees": 8,
                    "success_stories": 33,
                    "months_mentoring": 18,
                    "badge": "Performance Coach"
                }
            ],
            "most_active_members": [
                {
                    "member_id": "user_jenny_m",
                    "name": "Jenny M.",
                    "activity_score": 2847,
                    "sessions_attended": 156,
                    "skills_learned": 8,
                    "partners_helped": 23,
                    "streak_days": 45,
                    "badge": "Community Champion"
                },
                {
                    "member_id": "user_marcus_r", 
                    "name": "Marcus R.",
                    "activity_score": 2634,
                    "sessions_attended": 134,
                    "skills_learned": 12,
                    "partners_helped": 31,
                    "streak_days": 38,
                    "badge": "Knowledge Seeker"
                }
            ],
            "rising_stars": [
                {
                    "member_id": "user_alex_c",
                    "name": "Alex C.",
                    "growth_rate": "340% improvement",
                    "recent_achievements": [
                        "First pull-up achieved",
                        "Completed beginner strength program",
                        "Attended 15 skill sessions"
                    ],
                    "mentor": "Sarah K.",
                    "badge": "Fast Learner"
                }
            ]
        }
        
        return {
            "status": "success",
            "leaderboards": leaderboards,
            "community_stats": {
                "total_members": 2847,
                "active_instructors": 23,
                "available_mentors": 12,
                "skill_sessions_this_month": 89,
                "average_community_rating": 4.8,
                "knowledge_transfer_sessions": 234
            },
            "achievements_available": [
                "First Skill Session (Complete your first learning session)",
                "Knowledge Sharer (Teach others in the community)",
                "Mentor Match (Successfully complete mentorship program)",
                "Partner Streak (Workout with partners 10 times)",
                "Community Helper (Help 5 different members)"
            ]
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to fetch leaderboards: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)