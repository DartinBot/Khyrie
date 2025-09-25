"""
Comprehensive Fitness Database Models
Advanced database schema for complete fitness tracking, analytics, and AI insights
"""

import sqlite3
import json
from datetime import datetime, date, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from pathlib import Path

@dataclass
class User:
    user_id: str
    email: str
    name: str
    date_of_birth: str
    gender: str
    height_cm: float
    current_weight_kg: float
    fitness_level: str  # beginner, intermediate, advanced
    goals: List[str]  # weight_loss, muscle_gain, endurance, strength, etc.
    injuries: List[str]
    preferences: Dict[str, Any]
    created_at: str
    last_active: str

@dataclass 
class Exercise:
    exercise_id: str
    name: str
    category: str  # strength, cardio, flexibility, balance
    muscle_groups: List[str]
    equipment: List[str]
    difficulty_level: str
    instructions: List[str]
    demo_video_url: str
    safety_notes: List[str]
    variations: List[Dict]
    created_at: str

@dataclass
class WorkoutProgram:
    program_id: str
    name: str
    description: str
    creator_id: str
    duration_weeks: int
    frequency_per_week: int
    difficulty_level: str
    goals: List[str]
    exercises: List[Dict]  # exercise_id, sets, reps, weight, rest_time
    progression_scheme: Dict[str, Any]
    created_at: str
    is_public: bool

@dataclass
class WorkoutSession:
    session_id: str
    user_id: str
    program_id: Optional[str]
    workout_name: str
    start_time: str
    end_time: Optional[str]
    exercises_completed: List[Dict]
    total_volume_kg: float
    calories_burned: int
    average_heart_rate: Optional[int]
    max_heart_rate: Optional[int]
    rpe_score: Optional[int]  # Rate of Perceived Exertion 1-10
    notes: str
    mood_before: Optional[str]
    mood_after: Optional[str]
    created_at: str

@dataclass
class StrengthProgression:
    progression_id: str
    user_id: str
    exercise_id: str
    date: str
    one_rep_max: float
    calculated_method: str  # formula used, estimated vs tested
    actual_max: Optional[float]
    bodyweight: float
    notes: str

@dataclass
class NutritionPlan:
    plan_id: str
    user_id: str
    name: str
    goal_type: str  # weight_loss, muscle_gain, maintenance, cutting, bulking
    daily_calories: int
    macros: Dict[str, float]  # protein, carbs, fats percentages
    meal_plan: Dict[str, Any]
    restrictions: List[str]  # vegetarian, vegan, gluten_free, etc.
    created_at: str
    active: bool

@dataclass
class MealLog:
    log_id: str
    user_id: str
    date: str
    meal_type: str  # breakfast, lunch, dinner, snack
    foods: List[Dict]  # name, quantity, calories, macros
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float
    logged_at: str

@dataclass
class RecoverySession:
    session_id: str
    user_id: str
    date: str
    session_type: str  # sleep, massage, stretching, meditation, sauna
    duration_minutes: int
    quality_rating: int  # 1-10
    activities: List[str]
    metrics: Dict[str, Any]  # hrv, rhr, sleep_stages, etc.
    notes: str
    logged_at: str

@dataclass
class WearableData:
    data_id: str
    user_id: str
    device_type: str  # fitbit, apple_watch, garmin, etc.
    date: str
    steps: int
    distance_km: float
    calories_burned: int
    active_minutes: int
    heart_rate_avg: Optional[int]
    heart_rate_max: Optional[int]
    heart_rate_resting: Optional[int]
    sleep_hours: Optional[float]
    sleep_quality: Optional[str]
    stress_level: Optional[int]
    raw_data: Dict[str, Any]
    synced_at: str

@dataclass
class PhysicalTherapyPlan:
    plan_id: str
    user_id: str
    condition: str
    prescribed_by: str  # therapist name or self-guided
    exercises: List[Dict]
    frequency: str
    duration_weeks: int
    progress_markers: List[str]
    restrictions: List[str]
    created_at: str
    active: bool

