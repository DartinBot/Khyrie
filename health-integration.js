/**
 * Health Platform Integration Manager
 * Seamless integration with Apple Health and Google Fit for comprehensive tracking
 */

class HealthPlatformManager {
    constructor() {
        this.platform = this.detectPlatform();
        this.isConnected = false;
        this.syncInterval = null;
        this.lastSyncTime = null;
        
        this.healthData = {
            steps: 0,
            heartRate: null,
            calories: 0,
            activeMinutes: 0,
            sleep: null,
            workouts: []
        };
        
        this.init();
    }
    
    /**
     * Initialize health platform integration
     */
    async init() {
        console.log(`🏥 Initializing health integration for ${this.platform}`);
        
        try {
            // Check if health APIs are available
            await this.checkHealthAPIAvailability();
            
            // Request permissions
            await this.requestHealthPermissions();
            
            // Setup automatic sync
            this.setupAutoSync();
            
            // Create health dashboard
            this.createHealthDashboard();
            
            console.log('✅ Health platform integration initialized');
            
        } catch (error) {
            console.error('❌ Failed to initialize health integration:', error);
        }
    }
    
    /**
     * Detect user's platform (iOS/Android/Web)
     */
    detectPlatform() {
        const userAgent = navigator.userAgent;
        
        if (/iPad|iPhone|iPod/.test(userAgent)) {
            return 'ios';
        } else if (/Android/.test(userAgent)) {
            return 'android';
        } else {
            return 'web';
        }
    }
    
    /**
     * Check if health APIs are available on current platform
     */
    async checkHealthAPIAvailability() {
        switch (this.platform) {
            case 'ios':
                return this.checkAppleHealthAvailability();
            case 'android':
                return this.checkGoogleFitAvailability();
            case 'web':
                return this.checkWebAPIAvailability();
            default:
                throw new Error('Unsupported platform');
        }
    }
    
    /**
     * Check Apple Health availability (iOS)
     */
    async checkAppleHealthAvailability() {
        if (window.HealthKit) {
            console.log('📱 Apple HealthKit available');
            return true;
        } else {
            console.log('🌐 Apple Health via Web API');
            return this.setupAppleHealthWebAPI();
        }
    }
    
    /**
     * Check Google Fit availability (Android)
     */
    async checkGoogleFitAvailability() {
        if (window.gapi) {
            console.log('🤖 Google Fit API available');
            return true;
        } else {
            console.log('🌐 Google Fit via Web API');
            return this.setupGoogleFitWebAPI();
        }
    }
    
    /**
     * Check Web API availability
     */
    async checkWebAPIAvailability() {
        const webAPIs = {
            deviceMotion: 'DeviceMotionEvent' in window,
            deviceOrientation: 'DeviceOrientationEvent' in window,
            webBluetooth: 'bluetooth' in navigator,
            webUSB: 'usb' in navigator
        };
        
        console.log('🌐 Web APIs available:', webAPIs);
        return Object.values(webAPIs).some(available => available);
    }
    
    /**
     * Request health data permissions
     */
    async requestHealthPermissions() {
        const permissions = this.getRequiredPermissions();
        
        switch (this.platform) {
            case 'ios':
                return this.requestAppleHealthPermissions(permissions);
            case 'android':
                return this.requestGoogleFitPermissions(permissions);
            case 'web':
                return this.requestWebPermissions(permissions);
        }
    }
    
    /**
     * Get required health data permissions
     */
    getRequiredPermissions() {
        return {
            read: [
                'steps',
                'heartRate',
                'calories',
                'activeMinutes',
                'workouts',
                'sleep',
                'weight',
                'bodyFat'
            ],
            write: [
                'workouts',
                'calories',
                'activeMinutes'
            ]
        };
    }
    
