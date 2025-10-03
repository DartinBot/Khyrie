// FitFriendsClubs Wix Integration
// This file contains all the JavaScript code needed to connect your Wix site to the FitFriendsClubs API

// API Configuration
const API_BASE_URL = 'https://fitfriendsclub-api.darnellroy2.workers.dev';

// API Helper Functions
class FitFriendsAPI {
    constructor() {
        this.baseUrl = API_BASE_URL;
    }

    // Generic API call function
    async apiCall(endpoint, options = {}) {
        try {
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
            console.error('API Error:', error);
            throw error;
        }
    }

    // Health check
    async healthCheck() {
        return await this.apiCall('/');
    }

    // Get fitness clubs
    async getFitnessClubs() {
        return await this.apiCall('/test/clubs');
    }

    // Get virtual trails
    async getVirtualTrails() {
        return await this.apiCall('/test/trails');
    }

    // Run all tests
    async runAllTests() {
        return await this.apiCall('/test/all');
    }

    // Get database status
    async getDatabaseStatus() {
        return await this.apiCall('/test/database');
    }
}

// Initialize API instance
const fitFriendsAPI = new FitFriendsAPI();

// Wix Page Event Handlers
$w.onReady(function () {
    console.log('FitFriendsClubs Wix site loaded!');
    
    // Initialize the homepage
    initializeHomepage();
    
    // Setup navigation
    setupNavigation();
    
    // Load initial data
    loadInitialData();
});

// Homepage initialization
async function initializeHomepage() {
    try {
        // Show loading state
        showLoading('#homePageContent');
        
        // Test API connection
        const healthCheck = await fitFriendsAPI.healthCheck();
        console.log('API Health Check:', healthCheck);
        
        // Update status indicator
        if (healthCheck.status === 'success') {
            updateStatusIndicator('online', 'FitFriendsClubs API Connected ✅');
        }
        
        hideLoading('#homePageContent');
    } catch (error) {
        console.error('Homepage initialization failed:', error);
        updateStatusIndicator('offline', 'API Connection Failed ❌');
        hideLoading('#homePageContent');
    }
}

// Load fitness clubs for clubs page
async function loadFitnessClubs() {
    try {
        showLoading('#clubsContainer');
        
        const response = await fitFriendsAPI.getFitnessClubs();
        
        if (response.status === 'success' && response.data.clubs) {
            displayFitnessClubs(response.data.clubs);
        } else {
            showError('#clubsContainer', 'Failed to load fitness clubs');
        }
        
        hideLoading('#clubsContainer');
    } catch (error) {
        console.error('Failed to load clubs:', error);
        showError('#clubsContainer', 'Error loading fitness clubs');
        hideLoading('#clubsContainer');
    }
}

// Load virtual trails for trails page
async function loadVirtualTrails() {
    try {
        showLoading('#trailsContainer');
        
        const response = await fitFriendsAPI.getVirtualTrails();
        
        if (response.status === 'success' && response.data.trails) {
            displayVirtualTrails(response.data.trails);
        } else {
            showError('#trailsContainer', 'Failed to load virtual trails');
        }
        
        hideLoading('#trailsContainer');
    } catch (error) {
        console.error('Failed to load trails:', error);
        showError('#trailsContainer', 'Error loading virtual trails');
        hideLoading('#trailsContainer');
    }
}

// Display fitness clubs in Wix repeater
function displayFitnessClubs(clubs) {
    if ($w('#clubsRepeater')) {
        $w('#clubsRepeater').data = clubs.map((club, index) => ({
            _id: club.id || `club-${index}`,
            clubName: club.name || 'Unknown Club',
            clubCategory: club.category || 'General',
            equipmentType: club.equipment_type || 'Mixed',
            description: club.description || 'Premium fitness club with modern equipment'
        }));
        
        // Setup repeater item ready handler
        $w('#clubsRepeater').onItemReady(($item, itemData) => {
            $item('#clubNameText').text = itemData.clubName;
            $item('#clubCategoryText').text = itemData.clubCategory;
            $item('#equipmentTypeText').text = `Equipment: ${itemData.equipmentType}`;
            
            // Add click handler for club details
            $item('#clubContainer').onClick(() => {
                showClubDetails(itemData);
            });
        });
    }
}

// Display virtual trails in Wix repeater
function displayVirtualTrails(trails) {
    if ($w('#trailsRepeater')) {
        $w('#trailsRepeater').data = trails.map((trail, index) => ({
            _id: trail.id || `trail-${index}`,
            trailName: trail.name || 'Unknown Trail',
            location: trail.location || 'Unknown Location',
            difficulty: trail.difficulty || 'Moderate',
            distance: trail.distance_km ? `${trail.distance_km}km` : 'Distance TBD',
            description: trail.description || 'Scenic virtual trail experience'
        }));
        
        // Setup repeater item ready handler
        $w('#trailsRepeater').onItemReady(($item, itemData) => {
            $item('#trailNameText').text = itemData.trailName;
            $item('#locationText').text = itemData.location;
            $item('#difficultyText').text = `Difficulty: ${itemData.difficulty}`;
            $item('#distanceText').text = itemData.distance;
            
            // Add click handler for trail details
            $item('#trailContainer').onClick(() => {
                showTrailDetails(itemData);
            });
        });
    }
}

