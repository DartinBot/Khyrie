/* FitFriendsClubs Wix Integration - BODY Section (Fixed)
 * Place this in: Site Code > Site tab (for site-wide) OR Page Code (for specific pages)
 * This is the main application logic
 */

// Wrap everything in a safe execution context
(function() {
    'use strict';
    
    // Wait for configuration to be available
    function waitForConfig() {
        return new Promise((resolve) => {
            if (window.FitFriendsConfig) {
                resolve();
            } else {
                // Set default config if not loaded
                window.FitFriendsConfig = {
                    API_URL: 'https://fitfriendsclub-api.darnellroy2.workers.dev',
                    DEBUG_MODE: true,
                    AUTO_LOAD: true,
                    RETRY_ATTEMPTS: 3,
                    TIMEOUT: 10000,
                    FEATURES: {
                        CLUBS: true,
                        TRAILS: true,
                        DASHBOARD: true,
                        LIGHTBOXES: true,
                        AUTO_REFRESH: false
                    }
                };
                console.warn('⚠️ Using default FitFriends configuration');
                resolve();
            }
        });
    }

    // API Class with Safety Checks
    class FitFriendsAPI {
        constructor() {
            this.baseUrl = window.FitFriendsConfig?.API_URL || 'https://fitfriendsclub-api.darnellroy2.workers.dev';
            this.retryAttempts = window.FitFriendsConfig?.RETRY_ATTEMPTS || 3;
            this.timeout = window.FitFriendsConfig?.TIMEOUT || 10000;
        }

        async apiCall(endpoint, options = {}) {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), this.timeout);
            
            try {
                if (window.FitFriendsConfig?.DEBUG_MODE) {
                    console.log(`🔗 API Call: ${this.baseUrl}${endpoint}`);
                }
                
                const response = await fetch(`${this.baseUrl}${endpoint}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        ...options.headers
                    },
                    signal: controller.signal,
                    ...options
                });

                clearTimeout(timeoutId);

                if (!response.ok) {
                    throw new Error(`API call failed: ${response.status} ${response.statusText}`);
                }

                return await response.json();
            } catch (error) {
                clearTimeout(timeoutId);
                console.error('❌ API Error:', error);
                throw error;
            }
        }

        async healthCheck() {
            return await this.apiCall('/');
        }

        async getFitnessClubs() {
            return await this.apiCall('/test/clubs');
        }

        async getVirtualTrails() {
            return await this.apiCall('/test/trails');
        }

        async runAllTests() {
            return await this.apiCall('/test/all');
        }
    }

    // Initialize API
    let fitFriendsAPI;

    // Core Site Functions with Safety
    async function initializeFitFriendsClubs() {
        try {
            console.log('🚀 Initializing FitFriendsClubs...');
            
            // Initialize API if not already done
            if (!fitFriendsAPI) {
                fitFriendsAPI = new FitFriendsAPI();
            }
            
            // Show loading state (check if function exists)
            if (typeof showGlobalLoading === 'function') {
                showGlobalLoading();
            }
            
            // Test API connection
            const healthCheck = await fitFriendsAPI.healthCheck();
            console.log('✅ API Health Check:', healthCheck);
            
            // Update global status (check if function exists)
            if (typeof updateGlobalStatus === 'function') {
                if (healthCheck.status === 'success') {
                    updateGlobalStatus('online', 'API Connected ✅');
                }
            }
            
            // Hide loading state
            if (typeof hideGlobalLoading === 'function') {
                hideGlobalLoading();
            }
            
            return true;
        } catch (error) {
            console.error('❌ Initialization failed:', error);
            
            if (typeof updateGlobalStatus === 'function') {
                updateGlobalStatus('offline', 'API Connection Failed ❌');
            }
            if (typeof hideGlobalLoading === 'function') {
                hideGlobalLoading();
            }
            
            return false;
        }
    }

    // Navigation Setup with Safety
    function setupFitFriendsNavigation() {
        try {
            const navButtons = {
                '#homeButton': '/',
                '#clubsButton': '/clubs',
                '#trailsButton': '/trails',
                '#dashboardButton': '/dashboard'
            };
            
            Object.entries(navButtons).forEach(([selector, path]) => {
                try {
                    if ($w(selector)) {
                        $w(selector).onClick(() => {
                            wixLocation.to(path);
                        });
                    }
                } catch(e) {
                    console.warn(`Navigation button ${selector} not found:`, e);
                }
            });
            
            // Test API button
            try {
                if ($w('#testApiButton')) {
                    $w('#testApiButton').onClick(runAPITest);
                }
            } catch(e) {
                console.warn('Test API button not found:', e);
            }
        } catch (error) {
            console.error('❌ Navigation setup failed:', error);
        }
    }

    // API Test Function with Safety
    async function runAPITest() {
        try {
            if (typeof showLoading === 'function') {
                showLoading('#testResults');
            }
            
            const results = await fitFriendsAPI.runAllTests();
            
            try {
                if ($w('#testResults')) {
                    $w('#testResults').text = `✅ ${results.message}`;
                    $w('#testResults').style.color = '#4CAF50';
                }
            } catch(e) {
                console.warn('Test results element not found');
            }
            
            console.log('🧪 API Test Results:', results);
        } catch (error) {
            try {
                if ($w('#testResults')) {
                    $w('#testResults').text = `❌ Test Failed: ${error.message}`;
                    $w('#testResults').style.color = '#F44336';
                }
            } catch(e) {
                console.warn('Test results element not found');
            }
            console.error('❌ API Test failed:', error);
        } finally {
            if (typeof hideLoading === 'function') {
                hideLoading('#testResults');
            }
        }
    }

    // Data Loading Functions with Safety
    async function loadFitnessClubs() {
        if (!window.FitFriendsConfig?.FEATURES?.CLUBS) return;
        
        try {
            console.log('🏃‍♀️ Loading fitness clubs...');
            
            if (typeof showLoading === 'function') {
                showLoading('#clubsContainer');
            }
            
            const response = await fitFriendsAPI.getFitnessClubs();
            
            if (response.status === 'success' && response.data?.clubs) {
                displayFitnessClubs(response.data.clubs);
                if (typeof updateClubCount === 'function') {
                    updateClubCount(response.data.clubs.length);
                }
            } else {
                if (typeof showError === 'function') {
                    showError('Failed to load fitness clubs');
                }
            }
        } catch (error) {
            console.error('❌ Failed to load clubs:', error);
            if (typeof showError === 'function') {
                showError('Error loading fitness clubs');
            }
        } finally {
            if (typeof hideLoading === 'function') {
                hideLoading('#clubsContainer');
            }
        }
    }

    async function loadVirtualTrails() {
        if (!window.FitFriendsConfig?.FEATURES?.TRAILS) return;
        
        try {
            console.log('🗺️ Loading virtual trails...');
            
            if (typeof showLoading === 'function') {
                showLoading('#trailsContainer');
            }
            
            const response = await fitFriendsAPI.getVirtualTrails();
            
            if (response.status === 'success' && response.data?.trails) {
                displayVirtualTrails(response.data.trails);
                if (typeof updateTrailCount === 'function') {
                    updateTrailCount(response.data.trails.length);
                }
            } else {
                if (typeof showError === 'function') {
                    showError('Failed to load virtual trails');
                }
            }
        } catch (error) {
            console.error('❌ Failed to load trails:', error);
            if (typeof showError === 'function') {
                showError('Error loading virtual trails');
            }
        } finally {
            if (typeof hideLoading === 'function') {
                hideLoading('#trailsContainer');
            }
        }
    }

    async function loadDashboardData() {
        if (!window.FitFriendsConfig?.FEATURES?.DASHBOARD) return;
        
        try {
            console.log('📊 Loading dashboard...');
            
            if (typeof showLoading === 'function') {
                showLoading('#dashboardContainer');
            }
            
            const testResults = await fitFriendsAPI.runAllTests();
            
            try {
                if ($w('#dashboardRepeater')) {
                    displayDashboardData(testResults);
                }
            } catch(e) {
                console.warn('Dashboard repeater not found');
            }
        } catch (error) {
            console.error('❌ Failed to load dashboard:', error);
            if (typeof showError === 'function') {
                showError('Failed to load dashboard data');
            }
        } finally {
            if (typeof hideLoading === 'function') {
                hideLoading('#dashboardContainer');
            }
        }
    }

    // Display Functions with Safety
    function displayFitnessClubs(clubs) {
        try {
            if (!$w('#clubsRepeater')) {
                console.warn('Clubs repeater not found');
                return;
            }
            
            const clubData = clubs.map((club, index) => ({
                _id: club.id || `club-${index}`,
                clubName: club.name || 'Unknown Club',
                clubCategory: club.category || 'General',
                equipmentType: club.equipment_type || 'Mixed Equipment',
                description: club.description || 'Premium fitness club'
            }));
            
            $w('#clubsRepeater').data = clubData;
            
            $w('#clubsRepeater').onItemReady(($item, itemData) => {
                try {
                    const textElements = {
                        '#clubNameText': itemData.clubName,
                        '#clubCategoryText': itemData.clubCategory,
                        '#equipmentTypeText': `Equipment: ${itemData.equipmentType}`
                    };
                    
                    Object.entries(textElements).forEach(([selector, text]) => {
                        try {
                            if ($item(selector)) {
                                $item(selector).text = text;
                            }
                        } catch(e) {
                            console.warn(`Club element ${selector} not found`);
                        }
                    });
                    
                    // Add click handler
                    try {
                        if ($item('#clubContainer')) {
                            $item('#clubContainer').onClick(() => {
                                if (typeof showClubDetails === 'function') {
                                    showClubDetails(itemData);
                                }
                            });
                        }
                    } catch(e) {
                        console.warn('Club container click handler failed');
                    }
                } catch(e) {
                    console.warn('Club item setup failed:', e);
                }
            });
            
            console.log(`✅ Displayed ${clubs.length} fitness clubs`);
        } catch (error) {
            console.error('❌ Display clubs failed:', error);
        }
    }

    function displayVirtualTrails(trails) {
        try {
            if (!$w('#trailsRepeater')) {
                console.warn('Trails repeater not found');
                return;
            }
            
            const trailData = trails.map((trail, index) => ({
                _id: trail.id || `trail-${index}`,
                trailName: trail.name || 'Unknown Trail',
                location: trail.location || 'Unknown Location',
                difficulty: trail.difficulty || 'Moderate',
                distance: trail.distance_km ? `${trail.distance_km}km` : 'Distance TBD',
                description: trail.description || 'Scenic virtual trail'
            }));
            
            $w('#trailsRepeater').data = trailData;
            
            $w('#trailsRepeater').onItemReady(($item, itemData) => {
                try {
                    const textElements = {
                        '#trailNameText': itemData.trailName,
                        '#locationText': itemData.location,
                        '#difficultyText': `Difficulty: ${itemData.difficulty}`,
                        '#distanceText': itemData.distance
                    };
                    
                    Object.entries(textElements).forEach(([selector, text]) => {
                        try {
                            if ($item(selector)) {
                                $item(selector).text = text;
                            }
                        } catch(e) {
                            console.warn(`Trail element ${selector} not found`);
                        }
                    });
                    
                    // Add click handler
                    try {
                        if ($item('#trailContainer')) {
                            $item('#trailContainer').onClick(() => {
                                if (typeof showTrailDetails === 'function') {
                                    showTrailDetails(itemData);
                                }
                            });
                        }
                    } catch(e) {
                        console.warn('Trail container click handler failed');
                    }
                } catch(e) {
                    console.warn('Trail item setup failed:', e);
                }
            });
            
            console.log(`✅ Displayed ${trails.length} virtual trails`);
        } catch (error) {
            console.error('❌ Display trails failed:', error);
        }
    }

    function displayDashboardData(testResults) {
        try {
            if (!$w('#dashboardRepeater')) {
                console.warn('Dashboard repeater not found');
                return;
            }
            
            const dashboardItems = testResults.results.map((test, index) => ({
                _id: `test-${index}`,
                testName: test.name,
                status: test.status,
                message: test.message,
                responseTime: test.responseTime || 'N/A',
                dataCount: test.dataCount || 0
            }));
            
            $w('#dashboardRepeater').data = dashboardItems;
            
            $w('#dashboardRepeater').onItemReady(($item, itemData) => {
                try {
                    if ($item('#testNameText')) {
                        $item('#testNameText').text = itemData.testName;
                    }
                    
                    if ($item('#statusText')) {
                        $item('#statusText').text = itemData.status.toUpperCase();
                        
                        const statusColors = {
                            'success': '#4CAF50',
                            'error': '#F44336',
                            'warning': '#FF9800'
                        };
                        
                        $item('#statusText').style.color = statusColors[itemData.status] || '#757575';
                    }
                    
                    if ($item('#messageText')) {
                        $item('#messageText').text = itemData.message;
                    }
                    
                    if ($item('#responseTimeText')) {
                        $item('#responseTimeText').text = `${itemData.responseTime}ms`;
                    }
                } catch(e) {
                    console.warn('Dashboard item setup failed:', e);
                }
            });
            
            console.log(`✅ Dashboard loaded with ${dashboardItems.length} items`);
        } catch (error) {
            console.error('❌ Display dashboard failed:', error);
        }
    }

    // Page-Specific Loading with Safety
    function loadPageData() {
        try {
            const currentPage = wixLocation.path;
            
            const pageLoaders = {
                '/clubs': loadFitnessClubs,
                '/trails': loadVirtualTrails,
                '/dashboard': loadDashboardData
            };
            
            const loader = pageLoaders[currentPage];
            if (loader) {
                loader();
            }
            
            // Load dashboard stats for homepage
            if (currentPage === '/' || currentPage === '') {
                loadHomepageStats();
            }
        } catch (error) {
            console.error('❌ Load page data failed:', error);
        }
    }

    async function loadHomepageStats() {
        try {
            const testResults = await fitFriendsAPI.runAllTests();
            
            if (testResults.status === 'success') {
                const clubsTest = testResults.results.find(test => test.name === 'Fitness Clubs');
                const trailsTest = testResults.results.find(test => test.name === 'Virtual Trails');
                
                try {
                    if ($w('#clubCountText') && clubsTest?.dataCount !== undefined) {
                        $w('#clubCountText').text = `${clubsTest.dataCount} Premium Clubs`;
                    }
                    
                    if ($w('#trailCountText') && trailsTest?.dataCount !== undefined) {
                        $w('#trailCountText').text = `${trailsTest.dataCount} Virtual Trails`;
                    }
                    
                    if ($w('#platformStatusText')) {
                        const allWorking = testResults.results.every(test => test.status === 'success');
                        $w('#platformStatusText').text = allWorking ? 'All Systems Operational' : 'System Issues Detected';
                    }
                } catch(e) {
                    console.warn('Homepage stats elements not found');
                }
            }
        } catch (error) {
            console.error('❌ Failed to load homepage stats:', error);
        }
    }

    // Main Wix Integration Point with Full Safety
    function initializeWixIntegration() {
        $w.onReady(async function () {
            try {
                console.log('✅ FitFriendsClubs Wix page loaded!');
                
                // Wait for configuration
                await waitForConfig();
                
                // Initialize the application
                const initialized = await initializeFitFriendsClubs();
                
                if (initialized) {
                    // Setup navigation
                    setupFitFriendsNavigation();
                    
                    // Load page-specific data
                    if (window.FitFriendsConfig?.AUTO_LOAD) {
                        loadPageData();
                    }
                }
                
                // Export for testing (in debug mode)
                if (window.FitFriendsConfig?.DEBUG_MODE) {
                    window.FitFriendsClubs = {
                        api: fitFriendsAPI,
                        loadClubs: loadFitnessClubs,
                        loadTrails: loadVirtualTrails,
                        loadDashboard: loadDashboardData,
                        test: runAPITest
                    };
                }
                
            } catch (error) {
                console.error('❌ FitFriendsClubs initialization error:', error);
                if (typeof updateGlobalStatus === 'function') {
                    updateGlobalStatus('error', 'Initialization Failed');
                }
            }
        });
    }

    // Initialize when ready
    if (typeof $w !== 'undefined') {
        initializeWixIntegration();
    } else {
        console.warn('⚠️ Wix $w not available, deferring initialization');
        window.addEventListener('load', () => {
            setTimeout(initializeWixIntegration, 1000);
        });
    }

})();

console.log('✅ FitFriendsClubs Body Section Loaded Safely');