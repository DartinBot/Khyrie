-- Fitness Clubs & Equipment Integration Database Schema
-- Run this SQL to add the new tables for fitness clubs functionality

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

-- Club Activity Feed
CREATE TABLE IF NOT EXISTS club_activities (
    id SERIAL PRIMARY KEY,
    club_id INTEGER NOT NULL REFERENCES fitness_clubs(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL, -- 'joined', 'session_created', 'workout_completed', etc.
    activity_data JSONB, -- Additional context data
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for better performance
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
CREATE INDEX IF NOT EXISTS idx_club_activities_club ON club_activities(club_id);

-- Sample fitness clubs data
INSERT INTO fitness_clubs (creator_id, name, description, category, equipment_type, max_members) 
VALUES 
(1, 'Morning Runners Club', 'Early bird runners who love to start the day with energy!', 'run', 'treadmill', 50),
(1, 'Cycle Warriors', 'High-intensity cycling sessions for all fitness levels', 'cycle', 'stationary_bike', 30),
(1, 'Pilates Power', 'Core strength and flexibility focused sessions', 'pilates', 'none', 25),
(1, 'HIIT Squad', 'High Intensity Interval Training for maximum results', 'hiit', 'none', 40),
(1, 'Yoga Flow', 'Mindful movement and meditation sessions', 'yoga', 'none', 35),
(1, 'Strength Society', 'Build muscle and strength together', 'strength', 'none', 20)
ON CONFLICT DO NOTHING;

-- Sample group sessions
INSERT INTO group_sessions (club_id, instructor_id, title, description, start_time, duration_minutes, max_participants, equipment_settings)
VALUES 
(1, 1, '5K Morning Run Challenge', 'Virtual 5K run on treadmills - beat your personal best!', 
 NOW() + INTERVAL '1 day', 30, 20, 
 '{"target_distance": 5, "difficulty": "moderate", "incline_range": [0, 5], "speed_range": [6, 12]}'),
(2, 1, 'Hill Climb Cycling', '45-minute intense cycling session with hill simulations', 
 NOW() + INTERVAL '2 days', 45, 15, 
 '{"target_distance": 15, "difficulty": "hard", "resistance_range": [5, 15], "cadence_target": 80}'),
(3, 1, 'Core Strength Pilates', 'Focus on core stability and strength building', 
 NOW() + INTERVAL '3 days', 50, 12, 
 '{"difficulty": "intermediate", "equipment": "mat_only", "focus": "core"}')
ON CONFLICT DO NOTHING;

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

-- Indexes for virtual trails
CREATE INDEX IF NOT EXISTS idx_virtual_trails_activity ON virtual_trails(activity_type);
CREATE INDEX IF NOT EXISTS idx_virtual_trails_location ON virtual_trails(location, country);
CREATE INDEX IF NOT EXISTS idx_virtual_trails_difficulty ON virtual_trails(difficulty);
CREATE INDEX IF NOT EXISTS idx_virtual_trails_featured ON virtual_trails(is_featured);
CREATE INDEX IF NOT EXISTS idx_trail_sessions_user ON trail_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_trail_sessions_trail ON trail_sessions(trail_id);
CREATE INDEX IF NOT EXISTS idx_trail_sessions_completed ON trail_sessions(completed, completion_time_seconds);
CREATE INDEX IF NOT EXISTS idx_trail_achievements_user ON trail_achievements(user_id);

-- Insert Famous Virtual Trails

-- RUNNING TRAILS
INSERT INTO virtual_trails (name, description, location, country, activity_type, distance_km, elevation_gain_m, difficulty, route_data, is_featured) VALUES

-- New York Central Park Loop
('Central Park Loop', 'The iconic 6-mile loop around Central Park with rolling hills and scenic views of Manhattan skyline', 'Central Park, New York', 'USA', 'run', 9.7, 175, 'moderate', 
'{"elevation_profile": [0, 15, 25, 35, 42, 38, 45, 55, 48, 32, 25, 15, 8, 0], "scenery_points": [{"km": 0, "description": "Tavern on the Green"}, {"km": 2.4, "description": "Reservoir with Manhattan views"}, {"km": 4.8, "description": "Great Lawn"}, {"km": 7.2, "description": "Bethesda Fountain"}], "resistance_profile": [2, 3, 4, 5, 6, 5, 6, 7, 6, 4, 3, 2, 2, 1], "audio_cues": [{"km": 1, "message": "You are passing Sheep Meadow, keep your steady pace!"}, {"km": 5, "message": "Halfway point! You are doing great on the East Side"}]}', true),

-- London Thames Path
('Thames Path Marathon Route', 'Follow the historic Thames through London, passing Tower Bridge, Big Ben, and London Eye', 'Thames Path, London', 'UK', 'run', 42.2, 89, 'easy', 
'{"elevation_profile": [0, 5, 8, 12, 18, 15, 22, 28, 25, 18, 12, 8, 5, 0], "scenery_points": [{"km": 10, "description": "Tower Bridge"}, {"km": 20, "description": "London Bridge"}, {"km": 30, "description": "Westminster Bridge & Big Ben"}, {"km": 35, "description": "London Eye"}], "resistance_profile": [1, 2, 2, 3, 3, 3, 4, 4, 3, 2, 2, 1, 1, 1], "audio_cues": [{"km": 10, "message": "Tower Bridge ahead - one of Londons most iconic landmarks!"}, {"km": 42, "message": "Congratulations! You have completed the Thames Path Marathon!"}]}', true),

-- San Francisco Golden Gate
('Golden Gate Bridge to Sausalito', 'Cross the iconic Golden Gate Bridge with stunning bay views and Marin Headlands', 'Golden Gate Bridge, San Francisco', 'USA', 'both', 13.2, 245, 'moderate', 
'{"elevation_profile": [0, 65, 85, 95, 125, 145, 165, 185, 155, 125, 95, 65, 35, 0], "scenery_points": [{"km": 2.7, "description": "Golden Gate Bridge South Tower"}, {"km": 4.2, "description": "Golden Gate Bridge North Tower"}, {"km": 8, "description": "Sausalito Waterfront"}, {"km": 13, "description": "Sausalito Ferry Terminal"}], "resistance_profile": [2, 5, 6, 7, 8, 9, 10, 11, 8, 6, 4, 3, 2, 1], "audio_cues": [{"km": 2, "message": "Approaching the Golden Gate Bridge - feel the ocean breeze!"}, {"km": 8, "message": "Welcome to Sausalito! Enjoy the Mediterranean-style architecture"}]}', true),

-- Boston Freedom Trail
('Boston Freedom Trail', 'Historic 2.5 mile trail through downtown Boston visiting 16 Revolutionary War sites', 'Freedom Trail, Boston', 'USA', 'run', 4.0, 45, 'easy', 
'{"elevation_profile": [0, 8, 15, 22, 28, 25, 18, 12, 8, 5, 0], "scenery_points": [{"km": 0.5, "description": "Boston Common"}, {"km": 1.5, "description": "Paul Revere House"}, {"km": 2.5, "description": "USS Constitution"}, {"km": 4, "description": "Bunker Hill Monument"}], "resistance_profile": [1, 2, 3, 4, 4, 3, 2, 2, 1, 1, 1], "audio_cues": [{"km": 1, "message": "You are now in the North End, home to many Italian-American families"}, {"km": 4, "message": "Congratulations! You have completed the historic Freedom Trail"}]}', true);

-- CYCLING TRAILS  
INSERT INTO virtual_trails (name, description, location, country, activity_type, distance_km, elevation_gain_m, difficulty, route_data, is_featured) VALUES

-- Tour de France - Alpe d'Huez
('Alpe d''Huez Climb', 'Legendary Tour de France mountain climb with 21 hairpin turns and 8% average gradient', 'Alpe d''Huez, French Alps', 'France', 'cycle', 13.8, 1071, 'expert', 
'{"elevation_profile": [720, 850, 980, 1100, 1220, 1340, 1460, 1580, 1700, 1791], "scenery_points": [{"km": 2, "description": "Turn 19 - First major switchback"}, {"km": 7, "description": "Turn 12 - Halfway point with alpine views"}, {"km": 11, "description": "Turn 6 - Dutch Corner"}, {"km": 13.8, "description": "Alpe dHuez Summit - 1,850m elevation"}], "resistance_profile": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17], "audio_cues": [{"km": 0, "message": "Begin the legendary Alpe dHuez climb - pace yourself for 21 turns ahead!"}, {"km": 7, "message": "Halfway up! You are climbing like the Tour de France champions"}, {"km": 13.8, "message": "Summit conquered! You have climbed 1,071 meters - incredible achievement!"}]}', true),

-- Amsterdam Canal Ring
('Amsterdam Canal Ring', 'Scenic ride through UNESCO World Heritage canal district with historic architecture', 'Canal Ring, Amsterdam', 'Netherlands', 'cycle', 12.5, 15, 'easy', 
'{"elevation_profile": [0, 2, 4, 3, 5, 4, 6, 5, 3, 2, 1, 0], "scenery_points": [{"km": 2, "description": "Jordaan District"}, {"km": 5, "description": "Anne Frank House"}, {"km": 8, "description": "Rijksmuseum"}, {"km": 12, "description": "Vondelpark"}], "resistance_profile": [1, 1, 2, 2, 2, 2, 3, 2, 2, 1, 1, 1], "audio_cues": [{"km": 2, "message": "You are now cycling through the charming Jordaan neighborhood"}, {"km": 12, "message": "Completing your tour of Amsterdams beautiful canals - well done!"}]}', true),

-- Napa Valley Wine Country
('Napa Valley Wine Route', 'Rolling hills through world-famous wine country with vineyard views and mountain backdrops', 'Napa Valley, California', 'USA', 'cycle', 28.5, 420, 'moderate', 
'{"elevation_profile": [15, 45, 85, 125, 165, 195, 225, 255, 285, 315, 285, 255, 195, 155, 125, 85, 45, 15], "scenery_points": [{"km": 5, "description": "Domaine Chandon Winery"}, {"km": 12, "description": "Oakville AVA Vineyards"}, {"km": 18, "description": "St. Helena Historic Downtown"}, {"km": 25, "description": "Calistoga Hot Springs"}], "resistance_profile": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 10, 8, 6, 5, 4, 3, 2, 2], "audio_cues": [{"km": 10, "message": "You are cycling through some of the worlds finest wine regions"}, {"km": 28, "message": "Fantastic ride through Napa Valley wine country completed!"}]}', true),

-- Tuscany Hills
('Tuscany Hill Country', 'Classic Italian countryside with cypress trees, rolling hills, and medieval villages', 'Chianti Region, Tuscany', 'Italy', 'cycle', 45.2, 890, 'hard', 
'{"elevation_profile": [285, 345, 425, 485, 565, 625, 685, 745, 685, 625, 565, 485, 425, 365, 285], "scenery_points": [{"km": 8, "description": "San Gimignano Medieval Towers"}, {"km": 18, "description": "Chianti Classico Vineyards"}, {"km": 28, "description": "Siena Cathedral"}, {"km": 38, "description": "Cypress Tree Avenue"}], "resistance_profile": [4, 6, 8, 9, 11, 12, 14, 15, 12, 10, 8, 6, 5, 4, 3], "audio_cues": [{"km": 15, "message": "You are cycling through the heart of Chianti wine region"}, {"km": 45, "message": "Bellissimo! You have completed the beautiful Tuscany hill country route"}]}', true);

-- MORE RUNNING TRAILS
INSERT INTO virtual_trails (name, description, location, country, activity_type, distance_km, elevation_gain_m, difficulty, route_data, is_featured) VALUES

-- Big Sur Coastal Trail
('Big Sur Coastal Highway', 'Dramatic Pacific Coast cliffs with ocean views and redwood forests', 'Big Sur, California', 'USA', 'both', 15.8, 320, 'moderate', 
'{"elevation_profile": [5, 65, 125, 185, 245, 285, 325, 285, 245, 185, 125, 85, 45, 15, 5], "scenery_points": [{"km": 3, "description": "McWay Falls"}, {"km": 8, "description": "Bixby Creek Bridge"}, {"km": 12, "description": "Point Sur Lighthouse"}, {"km": 15, "description": "Hearst Castle Views"}], "resistance_profile": [2, 4, 6, 8, 10, 12, 13, 10, 8, 6, 4, 3, 2, 1, 1], "audio_cues": [{"km": 5, "message": "You are running along one of the most scenic coastlines in the world"}, {"km": 15, "message": "Amazing Big Sur coastal run completed - what breathtaking views!"}]}', true),

-- Machu Picchu Trail
('Inca Trail to Machu Picchu', 'Ancient Inca pathway through Andes mountains to the lost city', 'Cusco Region, Peru', 'South America', 'run', 26.0, 1200, 'expert', 
'{"elevation_profile": [2400, 2650, 2900, 3150, 3400, 3650, 3900, 4200, 4215, 3900, 3400, 2900, 2650, 2430], "scenery_points": [{"km": 5, "description": "Wayllabamba Village"}, {"km": 12, "description": "Dead Womans Pass - Highest Point"}, {"km": 18, "description": "Runkurakay Ruins"}, {"km": 26, "description": "Machu Picchu Citadel"}], "resistance_profile": [5, 7, 9, 11, 13, 15, 17, 18, 15, 12, 9, 6, 4, 3], "audio_cues": [{"km": 12, "message": "You have reached Dead Womans Pass - the highest point at 4,215 meters!"}, {"km": 26, "message": "Congratulations! You have reached the legendary Machu Picchu citadel!"}]}', true),

-- Great Wall of China
('Great Wall Marathon Route', 'Historic sections of the Great Wall with steep steps and mountain views', 'Huangyaguan, Beijing', 'China', 'run', 21.1, 850, 'hard', 
'{"elevation_profile": [150, 285, 420, 585, 720, 650, 785, 920, 785, 650, 520, 385, 285, 150], "scenery_points": [{"km": 3, "description": "Huangyaguan Fortress"}, {"km": 8, "description": "Great Wall Watchtower"}, {"km": 15, "description": "Restored Ming Dynasty Section"}, {"km": 21, "description": "Great Wall Museum"}], "resistance_profile": [3, 6, 9, 12, 15, 13, 16, 18, 15, 12, 8, 5, 3, 2], "audio_cues": [{"km": 5, "message": "You are running on one of the Seven Wonders of the World!"}, {"km": 21, "message": "Incredible! You have completed the Great Wall Marathon challenge!"}]}', true);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_virtual_trails_search ON virtual_trails USING GIN (to_tsvector('english', name || ' ' || description || ' ' || location));

-- Update timestamps trigger
CREATE OR REPLACE FUNCTION update_virtual_trails_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER virtual_trails_update_timestamp
    BEFORE UPDATE ON virtual_trails
    FOR EACH ROW
    EXECUTE FUNCTION update_virtual_trails_timestamp();