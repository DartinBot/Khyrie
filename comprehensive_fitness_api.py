"""
Comprehensive Fitness API with Database Storage
FastAPI server with persistent data for all workout sections
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
from datetime import datetime, timedelta

# Import our comprehensive database tools
from comprehensive_workout_tools import ComprehensiveWorkoutTools

# Initialize FastAPI app
app = FastAPI(
    title="Comprehensive Fitness API with Database",
    description="Complete fitness API with persistent storage for all workout sections",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tools
fitness_tools = ComprehensiveWorkoutTools()

# ===============================
# PYDANTIC MODELS
# ===============================

class UserCreate(BaseModel):
    username: str
    email: str
    profile_data: Dict
    preferences: Dict

class ExerciseCreate(BaseModel):
    name: str
    category: str
    muscle_groups: List[str]
    equipment: List[str]
    difficulty: str
    instructions: List[str]
    tips: List[str]
    variations: List[str]

class OneRMCalculation(BaseModel):
    weight: float
    reps: int
    method: str = "epley"
    user_id: Optional[str] = None
    exercise_name: Optional[str] = None
    bodyweight: Optional[float] = 180.0

class StrengthProgramRequest(BaseModel):
    user_id: str = "user_001"
    program_type: str = "starting_strength"
    level: str = "intermediate"
    duration_weeks: int = 12
    days_per_week: int = 3

class WorkoutSessionLog(BaseModel):
    user_id: str
    workout_type: str
    exercises: List[Dict]
    duration_minutes: int
    notes: str = ""
    program_id: Optional[str] = None

class NutritionPlanRequest(BaseModel):
    user_id: str
    goal_type: str
    daily_calories: int
    protein_percent: float = 25
    carb_percent: float = 45
    fat_percent: float = 30
    restrictions: List[str] = []

class MealLogRequest(BaseModel):
    user_id: str
    meal_type: str
    foods: List[Dict]
    plan_id: Optional[str] = None

class RecoverySessionRequest(BaseModel):
    user_id: str
    recovery_type: str
    duration_minutes: int
    quality_rating: int
    activities: List[str]
    metrics: Dict = {}

# ===============================
# ROOT & HEALTH ENDPOINTS
# ===============================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🏋️‍♂️ Comprehensive Fitness API with Database Storage",
        "version": "2.0.0",
        "features": [
            "User Management",
            "Exercise Library", 
            "Strength Training with Progress Tracking",
            "Workout Session Logging",
            "Nutrition Planning & Meal Logging",
            "Recovery Session Tracking",
            "Comprehensive Analytics",
            "Persistent SQLite Database"
        ],
        "database": "SQLite with comprehensive fitness schema",
        "endpoints": "/docs for full API documentation"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/database/stats")
async def get_database_stats():
    """Get database statistics"""
    with fitness_tools.db.get_connection() as conn:
        cursor = conn.cursor()
        
        stats = {}
        tables = [
            "users", "exercises", "workout_programs", "workout_sessions",
            "strength_progression", "nutrition_plans", "meal_logs",
            "recovery_sessions", "wearable_data", "physical_therapy_plans"
        ]
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table] = cursor.fetchone()[0]
    
    return {
        "database_stats": stats,
        "total_records": sum(stats.values()),
        "last_updated": datetime.now().isoformat()
    }

# ===============================
# USER MANAGEMENT
# ===============================

@app.post("/api/users")
async def create_user(user_data: UserCreate):
    """Create a new user account"""
    try:
        result = fitness_tools.create_user(
            username=user_data.username,
            email=user_data.email,
            profile_data=user_data.profile_data,
            preferences=user_data.preferences
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    """Get user profile and preferences"""
    user = fitness_tools.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ===============================
# EXERCISE LIBRARY
# ===============================

@app.get("/api/exercises")
async def get_exercises(category: Optional[str] = None, muscle_group: Optional[str] = None, 
                       difficulty: Optional[str] = None):
    """Get exercises with optional filtering"""
    try:
        exercises = fitness_tools.get_exercises(category, muscle_group, difficulty)
        return {
            "exercises": exercises,
            "total_count": len(exercises),
            "filters_applied": {
                "category": category,
                "muscle_group": muscle_group, 
                "difficulty": difficulty
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/exercises")
async def add_exercise(exercise_data: ExerciseCreate):
    """Add a new exercise to the library"""
    try:
        result = fitness_tools.add_exercise(
            name=exercise_data.name,
            category=exercise_data.category,
            muscle_groups=exercise_data.muscle_groups,
            equipment=exercise_data.equipment,
            difficulty=exercise_data.difficulty,
            instructions=exercise_data.instructions,
            tips=exercise_data.tips,
            variations=exercise_data.variations
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/exercises/{exercise_id}")
async def get_exercise_details(exercise_id: str):
    """Get detailed information for a specific exercise"""
    exercises = fitness_tools.get_exercises()
    exercise = next((ex for ex in exercises if ex["exercise_id"] == exercise_id), None)
    
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    return exercise

# ===============================
# STRENGTH TRAINING
# ===============================

@app.post("/api/strength/1rm-calculator")
async def calculate_1rm(calculation_data: OneRMCalculation):
    """Calculate 1RM with optional database storage"""
    try:
        if calculation_data.user_id and calculation_data.exercise_name:
            # Save to database and return progression
            result = fitness_tools.save_1rm_progress(
                user_id=calculation_data.user_id,
                exercise_name=calculation_data.exercise_name,
                weight=calculation_data.weight,
                reps=calculation_data.reps,
                method=calculation_data.method,
                bodyweight=calculation_data.bodyweight
            )
        else:
            # Just calculate, don't save
            result = fitness_tools.calculate_1rm(
                weight=calculation_data.weight,
                reps=calculation_data.reps,
                method=calculation_data.method
            )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/strength/program")
async def create_strength_program(program_data: StrengthProgramRequest):
    """Create a strength training program with database storage"""
    try:
        result = fitness_tools.create_strength_program(
            user_id=program_data.user_id,
            program_type=program_data.program_type,
            level=program_data.level,
            duration_weeks=program_data.duration_weeks,
            days_per_week=program_data.days_per_week
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/strength/progress")
async def get_strength_progress(user_id: str, exercise_name: Optional[str] = None, days: int = 90):
    """Get strength progression data from database"""
    try:
        result = fitness_tools.get_strength_progress(user_id, exercise_name, days)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===============================
# WORKOUT SESSIONS
# ===============================

@app.post("/api/workouts/log-session")
async def log_workout_session(session_data: WorkoutSessionLog):
    """Log a completed workout session"""
    try:
        result = fitness_tools.log_workout_session(
            user_id=session_data.user_id,
            workout_type=session_data.workout_type,
            exercises=session_data.exercises,
            duration_minutes=session_data.duration_minutes,
            notes=session_data.notes,
            program_id=session_data.program_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/workouts/history")
async def get_workout_history(user_id: str, workout_type: Optional[str] = None, days: int = 30):
    """Get workout session history"""
    try:
        sessions = fitness_tools.get_workout_history(user_id, workout_type, days)
        return {
            "sessions": sessions,
            "total_sessions": len(sessions),
            "period_days": days,
            "workout_type_filter": workout_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===============================
# SPRINT & CALISTHENICS WORKOUTS
# ===============================

@app.post("/api/workouts/sprint")
async def create_sprint_workout(workout_data: dict):
    """Create a sprint training workout with database integration"""
    
    # Generate sprint workout
    sprint_workout = {
        "workout_type": "sprint_training",
        "warm_up": {
            "duration_minutes": 15,
            "exercises": [
                {"name": "Dynamic Stretching", "duration": "5 minutes"},
                {"name": "Light Jogging", "duration": "5 minutes"},
                {"name": "Sprint Drills", "duration": "5 minutes"}
            ]
        },
        "main_work": {
            "intervals": workout_data.get("intervals", 8),
            "distance": workout_data.get("distance", "100m"),
            "rest_seconds": workout_data.get("rest_seconds", 90),
            "intensity": workout_data.get("intensity", "95%")
        },
        "cool_down": {
            "duration_minutes": 10,
            "exercises": [
                {"name": "Walking", "duration": "5 minutes"},
                {"name": "Static Stretching", "duration": "5 minutes"}
            ]
        }
    }
    
    # If user_id provided, save as workout program
    if "user_id" in workout_data:
        from datetime import datetime
        program_data = {
            "program_id": f"sprint_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_id": workout_data["user_id"],
            "name": "Sprint Training Session",
            "program_type": "cardio",
            "level": workout_data.get("level", "intermediate"),
            "duration_weeks": 1,
            "days_per_week": 1,
            "description": "High-intensity sprint interval training",
            "program_data": json.dumps(sprint_workout),
            "created_at": datetime.now().isoformat(),
            "is_active": True
        }
        
        # Save to database
        with fitness_tools.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO workout_programs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (program_data["program_id"], program_data["user_id"], program_data["name"],
                 program_data["program_type"], program_data["level"], program_data["duration_weeks"],
                 program_data["days_per_week"], program_data["description"], 
                 program_data["program_data"], program_data["created_at"], program_data["is_active"]))
            conn.commit()
    
    return {
        "success": True,
        "workout": sprint_workout,
        "estimated_duration": 40,  # minutes
        "calories_burned_estimate": 300
    }

@app.post("/api/workouts/calisthenics")
async def create_calisthenics_workout(workout_data: dict):
    """Generate calisthenics workout with database integration"""
    
    level = workout_data.get("level", "intermediate")
    focus = workout_data.get("focus", "full_body")
    
    # Calisthenics progressions based on level
    progressions = {
        "beginner": {
            "push_exercise": {"name": "Push-ups", "sets": 3, "reps": "8-12"},
            "pull_exercise": {"name": "Assisted Pull-ups", "sets": 3, "reps": "5-8"},
            "squat_exercise": {"name": "Bodyweight Squats", "sets": 3, "reps": "15-20"},
            "core_exercise": {"name": "Plank", "sets": 3, "duration": "30-45 seconds"}
        },
        "intermediate": {
            "push_exercise": {"name": "Diamond Push-ups", "sets": 4, "reps": "10-15"},
            "pull_exercise": {"name": "Pull-ups", "sets": 4, "reps": "8-12"},
            "squat_exercise": {"name": "Pistol Squat Progression", "sets": 3, "reps": "5-8 each leg"},
            "core_exercise": {"name": "L-sit Hold", "sets": 3, "duration": "15-30 seconds"}
        },
        "advanced": {
            "push_exercise": {"name": "Handstand Push-ups", "sets": 4, "reps": "5-10"},
            "pull_exercise": {"name": "Muscle-ups", "sets": 4, "reps": "3-6"},
            "squat_exercise": {"name": "Shrimp Squats", "sets": 3, "reps": "3-5 each leg"},
            "core_exercise": {"name": "Front Lever Hold", "sets": 3, "duration": "10-20 seconds"}
        }
    }
    
    workout_plan = progressions.get(level, progressions["intermediate"])
    
    calisthenics_workout = {
        "workout_type": "calisthenics",
        "level": level,
        "focus": focus,
        "warm_up": [
            {"name": "Joint Mobility", "duration": "5 minutes"},
            {"name": "Dynamic Stretching", "duration": "5 minutes"}
        ],
        "main_exercises": [
            workout_plan["push_exercise"],
            workout_plan["pull_exercise"],
            workout_plan["squat_exercise"],
            workout_plan["core_exercise"]
        ],
        "skill_work": [
            {"name": "Handstand Practice", "duration": "10 minutes"},
            {"name": "Balance Training", "duration": "5 minutes"}
        ],
        "cool_down": [
            {"name": "Static Stretching", "duration": "10 minutes"}
        ]
    }
    
    # Save to database if user_id provided
    if "user_id" in workout_data:
        from datetime import datetime
        program_data = {
            "program_id": f"calisthenics_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_id": workout_data["user_id"],
            "name": f"{level.title()} Calisthenics Program",
            "program_type": "calisthenics",
            "level": level,
            "duration_weeks": 4,
            "days_per_week": 3,
            "description": f"{level.title()} bodyweight training with skill progressions",
            "program_data": json.dumps(calisthenics_workout),
            "created_at": datetime.now().isoformat(),
            "is_active": True
        }
        
        with fitness_tools.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO workout_programs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (program_data["program_id"], program_data["user_id"], program_data["name"],
                 program_data["program_type"], program_data["level"], program_data["duration_weeks"],
                 program_data["days_per_week"], program_data["description"],
                 program_data["program_data"], program_data["created_at"], program_data["is_active"]))
            conn.commit()
    
    return {
        "success": True,
        "workout": calisthenics_workout,
        "estimated_duration": 45,  # minutes
        "progression_notes": [
            "Focus on perfect form over speed",
            "Progress to next level when you can complete max reps easily",
            "Rest 60-90 seconds between sets"
        ]
    }

# ===============================
# NUTRITION
# ===============================

@app.post("/api/nutrition/plan")
async def create_nutrition_plan(plan_data: NutritionPlanRequest):
    """Create a personalized nutrition plan"""
    try:
        result = fitness_tools.create_nutrition_plan(
            user_id=plan_data.user_id,
            goal_type=plan_data.goal_type,
            daily_calories=plan_data.daily_calories,
            protein_percent=plan_data.protein_percent,
            carb_percent=plan_data.carb_percent,
            fat_percent=plan_data.fat_percent,
            restrictions=plan_data.restrictions
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/nutrition/log-meal")
async def log_meal(meal_data: MealLogRequest):
    """Log a meal with nutritional information"""
    try:
        result = fitness_tools.log_meal(
            user_id=meal_data.user_id,
            meal_type=meal_data.meal_type,
            foods=meal_data.foods,
            plan_id=meal_data.plan_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/nutrition/daily-summary")
async def get_daily_nutrition_summary(user_id: str, date: Optional[str] = None):
    """Get daily nutrition summary from logged meals"""
    if not date:
        date = datetime.now().date().isoformat()
    
    with fitness_tools.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT meal_type, calories, macros FROM meal_logs
            WHERE user_id = ? AND date = ?
            ORDER BY logged_at
        ''', (user_id, date))
        
        meals = []
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        
        for row in cursor.fetchall():
            meal_type, calories, macros_json = row
            macros = json.loads(macros_json)
            
            meals.append({
                "meal_type": meal_type,
                "calories": calories,
                "macros": macros
            })
            
            total_calories += calories
            total_protein += macros.get("protein_grams", 0)
            total_carbs += macros.get("carbs_grams", 0)
            total_fat += macros.get("fat_grams", 0)
    
    return {
        "date": date,
        "meals": meals,
        "daily_totals": {
            "calories": total_calories,
            "protein_grams": total_protein,
            "carbs_grams": total_carbs,
            "fat_grams": total_fat
        }
    }

# ===============================
# RECOVERY
# ===============================

@app.post("/api/recovery/log-session")
async def log_recovery_session(recovery_data: RecoverySessionRequest):
    """Log a recovery session"""
    try:
        result = fitness_tools.log_recovery_session(
            user_id=recovery_data.user_id,
            recovery_type=recovery_data.recovery_type,
            duration_minutes=recovery_data.duration_minutes,
            quality_rating=recovery_data.quality_rating,
            activities=recovery_data.activities,
            metrics=recovery_data.metrics
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/recovery/assessment")
async def get_recovery_assessment(user_id: str):
    """Get recovery readiness assessment"""
    
    # Get recent recovery sessions
    with fitness_tools.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT recovery_type, quality_rating, metrics FROM recovery_sessions
            WHERE user_id = ? AND date >= date('now', '-7 days')
            ORDER BY date DESC
        ''', (user_id,))
        
        recent_sessions = []
        quality_scores = []
        
        for row in cursor.fetchall():
            recovery_type, quality_rating, metrics_json = row
            recent_sessions.append({
                "type": recovery_type,
                "quality": quality_rating,
                "metrics": json.loads(metrics_json)
            })
            quality_scores.append(quality_rating)
    
    # Calculate assessment
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 5
    
    assessment = {
        "recovery_score": round(avg_quality, 1),
        "status": "Good" if avg_quality >= 7 else "Moderate" if avg_quality >= 5 else "Poor",
        "recommendations": [],
        "recent_sessions": recent_sessions
    }
    
    # Add recommendations based on score
    if avg_quality < 5:
        assessment["recommendations"] = [
            "Prioritize 8+ hours of sleep",
            "Reduce training intensity",
            "Add active recovery sessions",
            "Consider stress management techniques"
        ]
    elif avg_quality < 7:
        assessment["recommendations"] = [
            "Maintain current sleep schedule",
            "Add light stretching or yoga",
            "Monitor stress levels",
            "Stay hydrated"
        ]
    else:
        assessment["recommendations"] = [
            "Continue current recovery practices",
            "You're ready for challenging workouts",
            "Consider progressive overload"
        ]
    
    return assessment

# ===============================
# ANALYTICS & REPORTS
# ===============================

@app.get("/api/analytics/dashboard")
async def get_analytics_dashboard(user_id: str, days: int = 30):
    """Get comprehensive fitness analytics dashboard"""
    try:
        analytics = fitness_tools.generate_workout_analytics(user_id, days)
        
        # Add nutrition summary
        with fitness_tools.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*), AVG(calories) FROM meal_logs
                WHERE user_id = ? AND date >= date('now', '-{} days')
            '''.format(days), (user_id,))
            
            nutrition_row = cursor.fetchone()
            nutrition_summary = {
                "meals_logged": nutrition_row[0] if nutrition_row[0] else 0,
                "avg_daily_calories": round(nutrition_row[1], 0) if nutrition_row[1] else 0
            }
        
        # Add recovery summary
        with fitness_tools.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*), AVG(quality_rating) FROM recovery_sessions
                WHERE user_id = ? AND date >= date('now', '-{} days')
            '''.format(days), (user_id,))
            
            recovery_row = cursor.fetchone()
            recovery_summary = {
                "recovery_sessions": recovery_row[0] if recovery_row[0] else 0,
                "avg_quality_rating": round(recovery_row[1], 1) if recovery_row[1] else 0
            }
        
        return {
            **analytics,
            "nutrition_summary": nutrition_summary,
            "recovery_summary": recovery_summary,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/progress-report")
async def get_progress_report(user_id: str, weeks: int = 12):
    """Generate comprehensive progress report"""
    days = weeks * 7
    
    try:
        # Get workout progress
        workout_analytics = fitness_tools.generate_workout_analytics(user_id, days)
        
        # Get strength progress
        strength_progress = fitness_tools.get_strength_progress(user_id, days=days)
        
        # Calculate weekly averages
        weekly_stats = {}
        for week in range(weeks):
            week_start = (datetime.now() - timedelta(days=(weeks - week) * 7)).date()
            week_end = (week_start + timedelta(days=6))
            
            with fitness_tools.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT COUNT(*), AVG(duration_minutes) FROM workout_sessions
                    WHERE user_id = ? AND date BETWEEN ? AND ?
                ''', (user_id, week_start.isoformat(), week_end.isoformat()))
                
                row = cursor.fetchone()
                weekly_stats[f"week_{week + 1}"] = {
                    "workouts": row[0] if row[0] else 0,
                    "avg_duration": round(row[1], 1) if row[1] else 0
                }
        
        return {
            "report_period": f"{weeks} weeks",
            "overall_progress": workout_analytics,
            "strength_gains": strength_progress,
            "weekly_breakdown": weekly_stats,
            "report_generated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===============================
# STARTUP
# ===============================

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Comprehensive Fitness API with Database Storage")
    print("📊 Database: SQLite with persistent storage for all workout sections")
    print("🌐 Server: http://localhost:8001")
    print("📖 API Docs: http://localhost:8001/docs")
    print("📈 Database Stats: http://localhost:8001/api/database/stats")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)