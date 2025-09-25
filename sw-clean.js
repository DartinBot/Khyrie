// Service Worker for Khyrie PWA
// Advanced caching, offline functionality, and background sync

const CACHE_VERSION = 'khyrie-v1.2.0';
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const DYNAMIC_CACHE = `${CACHE_VERSION}-dynamic`;
const API_CACHE = `${CACHE_VERSION}-api`;
const IMAGE_CACHE = `${CACHE_VERSION}-images`;

// Static assets to cache immediately
const STATIC_ASSETS = [
    '/',
    '/mobile-index.html',
    '/mobile-app.css',
    '/manifest.json',
    '/offline-worker.js',
    '/offline-manager.js',
    '/family-notifications.js',
    '/health-integration.js',
    '/camera-integration.js',
    '/pwa-installer.js',
    // Core app files
    '/Dashboard.css',
    '/Dashboard.js',
    '/AIDashboard.css',
    '/AIDashboard.js',
    // Icons (placeholder paths - will be updated when icons are generated)
    '/icons/khyrie-72.png',
    '/icons/khyrie-96.png',
    '/icons/khyrie-128.png',
    '/icons/khyrie-144.png',
    '/icons/khyrie-152.png',
    '/icons/khyrie-192.png',
    '/icons/khyrie-384.png',
    '/icons/khyrie-512.png'
];

// API endpoints to cache
const API_ENDPOINTS = [
    '/api/workouts',
    '/api/user/profile',
    '/api/family',
    '/api/trainers',
    '/api/health-data',
    '/api/offline-sync'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
    console.log('🔧 Service Worker installing...');
    
    event.waitUntil(
        Promise.all([
            caches.open(STATIC_CACHE).then((cache) => {
                console.log('📦 Caching static assets...');
                return cache.addAll(STATIC_ASSETS);
            }),
            caches.open(API_CACHE).then(() => {
                console.log('🔌 Initializing API cache...');
            }),
            caches.open(IMAGE_CACHE).then(() => {
                console.log('🖼️ Initializing image cache...');
            })
        ]).then(() => {
            console.log('✅ Service Worker installed successfully');
            return self.skipWaiting();
        })
    );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
    console.log('🚀 Service Worker activating...');
    
    event.waitUntil(
        Promise.all([
            caches.keys().then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (!cacheName.startsWith(CACHE_VERSION)) {
                            console.log(`🗑️ Deleting old cache: ${cacheName}`);
                            return caches.delete(cacheName);
                        }
                    })
                );
            }),
            self.clients.claim()
        ]).then(() => {
            console.log('✅ Service Worker activated successfully');
        })
    );
});

// Fetch event - handle all network requests
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip non-HTTP requests
    if (!url.protocol.startsWith('http')) {
        return;
    }
    
    // Determine cache strategy based on request type
    if (isStaticAsset(request)) {
        event.respondWith(handleStaticAsset(request));
    } else if (isAPIRequest(request)) {
        event.respondWith(handleAPIRequest(request));
    } else if (isImageRequest(request)) {
        event.respondWith(handleImageRequest(request));
    } else {
        event.respondWith(handleDynamicRequest(request));
    }
});

// Static asset handler - cache first
async function handleStaticAsset(request) {
    try {
        const cache = await caches.open(STATIC_CACHE);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            console.log(`📦 Serving from cache: ${request.url}`);
            return cachedResponse;
        }
        
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
            console.log(`📥 Cached static asset: ${request.url}`);
        }
        
        return networkResponse;
    } catch (error) {
        console.error(`❌ Static asset fetch failed: ${request.url}`, error);
        return new Response('Offline - Asset not available', { status: 503 });
    }
}

// API request handler - network first with offline fallback
async function handleAPIRequest(request) {
    try {
        const cache = await caches.open(API_CACHE);
        
        // Try network first
        try {
            const networkResponse = await fetch(request.clone());
            
            if (networkResponse.ok) {
                cache.put(request, networkResponse.clone());
                console.log(`🔌 API response cached: ${request.url}`);
            }
            
            return networkResponse;
        } catch (networkError) {
            console.log(`📡 Network failed for API: ${request.url}, trying cache...`);
            
            const cachedResponse = await cache.match(request);
            
            if (cachedResponse) {
                console.log(`📦 Serving API from cache: ${request.url}`);
                return cachedResponse;
            }
            
            return createOfflineAPIResponse(request);
        }
    } catch (error) {
        console.error(`❌ API request handler failed: ${request.url}`, error);
        return createOfflineAPIResponse(request);
    }
}

// Image request handler - cache first
async function handleImageRequest(request) {
    try {
        const cache = await caches.open(IMAGE_CACHE);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            console.log(`🖼️ Serving image from cache: ${request.url}`);
            return cachedResponse;
        }
        
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
            console.log(`📸 Cached image: ${request.url}`);
        }
        
        return networkResponse;
    } catch (error) {
        console.error(`❌ Image fetch failed: ${request.url}`, error);
        return createPlaceholderImage();
    }
}

// Dynamic request handler - network first
async function handleDynamicRequest(request) {
    try {
        const cache = await caches.open(DYNAMIC_CACHE);
        
        try {
            const networkResponse = await fetch(request);
            
            if (networkResponse.ok) {
                cache.put(request, networkResponse.clone());
                console.log(`🌐 Cached dynamic content: ${request.url}`);
            }
            
            return networkResponse;
        } catch (networkError) {
            console.log(`📡 Network failed for dynamic content: ${request.url}, trying cache...`);
            
            const cachedResponse = await cache.match(request);
            
            if (cachedResponse) {
                console.log(`📦 Serving dynamic content from cache: ${request.url}`);
                return cachedResponse;
            }
            
            if (request.headers.get('Accept')?.includes('text/html')) {
                return createOfflinePage();
            }
            
            return new Response('Offline', { status: 503 });
        }
    } catch (error) {
        console.error(`❌ Dynamic request handler failed: ${request.url}`, error);
        return new Response('Request failed', { status: 500 });
    }
}

