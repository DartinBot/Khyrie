/* FitFriendsClubs Wix Integration - BODY Section
 * Place this in: Page Code (for each page) OR Site Code > Site tab
 * This is the main application logic
 */

// API Class and Core Functions
class FitFriendsAPI {
    constructor() {
        this.baseUrl = window.FitFriendsConfig.API_URL;
        this.retryAttempts = window.FitFriendsConfig.RETRY_ATTEMPTS;
        this.timeout = window.FitFriendsConfig.TIMEOUT;
    }

    async apiCall(endpoint, options = {}) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        
        try {
            if (window.FitFriendsConfig.DEBUG_MODE) {
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
const fitFriendsAPI = new FitFriendsAPI();

// Core Site Functions
async function initializeFitFriendsClubs() {
    try {
        console.log('🚀 Initializing FitFriendsClubs...');
        
        // Show loading state
        showGlobalLoading();
        
        // Test API connection
        const healthCheck = await fitFriendsAPI.healthCheck();
        console.log('✅ API Health Check:', healthCheck);
        
        // Update global status
        if (healthCheck.status === 'success') {
            updateGlobalStatus('online', 'API Connected ✅');
        }
        
        // Hide loading state
        hideGlobalLoading();
        
        return true;
    } catch (error) {
        console.error('❌ Initialization failed:', error);
        updateGlobalStatus('offline', 'API Connection Failed ❌');
        hideGlobalLoading();
        return false;
    }
}

// Navigation Setup
function setupFitFriendsNavigation() {
    // Navigation buttons with error handling
    const navButtons = {
        '#homeButton': '/',
        '#clubsButton': '/clubs',
        '#trailsButton': '/trails',
        '#dashboardButton': '/dashboard'
    };
    
    Object.entries(navButtons).forEach(([selector, path]) => {
        if ($w(selector)) {
            $w(selector).onClick(() => {
                wixLocation.to(path);
            });
        }
    });
    
    // Test API button
    if ($w('#testApiButton')) {
        $w('#testApiButton').onClick(runAPITest);
    }
}

// API Test Function
async function runAPITest() {
    try {
        showLoading('#testResults');
        const results = await fitFriendsAPI.runAllTests();
        
        if ($w('#testResults')) {
            $w('#testResults').text = `✅ ${results.message}`;
            $w('#testResults').style.color = '#4CAF50';
        }
        
        console.log('🧪 API Test Results:', results);
    } catch (error) {
        if ($w('#testResults')) {
            $w('#testResults').text = `❌ Test Failed: ${error.message}`;
            $w('#testResults').style.color = '#F44336';
        }
        console.error('❌ API Test failed:', error);
    } finally {
        hideLoading('#testResults');
    }
}

// Data Loading Functions
async function loadFitnessClubs() {
    if (!window.FitFriendsConfig.FEATURES.CLUBS) return;
    
    try {
        console.log('🏃‍♀️ Loading fitness clubs...');
        showLoading('#clubsContainer');
        
        const response = await fitFriendsAPI.getFitnessClubs();
        
        if (response.status === 'success' && response.data?.clubs) {
            displayFitnessClubs(response.data.clubs);
            updateClubCount(response.data.clubs.length);
        } else {
            showError('Failed to load fitness clubs');
        }
    } catch (error) {
        console.error('❌ Failed to load clubs:', error);
        showError('Error loading fitness clubs');
    } finally {
        hideLoading('#clubsContainer');
    }
}

async function loadVirtualTrails() {
    if (!window.FitFriendsConfig.FEATURES.TRAILS) return;
    
    try {
        console.log('🗺️ Loading virtual trails...');
        showLoading('#trailsContainer');
        
        const response = await fitFriendsAPI.getVirtualTrails();
        
        if (response.status === 'success' && response.data?.trails) {
            displayVirtualTrails(response.data.trails);
            updateTrailCount(response.data.trails.length);
        } else {
            showError('Failed to load virtual trails');
        }
    } catch (error) {
        console.error('❌ Failed to load trails:', error);
        showError('Error loading virtual trails');
    } finally {
        hideLoading('#trailsContainer');
    }
}

async function loadDashboardData() {
    if (!window.FitFriendsConfig.FEATURES.DASHBOARD) return;
    
    try {
        console.log('📊 Loading dashboard...');
        showLoading('#dashboardContainer');
        
        const testResults = await fitFriendsAPI.runAllTests();
        
        if ($w('#dashboardRepeater')) {
            displayDashboardData(testResults);
        }
    } catch (error) {
        console.error('❌ Failed to load dashboard:', error);
        showError('Failed to load dashboard data');
    } finally {
        hideLoading('#dashboardContainer');
    }
}

// Display Functions
function displayFitnessClubs(clubs) {
    if (!$w('#clubsRepeater')) return;
    
    const clubData = clubs.map((club, index) => ({
        _id: club.id || `club-${index}`,
        clubName: club.name || 'Unknown Club',
        clubCategory: club.category || 'General',
        equipmentType: club.equipment_type || 'Mixed Equipment',
        description: club.description || 'Premium fitness club'
    }));
    
    $w('#clubsRepeater').data = clubData;
    
    $w('#clubsRepeater').onItemReady(($item, itemData) => {
        // Set text elements with safety checks
        const textElements = {
            '#clubNameText': itemData.clubName,
            '#clubCategoryText': itemData.clubCategory,
            '#equipmentTypeText': `Equipment: ${itemData.equipmentType}`
        };
        
        Object.entries(textElements).forEach(([selector, text]) => {
            if ($item(selector)) {
                $item(selector).text = text;
            }
        });
        
        // Add click handler
        if ($item('#clubContainer')) {
            $item('#clubContainer').onClick(() => showClubDetails(itemData));
        }
    });
    
    console.log(`✅ Displayed ${clubs.length} fitness clubs`);
}

function displayVirtualTrails(trails) {
    if (!$w('#trailsRepeater')) return;
    
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
        const textElements = {
            '#trailNameText': itemData.trailName,
            '#locationText': itemData.location,
            '#difficultyText': `Difficulty: ${itemData.difficulty}`,
            '#distanceText': itemData.distance
        };
        
        Object.entries(textElements).forEach(([selector, text]) => {
            if ($item(selector)) {
                $item(selector).text = text;
            }
        });
        
        // Add difficulty badge styling
        if ($item('#difficultyText')) {
            const difficultyClass = `fitfriends-difficulty-${itemData.difficulty.toLowerCase()}`;
            $item('#difficultyText').addClass(difficultyClass);
        }
        
        if ($item('#trailContainer')) {
            $item('#trailContainer').onClick(() => showTrailDetails(itemData));
        }
    });
    
    console.log(`✅ Displayed ${trails.length} virtual trails`);
}

function displayDashboardData(testResults) {
    if (!$w('#dashboardRepeater')) return;
    
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
        if ($item('#testNameText')) {
            $item('#testNameText').text = itemData.testName;
        }
        
        if ($item('#statusText')) {
            $item('#statusText').text = itemData.status.toUpperCase();
            
            // Status color coding
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
    });
}

