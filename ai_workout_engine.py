"""
AI Workout Engine - Machine Learning Powered Fitness Recommendations

This module implements advanced AI algorithms for personalized workout generation,
adaptive program modifications, and intelligent exercise selection.
"""

import numpy as np
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class WorkoutGoal(Enum):
    STRENGTH = "strength"
    HYPERTROPHY = "hypertrophy"
    ENDURANCE = "endurance"
    POWER = "power"
    WEIGHT_LOSS = "weight_loss"
    GENERAL_FITNESS = "general_fitness"

class ExperienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"
    ELITE = "elite"

@dataclass
class UserProfile:
    user_id: str
    age: int
    gender: str
    experience_level: ExperienceLevel
    primary_goals: List[WorkoutGoal]
    available_equipment: List[str]
    workout_frequency: int  # days per week
    session_duration: int   # minutes
    injury_history: List[str]
    preferences: Dict
    current_strength_levels: Dict[str, float]  # exercise -> weight
    recovery_metrics: Dict  # sleep, stress, etc.

@dataclass
class WorkoutRecommendation:
    workout_id: str
    name: str
    description: str
    estimated_duration: int
    difficulty_score: float
    exercises: List[Dict]
    periodization_phase: str
    adaptation_rationale: str
    confidence_score: float
    expected_outcomes: List[str]

