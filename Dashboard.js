// Khyrie Fitness Dashboard JavaScript

class FitnessDashboard {
    constructor() {
        this.currentUser = null;
        this.workoutData = [];
        this.familyData = [];
        this.progressChart = null;
        this.isOnline = navigator.onLine;
        this.syncQueue = [];
        
        this.init();
    }

    async init() {
        console.log('🏋️‍♂️ Initializing Khyrie Fitness Dashboard');
        
        // Check authentication
        await this.checkAuthentication();
        
        // Load user data
        await this.loadDashboardData();
        
        // Initialize components
        this.initializeChart();
        this.setupEventListeners();
        this.startPeriodicSync();
        
        // Register service worker
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js');
        }

        console.log('✅ Dashboard initialized successfully');
    }

    async checkAuthentication() {
        try {
            const response = await fetch('/api/auth/me');
            if (response.ok) {
                this.currentUser = await response.json();
                document.getElementById('user-greeting').textContent = 
                    `Welcome back, ${this.currentUser.name || 'Athlete'}!`;
            } else {
                // Redirect to login if not authenticated
                window.location.href = '/login';
            }
        } catch (error) {
            console.warn('Authentication check failed:', error);
            // Use offline mode with cached data
            this.currentUser = this.getOfflineUser();
        }
    }

    async loadDashboardData() {
        try {
            // Load data in parallel for better performance
            const [statsData, workoutData, familyData, progressData] = await Promise.all([
                this.fetchUserStats(),
                this.fetchTodaysWorkout(),
                this.fetchFamilyActivity(),
                this.fetchProgressData()
            ]);

            this.updateStatsDisplay(statsData);
            this.updateWorkoutDisplay(workoutData);
            this.updateFamilyFeed(familyData);
            this.updateProgressChart(progressData);

        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.loadOfflineData();
        }
    }

    async fetchUserStats() {
        try {
            const response = await fetch('/api/users/stats');
            return response.ok ? await response.json() : this.getDefaultStats();
        } catch (error) {
            return this.getDefaultStats();
        }
    }

    async fetchTodaysWorkout() {
        try {
            const response = await fetch('/api/workouts/today');
            return response.ok ? await response.json() : this.getDefaultWorkout();
        } catch (error) {
            return this.getDefaultWorkout();
        }
    }

    async fetchFamilyActivity() {
        try {
            const response = await fetch('/api/family/activity');
            return response.ok ? await response.json() : this.getDefaultFamilyActivity();
        } catch (error) {
            return this.getDefaultFamilyActivity();
        }
    }

    async fetchProgressData() {
        try {
            const response = await fetch('/api/analytics/progress');
            return response.ok ? await response.json() : this.getDefaultProgressData();
        } catch (error) {
            return this.getDefaultProgressData();
        }
    }

    updateStatsDisplay(stats) {
        const elements = {
            'workouts-week': stats.workoutsThisWeek || 0,
            'current-1rm': stats.currentOneRM || 0,
            'recovery-score': stats.recoveryScore || 0,
            'family-active': stats.familyActiveToday || 0
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                this.animateNumber(element, parseInt(value));
            }
        });
    }

    updateWorkoutDisplay(workout) {
        // Update workout card with AI-generated recommendations
        if (workout && workout.exercises) {
            const exerciseContainer = document.querySelector('.workout-exercises');
            exerciseContainer.innerHTML = workout.exercises.map(exercise => `
                <div class="exercise-item">
                    <span class="exercise-name">${exercise.name}</span>
                    <span class="exercise-sets">${exercise.sets} sets × ${exercise.reps} reps</span>
                </div>
            `).join('');
        }
    }

    updateFamilyFeed(activities) {
        const feed = document.getElementById('family-feed');
        if (activities && activities.length) {
            feed.innerHTML = activities.map(activity => `
                <div class="activity-item">
                    <div class="activity-avatar">${activity.avatar || '👤'}</div>
                    <div class="activity-content">
                        <strong>${activity.userName}</strong> ${activity.description}
                        <div class="activity-time">${this.formatTimeAgo(activity.timestamp)}</div>
                    </div>
                    <div class="activity-action">
                        <button class="btn btn-xs" onclick="dashboard.cheerActivity('${activity.id}')">
                            ${activity.reactions && activity.reactions.length ? '❤️' : '👏'} ${activity.reactions ? activity.reactions.length : 'Cheer'}
                        </button>
                    </div>
                </div>
            `).join('');
        }
    }

    initializeChart() {
        const canvas = document.getElementById('progressChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        
        // Simple chart implementation (you could replace with Chart.js)
        this.drawProgressChart(ctx, canvas.width, canvas.height);
    }

    drawProgressChart(ctx, width, height) {
        const padding = 40;
        const chartWidth = width - padding * 2;
        const chartHeight = height - padding * 2;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        // Draw axes
        ctx.strokeStyle = '#e2e8f0';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(padding, padding);
        ctx.lineTo(padding, height - padding);
        ctx.lineTo(width - padding, height - padding);
        ctx.stroke();

        // Sample data points
        const data = [65, 72, 78, 85, 92, 88, 95];
        const maxValue = Math.max(...data);
        
        // Draw line
        ctx.strokeStyle = '#00d4aa';
        ctx.lineWidth = 3;
        ctx.beginPath();
        
        data.forEach((value, index) => {
            const x = padding + (index / (data.length - 1)) * chartWidth;
            const y = height - padding - (value / maxValue) * chartHeight;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        ctx.stroke();

        // Draw points
        ctx.fillStyle = '#00d4aa';
        data.forEach((value, index) => {
            const x = padding + (index / (data.length - 1)) * chartWidth;
            const y = height - padding - (value / maxValue) * chartHeight;
            
            ctx.beginPath();
            ctx.arc(x, y, 6, 0, Math.PI * 2);
            ctx.fill();
        });

        // Add labels
        ctx.fillStyle = '#718096';
        ctx.font = '12px -apple-system, BlinkMacSystemFont, sans-serif';
        ctx.fillText('Strength Progress', padding, 20);
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                this.handleNavigation(e.target.closest('.nav-item'));
            });
        });

        // Progress metric selector
        const progressSelect = document.getElementById('progress-metric');
        if (progressSelect) {
            progressSelect.addEventListener('change', (e) => {
                this.updateProgressMetric(e.target.value);
            });
        }

        // Online/offline detection
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.syncOfflineData();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
        });

        // Pull to refresh for mobile
        let startY = 0;
        let pullDistance = 0;
        const refreshThreshold = 100;

        document.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                startY = e.touches[0].pageY;
            }
        });

        document.addEventListener('touchmove', (e) => {
            if (window.scrollY === 0 && startY) {
                pullDistance = e.touches[0].pageY - startY;
                if (pullDistance > 0 && pullDistance < refreshThreshold * 2) {
                    e.preventDefault();
                    this.showPullToRefreshIndicator(pullDistance / refreshThreshold);
                }
            }
        });

        document.addEventListener('touchend', () => {
            if (pullDistance > refreshThreshold) {
                this.refreshDashboard();
            }
            this.hidePullToRefreshIndicator();
            startY = 0;
            pullDistance = 0;
        });
    }

    handleNavigation(navItem) {
        // Remove active class from all nav items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });

        // Add active class to clicked item
        navItem.classList.add('active');

        // Handle navigation based on nav label
        const label = navItem.querySelector('.nav-label').textContent;
        switch (label) {
            case 'Dashboard':
                // Already on dashboard
                break;
            case 'Workouts':
                window.location.href = '/workouts';
                break;
            case 'Family':
                window.location.href = '/family';
                break;
            case 'Progress':
                window.location.href = '/progress';
                break;
            case 'Settings':
                window.location.href = '/settings';
                break;
        }
    }

    async cheerActivity(activityId) {
        try {
            const response = await fetch(`/api/family/activities/${activityId}/cheer`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                // Update UI optimistically
                const button = event.target;
                button.textContent = '❤️ +1';
                button.disabled = true;
                
                // Refresh family feed after short delay
                setTimeout(() => this.refreshFamilyFeed(), 500);
            }
        } catch (error) {
            console.error('Error cheering activity:', error);
            this.showToast('Unable to send cheer. Please try again.', 'error');
        }
    }

    async refreshDashboard() {
        this.showLoadingIndicator();
        try {
            await this.loadDashboardData();
            this.showToast('Dashboard refreshed!', 'success');
        } catch (error) {
            this.showToast('Unable to refresh. Using cached data.', 'warning');
        } finally {
            this.hideLoadingIndicator();
        }
    }

    async refreshFamilyFeed() {
        const familyData = await this.fetchFamilyActivity();
        this.updateFamilyFeed(familyData);
    }

    updateProgressMetric(metric) {
        // Update chart based on selected metric
        console.log('Updating progress metric:', metric);
        // This would fetch new data and redraw the chart
        this.initializeChart();
    }

    startPeriodicSync() {
        // Sync data every 5 minutes when online
        setInterval(() => {
            if (this.isOnline) {
                this.loadDashboardData();
            }
        }, 5 * 60 * 1000);
    }

    async syncOfflineData() {
        if (this.syncQueue.length > 0) {
            console.log('Syncing offline data...');
            
            for (const item of this.syncQueue) {
                try {
                    await fetch(item.url, item.options);
                } catch (error) {
                    console.error('Sync failed for:', item.url, error);
                }
            }
            
            this.syncQueue = [];
            this.showToast('Data synced successfully!', 'success');
        }
    }

    // Utility methods
    animateNumber(element, targetValue) {
        const startValue = parseInt(element.textContent) || 0;
        const duration = 1000; // 1 second
        const startTime = Date.now();

        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const currentValue = Math.round(startValue + (targetValue - startValue) * progress);
            
            element.textContent = currentValue;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        animate();
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

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#00d4aa' : type === 'error' ? '#ff6b6b' : '#4ecdc4'};
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
        }, 3000);
    }

    showLoadingIndicator() {
        document.body.style.cursor = 'wait';
        document.querySelector('#dashboard-container').classList.add('loading');
    }

    hideLoadingIndicator() {
        document.body.style.cursor = 'default';
        document.querySelector('#dashboard-container').classList.remove('loading');
    }

    showPullToRefreshIndicator(progress) {
        // Visual feedback for pull-to-refresh
        const indicator = document.querySelector('.refresh-indicator') || 
            this.createRefreshIndicator();
        indicator.style.opacity = Math.min(progress, 1);
        indicator.style.transform = `translateY(${progress * 50}px)`;
    }

    hidePullToRefreshIndicator() {
        const indicator = document.querySelector('.refresh-indicator');
        if (indicator) {
            indicator.style.opacity = '0';
            indicator.style.transform = 'translateY(-50px)';
        }
    }

    createRefreshIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'refresh-indicator';
        indicator.innerHTML = '↓ Pull to refresh';
        indicator.style.cssText = `
            position: fixed;
            top: -50px;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 8px 16px;
            border-radius: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            font-size: 14px;
            z-index: 1000;
            transition: all 0.2s ease;
        `;
        document.body.appendChild(indicator);
        return indicator;
    }

    // Default/fallback data methods
    getDefaultStats() {
        return {
            workoutsThisWeek: 4,
            currentOneRM: 225,
            recoveryScore: 87,
            familyActiveToday: 3
        };
    }

    getDefaultWorkout() {
        return {
            name: "Upper Body Strength Focus",
            duration: 45,
            intensity: "Moderate",
            targetMuscles: "Chest, Shoulders, Triceps",
            exercises: [
                { name: "Bench Press", sets: 4, reps: "6-8" },
                { name: "Overhead Press", sets: 3, reps: "8-10" },
                { name: "Push-ups", sets: 3, reps: "12-15" }
            ]
        };
    }

    getDefaultFamilyActivity() {
        return [
            {
                id: '1',
                userName: 'Sarah',
                description: 'completed a 5K run',
                timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
                avatar: '👩',
                reactions: []
            },
            {
                id: '2',
                userName: 'Mike',
                description: 'hit a new deadlift PR: 315 lbs!',
                timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
                avatar: '👨',
                reactions: ['❤️', '🔥']
            }
        ];
    }

    getDefaultProgressData() {
        return {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Strength Progress',
                data: [65, 72, 78, 85],
                borderColor: '#00d4aa',
                backgroundColor: 'rgba(0, 212, 170, 0.1)'
            }]
        };
    }

    getOfflineUser() {
        return JSON.parse(localStorage.getItem('user') || '{"name": "Athlete"}');
    }

    loadOfflineData() {
        console.log('Loading offline data...');
        const offlineData = {
            stats: this.getDefaultStats(),
            workout: this.getDefaultWorkout(),
            family: this.getDefaultFamilyActivity()
        };
        
        this.updateStatsDisplay(offlineData.stats);
        this.updateWorkoutDisplay(offlineData.workout);
        this.updateFamilyFeed(offlineData.family);
    }
}

