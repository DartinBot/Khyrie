// Khyrie Family & Friends Social Network JavaScript

class FamilyFriendsApp {
    constructor() {
        this.activeTab = 'dashboard';
        this.dashboardData = null;
        this.userGroups = [];
        this.activeChallenges = [];
        this.liveWorkouts = [];
        this.loading = true;
        this.userId = 'user123'; // Would come from authentication
        this.notifications = [];
        this.encouragementQueue = [];
        
        this.init();
    }

    async init() {
        console.log('🏋️‍♂️ Initializing Family & Friends Social Network');
        
        await this.loadDashboardData();
        this.setupEventListeners();
        this.initializeRealTimeUpdates();
        this.startNotificationSystem();
        
        // Initialize UI
        this.renderCurrentTab();
        
        console.log('✅ Family & Friends app initialized');
    }

    async loadDashboardData() {
        try {
            this.showLoadingState();
            
            // Load data in parallel for better performance
            const [dashboardData, groupsData, challengesData, liveData] = await Promise.all([
                this.fetchDashboardData(),
                this.fetchUserGroups(),
                this.fetchActiveChallenges(),
                this.fetchLiveWorkouts()
            ]);
            
            this.dashboardData = dashboardData;
            this.userGroups = groupsData;
            this.activeChallenges = challengesData;
            this.liveWorkouts = liveData;
            
            this.loading = false;
            this.hideLoadingState();
            
        } catch (error) {
            console.error('Error loading dashboard:', error);
            this.loading = false;
            this.loadOfflineData();
        }
    }

