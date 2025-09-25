"""
Comprehensive Workout Database Tools
Database operations for all fitness sections with persistent storage
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from comprehensive_fitness_database import (
    ComprehensiveFitnessDatabase, User, Exercise, WorkoutProgram, 
    WorkoutSession, StrengthProgression, NutritionPlan, MealLog,
    RecoverySession, WearableData, PhysicalTherapyPlan, WorkoutAnalytics
)

class ComprehensiveWorkoutTools:
    """Database-powered fitness tools for all workout sections"""
    
    def __init__(self, db_path: str = "comprehensive_fitness.db"):
        self.db = ComprehensiveFitnessDatabase(db_path)
    
    # ===============================
    # USER MANAGEMENT
    # ===============================
    
    def create_user(self, username: str, email: str, profile_data: Dict, preferences: Dict) -> Dict:
        """Create a new user account"""
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            created_at=datetime.now().isoformat(),
            profile_data=json.dumps(profile_data),
            preferences=json.dumps(preferences)
        )
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)
            ''', (user.user_id, user.username, user.email, user.created_at,
                 user.profile_data, user.preferences))
            conn.commit()
        
        return {
            "success": True,
            "user_id": user_id,
            "message": f"User {username} created successfully"
        }
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user profile and preferences"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM users WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    "user_id": row[0],
                    "username": row[1],
                    "email": row[2],
                    "created_at": row[3],
                    "profile_data": json.loads(row[4]),
                    "preferences": json.loads(row[5])
                }
        return None
    
    # ===============================
    # EXERCISE LIBRARY
    # ===============================
    
    def get_exercises(self, category: Optional[str] = None, muscle_group: Optional[str] = None,
                     difficulty: Optional[str] = None) -> List[Dict]:
        """Get exercises with optional filtering"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM exercises WHERE 1=1"
            params = []
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            if difficulty:
                query += " AND difficulty = ?"
                params.append(difficulty)
            
            if muscle_group:
                query += " AND muscle_groups LIKE ?"
                params.append(f"%{muscle_group}%")
            
            cursor.execute(query, params)
            exercises = []
            
            for row in cursor.fetchall():
                exercises.append({
                    "exercise_id": row[0],
                    "name": row[1],
                    "category": row[2],
                    "muscle_groups": json.loads(row[3]),
                    "equipment": json.loads(row[4]),
                    "difficulty": row[5],
                    "instructions": json.loads(row[6]),
                    "tips": json.loads(row[7]),
                    "variations": json.loads(row[8]),
                    "created_at": row[9]
                })
            
            return exercises
    
    def add_exercise(self, name: str, category: str, muscle_groups: List[str],
                    equipment: List[str], difficulty: str, instructions: List[str],
                    tips: List[str], variations: List[str]) -> Dict:
        """Add a new exercise to the library"""
        exercise_id = f"ex_{uuid.uuid4().hex[:8]}"
        exercise = Exercise(
            exercise_id=exercise_id,
            name=name,
            category=category,
            muscle_groups=json.dumps(muscle_groups),
            equipment=json.dumps(equipment),
            difficulty=difficulty,
            instructions=json.dumps(instructions),
            tips=json.dumps(tips),
            variations=json.dumps(variations),
            created_at=datetime.now().isoformat()
        )
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO exercises VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (exercise.exercise_id, exercise.name, exercise.category,
                 exercise.muscle_groups, exercise.equipment, exercise.difficulty,
                 exercise.instructions, exercise.tips, exercise.variations,
                 exercise.created_at))
            conn.commit()
        
        return {"success": True, "exercise_id": exercise_id, "message": "Exercise added successfully"}
    
    # ===============================
    # STRENGTH TRAINING
    # ===============================
    
    def calculate_1rm(self, weight: float, reps: int, method: str = "epley") -> Dict:
        """Calculate 1RM using various formulas with database storage"""
        formulas = {
            "epley": lambda w, r: w * (1 + r/30),
            "brzycki": lambda w, r: w * (36 / (37 - r)),
            "lombardi": lambda w, r: w * (r ** 0.10),
            "mcglothin": lambda w, r: (100 * w) / (101.3 - 2.67123 * r),
            "oconner": lambda w, r: w * (1 + 0.025 * r)
        }
        
        if method not in formulas:
            method = "epley"
        
        one_rm = round(formulas[method](weight, reps), 1)
        
        # Calculate training percentages
        percentages = {}
        for percent in [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]:
            percentages[f"{percent}%"] = round(one_rm * (percent / 100), 1)
        
        return {
            "one_rep_max": one_rm,
            "method_used": method,
            "original_lift": {"weight": weight, "reps": reps},
            "training_percentages": percentages,
            "formulas_comparison": {name: round(formula(weight, reps), 1) 
                                  for name, formula in formulas.items()}
        }
    
    def save_1rm_progress(self, user_id: str, exercise_name: str, weight: float, 
                         reps: int, method: str = "epley", bodyweight: float = 180.0) -> Dict:
        """Save 1RM progression to database"""
        # Calculate 1RM
        one_rm_data = self.calculate_1rm(weight, reps, method)
        one_rm = one_rm_data["one_rep_max"]
        
        # Find exercise_id
        exercises = self.get_exercises()
        exercise_id = None
        for ex in exercises:
            if exercise_name.lower() in ex["name"].lower():
                exercise_id = ex["exercise_id"]
                break
        
        if not exercise_id:
            exercise_id = f"ex_{uuid.uuid4().hex[:8]}"
        
        progression_id = f"prog_{uuid.uuid4().hex[:8]}"
        progression = StrengthProgression(
            progression_id=progression_id,
            user_id=user_id,
            exercise_id=exercise_id,
            date=date.today().isoformat(),
            one_rep_max=one_rm,
            calculated_method=method,
            actual_max=None,
            bodyweight=bodyweight,
            notes=f"Calculated from {weight} x {reps}"
        )
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO strength_progression VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (progression.progression_id, progression.user_id, progression.exercise_id,
                 progression.date, progression.one_rep_max, progression.calculated_method,
                 progression.actual_max, progression.bodyweight, progression.notes))
            conn.commit()
        
        return {
            "success": True,
            "progression_id": progression_id,
            **one_rm_data
        }
    
    def create_strength_program(self, user_id: str, program_type: str, level: str,
                               duration_weeks: int = 12, days_per_week: int = 3) -> Dict:
        """Create a strength training program with database storage"""
        
        programs = {
            "starting_strength": {
                "name": "Starting Strength",
                "description": "Linear progression focusing on compound movements",
                "exercises": [
                    {"name": "Back Squat", "sets": "3x5", "intensity": "Work up to 5RM, add 5lbs next session"},
                    {"name": "Bench Press", "sets": "3x5", "intensity": "Work up to 5RM, add 2.5lbs next session"},
                    {"name": "Deadlift", "sets": "1x5", "intensity": "Work up to 5RM, add 5lbs next session"},
                    {"name": "Overhead Press", "sets": "3x5", "intensity": "Alternate with bench press"},
                    {"name": "Barbell Row", "sets": "3x5", "intensity": "Same weight as bench press"}
                ],
                "training_notes": [
                    "Add weight every session if all reps completed",
                    "Rest 3-5 minutes between sets", 
                    "Focus on perfect form",
                    "Deload 10% if you fail 3 sessions in a row"
                ]
            },
            "531_program": {
                "name": "5/3/1 Program",
                "description": "Periodized strength program with accessory work",
                "exercises": [
                    {"name": "Squat", "sets": "5/3/1 + FSL", "intensity": "Based on 90% training max"},
                    {"name": "Bench Press", "sets": "5/3/1 + FSL", "intensity": "Based on 90% training max"},
                    {"name": "Deadlift", "sets": "5/3/1 + FSL", "intensity": "Based on 90% training max"},
                    {"name": "Overhead Press", "sets": "5/3/1 + FSL", "intensity": "Based on 90% training max"},
                    {"name": "Accessory Work", "sets": "50-100 reps", "intensity": "Push, Pull, Single Leg/Core"}
                ],
                "training_notes": [
                    "Calculate training max as 90% of current 1RM",
                    "Week 1: 5+ @ 85%, Week 2: 3+ @ 90%, Week 3: 1+ @ 95%",
                    "First Set Last (FSL) for volume work",
                    "Increase training max 5lbs upper, 10lbs lower each cycle"
                ]
            },
            "powerlifting": {
                "name": "Powerlifting Competition Prep",
                "description": "Competition-focused program for squat, bench, deadlift",
                "exercises": [
                    {"name": "Competition Squat", "sets": "Work to opener/2nd/3rd", "intensity": "85-105% range"},
                    {"name": "Competition Bench", "sets": "Work to opener/2nd/3rd", "intensity": "85-105% range"}, 
                    {"name": "Competition Deadlift", "sets": "Work to opener/2nd/3rd", "intensity": "85-105% range"},
                    {"name": "Pause Bench", "sets": "3x3", "intensity": "80-90%"},
                    {"name": "Deficit Deadlift", "sets": "3x3", "intensity": "80-85%"}
                ],
                "training_notes": [
                    "Practice competition commands and timing",
                    "Opener should be 90-95% of current max",
                    "Second attempt should be 100-103% for new PR",
                    "Third attempt can be 105-108% for big PR"
                ]
            },
            "olympic_lifting": {
                "name": "Olympic Lifting Development",
                "description": "Technique and strength for snatch and clean & jerk",
                "exercises": [
                    {"name": "Snatch", "sets": "Work up to daily max", "intensity": "80-100%"},
                    {"name": "Clean & Jerk", "sets": "Work up to daily max", "intensity": "80-100%"},
                    {"name": "Front Squat", "sets": "3x3", "intensity": "85-95%"},
                    {"name": "Overhead Squat", "sets": "3x5", "intensity": "70-80%"},
                    {"name": "Romanian Deadlift", "sets": "3x8", "intensity": "70-75%"}
                ],
                "training_notes": [
                    "Technique work should be prioritized over heavy weight",
                    "Work up to daily training max, not absolute max",
                    "Film lifts to analyze technique",
                    "Mobility work is essential for proper positions"
                ]
            }
        }
        
        if program_type not in programs:
            program_type = "starting_strength"
        
        program_data = programs[program_type]
        
        # Create database entry
        program_id = f"prog_{uuid.uuid4().hex[:8]}"
        program = WorkoutProgram(
            program_id=program_id,
            user_id=user_id,
            name=program_data["name"],
            program_type="strength",
            level=level,
            duration_weeks=duration_weeks,
            days_per_week=days_per_week,
            description=program_data["description"],
            program_data=json.dumps(program_data),
            created_at=datetime.now().isoformat(),
            is_active=True
        )
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO workout_programs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (program.program_id, program.user_id, program.name,
                 program.program_type, program.level, program.duration_weeks,
                 program.days_per_week, program.description, program.program_data,
                 program.created_at, program.is_active))
            conn.commit()
        
        return {
            "success": True,
            "program_id": program_id,
            "program": {
                "name": program_data["name"],
                "description": program_data["description"],
                "weeks": duration_weeks,
                "days_per_week": days_per_week,
                "level": level,
                "exercises": program_data["exercises"]
            },
            "training_notes": program_data["training_notes"]
        }
    
    def get_strength_progress(self, user_id: str, exercise_name: Optional[str] = None,
                             days: int = 90) -> Dict:
        """Get strength progression data from database"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Base query
            query = '''
                SELECT sp.*, e.name as exercise_name
                FROM strength_progression sp
                JOIN exercises e ON sp.exercise_id = e.exercise_id
                WHERE sp.user_id = ? AND sp.date >= ?
            '''
            params = [user_id, (datetime.now() - timedelta(days=days)).date().isoformat()]
            
            if exercise_name:
                query += " AND e.name LIKE ?"
                params.append(f"%{exercise_name}%")
            
            query += " ORDER BY sp.date DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            progress_data = []
            for row in rows:
                progress_data.append({
                    "date": row[3],
                    "exercise": row[10],  # exercise_name from JOIN
                    "one_rep_max": row[4],
                    "method": row[5],
                    "bodyweight": row[7],
                    "notes": row[8]
                })
            
            # Calculate trends
            if len(progress_data) >= 2:
                latest = progress_data[0]
                earliest = progress_data[-1]
                gain = latest["one_rep_max"] - earliest["one_rep_max"]
                gain_percent = (gain / earliest["one_rep_max"]) * 100 if earliest["one_rep_max"] > 0 else 0
            else:
                gain = 0
                gain_percent = 0
            
            return {
                "progress_data": progress_data,
                "summary": {
                    "total_entries": len(progress_data),
                    "date_range": f"{days} days",
                    "strength_gain": gain,
                    "gain_percentage": round(gain_percent, 1)
                }
            }
    
    # ===============================
    # WORKOUT SESSIONS
    # ===============================
    
    def log_workout_session(self, user_id: str, workout_type: str, exercises: List[Dict],
                           duration_minutes: int, notes: str = "", program_id: Optional[str] = None) -> Dict:
        """Log a completed workout session"""
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        # Calculate performance metrics
        total_volume = 0
        total_reps = 0
        
        for exercise in exercises:
            sets = exercise.get("sets", 0)
            reps = exercise.get("reps", 0)
            weight = exercise.get("weight", 0)
            total_volume += sets * reps * weight
            total_reps += sets * reps
        
        performance_data = {
            "total_volume": total_volume,
            "total_reps": total_reps,
            "average_intensity": total_volume / total_reps if total_reps > 0 else 0
        }
        
        session = WorkoutSession(
            session_id=session_id,
            user_id=user_id,
            program_id=program_id,
            workout_type=workout_type,
            date=date.today().isoformat(),
            duration_minutes=duration_minutes,
            exercises_performed=json.dumps(exercises),
            performance_data=json.dumps(performance_data),
            notes=notes,
            created_at=datetime.now().isoformat()
        )
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO workout_sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (session.session_id, session.user_id, session.program_id,
                 session.workout_type, session.date, session.duration_minutes,
                 session.exercises_performed, session.performance_data,
                 session.notes, session.created_at))
            conn.commit()
        
        return {
            "success": True,
            "session_id": session_id,
            "performance_summary": performance_data,
            "message": f"{workout_type.title()} workout logged successfully"
        }
    
    def get_workout_history(self, user_id: str, workout_type: Optional[str] = None,
                           days: int = 30) -> List[Dict]:
        """Get workout session history"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT * FROM workout_sessions 
                WHERE user_id = ? AND date >= ?
            '''
            params = [user_id, (datetime.now() - timedelta(days=days)).date().isoformat()]
            
            if workout_type:
                query += " AND workout_type = ?"
                params.append(workout_type)
            
            query += " ORDER BY date DESC"
            
            cursor.execute(query, params)
            sessions = []
            
            for row in cursor.fetchall():
                sessions.append({
                    "session_id": row[0],
                    "workout_type": row[3],
                    "date": row[4],
                    "duration_minutes": row[5],
                    "exercises": json.loads(row[6]),
                    "performance": json.loads(row[7]),
                    "notes": row[8]
                })
            
            return sessions
    
    # ===============================
    # NUTRITION TOOLS
    # ===============================
    
    def create_nutrition_plan(self, user_id: str, goal_type: str, daily_calories: int,
                             protein_percent: float = 25, carb_percent: float = 45,
                             fat_percent: float = 30, restrictions: List[str] = None) -> Dict:
        """Create a personalized nutrition plan"""
        
        if restrictions is None:
            restrictions = []
        
        # Calculate macros
        protein_grams = (daily_calories * protein_percent / 100) / 4
        carb_grams = (daily_calories * carb_percent / 100) / 4
        fat_grams = (daily_calories * fat_percent / 100) / 9
        
        macros = {
            "protein_percent": protein_percent,
            "carbs_percent": carb_percent,
            "fat_percent": fat_percent,
            "protein_grams": round(protein_grams),
            "carbs_grams": round(carb_grams),
            "fat_grams": round(fat_grams)
        }
        
        # Generate meal plan based on goal
        meal_plans = {
            "weight_loss": {
                "breakfast": ["egg_whites", "oatmeal", "berries"],
                "lunch": ["lean_protein", "quinoa", "vegetables"],
                "dinner": ["fish", "sweet_potato", "leafy_greens"],
                "snacks": ["greek_yogurt", "almonds"]
            },
            "muscle_gain": {
                "breakfast": ["whole_eggs", "oatmeal", "banana", "protein_shake"],
                "lunch": ["chicken_breast", "brown_rice", "mixed_vegetables"],
                "dinner": ["lean_beef", "pasta", "broccoli"],
                "snacks": ["cottage_cheese", "nuts", "fruit"]
            },
            "maintenance": {
                "breakfast": ["eggs", "toast", "avocado"],
                "lunch": ["turkey_sandwich", "soup", "fruit"],
                "dinner": ["salmon", "rice", "asparagus"],
                "snacks": ["yogurt", "trail_mix"]
            }
        }
        
        meal_plan = meal_plans.get(goal_type, meal_plans["maintenance"])
        
        # Create database entry
        plan_id = f"nutr_{uuid.uuid4().hex[:8]}"
        plan = NutritionPlan(
            plan_id=plan_id,
            user_id=user_id,
            name=f"{goal_type.replace('_', ' ').title()} Plan",
            goal_type=goal_type,
            daily_calories=daily_calories,
            macros=json.dumps(macros),
            meal_plan=json.dumps(meal_plan),
            restrictions=json.dumps(restrictions),
            created_at=datetime.now().isoformat(),
            is_active=True
        )
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO nutrition_plans VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (plan.plan_id, plan.user_id, plan.name, plan.goal_type,
                 plan.daily_calories, plan.macros, plan.meal_plan,
                 plan.restrictions, plan.created_at, plan.is_active))
            conn.commit()
        
        return {
            "success": True,
            "plan_id": plan_id,
            "nutrition_plan": {
                "name": plan.name,
                "goal": goal_type,
                "daily_calories": daily_calories,
                "macros": macros,
                "meal_plan": meal_plan,
                "restrictions": restrictions
            }
        }
    
    def log_meal(self, user_id: str, meal_type: str, foods: List[Dict], 
                plan_id: Optional[str] = None) -> Dict:
        """Log a meal with nutritional information"""
        
        # Calculate totals from foods
        total_calories = sum(food.get("calories", 0) for food in foods)
        total_protein = sum(food.get("protein", 0) for food in foods)
        total_carbs = sum(food.get("carbs", 0) for food in foods)
        total_fat = sum(food.get("fat", 0) for food in foods)
        
        macros = {
            "protein_grams": total_protein,
            "carbs_grams": total_carbs,
            "fat_grams": total_fat
        }
        
        log_id = f"meal_{uuid.uuid4().hex[:8]}"
        meal_log = MealLog(
            log_id=log_id,
            user_id=user_id,
            plan_id=plan_id,
            date=date.today().isoformat(),
            meal_type=meal_type,
            foods=json.dumps(foods),
            calories=total_calories,
            macros=json.dumps(macros),
            logged_at=datetime.now().isoformat()
        )
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO meal_logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (meal_log.log_id, meal_log.user_id, meal_log.plan_id,
                 meal_log.date, meal_log.meal_type, meal_log.foods,
                 meal_log.calories, meal_log.macros, meal_log.logged_at))
            conn.commit()
        
        return {
            "success": True,
            "log_id": log_id,
            "meal_summary": {
                "meal_type": meal_type,
                "total_calories": total_calories,
                "macros": macros
            }
        }
    
    # ===============================
    # RECOVERY TOOLS
    # ===============================
    
    def log_recovery_session(self, user_id: str, recovery_type: str, duration_minutes: int,
                            quality_rating: int, activities: List[str], metrics: Dict = None) -> Dict:
        """Log a recovery session"""
        
        if metrics is None:
            metrics = {}
        
        recovery_id = f"recovery_{uuid.uuid4().hex[:8]}"
        recovery = RecoverySession(
            recovery_id=recovery_id,
            user_id=user_id,
            date=date.today().isoformat(),
            recovery_type=recovery_type,
            duration_minutes=duration_minutes,
            quality_rating=quality_rating,
            metrics=json.dumps(metrics),
            activities=json.dumps(activities),
            notes=""
        )
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recovery_sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (recovery.recovery_id, recovery.user_id, recovery.date,
                 recovery.recovery_type, recovery.duration_minutes, recovery.quality_rating,
                 recovery.metrics, recovery.activities, recovery.notes))
            conn.commit()
        
        return {
            "success": True,
            "recovery_id": recovery_id,
            "session_summary": {
                "type": recovery_type,
                "duration": duration_minutes,
                "quality": quality_rating,
                "activities": activities
            }
        }
    
    # ===============================
    # ANALYTICS & REPORTS
    # ===============================
    
    def generate_workout_analytics(self, user_id: str, days: int = 30) -> Dict:
        """Generate comprehensive workout analytics"""
        
        # Get workout sessions
        sessions = self.get_workout_history(user_id, days=days)
        
        if not sessions:
            return {"message": "No workout data found for this period"}
        
        # Calculate metrics
        total_workouts = len(sessions)
        total_volume = sum(session["performance"].get("total_volume", 0) for session in sessions)
        avg_duration = sum(session["duration_minutes"] for session in sessions) / total_workouts
        
        # Workout type breakdown
        type_counts = {}
        for session in sessions:
            workout_type = session["workout_type"]
            type_counts[workout_type] = type_counts.get(workout_type, 0) + 1
        
        # Get strength progress
        strength_progress = self.get_strength_progress(user_id, days=days)
        
        analytics = {
            "period_summary": {
                "days_analyzed": days,
                "total_workouts": total_workouts,
                "total_volume": total_volume,
                "average_duration": round(avg_duration, 1),
                "workout_frequency": round(total_workouts / (days / 7), 1)  # workouts per week
            },
            "workout_breakdown": type_counts,
            "strength_progress": strength_progress["summary"],
            "trends": {
                "consistency": "High" if total_workouts >= days / 3 else "Moderate" if total_workouts >= days / 7 else "Low",
                "volume_trend": "Increasing" if total_volume > 0 else "Stable"
            }
        }
        
        return analytics

if __name__ == "__main__":
    # Test the comprehensive tools
    tools = ComprehensiveWorkoutTools()
    print("✅ Comprehensive Workout Tools initialized successfully!")