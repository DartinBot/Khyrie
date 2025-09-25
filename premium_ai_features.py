"""
Khyrie Fitness Platform - Premium AI Features
Copyright (C) 2025 Darnell Roy

Commercial License - Premium Features
These features require a paid subscription and are protected under commercial licensing.
"""

import openai
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from functools import wraps
from fastapi import HTTPException, Depends
from pydantic import BaseModel

from subscription_manager import SubscriptionManager

logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class PremiumFeatureError(Exception):
    """Raised when premium feature access is denied."""
    pass

def require_premium_feature(feature_name: str, track_usage: bool = True):
    """
    Decorator to gate premium features behind subscription checks.
    
    Args:
        feature_name: Name of the feature to check access for
        track_usage: Whether to track usage of this feature
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract user_id from function arguments
            user_id = kwargs.get('user_id')
            if user_id is None and len(args) > 0:
                user_id = args[0] if isinstance(args[0], int) else None
            
            if not user_id:
                raise HTTPException(status_code=401, detail="User authentication required")
            
            # Get database session (assuming it's passed in kwargs or available globally)
            db_session = kwargs.get('db_session')  # You'll need to pass this
            if not db_session:
                raise HTTPException(status_code=500, detail="Database session not available")
            
            subscription_manager = SubscriptionManager(db_session)
            
            # Check feature access
            access_info = await subscription_manager.check_feature_access(user_id, feature_name)
            
            if not access_info['has_access']:
                if access_info['upgrade_required']:
                    raise HTTPException(
                        status_code=402,
                        detail={
                            "error": "Premium feature requires subscription upgrade",
                            "feature": feature_name,
                            "current_plan": access_info['plan_type'],
                            "upgrade_url": "/subscription/upgrade"
                        }
                    )
                else:
                    raise HTTPException(
                        status_code=429,
                        detail={
                            "error": "Feature usage limit exceeded",
                            "feature": feature_name,
                            "usage_info": access_info['usage_info'],
                            "reset_date": "next month"
                        }
                    )
            
            # Track usage if enabled
            if track_usage:
                await subscription_manager.track_feature_usage(user_id, feature_name)
            
            # Execute the original function
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator

class WorkoutRequest(BaseModel):
    """Request model for AI workout generation."""
    fitness_level: str  # 'beginner', 'intermediate', 'advanced'
    available_time: int  # minutes
    goals: List[str]  # ['weight_loss', 'muscle_gain', 'endurance', etc.]
    equipment: List[str]  # ['dumbbells', 'resistance_bands', 'none', etc.]
    limitations: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

class InjuryAnalysisRequest(BaseModel):
    """Request model for injury risk analysis."""
    workout_intensity: str
    recovery_time: int
    sleep_quality: int  # 1-10
    stress_level: int  # 1-10
    pain_areas: Optional[List[str]] = None

class AICoachMessage(BaseModel):
    """Request model for AI coach conversation."""
    message: str
    context: Optional[str] = None

class PremiumAIFeatures:
    """Premium AI-powered fitness features."""
    
    @staticmethod
    @require_premium_feature('ai_recommendations', track_usage=True)
    async def generate_personalized_workout(user_id: int, request: WorkoutRequest, 
                                          db_session=None) -> Dict[str, Any]:
        """
        Generate AI-powered personalized workout plans.
        Premium Feature - Requires Premium, Pro, or Elite subscription.
        """
        try:
            # Get user's fitness history and preferences
            user_context = await get_user_fitness_context(user_id, db_session)
            
            # Build comprehensive prompt for AI
            prompt = f"""
            Create a personalized workout plan for a user with the following profile:
            
            FITNESS PROFILE:
            - Current Level: {request.fitness_level}
            - Available Time: {request.available_time} minutes
            - Primary Goals: {', '.join(request.goals)}
            - Available Equipment: {', '.join(request.equipment)}
            - Limitations: {request.limitations or 'None specified'}
            
            HISTORICAL DATA:
            - Recent Performance: {user_context.get('performance_summary', 'No recent data')}
            - Preferred Exercise Types: {', '.join(user_context.get('preferred_exercises', []))}
            - Previous Injuries: {user_context.get('injury_history', 'None')}
            - Workout Frequency: {user_context.get('weekly_frequency', 'Unknown')} times per week
            
            REQUIREMENTS:
            Generate a complete workout plan with:
            1. Dynamic warm-up (5-8 minutes)
            2. Main workout with specific exercises, sets, reps, and rest periods
            3. Cool-down and flexibility routine (5-10 minutes)
            4. Estimated calorie burn and difficulty rating
            5. Progress tracking recommendations
            6. Safety notes and form cues
            
            Format the response as a structured JSON with clear sections for each component.
            Ensure the workout is challenging but appropriate for their fitness level.
            """
            
            # Call OpenAI GPT-4 for workout generation
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert personal trainer and exercise physiologist. Create safe, effective, and personalized workout plans based on scientific principles."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            workout_content = response.choices[0].message.content
            
            # Parse and structure the workout plan
            workout_plan = await parse_workout_plan(workout_content)
            
            # Save generated workout to database
            await save_generated_workout(user_id, workout_plan, 'ai_premium', db_session)
            
            # Calculate estimated metrics
            estimated_calories = calculate_calorie_burn(
                request.fitness_level, 
                request.available_time, 
                workout_plan.get('intensity', 'moderate')
            )
            
            result = {
                "workout_id": workout_plan['id'],
                "title": f"AI Personalized Workout - {datetime.now().strftime('%Y-%m-%d')}",
                "workout_plan": workout_plan,
                "estimated_calories": estimated_calories,
                "estimated_duration": request.available_time,
                "difficulty_rating": workout_plan.get('difficulty', 7),
                "generated_at": datetime.utcnow().isoformat(),
                "personalization_score": calculate_personalization_score(user_context, request),
                "next_workout_recommendation": await get_next_workout_suggestion(user_id, db_session)
            }
            
            logger.info(f"Generated AI workout for user {user_id}, duration: {request.available_time}min")
            return result
            
        except Exception as e:
            logger.error(f"Error generating AI workout for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Workout generation failed")
    
    @staticmethod
    @require_premium_feature('injury_prevention', track_usage=True)
    async def analyze_injury_risk(user_id: int, request: InjuryAnalysisRequest, 
                                db_session=None) -> Dict[str, Any]:
        """
        Analyze injury risk based on workout patterns and biometric data.
        Pro Feature - Requires Pro or Elite subscription.
        """
        try:
            # Get comprehensive user health data
            health_data = await get_user_health_metrics(user_id, db_session)
            workout_history = await get_recent_workout_history(user_id, days=14, db_session=db_session)
            
            # Analyze risk factors
            risk_factors = {
                "overtraining": analyze_overtraining_risk(workout_history, request),
                "insufficient_recovery": analyze_recovery_patterns(health_data, request),
                "muscle_imbalance": detect_muscle_imbalances(workout_history),
                "form_degradation": assess_form_consistency(workout_history),
                "external_stress": calculate_stress_impact(request.stress_level, request.sleep_quality),
                "pain_indicators": assess_pain_risk(request.pain_areas or [])
            }
            
            # Calculate overall risk score (0-100)
            overall_risk = calculate_injury_risk_score(risk_factors)
            
            # Generate AI-powered recommendations
            recommendations = await generate_injury_prevention_recommendations(
                user_id, risk_factors, overall_risk, db_session
            )
            
            result = {
                "risk_assessment": {
                    "overall_score": overall_risk,
                    "risk_level": get_risk_level(overall_risk),
                    "primary_concerns": get_primary_risk_factors(risk_factors),
                    "trend": calculate_risk_trend(user_id, overall_risk, db_session)
                },
                "detailed_analysis": risk_factors,
                "recommendations": recommendations,
                "next_assessment_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
                "emergency_indicators": check_emergency_indicators(risk_factors),
                "generated_at": datetime.utcnow().isoformat()
            }
            
            # Save analysis for trend tracking
            await save_injury_analysis(user_id, result, db_session)
            
            logger.info(f"Generated injury risk analysis for user {user_id}, risk score: {overall_risk}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing injury risk for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Injury risk analysis failed")
    
    @staticmethod
    @require_premium_feature('ai_coach', track_usage=True)
    async def ai_coach_conversation(user_id: int, message: AICoachMessage, 
                                  db_session=None) -> Dict[str, Any]:
        """
        Personal AI coach with contextual fitness guidance.
        Elite Feature - Requires Elite subscription.
        """
        try:
            # Get comprehensive user context
            user_profile = await get_comprehensive_user_profile(user_id, db_session)
            conversation_history = await get_coach_conversation_history(user_id, limit=20, db_session=db_session)
            current_goals = await get_active_user_goals(user_id, db_session)
            recent_progress = await get_recent_progress_summary(user_id, db_session)
            
            # Build context-aware system prompt
            system_prompt = f"""
            You are an elite personal fitness coach and wellness expert for {user_profile.get('name', 'this user')}.
            
            USER PROFILE:
            - Fitness Level: {user_profile.get('fitness_level', 'Unknown')}
            - Primary Goals: {', '.join(current_goals)}
            - Current Program: {user_profile.get('current_program', 'None')}
            - Training Experience: {user_profile.get('training_years', 'Unknown')} years
            - Preferences: {user_profile.get('exercise_preferences', 'None specified')}
            
            RECENT PROGRESS:
            - Last 30 Days: {recent_progress.get('summary', 'No recent activity')}
            - Achievements: {', '.join(recent_progress.get('achievements', []))}
            - Challenges: {', '.join(recent_progress.get('challenges', []))}
            
            COACHING STYLE:
            - Be encouraging, motivational, and supportive
            - Provide specific, actionable fitness advice
            - Reference their progress and goals in responses
            - Ask follow-up questions when appropriate
            - Maintain professional expertise while being personable
            - Always prioritize safety and proper form
            
            Current conversation context: {message.context or 'General fitness discussion'}
            """
            
            # Build conversation messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent conversation history for context
            for msg in conversation_history[-10:]:  # Last 10 messages
                messages.extend([
                    {"role": "user", "content": msg['user_message']},
                    {"role": "assistant", "content": msg['coach_response']}
                ])
            
            # Add current message
            messages.append({"role": "user", "content": message.message})
            
            # Generate AI coach response
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=messages,
                temperature=0.8,
                max_tokens=600,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            coach_response = response.choices[0].message.content
            
            # Analyze response sentiment and coaching approach
            coaching_analysis = analyze_coaching_response(coach_response)
            
            # Save conversation to history
            await save_coach_conversation(
                user_id=user_id,
                user_message=message.message,
                coach_response=coach_response,
                context=message.context,
                db_session=db_session
            )
            
            # Determine follow-up actions
            follow_up_suggestions = await generate_follow_up_suggestions(
                user_id, message.message, coach_response, db_session
            )
            
            result = {
                "response": coach_response,
                "coaching_style": coaching_analysis.get('style', 'motivational'),
                "sentiment": coaching_analysis.get('sentiment', 'positive'),
                "key_topics": coaching_analysis.get('topics', []),
                "follow_up_suggestions": follow_up_suggestions,
                "conversation_id": await get_or_create_conversation_id(user_id, db_session),
                "response_time": datetime.utcnow().isoformat(),
                "coach_availability": "24/7 AI Coach"
            }
            
            logger.info(f"AI coach response generated for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error in AI coach conversation for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="AI coach conversation failed")

# Helper functions (to be implemented based on your database schema)

async def get_user_fitness_context(user_id: int, db_session) -> Dict[str, Any]:
    """Get comprehensive fitness context for a user."""
    # Implementation depends on your database schema
    return {
        "performance_summary": "Consistent moderate intensity workouts",
        "preferred_exercises": ["squats", "pushups", "running"],
        "injury_history": "Minor knee strain 6 months ago",
        "weekly_frequency": "4"
    }

async def parse_workout_plan(content: str) -> Dict[str, Any]:
    """Parse AI-generated workout content into structured format."""
    # You'll need to implement JSON parsing or structured text parsing
    return {
        "id": f"workout_{int(datetime.utcnow().timestamp())}",
        "warmup": [],
        "main_exercises": [],
        "cooldown": [],
        "intensity": "moderate",
        "difficulty": 7
    }

async def save_generated_workout(user_id: int, workout_plan: Dict, source: str, db_session):
    """Save generated workout to database."""
    # Implementation depends on your workout storage schema
    pass

def calculate_calorie_burn(fitness_level: str, duration: int, intensity: str) -> int:
    """Calculate estimated calorie burn."""
    base_rate = {"beginner": 6, "intermediate": 8, "advanced": 10}
    intensity_multiplier = {"low": 0.8, "moderate": 1.0, "high": 1.3}
    
    return int(base_rate.get(fitness_level, 8) * duration * intensity_multiplier.get(intensity, 1.0))

def calculate_personalization_score(user_context: Dict, request: WorkoutRequest) -> int:
    """Calculate how personalized the workout is (0-100)."""
    # Implementation based on how well the workout matches user preferences
    return 85

async def get_next_workout_suggestion(user_id: int, db_session) -> str:
    """Get suggestion for the next workout."""
    return "Focus on lower body strength training in 2-3 days"

# Additional helper functions would be implemented here...

def analyze_overtraining_risk(workout_history: List, request: InjuryAnalysisRequest) -> Dict[str, Any]:
    """Analyze overtraining risk from workout patterns."""
    return {"score": 25, "indicators": ["Consistent high intensity", "Limited rest days"]}

def analyze_recovery_patterns(health_data: Dict, request: InjuryAnalysisRequest) -> Dict[str, Any]:
    """Analyze recovery adequacy."""
    return {"score": 15, "factors": ["Good sleep quality", "Adequate rest periods"]}

def detect_muscle_imbalances(workout_history: List) -> Dict[str, Any]:
    """Detect potential muscle imbalances from exercise patterns."""
    return {"score": 30, "imbalances": ["Upper body dominant training"]}

def calculate_injury_risk_score(risk_factors: Dict) -> int:
    """Calculate overall injury risk score."""
    total_score = sum(factor.get('score', 0) for factor in risk_factors.values())
    return min(100, max(0, total_score // len(risk_factors)))

def get_risk_level(score: int) -> str:
    """Convert risk score to human-readable level."""
    if score < 20:
        return "Low"
    elif score < 40:
        return "Moderate"
    elif score < 60:
        return "High"
    else:
        return "Very High"