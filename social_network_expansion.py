"""
Social Network Expansion for Fitness App
Extending beyond family/friends to broader fitness community
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

# Extended Group Types
class GroupType(str, Enum):
    FAMILY = "family"
    FRIENDS = "friends" 
    WORKOUT_BUDDIES = "workout_buddies"
    # NEW: Broader social network types
    PUBLIC_GROUP = "public_group"
    FITNESS_CLUB = "fitness_club"
    TRAINING_PARTNERS = "training_partners"
    SPORT_COMMUNITY = "sport_community"
    LOCAL_GYM = "local_gym"
    ONLINE_COMMUNITY = "online_community"
    INTEREST_GROUP = "interest_group"  # e.g., "Powerlifters", "Runners", "Yoga"

# Extended Privacy Levels
class PrivacyLevel(str, Enum):
    PRIVATE = "private"           # Only invited members
    FAMILY = "family"             # Family members only
    FRIENDS = "friends"           # Friends network
    # NEW: Broader visibility
    LOCAL = "local"               # Local geographic area
    PUBLIC = "public"             # Anyone can join
    INVITE_ONLY = "invite_only"   # Private but discoverable
    VERIFIED_ONLY = "verified"    # Only verified fitness professionals

# Enhanced Group Discovery
class GroupDiscoveryRequest(BaseModel):
    user_location: Optional[str] = None
    fitness_interests: List[str] = []
    experience_level: str = "intermediate"
    preferred_group_size: str = "medium"  # small, medium, large
    activity_types: List[str] = []
    distance_km: Optional[int] = 50

# Community Features
class CommunityFeatures(BaseModel):
    group_id: str
    features: Dict = {
        # Existing features
        "shared_workouts": True,
        "challenges": True,
        "activity_feed": True,
        "real_time_tracking": True,
        
        # NEW: Community features
        "public_leaderboards": False,
        "skill_sharing": False,           # Members can teach/learn
        "equipment_sharing": False,      # Share gym equipment info
        "workout_scheduling": False,     # Schedule group workouts
        "achievement_badges": False,     # Community recognition
        "mentor_program": False,         # Experienced users mentor newbies
        "local_events": False,          # Real-world meetups
        "progress_showcases": False,    # Public transformation stories
    }

# Global Fitness Community API Extensions
app = FastAPI(title="Extended Social Fitness API", version="2.0.0")

@app.post("/api/community/discover-groups")
async def discover_fitness_groups(request: GroupDiscoveryRequest):
    """Discover fitness groups based on user preferences and location."""
    
    # Mock algorithm - would use ML/location services in production
    suggested_groups = [
        {
            "group_id": "powerlifters_downtown",
            "name": "Downtown Powerlifters",
            "type": "sport_community",
            "member_count": 150,
            "location": "Downtown Gym District",
            "distance_km": 5,
            "activity_level": "high",
            "primary_focus": ["powerlifting", "strength_training"],
            "experience_levels": ["intermediate", "advanced"],
            "meeting_schedule": "Mon/Wed/Fri 6:00 PM",
            "group_achievements": ["City Powerlifting Champions", "1000+ Total Lifts"],
            "join_requirements": "Squat 1.5x bodyweight minimum"
        },
        {
            "group_id": "morning_runners_central",
            "name": "Central Park Morning Runners", 
            "type": "public_group",
            "member_count": 300,
            "location": "Central Park",
            "distance_km": 2,
            "activity_level": "daily",
            "primary_focus": ["running", "cardio", "marathons"],
            "experience_levels": ["beginner", "intermediate", "advanced"],
            "meeting_schedule": "Daily 6:00 AM",
            "group_achievements": ["Boston Marathon Qualifiers", "10k+ Miles Logged"],
            "join_requirements": "Open to all levels"
        },
        {
            "group_id": "family_fitness_suburbs",
            "name": "Suburban Family Fitness",
            "type": "family",
            "member_count": 45,
            "location": "Westfield Community Center", 
            "distance_km": 12,
            "activity_level": "moderate",
            "primary_focus": ["family_workouts", "kids_fitness", "healthy_lifestyle"],
            "experience_levels": ["beginner", "intermediate"],
            "meeting_schedule": "Saturdays 10:00 AM",
            "group_achievements": ["Healthiest Family Challenge Winners"],
            "join_requirements": "Families with children welcome"
        }
    ]
    
    return {
        "suggested_groups": suggested_groups,
        "total_found": len(suggested_groups),
        "search_criteria": request.dict(),
        "recommendation_algorithm": "location + interests + experience_matching"
    }

@app.post("/api/community/create-public-group")
async def create_public_fitness_group(group_data: dict):
    """Create a public fitness group discoverable by the community."""
    
    # Enhanced group creation with community features
    return {
        "group_created": True,
        "group_id": f"public_{group_data['name'].lower().replace(' ', '_')}",
        "visibility": "public",
        "discoverable": True,
        "moderation_required": True,  # Public groups need moderation
        "community_features_enabled": [
            "public_leaderboards",
            "skill_sharing", 
            "achievement_badges",
            "local_events"
        ],
        "growth_potential": "high",
        "recommended_next_steps": [
            "Set group rules and guidelines",
            "Invite experienced members as moderators",
            "Schedule first community workout",
            "Create welcome challenge for new members"
        ]
    }

@app.get("/api/community/trending")
async def get_trending_fitness_content():
    """Get trending fitness content from the broader community."""
    
    return {
        "trending_challenges": [
            {
                "challenge_id": "global_squat_october",
                "name": "Global Squat October",
                "participants": 15000,
                "type": "monthly_challenge",
                "current_leader": "SquatQueen2024",
                "days_remaining": 15,
                "join_url": "/challenges/join/global_squat_october"
            }
        ],
        "popular_workouts": [
            {
                "workout_id": "hiit_cardio_burner",
                "name": "20-Minute HIIT Cardio Burner",
                "created_by": "FitnessCoach_Mike",
                "completions_today": 2300,
                "average_rating": 4.8,
                "difficulty": "intermediate"
            }
        ],
        "success_stories": [
            {
                "user_id": "transformation_sarah",
                "story": "Lost 50 lbs with community support!",
                "before_after_photos": True,
                "workout_plan": "strength_training_beginner",
                "support_group": "weight_loss_warriors",
                "timeframe_months": 8
            }
        ],
        "local_events": [
            {
                "event_id": "charity_5k_downtown",
                "name": "Downtown Charity 5K",
                "date": "2025-10-15",
                "location": "Downtown Park",
                "participants_registered": 450,
                "cause": "Children's Health Foundation"
            }
        ]
    }

@app.post("/api/community/skill-sharing")
async def create_skill_sharing_session(session_data: dict):
    """Allow community members to share fitness knowledge and skills."""
    
    return {
        "session_created": True,
        "session_id": f"skill_{session_data['skill_type']}_{datetime.now().strftime('%Y%m%d')}",
        "skill_type": session_data["skill_type"],  # e.g., "olympic_lifting", "nutrition_planning"
        "instructor": session_data["instructor_id"],
        "max_participants": session_data.get("max_participants", 10),
        "format": session_data.get("format", "in_person"),  # in_person, virtual, hybrid
        "skill_level": session_data.get("level", "beginner"),
        "session_fee": session_data.get("fee", 0),  # Community credits or real money
        "certification_offered": session_data.get("certification", False),
        "community_rating_required": True,
        "instructor_verification": "verified" if session_data.get("certified_trainer") else "community_member"
    }

@app.get("/api/community/leaderboards/{category}")
async def get_community_leaderboards(category: str, timeframe: str = "monthly"):
    """Get community-wide leaderboards for different fitness categories."""
    
    # Mock leaderboard data
    leaderboard_data = {
        "strength_training": [
            {"rank": 1, "username": "IronLifter99", "total_weight_moved": 125000, "workouts": 25},
            {"rank": 2, "username": "SquatGoddess", "total_weight_moved": 118500, "workouts": 28},
            {"rank": 3, "username": "DeadliftKing", "total_weight_moved": 115200, "workouts": 22}
        ],
        "cardio": [
            {"rank": 1, "username": "MarathonMike", "total_distance_km": 420, "workouts": 30},
            {"rank": 2, "username": "SprintSarah", "total_distance_km": 385, "workouts": 35},
            {"rank": 3, "username": "CyclistCarl", "total_distance_km": 1200, "workouts": 25}
        ]
    }
    
    return {
        "category": category,
        "timeframe": timeframe,
        "leaderboard": leaderboard_data.get(category, []),
        "total_participants": 15000,
        "user_rank": 147,  # Current user's rank
        "next_level_requirements": {
            "workouts_needed": 3,
            "points_needed": 450
        },
        "rewards": {
            "top_10": "Gold Badge + Premium Features",
            "top_100": "Silver Badge",
            "top_1000": "Bronze Badge"
        }
    }

# Geographic and Interest-Based Matching
@app.post("/api/community/find-workout-partners")
async def find_workout_partners(preferences: dict):
    """Find workout partners based on location, interests, and schedule."""
    
    return {
        "matches_found": 8,
        "workout_partners": [
            {
                "user_id": "fitness_buddy_123",
                "username": "MorningLifter",
                "compatibility_score": 92,
                "shared_interests": ["powerlifting", "early_workouts", "progressive_overload"],
                "location_distance_km": 3.2,
                "preferred_workout_times": ["6:00 AM", "6:30 AM"],
                "experience_level": "advanced",
                "gym_membership": "Iron Paradise Gym",
                "workout_streak": 45,
                "mutual_connections": 2
            }
        ],
        "matching_algorithm": "location + schedule + interests + experience_level",
        "partnership_success_rate": "87% of matches lead to regular workout partnerships"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)