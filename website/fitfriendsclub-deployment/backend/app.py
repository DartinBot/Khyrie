"""
FitFriendsClub Backend API
A Flask-based backend for the fitness community platform

JWT Implementation: Uses python-jose for enhanced security and JOSE compliance
Database: Hybrid SQLite/PostgreSQL system for development/production flexibility
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sqlite3
import hashlib
from jose import jwt, JWTError
import datetime
from functools import wraps
import json
from werkzeug.utils import secure_filename
from image_utils import ImageProcessor, save_image_to_disk, delete_image_file

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "fitfriendsclub-secret-key-2025"
)
CORS(app)

# Database configuration
DATABASE_PATH = "fitfriendsclub.db"
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DATABASE_PATH}")

# Check if we should use PostgreSQL (for production) or SQLite (for development)
USE_POSTGRESQL = DATABASE_URL.startswith("postgres")

if USE_POSTGRESQL:
    try:
        import psycopg2  # type: ignore[import-untyped] - Optional dependency for PostgreSQL
        from urllib.parse import urlparse

        POSTGRES_AVAILABLE = True
    except ImportError:
        print(
            "⚠️  PostgreSQL requested but psycopg2 not available, falling back to SQLite"
        )
        POSTGRES_AVAILABLE = False
        USE_POSTGRESQL = False
else:
    POSTGRES_AVAILABLE = False


def get_db_connection():
    """Get database connection based on environment"""
    if USE_POSTGRESQL and POSTGRES_AVAILABLE:
        # Parse DATABASE_URL for PostgreSQL
        url = urlparse(DATABASE_URL)
        return psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
        )
    else:
        return sqlite3.connect(DATABASE_PATH)


def init_database():
    """Initialize database with required tables"""
    if USE_POSTGRESQL and POSTGRES_AVAILABLE:
        init_postgresql_database()
    else:
        init_sqlite_database()


def init_postgresql_database():
    """Initialize PostgreSQL database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table (PostgreSQL syntax)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            fitness_goal VARCHAR(50),
            experience_level VARCHAR(20),
            profile_image VARCHAR(255),
            profile_thumbnail VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    """
    )

    # Workouts table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workouts (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            sport_type VARCHAR(50),
            duration_minutes INTEGER,
            calories_burned INTEGER,
            workout_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """
    )

    # Workout partners/friends table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS friendships (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            friend_id INTEGER NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (friend_id) REFERENCES users (id),
            UNIQUE(user_id, friend_id)
        )
    """
    )

    # Group workouts table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS group_workouts (
            id SERIAL PRIMARY KEY,
            organizer_id INTEGER NOT NULL,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            sport_type VARCHAR(50),
            max_participants INTEGER DEFAULT 10,
            workout_datetime TIMESTAMP NOT NULL,
            location VARCHAR(200),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organizer_id) REFERENCES users (id)
        )
    """
    )

    # Group workout participants
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS group_workout_participants (
            id SERIAL PRIMARY KEY,
            group_workout_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_workout_id) REFERENCES group_workouts (id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(group_workout_id, user_id)
        )
    """
    )

    # Workout photos table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workout_photos (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            workout_id INTEGER,
            photo_type VARCHAR(50) NOT NULL,
            image_path VARCHAR(255) NOT NULL,
            thumbnail_path VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (workout_id) REFERENCES workouts (id)
        )
    """
    )

    conn.commit()
    conn.close()
    print("✅ PostgreSQL database initialized successfully!")


