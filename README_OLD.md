# 👨‍👩‍👧‍👦 Family & Friends Fitness Tracking System

A comprehensive collaborative fitness tracking platform that enables families and friends to workout together, share progress, create challenges, and stay motivated as a group.

## 🌟 Key Features

### 👥 **Group Management**
- **Create Family Groups**: Set up fitness groups for family members
- **Friend Networks**: Connect with workout buddies and friends
- **Invite System**: Easy invite codes for joining groups
- **Privacy Controls**: Manage who sees your fitness data
- **Role Management**: Admin and member roles for group organization

### 🏋️‍♂️ **Shared Workouts**
- **Workout Creator**: Build custom workouts to share with groups
- **Exercise Library**: Pre-built exercises for different workout types
- **Workout Templates**: Save and reuse favorite workout routines
- **Difficulty Levels**: Beginner, intermediate, and advanced options
- **Exercise Variations**: Modifications for different fitness levels

### 🏆 **Group Challenges**
- **Challenge Types**: Step count, workout frequency, strength goals
- **Leaderboards**: Real-time rankings and progress tracking
- **Custom Metrics**: Set personalized challenge targets
- **Rewards System**: Virtual achievements and bragging rights
- **Time-Based**: Daily, weekly, and monthly challenges

### 📱 **Live Workout Tracking**
- **Real-Time Sessions**: Track workouts as they happen
- **Group Notifications**: Alert family/friends when you start working out
- **Live Updates**: See progress and encourage others in real-time
- **Social Reactions**: Send encouragement and motivation
- **Session Sharing**: Automatically share completed workouts

### 📊 **Social Dashboard**
- **Activity Feed**: See what family/friends are up to
- **Progress Tracking**: Monitor group and individual achievements
- **Weekly Stats**: Group workout completion and participation
- **Milestone Celebrations**: Celebrate achievements together
- **Motivation System**: Built-in encouragement tools

## 🚀 Getting Started

### Backend Setup (FastAPI)

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Backend Server**
   ```bash
   python backend_family_api.py
   ```
   
   Server will start at: `http://localhost:8000`

### Frontend Setup (React)

1. **Install Node Dependencies**
   ```bash
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm start
   ```
   
   App will open at: `http://localhost:3000`

## 📁 Project Structure

```
family-friends-fitness/
├── 🐍 Backend (FastAPI)
│   ├── family_friends_tools.py      # Core business logic
│   ├── backend_family_api.py        # API endpoints
│   └── requirements.txt             # Python dependencies
├── ⚛️ Frontend (React)
│   ├── FamilyFriends.js            # Main dashboard component
│   ├── FamilyFriends.css           # Dashboard styles
│   ├── SharedWorkout.js            # Workout creation component
│   ├── SharedWorkout.css           # Workout creator styles
│   └── package.json                # Node dependencies
└── 📚 Documentation
    └── README.md                    # This file
```

## 🔧 API Endpoints

### Group Management
- `POST /api/groups/create` - Create new fitness group
- `POST /api/groups/join` - Join group with invite code
- `GET /api/groups/user/{user_id}` - Get user's groups

### Shared Workouts
- `POST /api/workouts/shared/create` - Create shared workout
- `GET /api/workouts/shared/group/{group_id}` - Get group workouts

### Workout Sessions
- `POST /api/sessions/start` - Start group workout session
- `POST /api/sessions/complete` - Complete workout session
- `GET /api/sessions/live/{session_id}` - Get live session updates

### Challenges
- `POST /api/challenges/create` - Create group challenge
- `GET /api/challenges/group/{group_id}` - Get group challenges
- `GET /api/challenges/leaderboard/{challenge_id}` - Get challenge rankings

### Social Features
- `GET /api/dashboard/family-friends/{user_id}` - Get social dashboard
- `POST /api/social/react/{session_id}` - React to workout session
- `GET /api/groups/{group_id}/activity` - Get group activity feed

## 💡 Usage Examples

