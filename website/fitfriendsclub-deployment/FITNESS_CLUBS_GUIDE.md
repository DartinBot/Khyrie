# Fitness Clubs & Equipment Integration

## 🏃‍♀️ Overview

FitFriendsClubs now supports **virtual fitness clubs** with **real equipment integration**, enabling users to participate in group workouts using their treadmills, stationary bikes, and other connected fitness equipment. This creates an immersive, social fitness experience where users can compete, motivate each other, and achieve their fitness goals together.

## 🎯 Features

### 1. **Fitness Clubs**
- **Multiple Categories**: Run Club, Cycle Club, Pilates Club, Yoga Club, Strength Club, HIIT Squad, etc.
- **Club Management**: Create, join, leave clubs with member limits and admin controls
- **Community Building**: Member directories, club activity feeds, and social interactions

### 2. **Group Workout Sessions**
- **Scheduled Sessions**: Instructors can create live group workouts
- **Equipment Sync**: Real-time synchronization with treadmills, bikes, and other equipment
- **Live Competition**: Real-time leaderboards during group sessions
- **Performance Tracking**: Detailed metrics and progress tracking

### 3. **Equipment Integration**
- **Supported Equipment**:
  - Treadmills (Peloton, NordicTrack, etc.)
  - Stationary Bikes (Peloton, Echelon, etc.)
  - Elliptical Machines
  - Rowing Machines
  - Smart Trainers (Zwift-compatible)

### 4. **Smart Features**
- **Real-time Data Sync**: Speed, distance, heart rate, resistance, calories
- **Automatic Scoring**: Performance-based leaderboards
- **Progress Analytics**: Historical data and improvement tracking
- **Social Competition**: Compare with friends and club members

## 🔌 API Endpoints

### Club Management

#### Get Fitness Clubs
```http
GET /api/clubs?category=run
```
**Response:**
```json
{
  "clubs": [
    {
      "id": 1,
      "name": "Morning Runners Club",
      "description": "Early bird runners who love to start the day with energy!",
      "category": "run",
      "equipment_type": "treadmill",
      "member_count": 25,
      "max_members": 50,
      "creator_name": "john_doe"
    }
  ]
}
```

#### Create Fitness Club
```http
POST /api/clubs
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Evening Cyclists",
  "description": "After-work cycling sessions for stress relief",
  "category": "cycle",
  "equipment_type": "stationary_bike",
  "max_members": 30
}
```

#### Join/Leave Club
```http
POST /api/clubs/{club_id}/join
POST /api/clubs/{club_id}/leave
```

### Group Sessions

#### Get Group Sessions
```http
GET /api/clubs/sessions?club_id=1&upcoming=true
```

#### Create Group Session
```http
POST /api/clubs/sessions
Content-Type: application/json
Authorization: Bearer <token>

{
  "club_id": 1,
  "title": "5K Virtual Race",
  "description": "Competitive 5K run with live leaderboard",
  "start_time": "2025-10-02T07:00:00Z",
  "duration_minutes": 30,
  "max_participants": 20,
  "equipment_settings": {
    "target_distance": 5,
    "difficulty": "moderate",
    "incline_range": [0, 5],
    "speed_range": [6, 12]
  }
}
```

### Equipment Integration

#### Connect Equipment
```http
POST /api/equipment/connect
Content-Type: application/json
Authorization: Bearer <token>

{
  "equipment_type": "treadmill",
  "equipment_id": "peloton_tread_123456",
  "brand": "Peloton",
  "model": "Tread+",
  "connection_data": {
    "bluetooth_id": "AA:BB:CC:DD:EE:FF",
    "api_key": "encrypted_api_key",
    "firmware_version": "1.2.3"
  }
}
```

