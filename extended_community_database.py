"""
Database Schema Extensions for Broader Social Network
Extending the existing fitness database to support community features
"""

from comprehensive_fitness_database import ComprehensiveFitnessDatabase
import sqlite3
from dataclasses import dataclass
from typing import List, Optional, Dict
import json
from datetime import datetime

@dataclass
class CommunityGroup:
    """Extended group model for broader social network"""
    group_id: str
    name: str
    group_type: str  # family, friends, public_group, fitness_club, etc.
    privacy_level: str  # private, friends, local, public, invite_only
    creator_id: str
    description: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    member_limit: Optional[int] = None
    activity_focus: List[str] = None  # ["strength", "cardio", "yoga"]
    experience_levels: List[str] = None  # ["beginner", "intermediate", "advanced"]
    meeting_schedule: Optional[str] = None
    group_rules: Optional[str] = None
    moderation_enabled: bool = False
    verification_required: bool = False
    community_features: Dict = None
    created_at: str = ""
    is_discoverable: bool = True
    tags: List[str] = None

@dataclass
class CommunityMember:
    """Extended member model with community features"""
    user_id: str
    group_id: str
    role: str  # member, moderator, admin, mentor, trainee
    join_date: str
    status: str  # active, inactive, pending, banned
    reputation_score: int = 0
    skills_offered: List[str] = None  # ["olympic_lifting", "nutrition"]
    skills_seeking: List[str] = None  # ["mobility", "meal_prep"]
    mentor_status: str = "none"  # none, seeking_mentor, is_mentor, both
    community_contributions: int = 0  # posts, helpful answers, etc.
    badges_earned: List[str] = None
    last_active: str = ""

@dataclass
class SkillSharingSession:
    """Skill sharing between community members"""
    session_id: str
    instructor_id: str
    skill_type: str
    title: str
    description: str
    max_participants: int
    current_participants: int
    session_format: str  # in_person, virtual, hybrid
    skill_level: str
    duration_minutes: int
    location: Optional[str] = None
    session_date: str
    session_time: str
    fee_credits: int = 0
    certification_offered: bool = False
    materials_provided: List[str] = None
    prerequisites: List[str] = None
    created_at: str = ""
    status: str = "scheduled"  # scheduled, in_progress, completed, cancelled

@dataclass
class CommunityEvent:
    """Community-wide fitness events"""
    event_id: str
    organizer_id: str
    title: str
    description: str
    event_type: str  # workout, competition, charity, social, educational
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    start_date: str
    end_date: str
    max_participants: Optional[int] = None
    current_participants: int = 0
    registration_fee: float = 0.0
    charity_cause: Optional[str] = None
    skill_level: str = "all_levels"
    equipment_needed: List[str] = None
    prizes: List[str] = None
    sponsors: List[str] = None
    created_at: str = ""
    status: str = "upcoming"  # upcoming, active, completed, cancelled