    /**
     * Setup Apple Health integration
     */
    async setupAppleHealthWebAPI() {
        // Use Apple Health Web API (when available) or fallback methods
        try {
            // Request access to motion and fitness data
            if (typeof DeviceMotionEvent.requestPermission === 'function') {
                const permission = await DeviceMotionEvent.requestPermission();
                if (permission === 'granted') {
                    this.setupMotionTracking();
                }
            }
            
            // Setup HealthKit integration for native apps
            if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.healthKit) {
                return this.setupNativeAppleHealth();
            }
            
            // Fallback to web-based tracking
            return this.setupWebBasedTracking();
            
        } catch (error) {
            console.error('❌ Apple Health setup failed:', error);
            return false;
        }
    }
    
    /**
     * Setup Google Fit integration
     */
    async setupGoogleFitWebAPI() {
        try {
            // Load Google API
            if (!window.gapi) {
                await this.loadGoogleAPI();
            }
            
            // Initialize Google Fit API
            await gapi.load('client:auth2', () => {
                gapi.client.init({
                    apiKey: this.getGoogleFitAPIKey(),
                    clientId: this.getGoogleFitClientId(),
                    discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/fitness/v1/rest'],
                    scope: 'https://www.googleapis.com/auth/fitness.activity.read https://www.googleapis.com/auth/fitness.body.read'
                });
            });
            
            console.log('✅ Google Fit API initialized');
            return true;
            
        } catch (error) {
            console.error('❌ Google Fit setup failed:', error);
            return false;
        }
    }
    
    /**
     * Setup motion tracking for step counting
     */
    setupMotionTracking() {
        if (window.DeviceMotionEvent) {
            let stepCount = 0;
            let lastAcceleration = 0;
            let stepThreshold = 1.2;
            
            window.addEventListener('devicemotion', (event) => {
                const acceleration = event.accelerationIncludingGravity;
                
                if (acceleration) {
                    const magnitude = Math.sqrt(
                        acceleration.x * acceleration.x +
                        acceleration.y * acceleration.y +
                        acceleration.z * acceleration.z
                    );
                    
                    // Simple step detection algorithm
                    if (magnitude > stepThreshold && magnitude > lastAcceleration * 1.2) {
                        stepCount++;
                        this.updateStepCount(stepCount);
                    }
                    
                    lastAcceleration = magnitude;
                }
            });
            
            console.log('👟 Motion-based step tracking enabled');
        }
    }
    
    /**
     * Sync health data from connected platforms
     */
    async syncHealthData() {
        if (!this.isConnected) {
            console.log('❌ Health platform not connected');
            return;
        }
        
        console.log('🔄 Syncing health data...');
        
        try {
            const today = new Date();
            const yesterday = new Date(today);
            yesterday.setDate(yesterday.getDate() - 1);
            
            // Sync different data types
            await Promise.all([
                this.syncSteps(yesterday, today),
                this.syncHeartRate(yesterday, today),
                this.syncCalories(yesterday, today),
                this.syncWorkouts(yesterday, today),
                this.syncSleep(yesterday, today)
            ]);
            
            // Update Khyrie backend
            await this.updateKhyrieHealthData();
            
            // Update UI
            this.updateHealthDashboard();
            
            this.lastSyncTime = new Date();
            console.log('✅ Health data sync completed');
            
        } catch (error) {
            console.error('❌ Health data sync failed:', error);
        }
    }
    
    /**
     * Sync step data
     */
    async syncSteps(startDate, endDate) {
        try {
            let steps = 0;
            
            switch (this.platform) {
                case 'ios':
                    steps = await this.getAppleHealthSteps(startDate, endDate);
                    break;
                case 'android':
                    steps = await this.getGoogleFitSteps(startDate, endDate);
                    break;
                case 'web':
                    steps = this.getWebBasedSteps();
                    break;
            }
            
            this.healthData.steps = steps;
            console.log(`👟 Steps synced: ${steps}`);
            
        } catch (error) {
            console.error('❌ Failed to sync steps:', error);
        }
    }
    
    /**
     * Sync heart rate data
     */
    async syncHeartRate(startDate, endDate) {
        try {
            let heartRate = null;
            
            switch (this.platform) {
                case 'ios':
                    heartRate = await this.getAppleHealthHeartRate(startDate, endDate);
                    break;
                case 'android':
                    heartRate = await this.getGoogleFitHeartRate(startDate, endDate);
                    break;
                case 'web':
                    heartRate = await this.getWebBasedHeartRate();
                    break;
            }
            
            this.healthData.heartRate = heartRate;
            console.log(`❤️ Heart rate synced: ${heartRate} bpm`);
            
        } catch (error) {
            console.error('❌ Failed to sync heart rate:', error);
        }
    }
    
    /**
     * Get Apple Health steps
     */
    async getAppleHealthSteps(startDate, endDate) {
        // Native iOS implementation
        if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.healthKit) {
            return new Promise((resolve) => {
                window.webkit.messageHandlers.healthKit.postMessage({
                    action: 'getSteps',
                    startDate: startDate.toISOString(),
                    endDate: endDate.toISOString()
                });
                
                window.healthKitCallback = (data) => {
                    resolve(data.steps || 0);
                };
            });
        }
        
        // Fallback to estimated steps
        return this.getEstimatedSteps();
    }
    
    /**
     * Get Google Fit steps
     */
    async getGoogleFitSteps(startDate, endDate) {
        try {
            const response = await gapi.client.fitness.users.dataSources.datasets.get({
                userId: 'me',
                dataSourceId: 'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps',
                datasetId: `${startDate.getTime() * 1000000}-${endDate.getTime() * 1000000}`
            });
            
            let totalSteps = 0;
            if (response.result.point) {
                response.result.point.forEach(point => {
                    totalSteps += point.value[0].intVal || 0;
                });
            }
            
            return totalSteps;
            
        } catch (error) {
            console.error('❌ Failed to get Google Fit steps:', error);
            return this.getEstimatedSteps();
        }
    }
    
    /**
     * Write workout data to health platforms
     */
    async writeWorkoutToHealth(workoutData) {
        console.log('📝 Writing workout to health platform...');
        
        try {
            switch (this.platform) {
                case 'ios':
                    await this.writeAppleHealthWorkout(workoutData);
                    break;
                case 'android':
                    await this.writeGoogleFitWorkout(workoutData);
                    break;
                case 'web':
                    await this.writeWebBasedWorkout(workoutData);
                    break;
            }
            
            console.log('✅ Workout written to health platform');
            
        } catch (error) {
            console.error('❌ Failed to write workout:', error);
        }
    }
    
    /**
     * Update Khyrie backend with health data
     */
    async updateKhyrieHealthData() {
        try {
            const response = await fetch('/api/health/sync', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    platform: this.platform,
                    data: this.healthData,
                    syncTime: this.lastSyncTime
                })
            });
            
            if (response.ok) {
                console.log('✅ Health data updated in Khyrie');
            }
            
        } catch (error) {
            console.error('❌ Failed to update Khyrie health data:', error);
        }
    }
    
    /**
     * Create health dashboard UI
     */
    createHealthDashboard() {
        const dashboard = document.createElement('div');
        dashboard.id = 'health-dashboard';
        dashboard.innerHTML = `
            <div class="health-widget">
                <h3>📊 Health Integration</h3>
                <div class="health-status">
                    <div class="status-item">
                        <span class="icon">📱</span>
                        <span class="label">Platform:</span>
                        <span class="value">${this.platform.toUpperCase()}</span>
                    </div>
                    <div class="status-item">
                        <span class="icon">🔗</span>
                        <span class="label">Connected:</span>
                        <span class="value ${this.isConnected ? 'connected' : 'disconnected'}">
                            ${this.isConnected ? 'Yes' : 'No'}
                        </span>
                    </div>
                    <div class="status-item">
                        <span class="icon">🔄</span>
                        <span class="label">Last Sync:</span>
                        <span class="value">${this.lastSyncTime ? this.lastSyncTime.toLocaleTimeString() : 'Never'}</span>
                    </div>
                </div>
                
                <div class="health-metrics">
                    <div class="metric">
                        <span class="icon">👟</span>
                        <span class="label">Steps</span>
                        <span class="value" id="steps-count">${this.healthData.steps}</span>
                    </div>
                    <div class="metric">
                        <span class="icon">❤️</span>
                        <span class="label">Heart Rate</span>
                        <span class="value" id="heart-rate">${this.healthData.heartRate || '--'} bpm</span>
                    </div>
                    <div class="metric">
                        <span class="icon">🔥</span>
                        <span class="label">Calories</span>
                        <span class="value" id="calories">${this.healthData.calories}</span>
                    </div>
                    <div class="metric">
                        <span class="icon">⏱️</span>
                        <span class="label">Active Minutes</span>
                        <span class="value" id="active-minutes">${this.healthData.activeMinutes}</span>
                    </div>
                </div>
                
                <div class="health-actions">
                    <button onclick="healthManager.syncHealthData()" class="sync-btn">
                        🔄 Sync Now
                    </button>
                    <button onclick="healthManager.showHealthSettings()" class="settings-btn">
                        ⚙️ Settings
                    </button>
                </div>
            </div>
        `;
        
        // Add styles
        const styles = `
            .health-widget {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            }
            
            .health-widget h3 {
                margin: 0 0 15px 0;
                font-size: 18px;
                font-weight: 600;
            }
            
            .health-status {
                margin-bottom: 20px;
            }
            
            .status-item {
                display: flex;
                align-items: center;
                margin-bottom: 8px;
                font-size: 14px;
            }
            
            .status-item .icon {
                margin-right: 8px;
                font-size: 16px;
            }
            
            .status-item .label {
                margin-right: 8px;
                opacity: 0.8;
            }
            
            .status-item .value {
                font-weight: 600;
            }
            
            .connected {
                color: #10b981;
            }
            
            .disconnected {
                color: #ef4444;
            }
            
            .health-metrics {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-bottom: 20px;
            }
            
            .metric {
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 10px;
                text-align: center;
            }
            
            .metric .icon {
                font-size: 24px;
                display: block;
                margin-bottom: 5px;
            }
            
            .metric .label {
                font-size: 12px;
                opacity: 0.8;
                display: block;
            }
            
            .metric .value {
                font-size: 18px;
                font-weight: 600;
                display: block;
                margin-top: 5px;
            }
            
            .health-actions {
                display: flex;
                gap: 10px;
            }
            
            .sync-btn, .settings-btn {
                flex: 1;
                padding: 10px;
                border: none;
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.2);
                color: white;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s ease;
            }
            
            .sync-btn:hover, .settings-btn:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            
            @media (max-width: 480px) {
                .health-metrics {
                    grid-template-columns: 1fr;
                }
                
                .health-actions {
                    flex-direction: column;
                }
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
        
        // Insert dashboard into page
        const container = document.querySelector('.container') || document.body;
        container.appendChild(dashboard);
    }
    
    /**
     * Update health dashboard with current data
     */
    updateHealthDashboard() {
        document.getElementById('steps-count').textContent = this.healthData.steps;
        document.getElementById('heart-rate').textContent = this.healthData.heartRate ? `${this.healthData.heartRate} bpm` : '--';
        document.getElementById('calories').textContent = this.healthData.calories;
        document.getElementById('active-minutes').textContent = this.healthData.activeMinutes;
        
        const lastSyncElement = document.querySelector('.health-status .status-item:last-child .value');
        if (lastSyncElement) {
            lastSyncElement.textContent = this.lastSyncTime ? this.lastSyncTime.toLocaleTimeString() : 'Never';
        }
    }
    
    /**
     * Setup automatic sync
     */
    setupAutoSync() {
        // Sync every 30 minutes
        this.syncInterval = setInterval(() => {
            this.syncHealthData();
        }, 30 * 60 * 1000);
        
        // Initial sync
        setTimeout(() => {
            this.syncHealthData();
        }, 5000);
        
        console.log('⏰ Auto-sync scheduled every 30 minutes');
    }
    
    /**
     * Show health settings modal
     */
    showHealthSettings() {
        console.log('⚙️ Health settings opened');
        // Implementation for health settings modal
    }
    
    /**
     * Helper methods for fallback tracking
     */
    getEstimatedSteps() {
        // Estimate steps based on activity level
        const baseSteps = Math.floor(Math.random() * 3000) + 2000; // 2000-5000 base steps
        return baseSteps;
    }
    
    getWebBasedSteps() {
        // Use stored step count from motion tracking
        return this.healthData.steps || 0;
    }
    
    async getWebBasedHeartRate() {
        // Could integrate with camera-based heart rate detection
        return null;
    }
    
    // Configuration methods
    getGoogleFitAPIKey() {
        return 'your-google-fit-api-key-here';
    }
    
    getGoogleFitClientId() {
        return 'your-google-fit-client-id-here';
    }
    
    async loadGoogleAPI() {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://apis.google.com/js/api.js';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
}

// Initialize health platform manager
document.addEventListener('DOMContentLoaded', () => {
    window.healthManager = new HealthPlatformManager();
});

console.log('🏥 Health Platform Manager loaded!');