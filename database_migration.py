"""
Database Migration and Initialization Tool
Ensures comprehensive fitness database is properly set up and migrated
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from comprehensive_fitness_models import ComprehensiveFitnessDatabase
import logging

logger = logging.getLogger(__name__)

class DatabaseMigrator:
    """Handles database migrations and data integrity"""
    
    def __init__(self, db_path: str = "comprehensive_fitness.db"):
        self.db_path = db_path
        self.comprehensive_db = ComprehensiveFitnessDatabase(db_path)
    
    def migrate_from_simple_db(self, simple_db_path: str = "fitness.db"):
        """Migrate data from simple fitness.db to comprehensive schema"""
        if not Path(simple_db_path).exists():
            logger.info(f"Simple database {simple_db_path} not found, creating fresh database")
            self.initialize_fresh_database()
            return
        
        logger.info(f"Migrating data from {simple_db_path} to {self.db_path}")
        
        with sqlite3.connect(simple_db_path) as simple_conn:
            simple_cursor = simple_conn.cursor()
            
            # Check what tables exist in simple database
            simple_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            simple_tables = [table[0] for table in simple_cursor.fetchall()]
            
            logger.info(f"Found tables in simple database: {simple_tables}")
            
            # Migrate users if exists
            if 'users' in simple_tables:
                self._migrate_users(simple_cursor)
            
            # Migrate workouts if exists
            if 'workouts' in simple_tables:
                self._migrate_workouts(simple_cursor)
            
            # Migrate exercises if exists  
            if 'exercises' in simple_tables:
                self._migrate_exercises(simple_cursor)
                
        logger.info("Migration completed successfully")
    
    def _migrate_users(self, simple_cursor):
        """Migrate user data to comprehensive schema"""
        try:
            simple_cursor.execute("SELECT * FROM users")
            users = simple_cursor.fetchall()
            
            # Get column names
            simple_cursor.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in simple_cursor.fetchall()]
            
            logger.info(f"Migrating {len(users)} users with columns: {columns}")
            
            with sqlite3.connect(self.db_path) as comp_conn:
                comp_cursor = comp_conn.cursor()
                
                for user_row in users:
                    user_dict = dict(zip(columns, user_row))
                    
                    # Map simple schema to comprehensive schema
                    user_data = {
                        'user_id': user_dict.get('id', f"migrated_{datetime.now().timestamp()}"),
                        'email': user_dict.get('email', f"user_{user_dict.get('id')}@example.com"),
                        'name': user_dict.get('name', 'Migrated User'),
                        'date_of_birth': user_dict.get('date_of_birth', '1990-01-01'),
                        'gender': user_dict.get('gender', 'not_specified'),
                        'height_cm': user_dict.get('height_cm', 170.0),
                        'current_weight_kg': user_dict.get('weight_kg', user_dict.get('current_weight_kg', 70.0)),
                        'fitness_level': user_dict.get('fitness_level', 'intermediate'),
                        'goals': json.dumps(user_dict.get('goals', ['general_fitness']).split(',') if isinstance(user_dict.get('goals'), str) else user_dict.get('goals', ['general_fitness'])),
                        'injuries': json.dumps(user_dict.get('injuries', '').split(',') if user_dict.get('injuries') else []),
                        'preferences': json.dumps(user_dict.get('preferences', {})),
                        'created_at': user_dict.get('created_at', datetime.now().isoformat()),
                        'last_active': user_dict.get('last_active', datetime.now().isoformat())
                    }
                    
                    comp_cursor.execute('''
                        INSERT OR REPLACE INTO users_enhanced 
                        (user_id, email, name, date_of_birth, gender, height_cm, current_weight_kg,
                         fitness_level, goals, injuries, preferences, created_at, last_active)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', tuple(user_data.values()))
                    
                comp_conn.commit()
                logger.info(f"Successfully migrated {len(users)} users")
                
        except Exception as e:
            logger.error(f"Error migrating users: {e}")
    
    def _migrate_workouts(self, simple_cursor):
        """Migrate workout data to comprehensive schema"""
        try:
            simple_cursor.execute("SELECT * FROM workouts")
            workouts = simple_cursor.fetchall()
            
            # Get column names
            simple_cursor.execute("PRAGMA table_info(workouts)")
            columns = [col[1] for col in simple_cursor.fetchall()]
            
            logger.info(f"Migrating {len(workouts)} workouts with columns: {columns}")
            
            with sqlite3.connect(self.db_path) as comp_conn:
                comp_cursor = comp_conn.cursor()
                
                for workout_row in workouts:
                    workout_dict = dict(zip(columns, workout_row))
                    
                    # Map to comprehensive workout session schema
                    session_data = {
                        'session_id': workout_dict.get('id', f"migrated_session_{datetime.now().timestamp()}"),
                        'user_id': workout_dict.get('user_id', 'user_001'),
                        'program_id': workout_dict.get('program_id'),  # May be None
                        'workout_name': workout_dict.get('name', workout_dict.get('workout_name', 'Migrated Workout')),
                        'start_time': workout_dict.get('start_time', workout_dict.get('created_at', datetime.now().isoformat())),
                        'end_time': workout_dict.get('end_time'),  # May be None
                        'exercises_completed': json.dumps(workout_dict.get('exercises', [])),
                        'total_volume_kg': workout_dict.get('total_volume_kg', 0.0),
                        'calories_burned': workout_dict.get('calories_burned', 0),
                        'average_heart_rate': workout_dict.get('avg_heart_rate'),
                        'max_heart_rate': workout_dict.get('max_heart_rate'),
                        'rpe_score': workout_dict.get('rpe_score'),
                        'notes': workout_dict.get('notes', ''),
                        'mood_before': workout_dict.get('mood_before'),
                        'mood_after': workout_dict.get('mood_after'),
                        'created_at': workout_dict.get('created_at', datetime.now().isoformat())
                    }
                    
                    comp_cursor.execute('''
                        INSERT OR REPLACE INTO workout_sessions_enhanced 
                        (session_id, user_id, program_id, workout_name, start_time, end_time,
                         exercises_completed, total_volume_kg, calories_burned, average_heart_rate,
                         max_heart_rate, rpe_score, notes, mood_before, mood_after, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', tuple(session_data.values()))
                
                comp_conn.commit()
                logger.info(f"Successfully migrated {len(workouts)} workout sessions")
                
        except Exception as e:
            logger.error(f"Error migrating workouts: {e}")
    
    def _migrate_exercises(self, simple_cursor):
        """Migrate exercise data to comprehensive schema"""
        try:
            simple_cursor.execute("SELECT * FROM exercises")
            exercises = simple_cursor.fetchall()
            
            # Get column names
            simple_cursor.execute("PRAGMA table_info(exercises)")
            columns = [col[1] for col in simple_cursor.fetchall()]
            
            logger.info(f"Migrating {len(exercises)} exercises with columns: {columns}")
            
            with sqlite3.connect(self.db_path) as comp_conn:
                comp_cursor = comp_conn.cursor()
                
                for exercise_row in exercises:
                    exercise_dict = dict(zip(columns, exercise_row))
                    
                    # Map to comprehensive exercise schema
                    exercise_data = {
                        'exercise_id': exercise_dict.get('id', exercise_dict.get('exercise_id', f"migrated_ex_{datetime.now().timestamp()}")),
                        'name': exercise_dict.get('name', 'Migrated Exercise'),
                        'category': exercise_dict.get('category', 'strength'),
                        'muscle_groups': json.dumps(exercise_dict.get('muscle_groups', '').split(',') if exercise_dict.get('muscle_groups') else ['unknown']),
                        'equipment': json.dumps(exercise_dict.get('equipment', '').split(',') if exercise_dict.get('equipment') else ['bodyweight']),
                        'difficulty_level': exercise_dict.get('difficulty_level', 'intermediate'),
                        'instructions': json.dumps(exercise_dict.get('instructions', '').split('\n') if exercise_dict.get('instructions') else ['No instructions available']),
                        'demo_video_url': exercise_dict.get('demo_video_url', ''),
                        'safety_notes': json.dumps(exercise_dict.get('safety_notes', '').split('\n') if exercise_dict.get('safety_notes') else []),
                        'variations': json.dumps(exercise_dict.get('variations', [])),
                        'created_at': exercise_dict.get('created_at', datetime.now().isoformat())
                    }
                    
                    comp_cursor.execute('''
                        INSERT OR REPLACE INTO exercises_enhanced 
                        (exercise_id, name, category, muscle_groups, equipment, difficulty_level,
                         instructions, demo_video_url, safety_notes, variations, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', tuple(exercise_data.values()))
                
                comp_conn.commit()
                logger.info(f"Successfully migrated {len(exercises)} exercises")
                
        except Exception as e:
            logger.error(f"Error migrating exercises: {e}")
    
    def initialize_fresh_database(self):
        """Initialize a fresh database with sample data"""
        logger.info("Initializing fresh comprehensive database with sample data")
        
        # Database is already initialized by ComprehensiveFitnessDatabase constructor
        # Add some sample data
        self.comprehensive_db.add_sample_data()
        
        logger.info("Fresh database initialized with sample data")
    
    def verify_database_integrity(self):
        """Verify database integrity and completeness"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check all tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            
            expected_tables = [
                'users_enhanced', 'exercises_enhanced', 'workout_programs', 
                'workout_sessions_enhanced', 'strength_progression', 'nutrition_plans',
                'meal_logs', 'recovery_sessions', 'wearable_data', 
                'physical_therapy_plans', 'workout_analytics'
            ]
            
            missing_tables = [table for table in expected_tables if table not in tables]
            
            if missing_tables:
                logger.warning(f"Missing tables: {missing_tables}")
                return False
            
            # Check data counts
            counts = {}
            for table in expected_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                counts[table] = cursor.fetchone()[0]
            
            logger.info(f"Database integrity check - Table counts: {counts}")
            
            return True
    
    def get_migration_status(self):
        """Get current migration status and recommendations"""
        integrity = self.verify_database_integrity()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Count users
            cursor.execute("SELECT COUNT(*) FROM users_enhanced")
            user_count = cursor.fetchone()[0]
            
            # Count workout sessions
            cursor.execute("SELECT COUNT(*) FROM workout_sessions_enhanced")
            session_count = cursor.fetchone()[0]
            
            # Count exercises
            cursor.execute("SELECT COUNT(*) FROM exercises_enhanced")
            exercise_count = cursor.fetchone()[0]
        
        return {
            "database_integrity": integrity,
            "user_count": user_count,
            "workout_sessions": session_count,
            "exercises": exercise_count,
            "database_path": self.db_path,
            "migration_complete": user_count > 0 and exercise_count > 0,
            "recommendations": self._get_recommendations(user_count, session_count, exercise_count)
        }
    
    def _get_recommendations(self, user_count, session_count, exercise_count):
        """Generate recommendations based on data status"""
        recommendations = []
        
        if user_count == 0:
            recommendations.append("No users found - consider running sample data initialization")
        
        if exercise_count < 10:
            recommendations.append("Low exercise count - consider importing more exercise data")
        
        if session_count == 0:
            recommendations.append("No workout sessions - users may need to start logging workouts")
        
        if user_count > 0 and session_count > 0:
            recommendations.append("Database has active users and sessions - system is operational")
        
        return recommendations

def run_migration():
    """Run the complete migration process"""
    migrator = DatabaseMigrator()
    
    # Run migration
    migrator.migrate_from_simple_db()
    
    # Verify integrity
    status = migrator.get_migration_status()
    
    print("🔄 Database Migration Complete!")
    print(f"📊 Status: {json.dumps(status, indent=2)}")
    
    return status

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_migration()