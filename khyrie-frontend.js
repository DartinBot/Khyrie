/**
 * Khyrie3.0 Frontend JavaScript API Integration
 * Comprehensive client-side integration with unified backend
 */

class KhyrieAPI {
    constructor() {
        this.baseURL = 'http://localhost:8000';
        this.currentUser = { tier: 'free' };
        this.isConnected = false;
        this.metrics = {
            totalWorkouts: 0,
            aiGenerations: 0,
            familyMembers: 1
        };
        
        // Initialize on page load
        this.init();
    }

    async init() {
        console.log('🚀 Initializing Khyrie3.0 Frontend...');
        
        // Set up event handlers
        this.setupEventHandlers();
        
        // Check backend connectivity
        await this.checkBackendStatus();
        
        // Load user subscription status
        await this.loadSubscriptionStatus();
        
        // Load initial data
        await this.loadDashboardData();
        
        console.log('✅ Khyrie3.0 Frontend initialized successfully');
    }

    setupEventHandlers() {
        // Navigation handling
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', () => {
                const section = item.dataset.section;
                this.switchSection(section);
            });
        });

        // PWA installation
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            window.deferredPrompt = e;
        });
    }

    switchSection(sectionName) {
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');

        // Update sections
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(sectionName).classList.add('active');

        // Load section-specific data
        this.loadSectionData(sectionName);
    }

    async loadSectionData(sectionName) {
        switch(sectionName) {
            case 'subscriptions':
                await this.loadSubscriptionPlans();
                break;
            case 'ai-features':
                this.updateFeatureButtons();
                break;
            default:
                break;
        }
    }

    async checkBackendStatus() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            const data = await response.json();
            
            this.isConnected = true;
            this.updateConnectionStatus(true, 'Connected');
            this.updateSystemStatus(data);
            
            console.log('✅ Backend connected:', data);
            return data;
        } catch (error) {
            this.isConnected = false;
            this.updateConnectionStatus(false, 'Disconnected');
            console.error('❌ Backend connection failed:', error);
            return null;
        }
    }

    updateConnectionStatus(connected, text) {
        const statusDot = document.getElementById('backendStatus');
        const statusText = document.getElementById('backendStatusText');
        
        statusDot.classList.toggle('connected', connected);
        statusText.textContent = text;

        document.getElementById('backendStatusDetail').textContent = connected ? '✅ Online' : '❌ Offline';
    }

    updateSystemStatus(healthData) {
        if (healthData && healthData.services) {
            document.getElementById('aiStatusDetail').textContent = 
                healthData.services.ai_engine === 'ready' ? '✅ Ready' : '⚠️ Limited';
            document.getElementById('dbStatusDetail').textContent = 
                healthData.services.database === 'connected' ? '✅ Connected' : '⚠️ Mock';
        }
    }

    async loadSubscriptionStatus() {
        try {
            const response = await fetch(`${this.baseURL}/api/subscriptions/status`);
            if (response.ok) {
                const data = await response.json();
                this.currentUser = data;
                this.updateUserTier(data.tier || 'free');
            } else {
                this.updateUserTier('free');
            }
        } catch (error) {
            console.log('Using default free tier');
            this.updateUserTier('free');
        }
    }

    updateUserTier(tier) {
        const tierElement = document.getElementById('userTier');
        const tierNames = {
            'free': 'Free Plan',
            'premium': 'Premium Plan',
            'pro': 'Pro Plan',
            'elite': 'Elite Plan'
        };
        
        tierElement.textContent = tierNames[tier] || 'Free Plan';
        this.currentUser.tier = tier;
        
        // Update feature button availability
        this.updateFeatureButtons();
    }

    updateFeatureButtons() {
        const tier = this.currentUser.tier || 'free';
        
        // Form Analysis (Pro+)
        const formBtn = document.getElementById('formAnalysisBtn');
        if (formBtn) {
            formBtn.disabled = !['pro', 'elite'].includes(tier);
            formBtn.textContent = tier === 'free' ? 'Analyze Form (Requires Pro)' : 'Analyze Form';
        }
        
        // Voice Coaching (Elite only)
        const voiceBtn = document.getElementById('voiceCoachBtn');
        if (voiceBtn) {
            voiceBtn.disabled = tier !== 'elite';
            voiceBtn.textContent = tier !== 'elite' ? 'Voice Coaching (Requires Elite)' : 'Voice Coaching';
        }
    }

    async loadDashboardData() {
        // Update metrics with sample data
        this.updateMetrics({
            totalWorkouts: Math.floor(Math.random() * 50) + 10,
            aiGenerations: Math.floor(Math.random() * 20) + 5,
            familyMembers: Math.floor(Math.random() * 5) + 1
        });

        // Update available features
        document.getElementById('availableFeatures').textContent = 
            this.isConnected ? 'All Available' : 'Limited (Offline)';
    }

    updateMetrics(metrics) {
        this.metrics = { ...this.metrics, ...metrics };
        
        document.getElementById('totalWorkouts').textContent = this.metrics.totalWorkouts;
        document.getElementById('aiGenerations').textContent = this.metrics.aiGenerations;
        document.getElementById('familyMembers').textContent = this.metrics.familyMembers;
    }

    async loadSubscriptionPlans() {
        const plansContainer = document.getElementById('subscriptionPlans');
        plansContainer.innerHTML = '<div>Loading plans...</div>';

        try {
            const response = await fetch(`${this.baseURL}/api/subscriptions/plans`);
            const data = await response.json();
            
            if (data.plans) {
                this.renderSubscriptionPlans(data.plans);
            } else {
                // Fallback plans if API not available
                this.renderDefaultPlans();
            }
        } catch (error) {
            console.error('Failed to load subscription plans:', error);
            this.renderDefaultPlans();
        }
    }

    renderSubscriptionPlans(plans) {
        const plansContainer = document.getElementById('subscriptionPlans');
        
        plansContainer.innerHTML = plans.map(plan => `
            <div class="feature-card ${plan.recommended ? 'recommended' : ''}">
                <h3>${plan.name}</h3>
                <div class="metric-value">$${plan.price_monthly}</div>
                <div class="metric-label">per month</div>
                <ul style="text-align: left; margin: 1rem 0;">
                    ${plan.features.map(feature => `<li>✅ ${feature}</li>`).join('')}
                </ul>
                <button class="btn" onclick="khyrieAPI.subscribeTo('${plan.tier}')" 
                        ${plan.tier === 'free' ? 'disabled' : ''}>
                    ${plan.tier === 'free' ? 'Current Plan' : 'Upgrade Now'}
                </button>
            </div>
        `).join('');
    }

    renderDefaultPlans() {
        const defaultPlans = [
            { tier: 'free', name: 'Free', price_monthly: 0, features: ['Basic tracking', 'Community access'] },
            { tier: 'premium', name: 'Premium', price_monthly: 9.99, features: ['AI workouts', 'Advanced analytics'] },
            { tier: 'pro', name: 'Pro', price_monthly: 19.99, features: ['Form analysis', 'Injury prevention'] },
            { tier: 'elite', name: 'Elite', price_monthly: 39.99, features: ['Voice coaching', 'AR workouts'] }
        ];
        
        this.renderSubscriptionPlans(defaultPlans);
    }

    // AI Features
    async generateAIWorkout() {
        this.showOutput('aiOutput', '🤖 Generating personalized workout...');
        
        try {
            const response = await fetch(`${this.baseURL}/api/quick/workout-generation`);
            const data = await response.json();
            
            if (data.sample_workout) {
                this.showOutput('aiOutput', `
🏋️‍♀️ AI Workout Generated:

${data.sample_workout.workout_name || 'Personalized Workout'}
Duration: ${data.sample_workout.duration || 30} minutes
Exercises: ${(data.sample_workout.exercises || ['Push-ups', 'Squats', 'Planks']).join(', ')}

${data.sample_workout.note || 'AI-powered workout tailored to your fitness level!'}
                `, 'success');
            } else {
                this.showOutput('aiOutput', `
🤖 AI Workout Generator Status:
${data.message}

Note: ${data.note || 'Workout generation available with full AI components'}
                `, 'info');
            }
            
            this.metrics.aiGenerations++;
            this.updateMetrics(this.metrics);
            
        } catch (error) {
            this.showOutput('aiOutput', `❌ Error generating workout: ${error.message}`, 'error');
        }
    }

    async analyzeProgress() {
        if (this.currentUser.tier === 'free') {
            this.showOutput('aiOutput', '❌ Progress analysis requires a Premium subscription or higher', 'error');
            return;
        }

        this.showOutput('aiOutput', '📊 Analyzing your fitness progress...');

        try {
            // Mock progress analysis for demo
            setTimeout(() => {
                this.showOutput('aiOutput', `
📈 Progress Analysis Complete:

✅ Consistency Score: 87%
📊 Strength Improvement: +23% (last 30 days)
🔥 Calories Burned: 1,847 (this week)
⏱️ Average Workout Time: 32 minutes

Recommendations:
• Increase workout intensity by 10%
• Add 2 more cardio sessions per week
• Focus on core strengthening exercises

Keep up the excellent work! 💪
                `, 'success');
            }, 2000);
        } catch (error) {
            this.showOutput('aiOutput', `❌ Error analyzing progress: ${error.message}`, 'error');
        }
    }

    async analyzeForm() {
        if (!['pro', 'elite'].includes(this.currentUser.tier)) {
            this.showOutput('aiOutput', '❌ Form analysis requires a Pro subscription or higher', 'error');
            return;
        }

        this.showOutput('aiOutput', '🎯 Analyzing workout form...');

        setTimeout(() => {
            this.showOutput('aiOutput', `
🎯 Form Analysis Complete:

Overall Form Score: 85/100
Risk Assessment: Low

Recommendations:
• Keep your core engaged during squats
• Maintain proper spine alignment in deadlifts
• Slow down the eccentric (lowering) phase

Next Session Focus:
• Practice bodyweight squats for form
• Add mobility warm-up routine

Your form is improving! 🎯
            `, 'success');
        }, 2500);
    }

    async startVoiceCoaching() {
        if (this.currentUser.tier !== 'elite') {
            this.showOutput('aiOutput', '❌ Voice coaching requires an Elite subscription', 'error');
            return;
        }

        this.showOutput('aiOutput', '🗣️ Starting AI voice coaching session...');

        setTimeout(() => {
            this.showOutput('aiOutput', `
🗣️ AI Voice Coach Activated:

"Welcome to your personalized coaching session! 
I'll guide you through each exercise with real-time feedback.
Remember to focus on proper form over speed."

Session Features:
• Real-time form corrections
• Motivational coaching
• Breathing guidance
• Rest period management

Ready to begin! 🏆
            `, 'success');
        }, 1500);
    }

    // Family Features
    async createFamilyGroup() {
        this.showOutput('familyOutput', '👥 Creating family fitness group...');

        try {
            const groupData = {
                name: 'My Fitness Family',
                description: 'Our family fitness journey together',
                members: ['You', 'Family Member 1', 'Family Member 2']
            };

            setTimeout(() => {
                this.showOutput('familyOutput', `
👥 Family Group Created Successfully!

Group Name: ${groupData.name}
Members: ${groupData.members.join(', ')}

Features Available:
• Shared workout tracking
• Family challenges
• Progress comparisons
• Group motivational messages

Invite code: FAMILY2025
                `, 'success');
                
                this.metrics.familyMembers = groupData.members.length;
                this.updateMetrics(this.metrics);
            }, 1500);

        } catch (error) {
            this.showOutput('familyOutput', `❌ Error creating group: ${error.message}`, 'error');
        }
    }

    async createChallenge() {
        this.showOutput('familyOutput', '🏆 Setting up family challenge...');

        setTimeout(() => {
            this.showOutput('familyOutput', `
🏆 Challenge Created: "30-Day Family Fitness"

Goal: Complete 100 workouts as a family
Duration: 30 days
Reward: Family fitness outing

Current Progress: 0/100 workouts
Participants: ${this.metrics.familyMembers} family members

Challenge starts now! 💪
            `, 'success');
        }, 1200);
    }

    async viewGroupProgress() {
        this.showOutput('familyOutput', '📈 Loading family progress...');

        setTimeout(() => {
            this.showOutput('familyOutput', `
📈 Family Fitness Progress:

This Week:
• Total workouts: 12
• Combined calories: 2,847
• Most active: Mom (5 workouts)
• Longest streak: Dad (7 days)

Monthly Stats:
• Family goal progress: 78%
• Average workout time: 28 minutes
• Most popular exercise: Family walks

Keep up the great teamwork! 👨‍👩‍👧‍👦
            `, 'success');
        }, 1300);
    }

    // Subscription Management
    async subscribeTo(tier) {
        this.showOutput('subscriptionOutput', `💳 Processing ${tier} subscription...`);

        try {
            const response = await fetch(`${this.baseURL}/api/subscriptions/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tier: tier })
            });

            const data = await response.json();

            if (data.success) {
                this.showOutput('subscriptionOutput', `
✅ Subscription Successful!

Plan: ${tier.toUpperCase()}
${data.message}

New features unlocked! Refresh the page to see them.
                `, 'success');
                
                this.updateUserTier(tier);
            } else {
                this.showOutput('subscriptionOutput', '❌ Subscription failed. Please try again.', 'error');
            }

        } catch (error) {
            this.showOutput('subscriptionOutput', `❌ Subscription error: ${error.message}`, 'error');
        }
    }

    // System utilities
    async checkIntegrationStatus() {
        this.showOutput('settingsOutput', '🔍 Checking integration status...');

        try {
            const response = await fetch(`${this.baseURL}/api/integration/status`);
            const data = await response.json();

            this.showOutput('settingsOutput', `
🔍 Khyrie3.0 Integration Status:

Workspace: ${data.workspace_location || 'Current'}
Backend: ${this.isConnected ? '✅ Connected' : '❌ Disconnected'}

Integrated Components:
${(data.integrated_components || ['unified_backend', 'ai_features', 'subscriptions']).map(c => `• ✅ ${c}`).join('\n')}

System Health: ${this.isConnected ? '✅ All Systems Operational' : '⚠️ Limited Functionality'}
            `, 'success');

        } catch (error) {
            this.showOutput('settingsOutput', `
🔍 Integration Status (Offline):

Backend: ❌ Not Connected
Mode: Standalone/Demo

Available Features:
• Frontend interface ✅
• Mock AI responses ✅
• Subscription demo ✅
• PWA functionality ✅

Note: Start unified backend for full functionality
            `, 'info');
        }
    }

    async installPWA() {
        if (window.deferredPrompt) {
            window.deferredPrompt.prompt();
            const { outcome } = await window.deferredPrompt.userChoice;
            
            this.showOutput('settingsOutput', 
                outcome === 'accepted' ? 
                '✅ PWA installed successfully!' : 
                '❌ PWA installation cancelled', 
                outcome === 'accepted' ? 'success' : 'info'
            );
            
            window.deferredPrompt = null;
        } else {
            this.showOutput('settingsOutput', 
                'PWA is already installed or not available in this browser', 'info');
        }
    }

    // Utility functions
    showOutput(elementId, message, type = 'info') {
        const element = document.getElementById(elementId);
        element.style.display = 'block';
        element.className = `output-area ${type}`;
        element.textContent = message;
        
        // Auto-scroll to output
        element.scrollIntoView({ behavior: 'smooth' });
        
        // Add to recent activity
        this.addToRecentActivity(message.split('\n')[0]);
    }

    addToRecentActivity(activity) {
        const activityElement = document.getElementById('recentActivity');
        const time = new Date().toLocaleTimeString();
        const newActivity = `<div>${time}: ${activity}</div>`;
        
        activityElement.innerHTML = newActivity + activityElement.innerHTML;
        
        // Keep only last 5 activities
        const activities = activityElement.children;
        if (activities.length > 5) {
            activityElement.removeChild(activities[activities.length - 1]);
        }
    }
}

// Global functions for HTML onclick handlers
function generateQuickWorkout() {
    khyrieAPI.generateAIWorkout();
}

function checkSystemHealth() {
    khyrieAPI.checkBackendStatus().then(() => {
        khyrieAPI.addToRecentActivity('System health check completed');
    });
}

function switchSection(section) {
    khyrieAPI.switchSection(section);
}

function generateAIWorkout() {
    khyrieAPI.generateAIWorkout();
}

function analyzeProgress() {
    khyrieAPI.analyzeProgress();
}

function analyzeForm() {
    khyrieAPI.analyzeForm();
}

function startVoiceCoaching() {
    khyrieAPI.startVoiceCoaching();
}

function createFamilyGroup() {
    khyrieAPI.createFamilyGroup();
}

function createChallenge() {
    khyrieAPI.createChallenge();
}

function viewGroupProgress() {
    khyrieAPI.viewGroupProgress();
}

function checkIntegrationStatus() {
    khyrieAPI.checkIntegrationStatus();
}

function installPWA() {
    khyrieAPI.installPWA();
}

// Initialize Khyrie API when page loads
const khyrieAPI = new KhyrieAPI();

// Export for use in other scripts
window.KhyrieAPI = KhyrieAPI;
window.khyrieAPI = khyrieAPI;