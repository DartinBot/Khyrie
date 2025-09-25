// Khyrie PWA Service Worker
// Copyright (C) 2025 Darnell Roy

const CACHE_NAME = 'khyrie-fitness-v1';
const API_CACHE_NAME = 'khyrie-api-v1';

// Static files to cache for offline use
const urlsToCache = [
  '/',
  '/static/css/AIDashboard.css',
  '/static/js/AIDashboard.js', 
  '/static/css/ExerciseJournal.css',
  '/static/js/ExerciseJournal.js',
  '/static/css/FamilyFriends.css',
  '/static/js/FamilyFriends.js',
  '/static/css/WeightTracker.css',
  '/static/js/WeightTracker.js',
  '/static/css/SharedWorkout.css',
  '/static/js/SharedWorkout.js',
  '/manifest.json',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

// API endpoints to cache for offline functionality
const apiEndpoints = [
  '/health',
  '/exercises/basic',
  '/workouts/templates',
  '/family/groups'
];

// Install event - cache static resources
self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Install');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[ServiceWorker] Caching app shell');
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        console.log('[ServiceWorker] Skip waiting');
        return self.skipWaiting();
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[ServiceWorker] Activate');
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME && key !== API_CACHE_NAME) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    }).then(() => {
      console.log('[ServiceWorker] Claiming clients');
      return self.clients.claim();
    })
  );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);
  
  // Handle API requests
  if (requestUrl.pathname.startsWith('/api/')) {
    event.respondWith(
      caches.open(API_CACHE_NAME).then((cache) => {
        return fetch(event.request).then((response) => {
          // Cache successful API responses
          if (response.status === 200) {
            cache.put(event.request, response.clone());
          }
          return response;
        }).catch(() => {
          // Return cached API response if network fails
          return cache.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
              console.log('[ServiceWorker] Serving cached API response', event.request.url);
              return cachedResponse;
            }
            // Return offline fallback for API
            return new Response(JSON.stringify({
              error: 'Offline',
              message: 'This feature requires an internet connection',
              cached: false
            }), {
              status: 503,
              headers: { 'Content-Type': 'application/json' }
            });
          });
        });
      })
    );
    return;
  }

  // Handle static resources
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        if (response) {
          console.log('[ServiceWorker] Serving cached resource', event.request.url);
          return response;
        }

        return fetch(event.request).then((response) => {
          // Don't cache non-successful responses
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Clone the response for caching
          const responseToCache = response.clone();
          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseToCache);
            });

          return response;
        }).catch(() => {
          // Return offline page for navigation requests
          if (event.request.mode === 'navigate') {
            return caches.match('/').then((cachedResponse) => {
              return cachedResponse || new Response('Offline - Please check your connection', {
                status: 503,
                headers: { 'Content-Type': 'text/html' }
              });
            });
          }
        });
      })
  );
});

// Background sync for workout data
self.addEventListener('sync', (event) => {
  console.log('[ServiceWorker] Background sync', event.tag);
  
  if (event.tag === 'sync-workouts') {
    event.waitUntil(
      syncWorkoutData()
    );
  }
});

// Push notifications for workout reminders
self.addEventListener('push', (event) => {
  console.log('[ServiceWorker] Push received', event);
  
  const options = {
    body: event.data ? event.data.text() : 'Time for your Khyrie workout!',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    tag: 'workout-reminder',
    requireInteraction: true,
    actions: [
      {
        action: 'start-workout',
        title: 'Start Workout',
        icon: '/icons/start-workout.png'
      },
      {
        action: 'snooze',
        title: 'Remind Later', 
        icon: '/icons/snooze.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('Khyrie Fitness', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  console.log('[ServiceWorker] Notification click', event);
  
  event.notification.close();

  if (event.action === 'start-workout') {
    event.waitUntil(
      clients.openWindow('/workout')
    );
  } else if (event.action === 'snooze') {
    // Schedule another notification in 30 minutes
    console.log('[ServiceWorker] Workout snoozed');
  } else {
    // Default action - open app
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Sync workout data when connection is restored
async function syncWorkoutData() {
  try {
    // Get pending workouts from IndexedDB
    const pendingWorkouts = await getPendingWorkouts();
    
    for (const workout of pendingWorkouts) {
      try {
        const response = await fetch('/api/workouts', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(workout)
        });
        
        if (response.ok) {
          await removePendingWorkout(workout.id);
          console.log('[ServiceWorker] Synced workout', workout.id);
        }
      } catch (error) {
        console.log('[ServiceWorker] Failed to sync workout', workout.id, error);
      }
    }
  } catch (error) {
    console.log('[ServiceWorker] Sync failed', error);
  }
}

// Helper functions for offline data management
async function getPendingWorkouts() {
  // Implementation would use IndexedDB to store offline workout data
  return [];
}

async function removePendingWorkout(workoutId) {
  // Implementation would remove synced workout from IndexedDB
  console.log('Removing synced workout', workoutId);
}