#### Sync Workout Data
```http
POST /api/equipment/sync
Content-Type: application/json
Authorization: Bearer <token>

{
  "session_id": 101,
  "equipment_id": "peloton_tread_123456",
  "workout_data": {
    "duration_seconds": 1800,
    "distance": 3.1,
    "calories_burned": 285,
    "avg_heart_rate": 145,
    "max_heart_rate": 165,
    "speed_data": [6.0, 6.5, 7.0, 6.8, 7.2],
    "resistance_data": [2, 3, 4, 3, 5],
    "timestamps": ["2025-10-02T07:00:00Z", "2025-10-02T07:05:00Z"]
  }
}
```

## 🏋️‍♀️ Equipment Integration Examples

### Treadmill Integration
```javascript
// Example: Peloton Treadmill Integration
class PelotonTreadmillConnector {
  async connect() {
    // Bluetooth/WiFi connection to treadmill
    const device = await navigator.bluetooth.requestDevice({
      filters: [{ services: ['peloton-treadmill-service'] }]
    });
    // Initialize connection and sync capabilities
  }
  
  async syncWorkoutData(sessionId) {
    // Real-time data streaming during workout
    const workoutData = {
      duration_seconds: this.getCurrentDuration(),
      distance: this.getCurrentDistance(),
      speed_data: this.getSpeedHistory(),
      heart_rate: this.getCurrentHeartRate()
    };
    
    // Send to FitFriendsClubs API
    await fetch('/api/equipment/sync', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${userToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        session_id: sessionId,
        equipment_id: this.deviceId,
        workout_data: workoutData
      })
    });
  }
}
```

### Stationary Bike Integration
```javascript
// Example: Smart Bike Integration
class SmartBikeConnector {
  async startGroupSession(sessionConfig) {
    // Configure bike based on session parameters
    await this.setResistanceRange(sessionConfig.resistance_range);
    await this.setCadenceTarget(sessionConfig.cadence_target);
    
    // Start real-time data sync
    this.startDataSync();
  }
  
  async updateLeaderboard() {
    // Get current performance metrics
    const metrics = {
      distance: this.totalDistance,
      avg_power: this.averagePower,
      calories: this.caloriesBurned
    };
    
    // Sync with group session
    await this.syncToSession(metrics);
  }
}
```

## 📊 Workout Data Structure

### Equipment Workout Data
```json
{
  "user_id": 123,
  "session_id": 456,
  "equipment_id": "peloton_bike_789",
  "duration_seconds": 2700,
  "distance": 12.5,
  "calories_burned": 340,
  "avg_heart_rate": 152,
  "max_heart_rate": 178,
  "speed_data": [15.2, 16.1, 15.8, 17.2, 16.5],
  "resistance_data": [8, 10, 12, 10, 14],
  "timestamps": [
    "2025-10-02T07:00:00Z",
    "2025-10-02T07:05:00Z",
    "2025-10-02T07:10:00Z"
  ]
}
```

### Session Leaderboard
```json
{
  "session_id": 456,
  "leaderboard": [
    {
      "user_id": 123,
      "username": "speedster_mike",
      "rank": 1,
      "score": 1250,
      "distance": 12.5,
      "calories": 340,
      "duration_seconds": 2700
    },
    {
      "user_id": 124,
      "username": "fitness_sarah",
      "rank": 2,
      "score": 1180,
      "distance": 11.8,
      "calories": 315,
      "duration_seconds": 2700
    }
  ]
}
```

## 🎮 User Experience Flow

### 1. **Join a Fitness Club**
- Browse available clubs by category (Run, Cycle, Pilates, etc.)
- View club details, member count, and upcoming sessions
- Join clubs that match your interests and equipment

### 2. **Connect Your Equipment**
- Link treadmill, bike, or other smart fitness equipment
- Verify connection and calibrate settings
- Test data sync capabilities

### 3. **Join Group Sessions**
- Browse upcoming sessions in your clubs
- Register for sessions that fit your schedule
- Prepare equipment with session-specific settings

### 4. **Participate in Live Workouts**
- Start workout session on your equipment
- View live leaderboard and competitor progress
- Receive real-time motivation and coaching cues
- Track personal metrics and performance

