"""
Subscription Database Models
Enhanced user and subscription management for Khyrie Fitness Platform
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
from enum import Enum
import json

Base = declarative_base()

class SubscriptionStatus(Enum):
    FREE = "free"
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    TRIALING = "trialing"

class User(Base):
    """Enhanced User model with subscription support"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    
    # Subscription fields
    stripe_customer_id = Column(String, unique=True)
    subscription_tier = Column(String, default="free")  # free, premium, pro, elite
    subscription_status = Column(String, default="free")
    subscription_start = Column(DateTime)
    subscription_end = Column(DateTime)
    trial_end = Column(DateTime)
    
    # Account status
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    
    # Profile information
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    fitness_level = Column(String)  # beginner, intermediate, advanced
    fitness_goals = Column(Text)  # JSON string
    
    # Relationships
    subscriptions = relationship("Subscription", back_populates="user")
    workouts = relationship("WorkoutSession", back_populates="user")
    ai_insights = relationship("AIInsight", back_populates="user")
    
    def __repr__(self):
        return f"<User(username='{self.username}', tier='{self.subscription_tier}')>"
    
    def is_premium_user(self) -> bool:
        """Check if user has premium access"""
        return self.subscription_tier in ["premium", "pro", "elite"]
    
    def is_pro_user(self) -> bool:
        """Check if user has pro access"""
        return self.subscription_tier in ["pro", "elite"]
    
    def is_elite_user(self) -> bool:
        """Check if user has elite access"""
        return self.subscription_tier == "elite"
    
    def can_access_feature(self, feature_tier: str) -> bool:
        """Check if user can access a feature based on their tier"""
        tier_levels = {"free": 0, "premium": 1, "pro": 2, "elite": 3}
        user_level = tier_levels.get(self.subscription_tier, 0)
        required_level = tier_levels.get(feature_tier, 0)
        return user_level >= required_level

class Subscription(Base):
    """Subscription tracking and history"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Stripe information
    stripe_subscription_id = Column(String, unique=True)
    stripe_price_id = Column(String)
    stripe_invoice_id = Column(String)
    
    # Subscription details
    tier = Column(String, nullable=False)  # premium, pro, elite
    status = Column(String, default="active")  # active, canceled, past_due, etc.
    amount = Column(Integer)  # Amount in cents
    currency = Column(String, default="usd")
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    ends_at = Column(DateTime)
    canceled_at = Column(DateTime)
    trial_start = Column(DateTime)
    trial_end = Column(DateTime)
    
    # Billing
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    cancel_at_period_end = Column(Boolean, default=False)
    
    # Metadata
    subscription_metadata = Column(Text)  # JSON string for additional data
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    
    def __repr__(self):
        return f"<Subscription(user_id={self.user_id}, tier='{self.tier}', status='{self.status}')>"

class WorkoutSession(Base):
    """Enhanced workout sessions with premium features"""
    __tablename__ = "workout_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Basic workout data
    workout_name = Column(String, nullable=False)
    duration_minutes = Column(Integer)
    calories_burned = Column(Integer)
    exercises_completed = Column(Integer)
    
    # Premium features
    ai_form_analysis = Column(Text)  # JSON string - Pro/Elite feature
    injury_risk_score = Column(Float)  # Pro/Elite feature
    performance_prediction = Column(Text)  # JSON - Premium+ feature
    ai_recommendations = Column(Text)  # JSON - Premium+ feature
    
    # Timing
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="workouts")
    
    def __repr__(self):
        return f"<WorkoutSession(user_id={self.user_id}, workout='{self.workout_name}')>"

class AIInsight(Base):
    """AI-generated insights and recommendations (Premium features)"""
    __tablename__ = "ai_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Insight details
    insight_type = Column(String, nullable=False)  # form_analysis, injury_prediction, etc.
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # JSON string with detailed insights
    confidence_score = Column(Float)  # AI confidence level
    
    # Feature tier requirement
    required_tier = Column(String, default="premium")  # premium, pro, elite
    
    # Status
    is_read = Column(Boolean, default=False)
    is_actionable = Column(Boolean, default=True)
    priority = Column(String, default="medium")  # low, medium, high
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # Some insights may be time-sensitive
    
    # Relationships
    user = relationship("User", back_populates="ai_insights")
    
    def __repr__(self):
        return f"<AIInsight(user_id={self.user_id}, type='{self.insight_type}')>"

class FeatureUsage(Base):
    """Track feature usage for analytics and billing"""
    __tablename__ = "feature_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Usage details
    feature_name = Column(String, nullable=False)
    usage_count = Column(Integer, default=1)
    required_tier = Column(String)  # What tier is needed for this feature
    user_tier_at_time = Column(String)  # User's tier when they used the feature
    
    # Timing
    used_at = Column(DateTime, default=datetime.utcnow)
    date = Column(String)  # YYYY-MM-DD for daily aggregation
    
    # Metadata
    usage_metadata = Column(Text)  # JSON for additional context
    
    def __repr__(self):
        return f"<FeatureUsage(user_id={self.user_id}, feature='{self.feature_name}')>"

# Database setup
DATABASE_URL = "sqlite:///./khyrie_subscriptions.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Created subscription database tables")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Sample data for testing
def create_sample_data():
    """Create sample users and subscriptions for testing"""
    db = SessionLocal()
    
    try:
        # Sample free user
        free_user = User(
            email="free_user@example.com",
            username="free_user",
            password_hash="hashed_password",
            full_name="Free User",
            subscription_tier="free",
            fitness_level="beginner"
        )
        
        # Sample premium user
        premium_user = User(
            email="premium_user@example.com",
            username="premium_user", 
            password_hash="hashed_password",
            full_name="Premium User",
            subscription_tier="premium",
            subscription_status="active",
            subscription_start=datetime.utcnow(),
            subscription_end=datetime.utcnow() + timedelta(days=30),
            fitness_level="intermediate"
        )
        
        db.add_all([free_user, premium_user])
        db.commit()
        print("✅ Created sample users")
        
    except Exception as e:
        print(f"ℹ️  Sample data might already exist: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    create_sample_data()