-- Complete FitFriendsClubs Database Schema
-- Deploy this complete schema to set up your entire fitness platform database

-- ===== CORE TABLES (Prerequisites) =====

-- Users Table (Base table that others reference)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    profile_picture VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Basic workouts table
CREATE TABLE IF NOT EXISTS workouts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    duration INTEGER, -- in minutes
    intensity VARCHAR(20), -- 'low', 'moderate', 'high', 'extreme'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Social Posts Table
CREATE TABLE IF NOT EXISTS social_posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    image_url VARCHAR(500),
    likes INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ===== FITNESS CLUBS & EQUIPMENT =====

-- Fitness Clubs Table
CREATE TABLE IF NOT EXISTS fitness_clubs (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL, -- 'run', 'cycle', 'pilates', 'yoga', 'strength', etc.
    equipment_type VARCHAR(50), -- 'treadmill', 'stationary_bike', 'none', etc.
    max_members INTEGER DEFAULT 100,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Club Members Table
CREATE TABLE IF NOT EXISTS club_members (
    id SERIAL PRIMARY KEY,
    club_id INTEGER NOT NULL REFERENCES fitness_clubs(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member', -- 'admin', 'moderator', 'member'
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(club_id, user_id)
);

-- Group Workout Sessions
CREATE TABLE IF NOT EXISTS group_sessions (
    id SERIAL PRIMARY KEY,
    club_id INTEGER NOT NULL REFERENCES fitness_clubs(id) ON DELETE CASCADE,
    instructor_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 30,
    max_participants INTEGER DEFAULT 50,
    equipment_settings JSONB, -- Workout parameters, resistance levels, speed targets, etc.
    status VARCHAR(20) DEFAULT 'scheduled', -- 'scheduled', 'live', 'completed', 'cancelled'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Group Session Participants
CREATE TABLE IF NOT EXISTS group_session_participants (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES group_sessions(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(session_id, user_id)
);

-- User Equipment Connections
CREATE TABLE IF NOT EXISTS user_equipment (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    equipment_type VARCHAR(50) NOT NULL, -- 'treadmill', 'stationary_bike', 'elliptical', etc.
    equipment_id VARCHAR(100) NOT NULL, -- Unique equipment identifier
    brand VARCHAR(50),
    model VARCHAR(100),
    connection_data JSONB, -- Bluetooth/WiFi connection details, API keys, etc.
    is_active BOOLEAN DEFAULT true,
    connected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_sync TIMESTAMP WITH TIME ZONE
);

-- Equipment Workout Data
CREATE TABLE IF NOT EXISTS equipment_workout_data (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES group_sessions(id) ON DELETE CASCADE, -- NULL for solo workouts
    equipment_id VARCHAR(100) NOT NULL,
    duration_seconds INTEGER NOT NULL,
    distance DECIMAL(10,2), -- Miles or kilometers
    calories_burned INTEGER,
    avg_heart_rate INTEGER,
    max_heart_rate INTEGER,
    speed_data JSONB, -- Array of speed measurements over time
    resistance_data JSONB, -- Array of resistance levels over time
    timestamps JSONB, -- Array of timestamps for data points
    synced_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Session Leaderboard
CREATE TABLE IF NOT EXISTS session_leaderboard (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES group_sessions(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    score INTEGER NOT NULL DEFAULT 0, -- Calculated based on performance metrics
    distance DECIMAL(10,2),
    duration_seconds INTEGER,
    calories_burned INTEGER,
    rank_position INTEGER, -- Updated via triggers or batch jobs
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(session_id, user_id)
);

-- ===== VIRTUAL TRAILS SYSTEM =====

-- Virtual Trails Table - Famous routes from around the world
CREATE TABLE IF NOT EXISTS virtual_trails (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    location VARCHAR(100) NOT NULL, -- City/Park name
    country VARCHAR(100) NOT NULL,
    activity_type VARCHAR(20) NOT NULL, -- 'run', 'cycle', 'both'
    distance_km DECIMAL(10,2) NOT NULL,
    elevation_gain_m INTEGER DEFAULT 0,
    difficulty VARCHAR(20) NOT NULL, -- 'easy', 'moderate', 'hard', 'expert'
    route_data JSONB NOT NULL, -- Detailed route information, elevation profile, scenery points
    image_url VARCHAR(500),
    video_url VARCHAR(500), -- 360° video or route preview
    is_featured BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Trail Sessions - User sessions on virtual trails
CREATE TABLE IF NOT EXISTS trail_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    trail_id INTEGER NOT NULL REFERENCES virtual_trails(id) ON DELETE CASCADE,
    equipment_id VARCHAR(100), -- Connected equipment for this session
    session_mode VARCHAR(20) DEFAULT 'solo', -- 'solo', 'group', 'race'
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'paused', 'completed', 'abandoned'
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE,
    paused_duration_seconds INTEGER DEFAULT 0,
    target_distance_km DECIMAL(10,2),
    actual_distance_km DECIMAL(10,2),
    target_elevation_gain_m INTEGER,
    actual_elevation_gain_m INTEGER,
    completion_time_seconds INTEGER, -- Total time including pauses
    active_time_seconds INTEGER, -- Time excluding pauses
    avg_speed_kmh DECIMAL(8,2),
    max_speed_kmh DECIMAL(8,2),
    avg_heart_rate INTEGER,
    max_heart_rate INTEGER,
    calories_burned INTEGER,
    completed BOOLEAN DEFAULT false,
    performance_data JSONB -- Detailed metrics throughout the session
);

-- Trail Achievements
CREATE TABLE IF NOT EXISTS trail_achievements (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    trail_id INTEGER NOT NULL REFERENCES virtual_trails(id) ON DELETE CASCADE,
    achievement_type VARCHAR(50) NOT NULL, -- 'first_completion', 'personal_best', 'trail_master', etc.
    achievement_data JSONB,
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, trail_id, achievement_type)
);

-- ===== LIVE VIDEO STREAMING SYSTEM =====

-- Streaming Sessions Table
CREATE TABLE IF NOT EXISTS streaming_sessions (
    id SERIAL PRIMARY KEY,
    group_session_id INTEGER NOT NULL REFERENCES group_sessions(id) ON DELETE CASCADE,
    host_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stream_key VARCHAR(255) UNIQUE NOT NULL,
    room_id VARCHAR(255) UNIQUE NOT NULL,
    stream_title VARCHAR(200) NOT NULL,
    stream_description TEXT,
    max_viewers INTEGER DEFAULT 100,
    viewer_count INTEGER DEFAULT 0,
    stream_quality VARCHAR(20) DEFAULT 'HD', -- 'SD', 'HD', '4K'
    status VARCHAR(20) DEFAULT 'created', -- 'created', 'live', 'ended', 'paused'
    started_at TIMESTAMP WITH TIME ZONE,
    ended_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(group_session_id) -- One stream per group session
);

-- Stream Viewers Table
CREATE TABLE IF NOT EXISTS stream_viewers (
    id SERIAL PRIMARY KEY,
    streaming_session_id INTEGER NOT NULL REFERENCES streaming_sessions(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    left_at TIMESTAMP WITH TIME ZONE,
    total_watch_time INTEGER DEFAULT 0, -- in seconds
    UNIQUE(streaming_session_id, user_id)
);

-- Chat Messages for Live Streams
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    streaming_session_id INTEGER NOT NULL REFERENCES streaming_sessions(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text', -- 'text', 'emoji', 'system'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Stream Analytics Table
CREATE TABLE IF NOT EXISTS stream_analytics (
    id SERIAL PRIMARY KEY,
    streaming_session_id INTEGER NOT NULL REFERENCES streaming_sessions(id) ON DELETE CASCADE,
    metric_name VARCHAR(50) NOT NULL, -- 'peak_viewers', 'total_views', 'avg_watch_time', etc.
    metric_value DECIMAL(10,2) NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- 'live_stream_started', 'session_reminder', etc.
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    data JSONB, -- Additional notification data
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Stream Quality Settings & User Preferences
CREATE TABLE IF NOT EXISTS user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    preferred_stream_quality VARCHAR(20) DEFAULT 'HD',
    auto_quality BOOLEAN DEFAULT true,
    chat_enabled BOOLEAN DEFAULT true,
    notifications_enabled BOOLEAN DEFAULT true,
    email_notifications BOOLEAN DEFAULT true,
    push_notifications BOOLEAN DEFAULT true,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- ===== INDEXES FOR PERFORMANCE =====

-- Core table indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_workouts_user ON workouts(user_id);
CREATE INDEX IF NOT EXISTS idx_social_posts_user ON social_posts(user_id);

-- Fitness clubs indexes
CREATE INDEX IF NOT EXISTS idx_fitness_clubs_category ON fitness_clubs(category);
CREATE INDEX IF NOT EXISTS idx_fitness_clubs_creator ON fitness_clubs(creator_id);
CREATE INDEX IF NOT EXISTS idx_club_members_club_user ON club_members(club_id, user_id);
CREATE INDEX IF NOT EXISTS idx_group_sessions_club ON group_sessions(club_id);
CREATE INDEX IF NOT EXISTS idx_group_sessions_start_time ON group_sessions(start_time);
CREATE INDEX IF NOT EXISTS idx_session_participants_session ON group_session_participants(session_id);
CREATE INDEX IF NOT EXISTS idx_user_equipment_user ON user_equipment(user_id);
CREATE INDEX IF NOT EXISTS idx_equipment_workout_data_user ON equipment_workout_data(user_id);
CREATE INDEX IF NOT EXISTS idx_equipment_workout_data_session ON equipment_workout_data(session_id);
CREATE INDEX IF NOT EXISTS idx_session_leaderboard_session ON session_leaderboard(session_id);

-- Virtual trails indexes
CREATE INDEX IF NOT EXISTS idx_virtual_trails_activity ON virtual_trails(activity_type);
CREATE INDEX IF NOT EXISTS idx_virtual_trails_location ON virtual_trails(location, country);
CREATE INDEX IF NOT EXISTS idx_virtual_trails_difficulty ON virtual_trails(difficulty);
CREATE INDEX IF NOT EXISTS idx_virtual_trails_featured ON virtual_trails(is_featured);
CREATE INDEX IF NOT EXISTS idx_trail_sessions_user ON trail_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_trail_sessions_trail ON trail_sessions(trail_id);
CREATE INDEX IF NOT EXISTS idx_trail_sessions_completed ON trail_sessions(completed, completion_time_seconds);
CREATE INDEX IF NOT EXISTS idx_trail_achievements_user ON trail_achievements(user_id);

-- Streaming indexes
CREATE INDEX IF NOT EXISTS idx_streaming_sessions_status ON streaming_sessions(status);
CREATE INDEX IF NOT EXISTS idx_streaming_sessions_group_session ON streaming_sessions(group_session_id);
CREATE INDEX IF NOT EXISTS idx_stream_viewers_session ON stream_viewers(streaming_session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session ON chat_messages(streaming_session_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user_unread ON notifications(user_id, is_read);

-- Full-text search indexes
CREATE INDEX IF NOT EXISTS idx_virtual_trails_search ON virtual_trails USING GIN (to_tsvector('english', name || ' ' || description || ' ' || location));
CREATE INDEX IF NOT EXISTS idx_fitness_clubs_search ON fitness_clubs USING GIN (to_tsvector('english', name || ' ' || description));

-- ===== SAMPLE DATA =====

-- Insert sample user (for testing - remove in production)
INSERT INTO users (username, email, password) 
VALUES ('admin', 'admin@fitfriendsclubs.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8') -- 'hello' hashed
ON CONFLICT (username) DO NOTHING;

-- Sample fitness clubs
INSERT INTO fitness_clubs (creator_id, name, description, category, equipment_type, max_members) 
VALUES 
(1, 'Morning Runners Club', 'Early bird runners who love to start the day with energy!', 'run', 'treadmill', 50),
(1, 'Cycle Warriors', 'High-intensity cycling sessions for all fitness levels', 'cycle', 'stationary_bike', 30),
(1, 'Pilates Power', 'Core strength and flexibility focused sessions', 'pilates', 'none', 25),
(1, 'HIIT Squad', 'High Intensity Interval Training for maximum results', 'hiit', 'none', 40),
(1, 'Yoga Flow', 'Mindful movement and meditation sessions', 'yoga', 'none', 35),
(1, 'Strength Society', 'Build muscle and strength together', 'strength', 'none', 20)
ON CONFLICT DO NOTHING;

-- Sample virtual trails (Famous routes)
INSERT INTO virtual_trails (name, description, location, country, activity_type, distance_km, elevation_gain_m, difficulty, route_data, is_featured) VALUES

-- Running Trails
('Central Park Loop', 'The iconic 6-mile loop around Central Park with rolling hills and scenic views', 'Central Park, New York', 'USA', 'run', 9.7, 175, 'moderate', 
'{"elevation_profile": [0, 15, 25, 35, 42, 38, 45, 55, 48, 32, 25, 15, 8, 0], "scenery_points": [{"km": 0, "description": "Tavern on the Green"}, {"km": 2.4, "description": "Reservoir"}, {"km": 4.8, "description": "Great Lawn"}, {"km": 7.2, "description": "Bethesda Fountain"}]}', true),

('Thames Path London', 'Historic Thames through London passing Tower Bridge and Big Ben', 'Thames Path, London', 'UK', 'run', 21.1, 89, 'easy', 
'{"elevation_profile": [0, 5, 8, 12, 18, 15, 22, 28, 25, 18, 12, 8, 5, 0], "scenery_points": [{"km": 5, "description": "Tower Bridge"}, {"km": 10, "description": "London Bridge"}, {"km": 15, "description": "Big Ben"}, {"km": 21, "description": "London Eye"}]}', true),

-- Cycling Trails  
('Alpe d''Huez Climb', 'Legendary Tour de France mountain climb with 21 hairpin turns', 'Alpe d''Huez, French Alps', 'France', 'cycle', 13.8, 1071, 'expert', 
'{"elevation_profile": [720, 850, 980, 1100, 1220, 1340, 1460, 1580, 1700, 1791], "scenery_points": [{"km": 2, "description": "Turn 19"}, {"km": 7, "description": "Turn 12 - Halfway"}, {"km": 11, "description": "Dutch Corner"}, {"km": 13.8, "description": "Summit"}]}', true),

('Amsterdam Canal Ring', 'UNESCO World Heritage canal district cycling tour', 'Canal Ring, Amsterdam', 'Netherlands', 'cycle', 12.5, 15, 'easy', 
'{"elevation_profile": [0, 2, 4, 3, 5, 4, 6, 5, 3, 2, 1, 0], "scenery_points": [{"km": 2, "description": "Jordaan District"}, {"km": 5, "description": "Anne Frank House"}, {"km": 8, "description": "Rijksmuseum"}, {"km": 12, "description": "Vondelpark"}]}', true)

ON CONFLICT DO NOTHING;

-- Sample user preferences
INSERT INTO user_preferences (user_id, preferred_stream_quality, auto_quality, chat_enabled, notifications_enabled) 
VALUES 
(1, 'HD', true, true, true)
ON CONFLICT (user_id) DO NOTHING;

-- ===== SUCCESS MESSAGE =====
DO $$
BEGIN
    RAISE NOTICE 'FitFriendsClubs database schema deployed successfully!';
    RAISE NOTICE 'Tables created: users, workouts, social_posts, fitness_clubs, group_sessions, virtual_trails, streaming_sessions, and more';
    RAISE NOTICE 'Sample data inserted for testing';
    RAISE NOTICE 'Next step: Configure your Cloudflare Workers environment variables';
END $$;