class ExtendedFitnessDatabase(ComprehensiveFitnessDatabase):
    """Extends the comprehensive fitness database with community features"""
    
    def __init__(self, db_path: str = "extended_fitness_community.db"):
        super().__init__(db_path)
        self._create_community_tables()
        self._add_community_sample_data()
    
    def _create_community_tables(self):
        """Create additional tables for community features"""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Extended groups table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS community_groups (
                    group_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    group_type TEXT NOT NULL,
                    privacy_level TEXT NOT NULL,
                    creator_id TEXT NOT NULL,
                    description TEXT,
                    location TEXT,
                    latitude REAL,
                    longitude REAL,
                    member_limit INTEGER,
                    activity_focus TEXT,  -- JSON array
                    experience_levels TEXT,  -- JSON array
                    meeting_schedule TEXT,
                    group_rules TEXT,
                    moderation_enabled BOOLEAN DEFAULT FALSE,
                    verification_required BOOLEAN DEFAULT FALSE,
                    community_features TEXT,  -- JSON object
                    created_at TEXT,
                    is_discoverable BOOLEAN DEFAULT TRUE,
                    tags TEXT,  -- JSON array
                    FOREIGN KEY (creator_id) REFERENCES users (user_id)
                )
            ''')
            
            # Extended members table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS community_members (
                    user_id TEXT,
                    group_id TEXT,
                    role TEXT DEFAULT 'member',
                    join_date TEXT,
                    status TEXT DEFAULT 'active',
                    reputation_score INTEGER DEFAULT 0,
                    skills_offered TEXT,  -- JSON array
                    skills_seeking TEXT,  -- JSON array
                    mentor_status TEXT DEFAULT 'none',
                    community_contributions INTEGER DEFAULT 0,
                    badges_earned TEXT,  -- JSON array
                    last_active TEXT,
                    PRIMARY KEY (user_id, group_id),
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (group_id) REFERENCES community_groups (group_id)
                )
            ''')
            
            # Skill sharing sessions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skill_sharing_sessions (
                    session_id TEXT PRIMARY KEY,
                    instructor_id TEXT NOT NULL,
                    skill_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    max_participants INTEGER,
                    current_participants INTEGER DEFAULT 0,
                    session_format TEXT DEFAULT 'in_person',
                    skill_level TEXT DEFAULT 'beginner',
                    duration_minutes INTEGER,
                    location TEXT,
                    session_date TEXT,
                    session_time TEXT,
                    fee_credits INTEGER DEFAULT 0,
                    certification_offered BOOLEAN DEFAULT FALSE,
                    materials_provided TEXT,  -- JSON array
                    prerequisites TEXT,  -- JSON array
                    created_at TEXT,
                    status TEXT DEFAULT 'scheduled',
                    FOREIGN KEY (instructor_id) REFERENCES users (user_id)
                )
            ''')
            
            # Community events
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS community_events (
                    event_id TEXT PRIMARY KEY,
                    organizer_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    event_type TEXT NOT NULL,
                    location TEXT NOT NULL,
                    latitude REAL,
                    longitude REAL,
                    start_date TEXT,
                    end_date TEXT,
                    max_participants INTEGER,
                    current_participants INTEGER DEFAULT 0,
                    registration_fee REAL DEFAULT 0.0,
                    charity_cause TEXT,
                    skill_level TEXT DEFAULT 'all_levels',
                    equipment_needed TEXT,  -- JSON array
                    prizes TEXT,  -- JSON array
                    sponsors TEXT,  -- JSON array
                    created_at TEXT,
                    status TEXT DEFAULT 'upcoming',
                    FOREIGN KEY (organizer_id) REFERENCES users (user_id)
                )
            ''')
            
            # Global leaderboards
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS global_leaderboards (
                    user_id TEXT,
                    category TEXT,
                    timeframe TEXT,
                    score REAL,
                    rank INTEGER,
                    additional_metrics TEXT,  -- JSON object
                    last_updated TEXT,
                    PRIMARY KEY (user_id, category, timeframe),
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Workout partnerships
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workout_partnerships (
                    partnership_id TEXT PRIMARY KEY,
                    user1_id TEXT,
                    user2_id TEXT,
                    partnership_type TEXT,  -- regular, temporary, mentor_mentee
                    status TEXT DEFAULT 'active',
                    shared_interests TEXT,  -- JSON array
                    preferred_schedule TEXT,  -- JSON array
                    location_preference TEXT,
                    compatibility_score REAL,
                    created_at TEXT,
                    last_workout_together TEXT,
                    total_workouts_together INTEGER DEFAULT 0,
                    FOREIGN KEY (user1_id) REFERENCES users (user_id),
                    FOREIGN KEY (user2_id) REFERENCES users (user_id)
                )
            ''')
    
    def _add_community_sample_data(self):
        """Add sample data for community features"""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Sample community groups
            sample_groups = [
                CommunityGroup(
                    group_id="powerlifters_downtown",
                    name="Downtown Powerlifters",
                    group_type="sport_community",
                    privacy_level="public",
                    creator_id="user_001",
                    description="Serious powerlifting community in downtown area",
                    location="Downtown Gym District",
                    latitude=40.7589,
                    longitude=-73.9851,
                    member_limit=200,
                    activity_focus=json.dumps(["powerlifting", "strength_training"]),
                    experience_levels=json.dumps(["intermediate", "advanced"]),
                    meeting_schedule="Mon/Wed/Fri 6:00 PM",
                    group_rules="Squat 1.5x bodyweight minimum to join",
                    moderation_enabled=True,
                    verification_required=False,
                    community_features=json.dumps({
                        "public_leaderboards": True,
                        "skill_sharing": True,
                        "local_events": True,
                        "mentor_program": True
                    }),
                    created_at=datetime.now().isoformat(),
                    is_discoverable=True,
                    tags=json.dumps(["powerlifting", "strength", "downtown", "competitive"])
                ),
                CommunityGroup(
                    group_id="family_fitness_central",
                    name="Central Park Family Fitness",
                    group_type="public_group",
                    privacy_level="local",
                    creator_id="user_002",
                    description="Family-friendly fitness activities in Central Park",
                    location="Central Park, NYC",
                    latitude=40.7829,
                    longitude=-73.9654,
                    member_limit=100,
                    activity_focus=json.dumps(["family_workouts", "outdoor_fitness", "kids_activities"]),
                    experience_levels=json.dumps(["beginner", "intermediate"]),
                    meeting_schedule="Saturdays 9:00 AM",
                    group_rules="Family-friendly environment, children welcome",
                    moderation_enabled=True,
                    verification_required=False,
                    community_features=json.dumps({
                        "skill_sharing": True,
                        "local_events": True,
                        "achievement_badges": True
                    }),
                    created_at=datetime.now().isoformat(),
                    is_discoverable=True,
                    tags=json.dumps(["family", "outdoor", "kids", "beginner_friendly"])
                )
            ]
            
            for group in sample_groups:
                cursor.execute('''
                    INSERT OR IGNORE INTO community_groups VALUES 
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    group.group_id, group.name, group.group_type, group.privacy_level,
                    group.creator_id, group.description, group.location, group.latitude,
                    group.longitude, group.member_limit, group.activity_focus,
                    group.experience_levels, group.meeting_schedule, group.group_rules,
                    group.moderation_enabled, group.verification_required,
                    group.community_features, group.created_at, group.is_discoverable,
                    group.tags
                ))
            
            # Sample skill sharing sessions
            sample_sessions = [
                SkillSharingSession(
                    session_id="olympic_lifting_101",
                    instructor_id="user_003",
                    skill_type="olympic_lifting",
                    title="Olympic Lifting Fundamentals",
                    description="Learn proper technique for snatch and clean & jerk",
                    max_participants=8,
                    current_participants=5,
                    session_format="in_person",
                    skill_level="beginner",
                    duration_minutes=90,
                    location="Iron Paradise Gym",
                    session_date="2025-10-01",
                    session_time="10:00",
                    fee_credits=50,
                    certification_offered=False,
                    materials_provided=json.dumps(["technique_guide", "video_analysis"]),
                    prerequisites=json.dumps(["basic_barbell_experience"]),
                    created_at=datetime.now().isoformat(),
                    status="scheduled"
                )
            ]
            
            for session in sample_sessions:
                cursor.execute('''
                    INSERT OR IGNORE INTO skill_sharing_sessions VALUES 
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session.session_id, session.instructor_id, session.skill_type,
                    session.title, session.description, session.max_participants,
                    session.current_participants, session.session_format,
                    session.skill_level, session.duration_minutes, session.location,
                    session.session_date, session.session_time, session.fee_credits,
                    session.certification_offered, session.materials_provided,
                    session.prerequisites, session.created_at, session.status
                ))

if __name__ == "__main__":
    # Initialize extended database
    db = ExtendedFitnessDatabase()
    print("✅ Extended Community Database initialized successfully!")
    print("🌐 Ready for broader social network features!")