@dataclass
class WorkoutAnalytics:
    analytics_id: str
    user_id: str
    period_start: str
    period_end: str
    total_workouts: int
    total_volume_kg: float
    average_workout_duration: float
    most_trained_muscle_groups: List[str]
    strength_improvements: Dict[str, float]
    consistency_score: float
    injury_risk_score: float
    recommendations: List[str]
    generated_at: str

class ComprehensiveFitnessDatabase:
    """Advanced database for comprehensive fitness tracking and analytics"""
    
    def __init__(self, db_path: str = "comprehensive_fitness.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create all database tables and sample data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table - enhanced
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users_enhanced (
                    user_id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    date_of_birth TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    height_cm REAL NOT NULL,
                    current_weight_kg REAL NOT NULL,
                    fitness_level TEXT NOT NULL,
                    goals TEXT NOT NULL,
                    injuries TEXT NOT NULL,
                    preferences TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_active TEXT NOT NULL
                )
            ''')
            
            # Exercises table - comprehensive
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exercises_enhanced (
                    exercise_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    muscle_groups TEXT NOT NULL,
                    equipment TEXT NOT NULL,
                    difficulty_level TEXT NOT NULL,
                    instructions TEXT NOT NULL,
                    demo_video_url TEXT DEFAULT '',
                    safety_notes TEXT NOT NULL,
                    variations TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Workout Programs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workout_programs (
                    program_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    creator_id TEXT NOT NULL,
                    duration_weeks INTEGER NOT NULL,
                    frequency_per_week INTEGER NOT NULL,
                    difficulty_level TEXT NOT NULL,
                    goals TEXT NOT NULL,
                    exercises TEXT NOT NULL,
                    progression_scheme TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    is_public BOOLEAN DEFAULT 0,
                    FOREIGN KEY (creator_id) REFERENCES users_enhanced (user_id)
                )
            ''')
            
            # Workout Sessions table - enhanced
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workout_sessions_enhanced (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    program_id TEXT,
                    workout_name TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    exercises_completed TEXT NOT NULL,
                    total_volume_kg REAL NOT NULL,
                    calories_burned INTEGER NOT NULL,
                    average_heart_rate INTEGER,
                    max_heart_rate INTEGER,
                    rpe_score INTEGER,
                    notes TEXT DEFAULT '',
                    mood_before TEXT,
                    mood_after TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users_enhanced (user_id),
                    FOREIGN KEY (program_id) REFERENCES workout_programs (program_id)
                )
            ''')
            
            # Strength Progression table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS strength_progression (
                    progression_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    exercise_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    one_rep_max REAL NOT NULL,
                    calculated_method TEXT NOT NULL,
                    actual_max REAL,
                    bodyweight REAL NOT NULL,
                    notes TEXT DEFAULT '',
                    FOREIGN KEY (user_id) REFERENCES users_enhanced (user_id),
                    FOREIGN KEY (exercise_id) REFERENCES exercises_enhanced (exercise_id)
                )
            ''')
            
            # Nutrition Plans table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nutrition_plans (
                    plan_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    goal_type TEXT NOT NULL,
                    daily_calories INTEGER NOT NULL,
                    macros TEXT NOT NULL,
                    meal_plan TEXT NOT NULL,
                    restrictions TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users_enhanced (user_id)
                )
            ''')
            
            # Meal Logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meal_logs (
                    log_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    meal_type TEXT NOT NULL,
                    foods TEXT NOT NULL,
                    total_calories REAL NOT NULL,
                    total_protein REAL NOT NULL,
                    total_carbs REAL NOT NULL,
                    total_fats REAL NOT NULL,
                    logged_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users_enhanced (user_id)
                )
            ''')
            
            # Recovery Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recovery_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    session_type TEXT NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    quality_rating INTEGER NOT NULL,
                    activities TEXT NOT NULL,
                    metrics TEXT NOT NULL,
                    notes TEXT DEFAULT '',
                    logged_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users_enhanced (user_id)
                )
            ''')
            
            # Wearable Data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS wearable_data (
                    data_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    device_type TEXT NOT NULL,
                    date TEXT NOT NULL,
                    steps INTEGER NOT NULL,
                    distance_km REAL NOT NULL,
                    calories_burned INTEGER NOT NULL,
                    active_minutes INTEGER NOT NULL,
                    heart_rate_avg INTEGER,
                    heart_rate_max INTEGER,
                    heart_rate_resting INTEGER,
                    sleep_hours REAL,
                    sleep_quality TEXT,
                    stress_level INTEGER,
                    raw_data TEXT NOT NULL,
                    synced_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users_enhanced (user_id)
                )
            ''')
            
            # Physical Therapy Plans table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS physical_therapy_plans (
                    plan_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    condition TEXT NOT NULL,
                    prescribed_by TEXT NOT NULL,
                    exercises TEXT NOT NULL,
                    frequency TEXT NOT NULL,
                    duration_weeks INTEGER NOT NULL,
                    progress_markers TEXT NOT NULL,
                    restrictions TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users_enhanced (user_id)
                )
            ''')
            
            # Workout Analytics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workout_analytics (
                    analytics_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    period_start TEXT NOT NULL,
                    period_end TEXT NOT NULL,
                    total_workouts INTEGER NOT NULL,
                    total_volume_kg REAL NOT NULL,
                    average_workout_duration REAL NOT NULL,
                    most_trained_muscle_groups TEXT NOT NULL,
                    strength_improvements TEXT NOT NULL,
                    consistency_score REAL NOT NULL,
                    injury_risk_score REAL NOT NULL,
                    recommendations TEXT NOT NULL,
                    generated_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users_enhanced (user_id)
                )
            ''')
            
            # Create indexes for better performance
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_user_sessions ON workout_sessions_enhanced(user_id, created_at)",
                "CREATE INDEX IF NOT EXISTS idx_user_progression ON strength_progression(user_id, exercise_id, date)",
                "CREATE INDEX IF NOT EXISTS idx_user_nutrition ON meal_logs(user_id, date)",
                "CREATE INDEX IF NOT EXISTS idx_user_recovery ON recovery_sessions(user_id, date)",
                "CREATE INDEX IF NOT EXISTS idx_user_wearable ON wearable_data(user_id, date)",
                "CREATE INDEX IF NOT EXISTS idx_exercise_category ON exercises_enhanced(category)",
                "CREATE INDEX IF NOT EXISTS idx_program_creator ON workout_programs(creator_id, is_public)"
            ]
            
            # Create indexes with error handling
            for index in indexes:
                try:
                    cursor.execute(index)
                except sqlite3.OperationalError as e:
                    print(f"Warning: Could not create index - {e}")
            
            conn.commit()
            print("✅ Comprehensive fitness database initialized successfully!")
    
    def add_sample_data(self):
        """Add comprehensive sample data for testing"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Sample enhanced user
            sample_user = User(
                user_id="user_001",
                email="john.doe@example.com",
                name="John Doe",
                date_of_birth="1990-05-15",
                gender="male",
                height_cm=180.0,
                current_weight_kg=80.0,
                fitness_level="intermediate",
                goals=["muscle_gain", "strength", "endurance"],
                injuries=["previous_knee_injury"],
                preferences={
                    "workout_time": "morning",
                    "intensity": "moderate_high",
                    "equipment": ["dumbbells", "barbell", "resistance_bands"]
                },
                created_at=datetime.utcnow().isoformat(),
                last_active=datetime.utcnow().isoformat()
            )
            
            cursor.execute('''
                INSERT OR REPLACE INTO users_enhanced 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sample_user.user_id, sample_user.email, sample_user.name,
                sample_user.date_of_birth, sample_user.gender, sample_user.height_cm,
                sample_user.current_weight_kg, sample_user.fitness_level,
                json.dumps(sample_user.goals), json.dumps(sample_user.injuries),
                json.dumps(sample_user.preferences), sample_user.created_at,
                sample_user.last_active
            ))
            
            # Sample exercises
            sample_exercises = [
                Exercise(
                    exercise_id="ex_001",
                    name="Barbell Back Squat",
                    category="strength",
                    muscle_groups=["quadriceps", "glutes", "hamstrings", "core"],
                    equipment=["barbell", "squat_rack"],
                    difficulty_level="intermediate",
                    instructions=[
                        "Position barbell on upper back",
                        "Stand with feet shoulder-width apart",
                        "Descend by pushing hips back and bending knees",
                        "Keep chest up and core tight",
                        "Drive through heels to return to standing"
                    ],
                    demo_video_url="https://example.com/squat-demo",
                    safety_notes=["Always use safety bars", "Maintain proper form over heavy weight"],
                    variations=[
                        {"name": "Front Squat", "difficulty": "advanced"},
                        {"name": "Goblet Squat", "difficulty": "beginner"}
                    ],
                    created_at=datetime.utcnow().isoformat()
                ),
                Exercise(
                    exercise_id="ex_002",
                    name="Bench Press",
                    category="strength",
                    muscle_groups=["chest", "triceps", "shoulders"],
                    equipment=["barbell", "bench"],
                    difficulty_level="intermediate",
                    instructions=[
                        "Lie on bench with feet flat on floor",
                        "Grip barbell slightly wider than shoulders",
                        "Lower bar to chest with control",
                        "Press bar up explosively",
                        "Keep shoulder blades retracted"
                    ],
                    demo_video_url="https://example.com/bench-demo",
                    safety_notes=["Always use a spotter", "Don't bounce bar off chest"],
                    variations=[
                        {"name": "Dumbbell Bench Press", "difficulty": "beginner"},
                        {"name": "Incline Bench Press", "difficulty": "intermediate"}
                    ],
                    created_at=datetime.utcnow().isoformat()
                )
            ]
            
            for exercise in sample_exercises:
                cursor.execute('''
                    INSERT OR REPLACE INTO exercises_enhanced 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    exercise.exercise_id, exercise.name, exercise.category,
                    json.dumps(exercise.muscle_groups), json.dumps(exercise.equipment),
                    exercise.difficulty_level, json.dumps(exercise.instructions),
                    exercise.demo_video_url, json.dumps(exercise.safety_notes),
                    json.dumps(exercise.variations), exercise.created_at
                ))
            
            conn.commit()
            print("✅ Sample data added successfully!")
    
    def get_user_analytics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive user analytics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get workout statistics
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_workouts,
                    AVG(total_volume_kg) as avg_volume,
                    AVG((julianday(end_time) - julianday(start_time)) * 24 * 60) as avg_duration,
                    SUM(calories_burned) as total_calories
                FROM workout_sessions_enhanced 
                WHERE user_id = ? AND date(created_at) > date('now', '-{} days')
            '''.format(days), (user_id,))
            
            workout_stats = cursor.fetchone()
            
            # Get strength progression
            cursor.execute('''
                SELECT exercise_id, MAX(one_rep_max) as max_1rm
                FROM strength_progression 
                WHERE user_id = ? AND date(date) > date('now', '-{} days')
                GROUP BY exercise_id
            '''.format(days), (user_id,))
            
            strength_data = cursor.fetchall()
            
            return {
                "workout_stats": {
                    "total_workouts": workout_stats[0] or 0,
                    "average_volume_kg": round(workout_stats[1] or 0, 1),
                    "average_duration_minutes": round(workout_stats[2] or 0, 1),
                    "total_calories_burned": workout_stats[3] or 0
                },
                "strength_progression": [
                    {"exercise_id": ex[0], "max_1rm": ex[1]} 
                    for ex in strength_data
                ],
                "period_days": days,
                "generated_at": datetime.utcnow().isoformat()
            }

if __name__ == "__main__":
    # Initialize the comprehensive database
    db = ComprehensiveFitnessDatabase()
    db.add_sample_data()
    print("🏋️‍♂️ Comprehensive Fitness Database Setup Complete!")
    
    # Test analytics
    analytics = db.get_user_analytics("user_001")
    print("📊 Sample Analytics:", json.dumps(analytics, indent=2))