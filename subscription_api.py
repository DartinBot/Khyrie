"""
Subscription API Endpoints
FastAPI endpoints for managing Stripe subscriptions and premium features
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
import stripe
import json
from datetime import datetime, timedelta

from stripe_integration import stripe_manager, SubscriptionTier
from subscription_models import get_db, User, Subscription, AIInsight, FeatureUsage
from premium_ai_features import premium_ai, WorkoutAnalysis, FitnessInsight

# Create router
subscription_router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])

# Dependency to get current user (simplified for demo)
async def get_current_user(db: Session = Depends(get_db)) -> User:
    """Get current authenticated user - simplified for demo"""
    # In production, this would validate JWT tokens, etc.
    user = db.query(User).filter(User.email == "premium_user@example.com").first()
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

# SUBSCRIPTION MANAGEMENT ENDPOINTS

@subscription_router.get("/plans")
async def get_subscription_plans():
    """Get all available subscription plans"""
    plans = []
    
    for tier, details in stripe_manager.pricing_plans.items():
        plan = {
            "tier": tier.value,
            "name": f"Khyrie {tier.value.title()}",
            "price_monthly": details["price"] / 100 if details["price"] else 0,
            "features": details["features"],
            "recommended": tier == SubscriptionTier.PREMIUM
        }
        plans.append(plan)
    
    return {"plans": plans}

@subscription_router.post("/create")
async def create_subscription(
    plan_data: Dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new subscription for the user"""
    try:
        tier = plan_data.get("tier")
        if not tier or tier not in ["premium", "pro", "elite"]:
            raise HTTPException(status_code=400, detail="Invalid subscription tier")
        
        # Get or create Stripe customer
        if not current_user.stripe_customer_id:
            customer_id = await stripe_manager.create_customer(
                user_id=str(current_user.id),
                email=current_user.email,
                name=current_user.full_name
            )
            if not customer_id:
                raise HTTPException(status_code=500, detail="Failed to create customer")
            
            current_user.stripe_customer_id = customer_id
            db.commit()
        
        # Create subscription
        price_id = stripe_manager.pricing_plans[SubscriptionTier(tier)]["price_id"]
        subscription_result = await stripe_manager.create_subscription(
            customer_id=current_user.stripe_customer_id,
            price_id=price_id
        )
        
        if not subscription_result:
            raise HTTPException(status_code=500, detail="Failed to create subscription")
        
        # Update user subscription status
        current_user.subscription_tier = tier
        current_user.subscription_status = "active"
        current_user.subscription_start = datetime.utcnow()
        current_user.subscription_end = datetime.utcnow() + timedelta(days=30)
        
        # Create subscription record
        subscription = Subscription(
            user_id=current_user.id,
            stripe_subscription_id=subscription_result["subscription_id"],
            stripe_price_id=price_id,
            tier=tier,
            status="active",
            amount=stripe_manager.pricing_plans[SubscriptionTier(tier)]["price"],
            started_at=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=30)
        )
        
        db.add(subscription)
        db.commit()
        
        return {
            "success": True,
            "subscription_id": subscription_result["subscription_id"],
            "client_secret": subscription_result["client_secret"],
            "message": f"Successfully upgraded to {tier.title()} plan!"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Subscription creation failed: {str(e)}")

@subscription_router.get("/status")
async def get_subscription_status(current_user: User = Depends(get_current_user)):
    """Get current user's subscription status"""
    return {
        "user_id": current_user.id,
        "tier": current_user.subscription_tier,
        "status": current_user.subscription_status,
        "started": current_user.subscription_start,
        "ends": current_user.subscription_end,
        "features": stripe_manager.get_features_for_tier(SubscriptionTier(current_user.subscription_tier))
    }

@subscription_router.post("/cancel")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel current subscription"""
    try:
        if not current_user.stripe_customer_id:
            raise HTTPException(status_code=400, detail="No active subscription found")
        
        # Get current subscription
        subscription_info = await stripe_manager.get_subscription_status(current_user.stripe_customer_id)
        if not subscription_info:
            raise HTTPException(status_code=400, detail="No active subscription found")
        
        # Cancel in Stripe
        success = await stripe_manager.cancel_subscription(subscription_info["subscription_id"])
        if not success:
            raise HTTPException(status_code=500, detail="Failed to cancel subscription")
        
        # Update local records
        current_user.subscription_status = "canceled"
        
        # Update subscription record
        subscription = db.query(Subscription).filter(
            Subscription.stripe_subscription_id == subscription_info["subscription_id"]
        ).first()
        if subscription:
            subscription.status = "canceled"
            subscription.canceled_at = datetime.utcnow()
            subscription.cancel_at_period_end = True
        
        db.commit()
        
        return {
            "success": True,
            "message": "Subscription canceled. Access will continue until the end of your billing period."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cancellation failed: {str(e)}")

# PREMIUM FEATURE ENDPOINTS

@subscription_router.post("/ai/generate-workout")
async def generate_ai_workout(
    workout_request: Dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate AI-powered workout (Premium+ feature)"""
    # Check subscription tier
    if not current_user.is_premium_user():
        raise HTTPException(
            status_code=403, 
            detail="This feature requires a Premium subscription or higher"
        )
    
    # Track feature usage
    usage = FeatureUsage(
        user_id=current_user.id,
        feature_name="ai_workout_generation",
        required_tier="premium",
        user_tier_at_time=current_user.subscription_tier
    )
    db.add(usage)
    db.commit()
    
    # Generate workout
    user_data = {
        "fitness_level": current_user.fitness_level,
        "weight": current_user.weight,
        "age": current_user.age,
        "goals": json.loads(current_user.fitness_goals) if current_user.fitness_goals else ["general_fitness"]
    }
    
    workout = await premium_ai.generate_ai_workout(user_data, workout_request)
    
    return {"workout": workout, "tier_required": "premium"}

@subscription_router.post("/ai/analyze-progress")
async def analyze_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze workout progress trends (Premium+ feature)"""
    if not current_user.is_premium_user():
        raise HTTPException(
            status_code=403, 
            detail="This feature requires a Premium subscription or higher"
        )
    
    # Get user's workout history
    user_workouts = db.query(current_user.workouts).all()
    workout_data = [
        {
            "workout_name": w.workout_name,
            "duration": w.duration_minutes,
            "calories": w.calories_burned,
            "completed": w.completed_at is not None,
            "date": w.created_at
        }
        for w in user_workouts
    ]
    
    analysis = await premium_ai.analyze_progress_trends(workout_data)
    
    return {"analysis": analysis, "tier_required": "premium"}

@subscription_router.post("/ai/nutrition-recommendations")
async def get_nutrition_recommendations(
    current_user: User = Depends(get_current_user)
):
    """Get AI nutrition recommendations (Premium+ feature)"""
    if not current_user.is_premium_user():
        raise HTTPException(
            status_code=403, 
            detail="This feature requires a Premium subscription or higher"
        )
    
    user_data = {
        "weight": current_user.weight or 70,
        "height": current_user.height or 170,
        "age": current_user.age or 30,
        "activity_level": "moderate"  # Could be stored in user profile
    }
    
    goals = json.loads(current_user.fitness_goals) if current_user.fitness_goals else ["general_fitness"]
    
    recommendations = await premium_ai.get_nutrition_recommendations(user_data, goals)
    
    return {"nutrition": recommendations, "tier_required": "premium"}

@subscription_router.post("/ai/form-analysis")
async def analyze_workout_form(
    exercise_data: Dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze workout form with injury risk assessment (Pro+ feature)"""
    if not current_user.is_pro_user():
        raise HTTPException(
            status_code=403, 
            detail="This feature requires a Pro subscription or higher"
        )
    
    # Track feature usage
    usage = FeatureUsage(
        user_id=current_user.id,
        feature_name="ai_form_analysis",
        required_tier="pro",
        user_tier_at_time=current_user.subscription_tier
    )
    db.add(usage)
    db.commit()
    
    analysis = await premium_ai.analyze_workout_form(exercise_data)
    
    # Store AI insight
    insight = AIInsight(
        user_id=current_user.id,
        insight_type="form_analysis",
        title=f"Form Analysis: {exercise_data.get('name', 'Exercise')}",
        content=json.dumps({
            "form_score": analysis.form_score,
            "injury_risk": analysis.injury_risk,
            "recommendations": analysis.recommendations,
            "improvements": analysis.improvements
        }),
        confidence_score=analysis.form_score,
        required_tier="pro"
    )
    db.add(insight)
    db.commit()
    
    return {
        "analysis": {
            "form_score": analysis.form_score,
            "injury_risk": analysis.injury_risk,
            "recommendations": analysis.recommendations,
            "improvements": analysis.improvements,
            "next_workout": analysis.next_workout_suggestion
        },
        "tier_required": "pro"
    }

@subscription_router.post("/ai/injury-risk-prediction")
async def predict_injury_risk(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict injury risk based on workout patterns (Pro+ feature)"""
    if not current_user.is_pro_user():
        raise HTTPException(
            status_code=403, 
            detail="This feature requires a Pro subscription or higher"
        )
    
    # Get recent workout data
    recent_workouts = db.query(current_user.workouts).filter(
        current_user.workouts.created_at >= datetime.utcnow() - timedelta(days=7)
    ).all()
    
    workout_data = [
        {
            "intensity": "medium",  # Would be calculated from actual data
            "duration": w.duration_minutes,
            "date": w.created_at
        }
        for w in recent_workouts
    ]
    
    user_history = {
        "previous_injuries": False  # Would come from user profile
    }
    
    prediction = await premium_ai.predict_injury_risk(user_history, workout_data)
    
    return {"prediction": prediction, "tier_required": "pro"}

@subscription_router.post("/ai/voice-coaching")
async def create_voice_coaching_session(
    workout_data: Dict,
    current_user: User = Depends(get_current_user)
):
    """Create AI voice coaching session (Elite feature)"""
    if not current_user.is_elite_user():
        raise HTTPException(
            status_code=403, 
            detail="This feature requires an Elite subscription"
        )
    
    user_preferences = {
        "motivation_style": "encouraging"  # Would come from user profile
    }
    
    coaching_session = await premium_ai.create_ai_voice_coaching_session(workout_data, user_preferences)
    
    return {"coaching_session": coaching_session, "tier_required": "elite"}

@subscription_router.post("/ai/ar-workout")
async def generate_ar_workout(
    exercise_request: Dict,
    current_user: User = Depends(get_current_user)
):
    """Generate AR workout overlay (Elite feature)"""
    if not current_user.is_elite_user():
        raise HTTPException(
            status_code=403, 
            detail="This feature requires an Elite subscription"
        )
    
    exercise = exercise_request.get("exercise", "squat")
    user_space = exercise_request.get("space", {"width": 2.0, "length": 2.0})
    
    ar_overlay = await premium_ai.generate_ar_workout_overlay(exercise, user_space)
    
    return {"ar_overlay": ar_overlay, "tier_required": "elite"}

@subscription_router.post("/trainer/schedule")
async def schedule_trainer_session(
    preferences: Dict,
    current_user: User = Depends(get_current_user)
):
    """Schedule personal trainer session (Elite feature)"""
    if not current_user.is_elite_user():
        raise HTTPException(
            status_code=403, 
            detail="This feature requires an Elite subscription"
        )
    
    session = await premium_ai.schedule_personal_trainer_session(str(current_user.id), preferences)
    
    return {"trainer_session": session, "tier_required": "elite"}

# ANALYTICS AND INSIGHTS

@subscription_router.get("/insights")
async def get_ai_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated insights for the user"""
    # Get insights based on user's subscription tier
    insights_query = db.query(AIInsight).filter(AIInsight.user_id == current_user.id)
    
    # Filter by tier access
    if current_user.is_elite_user():
        pass  # Elite users see all insights
    elif current_user.is_pro_user():
        insights_query = insights_query.filter(AIInsight.required_tier.in_(["premium", "pro"]))
    elif current_user.is_premium_user():
        insights_query = insights_query.filter(AIInsight.required_tier == "premium")
    else:
        # Free users get no AI insights
        return {"insights": [], "message": "Upgrade to Premium for AI insights"}
    
    insights = insights_query.order_by(AIInsight.created_at.desc()).limit(10).all()
    
    insight_data = [
        {
            "id": insight.id,
            "type": insight.insight_type,
            "title": insight.title,
            "content": json.loads(insight.content),
            "confidence": insight.confidence_score,
            "priority": insight.priority,
            "created": insight.created_at,
            "is_read": insight.is_read
        }
        for insight in insights
    ]
    
    return {"insights": insight_data}

@subscription_router.get("/usage-analytics")
async def get_usage_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get feature usage analytics for the user"""
    if not current_user.is_premium_user():
        raise HTTPException(
            status_code=403, 
            detail="This feature requires a Premium subscription or higher"
        )
    
    # Get usage stats
    usage_stats = db.query(FeatureUsage).filter(
        FeatureUsage.user_id == current_user.id
    ).all()
    
    # Aggregate by feature
    feature_counts = {}
    for usage in usage_stats:
        feature_counts[usage.feature_name] = feature_counts.get(usage.feature_name, 0) + usage.usage_count
    
    return {
        "total_features_used": len(feature_counts),
        "feature_usage": feature_counts,
        "subscription_tier": current_user.subscription_tier,
        "member_since": current_user.subscription_start
    }

# STRIPE WEBHOOKS

@subscription_router.post("/webhooks/stripe")
async def handle_stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhooks for subscription events"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_manager.webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event['type'] == 'invoice.payment_succeeded':
        # Payment succeeded - activate/renew subscription
        subscription_data = event['data']['object']
        customer_id = subscription_data.get('customer')
        
        # Find user by customer ID
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.subscription_status = "active"
            db.commit()
    
    elif event['type'] == 'invoice.payment_failed':
        # Payment failed - mark subscription as past due
        subscription_data = event['data']['object']
        customer_id = subscription_data.get('customer')
        
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.subscription_status = "past_due"
            db.commit()
    
    elif event['type'] == 'customer.subscription.deleted':
        # Subscription canceled - downgrade to free
        subscription_data = event['data']['object']
        customer_id = subscription_data.get('customer')
        
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.subscription_tier = "free"
            user.subscription_status = "canceled"
            db.commit()
    
    return {"status": "success"}