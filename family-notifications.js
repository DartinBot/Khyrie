/**
 * Family Accountability Push Notification System
 * Sends motivational push notifications to family members for workout accountability
 */

class FamilyNotificationManager {
    constructor() {
        this.isSupported = 'Notification' in window && 'serviceWorker' in navigator;
        this.permission = Notification.permission;
        this.registrationEndpoint = '/api/notifications/register';
        this.familyId = null;
        this.userId = null;
        
        this.init();
    }
    
    /**
     * Initialize push notification system
     */
    async init() {
        if (!this.isSupported) {
            console.warn('⚠️ Push notifications not supported in this browser');
            return;
        }
        
        try {
            // Get user and family info
            await this.loadUserInfo();
            
            // Request permission if not granted
            if (this.permission !== 'granted') {
                await this.requestPermission();
            }
            
            // Register for push notifications
            if (this.permission === 'granted') {
                await this.registerForPushNotifications();
            }
            
            // Setup notification triggers
            this.setupNotificationTriggers();
            
            console.log('📱 Family notification system initialized');
            
        } catch (error) {
            console.error('❌ Failed to initialize notifications:', error);
        }
    }
    
    /**
     * Request notification permission from user
     */
    async requestPermission() {
        try {
            const permission = await Notification.requestPermission();
            this.permission = permission;
            
            if (permission === 'granted') {
                console.log('✅ Notification permission granted');
                this.showWelcomeNotification();
            } else {
                console.log('❌ Notification permission denied');
            }
            
            return permission;
            
        } catch (error) {
            console.error('❌ Failed to request notification permission:', error);
            return 'denied';
        }
    }
    
    /**
     * Register for push notifications with server
     */
    async registerForPushNotifications() {
        try {
            const registration = await navigator.serviceWorker.ready;
            
            // Subscribe to push notifications
            const subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: this.urlBase64ToUint8Array(this.getVapidPublicKey())
            });
            
