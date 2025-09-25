"""
Khyrie Fitness Platform - Subscription Management System
Copyright (C) 2025 Darnell Roy

Licensed under the Commercial License for premium features.
See LICENSE file for details.
"""

import stripe
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from fastapi import HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
logger = logging.getLogger(__name__)

Base = declarative_base()

class UserSubscription(Base):
    """User subscription model."""
    __tablename__ = "user_subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    plan_type = Column(String(20), nullable=False)  # 'free', 'premium', 'pro', 'elite'
    stripe_subscription_id = Column(String(255), unique=True)
    stripe_customer_id = Column(String(255))
    status = Column(String(20), default='active')  # 'active', 'cancelled', 'past_due'
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    trial_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PaymentHistory(Base):
    """Payment history model."""
    __tablename__ = "payment_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    subscription_id = Column(Integer, nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default='USD')
    stripe_payment_id = Column(String(255), unique=True)
    status = Column(String(20))  # 'succeeded', 'failed', 'pending'
    created_at = Column(DateTime, default=datetime.utcnow)

class FeatureUsage(Base):
    """Feature usage tracking model."""
    __tablename__ = "feature_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    feature_name = Column(String(100), nullable=False)
    usage_count = Column(Integer, default=1)
    monthly_limit = Column(Integer, nullable=True)
    last_used = Column(DateTime, default=datetime.utcnow)
    reset_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class SubscriptionManager:
    """Manages subscription operations and feature access."""
    
    # Plan definitions with features and limits
    PLANS = {
        'free': {
            'price': 0,
            'stripe_price_id': None,
            'features': {
                'basic_tracking': True,
                'exercise_library_limit': 50,
                'family_members_limit': 3,
                'ai_recommendations_limit': 0,
                'form_analysis': False,
                'injury_prevention': False,
                'ai_coach': False,
                'custom_workouts': False
            },
            'monthly_limits': {
                'workout_generations': 0,
                'ai_conversations': 0,
                'form_analyses': 0
            }
        },
        'premium': {
            'price': 999,  # $9.99 in cents
            'stripe_price_id': os.getenv('STRIPE_PREMIUM_PRICE_ID'),
            'features': {
                'basic_tracking': True,
                'exercise_library_limit': 500,
                'family_members_limit': 10,
                'ai_recommendations': True,
                'custom_meal_plans': True,
                'advanced_analytics': True,
                'priority_support': True,
                'form_analysis': False,
                'injury_prevention': False,
                'ai_coach': False
            },
            'monthly_limits': {
                'workout_generations': 30,
                'ai_conversations': 0,
                'form_analyses': 0
            }
        },
        'pro': {
            'price': 1999,  # $19.99 in cents
            'stripe_price_id': os.getenv('STRIPE_PRO_PRICE_ID'),
            'features': {
                'basic_tracking': True,
                'exercise_library_limit': -1,  # Unlimited
                'family_members_limit': -1,    # Unlimited
                'ai_recommendations': True,
                'custom_meal_plans': True,
                'advanced_analytics': True,
                'priority_support': True,
                'form_analysis': True,
                'injury_prevention': True,
                'wearable_integration': True,
                'api_access': True,
                'ai_coach': False
            },
            'monthly_limits': {
                'workout_generations': 100,
                'ai_conversations': 0,
                'form_analyses': 50
            }
        },
        'elite': {
            'price': 3999,  # $39.99 in cents
            'stripe_price_id': os.getenv('STRIPE_ELITE_PRICE_ID'),
            'features': {
                'basic_tracking': True,
                'exercise_library_limit': -1,  # Unlimited
                'family_members_limit': -1,    # Unlimited
                'ai_recommendations': True,
                'custom_meal_plans': True,
                'advanced_analytics': True,
                'priority_support': True,
                'form_analysis': True,
                'injury_prevention': True,
                'wearable_integration': True,
                'api_access': True,
                'ai_coach': True,
                'ar_vr_workouts': True,
                'trainer_sessions': True,
                'white_label': True
            },
            'monthly_limits': {
                'workout_generations': -1,  # Unlimited
                'ai_conversations': -1,     # Unlimited
                'form_analyses': -1         # Unlimited
            }
        }
    }
    
    def __init__(self, db_session):
        self.db = db_session
    
    async def create_subscription(self, user_id: int, plan_type: str, 
                                payment_method_id: str, user_email: str) -> Dict[str, Any]:
        """Create a new subscription with Stripe."""
        try:
            if plan_type not in self.PLANS:
                raise ValueError(f"Invalid plan type: {plan_type}")
            
            plan = self.PLANS[plan_type]
            
            if plan_type == 'free':
                # Handle free plan without Stripe
                return await self._create_free_subscription(user_id)
            
            # Create Stripe customer
            customer = stripe.Customer.create(
                payment_method=payment_method_id,
                email=user_email,
                invoice_settings={'default_payment_method': payment_method_id},
                metadata={'user_id': str(user_id)}
            )
            
            # Create subscription with 7-day trial for premium plans
            subscription_params = {
                'customer': customer.id,
                'items': [{'price': plan['stripe_price_id']}],
                'trial_period_days': 7,
                'expand': ['latest_invoice.payment_intent'],
                'metadata': {'user_id': str(user_id), 'plan_type': plan_type}
            }
            
            subscription = stripe.Subscription.create(**subscription_params)
            
            # Save subscription to database
            db_subscription = UserSubscription(
                user_id=user_id,
                plan_type=plan_type,
                stripe_subscription_id=subscription.id,
                stripe_customer_id=customer.id,
                status=subscription.status,
                current_period_start=datetime.fromtimestamp(subscription.current_period_start),
                current_period_end=datetime.fromtimestamp(subscription.current_period_end),
                trial_end=datetime.fromtimestamp(subscription.trial_end) if subscription.trial_end else None
            )
            
            self.db.add(db_subscription)
            self.db.commit()
            
            logger.info(f"Created subscription for user {user_id}, plan: {plan_type}")
            
            return {
                'subscription_id': subscription.id,
                'status': subscription.status,
                'trial_end': subscription.trial_end,
                'current_period_end': subscription.current_period_end,
                'plan_type': plan_type
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating subscription: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Payment processing error: {str(e)}")
        except Exception as e:
            logger.error(f"Error creating subscription: {str(e)}")
            raise HTTPException(status_code=500, detail="Subscription creation failed")
    
    async def _create_free_subscription(self, user_id: int) -> Dict[str, Any]:
        """Create a free tier subscription."""
        db_subscription = UserSubscription(
            user_id=user_id,
            plan_type='free',
            status='active',
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=365)  # Free for a year
        )
        
        self.db.add(db_subscription)
        self.db.commit()
        
        return {
            'subscription_id': None,
            'status': 'active',
            'plan_type': 'free'
        }
    
    async def check_feature_access(self, user_id: int, feature_name: str) -> Dict[str, Any]:
        """Check if user has access to a specific feature."""
        subscription = self.db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status == 'active'
        ).first()
        
        if not subscription:
            # Default to free plan
            plan_features = self.PLANS['free']['features']
            plan_type = 'free'
        else:
            plan_features = self.PLANS[subscription.plan_type]['features']
            plan_type = subscription.plan_type
        
        has_feature = plan_features.get(feature_name, False)
        
        # Check usage limits for premium features
        usage_info = await self._check_usage_limits(user_id, feature_name, plan_type)
        
        return {
            'has_access': has_feature and usage_info['within_limits'],
            'plan_type': plan_type,
            'usage_info': usage_info,
            'upgrade_required': not has_feature
        }
    
    async def _check_usage_limits(self, user_id: int, feature_name: str, plan_type: str) -> Dict[str, Any]:
        """Check if user is within usage limits for a feature."""
        plan_limits = self.PLANS[plan_type]['monthly_limits']
        
        # Get usage tracking for this month
        current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        usage_record = self.db.query(FeatureUsage).filter(
            FeatureUsage.user_id == user_id,
            FeatureUsage.feature_name == feature_name,
            FeatureUsage.reset_date >= current_month
        ).first()
        
        current_usage = usage_record.usage_count if usage_record else 0
        monthly_limit = plan_limits.get(feature_name, 0)
        
        # -1 means unlimited
        within_limits = monthly_limit == -1 or current_usage < monthly_limit
        
        return {
            'current_usage': current_usage,
            'monthly_limit': monthly_limit,
            'within_limits': within_limits,
            'unlimited': monthly_limit == -1
        }
    
    async def track_feature_usage(self, user_id: int, feature_name: str) -> None:
        """Track usage of a premium feature."""
        current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = (current_month + timedelta(days=32)).replace(day=1)
        
        usage_record = self.db.query(FeatureUsage).filter(
            FeatureUsage.user_id == user_id,
            FeatureUsage.feature_name == feature_name,
            FeatureUsage.reset_date >= current_month
        ).first()
        
        if usage_record:
            usage_record.usage_count += 1
            usage_record.last_used = datetime.utcnow()
        else:
            usage_record = FeatureUsage(
                user_id=user_id,
                feature_name=feature_name,
                usage_count=1,
                reset_date=next_month,
                last_used=datetime.utcnow()
            )
            self.db.add(usage_record)
        
        self.db.commit()
    
    async def get_subscription_status(self, user_id: int) -> Dict[str, Any]:
        """Get detailed subscription status for a user."""
        subscription = self.db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status == 'active'
        ).first()
        
        if not subscription:
            return {
                'plan_type': 'free',
                'status': 'active',
                'features': self.PLANS['free']['features'],
                'monthly_limits': self.PLANS['free']['monthly_limits']
            }
        
        plan = self.PLANS[subscription.plan_type]
        
        return {
            'plan_type': subscription.plan_type,
            'status': subscription.status,
            'current_period_end': subscription.current_period_end,
            'trial_end': subscription.trial_end,
            'features': plan['features'],
            'monthly_limits': plan['monthly_limits'],
            'stripe_subscription_id': subscription.stripe_subscription_id
        }
    
    async def cancel_subscription(self, user_id: int) -> Dict[str, Any]:
        """Cancel a user's subscription."""
        subscription = self.db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status == 'active'
        ).first()
        
        if not subscription or subscription.plan_type == 'free':
            raise HTTPException(status_code=404, detail="No active subscription found")
        
        try:
            # Cancel in Stripe
            stripe.Subscription.modify(
                subscription.stripe_subscription_id,
                cancel_at_period_end=True
            )
            
            # Update database
            subscription.status = 'cancelled'
            subscription.updated_at = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Cancelled subscription for user {user_id}")
            
            return {
                'success': True,
                'message': 'Subscription will be cancelled at the end of the current period',
                'current_period_end': subscription.current_period_end
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error cancelling subscription: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Cancellation failed: {str(e)}")
    
    async def handle_webhook_event(self, event: Dict[str, Any]) -> None:
        """Handle Stripe webhook events."""
        event_type = event['type']
        data = event['data']['object']
        
        if event_type == 'invoice.payment_succeeded':
            await self._handle_successful_payment(data)
        elif event_type == 'invoice.payment_failed':
            await self._handle_failed_payment(data)
        elif event_type == 'customer.subscription.deleted':
            await self._handle_subscription_deleted(data)
        elif event_type == 'customer.subscription.updated':
            await self._handle_subscription_updated(data)
    
    async def _handle_successful_payment(self, invoice: Dict[str, Any]) -> None:
        """Handle successful payment webhook."""
        subscription_id = invoice['subscription']
        amount = invoice['amount_paid']
        
        # Find subscription in database
        subscription = self.db.query(UserSubscription).filter(
            UserSubscription.stripe_subscription_id == subscription_id
        ).first()
        
        if subscription:
            # Record payment
            payment = PaymentHistory(
                user_id=subscription.user_id,
                subscription_id=subscription.id,
                amount=amount / 100,  # Convert cents to dollars
                stripe_payment_id=invoice['payment_intent'],
                status='succeeded'
            )
            self.db.add(payment)
            self.db.commit()
            
            logger.info(f"Payment succeeded for user {subscription.user_id}, amount: ${amount/100}")
    
    async def _handle_failed_payment(self, invoice: Dict[str, Any]) -> None:
        """Handle failed payment webhook."""
        subscription_id = invoice['subscription']
        
        subscription = self.db.query(UserSubscription).filter(
            UserSubscription.stripe_subscription_id == subscription_id
        ).first()
        
        if subscription:
            subscription.status = 'past_due'
            self.db.commit()
            
            logger.warning(f"Payment failed for user {subscription.user_id}")
    
    async def _handle_subscription_deleted(self, subscription_data: Dict[str, Any]) -> None:
        """Handle subscription deletion webhook."""
        subscription_id = subscription_data['id']
        
        subscription = self.db.query(UserSubscription).filter(
            UserSubscription.stripe_subscription_id == subscription_id
        ).first()
        
        if subscription:
            subscription.status = 'cancelled'
            self.db.commit()
            
            logger.info(f"Subscription deleted for user {subscription.user_id}")