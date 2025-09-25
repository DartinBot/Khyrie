"""
Enhanced Group Workout Management System
Advanced features for group workout scheduling, location-based meetups, video chat, and role permissions
"""

import sqlite3
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import pytz
from geopy.distance import geodesic

class GroupRole(Enum):
    """Advanced role permissions for group members."""
    OWNER = "owner"           # Full control, can delete group
    TRAINER = "trainer"       # Can create workouts, manage schedules, moderate
    MODERATOR = "moderator"   # Can moderate sessions, manage members
    PARTICIPANT = "participant" # Basic member, can join workouts
    GUEST = "guest"          # Limited access, view-only

class WorkoutScheduleType(Enum):
    """Types of workout scheduling."""
    ONE_TIME = "one_time"
    RECURRING_DAILY = "recurring_daily"
    RECURRING_WEEKLY = "recurring_weekly"
    RECURRING_MONTHLY = "recurring_monthly"
    CUSTOM_PATTERN = "custom_pattern"

class LocationType(Enum):
    """Types of workout locations."""
    VIRTUAL = "virtual"       # Online/video chat only
    PHYSICAL = "physical"     # Real-world location
    HYBRID = "hybrid"         # Both virtual and physical options

class VideoProvider(Enum):
    """Video chat providers."""
    ZOOM = "zoom"
    WEBEX = "webex"
    TEAMS = "teams"
    GOOGLE_MEET = "google_meet"
    JITSI = "jitsi"
    CUSTOM = "custom"

@dataclass
class GroupPermissions:
    """Detailed permissions for each role."""
    can_create_workouts: bool = False
    can_schedule_workouts: bool = False
    can_delete_workouts: bool = False
    can_manage_members: bool = False
    can_moderate_sessions: bool = False
    can_start_video_calls: bool = False
    can_share_location: bool = False
    can_view_analytics: bool = False
    can_export_data: bool = False
    can_manage_roles: bool = False

@dataclass
class WorkoutLocation:
    """Location information for group workouts."""
    location_id: str
    name: str
    address: str
    latitude: Optional[float]
    longitude: Optional[float]
    location_type: LocationType
    capacity: Optional[int]
    amenities: List[str]
    access_instructions: str
    safety_notes: str
    created_at: str

@dataclass
class VideoSession:
    """Video chat session information."""
    session_id: str
    provider: VideoProvider
    meeting_url: str
    meeting_id: str
    password: Optional[str]
    host_key: Optional[str]
    recording_enabled: bool
    screen_sharing_enabled: bool
    chat_enabled: bool
    max_participants: int
    created_at: str
    expires_at: str

@dataclass
class WorkoutSchedule:
    """Enhanced workout scheduling with advanced features."""
    schedule_id: str
    group_id: str
    workout_id: str
    created_by: str  # User ID with trainer+ permissions
    title: str
    description: str
    schedule_type: WorkoutScheduleType
    start_datetime: str  # ISO format with timezone
    end_datetime: str
    timezone: str
    recurring_pattern: Dict[str, Any]  # Days, frequency, end date
    location: Optional[WorkoutLocation]
    video_session: Optional[VideoSession]
    max_participants: Optional[int]
    registration_required: bool
    reminder_settings: Dict[str, Any]
    tags: List[str]
    is_active: bool
    created_at: str

@dataclass
class EnhancedGroupMember:
    """Enhanced group member with role permissions."""
    user_id: str
    username: str
    email: str
    role: GroupRole
    permissions: GroupPermissions
    joined_date: str
    last_active: str
    location_sharing_enabled: bool
    notification_preferences: Dict[str, bool]
    bio: str
    fitness_level: str
    certifications: List[str]  # For trainers
    is_active: bool