// Show club details in a lightbox or modal
function showClubDetails(clubData) {
    // You can customize this based on your Wix site structure
    if ($w('#clubDetailsLightbox')) {
        $w('#clubDetailsTitle').text = clubData.clubName;
        $w('#clubDetailsCategory').text = `Category: ${clubData.clubCategory}`;
        $w('#clubDetailsEquipment').text = `Equipment: ${clubData.equipmentType}`;
        $w('#clubDetailsDescription').text = clubData.description;
        
        $w('#clubDetailsLightbox').show();
    }
}

// Show trail details in a lightbox or modal
function showTrailDetails(trailData) {
    // You can customize this based on your Wix site structure
    if ($w('#trailDetailsLightbox')) {
        $w('#trailDetailsTitle').text = trailData.trailName;
        $w('#trailDetailsLocation').text = `Location: ${trailData.location}`;
        $w('#trailDetailsDifficulty').text = `Difficulty: ${trailData.difficulty}`;
        $w('#trailDetailsDistance').text = `Distance: ${trailData.distance}`;
        $w('#trailDetailsDescription').text = trailData.description;
        
        $w('#trailDetailsLightbox').show();
    }
}

// Navigation setup
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
            loadFitnessClubs();
        });
    }
    
    // Trails button
    if ($w('#trailsButton')) {
        $w('#trailsButton').onClick(() => {
            wixLocation.to('/trails');
            loadVirtualTrails();
        });
    }
    
    // Dashboard button
    if ($w('#dashboardButton')) {
        $w('#dashboardButton').onClick(() => {
            wixLocation.to('/dashboard');
            loadUserDashboard();
        });
    }
}

// Load initial data when site loads
async function loadInitialData() {
    try {
        // Run a comprehensive test to ensure everything is working
        const testResults = await fitFriendsAPI.runAllTests();
        console.log('Initial API Tests:', testResults);
        
        // Update dashboard stats if on homepage
        if (testResults.status === 'success') {
            updateDashboardStats(testResults.results);
        }
    } catch (error) {
        console.error('Failed to load initial data:', error);
    }
}

// Update dashboard statistics
function updateDashboardStats(testResults) {
    // Find clubs and trails test results
    const clubsTest = testResults.find(test => test.name === 'Fitness Clubs');
    const trailsTest = testResults.find(test => test.name === 'Virtual Trails');
    
    // Update club count
    if ($w('#clubCountText') && clubsTest && clubsTest.dataCount !== undefined) {
        $w('#clubCountText').text = `${clubsTest.dataCount} Premium Clubs`;
    }
    
    // Update trail count
    if ($w('#trailCountText') && trailsTest && trailsTest.dataCount !== undefined) {
        $w('#trailCountText').text = `${trailsTest.dataCount} Virtual Trails`;
    }
    
    // Update status
    if ($w('#platformStatusText')) {
        const allWorking = testResults.every(test => test.status === 'success');
        $w('#platformStatusText').text = allWorking ? 'All Systems Operational' : 'Some Issues Detected';
    }
}

// User dashboard functionality
async function loadUserDashboard() {
    try {
        showLoading('#dashboardContainer');
        
        // Load user-specific data (you'll need to implement user authentication)
        // For now, show general platform stats
        const testResults = await fitFriendsAPI.runAllTests();
        
        if ($w('#dashboardStats')) {
            displayDashboardData(testResults);
        }
        
        hideLoading('#dashboardContainer');
    } catch (error) {
        console.error('Failed to load dashboard:', error);
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
            $item('#testNameText').text = itemData.testName;
            $item('#statusText').text = itemData.status.toUpperCase();
            $item('#messageText').text = itemData.message;
            
            // Color code status
            if (itemData.status === 'success') {
                $item('#statusText').style.color = '#4CAF50';
            } else if (itemData.status === 'error') {
                $item('#statusText').style.color = '#F44336';
            } else {
                $item('#statusText').style.color = '#FF9800';
            }
        });
    }
}

// Utility functions
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
    console.error('Error:', message);
    if ($w('#errorMessage')) {
        $w('#errorMessage').text = message;
        $w('#errorMessage').show();
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

// Export functions for use in Wix pages
export {
    fitFriendsAPI,
    loadFitnessClubs,
    loadVirtualTrails,
    loadUserDashboard,
    initializeHomepage
};