### 1. Creating a Family Group

```javascript
// Create a family fitness group
const createGroup = async () => {
  const response = await fetch('/api/groups/create', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      group_name: "Smith Family Fitness",
      group_type: "family",
      creator_id: "user123",
      description: "Daily family workouts to stay healthy together!",
      privacy_level: "family"
    })
  });
  const result = await response.json();
  console.log('Invite Code:', result.invite_code);
};
```

### 2. Starting a Group Challenge

```javascript
// Create a 30-day step challenge
const createChallenge = async () => {
  const response = await fetch('/api/challenges/create', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      creator_id: "user123",
      group_id: "group_1",
      challenge_name: "Family Step Challenge",
      challenge_type: "step_count",
      duration_days: 30,
      target_metrics: { daily_steps: 10000 }
    })
  });
};
```

### 3. Sharing a Workout

```javascript
// Create a shared strength workout
const shareWorkout = async () => {
  const workout = {
    creator_id: "user123",
    workout_name: "Family Strength Training",
    workout_type: "strength",
    exercises: [
      {
        name: "Squats",
        sets: 3,
        reps: 15,
        rest_seconds: 60
      },
      {
        name: "Push-ups",
        sets: 3,
        reps: 12,
        rest_seconds: 45
      }
    ],
    share_with_groups: ["group_1"],
    difficulty: "beginner",
    estimated_duration: 45
  };
  
  const response = await fetch('/api/workouts/shared/create', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(workout)
  });
};
```

## 🎨 UI Components

### Dashboard Features
- **📊 Weekly Stats**: Group workout counts, encouragements sent, active challenges
- **📱 Social Feed**: Recent family/friend workout activities
- **⚡ Quick Actions**: Create group, start challenge, share workout
- **🏆 Challenge Updates**: Active challenge standings and progress

### Group Management
- **👥 Group Cards**: Visual group overview with member count and stats
- **🎯 Role Badges**: Admin and member role indicators
- **📈 Group Analytics**: Collective progress and achievements
- **💬 Activity Feed**: Real-time group workout updates

### Workout Creation
- **🏋️‍♂️ Exercise Builder**: Drag-and-drop workout creator
- **📚 Exercise Library**: Pre-populated exercise database
- **⚙️ Customization**: Sets, reps, weight, duration settings
- **🏷️ Tagging System**: Organize workouts with custom tags

## 🔐 Privacy & Security

- **Group Privacy**: Family, friends, or private sharing levels
- **User Controls**: Individual privacy settings per workout
- **Invite-Only Groups**: Secure group joining via invite codes
- **Data Protection**: User workout data isolated by group membership

## 🚀 Future Enhancements

### Phase 2 Features
- **🎥 Video Workouts**: Share workout videos with family/friends
- **📍 Location Sharing**: Find nearby family members for group workouts
- **💬 Group Chat**: In-app messaging for workout coordination
- **📅 Workout Calendar**: Schedule group workout sessions
- **🏅 Achievement System**: Unlock badges and rewards

### Phase 3 Features
- **🤖 AI Coach**: Personalized workout suggestions for groups
- **📊 Advanced Analytics**: Detailed progress tracking and insights
- **🎮 Gamification**: Points, levels, and competitive elements
- **📱 Mobile App**: Native iOS and Android applications
- **⌚ Wearable Integration**: Apple Watch and Fitbit sync

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/family-challenges`)
3. Commit changes (`git commit -m 'Add family challenge system'`)
4. Push to branch (`git push origin feature/family-challenges`)
5. Open Pull Request

## 📞 Support

For questions or support:
- **Email**: support@familyfitness.app
- **Issues**: Create GitHub issue
- **Documentation**: See `/docs` folder

## 📄 License

MIT License - see LICENSE file for details

---

**Built with ❤️ for families and friends who want to stay fit together!**

*Transform your fitness journey from a solo adventure into a shared family experience. Because fitness is better together!* 🏃‍♀️👨‍👩‍👧‍👦💪