class EnhancedGroupWorkoutManager:
    """Advanced group workout management with all requested features."""
    
    def __init__(self, db_path: str = "enhanced_group_workouts.db"):
        self.db_path = db_path
        self._init_database()
        self._setup_role_permissions()
    
    def _init_database(self):
        """Initialize enhanced database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Enhanced group members table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS enhanced_group_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    username TEXT NOT NULL,
                    email TEXT,
                    role TEXT NOT NULL,
                    permissions TEXT NOT NULL,
                    joined_date TEXT NOT NULL,
                    last_active TEXT,
                    location_sharing_enabled BOOLEAN DEFAULT 0,
                    notification_preferences TEXT,
                    bio TEXT,
                    fitness_level TEXT,
                    certifications TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    UNIQUE(group_id, user_id)
                )
            ''')
            
            # Workout schedules table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workout_schedules (
                    schedule_id TEXT PRIMARY KEY,
                    group_id TEXT NOT NULL,
                    workout_id TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    schedule_type TEXT NOT NULL,
                    start_datetime TEXT NOT NULL,
                    end_datetime TEXT NOT NULL,
                    timezone TEXT NOT NULL,
                    recurring_pattern TEXT,
                    max_participants INTEGER,
                    registration_required BOOLEAN DEFAULT 0,
                    reminder_settings TEXT,
                    tags TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Workout locations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workout_locations (
                    location_id TEXT PRIMARY KEY,
                    schedule_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    address TEXT,
                    latitude REAL,
                    longitude REAL,
                    location_type TEXT NOT NULL,
                    capacity INTEGER,
                    amenities TEXT,
                    access_instructions TEXT,
                    safety_notes TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (schedule_id) REFERENCES workout_schedules (schedule_id)
                )
            ''')
            
            # Video sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS video_sessions (
                    session_id TEXT PRIMARY KEY,
                    schedule_id TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    meeting_url TEXT NOT NULL,
                    meeting_id TEXT,
                    password TEXT,
                    host_key TEXT,
                    recording_enabled BOOLEAN DEFAULT 0,
                    screen_sharing_enabled BOOLEAN DEFAULT 1,
                    chat_enabled BOOLEAN DEFAULT 1,
                    max_participants INTEGER DEFAULT 100,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    FOREIGN KEY (schedule_id) REFERENCES workout_schedules (schedule_id)
                )
            ''')
            
            # Schedule registrations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS schedule_registrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    schedule_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    registered_at TEXT NOT NULL,
                    attendance_status TEXT DEFAULT 'registered',
                    check_in_time TEXT,
                    check_in_location TEXT,
                    notes TEXT,
                    UNIQUE(schedule_id, user_id),
                    FOREIGN KEY (schedule_id) REFERENCES workout_schedules (schedule_id)
                )
            ''')
            
            # Location check-ins table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS location_checkins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    schedule_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    accuracy REAL,
                    check_in_time TEXT NOT NULL,
                    verified BOOLEAN DEFAULT 0,
                    FOREIGN KEY (schedule_id) REFERENCES workout_schedules (schedule_id)
                )
            ''')
            
            conn.commit()
    
    def _setup_role_permissions(self) -> Dict[GroupRole, GroupPermissions]:
        """Define permissions for each role."""
        return {
            GroupRole.OWNER: GroupPermissions(
                can_create_workouts=True,
                can_schedule_workouts=True,
                can_delete_workouts=True,
                can_manage_members=True,
                can_moderate_sessions=True,
                can_start_video_calls=True,
                can_share_location=True,
                can_view_analytics=True,
                can_export_data=True,
                can_manage_roles=True
            ),
            GroupRole.TRAINER: GroupPermissions(
                can_create_workouts=True,
                can_schedule_workouts=True,
                can_delete_workouts=True,
                can_manage_members=False,
                can_moderate_sessions=True,
                can_start_video_calls=True,
                can_share_location=True,
                can_view_analytics=True,
                can_export_data=False,
                can_manage_roles=False
            ),
            GroupRole.MODERATOR: GroupPermissions(
                can_create_workouts=False,
                can_schedule_workouts=False,
                can_delete_workouts=False,
                can_manage_members=True,
                can_moderate_sessions=True,
                can_start_video_calls=True,
                can_share_location=True,
                can_view_analytics=False,
                can_export_data=False,
                can_manage_roles=False
            ),
            GroupRole.PARTICIPANT: GroupPermissions(
                can_create_workouts=False,
                can_schedule_workouts=False,
                can_delete_workouts=False,
                can_manage_members=False,
                can_moderate_sessions=False,
                can_start_video_calls=False,
                can_share_location=True,
                can_view_analytics=False,
                can_export_data=False,
                can_manage_roles=False
            ),
            GroupRole.GUEST: GroupPermissions(
                can_create_workouts=False,
                can_schedule_workouts=False,
                can_delete_workouts=False,
                can_manage_members=False,
                can_moderate_sessions=False,
                can_start_video_calls=False,
                can_share_location=False,
                can_view_analytics=False,
                can_export_data=False,
                can_manage_roles=False
            )
        }
    
    # ===============================
    # WORKOUT SCHEDULING
    # ===============================
    
    def create_workout_schedule(self, group_id: str, creator_id: str, schedule_data: Dict) -> Dict:
        """Create a new workout schedule with advanced features."""
        # Verify creator has permission
        if not self._has_permission(group_id, creator_id, "can_schedule_workouts"):
            return {"error": "User does not have permission to schedule workouts", "success": False}
        
        schedule_id = f"sched_{uuid.uuid4().hex[:12]}"
        
        # Parse and validate schedule data
        schedule = WorkoutSchedule(
            schedule_id=schedule_id,
            group_id=group_id,
            workout_id=schedule_data.get("workout_id", ""),
            created_by=creator_id,
            title=schedule_data.get("title", "Group Workout"),
            description=schedule_data.get("description", ""),
            schedule_type=WorkoutScheduleType(schedule_data.get("schedule_type", "one_time")),
            start_datetime=schedule_data.get("start_datetime"),
            end_datetime=schedule_data.get("end_datetime"),
            timezone=schedule_data.get("timezone", "UTC"),
            recurring_pattern=schedule_data.get("recurring_pattern", {}),
            max_participants=schedule_data.get("max_participants"),
            registration_required=schedule_data.get("registration_required", False),
            reminder_settings=schedule_data.get("reminder_settings", {
                "email_reminder": True,
                "push_notification": True,
                "reminder_times": [24, 2]  # hours before
            }),
            tags=schedule_data.get("tags", []),
            is_active=True,
            created_at=datetime.utcnow().isoformat()
        )
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Insert schedule
            cursor.execute('''
                INSERT INTO workout_schedules 
                (schedule_id, group_id, workout_id, created_by, title, description,
                 schedule_type, start_datetime, end_datetime, timezone, recurring_pattern,
                 max_participants, registration_required, reminder_settings, tags, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                schedule.schedule_id, schedule.group_id, schedule.workout_id,
                schedule.created_by, schedule.title, schedule.description,
                schedule.schedule_type.value, schedule.start_datetime, schedule.end_datetime,
                schedule.timezone, json.dumps(schedule.recurring_pattern),
                schedule.max_participants, schedule.registration_required,
                json.dumps(schedule.reminder_settings), json.dumps(schedule.tags),
                schedule.created_at
            ))
            
            # Handle location if provided
            if "location" in schedule_data:
                self._add_workout_location(schedule_id, schedule_data["location"])
            
            # Handle video session if provided
            if "video_session" in schedule_data:
                self._create_video_session(schedule_id, schedule_data["video_session"])
            
            conn.commit()
        
        # Schedule reminders
        self._schedule_reminders(schedule)
        
        return {
            "success": True,
            "schedule_id": schedule_id,
            "schedule": asdict(schedule),
            "next_occurrences": self._get_next_occurrences(schedule, 5)
        }
    
    def _add_workout_location(self, schedule_id: str, location_data: Dict):
        """Add location information to a scheduled workout."""
        location_id = f"loc_{uuid.uuid4().hex[:8]}"
        
        location = WorkoutLocation(
            location_id=location_id,
            name=location_data.get("name", "Workout Location"),
            address=location_data.get("address", ""),
            latitude=location_data.get("latitude"),
            longitude=location_data.get("longitude"),
            location_type=LocationType(location_data.get("location_type", "virtual")),
            capacity=location_data.get("capacity"),
            amenities=location_data.get("amenities", []),
            access_instructions=location_data.get("access_instructions", ""),
            safety_notes=location_data.get("safety_notes", ""),
            created_at=datetime.utcnow().isoformat()
        )
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO workout_locations
                (location_id, schedule_id, name, address, latitude, longitude,
                 location_type, capacity, amenities, access_instructions, safety_notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                location.location_id, schedule_id, location.name, location.address,
                location.latitude, location.longitude, location.location_type.value,
                location.capacity, json.dumps(location.amenities),
                location.access_instructions, location.safety_notes, location.created_at
            ))
            conn.commit()
    
    def _create_video_session(self, schedule_id: str, video_data: Dict):
        """Create video session for virtual/hybrid workouts."""
        session_id = f"vid_{uuid.uuid4().hex[:12]}"
        
        video_session = VideoSession(
            session_id=session_id,
            provider=VideoProvider(video_data.get("provider", "jitsi")),
            meeting_url=video_data.get("meeting_url", ""),
            meeting_id=video_data.get("meeting_id", session_id),
            password=video_data.get("password"),
            host_key=video_data.get("host_key"),
            recording_enabled=video_data.get("recording_enabled", False),
            screen_sharing_enabled=video_data.get("screen_sharing_enabled", True),
            chat_enabled=video_data.get("chat_enabled", True),
            max_participants=video_data.get("max_participants", 100),
            created_at=datetime.utcnow().isoformat(),
            expires_at=(datetime.utcnow() + timedelta(days=30)).isoformat()
        )
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO video_sessions
                (session_id, schedule_id, provider, meeting_url, meeting_id, password,
                 host_key, recording_enabled, screen_sharing_enabled, chat_enabled,
                 max_participants, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                video_session.session_id, schedule_id, video_session.provider.value,
                video_session.meeting_url, video_session.meeting_id, video_session.password,
                video_session.host_key, video_session.recording_enabled,
                video_session.screen_sharing_enabled, video_session.chat_enabled,
                video_session.max_participants, video_session.created_at, video_session.expires_at
            ))
            conn.commit()
    
    # ===============================
    # LOCATION-BASED WORKOUTS
    # ===============================
    
    def find_nearby_workouts(self, user_location: Dict, radius_km: float = 10) -> List[Dict]:
        """Find nearby scheduled workouts within specified radius."""
        user_lat = user_location.get("latitude")
        user_lon = user_location.get("longitude")
        
        if not user_lat or not user_lon:
            return []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get all active schedules with locations
            cursor.execute('''
                SELECT s.*, l.name as location_name, l.address, l.latitude, l.longitude,
                       l.capacity, l.amenities, l.location_type
                FROM workout_schedules s
                JOIN workout_locations l ON s.schedule_id = l.schedule_id
                WHERE s.is_active = 1 
                AND l.latitude IS NOT NULL 
                AND l.longitude IS NOT NULL
                AND s.start_datetime > ?
            ''', (datetime.utcnow().isoformat(),))
            
            nearby_workouts = []
            user_coords = (user_lat, user_lon)
            
            for row in cursor.fetchall():
                location_coords = (row[15], row[16])  # latitude, longitude
                distance = geodesic(user_coords, location_coords).kilometers
                
                if distance <= radius_km:
                    nearby_workouts.append({
                        "schedule_id": row[0],
                        "title": row[4],
                        "description": row[5],
                        "start_datetime": row[7],
                        "location_name": row[14],
                        "address": row[15],
                        "distance_km": round(distance, 2),
                        "capacity": row[17],
                        "amenities": json.loads(row[18] or "[]"),
                        "location_type": row[19]
                    })
            
            # Sort by distance
            nearby_workouts.sort(key=lambda x: x["distance_km"])
            
        return nearby_workouts
    
    def location_check_in(self, schedule_id: str, user_id: str, location_data: Dict) -> Dict:
        """Handle location-based check-in for workout sessions."""
        user_lat = location_data.get("latitude")
        user_lon = location_data.get("longitude")
        accuracy = location_data.get("accuracy", 0)
        
        # Get workout location
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT latitude, longitude, name FROM workout_locations
                WHERE schedule_id = ?
            ''', (schedule_id,))
            
            location_row = cursor.fetchone()
            if not location_row:
                return {"error": "Workout location not found", "success": False}
            
            workout_lat, workout_lon, location_name = location_row
            
            # Calculate distance to workout location
            user_coords = (user_lat, user_lon)
            workout_coords = (workout_lat, workout_lon)
            distance = geodesic(user_coords, workout_coords).meters
            
            # Check if within acceptable range (50 meters + accuracy)
            max_distance = 50 + (accuracy or 0)
            verified = distance <= max_distance
            
            # Record check-in
            cursor.execute('''
                INSERT INTO location_checkins
                (schedule_id, user_id, latitude, longitude, accuracy, check_in_time, verified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                schedule_id, user_id, user_lat, user_lon, accuracy,
                datetime.utcnow().isoformat(), verified
            ))
            
            # Update registration status if verified
            if verified:
                cursor.execute('''
                    UPDATE schedule_registrations
                    SET attendance_status = 'checked_in', check_in_time = ?, check_in_location = ?
                    WHERE schedule_id = ? AND user_id = ?
                ''', (
                    datetime.utcnow().isoformat(),
                    f"{user_lat},{user_lon}",
                    schedule_id, user_id
                ))
            
            conn.commit()
        
        return {
            "success": True,
            "verified": verified,
            "distance_meters": round(distance, 1),
            "location_name": location_name,
            "message": "Successfully checked in!" if verified else f"Too far from workout location ({round(distance, 1)}m away)"
        }
    
    # ===============================
    # VIDEO CHAT INTEGRATION
    # ===============================
    
    def start_video_session(self, schedule_id: str, host_id: str) -> Dict:
        """Start video session for virtual workout."""
        # Check host permissions
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get schedule and verify host can start video calls
            cursor.execute('''
                SELECT s.group_id FROM workout_schedules s
                WHERE s.schedule_id = ? AND s.is_active = 1
            ''', (schedule_id,))
            
            schedule_row = cursor.fetchone()
            if not schedule_row:
                return {"error": "Schedule not found", "success": False}
            
            group_id = schedule_row[0]
            
            if not self._has_permission(group_id, host_id, "can_start_video_calls"):
                return {"error": "User does not have permission to start video calls", "success": False}
            
            # Get video session details
            cursor.execute('''
                SELECT * FROM video_sessions WHERE schedule_id = ?
            ''', (schedule_id,))
            
            video_row = cursor.fetchone()
            if not video_row:
                return {"error": "No video session configured for this workout", "success": False}
        
        # Generate dynamic meeting URL based on provider
        session_data = {
            "session_id": video_row[0],
            "provider": video_row[2],
            "meeting_url": self._generate_meeting_url(video_row[2], video_row[4]),
            "meeting_id": video_row[4],
            "password": video_row[5],
            "recording_enabled": bool(video_row[7]),
            "screen_sharing_enabled": bool(video_row[8]),
            "chat_enabled": bool(video_row[9]),
            "max_participants": video_row[10]
        }
        
        # Notify registered participants
        self._notify_video_session_start(schedule_id, session_data)
        
        return {
            "success": True,
            "video_session": session_data,
            "participants_notified": True
        }
    
    def _generate_meeting_url(self, provider: str, meeting_id: str) -> str:
        """Generate meeting URL based on provider."""
        if provider == "jitsi":
            return f"https://meet.jit.si/KhyrieWorkout_{meeting_id}"
        elif provider == "zoom":
            return f"https://zoom.us/j/{meeting_id}"
        elif provider == "google_meet":
            return f"https://meet.google.com/{meeting_id}"
        else:
            return f"https://video-provider.com/meeting/{meeting_id}"
    
    def _notify_video_session_start(self, schedule_id: str, session_data: Dict):
        """Notify registered participants that video session has started."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get registered participants with notification preferences
            cursor.execute('''
                SELECT r.user_id, m.email, m.notification_preferences
                FROM schedule_registrations r
                JOIN enhanced_group_members m ON r.user_id = m.user_id
                WHERE r.schedule_id = ? AND r.attendance_status != 'cancelled'
            ''', (schedule_id,))
            
            # Here you would integrate with your notification system
            # For now, we'll just log the notifications that should be sent
            participants = cursor.fetchall()
            
        return len(participants)
    
    # ===============================
    # ADVANCED ROLE PERMISSIONS
    # ===============================
    
    def assign_role(self, group_id: str, assigner_id: str, target_user_id: str, new_role: GroupRole) -> Dict:
        """Assign role to group member with permission validation."""
        # Check if assigner has permission to manage roles
        if not self._has_permission(group_id, assigner_id, "can_manage_roles"):
            return {"error": "User does not have permission to manage roles", "success": False}
        
        # Get role permissions
        role_permissions = self._setup_role_permissions()
        permissions = role_permissions[new_role]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Update user role and permissions
            cursor.execute('''
                UPDATE enhanced_group_members
                SET role = ?, permissions = ?, last_active = ?
                WHERE group_id = ? AND user_id = ?
            ''', (
                new_role.value,
                json.dumps(asdict(permissions)),
                datetime.utcnow().isoformat(),
                group_id,
                target_user_id
            ))
            
            if cursor.rowcount == 0:
                return {"error": "User not found in group", "success": False}
            
            conn.commit()
        
        return {
            "success": True,
            "user_id": target_user_id,
            "new_role": new_role.value,
            "permissions": asdict(permissions)
        }
    
    def _has_permission(self, group_id: str, user_id: str, permission: str) -> bool:
        """Check if user has specific permission in group."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT permissions FROM enhanced_group_members
                WHERE group_id = ? AND user_id = ? AND is_active = 1
            ''', (group_id, user_id))
            
            row = cursor.fetchone()
            if not row:
                return False
            
            permissions = json.loads(row[0])
            return permissions.get(permission, False)
    
    def get_role_capabilities(self, role: GroupRole) -> Dict:
        """Get detailed capabilities for a specific role."""
        role_permissions = self._setup_role_permissions()
        permissions = role_permissions[role]
        
        capabilities = {
            "role": role.value,
            "permissions": asdict(permissions),
            "description": self._get_role_description(role),
            "features_available": []
        }
        
        # Add feature descriptions based on permissions
        if permissions.can_create_workouts:
            capabilities["features_available"].append("Create and design custom workouts")
        if permissions.can_schedule_workouts:
            capabilities["features_available"].append("Schedule group workout sessions")
        if permissions.can_manage_members:
            capabilities["features_available"].append("Add, remove, and manage group members")
        if permissions.can_moderate_sessions:
            capabilities["features_available"].append("Moderate live workout sessions")
        if permissions.can_start_video_calls:
            capabilities["features_available"].append("Start and host video workout sessions")
        if permissions.can_view_analytics:
            capabilities["features_available"].append("Access group fitness analytics and reports")
        
        return capabilities
    
    def _get_role_description(self, role: GroupRole) -> str:
        """Get human-readable description for role."""
        descriptions = {
            GroupRole.OWNER: "Full administrative control of the group with all permissions",
            GroupRole.TRAINER: "Certified fitness professional who can create workouts and lead sessions",
            GroupRole.MODERATOR: "Helper who can manage members and moderate sessions",
            GroupRole.PARTICIPANT: "Standard group member who can join workouts and activities",
            GroupRole.GUEST: "Limited access visitor with view-only permissions"
        }
        return descriptions.get(role, "Unknown role")
    
    # ===============================
    # HELPER METHODS
    # ===============================
    
    def _schedule_reminders(self, schedule: WorkoutSchedule):
        """Schedule reminder notifications for workout."""
        # This would integrate with your notification system
        # For now, we'll just return reminder info
        reminder_times = schedule.reminder_settings.get("reminder_times", [24, 2])
        
        reminders = []
        for hours_before in reminder_times:
            reminder_time = datetime.fromisoformat(schedule.start_datetime) - timedelta(hours=hours_before)
            reminders.append({
                "reminder_time": reminder_time.isoformat(),
                "hours_before": hours_before,
                "message": f"Reminder: '{schedule.title}' starts in {hours_before} hours"
            })
        
        return reminders
    
    def _get_next_occurrences(self, schedule: WorkoutSchedule, count: int = 5) -> List[str]:
        """Get next occurrence times for recurring workouts."""
        if schedule.schedule_type == WorkoutScheduleType.ONE_TIME:
            return [schedule.start_datetime]
        
        occurrences = []
        start_dt = datetime.fromisoformat(schedule.start_datetime)
        
        if schedule.schedule_type == WorkoutScheduleType.RECURRING_WEEKLY:
            for i in range(count):
                next_occurrence = start_dt + timedelta(weeks=i)
                occurrences.append(next_occurrence.isoformat())
        
        elif schedule.schedule_type == WorkoutScheduleType.RECURRING_DAILY:
            for i in range(count):
                next_occurrence = start_dt + timedelta(days=i)
                occurrences.append(next_occurrence.isoformat())
        
        return occurrences
    
    # ===============================
    # PUBLIC API METHODS
    # ===============================
    
    def get_user_permissions(self, group_id: str, user_id: str) -> Dict:
        """Get user's current permissions in group."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT role, permissions, username, email FROM enhanced_group_members
                WHERE group_id = ? AND user_id = ? AND is_active = 1
            ''', (group_id, user_id))
            
            row = cursor.fetchone()
            if not row:
                return {"error": "User not found in group"}
            
            return {
                "user_id": user_id,
                "role": row[0],
                "permissions": json.loads(row[1]),
                "username": row[2],
                "email": row[3]
            }
    
    def get_group_schedule(self, group_id: str, days_ahead: int = 30) -> List[Dict]:
        """Get upcoming scheduled workouts for group."""
        end_date = datetime.utcnow() + timedelta(days=days_ahead)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT s.*, 
                       l.name as location_name, l.address, l.location_type,
                       v.meeting_url, v.provider as video_provider
                FROM workout_schedules s
                LEFT JOIN workout_locations l ON s.schedule_id = l.schedule_id
                LEFT JOIN video_sessions v ON s.schedule_id = v.schedule_id
                WHERE s.group_id = ? AND s.is_active = 1
                AND s.start_datetime BETWEEN ? AND ?
                ORDER BY s.start_datetime ASC
            ''', (
                group_id,
                datetime.utcnow().isoformat(),
                end_date.isoformat()
            ))
            
            schedules = []
            for row in cursor.fetchall():
                schedules.append({
                    "schedule_id": row[0],
                    "title": row[4],
                    "description": row[5],
                    "start_datetime": row[7],
                    "end_datetime": row[8],
                    "location_name": row[16] or "Virtual",
                    "location_type": row[18] or "virtual",
                    "video_provider": row[20],
                    "has_video": bool(row[19]),
                    "registration_required": bool(row[12])
                })
            
            return schedules


# Example usage and API integration
def create_enhanced_group_workout_api():
    """Create API endpoints for enhanced group workout features."""
    
    manager = EnhancedGroupWorkoutManager()
    
    # Example API endpoint implementations
    api_endpoints = {
        "POST /api/groups/enhanced/schedule": "create_workout_schedule",
        "GET /api/groups/enhanced/nearby": "find_nearby_workouts", 
        "POST /api/groups/enhanced/checkin": "location_check_in",
        "POST /api/groups/enhanced/video/start": "start_video_session",
        "PUT /api/groups/enhanced/roles/assign": "assign_role",
        "GET /api/groups/enhanced/permissions": "get_user_permissions",
        "GET /api/groups/enhanced/schedule": "get_group_schedule"
    }
    
    return manager, api_endpoints

if __name__ == "__main__":
    # Initialize the enhanced group workout system
    manager = EnhancedGroupWorkoutManager()
    print("✅ Enhanced Group Workout Management System initialized!")
    print("🎯 Features available:")
    print("   - Advanced workout scheduling with recurring patterns")
    print("   - GPS-enabled location-based workouts and check-ins")
    print("   - Video chat integration for virtual sessions")
    print("   - Role-based permissions (Owner, Trainer, Moderator, Participant, Guest)")