import React, { useState, useEffect } from 'react';
import './SocialFitness.css';

const SocialFitness = () => {
  const [activeTab, setActiveTab] = useState('feed');
  const [workoutFeed, setWorkoutFeed] = useState([]);
  const [challenges, setChallenges] = useState([]);
  const [friends, setFriends] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const userId = 'user_001'; // In real app, get from auth context

  useEffect(() => {
    loadSocialData();
  }, [activeTab]);

  const loadSocialData = async () => {
    try {
      setLoading(true);
      
      // Mock data - in real app, these would be API calls
      if (activeTab === 'feed') {
        setWorkoutFeed([
          {
            id: 1,
            user: { name: 'Alex Johnson', avatar: '👨‍💼', level: 'Advanced' },
            activity: 'completed a strength workout',
            details: 'Deadlift 3×5 @ 180kg • Squat 3×8 @ 140kg',
            time: '2 hours ago',
            likes: 12,
            comments: 3,
            achievements: ['💪 New PR!']
          },
          {
            id: 2,
            user: { name: 'Sarah Miller', avatar: '👩‍💻', level: 'Intermediate' },
            activity: 'finished a 5K run',
            details: '5.2km in 24:15 - Personal best!',
            time: '4 hours ago',
            likes: 8,
            comments: 5,
            achievements: ['🏃‍♀️ 5K PR', '🔥 Week Streak: 5']
          },
          {
            id: 3,
            user: { name: 'Mike Chen', avatar: '👨‍🎓', level: 'Beginner' },
            activity: 'completed first workout',
            details: 'Full body beginner routine - 45 minutes',
            time: '6 hours ago',
            likes: 15,
            comments: 8,
            achievements: ['🎉 First Workout!']
          }
        ]);
      } else if (activeTab === 'challenges') {
        setChallenges([
          {
            id: 1,
            name: '30-Day Push-up Challenge',
            description: 'Build upper body strength with daily push-ups',
            participants: 127,
            daysLeft: 15,
            myProgress: 65,
            target: 100,
            reward: '🏆 Push-up Champion Badge'
          },
          {
            id: 2,
            name: 'Weekly Distance Goal',
            description: 'Run or walk 25km this week',
            participants: 89,
            daysLeft: 3,
            myProgress: 18.5,
            target: 25,
            reward: '🏃‍♀️ Distance Warrior'
          },
          {
            id: 3,
            name: 'Strength Milestone',
            description: 'Reach 1.5x bodyweight deadlift',
            participants: 45,
            daysLeft: 60,
            myProgress: 1.2,
            target: 1.5,
            reward: '💪 Strength Master'
          }
        ]);
      } else if (activeTab === 'friends') {
        setFriends([
          {
            id: 1,
            name: 'Emma Watson',
            avatar: '👩‍🦰',
            status: 'Currently working out',
            lastActive: 'Active now',
            weeklyWorkouts: 5,
            level: 'Advanced',
            commonGoals: ['Strength', 'Weight Loss']
          },
          {
            id: 2,
            name: 'David Kim',
            avatar: '👨‍💼',
            status: 'Rest day recovery',
            lastActive: '2 hours ago',
            weeklyWorkouts: 4,
            level: 'Intermediate',
            commonGoals: ['Endurance', 'Muscle Gain']
          },
          {
            id: 3,
            name: 'Lisa Rodriguez',
            avatar: '👩‍🎨',
            status: 'Planning next workout',
            lastActive: '1 day ago',
            weeklyWorkouts: 3,
            level: 'Beginner',
            commonGoals: ['General Fitness']
          }
        ]);
      } else if (activeTab === 'leaderboard') {
        setLeaderboard([
          { rank: 1, name: 'Chris Thompson', avatar: '👨‍💻', points: 2450, badge: '🏆' },
          { rank: 2, name: 'Anna Martinez', avatar: '👩‍🔬', points: 2398, badge: '🥈' },
          { rank: 3, name: 'You', avatar: '😊', points: 2201, badge: '🥉' },
          { rank: 4, name: 'James Wilson', avatar: '👨‍🎓', points: 2156, badge: '⭐' },
          { rank: 5, name: 'Sophie Lee', avatar: '👩‍💼', points: 2089, badge: '⭐' }
        ]);
      }
    } catch (err) {
      console.error('Error loading social data:', err);
    } finally {
      setLoading(false);
    }
  };

  const likePost = (postId) => {
    setWorkoutFeed(feed => 
      feed.map(post => 
        post.id === postId 
          ? { ...post, likes: post.likes + 1 }
          : post
      )
    );
  };

  const joinChallenge = (challengeId) => {
    setChallenges(challenges => 
      challenges.map(challenge => 
        challenge.id === challengeId 
          ? { ...challenge, participants: challenge.participants + 1 }
          : challenge
      )
    );
  };

  const TabButton = ({ tabId, icon, label, isActive, onClick }) => (
    <button
      className={`tab-button ${isActive ? 'active' : ''}`}
      onClick={() => onClick(tabId)}
    >
      <span className="tab-icon">{icon}</span>
      <span className="tab-label">{label}</span>
    </button>
  );

  const WorkoutFeedItem = ({ post }) => (
    <div className="feed-item">
      <div className="feed-header">
        <div className="user-info">
          <span className="user-avatar">{post.user.avatar}</span>
          <div className="user-details">
            <h4>{post.user.name}</h4>
            <span className="user-level">{post.user.level}</span>
          </div>
        </div>
        <span className="post-time">{post.time}</span>
      </div>
      
      <div className="feed-content">
        <p><strong>{post.user.name}</strong> {post.activity}</p>
        <div className="activity-details">{post.details}</div>
        
        {post.achievements.length > 0 && (
          <div className="achievements">
            {post.achievements.map((achievement, index) => (
              <span key={index} className="achievement-badge">
                {achievement}
              </span>
            ))}
          </div>
        )}
      </div>
      
      <div className="feed-actions">
        <button 
          className="action-btn like-btn"
          onClick={() => likePost(post.id)}
        >
          ❤️ {post.likes}
        </button>
        <button className="action-btn comment-btn">
          💬 {post.comments}
        </button>
        <button className="action-btn share-btn">
          🔗 Share
        </button>
      </div>
    </div>
  );

  const ChallengeCard = ({ challenge }) => (
    <div className="challenge-card">
      <div className="challenge-header">
        <h3>{challenge.name}</h3>
        <span className="days-left">{challenge.daysLeft} days left</span>
      </div>
      
      <p className="challenge-description">{challenge.description}</p>
      
      <div className="challenge-stats">
        <div className="stat-item">
          <label>Participants</label>
          <span>{challenge.participants}</span>
        </div>
        <div className="stat-item">
          <label>My Progress</label>
          <span>{challenge.myProgress}/{challenge.target}</span>
        </div>
      </div>
      
      <div className="progress-section">
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ width: `${(challenge.myProgress / challenge.target) * 100}%` }}
          ></div>
        </div>
        <span className="progress-text">
          {Math.round((challenge.myProgress / challenge.target) * 100)}% Complete
        </span>
      </div>
      
      <div className="challenge-reward">
        <span>Reward: {challenge.reward}</span>
      </div>
      
      <button className="join-challenge-btn" onClick={() => joinChallenge(challenge.id)}>
        🎯 Join Challenge
      </button>
    </div>
  );

  const FriendCard = ({ friend }) => (
    <div className="friend-card">
      <div className="friend-header">
        <span className="friend-avatar">{friend.avatar}</span>
        <div className="friend-info">
          <h4>{friend.name}</h4>
          <span className="friend-level">{friend.level}</span>
        </div>
        <div className={`status-indicator ${friend.lastActive === 'Active now' ? 'active' : ''}`}></div>
      </div>
      
      <div className="friend-status">
        <p>{friend.status}</p>
        <span className="last-active">{friend.lastActive}</span>
      </div>
      
      <div className="friend-stats">
        <div className="stat">
          <label>Weekly Workouts</label>
          <span>{friend.weeklyWorkouts}</span>
        </div>
      </div>
      
      <div className="common-goals">
        <label>Common Goals:</label>
        <div className="goal-tags">
          {friend.commonGoals.map((goal, index) => (
            <span key={index} className="goal-tag">{goal}</span>
          ))}
        </div>
      </div>
      
      <div className="friend-actions">
        <button className="friend-action-btn">💬 Message</button>
        <button className="friend-action-btn">🏋️ Workout Together</button>
      </div>
    </div>
  );

  const LeaderboardItem = ({ entry }) => (
    <div className={`leaderboard-item ${entry.name === 'You' ? 'current-user' : ''}`}>
      <div className="rank-badge">
        <span className="rank-number">#{entry.rank}</span>
        <span className="rank-icon">{entry.badge}</span>
      </div>
      
      <div className="user-info">
        <span className="user-avatar">{entry.avatar}</span>
        <span className="user-name">{entry.name}</span>
      </div>
      
      <div className="points-display">
        <span className="points">{entry.points.toLocaleString()}</span>
        <span className="points-label">pts</span>
      </div>
    </div>
  );

  return (
    <div className="social-fitness">
      <header className="social-header">
        <h1>👥 Social Fitness Hub</h1>
        <p>Connect, compete, and achieve together</p>
      </header>

      {/* Navigation Tabs */}
      <nav className="social-nav">
        <TabButton
          tabId="feed"
          icon="📱"
          label="Activity Feed"
          isActive={activeTab === 'feed'}
          onClick={setActiveTab}
        />
        <TabButton
          tabId="challenges"
          icon="🎯"
          label="Challenges"
          isActive={activeTab === 'challenges'}
          onClick={setActiveTab}
        />
        <TabButton
          tabId="friends"
          icon="👫"
          label="Friends"
          isActive={activeTab === 'friends'}
          onClick={setActiveTab}
        />
        <TabButton
          tabId="leaderboard"
          icon="🏆"
          label="Leaderboard"
          isActive={activeTab === 'leaderboard'}
          onClick={setActiveTab}
        />
      </nav>

      {/* Content Area */}
      <div className="social-content">
        {loading && (
          <div className="loading-section">
            <div className="loading-spinner"></div>
            <p>Loading social data...</p>
          </div>
        )}

        {activeTab === 'feed' && (
          <div className="feed-section">
            <div className="create-post">
              <h3>📝 Share Your Progress</h3>
              <textarea 
                placeholder="What did you accomplish today? Share your workout, achievement, or motivation!"
                rows={3}
              ></textarea>
              <div className="post-actions">
                <button className="attach-btn">📸 Add Photo</button>
                <button className="post-btn">🚀 Share</button>
              </div>
            </div>
            
            <div className="feed-list">
              {workoutFeed.map(post => (
                <WorkoutFeedItem key={post.id} post={post} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'challenges' && (
          <div className="challenges-section">
            <div className="section-header">
              <h2>🎯 Active Challenges</h2>
              <button className="create-challenge-btn">➕ Create Challenge</button>
            </div>
            
            <div className="challenges-grid">
              {challenges.map(challenge => (
                <ChallengeCard key={challenge.id} challenge={challenge} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'friends' && (
          <div className="friends-section">
            <div className="section-header">
              <h2>👫 Your Fitness Network</h2>
              <button className="add-friends-btn">➕ Add Friends</button>
            </div>
            
            <div className="friends-grid">
              {friends.map(friend => (
                <FriendCard key={friend.id} friend={friend} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'leaderboard' && (
          <div className="leaderboard-section">
            <div className="section-header">
              <h2>🏆 Monthly Leaderboard</h2>
              <select className="leaderboard-filter">
                <option>This Month</option>
                <option>This Week</option>
                <option>All Time</option>
              </select>
            </div>
            
            <div className="leaderboard-list">
              {leaderboard.map(entry => (
                <LeaderboardItem key={entry.rank} entry={entry} />
              ))}
            </div>
            
            <div className="leaderboard-info">
              <p>Points are earned through workouts, achievements, and social engagement!</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SocialFitness;