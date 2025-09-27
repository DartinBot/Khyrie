"""
FitFriendsClub Backend API
A Flask-based backend for the fitness community platform
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sqlite3
import hashlib
import jwt
import datetime
from functools import wraps
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fitfriendsclub-secret-key-2025')
CORS(app)

# Database configuration
DATABASE_PATH = 'fitfriendsclub.db'

def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            fitness_goal VARCHAR(50),
            experience_level VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Workouts table
    cursor.execute('''
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
    ''')
    
    # Workout partners/friends table
    cursor.execute('''
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
    ''')
    
    # Group workouts table
    cursor.execute('''
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
    ''')
    
    # Group workout participants
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_workout_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_workout_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_workout_id) REFERENCES group_workouts (id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(group_workout_id, user_id)
        )
    ''')
    
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
    """Generate JWT token for user authentication"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    """Decorator to require authentication token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
            
        if token.startswith('Bearer '):
            token = token[7:]
            
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            current_username = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
            
        return f(current_user_id, current_username, *args, **kwargs)
    
    return decorated

# API Routes

@app.route('/')
def home():
    """API health check"""
    return jsonify({
        'message': 'FitFriendsClub API is running!',
        'version': '1.0.0',
        'status': 'healthy'
    })

@app.route('/api/register', methods=['POST'])
def register():
    """User registration endpoint"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'full_name', 'fitness_goal', 'experience_level']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if user already exists
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', 
                  (data['username'], data['email']))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'User already exists'}), 400
    
    # Create new user
    password_hash = hash_password(data['password'])
    
    cursor.execute('''
        INSERT INTO users (username, email, password_hash, full_name, fitness_goal, experience_level)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['username'], data['email'], password_hash, data['full_name'], 
          data['fitness_goal'], data['experience_level']))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # Generate token
    token = generate_token(user_id, data['username'])
    
    return jsonify({
        'message': 'Registration successful!',
        'token': token,
        'user': {
            'id': user_id,
            'username': data['username'],
            'email': data['email'],
            'full_name': data['full_name']
        }
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, username, password_hash, full_name, email FROM users WHERE username = ? OR email = ?', 
                  (data['username'], data['username']))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not verify_password(data['password'], user[2]):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = generate_token(user[0], user[1])
    
    return jsonify({
        'message': 'Login successful!',
        'token': token,
        'user': {
            'id': user[0],
            'username': user[1],
            'full_name': user[3],
            'email': user[4]
        }
    })

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user_id, current_username):
    """Get user profile"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, email, full_name, fitness_goal, experience_level, created_at 
        FROM users WHERE id = ?
    ''', (current_user_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'full_name': user[3],
            'fitness_goal': user[4],
            'experience_level': user[5],
            'created_at': user[6]
        }
    })

@app.route('/api/workouts', methods=['GET', 'POST'])
@token_required
def workouts(current_user_id, current_username):
    """Get user workouts or create new workout"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('''
            SELECT id, title, description, sport_type, duration_minutes, 
                   calories_burned, workout_date, created_at
            FROM workouts WHERE user_id = ?
            ORDER BY workout_date DESC
        ''', (current_user_id,))
        
        workouts = []
        for row in cursor.fetchall():
            workouts.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'sport_type': row[3],
                'duration_minutes': row[4],
                'calories_burned': row[5],
                'workout_date': row[6],
                'created_at': row[7]
            })
        
        conn.close()
        return jsonify({'workouts': workouts})
    
    elif request.method == 'POST':
        data = request.get_json()
        
        required_fields = ['title', 'sport_type', 'duration_minutes', 'workout_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        cursor.execute('''
            INSERT INTO workouts (user_id, title, description, sport_type, 
                                duration_minutes, calories_burned, workout_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (current_user_id, data['title'], data.get('description', ''),
              data['sport_type'], data['duration_minutes'], 
              data.get('calories_burned', 0), data['workout_date']))
        
        workout_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Workout created successfully!',
            'workout_id': workout_id
        }), 201

@app.route('/api/group-workouts', methods=['GET', 'POST'])
@token_required
def group_workouts(current_user_id, current_username):
    """Get or create group workouts"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('''
            SELECT gw.id, gw.title, gw.description, gw.sport_type, gw.max_participants,
                   gw.workout_datetime, gw.location, u.full_name as organizer_name,
                   COUNT(gwp.user_id) as current_participants
            FROM group_workouts gw
            JOIN users u ON gw.organizer_id = u.id
            LEFT JOIN group_workout_participants gwp ON gw.id = gwp.group_workout_id
            WHERE gw.workout_datetime > datetime('now')
            GROUP BY gw.id
            ORDER BY gw.workout_datetime ASC
        ''')
        
        group_workouts = []
        for row in cursor.fetchall():
            group_workouts.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'sport_type': row[3],
                'max_participants': row[4],
                'workout_datetime': row[5],
                'location': row[6],
                'organizer_name': row[7],
                'current_participants': row[8]
            })
        
        conn.close()
        return jsonify({'group_workouts': group_workouts})
    
    elif request.method == 'POST':
        data = request.get_json()
        
        required_fields = ['title', 'sport_type', 'workout_datetime']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        cursor.execute('''
            INSERT INTO group_workouts (organizer_id, title, description, sport_type,
                                      max_participants, workout_datetime, location)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (current_user_id, data['title'], data.get('description', ''),
              data['sport_type'], data.get('max_participants', 10),
              data['workout_datetime'], data.get('location', '')))
        
        group_workout_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Group workout created successfully!',
            'group_workout_id': group_workout_id
        }), 201

if __name__ == '__main__':
    print("🚀 Initializing FitFriendsClub Backend...")
    init_database()
    print("🌐 Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)