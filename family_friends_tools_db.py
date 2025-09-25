"""
Family & Friends Fitness Tracking Tools - Database Version

This module provides collaborative fitness tracking capabilities with real data persistence:
- Family group creation and management with SQLite storage
- Friend connections and shared workouts with database backend
- Group challenges and competitions with progress tracking
- Real-time workout sync between users with persistent sessions
- Collaborative training programs stored in database
- Privacy controls for sharing preferences
- Group progress analytics and leaderboards from real data

Author: Fitness MCP Team  
Date: September 2025
"""

import json
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dataclasses import asdict
from enum import Enum
from database_models import (
    FitnessDatabaseManager, User, FitnessGroup, GroupMembership, 
    SharedWorkout, WorkoutSession, GroupChallenge, ChallengeParticipant, ActivityFeed
)


class RelationshipType(Enum):
    """Types of relationships between users."""
    FAMILY = "family"
    FRIEND = "friend"
    WORKOUT_BUDDY = "workout_buddy"
    TRAINER_CLIENT = "trainer_client"


class PrivacyLevel(Enum):
    """Privacy levels for sharing workout data."""
    PUBLIC = "public"
    FRIENDS = "friends" 
    FAMILY = "family"
    PRIVATE = "private"
    CUSTOM = "custom"


class WorkoutStatus(Enum):
    """Status of shared workouts."""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MISSED = "missed"