### 5. **Post-Workout Analysis**
- Review detailed performance analytics
- Compare with previous sessions and personal records
- Share achievements with club members
- Plan future workouts and set new goals

## 🔧 Technical Implementation

### Equipment Connection Protocols
- **Bluetooth Low Energy (BLE)**: For wireless equipment communication
- **WiFi API Integration**: For smart equipment with built-in connectivity
- **ANT+ Protocol**: For cycling computers and heart rate monitors
- **Zwift Integration**: For smart trainers and cycling platforms

### Real-time Data Streaming
- **WebSocket Connections**: For live data updates during sessions
- **MQTT Protocol**: For IoT device communication
- **Real-time Analytics**: Live performance calculations and leaderboard updates

### Supported Equipment Brands
- **Treadmills**: Peloton, NordicTrack, Bowflex, ProForm
- **Bikes**: Peloton, Echelon, SoulCycle, Schwinn
- **Smart Trainers**: Wahoo, Tacx, Elite, Saris
- **Wearables**: Apple Watch, Garmin, Fitbit, Polar

## 🚀 Getting Started

1. **Database Setup**: Run the `fitness-clubs-schema.sql` to create required tables
2. **Deploy Worker**: Upload the updated `cloudflare-worker.js` with club endpoints
3. **Equipment Integration**: Implement device-specific connectors for your supported equipment
4. **Frontend Integration**: Add club browsing, session joining, and live workout interfaces
5. **Testing**: Test with simulated equipment data before connecting real devices

## 🗺️ **Virtual Trails System**

### **World-Famous Virtual Routes**

Experience the world's most iconic trails from your home equipment! Our virtual trails system brings famous routes to your treadmill or bike with:

#### **🏃‍♀️ Running Trails**
- **Central Park Loop** (New York) - 9.7km with Manhattan skyline views
- **Thames Path Marathon** (London) - 42.2km past Tower Bridge, Big Ben & London Eye  
- **Golden Gate Bridge to Sausalito** - 13.2km with stunning San Francisco Bay views
- **Boston Freedom Trail** - 4km through Revolutionary War historic sites
- **Big Sur Coastal Highway** - 15.8km dramatic Pacific Coast cliffs
- **Inca Trail to Machu Picchu** - 26km ancient pathway through Andes mountains
- **Great Wall Marathon Route** - 21.1km on historic Great Wall sections

#### **🚴‍♀️ Cycling Trails**
- **Alpe d'Huez Climb** (France) - 13.8km legendary Tour de France mountain climb
- **Amsterdam Canal Ring** - 12.5km UNESCO World Heritage canal district
- **Napa Valley Wine Route** - 28.5km through world-famous wine country
- **Tuscany Hill Country** - 45.2km classic Italian countryside with medieval villages

### **Trail Features**
- **Real Elevation Profiles**: Equipment adjusts incline/resistance to match actual terrain
- **Scenic Checkpoints**: Virtual landmarks and points of interest along the route
- **Audio Commentary**: Historical facts and motivational cues during your journey
- **Weather Simulation**: Optional weather effects matching the real location
- **360° Video**: Immersive video of actual trail scenery (premium feature)

### **Virtual Trails API**

#### Browse Virtual Trails
```http
GET /api/trails?activity_type=run&difficulty=moderate&location=usa&featured=true
```

#### Get Trail Details with Leaderboard
```http
GET /api/trails/123
```
**Response:**
```json
{
  "trail": {
    "id": 123,
    "name": "Central Park Loop",
    "location": "Central Park, New York",
    "country": "USA",
    "distance_km": 9.7,
    "elevation_gain_m": 175,
    "difficulty": "moderate",
    "total_sessions": 2547,
    "total_participants": 892
  },
  "leaderboard": [
    {
      "rank": 1,
      "username": "marathon_mike",
      "completion_time_seconds": 2145,
      "avg_speed_kmh": 16.2
    }
  ],
  "recent_sessions": [...],
  "statistics": {...}
}
```