// Global functions for HTML onclick handlers
window.dashboard = null;

function startWorkout() {
    dashboard.showToast('Starting workout...', 'success');
    // Navigate to workout page or show workout modal
    window.location.href = '/workout-session';
}

function customizeWorkout() {
    dashboard.showToast('Opening workout customization...', 'info');
    // Open workout customization modal or page
}

function openAICoach() {
    // Check if user has premium subscription
    dashboard.showToast('Opening AI Coach chat...', 'success');
    window.location.href = '/ai-coach';
}

function logWorkout() {
    dashboard.showToast('Opening workout log...', 'info');
    window.location.href = '/log-workout';
}

function trackWeight() {
    dashboard.showToast('Opening weight tracker...', 'info');
    window.location.href = '/weight-tracker';
}

function shareProgress() {
    if (navigator.share) {
        navigator.share({
            title: 'My Fitness Progress',
            text: 'Check out my fitness progress on Khyrie!',
            url: window.location.href
        });
    } else {
        dashboard.showToast('Progress copied to clipboard!', 'success');
    }
}

function viewAnalytics() {
    dashboard.showToast('Opening detailed analytics...', 'info');
    window.location.href = '/analytics';
}

function showDashboard() {
    // Already on dashboard
}

function showWorkouts() {
    window.location.href = '/workouts';
}

function showFamily() {
    window.location.href = '/family';
}

function showProgress() {
    window.location.href = '/progress';
}

function showProfile() {
    window.location.href = '/profile';
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new FitnessDashboard();
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