def init_sqlite_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Users table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            fitness_goal VARCHAR(50),
            experience_level VARCHAR(20),
            profile_image VARCHAR(255),
            profile_thumbnail VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    """
    )

    # Workouts table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            sport_type VARCHAR(50),
            duration_minutes INTEGER,
            calories_burned INTEGER,
            workout_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """
    )

    # Workout partners/friends table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS friendships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            friend_id INTEGER NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (friend_id) REFERENCES users (id),
            UNIQUE(user_id, friend_id)
        )
    """
    )

    # Group workouts table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS group_workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organizer_id INTEGER NOT NULL,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            sport_type VARCHAR(50),
            max_participants INTEGER DEFAULT 10,
            workout_datetime DATETIME NOT NULL,
            location VARCHAR(200),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organizer_id) REFERENCES users (id)
        )
    """
    )

    # Group workout participants
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS group_workout_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_workout_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_workout_id) REFERENCES group_workouts (id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(group_workout_id, user_id)
        )
    """
    )

    # Workout photos table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workout_photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            workout_id INTEGER,
            photo_type VARCHAR(50) NOT NULL,
            image_path VARCHAR(255) NOT NULL,
            thumbnail_path VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (workout_id) REFERENCES workouts (id)
        )
    """
    )

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hash_password):
    """Verify password against hash"""
    return hashlib.sha256(password.encode()).hexdigest() == hash_password


def generate_token(user_id, username):
    """Generate JWT token for user authentication using python-jose"""
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow(),
        "iss": "FitFriendsClub",  # Issuer for better security
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")


def token_required(f):
    """Decorator to require authentication token"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        if token.startswith("Bearer "):
            token = token[7:]

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user_id = data["user_id"]
            current_username = data["username"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except JWTError:
            return jsonify({"message": "Token is invalid"}), 401

        return f(current_user_id, current_username, *args, **kwargs)

    return decorated


# API Routes


@app.route("/")
def home():
    """API health check"""
    return jsonify(
        {
            "message": "FitFriendsClub API is running!",
            "version": "1.0.0",
            "status": "healthy",
        }
    )


@app.route("/api/register", methods=["POST"])
def register():
    """User registration endpoint"""
    data = request.get_json()

    # Validate required fields
    required_fields = [
        "username",
        "email",
        "password",
        "full_name",
        "fitness_goal",
        "experience_level",
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    # Check if user already exists
    conn = get_db_connection()
    cursor = conn.cursor()

    if USE_POSTGRESQL and POSTGRES_AVAILABLE:
        cursor.execute(
            "SELECT id FROM users WHERE username = %s OR email = %s",
            (data["username"], data["email"]),
        )
        result = cursor.fetchone()
        if result:
            conn.close()
            return jsonify({"error": "User already exists"}), 400

        # Create new user
        password_hash = hash_password(data["password"])

        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, full_name, fitness_goal, experience_level)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """,
            (
                data["username"],
                data["email"],
                password_hash,
                data["full_name"],
                data["fitness_goal"],
                data["experience_level"],
            ),
        )

        user_id = cursor.fetchone()[0]
    else:
        cursor.execute(
            "SELECT id FROM users WHERE username = ? OR email = ?",
            (data["username"], data["email"]),
        )
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": "User already exists"}), 400

        # Create new user
        password_hash = hash_password(data["password"])

        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, full_name, fitness_goal, experience_level)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                data["username"],
                data["email"],
                password_hash,
                data["full_name"],
                data["fitness_goal"],
                data["experience_level"],
            ),
        )

        user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    # Generate token
    token = generate_token(user_id, data["username"])

    return (
        jsonify(
            {
                "message": "Registration successful!",
                "token": token,
                "user": {
                    "id": user_id,
                    "username": data["username"],
                    "email": data["email"],
                    "full_name": data["full_name"],
                },
            }
        ),
        201,
    )


@app.route("/api/login", methods=["POST"])
def login():
    """User login endpoint"""
    data = request.get_json()

    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password required"}), 400

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password_hash, full_name, email FROM users WHERE username = ? OR email = ?",
        (data["username"], data["username"]),
    )
    user = cursor.fetchone()
    conn.close()

    if not user or not verify_password(data["password"], user[2]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user[0], user[1])

    return jsonify(
        {
            "message": "Login successful!",
            "token": token,
            "user": {
                "id": user[0],
                "username": user[1],
                "full_name": user[3],
                "email": user[4],
            },
        }
    )


