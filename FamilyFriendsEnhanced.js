// Khyrie Family & Friends Social Network - Enhanced Vanilla JavaScript

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
        this.realTimeConnection = null;
        
        this.init();
    }

    async init() {
        console.log('🏋️‍♂️ Initializing Family & Friends Social Network');
        
        await this.loadDashboardData();
        this.setupEventListeners();
        this.initializeRealTimeUpdates();
        this.startNotificationSystem();
        
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

    async fetchDashboardData() {
        try {
            const response = await fetch(`/api/dashboard/family-friends/${this.userId}`);
            return response.ok ? (await response.json()).dashboard_data : this.getDefaultDashboardData();
        } catch (error) {
            return this.getDefaultDashboardData();
        }
    }

    async fetchUserGroups() {
        try {
            const response = await fetch(`/api/groups/user/${this.userId}`);
            return response.ok ? (await response.json()).user_groups || [] : this.getDefaultGroups();
        } catch (error) {
            return this.getDefaultGroups();
        }
    }

    async fetchActiveChallenges() {
        try {
            const response = await fetch(`/api/challenges/active/${this.userId}`);
            return response.ok ? await response.json() : this.getDefaultChallenges();
        } catch (error) {
            return this.getDefaultChallenges();
        }
    }

    async fetchLiveWorkouts() {
        try {
            const response = await fetch(`/api/live-workouts/${this.userId}`);
            return response.ok ? await response.json() : this.getDefaultLiveWorkouts();
        } catch (error) {
            return this.getDefaultLiveWorkouts();
        }
    }

    setupEventListeners() {
        // Tab switching
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-tab]')) {
                this.switchTab(e.target.dataset.tab);
            }
        });

        // Real-time updates
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.refreshData();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case '1': e.preventDefault(); this.switchTab('dashboard'); break;
                    case '2': e.preventDefault(); this.switchTab('groups'); break;
                    case '3': e.preventDefault(); this.switchTab('challenges'); break;
                    case '4': e.preventDefault(); this.switchTab('live'); break;
                }
            }
        });
    }

    switchTab(tabName) {
        this.activeTab = tabName;
        
        // Update tab UI
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        const activeTab = document.querySelector(`[data-tab="${tabName}"]`);
        if (activeTab) {
            activeTab.classList.add('active');
        }
        
        // Render new tab content
        this.renderCurrentTab();
        
        // Track analytics
        this.trackTabSwitch(tabName);
    }

    renderCurrentTab() {
        const container = document.getElementById('tab-content');
        if (!container) return;

        switch (this.activeTab) {
            case 'dashboard':
                container.innerHTML = this.renderDashboard();
                break;
            case 'groups':
                container.innerHTML = this.renderGroups();
                this.setupGroupsEventListeners();
                break;
            case 'challenges':
                container.innerHTML = this.renderChallenges();
                this.setupChallengesEventListeners();
                break;
            case 'live':
                container.innerHTML = this.renderLiveWorkouts();
                this.setupLiveWorkoutsEventListeners();
                break;
            case 'create-group':
                container.innerHTML = this.renderCreateGroup();
                this.setupCreateGroupEventListeners();
                break;
            default:
                container.innerHTML = this.renderDashboard();
        }
    }

    renderDashboard() {
        if (this.loading) {
            return `<div class="loading">Loading family & friends data...</div>`;
        }

        if (!this.dashboardData) {
            return `<div class="no-data">No dashboard data available</div>`;
        }

        const stats = this.dashboardData.weekly_stats || {};
        const activities = this.dashboardData.recent_group_activities || [];

        return `
            <div class="dashboard-content">
                <!-- Weekly Stats -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">${stats.group_workouts_completed || 0}</div>
                        <div class="stat-label">Group Workouts</div>
                        <div class="stat-icon">🏋️‍♂️</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.encouragements_sent || 0}</div>
                        <div class="stat-label">Encouragements Sent</div>
                        <div class="stat-icon">💪</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.challenges_participated || 0}</div>
                        <div class="stat-label">Active Challenges</div>
                        <div class="stat-icon">🏆</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.family_fitness_streak || 0}</div>
                        <div class="stat-label">Day Streak</div>
                        <div class="stat-icon">🔥</div>
                    </div>
                </div>

                <!-- Social Notifications -->
                <div class="notifications-section">
                    <h3>Recent Activity</h3>
                    <div class="notifications-list">
                        ${activities.slice(0, 5).map(activity => `
                            <div class="notification-item">
                                <div class="notification-avatar">${this.getActivityAvatar(activity.user_id)}</div>
                                <div class="notification-content">
                                    <div class="notification-text">
                                        <strong>${activity.user_name || activity.user_id}</strong> ${activity.action || 'completed a workout'}
                                    </div>
                                    <div class="notification-time">${this.formatTimeAgo(activity.timestamp || activity.completion_time)}</div>
                                </div>
                                <div class="notification-reactions">
                                    <button class="reaction-btn" onclick="familyApp.reactToActivity('${activity.id}', 'heart')">
                                        ❤️ <span class="reaction-count">${activity.reactions_count || 0}</span>
                                    </button>
                                    <button class="reaction-btn" onclick="familyApp.reactToActivity('${activity.id}', 'fire')">🔥</button>
                                    <button class="reaction-btn" onclick="familyApp.reactToActivity('${activity.id}', 'muscle')">💪</button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <!-- Quick Actions -->
                <div class="quick-actions">
                    <h3>Quick Actions</h3>
                    <div class="action-buttons">
                        <button class="action-btn primary" onclick="familyApp.switchTab('create-group')">
                            👥 Create New Group
                        </button>
                        <button class="action-btn" onclick="familyApp.switchTab('challenges')">
                            🏆 Start Challenge
                        </button>
                        <button class="action-btn" onclick="familyApp.shareWorkout()">
                            💪 Share Workout
                        </button>
                        <button class="action-btn" onclick="familyApp.joinLiveSession()">
                            📱 Join Live Session
                        </button>
                    </div>
                </div>

                <!-- Leaderboard Preview -->
                <div class="leaderboard-preview">
                    <h3>🏆 This Week's Leaders</h3>
                    <div class="leaderboard-list">
                        ${this.generateWeeklyLeaderboard().map((entry, index) => `
                            <div class="leaderboard-item ${index === 0 ? 'winner' : ''} ${entry.isCurrentUser ? 'current-user' : ''}">
                                <div class="rank">${index + 1}</div>
                                <div class="member-info">
                                    <div class="member-avatar">${entry.avatar}</div>
                                    <div class="member-name">${entry.name}</div>
                                </div>
                                <div class="member-score">
                                    <div class="score-value">${entry.score}</div>
                                    <div class="score-label">${entry.metric}</div>
                                </div>
                                ${index === 0 ? '<div class="winner-badge">👑</div>' : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    renderGroups() {
        return `
            <div class="groups-content">
                <div class="section-header">
                    <h2>My Fitness Groups</h2>
                    <button class="btn-primary" onclick="familyApp.switchTab('create-group')">
                        Create New Group
                    </button>
                </div>

                <div class="groups-grid">
                    ${this.userGroups.length > 0 ? this.userGroups.map(group => `
                        <div class="group-card" data-group-id="${group.group_id}">
                            <div class="group-header">
                                <div class="group-icon">
                                    ${group.type === 'family' ? '👨‍👩‍👧‍👦' : group.type === 'friends' ? '👥' : '🏋️‍♂️'}
                                </div>
                                <div class="group-info">
                                    <h3>${group.name}</h3>
                                    <p>${group.member_count || 1} members • ${group.type}</p>
                                </div>
                                <div class="group-role">
                                    <span class="role-badge ${group.role}">${group.role || 'member'}</span>
                                </div>
                            </div>
                            
                            <div class="group-stats">
                                <div class="stat">
                                    <span class="stat-value">${group.total_workouts || 15}</span>
                                    <span class="stat-label">Workouts</span>
                                </div>
                                <div class="stat">
                                    <span class="stat-value">${group.active_challenges || 3}</span>
                                    <span class="stat-label">Challenges</span>
                                </div>
                                <div class="stat">
                                    <span class="stat-value">${group.activity_rate || 85}%</span>
                                    <span class="stat-label">Active</span>
                                </div>
                            </div>
                            
                            <div class="group-activity-preview">
                                <div class="recent-activity">
                                    <strong>Recent:</strong> ${group.last_activity || 'Sarah completed Upper Body workout 2h ago'}
                                </div>
                            </div>
                            
                            <div class="group-actions">
                                <button class="btn-secondary" onclick="familyApp.viewGroupDetails('${group.group_id}')">
                                    View Details
                                </button>
                                <button class="btn-primary" onclick="familyApp.startGroupWorkout('${group.group_id}')">
                                    Start Workout
                                </button>
                            </div>
                        </div>
                    `).join('') : `
                        <div class="no-groups">
                            <div class="no-groups-icon">👥</div>
                            <h3>No Groups Yet</h3>
                            <p>Create your first fitness group to start tracking with family and friends!</p>
                            <button class="btn-primary" onclick="familyApp.switchTab('create-group')">
                                Create Your First Group
                            </button>
                        </div>
                    `}
                </div>
            </div>
        `;
    }

    renderChallenges() {
        return `
            <div class="challenges-content">
                <div class="section-header">
                    <h2>Family & Friends Challenges</h2>
                    <button class="btn-primary" onclick="familyApp.showCreateChallenge()">Create New Challenge</button>
                </div>

                <div class="challenges-grid">
                    ${this.activeChallenges.map(challenge => `
                        <div class="challenge-card ${challenge.status}" data-challenge-id="${challenge.id}">
                            <div class="challenge-header">
                                <div class="challenge-icon">${challenge.icon || '🏃‍♂️'}</div>
                                <div class="challenge-info">
                                    <h3>${challenge.name}</h3>
                                    <p>${challenge.description}</p>
                                </div>
                                <div class="challenge-status">
                                    <span class="status-badge ${challenge.status}">${challenge.status}</span>
                                </div>
                            </div>
                            
                            <div class="challenge-progress">
                                ${challenge.type === 'leaderboard' ? `
                                    <div class="leaderboard-preview">
                                        ${challenge.leaderboard.slice(0, 3).map((entry, index) => `
                                            <div class="position ${entry.isCurrentUser ? 'current-user' : ''}">
                                                <span class="rank">${this.getOrdinal(index + 1)}</span>
                                                <span class="name">${entry.name}</span>
                                                <span class="score">${entry.score} ${challenge.unit}</span>
                                            </div>
                                        `).join('')}
                                    </div>
                                ` : `
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: ${challenge.progress}%"></div>
                                    </div>
                                    <div class="progress-text">${challenge.current}/${challenge.target} ${challenge.unit} (${challenge.progress}%)</div>
                                `}
                            </div>
                            
                            <div class="challenge-footer">
                                <div class="time-remaining">${challenge.timeRemaining}</div>
                                <div class="challenge-actions">
                                    ${challenge.isParticipating ? `
                                        <button class="btn-primary" onclick="familyApp.viewFullLeaderboard('${challenge.id}')">
                                            View Full Leaderboard
                                        </button>
                                    ` : `
                                        <button class="btn-secondary" onclick="familyApp.joinChallenge('${challenge.id}')">
                                            Join Challenge
                                        </button>
                                    `}
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    renderLiveWorkouts() {
        return `
            <div class="live-workouts-content">
                <div class="section-header">
                    <h2>Live Group Workouts</h2>
                    <button class="btn-primary" onclick="familyApp.startLiveWorkout()">Start Live Session</button>
                </div>
                
                <div class="live-sessions">
                    ${this.liveWorkouts.map(session => `
                        <div class="session-card ${session.status}" data-session-id="${session.id}">
                            <div class="session-header">
                                <div class="user-avatar">${session.hostAvatar || '👤'}</div>
                                <div class="session-info">
                                    <h3>${session.hostName}'s ${session.workoutType}</h3>
                                    <p>${session.status === 'live' ? `Started ${session.duration} ago` : `Scheduled for ${session.scheduledTime}`} • ${session.description}</p>
                                </div>
                                <div class="session-status">
                                    <span class="status-dot ${session.status}"></span>
                                    <span>${session.status === 'live' ? 'Live' : 'Scheduled'}</span>
                                </div>
                            </div>
                            
                            ${session.status === 'live' ? `
                                <div class="session-progress">
                                    <div class="exercise-current">
                                        Currently: ${session.currentExercise} (Set ${session.currentSet}/${session.totalSets})
                                    </div>
                                    <div class="session-stats">
                                        <span>⏱️ ${session.duration}</span>
                                        <span>💪 ${session.completedExercises}/${session.totalExercises} exercises</span>
                                        <span>🔥 Est. ${session.estimatedCalories} cal</span>
                                    </div>
                                    <div class="live-participants">
                                        <span>👥 ${session.participants.length} participants</span>
                                        <div class="participant-avatars">
                                            ${session.participants.slice(0, 4).map(p => `<span class="participant-avatar">${p.avatar}</span>`).join('')}
                                            ${session.participants.length > 4 ? `<span class="more-participants">+${session.participants.length - 4}</span>` : ''}
                                        </div>
                                    </div>
                                </div>
                            ` : ''}
                            
                            <div class="session-actions">
                                <button class="btn-secondary" onclick="familyApp.sendEncouragement('${session.id}', '${session.hostId}')">
                                    💬 Send Encouragement
                                </button>
                                ${session.status === 'live' ? `
                                    <button class="btn-primary" onclick="familyApp.joinLiveWorkout('${session.id}')">
                                        🏋️‍♂️ Join Workout
                                    </button>
                                ` : `
                                    <button class="btn-primary" onclick="familyApp.joinScheduledWorkout('${session.id}')">📝 Join Session</button>
                                `}
                            </div>
                        </div>
                    `).join('')}
                </div>

                <!-- Quick Encouragement Section -->
                <div class="encouragement-section">
                    <h3>Send Quick Encouragement</h3>
                    <div class="encouragement-buttons">
                        <button class="encouragement-btn" onclick="familyApp.sendQuickEncouragement('keep-going')">💪 Keep going!</button>
                        <button class="encouragement-btn" onclick="familyApp.sendQuickEncouragement('you-got-this')">🔥 You've got this!</button>
                        <button class="encouragement-btn" onclick="familyApp.sendQuickEncouragement('beast-mode')">⚡ Beast mode!</button>
                        <button class="encouragement-btn" onclick="familyApp.sendQuickEncouragement('crushing-it')">🏆 Crushing it!</button>
                    </div>
                </div>
            </div>
        `;
    }

    renderCreateGroup() {
        return `
            <div class="create-group-content">
                <h2>Create Fitness Group</h2>
                <form id="create-group-form" class="create-group-form">
                    <div class="form-group">
                        <label>Group Name</label>
                        <input type="text" id="group-name" placeholder="e.g., Smith Family Fitness, Workout Buddies" required>
                    </div>

                    <div class="form-group">
                        <label>Group Type</label>
                        <select id="group-type">
                            <option value="family">Family</option>
                            <option value="friends">Friends</option>
                            <option value="workout_buddies">Workout Buddies</option>
                            <option value="challenge_group">Challenge Group</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Description</label>
                        <textarea id="group-description" placeholder="What's your group about? Goals, schedule, etc." rows="3"></textarea>
                    </div>

                    <div class="form-group">
                        <label>Privacy Level</label>
                        <select id="privacy-level">
                            <option value="family">Family Only</option>
                            <option value="friends">Friends</option>
                            <option value="private">Private (Invite Only)</option>
                        </select>
                    </div>

                    <div class="form-actions">
                        <button type="button" class="btn-secondary" onclick="familyApp.switchTab('groups')">
                            Cancel
                        </button>
                        <button type="submit" class="btn-primary">
                            Create Group
                        </button>
                    </div>
                </form>
            </div>
        `;
    }

    setupGroupsEventListeners() {
        // Group interaction handlers are set up via onclick attributes in the HTML
    }

    setupChallengesEventListeners() {
        // Challenge interaction handlers are set up via onclick attributes in the HTML
    }

    setupLiveWorkoutsEventListeners() {
        // Live workout handlers are set up via onclick attributes in the HTML
    }

    setupCreateGroupEventListeners() {
        const form = document.getElementById('create-group-form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.createGroup();
            });
        }
    }

    // Action Methods
    async createGroup() {
        const formData = {
            group_name: document.getElementById('group-name').value,
            group_type: document.getElementById('group-type').value,
            creator_id: this.userId,
            description: document.getElementById('group-description').value,
            privacy_level: document.getElementById('privacy-level').value,
            initial_members: []
        };

        try {
            const response = await fetch('/api/groups/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const result = await response.json();
            
            if (result.group_created) {
                this.showSuccessMessage(`Group created successfully! Invite code: ${result.invite_code}`);
                await this.loadDashboardData();
                this.switchTab('groups');
            } else {
                throw new Error('Failed to create group');
            }
        } catch (error) {
            console.error('Error creating group:', error);
            this.showErrorMessage('Failed to create group. Please try again.');
        }
    }

    async reactToActivity(activityId, reactionType) {
        try {
            const response = await fetch('/api/activities/react', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    activity_id: activityId,
                    user_id: this.userId,
                    reaction_type: reactionType
                })
            });

            if (response.ok) {
                this.showToast('Reaction sent! 💪', 'success');
                
                // Add haptic feedback
                if ('vibrate' in navigator) {
                    navigator.vibrate(25);
                }
            }
        } catch (error) {
            console.error('Error reacting to activity:', error);
            this.showToast('Failed to send reaction', 'error');
        }
    }

    async sendEncouragement(sessionId, targetUserId) {
        const encouragements = [
            "You're doing amazing! Keep it up! 💪",
            "Beast mode activated! 🔥",
            "Crushing it! Don't stop now! 💯",
            "You've got this! Push through! ⚡",
            "Incredible form! Keep going! 🏆"
        ];
        
        const message = encouragements[Math.floor(Math.random() * encouragements.length)];
        
        try {
            const response = await fetch('/api/encouragement/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: sessionId,
                    from_user_id: this.userId,
                    to_user_id: targetUserId,
                    message: message
                })
            });

            if (response.ok) {
                this.showToast('Encouragement sent! 🎉', 'success');
            }
        } catch (error) {
            console.error('Error sending encouragement:', error);
            this.showToast('Failed to send encouragement', 'error');
        }
    }

    shareWorkout() {
        const shareText = "Just completed an amazing workout! 💪 Join me on Khyrie Fitness! #KhyrieFitness";
        
        if (navigator.share) {
            navigator.share({
                title: 'Workout Complete',
                text: shareText,
                url: window.location.href
            });
        } else {
            navigator.clipboard.writeText(shareText);
            this.showToast('Workout details copied to clipboard!', 'success');
        }
    }

    joinLiveSession() {
        if (this.liveWorkouts.length > 0) {
            this.switchTab('live');
        } else {
            this.showToast('No live sessions available right now', 'info');
        }
    }

    // Utility Methods
    getActivityAvatar(userId) {
        const avatars = { 'mom': '👩', 'dad': '👨', 'sarah': '👧', 'mike': '👦' };
        return avatars[userId.toLowerCase()] || '👤';
    }

    formatTimeAgo(timestamp) {
        const now = new Date();
        const time = new Date(timestamp);
        const diffInSeconds = Math.floor((now - time) / 1000);

        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} min ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
        return `${Math.floor(diffInSeconds / 86400)} days ago`;
    }

    generateWeeklyLeaderboard() {
        return [
            { name: 'Sarah', score: 12, metric: 'workouts', avatar: '👧', isCurrentUser: false },
            { name: 'You', score: 11, metric: 'workouts', avatar: '😊', isCurrentUser: true },
            { name: 'Dad', score: 9, metric: 'workouts', avatar: '👨', isCurrentUser: false },
            { name: 'Mom', score: 8, metric: 'workouts', avatar: '👩', isCurrentUser: false }
        ];
    }

    getOrdinal(num) {
        const suffix = ['th', 'st', 'nd', 'rd'];
        const v = num % 100;
        return num + (suffix[(v - 20) % 10] || suffix[v] || suffix[0]);
    }

    // Default/Mock Data Methods
    getDefaultDashboardData() {
        return {
            weekly_stats: {
                group_workouts_completed: 4,
                encouragements_sent: 12,
                challenges_participated: 2,
                family_fitness_streak: 7
            },
            recent_group_activities: [
                {
                    id: '1',
                    user_id: 'sarah',
                    user_name: 'Sarah',
                    action: 'completed a 5K run',
                    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
                    reactions_count: 5
                },
                {
                    id: '2',
                    user_id: 'dad',
                    user_name: 'Dad',
                    action: 'hit a new deadlift PR: 315 lbs!',
                    timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
                    reactions_count: 8
                }
            ]
        };
    }

    getDefaultGroups() {
        return [
            {
                group_id: 'smith-family',
                name: 'Smith Family Fitness',
                type: 'family',
                member_count: 4,
                role: 'member',
                total_workouts: 45,
                active_challenges: 2,
                activity_rate: 92,
                last_activity: 'Sarah completed Upper Body workout 2h ago'
            }
        ];
    }

    getDefaultChallenges() {
        return [
            {
                id: 'family-steps',
                name: 'Family Step Challenge',
                description: 'Most steps in 30 days wins!',
                icon: '🏃‍♂️',
                status: 'active',
                type: 'leaderboard',
                timeRemaining: '3 days left',
                isParticipating: true,
                leaderboard: [
                    { name: 'Mom', score: 85420, isCurrentUser: false },
                    { name: 'You', score: 82150, isCurrentUser: true },
                    { name: 'Dad', score: 78900, isCurrentUser: false }
                ],
                unit: 'steps'
            },
            {
                id: 'workout-frequency',
                name: 'Workout Frequency Challenge',
                description: 'Most workouts completed this month',
                icon: '💪',
                status: 'active',
                type: 'progress',
                timeRemaining: '12 days left',
                isParticipating: false,
                current: 17,
                target: 25,
                progress: 68,
                unit: 'workouts'
            }
        ];
    }

    getDefaultLiveWorkouts() {
        return [
            {
                id: 'dads-workout',
                hostId: 'dad',
                hostName: 'Dad',
                hostAvatar: '👨',
                workoutType: 'Morning Strength Training',
                description: 'Upper body focus',
                status: 'live',
                duration: '25 min',
                currentExercise: 'Bench Press',
                currentSet: 3,
                totalSets: 4,
                completedExercises: 8,
                totalExercises: 12,
                estimatedCalories: 340,
                participants: [
                    { id: 'mom', name: 'Mom', avatar: '👩' },
                    { id: 'sarah', name: 'Sarah', avatar: '👧' }
                ]
            }
        ];
    }

    // Real-time and notification methods
    initializeRealTimeUpdates() {
        // Set up polling for real-time updates
        setInterval(() => {
            if (!document.hidden) {
                this.refreshData();
            }
        }, 30000); // Refresh every 30 seconds
    }

    startNotificationSystem() {
        // Request notification permission
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }

    async refreshData() {
        try {
            await this.loadDashboardData();
            if (this.activeTab === 'dashboard') {
                this.renderCurrentTab();
            }
        } catch (error) {
            console.error('Error refreshing data:', error);
        }
    }

    // UI helper methods
    showLoadingState() {
        const container = document.getElementById('tab-content');
        if (container) {
            container.innerHTML = '<div class="loading">Loading...</div>';
        }
    }

    hideLoadingState() {
        // Loading state will be replaced by actual content
    }

    loadOfflineData() {
        this.dashboardData = this.getDefaultDashboardData();
        this.userGroups = this.getDefaultGroups();
        this.activeChallenges = this.getDefaultChallenges();
        this.liveWorkouts = this.getDefaultLiveWorkouts();
        this.renderCurrentTab();
        this.showToast('Using offline data', 'warning');
    }

    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#48bb78' : type === 'error' ? '#f56565' : type === 'warning' ? '#ed8936' : '#4299e1'};
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    showSuccessMessage(message) {
        this.showToast(message, 'success', 5000);
    }

    showErrorMessage(message) {
        this.showToast(message, 'error', 5000);
    }

    trackTabSwitch(tabName) {
        // Analytics tracking
        console.log(`Tab switched to: ${tabName}`);
    }
}

// Global family app instance
let familyApp = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    familyApp = new FamilyFriendsApp();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);