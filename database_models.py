"""
Database Models for Family & Friends Fitness Tracking

This module defines the SQLite database schema and models for:
- Users and authentication
- Fitness groups and memberships  
- Shared workouts and sessions
- Challenges and progress tracking
- Activity feeds and social interactions

Author: Fitness MCP Team
Date: September 2025
"""

import sqlite3
import hashlib
import secrets
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class User:
    """User model for authentication and profile data"""
    user_id: str
    username: str
    email: str
    password_hash: str
    full_name: str = ""
    profile_picture: str = ""
    fitness_level: str = "beginner"  # beginner, intermediate, advanced
    created_at: str = ""
    is_active: bool = True


@dataclass
class FitnessGroup:
    """Model for family/friends fitness groups"""
    group_id: str
    name: str
    group_type: str  # family, friends, workout_buddies
    description: str
    creator_id: str
    invite_code: str
    privacy_level: str  # public, friends, family, private
    created_at: str
    is_active: bool = True
    member_count: int = 0


@dataclass
class GroupMembership:
    """Model for user memberships in groups"""
    membership_id: str
    user_id: str
    group_id: str
    role: str  # admin, moderator, member
    joined_at: str
    is_active: bool = True


@dataclass
class SharedWorkout:
    """Model for workouts shared within groups"""
    workout_id: str
    creator_id: str
    name: str
    description: str
    workout_type: str  # strength, cardio, flexibility, sports
    difficulty_level: str  # beginner, intermediate, advanced
    estimated_duration: int  # minutes
    exercises: str  # JSON string of exercise list
    tags: str  # JSON string of tags
    created_at: str
    is_active: bool = True


@dataclass
class WorkoutSession:
    """Model for individual workout session tracking"""
    session_id: str
    user_id: str
    workout_id: str
    group_id: str
    started_at: str
    completed_at: Optional[str] = None
    duration_minutes: Optional[int] = None
    calories_burned: Optional[int] = None
    exercises_completed: str = "[]"  # JSON string
    notes: str = ""
    achievements: str = "[]"  # JSON string
    status: str = "in_progress"  # planned, in_progress, completed, missed


@dataclass
class GroupChallenge:
    """Model for group fitness challenges"""
    challenge_id: str
    group_id: str
    creator_id: str
    name: str
    description: str
    challenge_type: str  # workout_frequency, step_count, calories_burned, distance
    target_metrics: str  # JSON string with target values
    start_date: str
    end_date: str
    rewards: str  # JSON string of rewards
    created_at: str
    is_active: bool = True


@dataclass
class ChallengeParticipant:
    """Model for challenge participation tracking"""
    participation_id: str
    challenge_id: str
    user_id: str
    joined_at: str
    current_progress: str = "{}"  # JSON string with progress data
    is_active: bool = True


@dataclass
class ActivityFeed:
    """Model for group activity feed entries"""
    activity_id: str
    user_id: str
    group_id: str
    activity_type: str  # workout_completed, challenge_joined, group_joined, etc.
    activity_data: str  # JSON string with activity details
    created_at: str
    is_visible: bool = True


