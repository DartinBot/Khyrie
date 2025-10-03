// FitFriendsClubs Complete Wix Integration - Single File Version
// Copy this entire code into Wix Custom Code section

console.log('🏋️ FitFriendsClubs Integration Loading...');

// API Configuration
const FITFRIENDS_API_URL = 'https://fitfriendsclub-api.darnellroy2.workers.dev';

// Main API Class
class FitFriendsAPI {
    constructor() {
        this.baseUrl = FITFRIENDS_API_URL;
    }

    async apiCall(endpoint, options = {}) {
        try {
            console.log(`🔗 API Call: ${this.baseUrl}${endpoint}`);
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`API call failed: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
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

// Main Wix Integration
$w.onReady(function () {
    console.log('✅ FitFriendsClubs Wix site loaded!');
    
    // Initialize the site
    initializeSite();
    
    // Setup navigation
    setupNavigation();
    
    // Load data based on current page
    loadPageData();
});

// Initialize site
async function initializeSite() {
    try {
        console.log('🚀 Initializing FitFriendsClubs site...');
        
        // Show loading if element exists
        showLoading('#homePageContent');
        
        // Test API connection
        const healthCheck = await fitFriendsAPI.healthCheck();
        console.log('✅ API Health Check:', healthCheck);
        
        // Update status indicator
        if (healthCheck.status === 'success') {
            updateStatusIndicator('online', 'API Connected ✅');
        }
        
        // Hide loading
        hideLoading('#homePageContent');
        
        // Load initial dashboard stats
        loadDashboardStats();
        
    } catch (error) {
        console.error('❌ Site initialization failed:', error);
        updateStatusIndicator('offline', 'API Connection Failed ❌');
        hideLoading('#homePageContent');
    }
}

// Setup navigation buttons
function setupNavigation() {
    // Home button
    if ($w('#homeButton')) {
        $w('#homeButton').onClick(() => {
            wixLocation.to('/');
        });
    }
    
    // Clubs button
    if ($w('#clubsButton')) {
        $w('#clubsButton').onClick(() => {
            wixLocation.to('/clubs');
        });
    }
    
    // Trails button
    if ($w('#trailsButton')) {
        $w('#trailsButton').onClick(() => {
            wixLocation.to('/trails');
        });
    }
    
    // Dashboard button
    if ($w('#dashboardButton')) {
        $w('#dashboardButton').onClick(() => {
            wixLocation.to('/dashboard');
        });
    }

    // Test API button (for debugging)
    if ($w('#testApiButton')) {
        $w('#testApiButton').onClick(async () => {
            try {
                const results = await fitFriendsAPI.runAllTests();
                console.log('🧪 API Test Results:', results);
                
                if ($w('#testResults')) {
                    $w('#testResults').text = results.message;
                }
            } catch (error) {
                console.error('❌ API Test failed:', error);
                if ($w('#testResults')) {
                    $w('#testResults').text = 'API Test Failed ❌';
                }
            }
        });
    }
}

// Load data based on current page
function loadPageData() {
    const currentPage = wixLocation.path;
    
    switch (currentPage) {
        case '/clubs':
            loadFitnessClubs();
            break;
        case '/trails':
            loadVirtualTrails();
            break;
        case '/dashboard':
            loadUserDashboard();
            break;
        default:
            // Homepage - already initialized
            break;
    }
}

// Load fitness clubs
async function loadFitnessClubs() {
    try {
        console.log('🏃‍♀️ Loading fitness clubs...');
        showLoading('#clubsContainer');
        
        const response = await fitFriendsAPI.getFitnessClubs();
        
        if (response.status === 'success' && response.data && response.data.clubs) {
            displayFitnessClubs(response.data.clubs);
            updateClubCount(response.data.clubs.length);
        } else {
            showError('#clubsContainer', 'Failed to load fitness clubs');
        }
        
        hideLoading('#clubsContainer');
    } catch (error) {
        console.error('❌ Failed to load clubs:', error);
        showError('#clubsContainer', 'Error loading fitness clubs');
        hideLoading('#clubsContainer');
    }
}

// Load virtual trails
async function loadVirtualTrails() {
    try {
        console.log('🗺️ Loading virtual trails...');
        showLoading('#trailsContainer');
        
        const response = await fitFriendsAPI.getVirtualTrails();
        
        if (response.status === 'success' && response.data && response.data.trails) {
            displayVirtualTrails(response.data.trails);
            updateTrailCount(response.data.trails.length);
        } else {
            showError('#trailsContainer', 'Failed to load virtual trails');
        }
        
        hideLoading('#trailsContainer');
    } catch (error) {
        console.error('❌ Failed to load trails:', error);
        showError('#trailsContainer', 'Error loading virtual trails');
        hideLoading('#trailsContainer');
    }
}

// Display fitness clubs in repeater
function displayFitnessClubs(clubs) {
    if ($w('#clubsRepeater')) {
        const clubData = clubs.map((club, index) => ({
            _id: club.id || `club-${index}`,
            clubName: club.name || 'Unknown Club',
            clubCategory: club.category || 'General',
            equipmentType: club.equipment_type || 'Mixed Equipment',
            description: club.description || 'Premium fitness club with modern equipment'
        }));
        
        $w('#clubsRepeater').data = clubData;
        
        $w('#clubsRepeater').onItemReady(($item, itemData) => {
            // Set club name
            if ($item('#clubNameText')) {
                $item('#clubNameText').text = itemData.clubName;
            }
            
            // Set category
            if ($item('#clubCategoryText')) {
                $item('#clubCategoryText').text = itemData.clubCategory;
            }
            
            // Set equipment type
            if ($item('#equipmentTypeText')) {
                $item('#equipmentTypeText').text = `Equipment: ${itemData.equipmentType}`;
            }
            
            // Add click handler for details
            if ($item('#clubContainer')) {
                $item('#clubContainer').onClick(() => {
                    showClubDetails(itemData);
                });
            }
        });
        
        console.log(`✅ Displayed ${clubs.length} fitness clubs`);
    }
}

// Display virtual trails in repeater
function displayVirtualTrails(trails) {
    if ($w('#trailsRepeater')) {
        const trailData = trails.map((trail, index) => ({
            _id: trail.id || `trail-${index}`,
            trailName: trail.name || 'Unknown Trail',
            location: trail.location || 'Unknown Location',
            difficulty: trail.difficulty || 'Moderate',
            distance: trail.distance_km ? `${trail.distance_km}km` : 'Distance TBD',
            description: trail.description || 'Scenic virtual trail experience'
        }));
        
        $w('#trailsRepeater').data = trailData;
        
        $w('#trailsRepeater').onItemReady(($item, itemData) => {
            // Set trail name
            if ($item('#trailNameText')) {
                $item('#trailNameText').text = itemData.trailName;
            }
            
            // Set location
            if ($item('#locationText')) {
                $item('#locationText').text = itemData.location;
            }
            
            // Set difficulty
            if ($item('#difficultyText')) {
                $item('#difficultyText').text = `Difficulty: ${itemData.difficulty}`;
            }
            
            // Set distance
            if ($item('#distanceText')) {
                $item('#distanceText').text = itemData.distance;
            }
            
            // Add click handler for details
            if ($item('#trailContainer')) {
                $item('#trailContainer').onClick(() => {
                    showTrailDetails(itemData);
                });
            }
        });
        
        console.log(`✅ Displayed ${trails.length} virtual trails`);
    }
}

// Load dashboard stats
async function loadDashboardStats() {
    try {
        const testResults = await fitFriendsAPI.runAllTests();
        
        if (testResults.status === 'success') {
            // Find clubs and trails counts
            const clubsTest = testResults.results.find(test => test.name === 'Fitness Clubs');
            const trailsTest = testResults.results.find(test => test.name === 'Virtual Trails');
            
            // Update counts on homepage
            if ($w('#clubCountText') && clubsTest && clubsTest.dataCount !== undefined) {
                $w('#clubCountText').text = `${clubsTest.dataCount} Premium Clubs`;
            }
            
            if ($w('#trailCountText') && trailsTest && trailsTest.dataCount !== undefined) {
                $w('#trailCountText').text = `${trailsTest.dataCount} Virtual Trails`;
            }
            
            if ($w('#platformStatusText')) {
                const allWorking = testResults.results.every(test => test.status === 'success');
                $w('#platformStatusText').text = allWorking ? 'All Systems Operational' : 'Some Issues Detected';
            }
        }
    } catch (error) {
        console.error('❌ Failed to load dashboard stats:', error);
    }
}

// Load user dashboard
async function loadUserDashboard() {
    try {
        console.log('📊 Loading user dashboard...');
        showLoading('#dashboardContainer');
        
        const testResults = await fitFriendsAPI.runAllTests();
        
        if ($w('#dashboardRepeater')) {
            displayDashboardData(testResults);
        }
        
        hideLoading('#dashboardContainer');
    } catch (error) {
        console.error('❌ Failed to load dashboard:', error);
        showError('#dashboardContainer', 'Failed to load dashboard data');
        hideLoading('#dashboardContainer');
    }
}

// Display dashboard data
function displayDashboardData(testResults) {
    if ($w('#dashboardRepeater')) {
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
                
                // Color code status
                if (itemData.status === 'success') {
                    $item('#statusText').style.color = '#4CAF50';
                } else if (itemData.status === 'error') {
                    $item('#statusText').style.color = '#F44336';
                } else {
                    $item('#statusText').style.color = '#FF9800';
                }
            }
            
            if ($item('#messageText')) {
                $item('#messageText').text = itemData.message;
            }
        });
        
        console.log(`✅ Dashboard loaded with ${dashboardItems.length} items`);
    }
}

// Show club details
function showClubDetails(clubData) {
    if ($w('#clubDetailsLightbox')) {
        if ($w('#clubDetailsTitle')) {
            $w('#clubDetailsTitle').text = clubData.clubName;
        }
        if ($w('#clubDetailsCategory')) {
            $w('#clubDetailsCategory').text = `Category: ${clubData.clubCategory}`;
        }
        if ($w('#clubDetailsEquipment')) {
            $w('#clubDetailsEquipment').text = `Equipment: ${clubData.equipmentType}`;
        }
        if ($w('#clubDetailsDescription')) {
            $w('#clubDetailsDescription').text = clubData.description;
        }
        
        $w('#clubDetailsLightbox').show();
    }
}

// Show trail details
function showTrailDetails(trailData) {
    if ($w('#trailDetailsLightbox')) {
        if ($w('#trailDetailsTitle')) {
            $w('#trailDetailsTitle').text = trailData.trailName;
        }
        if ($w('#trailDetailsLocation')) {
            $w('#trailDetailsLocation').text = `Location: ${trailData.location}`;
        }
        if ($w('#trailDetailsDifficulty')) {
            $w('#trailDetailsDifficulty').text = `Difficulty: ${trailData.difficulty}`;
        }
        if ($w('#trailDetailsDistance')) {
            $w('#trailDetailsDistance').text = `Distance: ${trailData.distance}`;
        }
        if ($w('#trailDetailsDescription')) {
            $w('#trailDetailsDescription').text = trailData.description;
        }
        
        $w('#trailDetailsLightbox').show();
    }
}

// Utility Functions
function showLoading(selector) {
    if ($w('#loadingIcon')) {
        $w('#loadingIcon').show();
    }
    if ($w(selector)) {
        $w(selector).hide();
    }
}

function hideLoading(selector) {
    if ($w('#loadingIcon')) {
        $w('#loadingIcon').hide();
    }
    if ($w(selector)) {
        $w(selector).show();
    }
}

function showError(selector, message) {
    console.error('❌ Error:', message);
    if ($w('#errorMessage')) {
        $w('#errorMessage').text = message;
        $w('#errorMessage').show();
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            $w('#errorMessage').hide();
        }, 5000);
    }
}

function updateStatusIndicator(status, message) {
    if ($w('#statusIndicator')) {
        $w('#statusIndicator').text = message;
        if (status === 'online') {
            $w('#statusIndicator').style.color = '#4CAF50';
        } else {
            $w('#statusIndicator').style.color = '#F44336';
        }
    }
}

function updateClubCount(count) {
    if ($w('#clubCountDisplay')) {
        $w('#clubCountDisplay').text = `${count} Clubs Available`;
    }
}

function updateTrailCount(count) {
    if ($w('#trailCountDisplay')) {
        $w('#trailCountDisplay').text = `${count} Trails Available`;
    }
}

// Global functions for testing
window.testFitFriendsAPI = async function() {
    try {
        console.log('🧪 Testing FitFriends API...');
        const results = await fitFriendsAPI.runAllTests();
        console.log('✅ Test Results:', results);
        return results;
    } catch (error) {
        console.error('❌ Test failed:', error);
        return { status: 'error', message: error.message };
    }
};

console.log('✅ FitFriendsClubs Integration Ready!');
console.log('🔗 API URL:', FITFRIENDS_API_URL);
console.log('🧪 Test command: testFitFriendsAPI()');