@app.route("/api/profile", methods=["GET"])
@token_required
def get_profile(current_user_id, current_username):
    """Get user profile"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, email, full_name, fitness_goal, experience_level, created_at 
        FROM users WHERE id = ?
    """,
        (current_user_id,),
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(
        {
            "user": {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "full_name": user[3],
                "fitness_goal": user[4],
                "experience_level": user[5],
                "created_at": user[6],
            }
        }
    )


@app.route("/api/workouts", methods=["GET", "POST"])
@token_required
def workouts(current_user_id, current_username):
    """Get user workouts or create new workout"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute(
            """
            SELECT id, title, description, sport_type, duration_minutes, 
                   calories_burned, workout_date, created_at
            FROM workouts WHERE user_id = ?
            ORDER BY workout_date DESC
        """,
            (current_user_id,),
        )

        workouts = []
        for row in cursor.fetchall():
            workouts.append(
                {
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "sport_type": row[3],
                    "duration_minutes": row[4],
                    "calories_burned": row[5],
                    "workout_date": row[6],
                    "created_at": row[7],
                }
            )

        conn.close()
        return jsonify({"workouts": workouts})

    elif request.method == "POST":
        data = request.get_json()

        required_fields = ["title", "sport_type", "duration_minutes", "workout_date"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        cursor.execute(
            """
            INSERT INTO workouts (user_id, title, description, sport_type, 
                                duration_minutes, calories_burned, workout_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                current_user_id,
                data["title"],
                data.get("description", ""),
                data["sport_type"],
                data["duration_minutes"],
                data.get("calories_burned", 0),
                data["workout_date"],
            ),
        )

        workout_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return (
            jsonify(
                {"message": "Workout created successfully!", "workout_id": workout_id}
            ),
            201,
        )


@app.route("/api/group-workouts", methods=["GET", "POST"])
@token_required
def group_workouts(current_user_id, current_username):
    """Get or create group workouts"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute(
            """
            SELECT gw.id, gw.title, gw.description, gw.sport_type, gw.max_participants,
                   gw.workout_datetime, gw.location, u.full_name as organizer_name,
                   COUNT(gwp.user_id) as current_participants
            FROM group_workouts gw
            JOIN users u ON gw.organizer_id = u.id
            LEFT JOIN group_workout_participants gwp ON gw.id = gwp.group_workout_id
            WHERE gw.workout_datetime > datetime('now')
            GROUP BY gw.id
            ORDER BY gw.workout_datetime ASC
        """
        )

        group_workouts = []
        for row in cursor.fetchall():
            group_workouts.append(
                {
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "sport_type": row[3],
                    "max_participants": row[4],
                    "workout_datetime": row[5],
                    "location": row[6],
                    "organizer_name": row[7],
                    "current_participants": row[8],
                }
            )

        conn.close()
        return jsonify({"group_workouts": group_workouts})

    elif request.method == "POST":
        try:
            data = request.get_json()

            required_fields = ["title", "sport_type", "workout_datetime"]
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"{field} is required"}), 400

            cursor.execute(
                """
                INSERT INTO group_workouts (organizer_id, title, description, sport_type,
                                          max_participants, workout_datetime, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    current_user_id,
                    data["title"],
                    data.get("description", ""),
                    data["sport_type"],
                    data.get("max_participants", 10),
                    data["workout_datetime"],
                    data.get("location", ""),
                ),
            )

            group_workout_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return (
                jsonify(
                    {
                        "message": "Group workout created successfully!",
                        "group_workout_id": group_workout_id,
                    }
                ),
                201,
            )

        except Exception as e:
            print(f"Error creating group workout: {str(e)}")
            return jsonify({"error": "Failed to create group workout"}), 500


# ===================================
# IMAGE PROCESSING ENDPOINTS
# ===================================


