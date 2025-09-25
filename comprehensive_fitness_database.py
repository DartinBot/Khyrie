"""
Comprehensive Fitness Database Models
Database schema for all workout sections with persistent data storage
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
    username: str
    email: str
    created_at: str
    profile_data: str  # JSON: age, weight, height, experience_level, goals
    preferences: str   # JSON: training_style, available_equipment, time_constraints

@dataclass 
class Exercise:
    exercise_id: str
    name: str
    category: str      # strength, cardio, flexibility, etc.
    muscle_groups: str # JSON list
    equipment: str     # JSON list
    difficulty: str    # beginner, intermediate, advanced
    instructions: str  # JSON list of steps
    tips: str         # JSON list
    variations: str   # JSON list
    created_at: str

@dataclass
class WorkoutProgram:
    program_id: str
    user_id: str
    name: str
    program_type: str  # strength, cardio, calisthenics, recovery, etc.
    level: str         # beginner, intermediate, advanced
    duration_weeks: int
    days_per_week: int
    description: str
    program_data: str  # JSON: exercises, sets, reps, progressions
    created_at: str
    is_active: bool

@dataclass
class WorkoutSession:
    session_id: str
    user_id: str
    program_id: Optional[str]
    workout_type: str  # strength, cardio, calisthenics, recovery
    date: str
    duration_minutes: int
    exercises_performed: str  # JSON list
    performance_data: str     # JSON: weights, reps, RPE, etc.
    notes: str
    created_at: str

@dataclass
class StrengthProgression:
    progression_id: str
    user_id: str
    exercise_id: str
    date: str
    one_rep_max: float
    calculated_method: str  # epley, brzycki, etc.
    actual_max: Optional[float]
    bodyweight: float
    notes: str

@dataclass
class NutritionPlan:
    plan_id: str
    user_id: str
    name: str
    goal_type: str     # weight_loss, muscle_gain, maintenance
    daily_calories: int
    macros: str        # JSON: protein, carbs, fat percentages
    meal_plan: str     # JSON: meals and foods
    restrictions: str  # JSON list: vegetarian, gluten_free, etc.
    created_at: str
    is_active: bool

@dataclass
class MealLog:
    log_id: str
    user_id: str
    plan_id: Optional[str]
    date: str
    meal_type: str     # breakfast, lunch, dinner, snack
    foods: str         # JSON list of foods with quantities
    calories: int
    macros: str        # JSON: protein, carbs, fat grams
    logged_at: str

@dataclass
class RecoverySession:
    recovery_id: str
    user_id: str
    date: str
    recovery_type: str  # active_recovery, sleep, stretching, massage
    duration_minutes: int
    quality_rating: int  # 1-10 scale
    metrics: str        # JSON: HRV, sleep_hours, stress_level
    activities: str     # JSON list of recovery activities
    notes: str

@dataclass
class WearableData:
    data_id: str
    user_id: str
    device_type: str    # fitbit, apple_watch, garmin, etc.
    date: str
    sync_time: str
    steps: Optional[int]
    calories_burned: Optional[int]
    heart_rate_data: str  # JSON: avg, max, resting, zones
    sleep_data: str       # JSON: total_sleep, deep_sleep, rem_sleep
    activity_data: str    # JSON: workouts, active_minutes
    raw_data: str        # JSON: complete device data

@dataclass
class PhysicalTherapyPlan:
    plan_id: str
    user_id: str
    injury_type: str
    assessment_data: str  # JSON: injury details, limitations
    treatment_plan: str   # JSON: exercises, frequency, progression
    created_at: str
    status: str          # active, completed, paused
    progress_notes: str  # JSON list of progress updates

@dataclass
class WorkoutAnalytics:
    analytics_id: str
    user_id: str
    period_start: str
    period_end: str
    total_workouts: int
    total_volume: float    # total weight lifted or cardio minutes
    strength_gains: str    # JSON: exercise improvements
    consistency_rating: float  # percentage of planned workouts completed
    trends: str           # JSON: performance trends and insights

class ComprehensiveFitnessDatabase:
    def __init__(self, db_path: str = "comprehensive_fitness.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Create all database tables and sample data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TEXT NOT NULL,
                    profile_data TEXT NOT NULL,
                    preferences TEXT NOT NULL
                )
            ''')
            
            # Exercises table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exercises (
                    exercise_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    muscle_groups TEXT NOT NULL,
                    equipment TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    instructions TEXT NOT NULL,
                    tips TEXT NOT NULL,
                    variations TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Workout Programs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workout_programs (
                    program_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    program_type TEXT NOT NULL,
                    level TEXT NOT NULL,
                    duration_weeks INTEGER NOT NULL,
                    days_per_week INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    program_data TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Workout Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workout_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    program_id TEXT,
                    workout_type TEXT NOT NULL,
                    date TEXT NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    exercises_performed TEXT NOT NULL,
                    performance_data TEXT NOT NULL,
                    notes TEXT DEFAULT '',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
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
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (exercise_id) REFERENCES exercises (exercise_id)
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
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Meal Logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meal_logs (
                    log_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    plan_id TEXT,
                    date TEXT NOT NULL,
                    meal_type TEXT NOT NULL,
                    foods TEXT NOT NULL,
                    calories INTEGER NOT NULL,
                    macros TEXT NOT NULL,
                    logged_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (plan_id) REFERENCES nutrition_plans (plan_id)
                )
            ''')
            
            # Recovery Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recovery_sessions (
                    recovery_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    recovery_type TEXT NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    quality_rating INTEGER NOT NULL,
                    metrics TEXT NOT NULL,
                    activities TEXT NOT NULL,
                    notes TEXT DEFAULT '',
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Wearable Data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS wearable_data (
                    data_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    device_type TEXT NOT NULL,
                    date TEXT NOT NULL,
                    sync_time TEXT NOT NULL,
                    steps INTEGER,
                    calories_burned INTEGER,
                    heart_rate_data TEXT NOT NULL,
                    sleep_data TEXT NOT NULL,
                    activity_data TEXT NOT NULL,
                    raw_data TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Physical Therapy Plans table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS physical_therapy_plans (
                    plan_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    injury_type TEXT NOT NULL,
                    assessment_data TEXT NOT NULL,
                    treatment_plan TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    progress_notes TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
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
                    total_volume REAL NOT NULL,
                    strength_gains TEXT NOT NULL,
                    consistency_rating REAL NOT NULL,
                    trends TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            conn.commit()
            
            # Add sample data
            self._add_sample_data()
    
    def _add_sample_data(self):
        """Add comprehensive sample data for all fitness sections"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if data already exists
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] > 0:
                return  # Data already exists
            
            # Sample users
            users = [
                User(
                    user_id="user_001",
                    username="john_lifter",
                    email="john@example.com",
                    created_at=datetime.now().isoformat(),
                    profile_data=json.dumps({
                        "age": 28,
                        "weight_lbs": 180,
                        "height_inches": 72,
                        "experience_level": "intermediate",
                        "primary_goals": ["strength", "muscle_gain"],
                        "available_time": "60min_per_session"
                    }),
                    preferences=json.dumps({
                        "training_style": "powerlifting",
                        "available_equipment": ["barbell", "dumbbells", "rack"],
                        "training_frequency": 4,
                        "preferred_time": "evening"
                    })
                ),
                User(
                    user_id="user_002", 
                    username="sarah_runner",
                    email="sarah@example.com",
                    created_at=datetime.now().isoformat(),
                    profile_data=json.dumps({
                        "age": 32,
                        "weight_lbs": 140,
                        "height_inches": 65,
                        "experience_level": "advanced", 
                        "primary_goals": ["endurance", "weight_loss"],
                        "available_time": "45min_per_session"
                    }),
                    preferences=json.dumps({
                        "training_style": "cardio_focused",
                        "available_equipment": ["bodyweight", "resistance_bands"],
                        "training_frequency": 5,
                        "preferred_time": "morning"
                    })
                )
            ]
            
            for user in users:
                cursor.execute('''
                    INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?)
                ''', (user.user_id, user.username, user.email, user.created_at, 
                     user.profile_data, user.preferences))
            
            # Sample exercises
            exercises = [
                Exercise(
                    exercise_id="ex_001",
                    name="Back Squat",
                    category="strength",
                    muscle_groups=json.dumps(["quadriceps", "glutes", "hamstrings", "core"]),
                    equipment=json.dumps(["barbell", "squat_rack", "plates"]),
                    difficulty="intermediate",
                    instructions=json.dumps([
                        "Position barbell on upper back",
                        "Step back and set feet shoulder-width apart",
                        "Lower by sitting back and down",
                        "Drive through heels to return to start"
                    ]),
                    tips=json.dumps([
                        "Keep chest up and core tight",
                        "Track knees over toes",
                        "Full depth for maximum effectiveness"
                    ]),
                    variations=json.dumps(["Front Squat", "Goblet Squat", "Box Squat"]),
                    created_at=datetime.now().isoformat()
                ),
                Exercise(
                    exercise_id="ex_002",
                    name="Deadlift",
                    category="strength", 
                    muscle_groups=json.dumps(["hamstrings", "glutes", "erectors", "traps", "lats"]),
                    equipment=json.dumps(["barbell", "plates"]),
                    difficulty="advanced",
                    instructions=json.dumps([
                        "Position feet hip-width apart",
                        "Grip bar with hands just outside legs",
                        "Keep back straight and lift by extending hips and knees",
                        "Stand tall and reverse the movement"
                    ]),
                    tips=json.dumps([
                        "Keep bar close to body throughout lift",
                        "Engage lats to maintain bar path",
                        "Drive through entire foot"
                    ]),
                    variations=json.dumps(["Romanian Deadlift", "Sumo Deadlift", "Trap Bar Deadlift"]),
                    created_at=datetime.now().isoformat()
                ),
                Exercise(
                    exercise_id="ex_003",
                    name="Push-up",
                    category="calisthenics",
                    muscle_groups=json.dumps(["chest", "shoulders", "triceps", "core"]),
                    equipment=json.dumps(["bodyweight"]),
                    difficulty="beginner",
                    instructions=json.dumps([
                        "Start in plank position",
                        "Lower chest to ground with control",
                        "Push back up to starting position",
                        "Maintain straight line from head to heels"
                    ]),
                    tips=json.dumps([
                        "Keep elbows at 45-degree angle",
                        "Engage core throughout movement",
                        "Full range of motion"
                    ]),
                    variations=json.dumps(["Diamond Push-up", "Incline Push-up", "One-Arm Push-up"]),
                    created_at=datetime.now().isoformat()
                )
            ]
            
            for exercise in exercises:
                cursor.execute('''
                    INSERT OR IGNORE INTO exercises VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (exercise.exercise_id, exercise.name, exercise.category, 
                     exercise.muscle_groups, exercise.equipment, exercise.difficulty,
                     exercise.instructions, exercise.tips, exercise.variations, 
                     exercise.created_at))
            
            # Sample workout programs
            programs = [
                WorkoutProgram(
                    program_id="prog_001",
                    user_id="user_001",
                    name="Starting Strength - Linear Progression",
                    program_type="strength",
                    level="beginner",
                    duration_weeks=12,
                    days_per_week=3,
                    description="Linear progression focusing on the big 3 compound lifts",
                    program_data=json.dumps({
                        "week_structure": "3_days_per_week",
                        "progression_type": "linear",
                        "main_lifts": ["squat", "bench_press", "deadlift"],
                        "accessory_work": ["rows", "pullups", "dips"],
                        "progression_scheme": "5lbs_upper_10lbs_lower"
                    }),
                    created_at=datetime.now().isoformat(),
                    is_active=True
                ),
                WorkoutProgram(
                    program_id="prog_002",
                    user_id="user_002",
                    name="Calisthenics Progression Program",
                    program_type="calisthenics", 
                    level="intermediate",
                    duration_weeks=16,
                    days_per_week=4,
                    description="Progressive bodyweight strength training program",
                    program_data=json.dumps({
                        "week_structure": "4_days_per_week",
                        "progression_type": "skill_based",
                        "main_skills": ["handstand", "muscle_up", "pistol_squat"],
                        "strength_work": ["pushup_variations", "pullup_variations"],
                        "progression_scheme": "time_reps_difficulty"
                    }),
                    created_at=datetime.now().isoformat(),
                    is_active=True
                )
            ]
            
            for program in programs:
                cursor.execute('''
                    INSERT OR IGNORE INTO workout_programs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (program.program_id, program.user_id, program.name, 
                     program.program_type, program.level, program.duration_weeks,
                     program.days_per_week, program.description, program.program_data,
                     program.created_at, program.is_active))
            
            # Sample workout sessions
            yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
            sessions = [
                WorkoutSession(
                    session_id="session_001",
                    user_id="user_001",
                    program_id="prog_001",
                    workout_type="strength",
                    date=yesterday,
                    duration_minutes=75,
                    exercises_performed=json.dumps([
                        {"exercise": "squat", "sets": 3, "reps": 5, "weight": 225},
                        {"exercise": "bench_press", "sets": 3, "reps": 5, "weight": 185},
                        {"exercise": "row", "sets": 3, "reps": 8, "weight": 135}
                    ]),
                    performance_data=json.dumps({
                        "total_volume": 2775,  # weight x reps
                        "average_rpe": 7.5,
                        "notes": "Felt strong today, good session"
                    }),
                    notes="New PR on squat!",
                    created_at=datetime.now().isoformat()
                )
            ]
            
            for session in sessions:
                cursor.execute('''
                    INSERT OR IGNORE INTO workout_sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (session.session_id, session.user_id, session.program_id,
                     session.workout_type, session.date, session.duration_minutes,
                     session.exercises_performed, session.performance_data,
                     session.notes, session.created_at))
            
            # Sample strength progression
            progressions = [
                StrengthProgression(
                    progression_id="prog_str_001",
                    user_id="user_001",
                    exercise_id="ex_001",  # Back Squat
                    date=yesterday,
                    one_rep_max=275.0,
                    calculated_method="epley",
                    actual_max=270.0,
                    bodyweight=180.0,
                    notes="Calculated from 225x5, actual tested at 270"
                )
            ]
            
            for prog in progressions:
                cursor.execute('''
                    INSERT OR IGNORE INTO strength_progression VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (prog.progression_id, prog.user_id, prog.exercise_id,
                     prog.date, prog.one_rep_max, prog.calculated_method,
                     prog.actual_max, prog.bodyweight, prog.notes))
            
            # Sample nutrition plan
            nutrition_plans = [
                NutritionPlan(
                    plan_id="nutr_001",
                    user_id="user_001",
                    name="Muscle Building Plan",
                    goal_type="muscle_gain",
                    daily_calories=2800,
                    macros=json.dumps({
                        "protein_percent": 25,
                        "carbs_percent": 45,
                        "fat_percent": 30,
                        "protein_grams": 175,
                        "carbs_grams": 315,
                        "fat_grams": 93
                    }),
                    meal_plan=json.dumps({
                        "breakfast": ["oatmeal", "berries", "protein_powder"],
                        "lunch": ["chicken_breast", "rice", "vegetables"],
                        "dinner": ["salmon", "sweet_potato", "asparagus"],
                        "snacks": ["greek_yogurt", "nuts", "fruit"]
                    }),
                    restrictions=json.dumps([]),
                    created_at=datetime.now().isoformat(),
                    is_active=True
                )
            ]
            
            for plan in nutrition_plans:
                cursor.execute('''
                    INSERT OR IGNORE INTO nutrition_plans VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (plan.plan_id, plan.user_id, plan.name, plan.goal_type,
                     plan.daily_calories, plan.macros, plan.meal_plan,
                     plan.restrictions, plan.created_at, plan.is_active))
            
            conn.commit()
            print("✅ Comprehensive fitness database initialized with sample data")
            print(f"📊 Database location: {self.db_path}")

if __name__ == "__main__":
    # Initialize the comprehensive database
    db = ComprehensiveFitnessDatabase()
    print("🏋️‍♂️ Comprehensive Fitness Database Setup Complete!")