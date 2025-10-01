-- Live Video Streaming Database Schema for FitFriendsClubs
-- Add these tables to support live video streaming for group sessions

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

-- Notifications Table (if not exists)
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

-- Stream Quality Settings
CREATE TABLE IF NOT EXISTS stream_settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    preferred_quality VARCHAR(20) DEFAULT 'HD',
    auto_quality BOOLEAN DEFAULT true,
    chat_enabled BOOLEAN DEFAULT true,
    notifications_enabled BOOLEAN DEFAULT true,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_streaming_sessions_status ON streaming_sessions(status);
CREATE INDEX IF NOT EXISTS idx_streaming_sessions_group_session ON streaming_sessions(group_session_id);
CREATE INDEX IF NOT EXISTS idx_stream_viewers_session ON stream_viewers(streaming_session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session ON chat_messages(streaming_session_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user_unread ON notifications(user_id, is_read);

-- Sample data for testing
INSERT INTO stream_settings (user_id, preferred_quality, auto_quality, chat_enabled) 
VALUES 
(1, 'HD', true, true),
(2, '4K', false, true),
(3, 'SD', true, false)
ON CONFLICT (user_id) DO NOTHING;

-- Sample streaming session (uncomment when you have group sessions)
/*
INSERT INTO streaming_sessions (
    group_session_id, host_user_id, stream_key, room_id, 
    stream_title, stream_description, max_viewers, status
) VALUES (
    1, 1, 'stream_key_123', 'room_abc_123',
    'Morning Yoga Flow - Live Session', 
    'Join us for a peaceful morning yoga session with breathing exercises and gentle stretches.',
    50, 'created'
);
*/