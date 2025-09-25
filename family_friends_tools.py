"""
Family & Friends Fitness Tracking Tools

This module provides collaborative fitness tracking capabilities including:
- Family group creation and management
- Friend connections and shared workouts
- Group challenges and competitions
- Real-time workout sync between users
- Collaborative training programs
- Privacy controls for sharing preferences
- Group progress analytics and leaderboards

Author: Fitness MCP Team  
Date: September 2025
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum


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


@dataclass
class FitnessGroup:
    """Represents a family or friends fitness group."""
    group_id: str
    name: str
    description: str
    group_type: str  # family, friends, workout_buddies, challenge
    creator_id: str
    members: List[Dict]
    created_date: str
    privacy_level: PrivacyLevel
    group_goals: List[Dict]
    is_active: bool = True


@dataclass 
class SharedWorkout:
    """Represents a workout that can be shared/tracked with others."""
    workout_id: str
    name: str
    description: str
    creator_id: str
    workout_type: str  # strength, cardio, yoga, etc.
    exercises: List[Dict]
    estimated_duration: int  # minutes
    difficulty_level: str
    shared_with: List[str]  # user IDs
    group_ids: List[str]
    created_date: str
    tags: List[str]


@dataclass
class GroupChallenge:
    """Represents a fitness challenge for groups."""
    challenge_id: str
    name: str
    description: str
    challenge_type: str  # step_count, workout_frequency, strength_goals
    group_id: str
    creator_id: str
    start_date: str
    end_date: str
    participants: List[str]
    target_metrics: Dict
    current_standings: List[Dict]
    prizes_rewards: List[str]
    is_active: bool = True


@dataclass
class WorkoutSession:
    """Represents a completed workout session with sharing info."""
    session_id: str
    user_id: str
    workout_id: str
    start_time: str
    end_time: Optional[str]
    status: WorkoutStatus
    exercises_completed: List[Dict]
    notes: str
    shared_with_groups: List[str]
    privacy_level: PrivacyLevel
    achievements_unlocked: List[str]
    social_reactions: List[Dict]  # likes, comments, encouragement


class FamilyFriendsTools:
    """Tools for collaborative family and friends fitness tracking."""
    
    def __init__(self):
        self.groups_database = {}
        self.shared_workouts = {}
        self.group_challenges = {}
        self.workout_sessions = {}
        self.user_connections = {}
        
    async def create_fitness_group(self, arguments: Dict) -> Dict:
        """Create a new family or friends fitness group."""
        group_name = arguments.get("group_name", "")
        group_type = arguments.get("group_type", "friends")  # family, friends, workout_buddies
        creator_id = arguments.get("creator_id", "")
        description = arguments.get("description", "")
        privacy_level = arguments.get("privacy_level", "friends")
        initial_members = arguments.get("initial_members", [])
        
        if not group_name or not creator_id:
            return {
                "error": "Group name and creator ID are required",
                "group_created": False
            }
        
        group_id = f"group_{len(self.groups_database) + 1}"
        
        # Add creator as first member
        members = [{
            "user_id": creator_id,
            "role": "admin",
            "joined_date": datetime.now().isoformat(),
            "is_active": True
        }]
        
        # Add initial members
        for member_id in initial_members:
            members.append({
                "user_id": member_id,
                "role": "member", 
                "joined_date": datetime.now().isoformat(),
                "is_active": True,
                "invitation_status": "pending"
            })
        
        fitness_group = FitnessGroup(
            group_id=group_id,
            name=group_name,
            description=description,
            group_type=group_type,
            creator_id=creator_id,
            members=members,
            created_date=datetime.now().isoformat(),
            privacy_level=PrivacyLevel(privacy_level),
            group_goals=[],
            is_active=True
        )
        
        self.groups_database[group_id] = fitness_group
        
        return {
            "group_created": True,
            "group_id": group_id,
            "group_details": asdict(fitness_group),
            "invite_code": f"JOIN-{group_id.upper()}",
            "member_count": len(members),
            "next_steps": [
                "Share the invite code with family/friends",
                "Set group fitness goals together", 
                "Create shared workout plans",
                "Start tracking progress as a team"
            ]
        }
    
    async def join_fitness_group(self, arguments: Dict) -> Dict:
        """Join an existing fitness group via invite code."""
        user_id = arguments.get("user_id", "")
        invite_code = arguments.get("invite_code", "")
        user_name = arguments.get("user_name", "New Member")
        
        if not user_id or not invite_code:
            return {
                "error": "User ID and invite code are required",
                "joined": False
            }
        
        # Extract group ID from invite code
        if not invite_code.startswith("JOIN-"):
            return {
                "error": "Invalid invite code format",
                "joined": False
            }
        
        group_id = invite_code.replace("JOIN-", "").lower()
        
        if group_id not in self.groups_database:
            return {
                "error": "Group not found or invite code expired",
                "joined": False
            }
        
        group = self.groups_database[group_id]
        
        # Check if user is already a member
        existing_member = next((m for m in group.members if m["user_id"] == user_id), None)
        if existing_member:
            return {
                "error": "You are already a member of this group",
                "joined": False
            }
        
        # Add user to group
        new_member = {
            "user_id": user_id,
            "user_name": user_name,
            "role": "member",
            "joined_date": datetime.now().isoformat(),
            "is_active": True,
            "invitation_status": "accepted"
        }
        
        group.members.append(new_member)
        
        return {
            "joined": True,
            "group_id": group_id,
            "group_name": group.name,
            "group_type": group.group_type,
            "member_count": len(group.members),
            "welcome_message": f"Welcome to {group.name}! Start tracking workouts with your {group.group_type}.",
            "group_goals": group.group_goals,
            "recent_activity": self._get_group_recent_activity(group_id)
        }
    
    async def create_shared_workout(self, arguments: Dict) -> Dict:
        """Create a workout that can be shared with family/friends."""
        creator_id = arguments.get("creator_id", "")
        workout_name = arguments.get("workout_name", "")
        workout_type = arguments.get("workout_type", "strength")
        exercises = arguments.get("exercises", [])
        share_with_groups = arguments.get("share_with_groups", [])
        difficulty = arguments.get("difficulty", "intermediate")
        estimated_duration = arguments.get("estimated_duration", 60)
        
        if not creator_id or not workout_name or not exercises:
            return {
                "error": "Creator ID, workout name, and exercises are required",
                "workout_created": False
            }
        
        workout_id = f"shared_workout_{len(self.shared_workouts) + 1}"
        
        # Determine who can access this workout
        shared_with = []
        for group_id in share_with_groups:
            if group_id in self.groups_database:
                group = self.groups_database[group_id]
                shared_with.extend([m["user_id"] for m in group.members])
        
        shared_workout = SharedWorkout(
            workout_id=workout_id,
            name=workout_name,
            description=arguments.get("description", f"Shared {workout_type} workout"),
            creator_id=creator_id,
            workout_type=workout_type,
            exercises=exercises,
            estimated_duration=estimated_duration,
            difficulty_level=difficulty,
            shared_with=list(set(shared_with)),  # Remove duplicates
            group_ids=share_with_groups,
            created_date=datetime.now().isoformat(),
            tags=arguments.get("tags", [])
        )
        
        self.shared_workouts[workout_id] = shared_workout
        
        return {
            "workout_created": True,
            "workout_id": workout_id,
            "workout_details": asdict(shared_workout),
            "shared_with_count": len(shared_with),
            "group_notifications": [
                f"New workout '{workout_name}' shared with {group_id}" 
                for group_id in share_with_groups
            ],
            "suggested_schedule": self._suggest_group_workout_times(share_with_groups)
        }
    
    async def start_group_workout_session(self, arguments: Dict) -> Dict:
        """Start a workout session that will be tracked with family/friends."""
        user_id = arguments.get("user_id", "")
        workout_id = arguments.get("workout_id", "")
        group_ids = arguments.get("group_ids", [])
        privacy_level = arguments.get("privacy_level", "friends")
        
        if not user_id or not workout_id:
            return {
                "error": "User ID and workout ID are required",
                "session_started": False
            }
        
        session_id = f"session_{user_id}_{len(self.workout_sessions) + 1}"
        
        workout_session = WorkoutSession(
            session_id=session_id,
            user_id=user_id,
            workout_id=workout_id,
            start_time=datetime.now().isoformat(),
            end_time=None,
            status=WorkoutStatus.IN_PROGRESS,
            exercises_completed=[],
            notes="",
            shared_with_groups=group_ids,
            privacy_level=PrivacyLevel(privacy_level),
            achievements_unlocked=[],
            social_reactions=[]
        )
        
        self.workout_sessions[session_id] = workout_session
        
        # Notify group members
        notifications = []
        for group_id in group_ids:
            if group_id in self.groups_database:
                group = self.groups_database[group_id]
                notifications.append({
                    "group_id": group_id,
                    "group_name": group.name,
                    "message": f"🏋️‍♂️ {user_id} started working out! Join them or send encouragement!"
                })
        
        return {
            "session_started": True,
            "session_id": session_id,
            "workout_details": self.shared_workouts.get(workout_id, {}),
            "live_tracking_enabled": True,
            "group_notifications_sent": notifications,
            "encouragement_options": [
                "💪 Keep going!",
                "🔥 You've got this!",
                "⚡ Beast mode activated!",
                "🏆 Crushing it!"
            ],
            "live_updates_url": f"/api/social/live-workout/{session_id}"
        }
    
    async def complete_workout_session(self, arguments: Dict) -> Dict:
        """Complete a workout session and share results with groups."""
        session_id = arguments.get("session_id", "")
        exercises_completed = arguments.get("exercises_completed", [])
        session_notes = arguments.get("notes", "")
        achievements = arguments.get("achievements", [])
        
        if session_id not in self.workout_sessions:
            return {
                "error": "Workout session not found",
                "session_completed": False
            }
        
        session = self.workout_sessions[session_id]
        session.end_time = datetime.now().isoformat()
        session.status = WorkoutStatus.COMPLETED
        session.exercises_completed = exercises_completed
        session.notes = session_notes
        session.achievements_unlocked = achievements
        
        # Calculate session stats
        start_time = datetime.fromisoformat(session.start_time)
        end_time = datetime.fromisoformat(session.end_time)
        duration_minutes = int((end_time - start_time).total_seconds() / 60)
        
        # Update group progress
        group_updates = []
        for group_id in session.shared_with_groups:
            group_updates.append(self._update_group_progress(group_id, session))
        
        return {
            "session_completed": True,
            "session_id": session_id,
            "session_stats": {
                "duration_minutes": duration_minutes,
                "exercises_completed": len(exercises_completed),
                "achievements_unlocked": len(achievements),
                "calories_estimated": duration_minutes * 8  # Rough estimate
            },
            "group_updates": group_updates,
            "social_sharing": {
                "auto_post": f"💪 Just completed a {duration_minutes}-minute workout!",
                "achievements_to_celebrate": achievements,
                "encouragement_received": len(session.social_reactions)
            },
            "next_suggestions": [
                "Share your workout highlights",
                "Challenge a family member to beat your time",
                "Plan your next group workout session"
            ]
        }
    
    async def create_group_challenge(self, arguments: Dict) -> Dict:
        """Create a fitness challenge for family/friends groups."""
        creator_id = arguments.get("creator_id", "")
        group_id = arguments.get("group_id", "")
        challenge_name = arguments.get("challenge_name", "")
        challenge_type = arguments.get("challenge_type", "workout_frequency")
        duration_days = arguments.get("duration_days", 30)
        target_metrics = arguments.get("target_metrics", {})
        
        if not all([creator_id, group_id, challenge_name]):
            return {
                "error": "Creator ID, group ID, and challenge name are required",
                "challenge_created": False
            }
        
        if group_id not in self.groups_database:
            return {
                "error": "Group not found",
                "challenge_created": False
            }
        
        challenge_id = f"challenge_{len(self.group_challenges) + 1}"
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_days)
        
        group = self.groups_database[group_id]
        participants = [m["user_id"] for m in group.members if m["is_active"]]
        
        group_challenge = GroupChallenge(
            challenge_id=challenge_id,
            name=challenge_name,
            description=arguments.get("description", f"Family/Friends {challenge_type} challenge"),
            challenge_type=challenge_type,
            group_id=group_id,
            creator_id=creator_id,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            participants=participants,
            target_metrics=target_metrics,
            current_standings=[],
            prizes_rewards=arguments.get("rewards", ["Bragging rights!", "Winner picks next workout"]),
            is_active=True
        )
        
        self.group_challenges[challenge_id] = group_challenge
        
        return {
            "challenge_created": True,
            "challenge_id": challenge_id,
            "challenge_details": asdict(group_challenge),
            "participant_count": len(participants),
            "challenge_duration": f"{duration_days} days",
            "leaderboard_url": f"/api/social/challenge-leaderboard/{challenge_id}",
            "motivation_message": f"🏆 {challenge_name} starts now! Who will come out on top?"
        }
    
    async def get_family_friends_dashboard(self, arguments: Dict) -> Dict:
        """Get comprehensive dashboard for family/friends fitness tracking."""
        user_id = arguments.get("user_id", "")
        
        if not user_id:
            return {
                "error": "User ID is required",
                "dashboard_data": None
            }
        
        # Get user's groups
        user_groups = []
        for group_id, group in self.groups_database.items():
            if any(m["user_id"] == user_id for m in group.members):
                user_groups.append({
                    "group_id": group_id,
                    "name": group.name,
                    "type": group.group_type,
                    "member_count": len(group.members),
                    "recent_activity_count": len(self._get_group_recent_activity(group_id))
                })
        
        # Get active challenges
        active_challenges = []
        for challenge_id, challenge in self.group_challenges.items():
            if user_id in challenge.participants and challenge.is_active:
                active_challenges.append({
                    "challenge_id": challenge_id,
                    "name": challenge.name,
                    "type": challenge.challenge_type,
                    "days_remaining": self._calculate_days_remaining(challenge.end_date),
                    "your_position": self._get_user_challenge_position(challenge_id, user_id),
                    "total_participants": len(challenge.participants)
                })
        
        # Get recent group activities
        recent_activities = []
        for session_id, session in self.workout_sessions.items():
            if session.shared_with_groups and any(
                group["group_id"] in session.shared_with_groups for group in user_groups
            ):
                recent_activities.append({
                    "session_id": session_id,
                    "user_id": session.user_id,
                    "workout_type": session.workout_id,
                    "completion_time": session.end_time,
                    "status": session.status.value,
                    "reactions_count": len(session.social_reactions)
                })
        
        # Sort by most recent
        recent_activities.sort(key=lambda x: x["completion_time"] or "", reverse=True)
        
        return {
            "dashboard_data": {
                "user_groups": user_groups,
                "active_challenges": active_challenges,
                "recent_group_activities": recent_activities[:10],
                "weekly_stats": {
                    "group_workouts_completed": len([
                        s for s in self.workout_sessions.values()
                        if s.user_id == user_id and s.status == WorkoutStatus.COMPLETED
                        and s.shared_with_groups
                    ]),
                    "encouragements_sent": 15,  # Mock data
                    "challenges_participated": len(active_challenges),
                    "family_fitness_streak": 7  # Mock data
                }
            },
            "quick_actions": [
                "Create new group workout",
                "Start family challenge", 
                "Send workout encouragement",
                "Join live group session"
            ],
            "social_notifications": [
                "Mom completed her morning yoga! 🧘‍♀️",
                "Your workout buddy is crushing their deadlift challenge 💪",
                "Family step challenge ends in 3 days - you're in 2nd place! 🏃‍♂️"
            ]
        }
    
    def _get_group_recent_activity(self, group_id: str) -> List[Dict]:
        """Get recent activity for a specific group."""
        activities = []
        for session in self.workout_sessions.values():
            if group_id in session.shared_with_groups:
                activities.append({
                    "user_id": session.user_id,
                    "activity": "workout_completed",
                    "timestamp": session.end_time,
                    "details": session.workout_id
                })
        return sorted(activities, key=lambda x: x["timestamp"] or "", reverse=True)[:5]
    
    def _update_group_progress(self, group_id: str, session: WorkoutSession) -> Dict:
        """Update group progress metrics after a workout."""
        return {
            "group_id": group_id,
            "update_type": "workout_completed",
            "user_id": session.user_id,
            "contribution": {
                "workouts_count": 1,
                "duration_minutes": 45,  # Mock calculation
                "consistency_points": 10
            }
        }
    
    def _suggest_group_workout_times(self, group_ids: List[str]) -> List[str]:
        """Suggest optimal workout times for groups."""
        return [
            "Tomorrow 7:00 AM - Great for family morning routine",
            "Saturday 10:00 AM - Perfect weekend group session", 
            "Tonight 6:00 PM - After-work family fitness time"
        ]
    
    def _calculate_days_remaining(self, end_date: str) -> int:
        """Calculate days remaining in a challenge."""
        end = datetime.fromisoformat(end_date)
        now = datetime.now()
        return max(0, (end - now).days)
    
    def _get_user_challenge_position(self, challenge_id: str, user_id: str) -> int:
        """Get user's current position in a challenge."""
        # Mock implementation - would calculate from actual progress data
        return 2