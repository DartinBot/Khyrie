"""
Stripe Subscription Management System
Handles premium subscriptions, billing, and feature access for Khyrie Fitness Platform
"""

import os
import stripe
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from dotenv import load_dotenv
from enum import Enum

# Load environment variables
load_dotenv()

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class SubscriptionTier(Enum):
    FREE = "free"
    PREMIUM = "premium"  # $9.99/month
    PRO = "pro"         # $19.99/month
    ELITE = "elite"     # $39.99/month

class StripeManager:
    """Manages all Stripe operations for subscriptions and payments"""
    
    def __init__(self):
        self.stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
        self.stripe_publishable_key = os.getenv("STRIPE_PUBLISHABLE_KEY")
        self.webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        
        # Subscription pricing (in cents)
        self.pricing_plans = {
            SubscriptionTier.FREE: {
                "price": 0,
                "price_id": None,
                "features": [
                    "Basic workout tracking",
                    "Exercise library (limited to 50 exercises)",
                    "Family group (up to 3 members)",
                    "Basic progress charts",
                    "Community features"
                ]
            },
            SubscriptionTier.PREMIUM: {
                "price": 999,  # $9.99
                "price_id": "price_premium_monthly",
                "features": [
                    "AI-powered workout recommendations",
                    "Advanced progress analytics",
                    "Unlimited family members",
                    "Full exercise library (500+ exercises)",
                    "Custom meal plans",
                    "Priority support",
                    "Workout form analysis",
                    "Progress predictions"
                ]
            },
            SubscriptionTier.PRO: {
                "price": 1999,  # $19.99
                "price_id": "price_pro_monthly",
                "features": [
                    "Everything in Premium +",
                    "Real-time form analysis",
                    "Predictive injury prevention",
                    "Advanced AI coaching",
                    "Wearable device integration",
                    "API access for developers",
                    "Custom workout AI generation",
                    "Biometric trend analysis",
                    "Nutrition AI recommendations"
                ]
            },
            SubscriptionTier.ELITE: {
                "price": 3999,  # $39.99
                "price_id": "price_elite_monthly",
                "features": [
                    "Everything in Pro +",
                    "Personal AI coach with voice guidance",
                    "AR/VR workout experiences",
                    "One-on-one trainer sessions (2/month)",
                    "Advanced biometric tracking",
                    "White-label licensing",
                    "Priority feature requests",
                    "24/7 AI health monitoring",
                    "Custom app branding"
                ]
            }
        }
    
    async def create_stripe_products(self):
        """Create Stripe products and prices for subscription tiers"""
        try:
            products_created = []
            
            for tier, details in self.pricing_plans.items():
                if tier == SubscriptionTier.FREE:
                    continue
                    
                # Create product
                product = stripe.Product.create(
                    name=f"Khyrie {tier.value.title()}",
                    description=f"Khyrie Fitness Platform - {tier.value.title()} Plan",
                    metadata={
                        "tier": tier.value,
                        "features": ", ".join(details["features"][:3])  # First 3 features
                    }
                )
                
                # Create price
                price = stripe.Price.create(
                    unit_amount=details["price"],
                    currency="usd",
                    recurring={"interval": "month"},
                    product=product.id,
                    metadata={"tier": tier.value}
                )
                
                products_created.append({
                    "tier": tier.value,
                    "product_id": product.id,
                    "price_id": price.id,
                    "amount": details["price"]
                })
                
                print(f"✅ Created Stripe product: {tier.value.title()} - ${details['price']/100:.2f}/month")
            
            return products_created
            
        except Exception as e:
            print(f"❌ Error creating Stripe products: {str(e)}")
            return None
    
    async def create_customer(self, user_id: str, email: str, name: str = None) -> Optional[str]:
        """Create a Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={"user_id": user_id}
            )
            return customer.id
        except Exception as e:
            print(f"❌ Error creating Stripe customer: {str(e)}")
            return None
    
    async def create_subscription(self, customer_id: str, price_id: str) -> Optional[Dict]:
        """Create a new subscription"""
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                payment_behavior="default_incomplete",
                payment_settings={"save_default_payment_method": "on_subscription"},
                expand=["latest_invoice.payment_intent"],
            )
            
            return {
                "subscription_id": subscription.id,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret,
                "status": subscription.status
            }
        except Exception as e:
            print(f"❌ Error creating subscription: {str(e)}")
            return None
    
    async def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancel a subscription"""
        try:
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
            return True
        except Exception as e:
            print(f"❌ Error canceling subscription: {str(e)}")
            return False
    
    async def get_subscription_status(self, customer_id: str) -> Optional[Dict]:
        """Get current subscription status for a customer"""
        try:
            subscriptions = stripe.Subscription.list(
                customer=customer_id,
                status="all",
                limit=1
            )
            
            if subscriptions.data:
                sub = subscriptions.data[0]
                return {
                    "subscription_id": sub.id,
                    "status": sub.status,
                    "current_period_end": sub.current_period_end,
                    "cancel_at_period_end": sub.cancel_at_period_end,
                    "price_id": sub.items.data[0].price.id if sub.items.data else None
                }
            return None
            
        except Exception as e:
            print(f"❌ Error getting subscription status: {str(e)}")
            return None
    
    def get_tier_from_price_id(self, price_id: str) -> SubscriptionTier:
        """Determine subscription tier from Stripe price ID"""
        for tier, details in self.pricing_plans.items():
            if details.get("price_id") == price_id:
                return tier
        return SubscriptionTier.FREE
    
    def get_features_for_tier(self, tier: SubscriptionTier) -> List[str]:
        """Get list of features for a subscription tier"""
        return self.pricing_plans[tier]["features"]
    
    def can_access_feature(self, user_tier: SubscriptionTier, required_tier: SubscriptionTier) -> bool:
        """Check if user's tier allows access to a feature"""
        tier_hierarchy = {
            SubscriptionTier.FREE: 0,
            SubscriptionTier.PREMIUM: 1,
            SubscriptionTier.PRO: 2,
            SubscriptionTier.ELITE: 3
        }
        return tier_hierarchy[user_tier] >= tier_hierarchy[required_tier]

# Global instance
stripe_manager = StripeManager()

# Feature access decorators
def requires_premium(func):
    """Decorator to restrict access to premium features"""
    async def wrapper(*args, **kwargs):
        # This would check user's subscription in practice
        return await func(*args, **kwargs)
    return wrapper

def requires_pro(func):
    """Decorator to restrict access to pro features"""
    async def wrapper(*args, **kwargs):
        # This would check user's subscription in practice
        return await func(*args, **kwargs)
    return wrapper

def requires_elite(func):
    """Decorator to restrict access to elite features"""
    async def wrapper(*args, **kwargs):
        # This would check user's subscription in practice
        return await func(*args, **kwargs)
    return wrapper