            // Send subscription to server
            await fetch(this.registrationEndpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    subscription: subscription,
                    userId: this.userId,
                    familyId: this.familyId,
                    preferences: this.getNotificationPreferences()
                })
            });
            
            console.log('📲 Registered for family push notifications');
            
        } catch (error) {
            console.error('❌ Failed to register for push notifications:', error);
        }
    }
    
    /**
     * Setup automatic notification triggers based on family activity
     */
    setupNotificationTriggers() {
        // Daily workout reminder
        this.scheduleDaily('08:00', 'workout-reminder', {
            title: '🏋️ Family Workout Time!',
            body: 'Your family is counting on you - start your workout now!',
            actions: [
                { action: 'start-workout', title: '💪 Start Workout' },
                { action: 'remind-later', title: '⏰ Remind Later' }
            ]
        });
        
        // Weekly progress check
        this.scheduleWeekly('sunday', '19:00', 'weekly-progress', {
            title: '📊 Weekly Family Fitness Report',
            body: 'See how your family performed this week!',
            actions: [
                { action: 'view-progress', title: '📈 View Progress' },
                { action: 'set-goals', title: '🎯 Set New Goals' }
            ]
        });
        
        // Family member workout completion notifications
        this.setupFamilyActivityNotifications();
        
        // Streak preservation notifications
        this.setupStreakNotifications();
        
        console.log('⏰ Notification triggers configured');
    }
    
    /**
     * Setup notifications for family member activity
     */
    setupFamilyActivityNotifications() {
        // Listen for family member workout completions
        setInterval(async () => {
            try {
                const recentActivity = await this.checkFamilyActivity();
                
                for (const activity of recentActivity) {
                    if (activity.shouldNotify && !activity.notified) {
                        await this.sendFamilyActivityNotification(activity);
                    }
                }
                
            } catch (error) {
                console.error('❌ Error checking family activity:', error);
            }
        }, 5 * 60 * 1000); // Check every 5 minutes
    }
    
    /**
     * Setup streak preservation notifications
     */
    setupStreakNotifications() {
        // Check for streak risks daily
        this.scheduleDaily('20:00', 'streak-check', async () => {
            try {
                const streakInfo = await this.checkStreakStatus();
                
                if (streakInfo.atRisk) {
                    await this.sendStreakRiskNotification(streakInfo);
                }
                
                if (streakInfo.milestone) {
                    await this.sendStreakMilestoneNotification(streakInfo);
                }
                
            } catch (error) {
                console.error('❌ Error checking streak status:', error);
            }
        });
    }
    
    /**
     * Send immediate notification to family members
     */
    async sendFamilyNotification(type, data) {
        try {
            const response = await fetch('/api/notifications/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    type: type,
                    familyId: this.familyId,
                    senderId: this.userId,
                    data: data
                })
            });
            
            if (response.ok) {
                console.log('📤 Family notification sent:', type);
            }
            
        } catch (error) {
            console.error('❌ Failed to send family notification:', error);
        }
    }
    
    /**
     * Send workout completion celebration
     */
    async celebrateWorkoutCompletion(workoutData) {
        await this.sendFamilyNotification('workout-celebration', {
            title: `🎉 ${workoutData.userName} completed a workout!`,
            body: `${workoutData.workoutName} - ${workoutData.duration} minutes`,
            icon: '🏋️',
            actions: [
                { action: 'cheer', title: '👏 Send Cheer' },
                { action: 'join-workout', title: '🏃 Join Workout' }
            ],
            workout: workoutData
        });
    }
    
    /**
     * Send motivational reminder to inactive family members
     */
    async sendMotivationalReminder(inactiveMember) {
        const messages = [
            `${inactiveMember.name}, your family is rooting for you! 💪`,
            `Don't break your streak, ${inactiveMember.name}! 🔥`,
            `${inactiveMember.name}, let's get moving together! 🏃‍♀️`,
            `Your family misses working out with you, ${inactiveMember.name}! ❤️`
        ];
        
        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        
        await this.sendFamilyNotification('motivational-reminder', {
            title: '💪 Family Fitness Motivation',
            body: randomMessage,
            targetUserId: inactiveMember.id,
            actions: [
                { action: 'start-workout', title: '🏋️ Start Workout' },
                { action: 'view-family', title: '👨‍👩‍👧‍👦 View Family' }
            ]
        });
    }
    
    /**
     * Send challenge invitation
     */
    async sendChallengeInvitation(challenge) {
        await this.sendFamilyNotification('challenge-invitation', {
            title: `🏆 New Family Challenge: ${challenge.name}`,
            body: `${challenge.description} - Join now!`,
            actions: [
                { action: 'join-challenge', title: '🎯 Join Challenge' },
                { action: 'view-details', title: '📋 View Details' }
            ],
            challenge: challenge
        });
    }
    
    /**
     * Send goal achievement celebration
     */
    async celebrateGoalAchievement(achievement) {
        await this.sendFamilyNotification('goal-achievement', {
            title: `🏆 Goal Achieved!`,
            body: `${achievement.userName} reached their ${achievement.goalType} goal!`,
            icon: '🎉',
            actions: [
                { action: 'celebrate', title: '🎊 Celebrate' },
                { action: 'set-new-goal', title: '🎯 Set New Goal' }
            ],
            achievement: achievement
        });
    }
    
    /**
     * Get family activity for notifications
     */
    async checkFamilyActivity() {
        try {
            const response = await fetch(`/api/family/activity/${this.familyId}/recent`);
            return await response.json();
        } catch (error) {
            console.error('❌ Failed to check family activity:', error);
            return [];
        }
    }
    
    /**
     * Check streak status for family members
     */
    async checkStreakStatus() {
        try {
            const response = await fetch(`/api/family/streaks/${this.familyId}`);
            return await response.json();
        } catch (error) {
            console.error('❌ Failed to check streak status:', error);
            return { atRisk: false, milestone: false };
        }
    }
    
    /**
     * Send family activity notification
     */
    async sendFamilyActivityNotification(activity) {
        const notifications = {
            'workout-completed': {
                title: `🎉 ${activity.userName} finished a workout!`,
                body: `${activity.workoutName} completed in ${activity.duration} minutes`,
                actions: [
                    { action: 'cheer', title: '👏 Send Cheer' },
                    { action: 'start-workout', title: '🏋️ Me Too!' }
                ]
            },
            'streak-started': {
                title: `🔥 ${activity.userName} started a new streak!`,
                body: `Day 1 of their fitness journey - show support!`,
                actions: [
                    { action: 'encourage', title: '💪 Encourage' },
                    { action: 'join-streak', title: '🏃 Join Streak' }
                ]
            },
            'goal-progress': {
                title: `📈 ${activity.userName} is making progress!`,
                body: `${activity.progress}% towards their ${activity.goalType} goal`,
                actions: [
                    { action: 'cheer', title: '👏 Cheer On' },
                    { action: 'view-progress', title: '📊 View Progress' }
                ]
            }
        };
        
        const notification = notifications[activity.type];
        if (notification) {
            await this.sendFamilyNotification(activity.type, notification);
        }
    }
    
    /**
     * Send streak risk notification
     */
    async sendStreakRiskNotification(streakInfo) {
        await this.sendFamilyNotification('streak-risk', {
            title: `⚠️ Streak Alert!`,
            body: `Your ${streakInfo.days}-day streak is at risk! Don't break it now!`,
            actions: [
                { action: 'quick-workout', title: '⚡ Quick Workout' },
                { action: 'family-support', title: '👨‍👩‍👧‍👦 Family Support' }
            ]
        });
    }
    
    /**
     * Send streak milestone notification
     */
    async sendStreakMilestoneNotification(streakInfo) {
        await this.sendFamilyNotification('streak-milestone', {
            title: `🔥 ${streakInfo.days}-Day Streak Achieved!`,
            body: `Amazing! You've maintained your fitness streak for ${streakInfo.days} days!`,
            actions: [
                { action: 'celebrate', title: '🎊 Celebrate' },
                { action: 'share-achievement', title: '📤 Share Achievement' }
            ]
        });
    }
    
    /**
     * Schedule daily notification
     */
    scheduleDaily(time, id, notification) {
        const [hours, minutes] = time.split(':').map(Number);
        
        setInterval(() => {
            const now = new Date();
            if (now.getHours() === hours && now.getMinutes() === minutes) {
                if (typeof notification === 'function') {
                    notification();
                } else {
                    this.sendLocalNotification(notification);
                }
            }
        }, 60000); // Check every minute
    }
    
    /**
     * Schedule weekly notification
     */
    scheduleWeekly(day, time, id, notification) {
        const dayMap = {
            'sunday': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3,
            'thursday': 4, 'friday': 5, 'saturday': 6
        };
        
        const [hours, minutes] = time.split(':').map(Number);
        const targetDay = dayMap[day.toLowerCase()];
        
        setInterval(() => {
            const now = new Date();
            if (now.getDay() === targetDay && 
                now.getHours() === hours && 
                now.getMinutes() === minutes) {
                if (typeof notification === 'function') {
                    notification();
                } else {
                    this.sendLocalNotification(notification);
                }
            }
        }, 60000); // Check every minute
    }
    
    /**
     * Send local notification
     */
    sendLocalNotification(notification) {
        if (this.permission === 'granted') {
            new Notification(notification.title, {
                body: notification.body,
                icon: '/icons/icon-192x192.png',
                badge: '/icons/badge-72x72.png',
                vibrate: [100, 50, 100],
                actions: notification.actions || []
            });
        }
    }
    
    /**
     * Show welcome notification
     */
    showWelcomeNotification() {
        this.sendLocalNotification({
            title: '🎉 Welcome to Khyrie Family Fitness!',
            body: 'You\'ll receive motivational notifications to keep your family active!'
        });
    }
    
    /**
     * Load user information
     */
    async loadUserInfo() {
        try {
            const response = await fetch('/api/user/profile');
            const userInfo = await response.json();
            
            this.userId = userInfo.id;
            this.familyId = userInfo.familyId;
            
        } catch (error) {
            console.error('❌ Failed to load user info:', error);
        }
    }
    
    /**
     * Get notification preferences
     */
    getNotificationPreferences() {
        return {
            workoutReminders: true,
            familyActivity: true,
            streakAlerts: true,
            goalProgress: true,
            challenges: true,
            quietHours: { start: '22:00', end: '07:00' }
        };
    }
    
    /**
     * Get VAPID public key for push notifications
     */
    getVapidPublicKey() {
        // This would be your actual VAPID public key from the server
        return 'BMxKgJgkFaVQqskhvr_EfRNk0j4X8X8YD8XK3K3kj8Y...';
    }
    
    /**
     * Convert VAPID key format
     */
    urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/-/g, '+')
            .replace(/_/g, '/');
        
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        
        return outputArray;
    }
}

/**
 * Notification Manager API for other components
 */
window.FamilyNotifications = {
    // Public methods for sending notifications
    celebrateWorkout: async (workoutData) => {
        if (window.familyNotificationManager) {
            await window.familyNotificationManager.celebrateWorkoutCompletion(workoutData);
        }
    },
    
    sendMotivation: async (memberId) => {
        if (window.familyNotificationManager) {
            const member = await fetch(`/api/family/member/${memberId}`).then(r => r.json());
            await window.familyNotificationManager.sendMotivationalReminder(member);
        }
    },
    
    inviteToChallenge: async (challenge) => {
        if (window.familyNotificationManager) {
            await window.familyNotificationManager.sendChallengeInvitation(challenge);
        }
    },
    
    celebrateGoal: async (achievement) => {
        if (window.familyNotificationManager) {
            await window.familyNotificationManager.celebrateGoalAchievement(achievement);
        }
    }
};

// Initialize notification manager
document.addEventListener('DOMContentLoaded', () => {
    window.familyNotificationManager = new FamilyNotificationManager();
});

console.log('📱 Family Notification Manager loaded!');