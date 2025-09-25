"""
Khyrie Fitness Platform - Subscription API Routes
Copyright (C) 2025 Darnell Roy

Premium subscription management endpoints.
"""

import os
import stripe
import logging
from datetime import datetime
from typing import Dict, List, Any
from fastapi import APIRouter, HTTPException, Request, Depends, Header
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from subscription_manager import SubscriptionManager, UserSubscription
from premium_ai_features import PremiumAIFeatures, WorkoutRequest, InjuryAnalysisRequest, AICoachMessage

# Configure logging
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Pydantic models for API requests
class SubscriptionCreateRequest(BaseModel):
    plan_type: str  # 'premium', 'pro', 'elite'
    payment_method_id: str
    user_email: EmailStr

class SubscriptionUpgradeRequest(BaseModel):
    new_plan_type: str

class UserAuthDep:
    """Dependency to get current user ID from authorization."""
    def __call__(self, authorization: str = Header(None)) -> int:
        # Implement your JWT token validation here
        # For now, returning a mock user ID
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header required")
        
        # Extract and validate JWT token
        try:
            # Mock implementation - replace with actual JWT validation
            user_id = self.extract_user_id_from_token(authorization)
            return user_id
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid authorization token")
    
    def extract_user_id_from_token(self, token: str) -> int:
        # Mock implementation - replace with actual JWT decoding
        return 1  # Return actual user ID from JWT

get_current_user = UserAuthDep()

def get_db_session():
    """Dependency to get database session."""
    # Implement your database session creation here
    # This is a placeholder - you'll need to integrate with your actual database
    pass

# Subscription Management Endpoints

@router.get("/plans")
async def get_subscription_plans():
    """Get available subscription plans with pricing and features."""
    return {
        "plans": [
            {
                "id": "premium",
                "name": "Premium",
                "price": 9.99,
                "currency": "USD",
                "interval": "month",
                "trial_days": 7,
                "description": "Perfect for individuals serious about fitness",
                "features": [
                    "AI-powered workout recommendations",
                    "Advanced progress analytics", 
                    "Unlimited family members (up to 10)",
                    "Custom meal plans",
                    "Priority email support",
                    "Exercise library (500+ exercises)",
                    "Monthly workout generation (30 workouts)"
                ],
                "limitations": {
                    "ai_conversations": 0,
                    "form_analyses": 0,
                    "workout_generations": 30
                },
                "most_popular": True,
                "savings_vs_personal_trainer": "$150-300/month"
            },
            {
                "id": "pro",
                "name": "Pro",
                "price": 19.99,
                "currency": "USD",
                "interval": "month", 
                "trial_days": 7,
                "description": "Advanced features for serious athletes",
                "features": [
                    "Everything in Premium",
                    "Real-time exercise form analysis",
                    "Predictive injury prevention",
                    "Wearable device integration",
                    "API access for developers",
                    "Unlimited exercise library",
                    "Unlimited family members",
                    "Monthly form analyses (50 analyses)"
                ],
                "limitations": {
                    "ai_conversations": 0,
                    "form_analyses": 50,
                    "workout_generations": 100
                },
                "best_value": True,
                "savings_vs_personal_trainer": "$200-500/month"
            },
            {
                "id": "elite",
                "name": "Elite",
                "price": 39.99,
                "currency": "USD",
                "interval": "month",
                "trial_days": 7,
                "description": "Complete fitness ecosystem with AI coach",
                "features": [
                    "Everything in Pro",
                    "24/7 Personal AI Coach with voice guidance",
                    "AR/VR workout experiences",
                    "One-on-one virtual trainer sessions",
                    "Advanced biometric tracking",
                    "White-label licensing",
                    "Unlimited everything",
                    "Priority phone support"
                ],
                "limitations": {
                    "ai_conversations": -1,  # Unlimited
                    "form_analyses": -1,     # Unlimited
                    "workout_generations": -1 # Unlimited
                },
                "enterprise": True,
                "savings_vs_personal_trainer": "$400-1000/month"
            }
        ],
        "free_tier": {
            "name": "Free",
            "price": 0,
            "features": [
                "Basic workout tracking",
                "Exercise library (50 exercises)",
                "Family group (up to 3 members)",
                "Basic progress charts",
                "Community access"
            ],
            "limitations": {
                "exercise_library_limit": 50,
                "family_members_limit": 3,
                "ai_recommendations_limit": 0
            }
        }
    }