#### Start Virtual Trail Session
```http
POST /api/trails/sessions
Content-Type: application/json
Authorization: Bearer <token>

{
  "trail_id": 123,
  "equipment_id": "peloton_tread_456",
  "session_mode": "solo"
}
```

**Response includes equipment configuration:**
```json
{
  "session": {...},
  "trail_info": {...},
  "equipment_config": {
    "incline_profile": [0, 1.5, 2.5, 3.5, 4.2, 3.8, 4.5, 5.5, 4.8, 3.2],
    "resistance_profile": [2, 3, 4, 5, 6, 5, 6, 7, 6, 4],
    "scenery_checkpoints": [
      {"km": 2.4, "description": "Reservoir with Manhattan views"},
      {"km": 4.8, "description": "Great Lawn"}
    ],
    "audio_cues": [
      {"km": 1, "message": "You're passing Sheep Meadow, keep your steady pace!"}
    ]
  }
}
```

### **Trail Equipment Integration**

#### Treadmill Configuration
```javascript
// Auto-adjust incline based on trail elevation
const configureTrail = async (trailConfig) => {
  for (let checkpoint of trailConfig.incline_profile) {
    await treadmill.setIncline(checkpoint.incline);
    await treadmill.setSpeed(checkpoint.target_speed);
    
    // Display scenery at key points
    if (checkpoint.scenery) {
      showSceneryImage(checkpoint.scenery.image_url);
      playAudioCue(checkpoint.scenery.description);
    }
  }
};
```

#### Cycling Resistance Mapping
```javascript
// Map trail difficulty to bike resistance
const mapTrailToBike = (elevation_gain, distance_km) => {
  const gradient = elevation_gain / (distance_km * 1000) * 100;
  
  if (gradient < 3) return 'flat_road';
  if (gradient < 6) return 'rolling_hills';  
  if (gradient < 10) return 'steep_climb';
  return 'mountain_pass';
};
```

## 🏆 **Trail Achievements System**

### **Achievement Types**
- **Trail Pioneer**: First to complete a newly added trail
- **Speed Demon**: Top 10 fastest completion on any trail  
- **World Explorer**: Complete trails from 5+ different countries
- **Elevation Master**: Climb 10,000+ meters across all trails
- **Consistency King**: Complete same trail 10+ times
- **Marathon Legends**: Complete all marathon-distance trails

### **Global Leaderboards**
```http
GET /api/trails/leaderboard?activity_type=run&period=month
```

- **Trail-Specific**: Best times for individual routes
- **Global Rankings**: Top performers across all trails
- **Country Leaderboards**: Best times by nationality  
- **Club Competitions**: Club vs club trail challenges
- **Seasonal Challenges**: Monthly featured trail competitions

## 🌍 **Immersive Experience Features**

### **Real-World Integration**
- **Live Weather**: Match current weather conditions at trail location
- **Time of Day**: Adjust lighting to match actual local time
- **Seasonal Changes**: Different scenery based on current season
- **Local Audio**: Ambient sounds from actual trail environment

### **Social Features**  
- **Group Trail Runs**: Multiple users on same trail simultaneously
- **Ghost Runners**: Race against previous performances
- **Trail Reviews**: User ratings and tips for each route
- **Photo Sharing**: Share virtual screenshots at scenic checkpoints

### **Premium Features**
- **4K Trail Videos**: Ultra-high-definition trail footage
- **VR Integration**: Full virtual reality trail experience
- **Personal Coaching**: AI-powered pacing and technique tips
- **Custom Trails**: Upload your own local routes for others

This comprehensive fitness clubs system with virtual trails transforms your platform into a complete social fitness ecosystem where users can connect, compete, and achieve their fitness goals together using their real equipment while exploring the world's most beautiful routes! 🏆🗺️