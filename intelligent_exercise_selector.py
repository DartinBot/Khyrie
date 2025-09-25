"""
Intelligent Exercise Selection & Predictive Analytics System

Advanced ML models for smart exercise substitution, injury risk prediction,
and optimal training load recommendations.
"""

import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from ai_workout_engine import WorkoutGoal, ExperienceLevel, UserProfile
from adaptive_program_engine import PerformanceMetrics, AdaptationRecommendation

@dataclass
class InjuryRiskProfile:
    user_id: str
    overall_risk_score: float
    joint_specific_risks: Dict[str, float]
    movement_pattern_risks: Dict[str, float]
    load_tolerance: Dict[str, float]
    recovery_capacity: float
    injury_history_impact: Dict[str, float]

@dataclass
class ExerciseSubstitution:
    original_exercise: str
    recommended_substitute: str
    substitution_reason: str
    effectiveness_retention: float  # How well substitute matches original
    difficulty_adjustment: float
    safety_improvement: float
    equipment_requirements: List[str]

@dataclass
class TrainingLoadRecommendation:
    recommended_intensity: float
    recommended_volume: int
    load_distribution: Dict[str, float]  # per exercise category
    progression_strategy: str
    deload_timing: Dict[str, Any]
    risk_mitigation: List[str]

class IntelligentExerciseSelector:
    """AI system for smart exercise selection and substitution"""
    
    def __init__(self):
        self.exercise_database = self._load_comprehensive_exercise_database()
        self.movement_patterns = self._define_movement_patterns()
        self.substitution_rules = self._initialize_substitution_rules()
        self.injury_models = self._initialize_injury_prediction_models()
        self.load_optimization_models = self._initialize_load_models()
        
    def _load_comprehensive_exercise_database(self) -> Dict:
        """Expanded exercise database with ML features"""
        return {
            # COMPOUND MOVEMENTS
            "back_squat": {
                "name": "Back Squat",
                "category": "compound",
                "movement_pattern": "squat",
                "primary_muscles": ["quadriceps", "glutes"],
                "secondary_muscles": ["hamstrings", "core", "calves"],
                "equipment": ["barbell", "squat_rack"],
                "difficulty": 8,
                "learning_curve": 8,
                "injury_risk": {"knee": 0.3, "lower_back": 0.4, "ankle": 0.2},
                "joint_loading": {"knee": 0.8, "hip": 0.9, "ankle": 0.6, "spine": 0.7},
                "strength_correlation": 0.95,
                "hypertrophy_effectiveness": 0.88,
                "power_development": 0.82,
                "calorie_burn_rate": 12.5,
                "technical_complexity": 8,
                "fatigue_factor": 0.9,  # How fatiguing the exercise is
                "recovery_demand": 0.8,
                "neural_demand": 0.9,
                "alternatives": ["front_squat", "goblet_squat", "leg_press", "hack_squat"],
                "prerequisites": ["ankle_mobility", "hip_mobility", "thoracic_spine_mobility"],
                "contraindications": ["acute_knee_injury", "lower_back_injury"],
                "progression_variants": ["box_squat", "pause_squat", "tempo_squat"],
                "regression_variants": ["goblet_squat", "bodyweight_squat", "assisted_squat"]
            },
            
            "front_squat": {
                "name": "Front Squat",
                "category": "compound", 
                "movement_pattern": "squat",
                "primary_muscles": ["quadriceps", "core"],
                "secondary_muscles": ["glutes", "upper_back"],
                "equipment": ["barbell", "squat_rack"],
                "difficulty": 9,
                "learning_curve": 9,
                "injury_risk": {"knee": 0.25, "lower_back": 0.2, "wrist": 0.3},
                "joint_loading": {"knee": 0.9, "hip": 0.7, "ankle": 0.7, "spine": 0.5},
                "strength_correlation": 0.88,
                "hypertrophy_effectiveness": 0.85,
                "power_development": 0.80,
                "calorie_burn_rate": 11.8,
                "technical_complexity": 9,
                "fatigue_factor": 0.85,
                "recovery_demand": 0.75,
                "neural_demand": 0.95,
                "alternatives": ["back_squat", "goblet_squat", "zercher_squat"],
                "prerequisites": ["wrist_mobility", "thoracic_spine_mobility", "ankle_mobility"],
                "contraindications": ["wrist_injury", "shoulder_injury"],
                "progression_variants": ["pause_front_squat", "front_squat_to_press"],
                "regression_variants": ["goblet_squat", "front_loaded_goblet_squat"]
            },
            
            "deadlift": {
                "name": "Conventional Deadlift",
                "category": "compound",
                "movement_pattern": "hinge",
                "primary_muscles": ["hamstrings", "glutes", "erector_spinae"],
                "secondary_muscles": ["lats", "traps", "rhomboids", "core"],
                "equipment": ["barbell", "plates"],
                "difficulty": 9,
                "learning_curve": 9,
                "injury_risk": {"lower_back": 0.5, "hamstring": 0.3, "knee": 0.2},
                "joint_loading": {"hip": 0.95, "knee": 0.4, "spine": 0.8},
                "strength_correlation": 0.96,
                "hypertrophy_effectiveness": 0.85,
                "power_development": 0.88,
                "calorie_burn_rate": 14.8,
                "technical_complexity": 9,
                "fatigue_factor": 0.95,
                "recovery_demand": 0.9,
                "neural_demand": 0.95,
                "alternatives": ["sumo_deadlift", "trap_bar_deadlift", "romanian_deadlift"],
                "prerequisites": ["hip_hinge_pattern", "hamstring_flexibility"],
                "contraindications": ["acute_lower_back_injury", "disc_herniation"],
                "progression_variants": ["deficit_deadlift", "pause_deadlift"],
                "regression_variants": ["rack_pulls", "kettlebell_deadlift", "romanian_deadlift"]
            },
            
            # ISOLATION EXERCISES
            "leg_curl": {
                "name": "Leg Curl",
                "category": "isolation",
                "movement_pattern": "knee_flexion",
                "primary_muscles": ["hamstrings"],
                "secondary_muscles": [],
                "equipment": ["leg_curl_machine"],
                "difficulty": 3,
                "learning_curve": 2,
                "injury_risk": {"hamstring": 0.15, "knee": 0.1},
                "joint_loading": {"knee": 0.3, "hip": 0.2},
                "strength_correlation": 0.6,
                "hypertrophy_effectiveness": 0.8,
                "power_development": 0.3,
                "calorie_burn_rate": 6.2,
                "technical_complexity": 2,
                "fatigue_factor": 0.4,
                "recovery_demand": 0.3,
                "neural_demand": 0.2,
                "alternatives": ["nordic_curls", "good_mornings", "romanian_deadlifts"],
                "prerequisites": [],
                "contraindications": ["acute_hamstring_strain"],
                "progression_variants": ["single_leg_curl", "eccentric_leg_curl"],
                "regression_variants": ["assisted_leg_curl", "resistance_band_curl"]
            },
            
            # BODYWEIGHT EXERCISES
            "push_ups": {
                "name": "Push-ups",
                "category": "compound",
                "movement_pattern": "horizontal_push",
                "primary_muscles": ["chest", "triceps"],
                "secondary_muscles": ["shoulders", "core"],
                "equipment": [],
                "difficulty": 4,
                "learning_curve": 3,
                "injury_risk": {"shoulder": 0.2, "wrist": 0.25, "elbow": 0.15},
                "joint_loading": {"shoulder": 0.5, "elbow": 0.4, "wrist": 0.6},
                "strength_correlation": 0.7,
                "hypertrophy_effectiveness": 0.75,
                "power_development": 0.6,
                "calorie_burn_rate": 8.5,
                "technical_complexity": 3,
                "fatigue_factor": 0.5,
                "recovery_demand": 0.4,
                "neural_demand": 0.3,
                "alternatives": ["bench_press", "dumbbell_press", "dips"],
                "prerequisites": ["basic_upper_body_strength"],
                "contraindications": ["wrist_injury", "shoulder_impingement"],
                "progression_variants": ["diamond_pushups", "archer_pushups", "one_arm_pushups"],
                "regression_variants": ["incline_pushups", "knee_pushups", "wall_pushups"]
            }
        }
    
    def _define_movement_patterns(self) -> Dict:
        """Define movement patterns for intelligent substitution"""
        return {
            "squat": {
                "primary_joints": ["hip", "knee", "ankle"],
                "movement_plane": "sagittal",
                "muscle_emphasis": "quad_dominant",
                "exercises": ["back_squat", "front_squat", "goblet_squat", "leg_press"]
            },
            "hinge": {
                "primary_joints": ["hip", "knee"],
                "movement_plane": "sagittal", 
                "muscle_emphasis": "hip_dominant",
                "exercises": ["deadlift", "romanian_deadlift", "good_morning", "hip_thrust"]
            },
            "vertical_push": {
                "primary_joints": ["shoulder", "elbow"],
                "movement_plane": "frontal",
                "muscle_emphasis": "shoulder_dominant",
                "exercises": ["overhead_press", "handstand_pushup", "dumbbell_press"]
            },
            "vertical_pull": {
                "primary_joints": ["shoulder", "elbow"],
                "movement_plane": "frontal",
                "muscle_emphasis": "lat_dominant",
                "exercises": ["pull_ups", "chin_ups", "lat_pulldown"]
            },
            "horizontal_push": {
                "primary_joints": ["shoulder", "elbow"],
                "movement_plane": "transverse",
                "muscle_emphasis": "chest_dominant", 
                "exercises": ["bench_press", "push_ups", "dumbbell_press"]
            },
            "horizontal_pull": {
                "primary_joints": ["shoulder", "elbow"],
                "movement_plane": "transverse",
                "muscle_emphasis": "rhomboid_dominant",
                "exercises": ["rows", "face_pulls", "reverse_fly"]
            }
        }
    
    def _initialize_substitution_rules(self) -> Dict:
        """Initialize ML rules for exercise substitution"""
        return {
            "injury_based": {
                "knee_injury": {
                    "avoid_patterns": ["squat", "lunge"],
                    "safe_alternatives": ["leg_press", "leg_extension", "wall_sit"],
                    "modification_strategies": ["reduce_range_of_motion", "unload_joint", "isometric_holds"]
                },
                "lower_back_injury": {
                    "avoid_patterns": ["hinge", "spinal_loading"],
                    "safe_alternatives": ["machine_exercises", "supported_movements"],
                    "modification_strategies": ["neutral_spine", "external_support", "reduced_loading"]
                },
                "shoulder_injury": {
                    "avoid_patterns": ["overhead", "behind_neck"],
                    "safe_alternatives": ["neutral_grip", "supported_press"],
                    "modification_strategies": ["limited_range_of_motion", "neutral_positions"]
                }
            },
            "equipment_based": {
                "no_barbell": {
                    "substitutions": {
                        "back_squat": "goblet_squat",
                        "bench_press": "push_ups",
                        "deadlift": "kettlebell_deadlift",
                        "overhead_press": "dumbbell_press"
                    }
                },
                "home_gym": {
                    "substitutions": {
                        "leg_press": "goblet_squat",
                        "lat_pulldown": "pull_ups",
                        "leg_curl": "single_leg_deadlift"
                    }
                }
            },
            "progression_based": {
                "beginner_modifications": {
                    "back_squat": "bodyweight_squat",
                    "pull_ups": "assisted_pull_ups",
                    "deadlift": "kettlebell_deadlift"
                },
                "advanced_progressions": {
                    "push_ups": "handstand_pushups",
                    "squat": "pistol_squat",
                    "pull_ups": "weighted_pull_ups"
                }
            }
        }
    
    def _initialize_injury_prediction_models(self) -> Dict:
        """Initialize ML models for injury risk prediction"""
        return {
            "acute_injury_model": {
                "model_type": "logistic_regression",
                "features": {
                    "load_spike": {"weight": 0.3, "threshold": 1.5},  # >50% load increase
                    "fatigue_accumulation": {"weight": 0.25, "threshold": 0.8},
                    "movement_quality": {"weight": 0.2, "threshold": 0.6}, 
                    "recovery_deficit": {"weight": 0.15, "threshold": 0.4},
                    "previous_injury": {"weight": 0.1, "multiplier": 2.0}
                },
                "baseline_risk": 0.05  # 5% baseline injury risk
            },
            "overuse_injury_model": {
                "model_type": "cumulative_load_model",
                "parameters": {
                    "tissue_tolerance": 1.0,
                    "adaptation_rate": 0.1,  # per week
                    "fatigue_decay": 0.9,    # per day
                    "damage_threshold": 1.2,
                    "chronic_load_window": 28  # days
                }
            },
            "joint_specific_models": {
                "knee": {
                    "risk_factors": ["squat_volume", "running_volume", "quad_strength_imbalance"],
                    "protection_factors": ["hamstring_strength", "ankle_mobility"]
                },
                "lower_back": {
                    "risk_factors": ["deadlift_volume", "sitting_time", "hip_flexor_tightness"],
                    "protection_factors": ["core_strength", "hip_mobility"]
                },
                "shoulder": {
                    "risk_factors": ["overhead_volume", "internal_rotation_deficit"],
                    "protection_factors": ["external_rotator_strength", "thoracic_mobility"]
                }
            }
        }
    
    def _initialize_load_models(self) -> Dict:
        """Initialize models for optimal load recommendations"""
        return {
            "periodization_model": {
                "model_type": "optimal_control",
                "parameters": {
                    "adaptation_time_constant": 14,  # days
                    "fatigue_time_constant": 7,     # days
                    "performance_decay": 0.02,      # per day without training
                    "supercompensation_window": 3   # days
                }
            },
            "individual_response_model": {
                "model_type": "bayesian_updating",
                "priors": {
                    "volume_response": {"mean": 0.02, "std": 0.01},
                    "intensity_response": {"mean": 0.015, "std": 0.008},
                    "recovery_rate": {"mean": 0.8, "std": 0.2}
                }
            }
        }

    async def predict_injury_risk(self, user_profile: UserProfile, 
                                planned_workout: Dict, 
                                recent_training_history: List[Dict]) -> InjuryRiskProfile:
        """Advanced ML-based injury risk prediction"""
        
        # Calculate acute injury risk
        acute_risk = await self._calculate_acute_injury_risk(
            user_profile, planned_workout, recent_training_history
        )
        
        # Calculate overuse injury risk
        overuse_risk = await self._calculate_overuse_injury_risk(
            user_profile, recent_training_history
        )
        
        # Calculate joint-specific risks
        joint_risks = await self._calculate_joint_specific_risks(
            user_profile, planned_workout, recent_training_history
        )
        
        # Calculate movement pattern risks
        pattern_risks = await self._calculate_movement_pattern_risks(
            planned_workout, recent_training_history
        )
        
        # Calculate load tolerance
        load_tolerance = await self._calculate_load_tolerance(
            user_profile, recent_training_history
        )
        
        # Overall risk integration
        overall_risk = self._integrate_risk_factors(
            acute_risk, overuse_risk, joint_risks, pattern_risks
        )
        
        return InjuryRiskProfile(
            user_id=user_profile.user_id,
            overall_risk_score=overall_risk,
            joint_specific_risks=joint_risks,
            movement_pattern_risks=pattern_risks,
            load_tolerance=load_tolerance,
            recovery_capacity=user_profile.recovery_metrics.get("recovery_score", 0.7),
            injury_history_impact=self._calculate_injury_history_impact(user_profile.injury_history)
        )

    async def generate_smart_substitutions(self, original_exercise: str, 
                                         user_profile: UserProfile,
                                         injury_risk: InjuryRiskProfile,
                                         available_equipment: List[str]) -> List[ExerciseSubstitution]:
        """Generate intelligent exercise substitutions"""
        
        if original_exercise not in self.exercise_database:
            return []
        
        original = self.exercise_database[original_exercise]
        substitutions = []
        
        # Get movement pattern for original exercise
        movement_pattern = original["movement_pattern"]
        pattern_info = self.movement_patterns.get(movement_pattern, {})
        
        # Find exercises in same movement pattern
        pattern_exercises = pattern_info.get("exercises", [])
        
        for candidate_id in pattern_exercises:
            if candidate_id == original_exercise:
                continue
                
            if candidate_id not in self.exercise_database:
                continue
                
            candidate = self.exercise_database[candidate_id]
            
            # Check equipment availability
            if not self._check_equipment_availability(candidate["equipment"], available_equipment):
                continue
            
            # Calculate substitution quality
            effectiveness_retention = self._calculate_effectiveness_retention(original, candidate)
            safety_improvement = self._calculate_safety_improvement(
                original, candidate, injury_risk, user_profile
            )
            difficulty_adjustment = self._calculate_difficulty_adjustment(
                original, candidate, user_profile.experience_level
            )
            
            # Determine substitution reason
            reason = self._determine_substitution_reason(
                original, candidate, injury_risk, user_profile
            )
            
            # Only include if it's a meaningful substitution
            if effectiveness_retention > 0.6 or safety_improvement > 0.2:
                substitutions.append(ExerciseSubstitution(
                    original_exercise=original_exercise,
                    recommended_substitute=candidate_id,
                    substitution_reason=reason,
                    effectiveness_retention=effectiveness_retention,
                    difficulty_adjustment=difficulty_adjustment,
                    safety_improvement=safety_improvement,
                    equipment_requirements=candidate["equipment"]
                ))
        
        # Sort by overall quality score
        substitutions.sort(
            key=lambda x: x.effectiveness_retention + x.safety_improvement,
            reverse=True
        )
        
        return substitutions[:3]  # Return top 3 substitutions

    async def optimize_training_load(self, user_profile: UserProfile,
                                   performance_history: List[PerformanceMetrics],
                                   injury_risk: InjuryRiskProfile) -> TrainingLoadRecommendation:
        """ML-powered training load optimization"""
        
        # Analyze individual response patterns
        individual_response = await self._analyze_individual_response(
            user_profile.user_id, performance_history
        )
        
        # Calculate optimal intensity
        optimal_intensity = await self._calculate_optimal_intensity(
            user_profile, individual_response, injury_risk
        )
        
        # Calculate optimal volume
        optimal_volume = await self._calculate_optimal_volume(
            user_profile, individual_response, injury_risk
        )
        
        # Determine load distribution across exercise categories
        load_distribution = await self._optimize_load_distribution(
            user_profile, injury_risk, optimal_volume
        )
        
        # Generate progression strategy
        progression_strategy = await self._generate_progression_strategy(
            user_profile, individual_response, performance_history
        )
        
        # Plan deload timing
        deload_timing = await self._plan_deload_timing(
            performance_history, individual_response
        )
        
        # Generate risk mitigation strategies
        risk_mitigation = await self._generate_risk_mitigation(
            injury_risk, user_profile
        )
        
        return TrainingLoadRecommendation(
            recommended_intensity=optimal_intensity,
            recommended_volume=optimal_volume,
            load_distribution=load_distribution,
            progression_strategy=progression_strategy,
            deload_timing=deload_timing,
            risk_mitigation=risk_mitigation
        )

    # Helper methods for ML calculations
    async def _calculate_acute_injury_risk(self, user_profile: UserProfile,
                                         planned_workout: Dict,
                                         history: List[Dict]) -> float:
        """Calculate risk of acute injury from planned workout"""
        
        model = self.injury_models["acute_injury_model"]
        features = model["features"]
        baseline_risk = model["baseline_risk"]
        
        risk_score = baseline_risk
        
        # Calculate load spike
        if len(history) >= 2:
            current_load = sum([ex.get("volume", 0) * ex.get("intensity", 0.7) 
                               for ex in planned_workout.get("exercises", [])])
            avg_recent_load = np.mean([
                sum([ex.get("volume", 0) * ex.get("intensity", 0.7) 
                     for ex in workout.get("exercises", [])])
                for workout in history[-4:]
            ])
            
            load_spike = current_load / avg_recent_load if avg_recent_load > 0 else 1.0
            
            if load_spike > features["load_spike"]["threshold"]:
                risk_score += (load_spike - 1.0) * features["load_spike"]["weight"]
        
        # Factor in fatigue accumulation
        fatigue_level = 1 - user_profile.recovery_metrics.get("recovery_score", 0.7)
        if fatigue_level > features["fatigue_accumulation"]["threshold"]:
            risk_score += fatigue_level * features["fatigue_accumulation"]["weight"]
        
        # Factor in previous injuries
        if user_profile.injury_history:
            risk_score *= features["previous_injury"]["multiplier"]
        
        return min(1.0, risk_score)

    async def _calculate_overuse_injury_risk(self, user_profile: UserProfile,
                                           history: List[Dict]) -> float:
        """Calculate cumulative overuse injury risk"""
        
        model = self.injury_models["overuse_injury_model"]
        params = model["parameters"]
        
        if len(history) < 4:
            return 0.1  # Low risk with insufficient data
        
        # Calculate chronic workload
        chronic_loads = []
        for i in range(len(history)):
            workout = history[i]
            load = sum([ex.get("volume", 0) * ex.get("intensity", 0.7) 
                       for ex in workout.get("exercises", [])])
            chronic_loads.append(load)
        
        # Calculate tissue adaptation vs. damage accumulation
        chronic_load = np.mean(chronic_loads[-4:])  # 4-week average
        acute_load = np.mean(chronic_loads[-1:])    # Current week
        
        # Acute:Chronic load ratio
        ac_ratio = acute_load / chronic_load if chronic_load > 0 else 1.0
        
        # Risk increases with high AC ratios
        if ac_ratio > 1.3:
            overuse_risk = (ac_ratio - 1.0) * 0.5
        else:
            overuse_risk = 0.05  # Baseline low risk
        
        return min(1.0, overuse_risk)

    def _calculate_effectiveness_retention(self, original: Dict, candidate: Dict) -> float:
        """Calculate how well substitute retains training effectiveness"""
        
        # Compare muscle activation patterns
        muscle_overlap = len(set(original["primary_muscles"]) & 
                           set(candidate["primary_muscles"])) / len(original["primary_muscles"])
        
        # Compare training qualities
        strength_retention = min(candidate["strength_correlation"], 
                               original["strength_correlation"]) / original["strength_correlation"]
        
        hypertrophy_retention = min(candidate["hypertrophy_effectiveness"],
                                  original["hypertrophy_effectiveness"]) / original["hypertrophy_effectiveness"]
        
        # Weighted average based on training goals
        effectiveness = (
            muscle_overlap * 0.4 +
            strength_retention * 0.3 +
            hypertrophy_retention * 0.3
        )
        
        return effectiveness

    def _calculate_safety_improvement(self, original: Dict, candidate: Dict,
                                    injury_risk: InjuryRiskProfile,
                                    user_profile: UserProfile) -> float:
        """Calculate safety improvement from substitution"""
        
        # Compare injury risks
        original_risk = sum(original["injury_risk"].values()) / len(original["injury_risk"])
        candidate_risk = sum(candidate["injury_risk"].values()) / len(candidate["injury_risk"])
        
        base_safety_improvement = max(0, original_risk - candidate_risk)
        
        # Factor in user's specific injury history
        safety_bonus = 0
        for injury in user_profile.injury_history:
            if injury in original["contraindications"] and injury not in candidate["contraindications"]:
                safety_bonus += 0.3
        
        return base_safety_improvement + safety_bonus

    def _determine_substitution_reason(self, original: Dict, candidate: Dict,
                                     injury_risk: InjuryRiskProfile,
                                     user_profile: UserProfile) -> str:
        """Determine why substitution is recommended"""
        
        reasons = []
        
        # Safety reasons
        for injury in user_profile.injury_history:
            if injury in original["contraindications"]:
                reasons.append(f"Safer for {injury}")
        
        # Difficulty reasons
        if candidate["difficulty"] < original["difficulty"] - 2:
            reasons.append("Reduced complexity for skill development")
        elif candidate["difficulty"] > original["difficulty"] + 2:
            reasons.append("Increased challenge for progression")
        
        # Equipment reasons
        if len(candidate["equipment"]) < len(original["equipment"]):
            reasons.append("Requires less equipment")
        
        # Recovery reasons  
        if candidate["recovery_demand"] < original["recovery_demand"]:
            reasons.append("Lower recovery demand")
        
        return "; ".join(reasons) if reasons else "Movement pattern alternative"

    async def _analyze_individual_response(self, user_id: str,
                                         history: List[PerformanceMetrics]) -> Dict:
        """Analyze individual's response patterns to training"""
        
        if len(history) < 6:
            return {
                "volume_response_rate": 0.02,    # Default response rates
                "intensity_response_rate": 0.015,
                "recovery_rate": 0.8,
                "adaptation_speed": "average"
            }
        
        # Analyze volume-response relationship
        volumes = [m.volume_tolerance for m in history[-6:]]
        progressions = [m.progression_rate for m in history[-6:]]
        
        # Simple linear regression for volume response
        volume_response = np.corrcoef(volumes, progressions)[0, 1] if len(volumes) > 1 else 0.02
        
        # Analyze recovery patterns
        recovery_scores = [m.recovery_score for m in history[-6:]]
        recovery_rate = np.mean(recovery_scores)
        
        # Classify adaptation speed
        avg_progression = np.mean(progressions)
        if avg_progression > 0.025:
            adaptation_speed = "fast"
        elif avg_progression < 0.01:
            adaptation_speed = "slow" 
        else:
            adaptation_speed = "average"
        
        return {
            "volume_response_rate": max(0, volume_response),
            "intensity_response_rate": avg_progression,
            "recovery_rate": recovery_rate,
            "adaptation_speed": adaptation_speed
        }

    # Additional helper methods would continue here...