// Page-Specific Loading
function loadPageData() {
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
}

async function loadHomepageStats() {
    try {
        const testResults = await fitFriendsAPI.runAllTests();
        
        if (testResults.status === 'success') {
            const clubsTest = testResults.results.find(test => test.name === 'Fitness Clubs');
            const trailsTest = testResults.results.find(test => test.name === 'Virtual Trails');
            
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
        }
    } catch (error) {
        console.error('❌ Failed to load homepage stats:', error);
    }
}

// Main Wix Integration Point
$w.onReady(async function () {
    console.log('✅ FitFriendsClubs Wix page loaded!');
    
    try {
        // Initialize the application
        const initialized = await initializeFitFriendsClubs();
        
        if (initialized) {
            // Setup navigation
            setupFitFriendsNavigation();
            
            // Load page-specific data
            if (window.FitFriendsConfig.AUTO_LOAD) {
                loadPageData();
            }
        }
    } catch (error) {
        console.error('❌ FitFriendsClubs initialization error:', error);
        updateGlobalStatus('error', 'Initialization Failed');
    }
});

// Export for testing
if (window.FitFriendsConfig.DEBUG_MODE) {
    window.FitFriendsClubs = {
        api: fitFriendsAPI,
        loadClubs: loadFitnessClubs,
        loadTrails: loadVirtualTrails,
        loadDashboard: loadDashboardData,
        test: runAPITest
    };
}