class AIWorkoutEngine:
    """Advanced AI engine for personalized workout recommendations"""
    
    def __init__(self):
        self.exercise_database = self._load_exercise_database()
        self.ml_models = self._initialize_ml_models()
        self.user_profiles = {}
        self.workout_history = {}
        self.adaptation_parameters = self._initialize_adaptation_parameters()
        
    def _load_exercise_database(self) -> Dict:
        """Load comprehensive exercise database with ML features"""
        return {
            "squat": {
                "name": "Back Squat",
                "category": "compound",
                "primary_muscles": ["quadriceps", "glutes"],
                "secondary_muscles": ["hamstrings", "core"],
                "equipment": ["barbell", "squat_rack"],
                "difficulty": 7,
                "learning_curve": 8,
                "injury_risk": 6,
                "strength_correlation": 0.95,
                "hypertrophy_effectiveness": 0.88,
                "power_development": 0.82,
                "calorie_burn_rate": 12.5,
                "technical_complexity": 8,
                "alternatives": ["front_squat", "goblet_squat", "leg_press"],
                "prerequisites": [],
                "contraindications": ["knee_injury", "lower_back_injury"]
            },
            "bench_press": {
                "name": "Bench Press",
                "category": "compound", 
                "primary_muscles": ["chest", "triceps"],
                "secondary_muscles": ["shoulders"],
                "equipment": ["barbell", "bench"],
                "difficulty": 6,
                "learning_curve": 6,
                "injury_risk": 5,
                "strength_correlation": 0.92,
                "hypertrophy_effectiveness": 0.90,
                "power_development": 0.75,
                "calorie_burn_rate": 10.2,
                "technical_complexity": 6,
                "alternatives": ["dumbbell_press", "pushups", "incline_press"],
                "prerequisites": [],
                "contraindications": ["shoulder_injury"]
            },
            "deadlift": {
                "name": "Deadlift",
                "category": "compound",
                "primary_muscles": ["hamstrings", "glutes", "erector_spinae"],
                "secondary_muscles": ["lats", "traps", "rhomboids"],
                "equipment": ["barbell"],
                "difficulty": 9,
                "learning_curve": 9,
                "injury_risk": 8,
                "strength_correlation": 0.96,
                "hypertrophy_effectiveness": 0.85,
                "power_development": 0.88,
                "calorie_burn_rate": 14.8,
                "technical_complexity": 9,
                "alternatives": ["trap_bar_deadlift", "romanian_deadlift", "rack_pulls"],
                "prerequisites": ["hip_hinge_pattern"],
                "contraindications": ["lower_back_injury", "disc_issues"]
            },
            "overhead_press": {
                "name": "Overhead Press",
                "category": "compound",
                "primary_muscles": ["shoulders", "triceps"],
                "secondary_muscles": ["core", "upper_back"],
                "equipment": ["barbell"],
                "difficulty": 7,
                "learning_curve": 7,
                "injury_risk": 6,
                "strength_correlation": 0.88,
                "hypertrophy_effectiveness": 0.82,
                "power_development": 0.78,
                "calorie_burn_rate": 9.5,
                "technical_complexity": 7,
                "alternatives": ["dumbbell_press", "pike_pushups", "handstand_pushups"],
                "prerequisites": ["shoulder_mobility"],
                "contraindications": ["shoulder_impingement"]
            },
            "pull_ups": {
                "name": "Pull-ups",
                "category": "compound",
                "primary_muscles": ["lats", "rhomboids"],
                "secondary_muscles": ["biceps", "rear_delts"],
                "equipment": ["pull_up_bar"],
                "difficulty": 8,
                "learning_curve": 6,
                "injury_risk": 3,
                "strength_correlation": 0.85,
                "hypertrophy_effectiveness": 0.88,
                "power_development": 0.65,
                "calorie_burn_rate": 11.3,
                "technical_complexity": 5,
                "alternatives": ["lat_pulldown", "assisted_pullups", "inverted_rows"],
                "prerequisites": ["basic_upper_body_strength"],
                "contraindications": ["shoulder_injury", "elbow_injury"]
            }
        }
    
    def _initialize_ml_models(self) -> Dict:
        """Initialize machine learning models for workout optimization"""
        return {
            "volume_prediction": {
                "model_type": "linear_regression",
                "coefficients": {
                    "experience_multiplier": 1.2,
                    "recovery_factor": 0.8,
                    "goal_adjustment": 1.1,
                    "frequency_scaling": 0.9
                },
                "bias": 0.15,
                "accuracy": 0.87
            },
            "exercise_selection": {
                "model_type": "weighted_scoring",
                "feature_weights": {
                    "goal_alignment": 0.25,
                    "equipment_availability": 0.20,
                    "injury_safety": 0.20,
                    "experience_suitability": 0.15,
                    "preference_score": 0.10,
                    "recovery_demand": 0.10
                }
            },
            "progression_prediction": {
                "model_type": "exponential_decay",
                "parameters": {
                    "initial_adaptation_rate": 0.025,
                    "decay_constant": 0.98,
                    "minimum_progression": 0.005,
                    "plateau_threshold": 0.01
                }
            },
            "fatigue_estimation": {
                "model_type": "multi_factor",
                "factors": {
                    "volume_load": 0.35,
                    "intensity_load": 0.30,
                    "exercise_complexity": 0.20,
                    "recovery_status": 0.15
                }
            }
        }
    
    def _initialize_adaptation_parameters(self) -> Dict:
        """Initialize parameters for adaptive workout modification"""
        return {
            "beginner": {
                "volume_tolerance": 0.6,
                "intensity_cap": 0.75,
                "complexity_limit": 5,
                "progression_rate": 0.05,
                "recovery_multiplier": 1.3
            },
            "intermediate": {
                "volume_tolerance": 0.8,
                "intensity_cap": 0.90,
                "complexity_limit": 7,
                "progression_rate": 0.025,
                "recovery_multiplier": 1.0
            },
            "advanced": {
                "volume_tolerance": 1.0,
                "intensity_cap": 0.95,
                "complexity_limit": 9,
                "progression_rate": 0.015,
                "recovery_multiplier": 0.8
            },
            "elite": {
                "volume_tolerance": 1.2,
                "intensity_cap": 0.98,
                "complexity_limit": 10,
                "progression_rate": 0.01,
                "recovery_multiplier": 0.7
            }
        }

    async def generate_ai_workout(self, profile: UserProfile, context: Dict) -> WorkoutRecommendation:
        """Generate AI-powered workout recommendation"""
        
        # Analyze user's training history and current state
        performance_analysis = await self._analyze_user_performance(profile.user_id)
        fatigue_score = self._calculate_fatigue_score(profile, performance_analysis)
        adaptation_phase = self._determine_adaptation_phase(profile, performance_analysis)
        
        # ML-powered exercise selection
        selected_exercises = await self._ai_exercise_selection(
            profile, 
            fatigue_score, 
            adaptation_phase,
            context
        )
        
        # Optimize volume and intensity using ML models
        optimized_parameters = self._optimize_training_parameters(
            profile, 
            selected_exercises, 
            performance_analysis
        )
        
        # Generate workout structure
        workout = self._construct_workout(
            selected_exercises,
            optimized_parameters,
            profile,
            adaptation_phase
        )
        
        # Calculate confidence and expected outcomes
        confidence = self._calculate_recommendation_confidence(
            profile, 
            performance_analysis, 
            workout
        )
        
        expected_outcomes = self._predict_workout_outcomes(
            profile,
            workout,
            performance_analysis
        )
        
        return WorkoutRecommendation(
            workout_id=f"ai_workout_{profile.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=self._generate_workout_name(profile.primary_goals, adaptation_phase),
            description=self._generate_workout_description(workout, adaptation_phase),
            estimated_duration=optimized_parameters["estimated_duration"],
            difficulty_score=optimized_parameters["difficulty_score"],
            exercises=workout["exercises"],
            periodization_phase=adaptation_phase,
            adaptation_rationale=self._explain_adaptations(profile, performance_analysis),
            confidence_score=confidence,
            expected_outcomes=expected_outcomes
        )
    
    async def _analyze_user_performance(self, user_id: str) -> Dict:
        """Advanced ML analysis of user's performance trends"""
        
        # Get workout history (would query from database in production)
        history = self.workout_history.get(user_id, [])
        
        if not history:
            return {
                "trend": "new_user",
                "strength_velocity": 0.0,
                "volume_tolerance": 0.5,
                "consistency_score": 0.0,
                "plateau_risk": 0.0,
                "injury_risk": 0.1,
                "optimal_frequency": 3,
                "preferred_intensity": 0.7
            }
        
        # Calculate performance metrics using ML algorithms
        recent_workouts = history[-10:]  # Last 10 workouts
        
        strength_progression = self._calculate_strength_velocity(recent_workouts)
        volume_adaptation = self._analyze_volume_response(recent_workouts) 
        consistency = self._calculate_consistency_score(history)
        plateau_detection = self._detect_plateau_patterns(recent_workouts)
        injury_risk = self._assess_injury_risk(recent_workouts, user_id)
        
        return {
            "trend": self._classify_performance_trend(strength_progression),
            "strength_velocity": strength_progression,
            "volume_tolerance": volume_adaptation,
            "consistency_score": consistency,
            "plateau_risk": plateau_detection,
            "injury_risk": injury_risk,
            "optimal_frequency": self._predict_optimal_frequency(history),
            "preferred_intensity": self._analyze_intensity_preference(recent_workouts)
        }
    
    def _calculate_fatigue_score(self, profile: UserProfile, performance: Dict) -> float:
        """AI-powered fatigue estimation"""
        
        model = self.ml_models["fatigue_estimation"]
        factors = model["factors"]
        
        # Get recent training load
        recent_volume = performance.get("recent_volume_load", 1.0)
        recent_intensity = performance.get("recent_intensity_load", 0.7)
        
        # Calculate fatigue components
        volume_fatigue = min(recent_volume * factors["volume_load"], 1.0)
        intensity_fatigue = min(recent_intensity * factors["intensity_load"], 1.0)
        
        # Factor in recovery metrics
        sleep_quality = profile.recovery_metrics.get("sleep_quality", 0.7)
        stress_level = profile.recovery_metrics.get("stress_level", 0.5)
        
        recovery_factor = (sleep_quality * (1 - stress_level)) * factors["recovery_status"]
        
        # Calculate composite fatigue score
        fatigue_score = (volume_fatigue + intensity_fatigue) - recovery_factor
        
        return max(0.0, min(1.0, fatigue_score))
    
    def _determine_adaptation_phase(self, profile: UserProfile, performance: Dict) -> str:
        """Determine current training phase using ML classification"""
        
        strength_velocity = performance["strength_velocity"]
        plateau_risk = performance["plateau_risk"]
        volume_tolerance = performance["volume_tolerance"]
        
        # AI-based phase classification
        if strength_velocity > 0.02 and plateau_risk < 0.3:
            return "accumulation"  # Building volume and strength
        elif plateau_risk > 0.7 or strength_velocity < 0.005:
            return "intensification"  # Breaking through plateaus
        elif volume_tolerance < 0.6:
            return "recovery"  # Deload and adaptation
        elif strength_velocity > 0.015 and volume_tolerance > 0.8:
            return "peak"  # High performance phase
        else:
            return "development"  # General progression
    
    async def _ai_exercise_selection(self, profile: UserProfile, fatigue_score: float, 
                                   adaptation_phase: str, context: Dict) -> List[Dict]:
        """ML-powered intelligent exercise selection"""
        
        model = self.ml_models["exercise_selection"]
        weights = model["feature_weights"]
        
        # Available exercises based on equipment
        available_exercises = [
            ex for ex_id, ex in self.exercise_database.items()
            if any(eq in profile.available_equipment for eq in ex["equipment"])
        ]
        
        scored_exercises = []
        
        for exercise in available_exercises:
            # Calculate ML-based scoring
            goal_score = self._calculate_goal_alignment(exercise, profile.primary_goals)
            equipment_score = self._calculate_equipment_score(exercise, profile.available_equipment)
            safety_score = self._calculate_safety_score(exercise, profile.injury_history, fatigue_score)
            experience_score = self._calculate_experience_suitability(exercise, profile.experience_level)
            preference_score = self._calculate_preference_score(exercise, profile.preferences)
            recovery_score = self._calculate_recovery_demand_score(exercise, fatigue_score)
            
            # Weighted composite score
            composite_score = (
                goal_score * weights["goal_alignment"] +
                equipment_score * weights["equipment_availability"] +
                safety_score * weights["injury_safety"] +
                experience_score * weights["experience_suitability"] +
                preference_score * weights["preference_score"] +
                recovery_score * weights["recovery_demand"]
            )
            
            scored_exercises.append({
                "exercise": exercise,
                "score": composite_score,
                "rationale": self._generate_selection_rationale(
                    exercise, goal_score, safety_score, experience_score
                )
            })
        
        # Sort by score and select top exercises
        scored_exercises.sort(key=lambda x: x["score"], reverse=True)
        
        # Intelligent exercise combination based on adaptation phase
        selected = self._select_exercise_combination(
            scored_exercises, 
            profile, 
            adaptation_phase,
            fatigue_score
        )
        
        return selected
    
    def _optimize_training_parameters(self, profile: UserProfile, exercises: List[Dict], 
                                    performance: Dict) -> Dict:
        """ML-powered optimization of training volume, intensity, and structure"""
        
        # Get adaptation parameters for user level
        adaptation_params = self.adaptation_parameters[profile.experience_level.value]
        
        # ML model for volume prediction
        volume_model = self.ml_models["volume_prediction"]
        
        # Calculate optimal training volume
        base_volume = len(exercises) * 3  # Base sets per exercise
        
        experience_adjustment = volume_model["coefficients"]["experience_multiplier"] ** (
            {"beginner": 0.5, "intermediate": 1.0, "advanced": 1.5, "elite": 2.0}[profile.experience_level.value]
        )
        
        recovery_adjustment = volume_model["coefficients"]["recovery_factor"] * (
            1 - performance["plateau_risk"]
        )
        
        goal_adjustment = volume_model["coefficients"]["goal_adjustment"]
        if WorkoutGoal.STRENGTH in profile.primary_goals:
            goal_adjustment *= 0.9  # Lower volume for strength
        elif WorkoutGoal.HYPERTROPHY in profile.primary_goals:
            goal_adjustment *= 1.2  # Higher volume for hypertrophy
        elif WorkoutGoal.ENDURANCE in profile.primary_goals:
            goal_adjustment *= 1.4  # Higher volume for endurance
        
        optimal_volume = base_volume * experience_adjustment * recovery_adjustment * goal_adjustment
        optimal_volume = max(6, min(25, optimal_volume))  # Bounds checking
        
        # Calculate optimal intensity using progression model
        progression_model = self.ml_models["progression_prediction"]
        
        base_intensity = 0.75  # Starting intensity
        if performance["strength_velocity"] < progression_model["parameters"]["plateau_threshold"]:
            base_intensity *= 1.1  # Increase intensity if plateauing
        
        # Adjust for fatigue and recovery
        fatigue_adjustment = 1 - (performance.get("fatigue_score", 0.3) * 0.2)
        optimal_intensity = base_intensity * fatigue_adjustment
        optimal_intensity = max(0.6, min(adaptation_params["intensity_cap"], optimal_intensity))
        
        # Calculate workout duration
        exercise_time = sum([
            ex["exercise"]["technical_complexity"] * 2.5 + 8  # Base time per exercise
            for ex in exercises
        ])
        rest_time = optimal_volume * 2.5  # Rest between sets
        warm_up_time = 10
        
        total_duration = exercise_time + rest_time + warm_up_time
        target_duration = profile.session_duration
        
        if total_duration > target_duration * 1.2:
            # Adjust volume to fit time constraint
            time_adjustment = target_duration / total_duration
            optimal_volume *= time_adjustment
        
        # Calculate difficulty score
        avg_exercise_difficulty = np.mean([ex["exercise"]["difficulty"] for ex in exercises])
        volume_difficulty = min(optimal_volume / 15, 1.0)
        intensity_difficulty = optimal_intensity
        
        difficulty_score = (avg_exercise_difficulty/10 * 0.4 + 
                          volume_difficulty * 0.3 + 
                          intensity_difficulty * 0.3) * 10
        
        return {
            "optimal_volume": int(optimal_volume),
            "optimal_intensity": optimal_intensity,
            "estimated_duration": int(min(total_duration, target_duration)),
            "difficulty_score": difficulty_score,
            "volume_rationale": f"Optimized for {profile.experience_level.value} level with {performance['consistency_score']:.1%} consistency",
            "intensity_rationale": f"Adjusted for current strength velocity ({performance['strength_velocity']:.1%}/week)"
        }

    def _construct_workout(self, exercises: List[Dict], parameters: Dict, 
                         profile: UserProfile, phase: str) -> Dict:
        """Construct the final workout structure with AI optimization"""
        
        workout_exercises = []
        total_sets = parameters["optimal_volume"]
        intensity = parameters["optimal_intensity"]
        
        # Distribute sets across exercises based on importance and type
        for i, ex_data in enumerate(exercises):
            exercise = ex_data["exercise"]
            
            # Calculate sets for this exercise
            if exercise["category"] == "compound":
                base_sets = max(3, int(total_sets * 0.4 / len([e for e in exercises if e["exercise"]["category"] == "compound"])))
            else:
                base_sets = max(2, int(total_sets * 0.6 / len([e for e in exercises if e["exercise"]["category"] != "compound"])))
            
            # Adjust reps based on primary goal and exercise type
            if WorkoutGoal.STRENGTH in profile.primary_goals:
                rep_range = [3, 5] if exercise["category"] == "compound" else [6, 8]
            elif WorkoutGoal.HYPERTROPHY in profile.primary_goals:
                rep_range = [6, 10] if exercise["category"] == "compound" else [8, 15]
            elif WorkoutGoal.ENDURANCE in profile.primary_goals:
                rep_range = [12, 20]
            else:  # General fitness
                rep_range = [8, 12]
            
            # Calculate weight based on user's strength levels and intensity
            current_max = profile.current_strength_levels.get(exercise["name"].lower().replace(" ", "_"), 100)
            working_weight = current_max * intensity
            
            # Generate set-by-set prescription
            sets_prescription = []
            for set_num in range(base_sets):
                # Vary intensity across sets (pyramid, reverse pyramid, or straight sets)
                if phase == "intensification":
                    # Reverse pyramid for strength focus
                    set_intensity = intensity - (set_num * 0.05)
                    set_reps = rep_range[0] + set_num
                elif phase == "accumulation":
                    # Straight sets for volume
                    set_intensity = intensity
                    set_reps = rep_range[1]
                else:
                    # Pyramid for general development
                    set_intensity = intensity + (0.05 if set_num < base_sets // 2 else -0.05)
                    set_reps = rep_range[0] + (set_num % (rep_range[1] - rep_range[0] + 1))
                
                sets_prescription.append({
                    "set_number": set_num + 1,
                    "reps": max(rep_range[0], min(rep_range[1], set_reps)),
                    "weight": round(working_weight * set_intensity, 2),
                    "rpe_target": min(10, 6 + set_intensity * 4),  # RPE 6-10 scale
                    "rest_seconds": self._calculate_optimal_rest(exercise, set_intensity, profile.primary_goals)
                })
            
            workout_exercises.append({
                "exercise_name": exercise["name"],
                "exercise_id": list(self.exercise_database.keys())[list(self.exercise_database.values()).index(exercise)],
                "sets": base_sets,
                "sets_prescription": sets_prescription,
                "primary_muscles": exercise["primary_muscles"],
                "equipment": exercise["equipment"],
                "technique_focus": self._generate_technique_focus(exercise, profile.experience_level),
                "form_cues": self._generate_form_cues(exercise),
                "ai_rationale": ex_data["rationale"],
                "progression_strategy": self._generate_progression_strategy(exercise, profile, phase)
            })
        
        return {
            "exercises": workout_exercises,
            "warm_up": self._generate_ai_warmup(exercises, profile),
            "cool_down": self._generate_ai_cooldown(exercises, profile),
            "periodization_notes": self._generate_periodization_notes(phase, profile),
            "adaptation_focus": self._get_adaptation_focus(phase),
            "ai_insights": self._generate_ai_insights(exercises, parameters, profile)
        }

    def _calculate_recommendation_confidence(self, profile: UserProfile, 
                                          performance: Dict, workout: Dict) -> float:
        """Calculate AI confidence in the recommendation"""
        
        # Factors affecting confidence
        data_quality = min(1.0, len(self.workout_history.get(profile.user_id, [])) / 10)  # More history = higher confidence
        goal_clarity = len(profile.primary_goals) / 3  # Clearer goals = higher confidence
        equipment_match = 1.0  # Assume perfect equipment match for now
        experience_alignment = 0.9  # High confidence in experience-based recommendations
        
        # Penalty for high injury risk or fatigue
        safety_confidence = 1 - (performance.get("injury_risk", 0.1) * 0.5)
        fatigue_confidence = 1 - (performance.get("fatigue_score", 0.3) * 0.3)
        
        # Composite confidence score
        confidence = (
            data_quality * 0.25 +
            goal_clarity * 0.20 +
            equipment_match * 0.15 +
            experience_alignment * 0.20 +
            safety_confidence * 0.10 +
            fatigue_confidence * 0.10
        )
        
        return max(0.3, min(1.0, confidence))  # Bound between 30% and 100%

    def _predict_workout_outcomes(self, profile: UserProfile, workout: Dict, 
                                performance: Dict) -> List[str]:
        """AI-powered prediction of workout outcomes"""
        
        outcomes = []
        
        # Strength outcomes
        if WorkoutGoal.STRENGTH in profile.primary_goals:
            strength_gain = performance["strength_velocity"] * 4  # Weekly to monthly
            outcomes.append(f"Expected strength gain: {strength_gain:.1%} over 4 weeks")
        
        # Hypertrophy outcomes
        if WorkoutGoal.HYPERTROPHY in profile.primary_goals:
            volume_factor = sum([ex["sets"] for ex in workout["exercises"]]) / 20
            outcomes.append(f"Muscle growth stimulus: {min(100, volume_factor * 85):.0f}% optimal")
        
        # Calorie burn prediction
        total_calorie_burn = sum([
            ex["exercise"]["calorie_burn_rate"] * ex["sets"] * 3  # Approx 3 min per set
            for ex in workout["exercises"]
        ])
        outcomes.append(f"Estimated calorie burn: {total_calorie_burn:.0f} calories")
        
        # Fatigue prediction
        fatigue_accumulation = sum([
            ex["exercise"]["difficulty"] * ex["sets"] / 100
            for ex in workout["exercises"]
        ])
        recovery_time = max(24, fatigue_accumulation * 12)
        outcomes.append(f"Estimated recovery time: {recovery_time:.0f} hours")
        
        # Performance prediction
        if performance["consistency_score"] > 0.8:
            outcomes.append("High probability of performance improvement with consistent execution")
        
        return outcomes

    # Helper methods for ML calculations
    def _calculate_goal_alignment(self, exercise: Dict, goals: List[WorkoutGoal]) -> float:
        """Calculate how well exercise aligns with user goals"""
        alignment_scores = {
            WorkoutGoal.STRENGTH: exercise["strength_correlation"],
            WorkoutGoal.HYPERTROPHY: exercise["hypertrophy_effectiveness"],  
            WorkoutGoal.POWER: exercise["power_development"],
            WorkoutGoal.ENDURANCE: 1 - exercise["strength_correlation"],  # Inverse relationship
            WorkoutGoal.WEIGHT_LOSS: exercise["calorie_burn_rate"] / 15,
            WorkoutGoal.GENERAL_FITNESS: (exercise["strength_correlation"] + exercise["hypertrophy_effectiveness"]) / 2
        }
        
        if not goals:
            return 0.5
            
        return np.mean([alignment_scores.get(goal, 0.5) for goal in goals])
    
    def _calculate_equipment_score(self, exercise: Dict, available_equipment: List[str]) -> float:
        """Calculate equipment availability score"""
        required_equipment = exercise["equipment"]
        available_count = sum([1 for eq in required_equipment if eq in available_equipment])
        return available_count / len(required_equipment) if required_equipment else 1.0
    
    def _calculate_safety_score(self, exercise: Dict, injury_history: List[str], fatigue: float) -> float:
        """Calculate safety score based on injury risk and contraindications"""
        base_safety = 1 - (exercise["injury_risk"] / 10)
        
        # Penalize exercises with contraindications
        contraindication_penalty = 0
        for contraindication in exercise["contraindications"]:
            if contraindication in injury_history:
                contraindication_penalty += 0.3
        
        # Reduce safety score when fatigued
        fatigue_penalty = fatigue * 0.2
        
        return max(0.1, base_safety - contraindication_penalty - fatigue_penalty)
    
    def _calculate_experience_suitability(self, exercise: Dict, experience: ExperienceLevel) -> float:
        """Calculate how suitable exercise is for experience level"""
        experience_values = {
            ExperienceLevel.BEGINNER: 2,
            ExperienceLevel.INTERMEDIATE: 5,  
            ExperienceLevel.ADVANCED: 8,
            ExperienceLevel.ELITE: 10
        }
        
        user_level = experience_values[experience]
        exercise_difficulty = exercise["technical_complexity"]
        
        # Optimal when exercise difficulty matches user level ±2
        difference = abs(user_level - exercise_difficulty)
        if difference <= 2:
            return 1.0
        elif difference <= 4:
            return 0.7
        else:
            return 0.3

    def _generate_workout_name(self, goals: List[WorkoutGoal], phase: str) -> str:
        """Generate descriptive workout name"""
        goal_names = {
            WorkoutGoal.STRENGTH: "Strength",
            WorkoutGoal.HYPERTROPHY: "Hypertrophy", 
            WorkoutGoal.POWER: "Power",
            WorkoutGoal.ENDURANCE: "Endurance",
            WorkoutGoal.WEIGHT_LOSS: "Fat Loss",
            WorkoutGoal.GENERAL_FITNESS: "Fitness"
        }
        
        primary_goal = goals[0] if goals else WorkoutGoal.GENERAL_FITNESS
        goal_name = goal_names[primary_goal]
        
        phase_names = {
            "accumulation": "Volume",
            "intensification": "Intensity", 
            "recovery": "Recovery",
            "peak": "Peak",
            "development": "Development"
        }
        
        return f"AI {goal_name} - {phase_names.get(phase, 'Custom')} Phase"

    def _generate_workout_description(self, workout: Dict, phase: str) -> str:
        """Generate AI workout description"""
        exercise_count = len(workout["exercises"])
        compound_count = sum(1 for ex in workout["exercises"] if ex["exercise"]["category"] == "compound")
        
        description = f"AI-optimized workout featuring {exercise_count} exercises "
        description += f"({compound_count} compound movements) "
        description += f"designed for {phase} phase training. "
        description += "Personalized based on your performance data, goals, and recovery status."
        
        return description

    # Additional helper methods would continue here...
    def _explain_adaptations(self, profile: UserProfile, performance: Dict) -> str:
        """Explain why specific adaptations were made"""
        reasons = []
        
        if performance["plateau_risk"] > 0.6:
            reasons.append("Increased intensity to break through performance plateau")
        
        if performance["fatigue_score"] > 0.7:
            reasons.append("Reduced volume to accommodate high fatigue levels")
            
        if performance["consistency_score"] < 0.5:
            reasons.append("Simplified exercise selection to improve adherence")
            
        if not reasons:
            reasons.append("Optimized for continued progressive development")
            
        return "; ".join(reasons)

# Additional utility functions and ML algorithms would continue...