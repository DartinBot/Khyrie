"""
Khyrie Fitness - Trainer Marketplace System
Complete platform for personal trainers to join, monetize services, and manage their fitness business
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from enum import Enum
from dataclasses import dataclass, asdict
import sqlite3
import json
import uuid
from decimal import Decimal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrainerStatus(Enum):
    PENDING = "pending"              # Application submitted, under review
    VERIFIED = "verified"            # Background check and certification verified
    ACTIVE = "active"               # Approved and actively taking clients
    INACTIVE = "inactive"           # Temporarily not taking clients
    SUSPENDED = "suspended"         # Platform suspended for violations
    REJECTED = "rejected"           # Application rejected

class CertificationType(Enum):
    PERSONAL_TRAINER = "personal_trainer"
    NUTRITIONIST = "nutritionist"
    YOGA_INSTRUCTOR = "yoga_instructor"
    STRENGTH_COACH = "strength_coach"
    CARDIO_SPECIALIST = "cardio_specialist"
    REHABILITATION = "rehabilitation"
    SPORTS_SPECIFIC = "sports_specific"
    GROUP_FITNESS = "group_fitness"
    WELLNESS_COACH = "wellness_coach"

class ServiceType(Enum):
    PERSONAL_TRAINING = "personal_training"
    GROUP_CLASS = "group_class"
    NUTRITION_COACHING = "nutrition_coaching"
    ONLINE_CONSULTATION = "online_consultation"
    PROGRAM_DESIGN = "program_design"
    FORM_ANALYSIS = "form_analysis"
    WELLNESS_COACHING = "wellness_coaching"
    SPECIALIZED_TRAINING = "specialized_training"

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

@dataclass
class TrainerProfile:
    trainer_id: str
    user_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    bio: str
    experience_years: int
    hourly_rate_min: float
    hourly_rate_max: float
    specializations: List[str]
    certifications: List[Dict]
    languages: List[str]
    availability_schedule: Dict
    profile_image_url: Optional[str] = None
    status: TrainerStatus = TrainerStatus.PENDING
    rating: float = 0.0
    total_reviews: int = 0
    total_sessions: int = 0
    total_earnings: float = 0.0
    commission_rate: float = 0.15  # 15% platform commission
    created_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None
    last_active: Optional[datetime] = None

@dataclass
class TrainerService:
    service_id: str
    trainer_id: str
    service_type: ServiceType
    title: str
    description: str
    duration_minutes: int
    price: float
    max_participants: int = 1  # 1 for personal, >1 for group
    requirements: Optional[str] = None
    equipment_needed: List[str] = None
    online_available: bool = True
    in_person_available: bool = True
    location_radius_km: int = 10
    is_active: bool = True
    created_at: Optional[datetime] = None

@dataclass
class TrainerBooking:
    booking_id: str
    client_user_id: str
    trainer_id: str
    service_id: str
    session_date: datetime
    duration_minutes: int
    total_price: float
    platform_fee: float
    trainer_earnings: float
    payment_status: PaymentStatus = PaymentStatus.PENDING
    session_notes: Optional[str] = None
    client_rating: Optional[int] = None
    client_review: Optional[str] = None
    trainer_notes: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class TrainerMarketplace:
    def __init__(self, db_path: str = "trainer_marketplace.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the trainer marketplace database with all required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Trainer Profiles Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trainer_profiles (
                    trainer_id TEXT PRIMARY KEY,
                    user_id TEXT UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    bio TEXT,
                    experience_years INTEGER DEFAULT 0,
                    hourly_rate_min REAL DEFAULT 50.0,
                    hourly_rate_max REAL DEFAULT 150.0,
                    specializations TEXT, -- JSON array
                    certifications TEXT, -- JSON array of certification objects
                    languages TEXT, -- JSON array
                    availability_schedule TEXT, -- JSON object
                    profile_image_url TEXT,
                    status TEXT DEFAULT 'pending',
                    rating REAL DEFAULT 0.0,
                    total_reviews INTEGER DEFAULT 0,
                    total_sessions INTEGER DEFAULT 0,
                    total_earnings REAL DEFAULT 0.0,
                    commission_rate REAL DEFAULT 0.15,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    verified_at TIMESTAMP,
                    last_active TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users_enhanced(user_id)
                )
            """)
            
            # Trainer Services Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trainer_services (
                    service_id TEXT PRIMARY KEY,
                    trainer_id TEXT NOT NULL,
                    service_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    duration_minutes INTEGER NOT NULL,
                    price REAL NOT NULL,
                    max_participants INTEGER DEFAULT 1,
                    requirements TEXT,
                    equipment_needed TEXT, -- JSON array
                    online_available BOOLEAN DEFAULT TRUE,
                    in_person_available BOOLEAN DEFAULT TRUE,
                    location_radius_km INTEGER DEFAULT 10,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (trainer_id) REFERENCES trainer_profiles(trainer_id)
                )
            """)
            
            # Trainer Bookings Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trainer_bookings (
                    booking_id TEXT PRIMARY KEY,
                    client_user_id TEXT NOT NULL,
                    trainer_id TEXT NOT NULL,
                    service_id TEXT NOT NULL,
                    session_date TIMESTAMP NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    total_price REAL NOT NULL,
                    platform_fee REAL NOT NULL,
                    trainer_earnings REAL NOT NULL,
                    payment_status TEXT DEFAULT 'pending',
                    session_notes TEXT,
                    client_rating INTEGER,
                    client_review TEXT,
                    trainer_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (client_user_id) REFERENCES users_enhanced(user_id),
                    FOREIGN KEY (trainer_id) REFERENCES trainer_profiles(trainer_id),
                    FOREIGN KEY (service_id) REFERENCES trainer_services(service_id)
                )
            """)
            
            # Trainer Earnings Table (for detailed financial tracking)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trainer_earnings (
                    earning_id TEXT PRIMARY KEY,
                    trainer_id TEXT NOT NULL,
                    booking_id TEXT,
                    earning_type TEXT NOT NULL, -- 'session', 'bonus', 'adjustment'
                    amount REAL NOT NULL,
                    platform_fee REAL DEFAULT 0.0,
                    net_amount REAL NOT NULL,
                    payment_date TIMESTAMP,
                    payment_method TEXT,
                    transaction_id TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (trainer_id) REFERENCES trainer_profiles(trainer_id),
                    FOREIGN KEY (booking_id) REFERENCES trainer_bookings(booking_id)
                )
            """)
            
            # Trainer Reviews Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trainer_reviews (
                    review_id TEXT PRIMARY KEY,
                    trainer_id TEXT NOT NULL,
                    client_user_id TEXT NOT NULL,
                    booking_id TEXT,
                    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                    review_text TEXT,
                    is_verified BOOLEAN DEFAULT FALSE,
                    is_public BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (trainer_id) REFERENCES trainer_profiles(trainer_id),
                    FOREIGN KEY (client_user_id) REFERENCES users_enhanced(user_id),
                    FOREIGN KEY (booking_id) REFERENCES trainer_bookings(booking_id)
                )
            """)
            
            # Trainer Certifications Table (for detailed certification tracking)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trainer_certifications (
                    certification_id TEXT PRIMARY KEY,
                    trainer_id TEXT NOT NULL,
                    certification_type TEXT NOT NULL,
                    certification_name TEXT NOT NULL,
                    issuing_organization TEXT NOT NULL,
                    issue_date DATE,
                    expiry_date DATE,
                    certificate_url TEXT,
                    verification_status TEXT DEFAULT 'pending',
                    verified_at TIMESTAMP,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (trainer_id) REFERENCES trainer_profiles(trainer_id)
                )
            """)
            
            # Create indices for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_trainer_status ON trainer_profiles(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_trainer_rating ON trainer_profiles(rating DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_service_type ON trainer_services(service_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_booking_date ON trainer_bookings(session_date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_booking_status ON trainer_bookings(payment_status)")
            
            conn.commit()
            conn.close()
            logger.info("✅ Trainer marketplace database initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error initializing trainer marketplace database: {e}")
            raise

    def register_trainer(self, trainer_data: Dict) -> Dict:
        """Register a new trainer with the platform"""
        try:
            trainer_id = f"trainer_{uuid.uuid4().hex[:12]}"
            
            # Validate required fields
            required_fields = ['user_id', 'first_name', 'last_name', 'email', 'bio', 'experience_years']
            for field in required_fields:
                if field not in trainer_data:
                    return {"success": False, "error": f"Missing required field: {field}"}
            
            trainer = TrainerProfile(
                trainer_id=trainer_id,
                user_id=trainer_data['user_id'],
                first_name=trainer_data['first_name'],
                last_name=trainer_data['last_name'],
                email=trainer_data['email'],
                phone=trainer_data.get('phone', ''),
                bio=trainer_data['bio'],
                experience_years=trainer_data['experience_years'],
                hourly_rate_min=trainer_data.get('hourly_rate_min', 50.0),
                hourly_rate_max=trainer_data.get('hourly_rate_max', 150.0),
                specializations=trainer_data.get('specializations', []),
                certifications=trainer_data.get('certifications', []),
                languages=trainer_data.get('languages', ['English']),
                availability_schedule=trainer_data.get('availability_schedule', {}),
                profile_image_url=trainer_data.get('profile_image_url'),
                created_at=datetime.now()
            )
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert trainer profile
            cursor.execute("""
                INSERT INTO trainer_profiles 
                (trainer_id, user_id, first_name, last_name, email, phone, bio, 
                 experience_years, hourly_rate_min, hourly_rate_max, specializations, 
                 certifications, languages, availability_schedule, profile_image_url, 
                 status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                trainer.trainer_id, trainer.user_id, trainer.first_name, trainer.last_name,
                trainer.email, trainer.phone, trainer.bio, trainer.experience_years,
                trainer.hourly_rate_min, trainer.hourly_rate_max,
                json.dumps(trainer.specializations), json.dumps(trainer.certifications),
                json.dumps(trainer.languages), json.dumps(trainer.availability_schedule),
                trainer.profile_image_url, trainer.status.value, trainer.created_at
            ))
            
            # Add certifications if provided
            if trainer_data.get('certifications'):
                for cert in trainer_data['certifications']:
                    self._add_certification(cursor, trainer_id, cert)
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "trainer_id": trainer_id,
                "status": "pending",
                "message": "Trainer application submitted successfully. Our team will review your application and certifications within 2-3 business days.",
                "next_steps": [
                    "Upload required certifications",
                    "Complete background verification",
                    "Set up payment details",
                    "Create your first service offerings"
                ]
            }
            
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: trainer_profiles.email" in str(e):
                return {"success": False, "error": "Email already registered as a trainer"}
            elif "UNIQUE constraint failed: trainer_profiles.user_id" in str(e):
                return {"success": False, "error": "User already has a trainer profile"}
            else:
                return {"success": False, "error": f"Database constraint error: {e}"}
        except Exception as e:
            logger.error(f"Error registering trainer: {e}")
            return {"success": False, "error": str(e)}

    def _add_certification(self, cursor, trainer_id: str, cert_data: Dict):
        """Add a certification for a trainer"""
        cert_id = f"cert_{uuid.uuid4().hex[:12]}"
        cursor.execute("""
            INSERT INTO trainer_certifications
            (certification_id, trainer_id, certification_type, certification_name,
             issuing_organization, issue_date, expiry_date, certificate_url, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cert_id, trainer_id, cert_data.get('type', 'personal_trainer'),
            cert_data.get('name', ''), cert_data.get('organization', ''),
            cert_data.get('issue_date'), cert_data.get('expiry_date'),
            cert_data.get('certificate_url'), datetime.now()
        ))

    def create_service(self, service_data: Dict) -> Dict:
        """Create a new service offering for a trainer"""
        try:
            service_id = f"service_{uuid.uuid4().hex[:12]}"
            
            required_fields = ['trainer_id', 'service_type', 'title', 'description', 'duration_minutes', 'price']
            for field in required_fields:
                if field not in service_data:
                    return {"success": False, "error": f"Missing required field: {field}"}
            
            service = TrainerService(
                service_id=service_id,
                trainer_id=service_data['trainer_id'],
                service_type=ServiceType(service_data['service_type']),
                title=service_data['title'],
                description=service_data['description'],
                duration_minutes=service_data['duration_minutes'],
                price=service_data['price'],
                max_participants=service_data.get('max_participants', 1),
                requirements=service_data.get('requirements'),
                equipment_needed=service_data.get('equipment_needed', []),
                online_available=service_data.get('online_available', True),
                in_person_available=service_data.get('in_person_available', True),
                location_radius_km=service_data.get('location_radius_km', 10),
                created_at=datetime.now()
            )
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO trainer_services
                (service_id, trainer_id, service_type, title, description, duration_minutes,
                 price, max_participants, requirements, equipment_needed, online_available,
                 in_person_available, location_radius_km, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                service.service_id, service.trainer_id, service.service_type.value,
                service.title, service.description, service.duration_minutes,
                service.price, service.max_participants, service.requirements,
                json.dumps(service.equipment_needed), service.online_available,
                service.in_person_available, service.location_radius_km, service.created_at
            ))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "service_id": service_id,
                "message": "Service created successfully",
                "service_preview": {
                    "title": service.title,
                    "price": service.price,
                    "duration": service.duration_minutes,
                    "type": service.service_type.value
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating service: {e}")
            return {"success": False, "error": str(e)}

    def search_trainers(self, search_params: Dict) -> Dict:
        """Search for trainers based on various criteria"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build dynamic search query
            where_conditions = ["tp.status = 'active'"]
            params = []
            
            if search_params.get('specialization'):
                where_conditions.append("tp.specializations LIKE ?")
                params.append(f"%{search_params['specialization']}%")
            
            if search_params.get('service_type'):
                where_conditions.append("ts.service_type = ?")
                params.append(search_params['service_type'])
            
            if search_params.get('max_price'):
                where_conditions.append("tp.hourly_rate_min <= ?")
                params.append(search_params['max_price'])
            
            if search_params.get('min_rating'):
                where_conditions.append("tp.rating >= ?")
                params.append(search_params['min_rating'])
            
            if search_params.get('online_only'):
                where_conditions.append("ts.online_available = TRUE")
            
            if search_params.get('in_person_only'):
                where_conditions.append("ts.in_person_available = TRUE")
            
            # Order by preference
            order_by = "tp.rating DESC, tp.total_reviews DESC, tp.created_at DESC"
            if search_params.get('sort_by') == 'price_low':
                order_by = "tp.hourly_rate_min ASC"
            elif search_params.get('sort_by') == 'experience':
                order_by = "tp.experience_years DESC"
            
            query = f"""
                SELECT DISTINCT tp.trainer_id, tp.first_name, tp.last_name, tp.bio, 
                       tp.experience_years, tp.hourly_rate_min, tp.hourly_rate_max,
                       tp.specializations, tp.rating, tp.total_reviews, tp.total_sessions,
                       tp.profile_image_url, tp.languages
                FROM trainer_profiles tp
                LEFT JOIN trainer_services ts ON tp.trainer_id = ts.trainer_id
                WHERE {' AND '.join(where_conditions)}
                ORDER BY {order_by}
                LIMIT ?
            """
            
            limit = search_params.get('limit', 20)
            params.append(limit)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            trainers = []
            for row in results:
                trainer = {
                    "trainer_id": row[0],
                    "name": f"{row[1]} {row[2]}",
                    "bio": row[3],
                    "experience_years": row[4],
                    "hourly_rate_range": f"${row[5]}-${row[6]}",
                    "specializations": json.loads(row[7] or "[]"),
                    "rating": row[8],
                    "total_reviews": row[9],
                    "total_sessions": row[10],
                    "profile_image_url": row[11],
                    "languages": json.loads(row[12] or '["English"]'),
                    "availability_preview": "Available this week"  # TODO: Calculate from schedule
                }
                trainers.append(trainer)
            
            conn.close()
            
            return {
                "success": True,
                "total_found": len(trainers),
                "trainers": trainers,
                "search_filters_applied": len([k for k, v in search_params.items() if v])
            }
            
        except Exception as e:
            logger.error(f"Error searching trainers: {e}")
            return {"success": False, "error": str(e)}

    def book_session(self, booking_data: Dict) -> Dict:
        """Book a training session with a trainer"""
        try:
            booking_id = f"booking_{uuid.uuid4().hex[:12]}"
            
            required_fields = ['client_user_id', 'trainer_id', 'service_id', 'session_date']
            for field in required_fields:
                if field not in booking_data:
                    return {"success": False, "error": f"Missing required field: {field}"}
            
            # Get service details for pricing
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT ts.price, ts.duration_minutes, tp.commission_rate
                FROM trainer_services ts
                JOIN trainer_profiles tp ON ts.trainer_id = tp.trainer_id
                WHERE ts.service_id = ?
            """, (booking_data['service_id'],))
            
            service_info = cursor.fetchone()
            if not service_info:
                return {"success": False, "error": "Service not found"}
            
            total_price = float(service_info[0])
            duration_minutes = service_info[1]
            commission_rate = service_info[2]
            platform_fee = total_price * commission_rate
            trainer_earnings = total_price - platform_fee
            
            booking = TrainerBooking(
                booking_id=booking_id,
                client_user_id=booking_data['client_user_id'],
                trainer_id=booking_data['trainer_id'],
                service_id=booking_data['service_id'],
                session_date=datetime.fromisoformat(booking_data['session_date'].replace('Z', '+00:00')),
                duration_minutes=duration_minutes,
                total_price=total_price,
                platform_fee=platform_fee,
                trainer_earnings=trainer_earnings,
                session_notes=booking_data.get('session_notes'),
                created_at=datetime.now()
            )
            
            cursor.execute("""
                INSERT INTO trainer_bookings
                (booking_id, client_user_id, trainer_id, service_id, session_date,
                 duration_minutes, total_price, platform_fee, trainer_earnings,
                 payment_status, session_notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                booking.booking_id, booking.client_user_id, booking.trainer_id,
                booking.service_id, booking.session_date, booking.duration_minutes,
                booking.total_price, booking.platform_fee, booking.trainer_earnings,
                booking.payment_status.value, booking.session_notes, booking.created_at
            ))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "booking_id": booking_id,
                "total_price": total_price,
                "platform_fee": platform_fee,
                "trainer_earnings": trainer_earnings,
                "session_details": {
                    "date": booking.session_date.isoformat(),
                    "duration_minutes": duration_minutes,
                    "payment_status": "pending"
                },
                "message": "Session booked successfully! Please complete payment to confirm.",
                "next_steps": [
                    "Complete payment",
                    "Receive trainer contact information",
                    "Join session at scheduled time"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error booking session: {e}")
            return {"success": False, "error": str(e)}

    def get_trainer_dashboard(self, trainer_id: str) -> Dict:
        """Get comprehensive dashboard data for a trainer"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get trainer profile
            cursor.execute("""
                SELECT first_name, last_name, status, rating, total_reviews, 
                       total_sessions, total_earnings, created_at
                FROM trainer_profiles WHERE trainer_id = ?
            """, (trainer_id,))
            
            profile = cursor.fetchone()
            if not profile:
                return {"success": False, "error": "Trainer not found"}
            
            # Get recent bookings
            cursor.execute("""
                SELECT booking_id, client_user_id, session_date, total_price, 
                       trainer_earnings, payment_status, client_rating
                FROM trainer_bookings 
                WHERE trainer_id = ? 
                ORDER BY session_date DESC LIMIT 10
            """, (trainer_id,))
            
            recent_bookings = [
                {
                    "booking_id": row[0],
                    "client_id": row[1],
                    "session_date": row[2],
                    "total_price": row[3],
                    "earnings": row[4],
                    "status": row[5],
                    "rating": row[6]
                }
                for row in cursor.fetchall()
            ]
            
            # Get earnings summary (last 30 days)
            cursor.execute("""
                SELECT COUNT(*) as sessions, SUM(trainer_earnings) as earnings
                FROM trainer_bookings 
                WHERE trainer_id = ? AND session_date >= date('now', '-30 days')
                AND payment_status = 'completed'
            """, (trainer_id,))
            
            monthly_stats = cursor.fetchone()
            
            # Get active services
            cursor.execute("""
                SELECT service_id, title, service_type, price, duration_minutes, is_active
                FROM trainer_services 
                WHERE trainer_id = ? 
                ORDER BY created_at DESC
            """, (trainer_id,))
            
            services = [
                {
                    "service_id": row[0],
                    "title": row[1],
                    "type": row[2],
                    "price": row[3],
                    "duration": row[4],
                    "active": bool(row[5])
                }
                for row in cursor.fetchall()
            ]
            
            conn.close()
            
            return {
                "success": True,
                "trainer_profile": {
                    "name": f"{profile[0]} {profile[1]}",
                    "status": profile[2],
                    "rating": profile[3],
                    "total_reviews": profile[4],
                    "total_sessions": profile[5],
                    "total_earnings": profile[6],
                    "member_since": profile[7]
                },
                "monthly_stats": {
                    "sessions_completed": monthly_stats[0] or 0,
                    "earnings": monthly_stats[1] or 0.0
                },
                "recent_bookings": recent_bookings,
                "active_services": services,
                "dashboard_metrics": {
                    "response_rate": "95%",  # TODO: Calculate actual rate
                    "booking_conversion": "78%",  # TODO: Calculate actual rate
                    "client_retention": "85%"  # TODO: Calculate actual rate
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting trainer dashboard: {e}")
            return {"success": False, "error": str(e)}

    def update_trainer_status(self, trainer_id: str, new_status: TrainerStatus, notes: str = "") -> Dict:
        """Update trainer status (for admin use)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            update_fields = ["status = ?"]
            params = [new_status.value]
            
            if new_status == TrainerStatus.VERIFIED:
                update_fields.append("verified_at = ?")
                params.append(datetime.now())
            
            params.append(trainer_id)
            
            cursor.execute(f"""
                UPDATE trainer_profiles 
                SET {', '.join(update_fields)}
                WHERE trainer_id = ?
            """, params)
            
            if cursor.rowcount == 0:
                return {"success": False, "error": "Trainer not found"}
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "new_status": new_status.value,
                "message": f"Trainer status updated to {new_status.value}",
                "notes": notes
            }
            
        except Exception as e:
            logger.error(f"Error updating trainer status: {e}")
            return {"success": False, "error": str(e)}

# Initialize the marketplace
def get_trainer_marketplace():
    """Get or create trainer marketplace instance"""
    return TrainerMarketplace()