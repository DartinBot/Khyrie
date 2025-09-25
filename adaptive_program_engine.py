"""
Adaptive Program Modification System

Advanced ML models for automatic program adjustments based on performance trends,
recovery data, and progress patterns.
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from ai_workout_engine import WorkoutGoal, ExperienceLevel, UserProfile, AIWorkoutEngine

@dataclass
class PerformanceMetrics:
    user_id: str
    timestamp: datetime
    strength_indicators: Dict[str, float]  # exercise -> relative strength
    volume_tolerance: float
    recovery_score: float
    motivation_level: float
    adherence_rate: float
    rpe_accuracy: float  # How well user estimates RPE
    progression_rate: float

@dataclass
class AdaptationRecommendation:
    adaptation_type: str
    confidence: float
    rationale: str
    parameters: Dict
    expected_outcome: str
    monitoring_metrics: List[str]

class AdaptiveProgramEngine:
    """ML-powered system for automatic program modifications"""
    
    def __init__(self, ai_engine: AIWorkoutEngine):
        self.ai_engine = ai_engine
        self.adaptation_models = self._initialize_adaptation_models()
        self.performance_history = {}
        self.adaptation_history = {}
        
    def _initialize_adaptation_models(self) -> Dict:
        """Initialize ML models for adaptive modifications"""
        return {
            "plateau_detection": {
                "model_type": "change_point_detection",
                "parameters": {
                    "window_size": 6,  # weeks
                    "significance_threshold": 0.02,
                    "minimum_plateau_duration": 3,  # weeks
                    "strength_variance_threshold": 0.005
                }
            },
            "overreaching_detection": {
                "model_type": "multi_factor_analysis",
                "indicators": {
                    "performance_decline": {"weight": 0.3, "threshold": -0.05},
                    "rpe_inflation": {"weight": 0.25, "threshold": 1.5},
                    "recovery_degradation": {"weight": 0.25, "threshold": -0.2},
                    "motivation_drop": {"weight": 0.20, "threshold": -0.3}
                }
            },
            "optimal_volume": {
                "model_type": "response_surface_methodology",
                "parameters": {
                    "baseline_volume": 12,  # sets per week
                    "adaptation_rate": 0.1,
                    "fatigue_threshold": 0.7,
                    "recovery_coefficient": 1.2
                }
            },
            "periodization_optimizer": {
                "model_type": "dynamic_programming",
                "phases": {
                    "accumulation": {"duration": 3, "volume_emphasis": 0.8, "intensity_cap": 0.75},
                    "intensification": {"duration": 2, "volume_emphasis": 0.4, "intensity_cap": 0.95},
                    "realization": {"duration": 1, "volume_emphasis": 0.3, "intensity_cap": 0.98},
                    "recovery": {"duration": 1, "volume_emphasis": 0.2, "intensity_cap": 0.60}
                }
            },
            "exercise_rotation": {
                "model_type": "fatigue_accumulation_model",
                "parameters": {
                    "movement_pattern_fatigue": 0.15,  # per week
                    "joint_stress_accumulation": 0.12,
                    "neural_fatigue_factor": 0.08,
                    "rotation_threshold": 0.6
                }
            }
        }

    async def analyze_adaptation_needs(self, user_id: str, current_program: Dict) -> List[AdaptationRecommendation]:
        """Analyze user's current state and recommend program adaptations"""
        
        # Get recent performance data
        performance_data = await self._get_performance_metrics(user_id)
        
        if not performance_data:
            return []
        
        recommendations = []
        
        # Check for plateau patterns
        plateau_analysis = await self._detect_plateau(user_id, performance_data)
        if plateau_analysis["detected"]:
            recommendations.append(await self._generate_plateau_solution(plateau_analysis, current_program))
        
        # Check for overreaching
        overreaching_analysis = await self._detect_overreaching(performance_data)
        if overreaching_analysis["risk_level"] > 0.6:
            recommendations.append(await self._generate_recovery_protocol(overreaching_analysis, current_program))
        
        # Optimize volume based on response
        volume_analysis = await self._analyze_volume_response(user_id, performance_data)
        if abs(volume_analysis["optimal_adjustment"]) > 0.1:
            recommendations.append(await self._generate_volume_adjustment(volume_analysis, current_program))
        
        # Check exercise rotation needs
        exercise_fatigue = await self._analyze_exercise_fatigue(user_id, current_program)
        if exercise_fatigue["rotation_needed"]:
            recommendations.append(await self._generate_exercise_rotation(exercise_fatigue, current_program))
        
        # Periodization phase optimization
        periodization_analysis = await self._analyze_periodization_status(user_id, current_program)
        if periodization_analysis["phase_change_recommended"]:
            recommendations.append(await self._generate_periodization_adjustment(periodization_analysis))
        
        return recommendations

    async def _detect_plateau(self, user_id: str, performance_data: List[PerformanceMetrics]) -> Dict:
        """Advanced plateau detection using change-point analysis"""
        
        model = self.adaptation_models["plateau_detection"]
        params = model["parameters"]
        
        if len(performance_data) < params["window_size"]:
            return {"detected": False, "reason": "insufficient_data"}
        
        # Analyze strength progression trends
        recent_data = performance_data[-params["window_size"]:]
        strength_changes = []
        
        for i in range(1, len(recent_data)):
            prev_strength = np.mean(list(recent_data[i-1].strength_indicators.values()))
            curr_strength = np.mean(list(recent_data[i].strength_indicators.values()))
            change = (curr_strength - prev_strength) / prev_strength if prev_strength > 0 else 0
            strength_changes.append(change)
        
        # Calculate moving averages and variance
        avg_change = np.mean(strength_changes)
        change_variance = np.var(strength_changes)
        
        # Plateau detection logic
        plateau_detected = (
            avg_change < params["significance_threshold"] and
            change_variance < params["strength_variance_threshold"] and
            len([c for c in strength_changes[-params["minimum_plateau_duration"]:] if c < params["significance_threshold"]]) >= params["minimum_plateau_duration"]
        )
        
        return {
            "detected": plateau_detected,
            "strength_change_rate": avg_change,
            "variance": change_variance,
            "duration_weeks": len([c for c in strength_changes if c < params["significance_threshold"]]),
            "plateau_type": self._classify_plateau_type(strength_changes, performance_data),
            "confidence": min(1.0, len(strength_changes) / params["window_size"])
        }

    async def _detect_overreaching(self, performance_data: List[PerformanceMetrics]) -> Dict:
        """Detect overreaching using multi-factor analysis"""
        
        model = self.adaptation_models["overreaching_detection"]
        indicators = model["indicators"]
        
        if len(performance_data) < 4:
            return {"risk_level": 0.0, "factors": []}
        
        recent = performance_data[-4:]  # Last 4 weeks
        baseline = performance_data[-8:-4] if len(performance_data) >= 8 else performance_data[:-4]
        
        risk_factors = []
        risk_scores = []
        
        # Performance decline analysis
        recent_perf = np.mean([p.progression_rate for p in recent])
        baseline_perf = np.mean([p.progression_rate for p in baseline])
        perf_change = (recent_perf - baseline_perf) / baseline_perf if baseline_perf > 0 else 0
        
        if perf_change < indicators["performance_decline"]["threshold"]:
            risk_factors.append("performance_decline")
            risk_scores.append(abs(perf_change) * indicators["performance_decline"]["weight"])
        
        # RPE inflation (workouts feeling harder than they should)
        recent_rpe_accuracy = np.mean([p.rpe_accuracy for p in recent])
        baseline_rpe_accuracy = np.mean([p.rpe_accuracy for p in baseline])
        rpe_inflation = recent_rpe_accuracy - baseline_rpe_accuracy
        
        if rpe_inflation > indicators["rpe_inflation"]["threshold"]:
            risk_factors.append("rpe_inflation") 
            risk_scores.append(rpe_inflation * indicators["rpe_inflation"]["weight"])
        
        # Recovery degradation
        recent_recovery = np.mean([p.recovery_score for p in recent])
        baseline_recovery = np.mean([p.recovery_score for p in baseline])
        recovery_change = (recent_recovery - baseline_recovery) / baseline_recovery if baseline_recovery > 0 else 0
        
        if recovery_change < indicators["recovery_degradation"]["threshold"]:
            risk_factors.append("recovery_degradation")
            risk_scores.append(abs(recovery_change) * indicators["recovery_degradation"]["weight"])
        
        # Motivation drop
        recent_motivation = np.mean([p.motivation_level for p in recent])
        baseline_motivation = np.mean([p.motivation_level for p in baseline])
        motivation_change = (recent_motivation - baseline_motivation) / baseline_motivation if baseline_motivation > 0 else 0
        
        if motivation_change < indicators["motivation_drop"]["threshold"]:
            risk_factors.append("motivation_drop")
            risk_scores.append(abs(motivation_change) * indicators["motivation_drop"]["weight"])
        
        total_risk = sum(risk_scores)
        
        return {
            "risk_level": min(1.0, total_risk),
            "factors": risk_factors,
            "performance_decline": perf_change,
            "rpe_inflation": rpe_inflation,
            "recovery_degradation": recovery_change,
            "motivation_decline": motivation_change,
            "recommendation_urgency": "high" if total_risk > 0.7 else "medium" if total_risk > 0.4 else "low"
        }

    async def _analyze_volume_response(self, user_id: str, performance_data: List[PerformanceMetrics]) -> Dict:
        """Analyze volume-response relationship and optimize training load"""
        
        model = self.adaptation_models["optimal_volume"]
        params = model["parameters"]
        
        if len(performance_data) < 6:
            return {"optimal_adjustment": 0.0, "confidence": 0.0}
        
        # Get volume and response data
        volumes = []
        responses = []
        
        for data_point in performance_data[-6:]:
            volume = data_point.volume_tolerance  # Proxy for current volume load
            response = data_point.progression_rate
            volumes.append(volume)
            responses.append(response)
        
        # Fit dose-response curve using polynomial regression
        volume_array = np.array(volumes)
        response_array = np.array(responses)
        
        # Find optimal volume using gradient descent approach
        current_volume = volume_array[-1]
        current_response = response_array[-1]
        
        # Calculate response gradient
        if len(volumes) >= 3:
            recent_volume_change = volumes[-1] - volumes[-3]
            recent_response_change = responses[-1] - responses[-3]
            
            response_gradient = recent_response_change / recent_volume_change if recent_volume_change != 0 else 0
        else:
            response_gradient = 0
        
        # Optimal volume prediction
        if response_gradient > 0.01:  # Positive response to volume
            optimal_adjustment = min(0.2, 0.1 * response_gradient)
        elif response_gradient < -0.01:  # Negative response to volume
            optimal_adjustment = max(-0.2, 0.1 * response_gradient)
        else:  # Neutral response
            optimal_adjustment = 0.0
        
        # Account for fatigue accumulation
        avg_fatigue = np.mean([1 - p.recovery_score for p in performance_data[-3:]])
        if avg_fatigue > params["fatigue_threshold"]:
            optimal_adjustment -= 0.15  # Reduce volume when fatigued
        
        confidence = min(1.0, len(performance_data) / 10)
        
        return {
            "current_volume": current_volume,
            "optimal_adjustment": optimal_adjustment,
            "response_gradient": response_gradient,
            "fatigue_level": avg_fatigue,
            "confidence": confidence,
            "rationale": self._generate_volume_rationale(response_gradient, avg_fatigue)
        }

    async def _analyze_exercise_fatigue(self, user_id: str, current_program: Dict) -> Dict:
        """Analyze exercise-specific fatigue and rotation needs"""
        
        model = self.adaptation_models["exercise_rotation"]
        params = model["parameters"]
        
        # Get exercise performance history
        exercise_history = await self._get_exercise_performance_history(user_id)
        
        rotation_candidates = []
        
        for exercise_name, history in exercise_history.items():
            if len(history) < 4:
                continue
                
            # Calculate fatigue accumulation
            recent_performance = history[-4:]
            
            # Movement pattern fatigue
            weeks_performed = len(recent_performance)
            movement_fatigue = weeks_performed * params["movement_pattern_fatigue"]
            
            # Performance degradation
            performance_trend = (recent_performance[-1]["strength"] - recent_performance[0]["strength"]) / recent_performance[0]["strength"]
            
            # RPE trend (increasing RPE for same loads indicates fatigue)
            rpe_trend = recent_performance[-1]["avg_rpe"] - recent_performance[0]["avg_rpe"]
            
            # Joint stress accumulation
            joint_stress = weeks_performed * params["joint_stress_accumulation"]
            
            # Neural fatigue (complex exercises accumulate more neural fatigue)
            exercise_complexity = self._get_exercise_complexity(exercise_name)
            neural_fatigue = weeks_performed * params["neural_fatigue_factor"] * (exercise_complexity / 10)
            
            total_fatigue = movement_fatigue + joint_stress + neural_fatigue
            
            # Account for negative performance trends and RPE inflation
            if performance_trend < -0.02:
                total_fatigue += 0.2
            if rpe_trend > 1.0:
                total_fatigue += 0.15
            
            if total_fatigue > params["rotation_threshold"]:
                rotation_candidates.append({
                    "exercise": exercise_name,
                    "fatigue_score": total_fatigue,
                    "performance_trend": performance_trend,
                    "rpe_trend": rpe_trend,
                    "weeks_performed": weeks_performed
                })
        
        return {
            "rotation_needed": len(rotation_candidates) > 0,
            "candidates": sorted(rotation_candidates, key=lambda x: x["fatigue_score"], reverse=True),
            "total_exercises_needing_rotation": len(rotation_candidates),
            "analysis_confidence": min(1.0, len(exercise_history) / 5)
        }

    async def _generate_plateau_solution(self, plateau_analysis: Dict, current_program: Dict) -> AdaptationRecommendation:
        """Generate ML-powered solution for breaking plateaus"""
        
        plateau_type = plateau_analysis["plateau_type"]
        
        if plateau_type == "strength_plateau":
            # Intensity-focused solution
            adaptation = {
                "type": "intensity_increase",
                "intensity_adjustment": 0.05,
                "volume_adjustment": -0.1,
                "exercise_modifications": ["add_pause_reps", "cluster_sets", "tempo_manipulation"],
                "duration_weeks": 3
            }
            rationale = "Strength plateau detected. Increasing intensity while reducing volume to stimulate new adaptations."
            
        elif plateau_type == "volume_plateau":
            # Volume periodization solution
            adaptation = {
                "type": "volume_periodization", 
                "volume_wave": [0.8, 1.0, 1.2, 0.6],  # 4-week wave
                "exercise_modifications": ["exercise_rotation", "rep_range_variation"],
                "duration_weeks": 4
            }
            rationale = "Volume-based plateau. Implementing undulating volume to restore sensitivity."
            
        else:  # general_plateau
            # Comprehensive program overhaul
            adaptation = {
                "type": "program_overhaul",
                "phase_change": "intensification",
                "exercise_rotation_percentage": 0.6,
                "new_training_variables": ["rest_pause", "drop_sets", "pre_fatigue"],
                "duration_weeks": 6
            }
            rationale = "General plateau detected. Major program restructuring needed for continued progress."
        
        return AdaptationRecommendation(
            adaptation_type=adaptation["type"],
            confidence=plateau_analysis["confidence"],
            rationale=rationale,
            parameters=adaptation,
            expected_outcome=f"Break through plateau within {adaptation['duration_weeks']} weeks",
            monitoring_metrics=["strength_progression", "rpe_trends", "motivation_levels"]
        )

    async def _generate_recovery_protocol(self, overreaching_analysis: Dict, current_program: Dict) -> AdaptationRecommendation:
        """Generate recovery protocol for overreaching"""
        
        risk_level = overreaching_analysis["risk_level"]
        factors = overreaching_analysis["factors"]
        
        if risk_level > 0.8:
            # Severe overreaching - aggressive deload
            protocol = {
                "type": "aggressive_deload",
                "volume_reduction": 0.5,
                "intensity_reduction": 0.2,
                "duration_weeks": 2,
                "recovery_focus": ["sleep_optimization", "stress_management", "active_recovery"]
            }
            
        elif risk_level > 0.6:
            # Moderate overreaching - standard deload
            protocol = {
                "type": "standard_deload",
                "volume_reduction": 0.3,
                "intensity_reduction": 0.1,
                "duration_weeks": 1,
                "recovery_focus": ["load_reduction", "movement_quality"]
            }
            
        else:
            # Mild overreaching - light adjustment
            protocol = {
                "type": "light_adjustment",
                "volume_reduction": 0.15,
                "intensity_maintenance": True,
                "duration_weeks": 1,
                "recovery_focus": ["sleep_hygiene", "nutrition_optimization"]
            }
        
        rationale = f"Overreaching detected (risk: {risk_level:.0%}). Primary factors: {', '.join(factors)}"
        
        return AdaptationRecommendation(
            adaptation_type=protocol["type"],
            confidence=0.9,
            rationale=rationale,
            parameters=protocol,
            expected_outcome="Restore performance capacity and reduce overreaching symptoms",
            monitoring_metrics=["recovery_scores", "performance_metrics", "subjective_wellness"]
        )

    # Additional helper methods for ML analysis
    def _classify_plateau_type(self, strength_changes: List[float], performance_data: List[PerformanceMetrics]) -> str:
        """Classify the type of plateau for targeted intervention"""
        
        avg_change = np.mean(strength_changes)
        recent_volume = np.mean([p.volume_tolerance for p in performance_data[-3:]])
        
        if avg_change < 0.005 and recent_volume > 0.8:
            return "volume_plateau"  # High volume, no progress
        elif avg_change < 0.005 and recent_volume < 0.6:
            return "intensity_plateau"  # Low volume, need intensity
        else:
            return "general_plateau"  # Need comprehensive change

    def _generate_volume_rationale(self, response_gradient: float, fatigue_level: float) -> str:
        """Generate explanation for volume adjustments"""
        
        if response_gradient > 0.01:
            return f"Positive response to volume (gradient: {response_gradient:.3f}). Increase recommended."
        elif response_gradient < -0.01:
            return f"Negative response to volume (gradient: {response_gradient:.3f}). Decrease recommended."
        elif fatigue_level > 0.7:
            return f"High fatigue levels ({fatigue_level:.0%}). Volume reduction for recovery."
        else:
            return "Volume appears optimal. Minor adjustments only."

    async def _get_performance_metrics(self, user_id: str) -> List[PerformanceMetrics]:
        """Get user's performance metrics history"""
        # In production, this would query the database
        # For now, return mock data
        
        base_date = datetime.now() - timedelta(weeks=12)
        metrics = []
        
        for week in range(12):
            date = base_date + timedelta(weeks=week)
            
            # Simulate realistic performance progression with plateaus
            strength_base = 1.0 + (week * 0.01)  # 1% per week base progression
            
            # Add plateau pattern after week 8
            if week > 8:
                strength_base += 0.002 * (week - 8)  # Slower progression
            
            # Add noise and individual variations
            strength_noise = np.random.normal(0, 0.005)
            
            metrics.append(PerformanceMetrics(
                user_id=user_id,
                timestamp=date,
                strength_indicators={
                    "squat": strength_base + strength_noise,
                    "bench": strength_base * 0.8 + strength_noise,
                    "deadlift": strength_base * 1.2 + strength_noise
                },
                volume_tolerance=min(1.0, 0.5 + week * 0.04),
                recovery_score=max(0.3, 0.8 - week * 0.02),  # Declining recovery
                motivation_level=max(0.4, 0.9 - week * 0.03),  # Declining motivation
                adherence_rate=max(0.6, 1.0 - week * 0.02),
                rpe_accuracy=1.0 + week * 0.05,  # RPE inflation over time
                progression_rate=max(0.0, 0.02 - week * 0.002)
            ))
        
        return metrics

    async def _get_exercise_performance_history(self, user_id: str) -> Dict[str, List[Dict]]:
        """Get exercise-specific performance history"""
        # Mock data for demonstration
        exercises = ["squat", "bench_press", "deadlift", "overhead_press"]
        history = {}
        
        for exercise in exercises:
            exercise_history = []
            base_strength = 100
            
            for week in range(8):
                # Simulate performance degradation over time for some exercises
                strength_decline = 0.98 ** week if exercise == "deadlift" else 1.01 ** week
                
                exercise_history.append({
                    "week": week + 1,
                    "strength": base_strength * strength_decline,
                    "avg_rpe": 7.0 + (week * 0.2) if exercise == "deadlift" else 7.0,
                    "volume": 12 - (week * 0.5) if exercise == "squat" else 12
                })
            
            history[exercise] = exercise_history
        
        return history

    def _get_exercise_complexity(self, exercise_name: str) -> int:
        """Get exercise complexity rating (1-10)"""
        complexity_map = {
            "squat": 8,
            "deadlift": 9,
            "bench_press": 6,
            "overhead_press": 7,
            "pull_ups": 5,
            "rows": 4,
            "curls": 2
        }
        
        return complexity_map.get(exercise_name.lower(), 5)