@app.route("/api/upload-profile-image", methods=["POST"])
@token_required
def upload_profile_image(current_user_id, current_username):
    """Upload and process profile picture"""
    try:

        # Check if image file is present
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No image file selected"}), 400

        # Read and validate image
        image_data = file.read()
        is_valid, message = ImageProcessor.validate_image(image_data)

        if not is_valid:
            return jsonify({"error": message}), 400

        # Process profile image
        processed_image = ImageProcessor.resize_profile_image(image_data)
        thumbnail = ImageProcessor.create_thumbnail(image_data)

        # Generate filenames
        profile_filename = ImageProcessor.generate_filename(current_user_id, "profile")
        thumbnail_filename = ImageProcessor.generate_filename(
            current_user_id, "profile_thumb"
        )

        # Save processed images
        profile_path = save_image_to_disk(processed_image, profile_filename)
        thumbnail_path = save_image_to_disk(thumbnail, thumbnail_filename)

        # Update user record with image paths
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get old profile image to delete it
        cursor.execute(
            "SELECT profile_image, profile_thumbnail FROM users WHERE id = ?",
            (current_user_id,),
        )
        old_images = cursor.fetchone()

        # Update with new image paths
        cursor.execute(
            """
            UPDATE users 
            SET profile_image = ?, profile_thumbnail = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """,
            (profile_filename, thumbnail_filename, current_user_id),
        )

        conn.commit()
        conn.close()

        # Delete old images if they exist
        if old_images and old_images[0]:
            delete_image_file(os.path.join("uploads", old_images[0]))
        if old_images and old_images[1]:
            delete_image_file(os.path.join("uploads", old_images[1]))

        return jsonify(
            {
                "success": True,
                "message": "Profile image updated successfully",
                "profile_image": profile_filename,
                "thumbnail": thumbnail_filename,
            }
        )

    except Exception as e:
        print(f"Error uploading profile image: {str(e)}")
        return jsonify({"error": "Failed to upload profile image"}), 500


@app.route("/api/upload-workout-photo", methods=["POST"])
@token_required
def upload_workout_photo(current_user_id, current_username):
    """Upload and process workout/progress photo"""
    try:

        # Check if image file is present
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No image file selected"}), 400

        # Get optional parameters
        add_watermark = request.form.get("watermark", "true").lower() == "true"
        workout_id = request.form.get("workout_id")
        photo_type = request.form.get(
            "type", "workout"
        )  # workout, progress, before, after

        # Read and validate image
        image_data = file.read()
        is_valid, message = ImageProcessor.validate_image(image_data)

        if not is_valid:
            return jsonify({"error": message}), 400

        # Process workout photo
        processed_image = ImageProcessor.process_workout_photo(
            image_data, add_watermark
        )
        thumbnail = ImageProcessor.create_thumbnail(image_data)

        # Generate filenames
        photo_filename = ImageProcessor.generate_filename(
            current_user_id, f"{photo_type}_photo"
        )
        thumbnail_filename = ImageProcessor.generate_filename(
            current_user_id, f"{photo_type}_thumb"
        )

        # Save processed images
        photo_path = save_image_to_disk(processed_image, photo_filename)
        thumbnail_path = save_image_to_disk(thumbnail, thumbnail_filename)

        # Save photo record to database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO workout_photos (user_id, workout_id, photo_type, image_path, 
                                      thumbnail_path, created_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
            (
                current_user_id,
                workout_id,
                photo_type,
                photo_filename,
                thumbnail_filename,
            ),
        )

        photo_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify(
            {
                "success": True,
                "message": "Workout photo uploaded successfully",
                "photo_id": photo_id,
                "image_path": photo_filename,
                "thumbnail": thumbnail_filename,
            }
        )

    except Exception as e:
        print(f"Error uploading workout photo: {str(e)}")
        return jsonify({"error": "Failed to upload workout photo"}), 500