class FitnessDatabaseManager:
    """Database manager for all fitness tracking data"""
    
    def __init__(self, db_path: str = "fitness_family_friends.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        return conn
    
    def init_database(self):
        """Create all tables and indexes"""
        with self.get_connection() as conn:
            # Users table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT DEFAULT '',
                    profile_picture TEXT DEFAULT '',
                    fitness_level TEXT DEFAULT 'beginner',
                    created_at TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            # Fitness groups table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS fitness_groups (
                    group_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    group_type TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    creator_id TEXT NOT NULL,
                    invite_code TEXT UNIQUE NOT NULL,
                    privacy_level TEXT DEFAULT 'friends',
                    created_at TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (creator_id) REFERENCES users (user_id)
                )
            """)
            
            # Group memberships table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS group_memberships (
                    membership_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    group_id TEXT NOT NULL,
                    role TEXT DEFAULT 'member',
                    joined_at TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (group_id) REFERENCES fitness_groups (group_id),
                    UNIQUE(user_id, group_id)
                )
            """)
            
            # Shared workouts table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS shared_workouts (
                    workout_id TEXT PRIMARY KEY,
                    creator_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    workout_type TEXT DEFAULT 'strength',
                    difficulty_level TEXT DEFAULT 'intermediate',
                    estimated_duration INTEGER DEFAULT 60,
                    exercises TEXT DEFAULT '[]',
                    tags TEXT DEFAULT '[]',
                    created_at TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (creator_id) REFERENCES users (user_id)
                )
            """)
            
            # Workout sessions table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workout_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    workout_id TEXT NOT NULL,
                    group_id TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    completed_at TEXT,
                    duration_minutes INTEGER,
                    calories_burned INTEGER,
                    exercises_completed TEXT DEFAULT '[]',
                    notes TEXT DEFAULT '',
                    achievements TEXT DEFAULT '[]',
                    status TEXT DEFAULT 'in_progress',
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (workout_id) REFERENCES shared_workouts (workout_id),
                    FOREIGN KEY (group_id) REFERENCES fitness_groups (group_id)
                )
            """)
            
            # Group challenges table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS group_challenges (
                    challenge_id TEXT PRIMARY KEY,
                    group_id TEXT NOT NULL,
                    creator_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    challenge_type TEXT NOT NULL,
                    target_metrics TEXT DEFAULT '{}',
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    rewards TEXT DEFAULT '[]',
                    is_active BOOLEAN DEFAULT 1,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (group_id) REFERENCES fitness_groups (group_id),
                    FOREIGN KEY (creator_id) REFERENCES users (user_id)
                )
            """)
            
            # Challenge participants table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS challenge_participants (
                    participation_id TEXT PRIMARY KEY,
                    challenge_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    joined_at TEXT NOT NULL,
                    current_progress TEXT DEFAULT '{}',
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (challenge_id) REFERENCES group_challenges (challenge_id),
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    UNIQUE(challenge_id, user_id)
                )
            """)
            
            # Activity feed table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS activity_feed (
                    activity_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    group_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    activity_data TEXT DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    is_visible BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (group_id) REFERENCES fitness_groups (group_id)
                )
            """)
            
            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_groups_invite_code ON fitness_groups(invite_code)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_memberships_user_id ON group_memberships(user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_memberships_group_id ON group_memberships(group_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON workout_sessions(user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_group_id ON workout_sessions(group_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_challenges_group_id ON group_challenges(group_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_activity_group_id ON activity_feed(group_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_activity_created_at ON activity_feed(created_at)")
            
            conn.commit()
    
    def create_sample_data(self):
        """Create sample users and groups for testing"""
        with self.get_connection() as conn:
            # Check if sample data already exists
            result = conn.execute("SELECT COUNT(*) FROM users").fetchone()
            if result[0] > 0:
                return  # Sample data already exists
            
            # Create sample users
            users = [
                ("user_123", "john_smith", "john@example.com", "Test Family Dad"),
                ("user_456", "jane_smith", "jane@example.com", "Test Family Mom"), 
                ("user_789", "alex_smith", "alex@example.com", "Test Family Kid"),
                ("user_101", "mike_jones", "mike@example.com", "Family Friend"),
                ("user_202", "sarah_doe", "sarah@example.com", "Workout Buddy")
            ]
            
            now = datetime.now().isoformat()
            for user_id, username, email, full_name in users:
                password_hash = hashlib.sha256(b"password123").hexdigest()
                conn.execute("""
                    INSERT INTO users (user_id, username, email, password_hash, full_name, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, username, email, password_hash, full_name, now))
            
            # Create sample groups
            groups = [
                ("group_family_1", "Smith Family Fitness", "family", "Our family fitness journey", "user_123", "FAMILY2024"),
                ("group_friends_1", "Running Buddies", "friends", "Weekend running group", "user_101", "RUN2024"),
                ("group_workout_1", "Gym Warriors", "workout_buddies", "Strength training group", "user_202", "GYM2024")
            ]
            
            for group_id, name, group_type, description, creator_id, invite_code in groups:
                conn.execute("""
                    INSERT INTO fitness_groups (group_id, name, group_type, description, creator_id, invite_code, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (group_id, name, group_type, description, creator_id, invite_code, now))
            
            # Create sample memberships
            memberships = [
                # Smith family members
                ("mem_1", "user_123", "group_family_1", "admin"),
                ("mem_2", "user_456", "group_family_1", "member"),
                ("mem_3", "user_789", "group_family_1", "member"),
                # Running buddies
                ("mem_4", "user_101", "group_friends_1", "admin"),
                ("mem_5", "user_123", "group_friends_1", "member"),
                ("mem_6", "user_202", "group_friends_1", "member"),
                # Gym warriors
                ("mem_7", "user_202", "group_workout_1", "admin"),
                ("mem_8", "user_456", "group_workout_1", "member")
            ]
            
            for membership_id, user_id, group_id, role in memberships:
                conn.execute("""
                    INSERT INTO group_memberships (membership_id, user_id, group_id, role, joined_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (membership_id, user_id, group_id, role, now))
            
            # Create sample challenges
            end_date = (datetime.now() + timedelta(days=30)).isoformat()
            challenges = [
                ("challenge_1", "group_family_1", "user_123", "30-Day Step Challenge", "Get 10,000 steps daily", "step_count"),
                ("challenge_2", "group_friends_1", "user_101", "Weekly 5K Run", "Complete 3 runs per week", "workout_frequency")
            ]
            
            for challenge_id, group_id, creator_id, name, description, challenge_type in challenges:
                target_metrics = json.dumps({"daily_steps": 10000} if challenge_type == "step_count" else {"weekly_workouts": 3})
                conn.execute("""
                    INSERT INTO group_challenges (challenge_id, group_id, creator_id, name, description, 
                                                challenge_type, target_metrics, start_date, end_date, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (challenge_id, group_id, creator_id, name, description, challenge_type, target_metrics, now, end_date, now))
            
            conn.commit()
            print("✅ Sample data created successfully!")
    
    def generate_id(self, prefix: str = "") -> str:
        """Generate a unique ID with optional prefix"""
        return f"{prefix}_{secrets.token_urlsafe(8)}" if prefix else secrets.token_urlsafe(12)
    
    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{password_hash.hex()}"
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, stored_hash = password_hash.split(':')
            password_hash_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return stored_hash == password_hash_check.hex()
        except:
            return False


if __name__ == "__main__":
    # Initialize database and create sample data
    print("🔄 Initializing Family & Friends Fitness Database...")
    db_manager = FitnessDatabaseManager()
    db_manager.create_sample_data()
    print("🎉 Database setup complete!")
    print("\n📊 Database Statistics:")
    
    with db_manager.get_connection() as conn:
        tables = ["users", "fitness_groups", "group_memberships", "group_challenges"]
        for table in tables:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  - {table}: {count} records")