  const renderDashboard = () => {
    if (loading) {
      return <div className="loading">Loading family & friends data...</div>;
    }

    if (!dashboardData) {
      return <div className="no-data">No dashboard data available</div>;
    }

    return (
      <div className="dashboard-content">
        {/* Weekly Stats */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-number">{dashboardData.weekly_stats?.group_workouts_completed || 0}</div>
            <div className="stat-label">Group Workouts</div>
            <div className="stat-icon">🏋️‍♂️</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{dashboardData.weekly_stats?.encouragements_sent || 0}</div>
            <div className="stat-label">Encouragements Sent</div>
            <div className="stat-icon">💪</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{dashboardData.weekly_stats?.challenges_participated || 0}</div>
            <div className="stat-label">Active Challenges</div>
            <div className="stat-icon">🏆</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{dashboardData.weekly_stats?.family_fitness_streak || 0}</div>
            <div className="stat-label">Day Streak</div>
            <div className="stat-icon">🔥</div>
          </div>
        </div>

        {/* Social Notifications */}
        <div className="notifications-section">
          <h3>Recent Activity</h3>
          <div className="notifications-list">
            {dashboardData.recent_group_activities?.slice(0, 5).map((activity, index) => (
              <div key={index} className="notification-item">
                <div className="notification-avatar">👤</div>
                <div className="notification-content">
                  <div className="notification-text">
                    {activity.user_id} completed a {activity.workout_type}
                  </div>
                  <div className="notification-time">{activity.completion_time}</div>
                </div>
                <div className="notification-reactions">
                  <span className="reaction-count">❤️ {activity.reactions_count}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="quick-actions">
          <h3>Quick Actions</h3>
          <div className="action-buttons">
            <button className="action-btn primary" onClick={() => setActiveTab('create-group')}>
              👥 Create New Group
            </button>
            <button className="action-btn" onClick={() => setActiveTab('challenges')}>
              🏆 Start Challenge
            </button>
            <button className="action-btn" onClick={() => setActiveTab('workouts')}>
              💪 Share Workout
            </button>
            <button className="action-btn" onClick={() => setActiveTab('live')}>
              📱 Join Live Session
            </button>
          </div>
        </div>
      </div>
    );
  };

  const renderGroups = () => {
    return (
      <div className="groups-content">
        <div className="section-header">
          <h2>My Fitness Groups</h2>
          <button className="btn-primary" onClick={() => setActiveTab('create-group')}>
            Create New Group
          </button>
        </div>

        <div className="groups-grid">
          {userGroups.map((group, index) => (
            <div key={group.group_id} className="group-card">
              <div className="group-header">
                <div className="group-icon">
                  {group.type === 'family' ? '👨‍👩‍👧‍👦' : '👥'}
                </div>
                <div className="group-info">
                  <h3>{group.name}</h3>
                  <p>{group.member_count} members • {group.type}</p>
                </div>
                <div className="group-role">
                  <span className={`role-badge ${group.role}`}>{group.role}</span>
                </div>
              </div>
              
              <div className="group-stats">
                <div className="stat">
                  <span className="stat-value">15</span>
                  <span className="stat-label">Workouts</span>
                </div>
                <div className="stat">
                  <span className="stat-value">3</span>
                  <span className="stat-label">Challenges</span>
                </div>
                <div className="stat">
                  <span className="stat-value">85%</span>
                  <span className="stat-label">Active</span>
                </div>
              </div>
              
              <div className="group-actions">
                <button className="btn-secondary">View Details</button>
                <button className="btn-primary">Start Workout</button>
              </div>
            </div>
          ))}
          
          {userGroups.length === 0 && (
            <div className="no-groups">
              <div className="no-groups-icon">👥</div>
              <h3>No Groups Yet</h3>
              <p>Create your first fitness group to start tracking with family and friends!</p>
              <button className="btn-primary" onClick={() => setActiveTab('create-group')}>
                Create Your First Group
              </button>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderCreateGroup = () => {
    const [groupName, setGroupName] = useState('');
    const [groupType, setGroupType] = useState('family');
    const [description, setDescription] = useState('');
    const [privacyLevel, setPrivacyLevel] = useState('family');
    const [inviteCode, setInviteCode] = useState('');
    const [createSuccess, setCreateSuccess] = useState(false);

    const handleCreateGroup = async (e) => {
      e.preventDefault();
      
      try {
        const response = await fetch('/api/groups/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            group_name: groupName,
            group_type: groupType,
            creator_id: userId,
            description: description,
            privacy_level: privacyLevel,
            initial_members: []
          })
        });

        const result = await response.json();
        
        if (result.group_created) {
          setInviteCode(result.invite_code);
          setCreateSuccess(true);
          // Reload groups
          loadDashboardData();
        }
      } catch (error) {
        console.error('Error creating group:', error);
      }
    };

    if (createSuccess) {
      return (
        <div className="create-success">
          <div className="success-icon">🎉</div>
          <h2>Group Created Successfully!</h2>
          <div className="invite-code-section">
            <h3>Share this invite code with your family/friends:</h3>
            <div className="invite-code">{inviteCode}</div>
            <button className="btn-secondary" onClick={() => navigator.clipboard.writeText(inviteCode)}>
              📋 Copy Code
            </button>
          </div>
          <div className="next-steps">
            <h3>Next Steps:</h3>
            <ul>
              <li>Share the invite code with family/friends</li>
              <li>Set group fitness goals together</li>
              <li>Create shared workout plans</li>
              <li>Start tracking progress as a team</li>
            </ul>
          </div>
          <button className="btn-primary" onClick={() => {
            setCreateSuccess(false);
            setActiveTab('groups');
          }}>
            View My Groups
          </button>
        </div>
      );
    }

    return (
      <div className="create-group-content">
        <h2>Create Fitness Group</h2>
        <form onSubmit={handleCreateGroup} className="create-group-form">
          <div className="form-group">
            <label>Group Name</label>
            <input
              type="text"
              value={groupName}
              onChange={(e) => setGroupName(e.target.value)}
              placeholder="e.g., Smith Family Fitness, Workout Buddies"
              required
            />
          </div>

          <div className="form-group">
            <label>Group Type</label>
            <select value={groupType} onChange={(e) => setGroupType(e.target.value)}>
              <option value="family">Family</option>
              <option value="friends">Friends</option>
              <option value="workout_buddies">Workout Buddies</option>
            </select>
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="What's your group about? Goals, schedule, etc."
              rows="3"
            />
          </div>

          <div className="form-group">
            <label>Privacy Level</label>
            <select value={privacyLevel} onChange={(e) => setPrivacyLevel(e.target.value)}>
              <option value="family">Family Only</option>
              <option value="friends">Friends</option>
              <option value="private">Private (Invite Only)</option>
            </select>
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={() => setActiveTab('groups')}>
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              Create Group
            </button>
          </div>
        </form>
      </div>
    );
  };

  const renderChallenges = () => {
    return (
      <div className="challenges-content">
        <div className="section-header">
          <h2>Family & Friends Challenges</h2>
          <button className="btn-primary">Create New Challenge</button>
        </div>

        <div className="challenges-grid">
          <div className="challenge-card active">
            <div className="challenge-header">
              <div className="challenge-icon">🏃‍♂️</div>
              <div className="challenge-info">
                <h3>Family Step Challenge</h3>
                <p>Most steps in 30 days wins!</p>
              </div>
              <div className="challenge-status">
                <span className="status-badge active">Active</span>
              </div>
            </div>
            
            <div className="challenge-progress">
              <div className="leaderboard-preview">
                <div className="position">
                  <span className="rank">1st</span>
                  <span className="name">Mom</span>
                  <span className="score">85,420 steps</span>
                </div>
                <div className="position current-user">
                  <span className="rank">2nd</span>
                  <span className="name">You</span>
                  <span className="score">82,150 steps</span>
                </div>
                <div className="position">
                  <span className="rank">3rd</span>
                  <span className="name">Dad</span>
                  <span className="score">78,900 steps</span>
                </div>
              </div>
            </div>
            
            <div className="challenge-footer">
              <div className="time-remaining">3 days left</div>
              <button className="btn-primary">View Full Leaderboard</button>
            </div>
          </div>

          <div className="challenge-card">
            <div className="challenge-header">
              <div className="challenge-icon">💪</div>
              <div className="challenge-info">
                <h3>Workout Frequency Challenge</h3>
                <p>Most workouts completed this month</p>
              </div>
              <div className="challenge-status">
                <span className="status-badge active">Active</span>
              </div>
            </div>
            
            <div className="challenge-progress">
              <div className="progress-bar">
                <div className="progress-fill" style={{width: '68%'}}></div>
              </div>
              <div className="progress-text">17/25 workouts (68%)</div>
            </div>
            
            <div className="challenge-footer">
              <div className="time-remaining">12 days left</div>
              <button className="btn-secondary">Join Challenge</button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderLiveWorkouts = () => {
    return (
      <div className="live-workouts-content">
        <h2>Live Group Workouts</h2>
        
        <div className="live-sessions">
          <div className="session-card active">
            <div className="session-header">
              <div className="user-avatar">👨</div>
              <div className="session-info">
                <h3>Dad's Morning Strength Training</h3>
                <p>Started 25 minutes ago • Upper body focus</p>
              </div>
              <div className="session-status">
                <span className="status-dot active"></span>
                <span>Live</span>
              </div>
            </div>
            
            <div className="session-progress">
              <div className="exercise-current">
                Currently: Bench Press (Set 3/4)
              </div>
              <div className="session-stats">
                <span>⏱️ 25 min</span>
                <span>💪 8/12 exercises</span>
                <span>🔥 Est. 340 cal</span>
              </div>
            </div>
            
            <div className="session-actions">
              <button className="btn-secondary">💬 Send Encouragement</button>
              <button className="btn-primary">🏋️‍♂️ Join Workout</button>
            </div>
          </div>

          <div className="session-card">
            <div className="session-header">
              <div className="user-avatar">👩</div>
              <div className="session-info">
                <h3>Mom's Evening Yoga</h3>
                <p>Scheduled for 7:00 PM • 45 min session</p>
              </div>
              <div className="session-status">
                <span className="status-dot scheduled"></span>
                <span>Scheduled</span>
              </div>
            </div>
            
            <div className="session-actions">
              <button className="btn-secondary">🔔 Set Reminder</button>
              <button className="btn-primary">📝 Join Session</button>
            </div>
          </div>
        </div>

        <div className="encouragement-section">
          <h3>Send Quick Encouragement</h3>
          <div className="encouragement-buttons">
            <button className="encouragement-btn">💪 Keep going!</button>
            <button className="encouragement-btn">🔥 You've got this!</button>
            <button className="encouragement-btn">⚡ Beast mode!</button>
            <button className="encouragement-btn">🏆 Crushing it!</button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="family-friends-page">
      <div className="page-header">
        <h1>Family & Friends Fitness</h1>
        <p>Track workouts, share progress, and stay motivated together</p>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          📊 Dashboard
        </button>
        <button 
          className={`tab ${activeTab === 'groups' ? 'active' : ''}`}
          onClick={() => setActiveTab('groups')}
        >
          👥 My Groups
        </button>
        <button 
          className={`tab ${activeTab === 'challenges' ? 'active' : ''}`}
          onClick={() => setActiveTab('challenges')}
        >
          🏆 Challenges
        </button>
        <button 
          className={`tab ${activeTab === 'live' ? 'active' : ''}`}
          onClick={() => setActiveTab('live')}
        >
          📱 Live Workouts
        </button>
        <button 
          className={`tab ${activeTab === 'create-group' ? 'active' : ''}`}
          onClick={() => setActiveTab('create-group')}
        >
          ➕ Create Group
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'dashboard' && renderDashboard()}
        {activeTab === 'groups' && renderGroups()}
        {activeTab === 'challenges' && renderChallenges()}
        {activeTab === 'live' && renderLiveWorkouts()}
        {activeTab === 'create-group' && renderCreateGroup()}
      </div>
    </div>
  );
};

export default FamilyFriends;