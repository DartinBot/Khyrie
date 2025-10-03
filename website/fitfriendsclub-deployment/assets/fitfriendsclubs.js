/**
 * FitFriendsClubs WordPress Plugin JavaScript
 * Converted from Wix $w API to standard DOM manipulation
 */

(function() {
    'use strict';
    
    // Configuration from WordPress localized script
    var config = {
        API_URL: fitfriendsclubs_ajax.api_url || 'https://fitfriendsclub-api.darnellroy2.workers.dev',
        DEBUG: parseInt(fitfriendsclubs_ajax.debug_mode) || 0,
        AUTO_LOAD: parseInt(fitfriendsclubs_ajax.auto_load) || 1,
        RETRY: 3,
        TIMEOUT: 15000,
        FEATURES: {
            CLUBS: 1,
            TRAILS: 1,
            DASHBOARD: 1,
            MODALS: 1
        }
    };
    
    var api;
    
    // Utility Functions (converted from Wix $w to DOM)
    function $(selector) {
        return document.querySelector(selector);
    }
    
    function $$(selector) {
        return document.querySelectorAll(selector);
    }
    
    function showLoading(selector) {
        try {
            var loadingIcon = $('#ff-loading-indicator');
            if (loadingIcon) loadingIcon.style.display = 'block';
            
            if (selector) {
                var element = $(selector);
                if (element) element.classList.add('loading');
            }
        } catch (e) {
            if (config.DEBUG) console.error('showLoading error:', e);
        }
    }
    
    function hideLoading(selector) {
        try {
            var loadingIcon = $('#ff-loading-indicator');
            if (loadingIcon) loadingIcon.style.display = 'none';
            
            if (selector) {
                var element = $(selector);
                if (element) element.classList.remove('loading');
            }
        } catch (e) {
            if (config.DEBUG) console.error('hideLoading error:', e);
        }
    }
    
    function showError(message) {
        console.error('ERROR:', message);
        try {
            var errorContainer = $('#ff-error-message') || createMessageContainer('error');
            errorContainer.textContent = message;
            errorContainer.className = 'ff-error';
            errorContainer.style.display = 'block';
            setTimeout(function() {
                if (errorContainer) errorContainer.style.display = 'none';
            }, 7000);
        } catch (e) {
            if (config.DEBUG) console.error('showError error:', e);
        }
    }
    
    function showSuccess(message) {
        console.log('SUCCESS:', message);
        try {
            var successContainer = $('#ff-success-message') || createMessageContainer('success');
            successContainer.textContent = message;
            successContainer.className = 'ff-success';
            successContainer.style.display = 'block';
            setTimeout(function() {
                if (successContainer) successContainer.style.display = 'none';
            }, 4000);
        } catch (e) {
            if (config.DEBUG) console.error('showSuccess error:', e);
        }
    }
    
    function createMessageContainer(type) {
        var container = document.createElement('div');
        container.id = 'ff-' + type + '-message';
        container.style.position = 'fixed';
        container.style.top = (type === 'error' ? '20px' : '60px');
        container.style.right = '20px';
        container.style.zIndex = '9998';
        container.style.maxWidth = '350px';
        container.style.display = 'none';
        document.body.appendChild(container);
        return container;
    }
    
    function updateStatus(type, message) {
        var statusSelectors = [
            '#ff-connection-status',
            '#ff-system-status',
            '#ff-status-display',
            '#ff-global-status'
        ];
        
        statusSelectors.forEach(function(selector) {
            try {
                var element = $(selector);
                if (element) {
                    element.textContent = message;
                    element.className = '';
                    if (type === 'online' || type === 'success') {
                        element.classList.add('ff-online');
                    } else if (type === 'offline' || type === 'error') {
                        element.classList.add('ff-offline');
                    } else if (type === 'connecting') {
                        element.classList.add('ff-connecting');
                    }
                }
            } catch (e) {
                if (config.DEBUG) console.error('updateStatus error:', e);
            }
        });
    }
    
    function updateClubCount(count) {
        var countSelectors = [
            '#ff-club-count',
            '#ff-clubs-count',
            '#ff-total-clubs'
        ];
        
        countSelectors.forEach(function(selector) {
            try {
                var element = $(selector);
                if (element) {
                    element.textContent = count + ' Clubs Available';
                }
            } catch (e) {
                if (config.DEBUG) console.error('updateClubCount error:', e);
            }
        });
    }
    
    function updateTrailCount(count) {
        var countSelectors = [
            '#ff-trail-count',
            '#ff-trails-count',
            '#ff-total-trails'
        ];
        
        countSelectors.forEach(function(selector) {
            try {
                var element = $(selector);
                if (element) {
                    element.textContent = count + ' Trails Available';
                }
            } catch (e) {
                if (config.DEBUG) console.error('updateTrailCount error:', e);
            }
        });
    }
    
    // API Class
    class FitFriendsAPI {
        constructor() {
            this.baseUrl = config.API_URL;
            this.timeout = config.TIMEOUT || 15000;
            this.retryAttempts = config.RETRY || 3;
        }
        
        async call(endpoint, options = {}, attempt = 1) {
            var controller = new AbortController();
            var timeoutId = setTimeout(function() { controller.abort(); }, this.timeout);
            
            try {
                if (config.DEBUG) {
                    console.log('API Call (' + attempt + '): ' + this.baseUrl + endpoint);
                }
                
                var response = await fetch(this.baseUrl + endpoint, {
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
                    throw new Error('HTTP ' + response.status + ': ' + response.statusText);
                }
                
                var result = await response.json();
                
                if (config.DEBUG) {
                    console.log('API Success: ' + endpoint, result);
                }
                
                return result;
            } catch (error) {
                clearTimeout(timeoutId);
                console.error('API Error (' + attempt + '):', error);
                
                if (attempt < this.retryAttempts && error.name !== 'AbortError') {
                    console.log('Retrying... (' + (attempt + 1) + '/' + this.retryAttempts + ')');
                    await new Promise(function(resolve) {
                        setTimeout(resolve, 1000 * attempt);
                    });
                    return this.call(endpoint, options, attempt + 1);
                }
                
                throw error;
            }
        }
        
        async health() {
            return await this.call('/');
        }
        
        async getClubs() {
            return await this.call('/test/clubs');
        }
        
        async getTrails() {
            return await this.call('/test/trails');
        }
        
        async runTests() {
            return await this.call('/test/all');
        }
    }
    
    // Main Functions
    async function init() {
        try {
            console.log('Initializing FitFriendsClubs...');
            
            if (!api) {
                api = new FitFriendsAPI();
            }
            
            showLoading();
            updateStatus('connecting', 'Connecting...');
            
            var health = await api.health();
            console.log('Health Check:', health);
            
            if (health.status === 'success') {
                updateStatus('online', 'API Connected');
                showSuccess('Connected to FitFriendsClubs API!');
            } else {
                throw new Error('Health check failed');
            }
            
            hideLoading();
            return true;
        } catch (error) {
            console.error('Init failed:', error);
            updateStatus('offline', 'Connection Failed');
            showError('Failed to connect: ' + error.message);
            hideLoading();
            return false;
        }
    }
    
    async function runTest() {
        try {
            console.log('Running API test...');
            showLoading('#ff-test-output');
            updateStatus('testing', 'Running Tests...');
            
            var result = await api.runTests();
            
            var testElements = $$('#ff-test-output, #ff-test-results, #admin-test-results');
            testElements.forEach(function(element) {
                if (element) {
                    element.innerHTML = '<div class="ff-success">SUCCESS: ' + (result.message || 'All tests passed!') + '</div>';
                }
            });
            
            console.log('Test Results:', result);
            showSuccess('Tests completed successfully!');
            updateStatus('online', 'Tests Passed');
            
            return result;
        } catch (error) {
            console.error('Test failed:', error);
            
            var testElements = $$('#ff-test-output, #ff-test-results, #admin-test-results');
            testElements.forEach(function(element) {
                if (element) {
                    element.innerHTML = '<div class="ff-error">FAILED: ' + error.message + '</div>';
                }
            });
            
            showError('Test failed: ' + error.message);
            updateStatus('error', 'Tests Failed');
            
            return { status: 'error', message: error.message };
        } finally {
            hideLoading('#ff-test-output');
        }
    }
    
    async function loadClubs(limit = 10) {
        if (!config.FEATURES.CLUBS) return;
        
        try {
            console.log('Loading clubs...');
            showLoading('#ff-clubs-loading');
            
            var result = await api.getClubs();
            
            if (result.status === 'success' && result.data && result.data.clubs) {
                displayClubs(result.data.clubs.slice(0, limit));
                updateClubCount(result.data.clubs.length);
                console.log('Loaded ' + result.data.clubs.length + ' clubs');
            } else {
                throw new Error('Invalid clubs data');
            }
        } catch (error) {
            console.error('Load clubs failed:', error);
            showError('Error loading clubs: ' + error.message);
        } finally {
            hideLoading('#ff-clubs-loading');
        }
    }
    
    async function loadTrails(limit = 10, difficulty = 'all') {
        if (!config.FEATURES.TRAILS) return;
        
        try {
            console.log('Loading trails...');
            showLoading('#ff-trails-loading');
            
            var result = await api.getTrails();
            
            if (result.status === 'success' && result.data && result.data.trails) {
                var trails = result.data.trails;
                
                // Filter by difficulty if specified
                if (difficulty !== 'all') {
                    trails = trails.filter(function(trail) {
                        return trail.difficulty && trail.difficulty.toLowerCase() === difficulty.toLowerCase();
                    });
                }
                
                displayTrails(trails.slice(0, limit));
                updateTrailCount(result.data.trails.length);
                console.log('Loaded ' + trails.length + ' trails');
            } else {
                throw new Error('Invalid trails data');
            }
        } catch (error) {
            console.error('Load trails failed:', error);
            showError('Error loading trails: ' + error.message);
        } finally {
            hideLoading('#ff-trails-loading');
        }
    }
    
    function displayClubs(clubs) {
        try {
            var container = $('#ff-clubs-list');
            if (!container) {
                console.warn('Clubs container not found');
                return;
            }
            
            container.innerHTML = '';
            
            clubs.forEach(function(club, index) {
                var clubCard = document.createElement('div');
                clubCard.className = 'ff-club-card';
                clubCard.innerHTML = `
                    <h4>${club.name || 'Unknown Club'}</h4>
                    <p><strong>Category:</strong> ${club.category || 'General Fitness'}</p>
                    <p><strong>Equipment:</strong> ${club.equipment_type || 'Mixed'}</p>
                    <p><strong>Location:</strong> ${club.location || 'Location TBD'}</p>
                    <p><strong>Members:</strong> ${club.member_count || 0}</p>
                    <p>${club.description || 'Premium fitness club experience'}</p>
                `;
                
                clubCard.addEventListener('click', function() {
                    showClubDetails({
                        clubName: club.name || 'Unknown Club',
                        clubCategory: club.category || 'General',
                        equipmentType: club.equipment_type || 'Mixed',
                        location: club.location || 'Location TBD',
                        memberCount: club.member_count || 0,
                        description: club.description || 'Premium fitness club'
                    });
                });
                
                container.appendChild(clubCard);
            });
            
            console.log('Displayed ' + clubs.length + ' clubs');
        } catch (error) {
            console.error('Display clubs failed:', error);
        }
    }
    
    function displayTrails(trails) {
        try {
            var container = $('#ff-trails-list');
            if (!container) {
                console.warn('Trails container not found');
                return;
            }
            
            container.innerHTML = '';
            
            trails.forEach(function(trail, index) {
                var trailCard = document.createElement('div');
                trailCard.className = 'ff-trail-card';
                
                var difficultyClass = 'ff-diff-' + (trail.difficulty || 'moderate').toLowerCase();
                
                trailCard.innerHTML = `
                    <h4>${trail.name || 'Unknown Trail'}</h4>
                    <p><strong>Location:</strong> ${trail.location || 'Unknown Location'}</p>
                    <p><strong>Difficulty:</strong> <span class="ff-badge ${difficultyClass}">${trail.difficulty || 'Moderate'}</span></p>
                    <p><strong>Distance:</strong> ${trail.distance_km ? trail.distance_km + 'km' : 'Distance TBD'}</p>
                    <p><strong>Est. Time:</strong> ${trail.estimated_time || '30-60 min'}</p>
                    <p>${trail.description || 'Virtual trail experience'}</p>
                `;
                
                trailCard.addEventListener('click', function() {
                    showTrailDetails({
                        trailName: trail.name || 'Unknown Trail',
                        location: trail.location || 'Unknown Location',
                        difficulty: trail.difficulty || 'Moderate',
                        distance: trail.distance_km ? trail.distance_km + 'km' : 'Distance TBD',
                        estimatedTime: trail.estimated_time || '30-60 min',
                        elevation: trail.elevation_gain || 'Moderate',
                        description: trail.description || 'Virtual trail experience'
                    });
                });
                
                container.appendChild(trailCard);
            });
            
            console.log('Displayed ' + trails.length + ' trails');
        } catch (error) {
            console.error('Display trails failed:', error);
        }
    }
    
    function showClubDetails(clubData) {
        if (!config.FEATURES.MODALS) return;
        
        try {
            var modal = $('#ff-club-modal');
            if (!modal) return;
            
            $('#ff-club-title').textContent = clubData.clubName;
            $('#ff-club-category').textContent = clubData.clubCategory;
            $('#ff-club-equipment').textContent = clubData.equipmentType;
            $('#ff-club-location').textContent = clubData.location;
            $('#ff-club-members').textContent = clubData.memberCount + ' members';
            $('#ff-club-description').textContent = clubData.description;
            
            modal.style.display = 'block';
        } catch (error) {
            console.error('Show club details failed:', error);
        }
    }
    
    function showTrailDetails(trailData) {
        if (!config.FEATURES.MODALS) return;
        
        try {
            var modal = $('#ff-trail-modal');
            if (!modal) return;
            
            $('#ff-trail-title').textContent = trailData.trailName;
            $('#ff-trail-location').textContent = trailData.location;
            $('#ff-trail-difficulty').textContent = trailData.difficulty;
            $('#ff-trail-difficulty').className = 'ff-badge ff-diff-' + trailData.difficulty.toLowerCase();
            $('#ff-trail-distance').textContent = trailData.distance;
            $('#ff-trail-time').textContent = trailData.estimatedTime;
            $('#ff-trail-elevation').textContent = trailData.elevation;
            $('#ff-trail-description').textContent = trailData.description;
            
            modal.style.display = 'block';
        } catch (error) {
            console.error('Show trail details failed:', error);
        }
    }
    
    async function initDashboard() {
        try {
            console.log('Loading dashboard...');
            showLoading('#fitfriendsclubs-dashboard-container');
            
            var testResult = await api.runTests();
            
            if (testResult.status === 'success') {
                var clubTest = testResult.results.find(function(test) {
                    return test.name.toLowerCase().includes('club');
                });
                var trailTest = testResult.results.find(function(test) {
                    return test.name.toLowerCase().includes('trail');
                });
                
                if (clubTest) updateClubCount(clubTest.dataCount || 0);
                if (trailTest) updateTrailCount(trailTest.dataCount || 0);
                
                updateStatus('online', 'All Systems Operational');
            }
            
            console.log('Dashboard loaded');
        } catch (error) {
            console.error('Dashboard load failed:', error);
            showError('Dashboard error: ' + error.message);
        } finally {
            hideLoading('#fitfriendsclubs-dashboard-container');
        }
    }
    
    // Event Listeners
    function setupEventListeners() {
        // Modal close buttons
        var closeButtons = $$('.ff-close');
        closeButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                var modal = button.closest('.ff-modal');
                if (modal) modal.style.display = 'none';
            });
        });
        
        // Click outside modal to close
        window.addEventListener('click', function(event) {
            if (event.target.classList.contains('ff-modal')) {
                event.target.style.display = 'none';
            }
        });
        
        // Test button
        var testButton = $('#ff-test-button');
        if (testButton) {
            testButton.addEventListener('click', runTest);
        }
        
        // Run test button
        var runTestButton = $('#ff-run-test');
        if (runTestButton) {
            runTestButton.addEventListener('click', runTest);
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                var modals = $$('.ff-modal');
                modals.forEach(function(modal) {
                    modal.style.display = 'none';
                });
            }
            
            if ((event.ctrlKey || event.metaKey) && event.key === 't' && config.DEBUG) {
                event.preventDefault();
                runTest();
            }
            
            if ((event.ctrlKey || event.metaKey) && event.key === 'd' && config.DEBUG) {
                event.preventDefault();
                console.log('Debug Info:', {
                    config: config,
                    api: api,
                    timestamp: new Date().toISOString()
                });
            }
        });
    }
    
    // Initialize when DOM is ready
    function initializePlugin() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                init().then(function(success) {
                    if (success) {
                        setupEventListeners();
                    }
                });
            });
        } else {
            init().then(function(success) {
                if (success) {
                    setupEventListeners();
                }
            });
        }
    }
    
    // Global interface
    window.FitFriendsClubs = {
        api: api,
        config: config,
        init: init,
        runTest: runTest,
        loadClubs: loadClubs,
        loadTrails: loadTrails,
        initDashboard: initDashboard,
        showClubDetails: showClubDetails,
        showTrailDetails: showTrailDetails,
        utils: {
            showLoading: showLoading,
            hideLoading: hideLoading,
            showError: showError,
            showSuccess: showSuccess,
            updateStatus: updateStatus
        }
    };
    
    // Auto-initialize
    initializePlugin();
    
    console.log('FitFriendsClubs WordPress Plugin Loaded!');
    
})();