// Utility functions
function isStaticAsset(request) {
    const url = new URL(request.url);
    const pathname = url.pathname;
    
    return STATIC_ASSETS.some(asset => pathname.endsWith(asset)) ||
           pathname.endsWith('.css') ||
           pathname.endsWith('.js') ||
           pathname.endsWith('.json') ||
           pathname === '/' ||
           pathname === '/mobile-index.html';
}

function isAPIRequest(request) {
    const url = new URL(request.url);
    return url.pathname.startsWith('/api/') || 
           API_ENDPOINTS.some(endpoint => url.pathname.startsWith(endpoint));
}

function isImageRequest(request) {
    const url = new URL(request.url);
    const pathname = url.pathname;
    
    return pathname.endsWith('.png') ||
           pathname.endsWith('.jpg') ||
           pathname.endsWith('.jpeg') ||
           pathname.endsWith('.gif') ||
           pathname.endsWith('.svg') ||
           pathname.endsWith('.webp') ||
           pathname.startsWith('/icons/');
}

function createOfflineAPIResponse(request) {
    const url = new URL(request.url);
    
    if (url.pathname.includes('/workouts')) {
        return new Response(JSON.stringify({
            error: 'offline',
            message: 'Workouts will sync when online',
            cached_workouts: []
        }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });
    }
    
    if (url.pathname.includes('/family')) {
        return new Response(JSON.stringify({
            error: 'offline',
            message: 'Family data will sync when online',
            cached_family: []
        }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });
    }
    
    return new Response(JSON.stringify({
        error: 'offline',
        message: 'This feature requires an internet connection'
    }), {
        status: 503,
        headers: { 'Content-Type': 'application/json' }
    });
}

function createPlaceholderImage() {
    const placeholderSvg = `
        <svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="200" height="200" fill="#f3f4f6"/>
            <text x="100" y="100" text-anchor="middle" dy=".3em" fill="#9ca3af">
                📷 Image Offline
            </text>
        </svg>
    `;
    
    return new Response(placeholderSvg, {
        headers: { 'Content-Type': 'image/svg+xml' }
    });
}

function createOfflinePage() {
    const offlineHtml = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Khyrie - Offline</title>
            <link rel="stylesheet" href="/mobile-app.css">
        </head>
        <body>
            <div class="pwa-container">
                <main class="main-content offline-page">
                    <div class="mobile-card">
                        <div class="mobile-card-header">
                            <div class="mobile-card-icon">📶</div>
                            <div>
                                <h1 class="mobile-card-title">You're Offline</h1>
                                <p class="mobile-card-subtitle">Check your connection and try again</p>
                            </div>
                        </div>
                        
                        <div class="offline-actions">
                            <button class="mobile-btn mobile-btn-primary" onclick="window.location.reload()">
                                Try Again
                            </button>
                            
                            <button class="mobile-btn mobile-btn-secondary" onclick="history.back()">
                                Go Back
                            </button>
                        </div>
                    </div>
                </main>
            </div>
        </body>
        </html>
    `;
    
    return new Response(offlineHtml, {
        headers: { 'Content-Type': 'text/html' }
    });
}

// Push notification handler
self.addEventListener('push', (event) => {
    console.log('🔔 Push notification received:', event.data?.text());
    
    const data = event.data ? event.data.json() : {};
    const options = {
        body: data.body || 'New notification from Khyrie',
        icon: '/icons/khyrie-192.png',
        badge: '/icons/khyrie-72.png',
        vibrate: [200, 100, 200],
        data: data
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title || 'Khyrie Fitness', options)
    );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
    console.log('🔔 Notification clicked:', event.notification.data);
    
    event.notification.close();
    
    if (event.action === 'view') {
        event.waitUntil(
            clients.openWindow(event.notification.data?.url || '/')
        );
    }
});

// Background sync for offline actions
self.addEventListener('sync', (event) => {
    console.log('🔄 Background sync triggered:', event.tag);
    
    if (event.tag === 'workout-sync') {
        event.waitUntil(syncWorkoutData());
    } else if (event.tag === 'family-sync') {
        event.waitUntil(syncFamilyData());
    }
});

// Sync functions
async function syncWorkoutData() {
    try {
        console.log('🏋️ Syncing workout data...');
        
        const response = await fetch('/api/sync/workouts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'sync_offline_workouts' })
        });
        
        if (response.ok) {
            console.log('✅ Workout data synced successfully');
        }
    } catch (error) {
        console.error('❌ Workout sync failed:', error);
    }
}

async function syncFamilyData() {
    try {
        console.log('👨‍👩‍👧‍👦 Syncing family data...');
        
        const response = await fetch('/api/sync/family', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'sync_offline_family' })
        });
        
        if (response.ok) {
            console.log('✅ Family data synced successfully');
        }
    } catch (error) {
        console.error('❌ Family sync failed:', error);
    }
}

// Performance monitoring
console.log('🔧 Khyrie Service Worker initialized');
console.log(`📦 Cache version: ${CACHE_VERSION}`);
console.log(`🎯 Static assets to cache: ${STATIC_ASSETS.length}`);
console.log(`🔌 API endpoints to monitor: ${API_ENDPOINTS.length}`);