@router.post("/create")
async def create_subscription(
    request: SubscriptionCreateRequest,
    user_id: int = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Create a new subscription with Stripe."""
    try:
        subscription_manager = SubscriptionManager(db_session)
        
        # Validate plan type
        if request.plan_type not in ['premium', 'pro', 'elite']:
            raise HTTPException(status_code=400, detail="Invalid plan type")
        
        # Create subscription
        result = await subscription_manager.create_subscription(
            user_id=user_id,
            plan_type=request.plan_type,
            payment_method_id=request.payment_method_id,
            user_email=request.user_email
        )
        
        return {
            "success": True,
            "message": f"Successfully subscribed to {request.plan_type.title()} plan",
            "subscription": result,
            "trial_info": {
                "trial_days": 7,
                "trial_end": result.get('trial_end'),
                "message": "Your free trial starts now! Cancel anytime during the trial period."
            },
            "next_steps": [
                "Explore AI workout recommendations",
                "Set up your fitness goals",
                "Invite family members to your group"
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Subscription creation failed for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Subscription creation failed")

@router.get("/status")
async def get_subscription_status(
    user_id: int = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Get current subscription status and usage information."""
    try:
        subscription_manager = SubscriptionManager(db_session)
        status = await subscription_manager.get_subscription_status(user_id)
        
        # Get current month usage for premium features
        if status['plan_type'] != 'free':
            usage_stats = await get_monthly_usage_stats(user_id, db_session)
            status['usage_statistics'] = usage_stats
        
        return {
            "subscription": status,
            "billing_info": await get_billing_info(user_id, db_session) if status['plan_type'] != 'free' else None,
            "upgrade_benefits": get_upgrade_benefits(status['plan_type']),
            "support_level": get_support_level(status['plan_type'])
        }
        
    except Exception as e:
        logger.error(f"Error getting subscription status for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve subscription status")

@router.post("/cancel")
async def cancel_subscription(
    user_id: int = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Cancel current subscription (at end of billing period)."""
    try:
        subscription_manager = SubscriptionManager(db_session)
        result = await subscription_manager.cancel_subscription(user_id)
        
        return {
            "success": True,
            "message": result['message'],
            "access_until": result['current_period_end'],
            "feedback_request": "We'd love to know why you're leaving. Please share your feedback.",
            "reactivation_info": "You can reactivate your subscription anytime before it expires."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Subscription cancellation failed for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Subscription cancellation failed")

@router.post("/upgrade")
async def upgrade_subscription(
    request: SubscriptionUpgradeRequest,
    user_id: int = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Upgrade to a higher tier subscription."""
    try:
        # Get current subscription
        subscription_manager = SubscriptionManager(db_session)
        current_status = await subscription_manager.get_subscription_status(user_id)
        
        if current_status['plan_type'] == 'free':
            raise HTTPException(
                status_code=400, 
                detail="Cannot upgrade from free plan. Please create a new subscription."
            )
        
        # Validate upgrade path
        plan_hierarchy = {'premium': 1, 'pro': 2, 'elite': 3}
        current_level = plan_hierarchy.get(current_status['plan_type'], 0)
        new_level = plan_hierarchy.get(request.new_plan_type, 0)
        
        if new_level <= current_level:
            raise HTTPException(
                status_code=400,
                detail="Cannot downgrade or switch to same plan. Please contact support."
            )
        
        # Perform upgrade via Stripe
        stripe_subscription_id = current_status['stripe_subscription_id']
        new_price_id = subscription_manager.PLANS[request.new_plan_type]['stripe_price_id']
        
        # Update Stripe subscription
        updated_subscription = stripe.Subscription.modify(
            stripe_subscription_id,
            items=[{
                'id': stripe_subscription_id,
                'price': new_price_id,
            }],
            proration_behavior='create_prorations'
        )
        
        # Update database
        db_subscription = db_session.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status == 'active'
        ).first()
        
        if db_subscription:
            db_subscription.plan_type = request.new_plan_type
            db_subscription.updated_at = datetime.utcnow()
            db_session.commit()
        
        return {
            "success": True,
            "message": f"Successfully upgraded to {request.new_plan_type.title()} plan",
            "new_features": get_new_features_after_upgrade(current_status['plan_type'], request.new_plan_type),
            "billing_change": "Prorated billing will be applied to your next invoice",
            "immediate_access": "All new features are available immediately"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Subscription upgrade failed for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Subscription upgrade failed")

# Premium Feature Endpoints

@router.post("/premium/workout-generation")
async def generate_ai_workout(
    request: WorkoutRequest,
    user_id: int = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Generate AI-powered personalized workout (Premium feature)."""
    return await PremiumAIFeatures.generate_personalized_workout(
        user_id=user_id,
        request=request,
        db_session=db_session
    )

@router.post("/premium/injury-analysis")
async def analyze_injury_risk(
    request: InjuryAnalysisRequest,
    user_id: int = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Analyze injury risk patterns (Pro feature)."""
    return await PremiumAIFeatures.analyze_injury_risk(
        user_id=user_id,
        request=request,
        db_session=db_session
    )

@router.post("/premium/ai-coach")
async def ai_coach_conversation(
    message: AICoachMessage,
    user_id: int = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Chat with personal AI coach (Elite feature)."""
    return await PremiumAIFeatures.ai_coach_conversation(
        user_id=user_id,
        message=message,
        db_session=db_session
    )

@router.get("/premium/usage")
async def get_premium_usage_stats(
    user_id: int = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """Get detailed usage statistics for premium features."""
    try:
        subscription_manager = SubscriptionManager(db_session)
        
        # Get subscription info
        subscription_status = await subscription_manager.get_subscription_status(user_id)
        
        if subscription_status['plan_type'] == 'free':
            return {
                "message": "Premium usage tracking requires a paid subscription",
                "upgrade_url": "/subscription/upgrade"
            }
        
        # Get usage statistics
        usage_stats = await get_detailed_usage_stats(user_id, db_session)
        
        return {
            "current_plan": subscription_status['plan_type'],
            "billing_period": {
                "start": subscription_status['current_period_start'],
                "end": subscription_status['current_period_end']
            },
            "usage_statistics": usage_stats,
            "recommendations": await get_usage_recommendations(user_id, usage_stats, db_session)
        }
        
    except Exception as e:
        logger.error(f"Error getting usage stats for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve usage statistics")

# Stripe Webhook Endpoint

@router.post("/webhook")
async def stripe_webhook(request: Request, db_session: Session = Depends(get_db_session)):
    """Handle Stripe webhook events for subscription management."""
    try:
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature')
        
        if not sig_header or not STRIPE_WEBHOOK_SECRET:
            raise HTTPException(status_code=400, detail="Missing webhook signature")
        
        # Verify webhook signature
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Handle webhook event
        subscription_manager = SubscriptionManager(db_session)
        await subscription_manager.handle_webhook_event(event)
        
        logger.info(f"Processed Stripe webhook event: {event['type']}")
        
        return {"success": True}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")

# Helper Functions

async def get_monthly_usage_stats(user_id: int, db_session) -> Dict[str, Any]:
    """Get current month usage statistics."""
    # Implementation depends on your FeatureUsage tracking
    return {
        "workout_generations": {"used": 15, "limit": 30},
        "ai_conversations": {"used": 0, "limit": 0},
        "form_analyses": {"used": 0, "limit": 0}
    }

async def get_billing_info(user_id: int, db_session) -> Dict[str, Any]:
    """Get billing information for user."""
    return {
        "next_billing_date": "2025-10-25",
        "amount": 9.99,
        "currency": "USD",
        "payment_method": "**** **** **** 1234"
    }

def get_upgrade_benefits(current_plan: str) -> List[str]:
    """Get benefits of upgrading from current plan."""
    if current_plan == 'free':
        return [
            "AI-powered workout recommendations",
            "Advanced analytics",
            "Priority support",
            "7-day free trial"
        ]
    elif current_plan == 'premium':
        return [
            "Real-time form analysis",
            "Injury prevention insights",
            "Wearable integration",
            "API access"
        ]
    elif current_plan == 'pro':
        return [
            "Personal AI coach",
            "AR/VR workouts",
            "Trainer sessions",
            "Unlimited everything"
        ]
    return []

def get_support_level(plan_type: str) -> str:
    """Get support level description."""
    support_levels = {
        'free': 'Community support',
        'premium': 'Priority email support',
        'pro': 'Priority email + chat support',
        'elite': 'Priority phone + email + chat support'
    }
    return support_levels.get(plan_type, 'Community support')

def get_new_features_after_upgrade(old_plan: str, new_plan: str) -> List[str]:
    """Get list of new features available after upgrade."""
    # Implementation based on plan feature differences
    return [
        "Real-time form analysis",
        "Injury prevention insights",
        "Advanced biometric tracking"
    ]

async def get_detailed_usage_stats(user_id: int, db_session) -> Dict[str, Any]:
    """Get detailed usage statistics for all premium features."""
    return {
        "ai_workouts": {
            "total_generated": 45,
            "this_month": 15,
            "favorite_types": ["strength", "cardio", "flexibility"],
            "avg_rating": 4.7
        },
        "injury_prevention": {
            "analyses_run": 8,
            "risk_trend": "decreasing",
            "recommendations_followed": "78%"
        },
        "ai_coach": {
            "conversations": 0,
            "topics_discussed": [],
            "satisfaction_score": None
        }
    }

async def get_usage_recommendations(user_id: int, usage_stats: Dict, db_session) -> List[str]:
    """Get personalized recommendations based on usage patterns."""
    return [
        "Try generating a different workout style to explore new exercises",
        "Consider upgrading to Pro for injury prevention features",
        "Your workout consistency is excellent - keep it up!"
    ]