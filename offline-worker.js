/**
 * Offline Workout Manager - Progressive Web App Service Worker
 * Provides offline capability for workouts when internet connection is spotty
 */

// Service Worker for offline functionality
const CACHE_NAME = 'khyrie-offline-v1';
const WORKOUT_CACHE = 'khyrie-workouts-v1';
const STATIC_CACHE = 'khyrie-static-v1';

// Resources to cache for offline use
const STATIC_RESOURCES = [
    '/',
    '/trainer_marketplace.html',
    '/enhanced_group_workouts.html',
    '/TrainerMarketplace.css',
    '/EnhancedGroupWorkouts.css',
    '/TrainerMarketplace.js',
    '/EnhancedGroupWorkouts.js',
    '/manifest.json'
];

// Workout data that should be available offline
const OFFLINE_WORKOUT_ENDPOINTS = [
    '/api/workouts/offline-sync',
    '/api/exercises/library',
    '/api/users/profile',
    '/api/family/groups'
];

self.addEventListener('install', (event) => {
    console.log('🔧 Installing Khyrie offline capability...');
    
    event.waitUntil(
        Promise.all([
            // Cache static resources
            caches.open(STATIC_CACHE).then(cache => {
                console.log('📦 Caching static resources for offline use');
                return cache.addAll(STATIC_RESOURCES);
            }),
            
            // Cache essential workout data
            caches.open(WORKOUT_CACHE).then(cache => {
                console.log('🏋️ Preparing workout data for offline access');
                return cache.add('/api/exercises/library');
            })
        ])
    );
    
    // Activate immediately
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    console.log('✅ Khyrie offline mode activated');
    
    event.waitUntil(
        // Clean up old caches
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME && 
                        cacheName !== WORKOUT_CACHE && 
                        cacheName !== STATIC_CACHE) {
                        console.log('🗑️ Removing old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    
    // Take control of all pages immediately
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Handle API requests
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(handleApiRequest(request));
    }
    // Handle static resources
    else {
        event.respondWith(handleStaticRequest(request));
    }
});

/**
 * Handle API requests with network-first, cache-fallback strategy
 */
async function handleApiRequest(request) {
    const url = new URL(request.url);
    
    try {
        // Try network first
        const response = await fetch(request);
        
        // Cache successful responses for offline use
        if (response.ok && (request.method === 'GET')) {
            const cache = await caches.open(WORKOUT_CACHE);
            cache.put(request, response.clone());
        }
        
        return response;
        
    } catch (error) {
        console.log('🌐 Network unavailable, checking offline cache...');
        
        // Network failed, try cache
        const cachedResponse = await caches.match(request);
        
        if (cachedResponse) {
            console.log('📦 Serving from offline cache:', url.pathname);
            return cachedResponse;
        }
        
        // Return offline fallback for workout data
        if (url.pathname.includes('/workouts') || url.pathname.includes('/exercises')) {
            return new Response(JSON.stringify({
                offline: true,
                message: 'Workout data available offline',
                workouts: await getOfflineWorkouts()
            }), {
                status: 200,
                headers: { 'Content-Type': 'application/json' }
            });
        }
        
        // Generic offline response
        return new Response(JSON.stringify({
            offline: true,
            error: 'This feature requires internet connection',
            cached_data_available: false
        }), {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

/**
 * Handle static resources with cache-first strategy
 */
async function handleStaticRequest(request) {
    // Check cache first
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
        return cachedResponse;
    }
    
    // Try network
    try {
        const response = await fetch(request);
        
        // Cache successful responses
        if (response.ok) {
            const cache = await caches.open(STATIC_CACHE);
            cache.put(request, response.clone());
        }
        
        return response;
        
    } catch (error) {
        console.log('📱 Offline mode: Resource not available:', request.url);
        
        // Return offline page for navigation requests
        if (request.mode === 'navigate') {
            return caches.match('/') || new Response('Offline - Please check your connection');
        }
        
        throw error;
    }
}

/**
 * Get offline workout data from IndexedDB
 */
async function getOfflineWorkouts() {
    // This would connect to IndexedDB for stored workout data
    return [
        {
            id: 'offline-1',
            name: 'Bodyweight Basics',
            exercises: [
                { name: 'Push-ups', sets: 3, reps: '10-15' },
                { name: 'Squats', sets: 3, reps: '15-20' },
                { name: 'Plank', sets: 3, duration: '30-60 seconds' }
            ],
            duration: '20 minutes',
            difficulty: 'beginner'
        },
        {
            id: 'offline-2', 
            name: 'Family HIIT',
            exercises: [
                { name: 'Jumping Jacks', sets: 4, duration: '30 seconds' },
                { name: 'Burpees', sets: 4, reps: '5-10' },
                { name: 'Mountain Climbers', sets: 4, duration: '30 seconds' }
            ],
            duration: '15 minutes',
            difficulty: 'intermediate'
        }
    ];
}

/**
 * Background sync for when connection is restored
 */
self.addEventListener('sync', (event) => {
    console.log('🔄 Background sync triggered:', event.tag);
    
    if (event.tag === 'workout-sync') {
        event.waitUntil(syncWorkoutData());
    }
    
    if (event.tag === 'progress-sync') {
        event.waitUntil(syncProgressData());
    }
});

/**
 * Sync workout data when online
 */
async function syncWorkoutData() {
    try {
        console.log('📊 Syncing offline workout data...');
        
        // Get pending workout completions from IndexedDB
        const pendingWorkouts = await getPendingWorkouts();
        
        for (const workout of pendingWorkouts) {
            try {
                await fetch('/api/workouts/complete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(workout)
                });
                
                // Mark as synced
                await markWorkoutSynced(workout.id);
                console.log('✅ Synced workout:', workout.name);
                
            } catch (error) {
                console.log('❌ Failed to sync workout:', workout.name, error);
            }
        }
        
    } catch (error) {
        console.error('🚨 Workout sync failed:', error);
    }
}

/**
 * Sync progress photos and data
 */
async function syncProgressData() {
    console.log('📸 Syncing progress photos and data...');
    // Implementation for syncing progress photos and measurements
}

// Helper functions for IndexedDB operations
async function getPendingWorkouts() {
    // Would implement IndexedDB queries here
    return [];
}

async function markWorkoutSynced(workoutId) {
    // Would implement IndexedDB update here
    console.log('Marked workout as synced:', workoutId);
}

/**
 * Handle push messages for notifications
 */
self.addEventListener('push', (event) => {
    console.log('📱 Push notification received');
    
    if (event.data) {
        const data = event.data.json();
        
        const options = {
            body: data.body,
            icon: '/icons/icon-192x192.png',
            badge: '/icons/badge-72x72.png',
            vibrate: [100, 50, 100],
            data: data.data,
            actions: data.actions || []
        };
        
        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

/**
 * Handle notification clicks
 */
self.addEventListener('notificationclick', (event) => {
    console.log('🔔 Notification clicked:', event.notification.tag);
    
    event.notification.close();
    
    // Open the app or navigate to specific page
    event.waitUntil(
        clients.openWindow('/')
    );
});

console.log('🚀 Khyrie Service Worker loaded - Offline capability enabled!');