class FamilyFriendsToolsDB:
    """
    Enhanced Family & Friends Fitness Tools with Database Persistence
    
    This class provides all the collaborative fitness tracking functionality
    with real SQLite database storage instead of in-memory mock data.
    """
    
    def __init__(self, db_path: str = "fitness_family_friends.db"):
        """Initialize with database connection"""
        self.db_manager = FitnessDatabaseManager(db_path)
        print(f"✅ FamilyFriendsTools initialized with database: {db_path}")
    
    async def create_fitness_group(self, data: Dict) -> Dict:
        """Create a new family or friends fitness group with database storage"""
        try:
            group_id = self.db_manager.generate_id("group")
            invite_code = self._generate_invite_code()
            now = datetime.now().isoformat()
            
            # Insert group into database
            with self.db_manager.get_connection() as conn:
                conn.execute("""
                    INSERT INTO fitness_groups 
                    (group_id, name, group_type, description, creator_id, invite_code, privacy_level, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    group_id,
                    data["group_name"],
                    data["group_type"],
                    data.get("description", ""),
                    data["creator_id"],
                    invite_code,
                    data.get("privacy_level", "friends"),
                    now
                ))
                
                # Add creator as admin member
                membership_id = self.db_manager.generate_id("mem")
                conn.execute("""
                    INSERT INTO group_memberships (membership_id, user_id, group_id, role, joined_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (membership_id, data["creator_id"], group_id, "admin", now))
                
                # Add initial members if provided
                for member_id in data.get("initial_members", []):
                    mem_id = self.db_manager.generate_id("mem")
                    conn.execute("""
                        INSERT INTO group_memberships (membership_id, user_id, group_id, role, joined_at)
                        VALUES (?, ?, ?, ?, ?)
                    """, (mem_id, member_id, group_id, "member", now))
                
                # Add activity to feed
                activity_id = self.db_manager.generate_id("act")
                activity_data = json.dumps({
                    "group_name": data["group_name"],
                    "group_type": data["group_type"]
                })
                conn.execute("""
                    INSERT INTO activity_feed (activity_id, user_id, group_id, activity_type, activity_data, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (activity_id, data["creator_id"], group_id, "group_created", activity_data, now))
                
                conn.commit()
            
            return {
                "group_created": True,
                "group_id": group_id,
                "invite_code": invite_code,
                "message": f"'{data['group_name']}' group created successfully!",
                "created_at": now,
                "member_count": 1 + len(data.get("initial_members", []))
            }
            
        except Exception as e:
            return {
                "group_created": False,
                "error": f"Failed to create group: {str(e)}"
            }
    
    async def join_fitness_group(self, data: Dict) -> Dict:
        """Join an existing fitness group using invite code"""
        try:
            with self.db_manager.get_connection() as conn:
                # Find group by invite code
                group = conn.execute("""
                    SELECT group_id, name, group_type, creator_id 
                    FROM fitness_groups 
                    WHERE invite_code = ? AND is_active = 1
                """, (data["invite_code"],)).fetchone()
                
                if not group:
                    return {
                        "joined": False,
                        "error": "Invalid invite code or group not found"
                    }
                
                group_id = group["group_id"]
                
                # Check if user is already a member
                existing = conn.execute("""
                    SELECT membership_id FROM group_memberships 
                    WHERE user_id = ? AND group_id = ? AND is_active = 1
                """, (data["user_id"], group_id)).fetchone()
                
                if existing:
                    return {
                        "joined": False,
                        "error": "User is already a member of this group"
                    }
                
                # Add user as member
                now = datetime.now().isoformat()
                membership_id = self.db_manager.generate_id("mem")
                conn.execute("""
                    INSERT INTO group_memberships (membership_id, user_id, group_id, role, joined_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (membership_id, data["user_id"], group_id, "member", now))
                
                # Add activity to feed
                activity_id = self.db_manager.generate_id("act")
                activity_data = json.dumps({
                    "user_name": data.get("user_name", "New Member"),
                    "group_name": group["name"]
                })
                conn.execute("""
                    INSERT INTO activity_feed (activity_id, user_id, group_id, activity_type, activity_data, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (activity_id, data["user_id"], group_id, "group_joined", activity_data, now))
                
                conn.commit()
                
                return {
                    "joined": True,
                    "group_id": group_id,
                    "group_name": group["name"],
                    "group_type": group["group_type"],
                    "message": f"Successfully joined '{group['name']}' group!",
                    "joined_at": now
                }
                
        except Exception as e:
            return {
                "joined": False,
                "error": f"Failed to join group: {str(e)}"
            }
    
    async def get_user_groups(self, user_id: str) -> Dict:
        """Get all groups for a specific user from database"""
        try:
            with self.db_manager.get_connection() as conn:
                groups = conn.execute("""
                    SELECT fg.group_id, fg.name, fg.group_type, fg.created_at, gm.role,
                           COUNT(gm2.user_id) as member_count
                    FROM fitness_groups fg
                    JOIN group_memberships gm ON fg.group_id = gm.group_id
                    LEFT JOIN group_memberships gm2 ON fg.group_id = gm2.group_id AND gm2.is_active = 1
                    WHERE gm.user_id = ? AND gm.is_active = 1 AND fg.is_active = 1
                    GROUP BY fg.group_id, fg.name, fg.group_type, fg.created_at, gm.role
                """, (user_id,)).fetchall()
                
                user_groups = []
                for group in groups:
                    user_groups.append({
                        "group_id": group["group_id"],
                        "name": group["name"],
                        "type": group["group_type"],
                        "member_count": group["member_count"],
                        "role": group["role"],
                        "created_date": group["created_at"]
                    })
                
                return {"user_groups": user_groups}
                
        except Exception as e:
            return {"user_groups": [], "error": f"Failed to get user groups: {str(e)}"}
    
    async def create_shared_workout(self, data: Dict) -> Dict:
        """Create a workout that can be shared with family/friends"""
        try:
            workout_id = self.db_manager.generate_id("workout")
            now = datetime.now().isoformat()
            
            with self.db_manager.get_connection() as conn:
                # Create the workout
                conn.execute("""
                    INSERT INTO shared_workouts 
                    (workout_id, creator_id, name, description, workout_type, 
                     difficulty_level, estimated_duration, exercises, tags, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    workout_id,
                    data["creator_id"],
                    data["workout_name"],
                    data.get("description", ""),
                    data.get("workout_type", "strength"),
                    data.get("difficulty", "intermediate"),
                    data.get("estimated_duration", 60),
                    json.dumps(data.get("exercises", [])),
                    json.dumps(data.get("tags", [])),
                    now
                ))
                
                # Add activity to feed for each group it's shared with
                for group_id in data.get("share_with_groups", []):
                    activity_id = self.db_manager.generate_id("act")
                    activity_data = json.dumps({
                        "workout_name": data["workout_name"],
                        "workout_type": data.get("workout_type", "strength"),
                        "difficulty": data.get("difficulty", "intermediate")
                    })
                    conn.execute("""
                        INSERT INTO activity_feed (activity_id, user_id, group_id, activity_type, activity_data, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (activity_id, data["creator_id"], group_id, "workout_shared", activity_data, now))
                
                conn.commit()
            
            return {
                "workout_created": True,
                "workout_id": workout_id,
                "message": f"Shared workout '{data['workout_name']}' created successfully!",
                "created_at": now,
                "shared_with_groups": len(data.get("share_with_groups", []))
            }
            
        except Exception as e:
            return {
                "workout_created": False,
                "error": f"Failed to create shared workout: {str(e)}"
            }
    
    async def start_group_workout_session(self, data: Dict) -> Dict:
        """Start a workout session that will be tracked with family/friends"""
        try:
            session_id = self.db_manager.generate_id("session")
            now = datetime.now().isoformat()
            
            with self.db_manager.get_connection() as conn:
                conn.execute("""
                    INSERT INTO workout_sessions 
                    (session_id, user_id, workout_id, group_id, started_at, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    session_id,
                    data["user_id"],
                    data["workout_id"],
                    data.get("group_ids", [None])[0] if data.get("group_ids") else None,
                    now,
                    "in_progress"
                ))
                
                # Add activity to feed
                if data.get("group_ids"):
                    for group_id in data["group_ids"]:
                        activity_id = self.db_manager.generate_id("act")
                        activity_data = json.dumps({
                            "workout_id": data["workout_id"],
                            "session_id": session_id
                        })
                        conn.execute("""
                            INSERT INTO activity_feed (activity_id, user_id, group_id, activity_type, activity_data, created_at)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (activity_id, data["user_id"], group_id, "workout_started", activity_data, now))
                
                conn.commit()
            
            return {
                "session_started": True,
                "session_id": session_id,
                "message": "Workout session started successfully!",
                "started_at": now,
                "privacy_level": data.get("privacy_level", "friends")
            }
            
        except Exception as e:
            return {
                "session_started": False,
                "error": f"Failed to start workout session: {str(e)}"
            }
    
    async def complete_workout_session(self, data: Dict) -> Dict:
        """Complete a workout session and share results with groups"""
        try:
            now = datetime.now().isoformat()
            
            with self.db_manager.get_connection() as conn:
                # Update session with completion data
                conn.execute("""
                    UPDATE workout_sessions 
                    SET completed_at = ?, exercises_completed = ?, notes = ?, 
                        achievements = ?, status = 'completed'
                    WHERE session_id = ?
                """, (
                    now,
                    json.dumps(data.get("exercises_completed", [])),
                    data.get("notes", ""),
                    json.dumps(data.get("achievements", [])),
                    data["session_id"]
                ))
                
                # Get session info for activity feed
                session = conn.execute("""
                    SELECT user_id, group_id FROM workout_sessions WHERE session_id = ?
                """, (data["session_id"],)).fetchone()
                
                if session and session["group_id"]:
                    activity_id = self.db_manager.generate_id("act")
                    activity_data = json.dumps({
                        "session_id": data["session_id"],
                        "achievements": data.get("achievements", []),
                        "notes": data.get("notes", "")
                    })
                    conn.execute("""
                        INSERT INTO activity_feed (activity_id, user_id, group_id, activity_type, activity_data, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (activity_id, session["user_id"], session["group_id"], "workout_completed", activity_data, now))
                
                conn.commit()
            
            return {
                "session_completed": True,
                "session_id": data["session_id"],
                "achievements": data.get("achievements", []),
                "message": "Workout session completed successfully!",
                "completed_at": now
            }
            
        except Exception as e:
            return {
                "session_completed": False,
                "error": f"Failed to complete workout session: {str(e)}"
            }
    
    async def create_group_challenge(self, data: Dict) -> Dict:
        """Create a fitness challenge for family/friends groups"""
        try:
            challenge_id = self.db_manager.generate_id("challenge")
            now = datetime.now().isoformat()
            end_date = (datetime.now() + timedelta(days=data.get("duration_days", 30))).isoformat()
            
            with self.db_manager.get_connection() as conn:
                conn.execute("""
                    INSERT INTO group_challenges 
                    (challenge_id, group_id, creator_id, name, description, challenge_type,
                     target_metrics, start_date, end_date, rewards, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    challenge_id,
                    data["group_id"],
                    data["creator_id"],
                    data["challenge_name"],
                    data.get("description", ""),
                    data["challenge_type"],
                    json.dumps(data.get("target_metrics", {})),
                    now,
                    end_date,
                    json.dumps(data.get("rewards", [])),
                    now
                ))
                
                # Add activity to feed
                activity_id = self.db_manager.generate_id("act")
                activity_data = json.dumps({
                    "challenge_name": data["challenge_name"],
                    "challenge_type": data["challenge_type"],
                    "duration_days": data.get("duration_days", 30)
                })
                conn.execute("""
                    INSERT INTO activity_feed (activity_id, user_id, group_id, activity_type, activity_data, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (activity_id, data["creator_id"], data["group_id"], "challenge_created", activity_data, now))
                
                conn.commit()
            
            return {
                "challenge_created": True,
                "challenge_id": challenge_id,
                "message": f"Challenge '{data['challenge_name']}' created successfully!",
                "start_date": now,
                "end_date": end_date,
                "duration_days": data.get("duration_days", 30)
            }
            
        except Exception as e:
            return {
                "challenge_created": False,
                "error": f"Failed to create challenge: {str(e)}"
            }
    
    async def get_family_friends_dashboard(self, data: Dict) -> Dict:
        """Get comprehensive dashboard for family/friends fitness tracking"""
        try:
            user_id = data["user_id"]
            
            with self.db_manager.get_connection() as conn:
                # Get user's groups
                groups = conn.execute("""
                    SELECT fg.name FROM fitness_groups fg
                    JOIN group_memberships gm ON fg.group_id = gm.group_id
                    WHERE gm.user_id = ? AND gm.is_active = 1 AND fg.is_active = 1
                """, (user_id,)).fetchall()
                
                # Get active challenges
                challenges = conn.execute("""
                    SELECT gc.challenge_id, gc.name, gc.challenge_type, gc.end_date,
                           COUNT(cp.user_id) as participant_count
                    FROM group_challenges gc
                    JOIN group_memberships gm ON gc.group_id = gm.group_id
                    LEFT JOIN challenge_participants cp ON gc.challenge_id = cp.challenge_id AND cp.is_active = 1
                    WHERE gm.user_id = ? AND gc.is_active = 1 AND gc.end_date > ?
                    GROUP BY gc.challenge_id, gc.name, gc.challenge_type, gc.end_date
                """, (user_id, datetime.now().isoformat())).fetchall()
                
                # Get recent workouts
                recent_workouts = conn.execute("""
                    SELECT sw.name FROM shared_workouts sw
                    JOIN workout_sessions ws ON sw.workout_id = ws.workout_id
                    WHERE ws.user_id = ? AND ws.status = 'completed'
                    ORDER BY ws.completed_at DESC
                    LIMIT 5
                """, (user_id,)).fetchall()
                
                # Calculate some stats (mock for now)
                week_start = (datetime.now() - timedelta(days=7)).isoformat()
                weekly_sessions = conn.execute("""
                    SELECT COUNT(*) FROM workout_sessions 
                    WHERE user_id = ? AND status = 'completed' AND completed_at > ?
                """, (user_id, week_start)).fetchone()[0]
                
                dashboard_data = {
                    "user_groups": [group["name"] for group in groups],
                    "active_challenges": [
                        {
                            "id": c["challenge_id"],
                            "name": c["name"],
                            "days_remaining": max(0, (datetime.fromisoformat(c["end_date"]) - datetime.now()).days),
                            "participant_count": c["participant_count"]
                        } for c in challenges
                    ],
                    "recent_workouts": [workout["name"] for workout in recent_workouts],
                    "weekly_stats": {
                        "workouts_completed": weekly_sessions,
                        "total_minutes": weekly_sessions * 45,  # Estimate
                        "calories_burned": weekly_sessions * 300  # Estimate
                    }
                }
                
                return {"dashboard_data": dashboard_data}
                
        except Exception as e:
            return {
                "dashboard_data": {},
                "error": f"Failed to load dashboard: {str(e)}"
            }
    
    def _get_group_recent_activity(self, group_id: str, limit: int = 20) -> List[Dict]:
        """Get recent activity feed for a group"""
        try:
            with self.db_manager.get_connection() as conn:
                activities = conn.execute("""
                    SELECT af.activity_id, af.user_id, af.activity_type, af.activity_data, af.created_at
                    FROM activity_feed af
                    WHERE af.group_id = ? AND af.is_visible = 1
                    ORDER BY af.created_at DESC
                    LIMIT ?
                """, (group_id, limit)).fetchall()
                
                return [
                    {
                        "id": activity["activity_id"],
                        "user_id": activity["user_id"],
                        "activity": activity["activity_type"],
                        "details": json.loads(activity["activity_data"]),
                        "timestamp": activity["created_at"]
                    } for activity in activities
                ]
                
        except Exception as e:
            print(f"Error getting group activity: {e}")
            return []
    
    def _generate_invite_code(self) -> str:
        """Generate a unique invite code for group joining"""
        import string
        import random
        
        # Generate a 8-character alphanumeric code
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(8))
    
    def get_group_challenges(self, group_id: str, active_only: bool = True) -> Dict:
        """Get all challenges for a specific group"""
        try:
            with self.db_manager.get_connection() as conn:
                query = """
                    SELECT gc.challenge_id, gc.name, gc.challenge_type, gc.start_date, gc.end_date, gc.is_active,
                           COUNT(cp.user_id) as participant_count
                    FROM group_challenges gc
                    LEFT JOIN challenge_participants cp ON gc.challenge_id = cp.challenge_id AND cp.is_active = 1
                    WHERE gc.group_id = ?
                """
                params = [group_id]
                
                if active_only:
                    query += " AND gc.is_active = 1 AND gc.end_date > ?"
                    params.append(datetime.now().isoformat())
                
                query += " GROUP BY gc.challenge_id, gc.name, gc.challenge_type, gc.start_date, gc.end_date, gc.is_active"
                
                challenges = conn.execute(query, params).fetchall()
                
                group_challenges = []
                for challenge in challenges:
                    end_date = datetime.fromisoformat(challenge["end_date"])
                    days_remaining = max(0, (end_date - datetime.now()).days)
                    
                    group_challenges.append({
                        "challenge_id": challenge["challenge_id"],
                        "name": challenge["name"],
                        "type": challenge["challenge_type"],
                        "days_remaining": days_remaining,
                        "participant_count": challenge["participant_count"],
                        "is_active": challenge["is_active"],
                        "start_date": challenge["start_date"],
                        "end_date": challenge["end_date"]
                    })
                
                return {"group_challenges": group_challenges}
                
        except Exception as e:
            return {
                "group_challenges": [],
                "error": f"Failed to get group challenges: {str(e)}"
            }


# For backward compatibility, create an alias
FamilyFriendsTools = FamilyFriendsToolsDB