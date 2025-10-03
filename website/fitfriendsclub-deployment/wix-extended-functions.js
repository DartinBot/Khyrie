// Extended API Integration Functions for FitFriendsClubs Wix Site
// This file provides additional functionality beyond basic club/trail display

// Enhanced API Class with more fitness-specific functions
class ExtendedFitFriendsAPI extends FitFriendsAPI {
    constructor() {
        super();
    }

    // User Management Functions (for future authentication)
    async createUser(userData) {
        return await this.apiCall('/api/users', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async getUserProfile(userId) {
        return await this.apiCall(`/api/users/${userId}`);
    }

    // Workout Session Functions
    async startWorkoutSession(sessionData) {
        return await this.apiCall('/api/sessions/start', {
            method: 'POST',
            body: JSON.stringify(sessionData)
        });
    }

    async endWorkoutSession(sessionId, sessionStats) {
        return await this.apiCall(`/api/sessions/${sessionId}/end`, {
            method: 'PUT',
            body: JSON.stringify(sessionStats)
        });
    }

    // Search and Filter Functions
    async searchClubs(query, filters = {}) {
        const params = new URLSearchParams({
            q: query,
            ...filters
        });
        return await this.apiCall(`/api/clubs/search?${params}`);
    }

    async searchTrails(query, filters = {}) {
        const params = new URLSearchParams({
            q: query,
            ...filters
        });
        return await this.apiCall(`/api/trails/search?${params}`);
    }

    // Statistics Functions
    async getUserStats(userId) {
        return await this.apiCall(`/api/users/${userId}/stats`);
    }

    async getClubStats(clubId) {
        return await this.apiCall(`/api/clubs/${clubId}/stats`);
    }
}

// Initialize extended API
const extendedAPI = new ExtendedFitFriendsAPI();

// Advanced Wix Integration Functions

// Enhanced Club Display with Filtering
async function displayClubsWithFilters() {
    try {
        // Get filter values from Wix form elements
        const category = $w('#clubCategoryFilter').value || '';
        const equipment = $w('#equipmentTypeFilter').value || '';
        
        showLoading('#clubsContainer');
        
        let response;
        if (category || equipment) {
            // Use search with filters when available
            response = await extendedAPI.searchClubs('', { category, equipment });
        } else {
            // Default to getting all clubs
            response = await fitFriendsAPI.getFitnessClubs();
        }
        
        if (response.status === 'success' && response.data.clubs) {
            displayFitnessClubs(response.data.clubs);
            updateClubCount(response.data.clubs.length);
        }
        
        hideLoading('#clubsContainer');
    } catch (error) {
        console.error('Failed to load filtered clubs:', error);
        showError('#clubsContainer', 'Error loading clubs with filters');
    }
}

// Enhanced Trail Display with Difficulty Filtering
async function displayTrailsWithFilters() {
    try {
        // Get filter values
        const difficulty = $w('#trailDifficultyFilter').value || '';
        const location = $w('#trailLocationFilter').value || '';
        
        showLoading('#trailsContainer');
        
        let response;
        if (difficulty || location) {
            response = await extendedAPI.searchTrails('', { difficulty, location });
        } else {
            response = await fitFriendsAPI.getVirtualTrails();
        }
        
        if (response.status === 'success' && response.data.trails) {
            displayVirtualTrails(response.data.trails);
            updateTrailCount(response.data.trails.length);
        }
        
        hideLoading('#trailsContainer');
    } catch (error) {
        console.error('Failed to load filtered trails:', error);
        showError('#trailsContainer', 'Error loading trails with filters');
    }
}

// Workout Session Management
class WorkoutSessionManager {
    constructor() {
        this.currentSession = null;
        this.sessionStartTime = null;
        this.sessionTimer = null;
    }

    async startSession(clubId, trailId, userId = 'demo-user') {
        try {
            const sessionData = {
                userId: userId,
                clubId: clubId,
                trailId: trailId,
                startTime: new Date().toISOString()
            };

            // Start session via API (when available)
            // const response = await extendedAPI.startWorkoutSession(sessionData);
            
            // For now, simulate local session
            this.currentSession = {
                id: `session-${Date.now()}`,
                ...sessionData
            };
            
            this.sessionStartTime = Date.now();
            this.startSessionTimer();
            
            // Update UI
            this.showSessionUI();
            
            return this.currentSession;
        } catch (error) {
            console.error('Failed to start workout session:', error);
            throw error;
        }
    }

    async endSession() {
        if (!this.currentSession) return;

        try {
            const endTime = Date.now();
            const duration = Math.floor((endTime - this.sessionStartTime) / 1000); // seconds

            const sessionStats = {
                endTime: new Date().toISOString(),
                duration: duration,
                // Add more stats as needed
            };

            // End session via API (when available)
            // await extendedAPI.endWorkoutSession(this.currentSession.id, sessionStats);

            this.stopSessionTimer();
            this.hideSessionUI();
            this.showSessionSummary(duration);

            this.currentSession = null;
            this.sessionStartTime = null;
        } catch (error) {
            console.error('Failed to end workout session:', error);
        }
    }

    startSessionTimer() {
        this.sessionTimer = setInterval(() => {
            if (this.sessionStartTime) {
                const elapsed = Math.floor((Date.now() - this.sessionStartTime) / 1000);
                this.updateSessionDisplay(elapsed);
            }
        }, 1000);
    }

    stopSessionTimer() {
        if (this.sessionTimer) {
            clearInterval(this.sessionTimer);
            this.sessionTimer = null;
        }
    }

    updateSessionDisplay(elapsedSeconds) {
        const minutes = Math.floor(elapsedSeconds / 60);
        const seconds = elapsedSeconds % 60;
        const timeDisplay = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        if ($w('#sessionTimer')) {
            $w('#sessionTimer').text = timeDisplay;
        }
    }

    showSessionUI() {
        if ($w('#sessionControls')) {
            $w('#sessionControls').show();
        }
        if ($w('#endSessionButton')) {
            $w('#endSessionButton').onClick(() => this.endSession());
        }
    }

    hideSessionUI() {
        if ($w('#sessionControls')) {
            $w('#sessionControls').hide();
        }
    }

    showSessionSummary(duration) {
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        
        if ($w('#sessionSummaryLightbox')) {
            if ($w('#sessionDurationText')) {
                $w('#sessionDurationText').text = `${minutes}m ${seconds}s`;
            }
            $w('#sessionSummaryLightbox').show();
        }
    }
}

// Initialize session manager
const sessionManager = new WorkoutSessionManager();

// Enhanced Search Functionality
function setupSearchFunctionality() {
    // Club search
    if ($w('#clubSearchInput')) {
        $w('#clubSearchInput').onInput(debounce(async () => {
            const query = $w('#clubSearchInput').value;
            if (query.length >= 3) {
                await searchAndDisplayClubs(query);
            } else if (query.length === 0) {
                await loadFitnessClubs(); // Reset to all clubs
            }
        }, 300));
    }

    // Trail search
    if ($w('#trailSearchInput')) {
        $w('#trailSearchInput').onInput(debounce(async () => {
            const query = $w('#trailSearchInput').value;
            if (query.length >= 3) {
                await searchAndDisplayTrails(query);
            } else if (query.length === 0) {
                await loadVirtualTrails(); // Reset to all trails
            }
        }, 300));
    }
}

async function searchAndDisplayClubs(query) {
    try {
        showLoading('#clubsContainer');
        
        // For now, filter existing data (until search API is available)
        const response = await fitFriendsAPI.getFitnessClubs();
        
        if (response.status === 'success' && response.data.clubs) {
            const filteredClubs = response.data.clubs.filter(club =>
                club.name.toLowerCase().includes(query.toLowerCase()) ||
                club.category.toLowerCase().includes(query.toLowerCase())
            );
            displayFitnessClubs(filteredClubs);
        }
        
        hideLoading('#clubsContainer');
    } catch (error) {
        console.error('Search failed:', error);
        showError('#clubsContainer', 'Search failed');
    }
}

async function searchAndDisplayTrails(query) {
    try {
        showLoading('#trailsContainer');
        
        const response = await fitFriendsAPI.getVirtualTrails();
        
        if (response.status === 'success' && response.data.trails) {
            const filteredTrails = response.data.trails.filter(trail =>
                trail.name.toLowerCase().includes(query.toLowerCase()) ||
                trail.location.toLowerCase().includes(query.toLowerCase())
            );
            displayVirtualTrails(filteredTrails);
        }
        
        hideLoading('#trailsContainer');
    } catch (error) {
        console.error('Search failed:', error);
        showError('#trailsContainer', 'Trail search failed');
    }
}

// Favorites System (Local Storage)
class FavoritesManager {
    constructor() {
        this.favorites = this.loadFavorites();
    }

    loadFavorites() {
        try {
            return JSON.parse(localStorage.getItem('fitfriends_favorites') || '{"clubs": [], "trails": []}');
        } catch {
            return { clubs: [], trails: [] };
        }
    }

    saveFavorites() {
        localStorage.setItem('fitfriends_favorites', JSON.stringify(this.favorites));
    }

    addClubToFavorites(clubId) {
        if (!this.favorites.clubs.includes(clubId)) {
            this.favorites.clubs.push(clubId);
            this.saveFavorites();
            return true;
        }
        return false;
    }

    removeClubFromFavorites(clubId) {
        const index = this.favorites.clubs.indexOf(clubId);
        if (index > -1) {
            this.favorites.clubs.splice(index, 1);
            this.saveFavorites();
            return true;
        }
        return false;
    }

    addTrailToFavorites(trailId) {
        if (!this.favorites.trails.includes(trailId)) {
            this.favorites.trails.push(trailId);
            this.saveFavorites();
            return true;
        }
        return false;
    }

    removeTrailFromFavorites(trailId) {
        const index = this.favorites.trails.indexOf(trailId);
        if (index > -1) {
            this.favorites.trails.splice(index, 1);
            this.saveFavorites();
            return true;
        }
        return false;
    }

    isClubFavorite(clubId) {
        return this.favorites.clubs.includes(clubId);
    }

    isTrailFavorite(trailId) {
        return this.favorites.trails.includes(trailId);
    }
}

// Initialize favorites manager
const favoritesManager = new FavoritesManager();

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function updateClubCount(count) {
    if ($w('#clubCountDisplay')) {
        $w('#clubCountDisplay').text = `${count} Clubs Found`;
    }
}

function updateTrailCount(count) {
    if ($w('#trailCountDisplay')) {
        $w('#trailCountDisplay').text = `${count} Trails Available`;
    }
}

// Export additional functions
export {
    extendedAPI,
    sessionManager,
    favoritesManager,
    displayClubsWithFilters,
    displayTrailsWithFilters,
    setupSearchFunctionality,
    WorkoutSessionManager,
    FavoritesManager
};