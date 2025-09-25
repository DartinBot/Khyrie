/**
 * Offline Workout Manager - Client-side JavaScript
 * Manages offline workout storage, synchronization, and user interface
 */

class OfflineWorkoutManager {
    constructor() {
        this.dbName = 'KhyrieOfflineDB';
        this.dbVersion = 1;
        this.db = null;
        this.isOnline = navigator.onLine;
        
        this.init();
        this.setupEventListeners();
    }
    
    /**
     * Initialize offline capabilities
     */
    async init() {
        try {
            // Register service worker
            await this.registerServiceWorker();
            
            // Initialize IndexedDB
            await this.initDatabase();
            
            // Setup offline UI indicators
            this.updateOfflineStatus();
            
            // Sync any pending data if online
            if (this.isOnline) {
                await this.syncPendingData();
            }
            
            console.log('🏋️ Offline workout capability initialized');
            
        } catch (error) {
            console.error('❌ Failed to initialize offline capability:', error);
        }
    }
    
    /**
     * Register service worker for offline functionality
     */
    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/offline-worker.js');
                console.log('✅ Service worker registered for offline support');
                
                // Listen for service worker updates
                registration.addEventListener('updatefound', () => {
                    console.log('🔄 Service worker updating...');
                });
                
                return registration;
                
            } catch (error) {
                console.error('❌ Service worker registration failed:', error);
                throw error;
            }
        } else {
            throw new Error('Service workers not supported');
        }
    }
    
    /**
     * Initialize IndexedDB for offline data storage
     */
    async initDatabase() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.dbVersion);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve(this.db);
            };
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                
                // Workouts store
                if (!db.objectStoreNames.contains('workouts')) {
                    const workoutStore = db.createObjectStore('workouts', { keyPath: 'id', autoIncrement: true });
                    workoutStore.createIndex('synced', 'synced', { unique: false });
                    workoutStore.createIndex('timestamp', 'timestamp', { unique: false });
                }
                
                // Exercise library store
                if (!db.objectStoreNames.contains('exercises')) {
                    const exerciseStore = db.createObjectStore('exercises', { keyPath: 'id' });
                    exerciseStore.createIndex('category', 'category', { unique: false });
                }
                
                // User progress store
                if (!db.objectStoreNames.contains('progress')) {
                    const progressStore = db.createObjectStore('progress', { keyPath: 'id', autoIncrement: true });
                    progressStore.createIndex('date', 'date', { unique: false });
                    progressStore.createIndex('synced', 'synced', { unique: false });
                }
                
                console.log('📊 Offline database schema created');
            };
        });
    }
    
    /**
     * Setup event listeners for online/offline detection
     */
    setupEventListeners() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.updateOfflineStatus();
            this.syncPendingData();
            console.log('🌐 Back online - syncing data...');
        });
        
        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.updateOfflineStatus();
            console.log('📱 Gone offline - enabling offline mode...');
        });
        
        // Listen for service worker messages
        navigator.serviceWorker.addEventListener('message', (event) => {
            console.log('📨 Message from service worker:', event.data);
        });
    }
    
    /**
     * Update UI to show offline/online status
     */
    updateOfflineStatus() {
        const statusIndicator = document.getElementById('offline-status');
        
        if (!statusIndicator) {
            // Create status indicator if it doesn't exist
            const indicator = document.createElement('div');
            indicator.id = 'offline-status';
            indicator.style.cssText = `
                position: fixed;
                top: 10px;
                right: 10px;
                padding: 8px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                z-index: 1000;
                transition: all 0.3s ease;
            `;
            document.body.appendChild(indicator);
        }
        
        const indicator = document.getElementById('offline-status');
        
        if (this.isOnline) {
            indicator.textContent = '🌐 Online';
            indicator.style.backgroundColor = '#10b981';
            indicator.style.color = 'white';
        } else {
            indicator.textContent = '📱 Offline Mode';
            indicator.style.backgroundColor = '#f59e0b';
            indicator.style.color = 'white';
        }
    }
    
    /**
     * Save workout data for offline use
     */
    async saveWorkoutOffline(workoutData) {
        try {
            const transaction = this.db.transaction(['workouts'], 'readwrite');
            const store = transaction.objectStore('workouts');
            
            const offlineWorkout = {
                ...workoutData,
                timestamp: new Date().toISOString(),
                synced: false,
                offline: true
            };
            
            await store.add(offlineWorkout);
            
            console.log('💾 Workout saved offline:', workoutData.name);
            
            // Show offline confirmation
            this.showOfflineConfirmation('Workout saved offline - will sync when online');
            
            // Schedule background sync when online
            if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
                const registration = await navigator.serviceWorker.ready;
                await registration.sync.register('workout-sync');
            }
            
            return true;
            
        } catch (error) {
            console.error('❌ Failed to save workout offline:', error);
            return false;
        }
    }
    
    /**
     * Get offline workouts
     */
    async getOfflineWorkouts() {
        try {
            const transaction = this.db.transaction(['workouts'], 'readonly');
            const store = transaction.objectStore('workouts');
            
            return new Promise((resolve, reject) => {
                const request = store.getAll();
                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            });
            
        } catch (error) {
            console.error('❌ Failed to get offline workouts:', error);
            return [];
        }
    }
    
    /**
     * Cache exercise library for offline use
     */
    async cacheExerciseLibrary() {
        try {
            const response = await fetch('/api/exercises/library');
            const exercises = await response.json();
            
            const transaction = this.db.transaction(['exercises'], 'readwrite');
            const store = transaction.objectStore('exercises');
            
            for (const exercise of exercises) {
                await store.put(exercise);
            }
            
            console.log('📚 Exercise library cached for offline use');
            
        } catch (error) {
            console.error('❌ Failed to cache exercise library:', error);
        }
    }
    
    /**
     * Get cached exercise library
     */
    async getCachedExercises() {
        try {
            const transaction = this.db.transaction(['exercises'], 'readonly');
            const store = transaction.objectStore('exercises');
            
            return new Promise((resolve, reject) => {
                const request = store.getAll();
                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            });
            
        } catch (error) {
            console.error('❌ Failed to get cached exercises:', error);
            return [];
        }
    }
    
    /**
     * Sync pending data when back online
     */
    async syncPendingData() {
        if (!this.isOnline || !this.db) return;
        
        try {
            console.log('🔄 Syncing offline data...');
            
            // Get unsynced workouts
            const transaction = this.db.transaction(['workouts'], 'readonly');
            const store = transaction.objectStore('workouts');
            const index = store.index('synced');
            
            const unsyncedWorkouts = await new Promise((resolve, reject) => {
                const request = index.getAll(false);
                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            });
            
            // Sync each workout
            for (const workout of unsyncedWorkouts) {
                try {
                    await this.syncWorkout(workout);
                } catch (error) {
                    console.error('❌ Failed to sync workout:', workout.id, error);
                }
            }
            
            if (unsyncedWorkouts.length > 0) {
                this.showOfflineConfirmation(`✅ Synced ${unsyncedWorkouts.length} offline workouts`);
            }
            
        } catch (error) {
            console.error('❌ Data sync failed:', error);
        }
    }
    
    /**
     * Sync individual workout
     */
    async syncWorkout(workout) {
        try {
            const response = await fetch('/api/workouts/complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(workout)
            });
            
            if (response.ok) {
                // Mark as synced in local database
                const transaction = this.db.transaction(['workouts'], 'readwrite');
                const store = transaction.objectStore('workouts');
                
                workout.synced = true;
                workout.syncedAt = new Date().toISOString();
                
                await store.put(workout);
                
                console.log('✅ Workout synced:', workout.id);
            }
            
        } catch (error) {
            console.error('❌ Failed to sync workout:', error);
            throw error;
        }
    }
    
    /**
     * Show offline confirmation message
     */
    showOfflineConfirmation(message) {
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #1f2937;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            z-index: 1001;
            animation: slideUp 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
    
    /**
     * Get offline workout templates
     */
    getOfflineWorkoutTemplates() {
        return [
            {
                id: 'offline-bodyweight',
                name: 'Bodyweight Basics',
                description: 'No equipment needed - perfect for offline workouts',
                duration: 20,
                difficulty: 'beginner',
                exercises: [
                    { name: 'Push-ups', sets: 3, reps: '8-12', rest: 60 },
                    { name: 'Squats', sets: 3, reps: '12-15', rest: 60 },
                    { name: 'Lunges', sets: 3, reps: '10 each leg', rest: 60 },
                    { name: 'Plank', sets: 3, duration: '30-45 seconds', rest: 60 },
                    { name: 'Jumping Jacks', sets: 3, duration: '30 seconds', rest: 60 }
                ]
            },
            {
                id: 'offline-hiit',
                name: 'Family HIIT Circuit',
                description: 'High intensity workout for the whole family',
                duration: 15,
                difficulty: 'intermediate',
                exercises: [
                    { name: 'Burpees', sets: 4, reps: '5-8', rest: 30 },
                    { name: 'Mountain Climbers', sets: 4, duration: '20 seconds', rest: 30 },
                    { name: 'Jump Squats', sets: 4, reps: '10-12', rest: 30 },
                    { name: 'High Knees', sets: 4, duration: '20 seconds', rest: 30 }
                ]
            },
            {
                id: 'offline-strength',
                name: 'Bodyweight Strength',
                description: 'Build strength without equipment',
                duration: 25,
                difficulty: 'intermediate',
                exercises: [
                    { name: 'Pike Push-ups', sets: 3, reps: '5-8', rest: 90 },
                    { name: 'Single-leg Squats', sets: 3, reps: '5 each leg', rest: 90 },
                    { name: 'Diamond Push-ups', sets: 3, reps: '5-10', rest: 90 },
                    { name: 'Wall Sit', sets: 3, duration: '45-60 seconds', rest: 90 }
                ]
            }
        ];
    }
}

// CSS for offline animations
const offlineStyles = `
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }
    
    .offline-workout-card {
        border: 2px solid #f59e0b;
        background: linear-gradient(135deg, #fef3c7 0%, #fcd34d 100%);
        position: relative;
    }
    
    .offline-workout-card::before {
        content: "📱 OFFLINE";
        position: absolute;
        top: 10px;
        right: 10px;
        background: #f59e0b;
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 600;
    }
    
    .sync-pending {
        border-left: 4px solid #3b82f6;
        background: linear-gradient(135deg, #dbeafe 0%, #93c5fd 100%);
    }
    
    .sync-pending::after {
        content: "🔄 SYNC PENDING";
        position: absolute;
        bottom: 10px;
        right: 10px;
        color: #1d4ed8;
        font-size: 10px;
        font-weight: 600;
    }
`;

// Add offline styles to document
const styleSheet = document.createElement('style');
styleSheet.textContent = offlineStyles;
document.head.appendChild(styleSheet);

// Initialize offline manager when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.offlineWorkoutManager = new OfflineWorkoutManager();
    });
} else {
    window.offlineWorkoutManager = new OfflineWorkoutManager();
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OfflineWorkoutManager;
}

console.log('🏋️ Offline Workout Manager loaded!');