@app.route("/api/create-progress-comparison", methods=["POST"])
@token_required
def create_progress_comparison(current_user_id, current_username):
    """Create before/after progress comparison image"""
    try:

        # Check if both image files are present
        if "before_image" not in request.files or "after_image" not in request.files:
            return jsonify({"error": "Both before and after images are required"}), 400

        before_file = request.files["before_image"]
        after_file = request.files["after_image"]

        if before_file.filename == "" or after_file.filename == "":
            return jsonify({"error": "Both image files must be selected"}), 400

        # Read and validate images
        before_data = before_file.read()
        after_data = after_file.read()

        for data, name in [(before_data, "before"), (after_data, "after")]:
            is_valid, message = ImageProcessor.validate_image(data)
            if not is_valid:
                return jsonify({"error": f"{name.title()} image: {message}"}), 400

        # Create comparison image
        comparison_image = ImageProcessor.create_progress_comparison(
            before_data, after_data
        )
        thumbnail = ImageProcessor.create_thumbnail(comparison_image)

        # Generate filenames
        comparison_filename = ImageProcessor.generate_filename(
            current_user_id, "progress_comparison"
        )
        thumbnail_filename = ImageProcessor.generate_filename(
            current_user_id, "progress_thumb"
        )

        # Save images
        comparison_path = save_image_to_disk(comparison_image, comparison_filename)
        thumbnail_path = save_image_to_disk(thumbnail, thumbnail_filename)

        # Save record to database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO workout_photos (user_id, photo_type, image_path, 
                                      thumbnail_path, created_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
            (
                current_user_id,
                "progress_comparison",
                comparison_filename,
                thumbnail_filename,
            ),
        )

        comparison_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify(
            {
                "success": True,
                "message": "Progress comparison created successfully",
                "comparison_id": comparison_id,
                "image_path": comparison_filename,
                "thumbnail": thumbnail_filename,
            }
        )

    except Exception as e:
        print(f"Error creating progress comparison: {str(e)}")
        return jsonify({"error": "Failed to create progress comparison"}), 500


@app.route("/api/images/<filename>")
def serve_image(filename):
    """Serve uploaded images"""
    try:
        # Security check: ensure filename is safe
        safe_filename = secure_filename(filename)
        return send_from_directory("uploads", safe_filename)

    except Exception as e:
        print(f"Error serving image: {str(e)}")
        return jsonify({"error": "Image not found"}), 404


@app.route("/api/user-photos")
@token_required
def get_user_photos(current_user_id, current_username):
    """Get all photos for current user"""
    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, workout_id, photo_type, image_path, thumbnail_path, created_at
            FROM workout_photos 
            WHERE user_id = ?
            ORDER BY created_at DESC
        """,
            (current_user_id,),
        )

        photos = []
        for row in cursor.fetchall():
            photos.append(
                {
                    "id": row[0],
                    "workout_id": row[1],
                    "photo_type": row[2],
                    "image_url": f"/api/images/{row[3]}",
                    "thumbnail_url": f"/api/images/{row[4]}",
                    "created_at": row[5],
                }
            )

        conn.close()

        return jsonify({"success": True, "photos": photos})

    except Exception as e:
        print(f"Error getting user photos: {str(e)}")
        return jsonify({"error": "Failed to retrieve photos"}), 500


@app.route("/api/delete-photo/<int:photo_id>", methods=["DELETE"])
@token_required
def delete_photo(current_user_id, current_username, photo_id):
    """Delete a user's photo"""
    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get photo info and verify ownership
        cursor.execute(
            """
            SELECT image_path, thumbnail_path FROM workout_photos 
            WHERE id = ? AND user_id = ?
        """,
            (photo_id, current_user_id),
        )

        photo_info = cursor.fetchone()
        if not photo_info:
            return jsonify({"error": "Photo not found or access denied"}), 404

        # Delete from database
        cursor.execute(
            "DELETE FROM workout_photos WHERE id = ? AND user_id = ?",
            (photo_id, current_user_id),
        )

        conn.commit()
        conn.close()

        # Delete files from disk
        delete_image_file(os.path.join("uploads", photo_info[0]))
        delete_image_file(os.path.join("uploads", photo_info[1]))

        return jsonify({"success": True, "message": "Photo deleted successfully"})

    except Exception as e:
        print(f"Error deleting photo: {str(e)}")
        return jsonify({"error": "Failed to delete photo"}), 500


if __name__ == "__main__":
    print("🚀 Initializing FitFriendsClub Backend...")
    init_database()
    print("🌐 Starting Flask server...")
    app.run(debug=True, host="0.0.0.0", port=5000)
