// FitFriendsClubs Authentication System for Wix
// This provides user authentication using Supabase Auth via your API

class FitFriendsAuth {
    constructor() {
        this.currentUser = null;
        this.authToken = null;
        this.apiBaseUrl = 'https://fitfriendsclub-api.darnellroy2.workers.dev';
        
        // Load saved auth state
        this.loadAuthState();
        
        // Setup auth UI handlers
        this.setupAuthHandlers();
    }

    // Load authentication state from localStorage
    loadAuthState() {
        try {
            const savedAuth = localStorage.getItem('fitfriends_auth');
            if (savedAuth) {
                const authData = JSON.parse(savedAuth);
                this.currentUser = authData.user;
                this.authToken = authData.token;
                
                // Validate token (you might want to check expiry)
                if (this.authToken) {
                    this.updateUIForAuthenticatedUser();
                }
            }
        } catch (error) {
            console.error('Failed to load auth state:', error);
            this.clearAuthState();
        }
    }

    // Save authentication state to localStorage
    saveAuthState() {
        if (this.currentUser && this.authToken) {
            localStorage.setItem('fitfriends_auth', JSON.stringify({
                user: this.currentUser,
                token: this.authToken
            }));
        }
    }

    // Clear authentication state
    clearAuthState() {
        this.currentUser = null;
        this.authToken = null;
        localStorage.removeItem('fitfriends_auth');
        this.updateUIForUnauthenticatedUser();
    }

    // Setup event handlers for auth UI elements
    setupAuthHandlers() {
        // Login form
        if ($w('#loginButton')) {
            $w('#loginButton').onClick(() => this.handleLogin());
        }

        // Register form
        if ($w('#registerButton')) {
            $w('#registerButton').onClick(() => this.handleRegister());
        }

        // Logout button
        if ($w('#logoutButton')) {
            $w('#logoutButton').onClick(() => this.handleLogout());
        }

        // Show login modal
        if ($w('#showLoginButton')) {
            $w('#showLoginButton').onClick(() => {
                if ($w('#loginModal')) {
                    $w('#loginModal').show();
                }
            });
        }

        // Show register modal
        if ($w('#showRegisterButton')) {
            $w('#showRegisterButton').onClick(() => {
                if ($w('#registerModal')) {
                    $w('#registerModal').show();
                }
            });
        }

        // Close modals
        if ($w('#closeLoginModal')) {
            $w('#closeLoginModal').onClick(() => {
                if ($w('#loginModal')) {
                    $w('#loginModal').hide();
                }
            });
        }

        if ($w('#closeRegisterModal')) {
            $w('#closeRegisterModal').onClick(() => {
                if ($w('#registerModal')) {
                    $w('#registerModal').hide();
                }
            });
        }
    }

    // Handle user login
    async handleLogin() {
        try {
            const email = $w('#loginEmail').value;
            const password = $w('#loginPassword').value;

            if (!email || !password) {
                this.showAuthError('Please enter both email and password');
                return;
            }

            // Show loading
            this.showAuthLoading(true);

            // For now, simulate login since auth API isn't implemented yet
            // In a real implementation, you would call your auth API
            const loginResult = await this.simulateLogin(email, password);

            if (loginResult.success) {
                this.currentUser = loginResult.user;
                this.authToken = loginResult.token;
                this.saveAuthState();
                this.updateUIForAuthenticatedUser();
                
                // Hide login modal
                if ($w('#loginModal')) {
                    $w('#loginModal').hide();
                }
                
                // Show success message
                this.showAuthSuccess('Login successful!');
            } else {
                this.showAuthError(loginResult.error);
            }

        } catch (error) {
            console.error('Login failed:', error);
            this.showAuthError('Login failed. Please try again.');
        } finally {
            this.showAuthLoading(false);
        }
    }

    // Handle user registration
    async handleRegister() {
        try {
            const email = $w('#registerEmail').value;
            const password = $w('#registerPassword').value;
            const username = $w('#registerUsername').value;

            if (!email || !password || !username) {
                this.showAuthError('Please fill in all fields');
                return;
            }

            if (password.length < 6) {
                this.showAuthError('Password must be at least 6 characters');
                return;
            }

            // Show loading
            this.showAuthLoading(true);

            // Simulate registration
            const registerResult = await this.simulateRegister(email, password, username);

            if (registerResult.success) {
                this.currentUser = registerResult.user;
                this.authToken = registerResult.token;
                this.saveAuthState();
                this.updateUIForAuthenticatedUser();
                
                // Hide register modal
                if ($w('#registerModal')) {
                    $w('#registerModal').hide();
                }
                
                this.showAuthSuccess('Registration successful!');
            } else {
                this.showAuthError(registerResult.error);
            }

        } catch (error) {
            console.error('Registration failed:', error);
            this.showAuthError('Registration failed. Please try again.');
        } finally {
            this.showAuthLoading(false);
        }
    }

    // Handle user logout
    handleLogout() {
        this.clearAuthState();
        this.showAuthSuccess('Logged out successfully');
        
        // Redirect to home page
        wixLocation.to('/');
    }

    // Simulate login (replace with real API call later)
    async simulateLogin(email, password) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Simple demo validation
        if (email === 'demo@fitfriendsclub.com' && password === 'demo123') {
            return {
                success: true,
                user: {
                    id: 'demo-user-123',
                    email: email,
                    username: 'Demo User',
                    created_at: new Date().toISOString()
                },
                token: 'demo-jwt-token-' + Date.now()
            };
        } else {
            return {
                success: false,
                error: 'Invalid email or password'
            };
        }
    }

    // Simulate registration (replace with real API call later)
    async simulateRegister(email, password, username) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Simple validation
        if (email.includes('@') && password.length >= 6) {
            return {
                success: true,
                user: {
                    id: 'user-' + Date.now(),
                    email: email,
                    username: username,
                    created_at: new Date().toISOString()
                },
                token: 'jwt-token-' + Date.now()
            };
        } else {
            return {
                success: false,
                error: 'Registration failed. Please check your information.'
            };
        }
    }

    // Update UI for authenticated users
    updateUIForAuthenticatedUser() {
        // Hide login/register buttons
        if ($w('#showLoginButton')) {
            $w('#showLoginButton').hide();
        }
        if ($w('#showRegisterButton')) {
            $w('#showRegisterButton').hide();
        }

        // Show user menu
        if ($w('#userMenu')) {
            $w('#userMenu').show();
        }

        // Update user display
        if ($w('#currentUserText') && this.currentUser) {
            $w('#currentUserText').text = `Welcome, ${this.currentUser.username}!`;
        }

        // Show logout button
        if ($w('#logoutButton')) {
            $w('#logoutButton').show();
        }

        // Enable authenticated features
        this.enableAuthenticatedFeatures();
    }

    // Update UI for unauthenticated users
    updateUIForUnauthenticatedUser() {
        // Show login/register buttons
        if ($w('#showLoginButton')) {
            $w('#showLoginButton').show();
        }
        if ($w('#showRegisterButton')) {
            $w('#showRegisterButton').show();
        }

        // Hide user menu
        if ($w('#userMenu')) {
            $w('#userMenu').hide();
        }

        // Hide logout button
        if ($w('#logoutButton')) {
            $w('#logoutButton').hide();
        }

        // Clear user display
        if ($w('#currentUserText')) {
            $w('#currentUserText').text = '';
        }

        // Disable authenticated features
        this.disableAuthenticatedFeatures();
    }

    // Enable features that require authentication
    enableAuthenticatedFeatures() {
        // Enable workout session buttons
        if ($w('#startWorkoutButton')) {
            $w('#startWorkoutButton').enable();
            $w('#startWorkoutButton').onClick(() => {
                // Integration with session manager
                if (typeof sessionManager !== 'undefined') {
                    sessionManager.startSession('demo-club', 'demo-trail', this.currentUser.id);
                }
            });
        }

        // Enable favorites
        if ($w('#favoriteButtons')) {
            $w('#favoriteButtons').show();
        }

        // Show user dashboard access
        if ($w('#dashboardButton')) {
            $w('#dashboardButton').show();
        }
    }

    // Disable features that require authentication
    disableAuthenticatedFeatures() {
        // Disable workout session buttons
        if ($w('#startWorkoutButton')) {
            $w('#startWorkoutButton').disable();
        }

        // Hide favorites
        if ($w('#favoriteButtons')) {
            $w('#favoriteButtons').hide();
        }

        // Hide user dashboard access (keep visible but show login prompt)
        if ($w('#dashboardButton')) {
            $w('#dashboardButton').onClick(() => {
                this.showAuthError('Please login to access your dashboard');
                if ($w('#loginModal')) {
                    $w('#loginModal').show();
                }
            });
        }
    }

    // Show loading state for auth operations
    showAuthLoading(isLoading) {
        if ($w('#authLoadingIcon')) {
            if (isLoading) {
                $w('#authLoadingIcon').show();
            } else {
                $w('#authLoadingIcon').hide();
            }
        }

        // Disable form buttons during loading
        const buttons = ['#loginButton', '#registerButton'];
        buttons.forEach(buttonId => {
            if ($w(buttonId)) {
                if (isLoading) {
                    $w(buttonId).disable();
                } else {
                    $w(buttonId).enable();
                }
            }
        });
    }

    // Show auth error messages
    showAuthError(message) {
        if ($w('#authErrorMessage')) {
            $w('#authErrorMessage').text = message;
            $w('#authErrorMessage').show();
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                $w('#authErrorMessage').hide();
            }, 5000);
        }
    }

    // Show auth success messages
    showAuthSuccess(message) {
        if ($w('#authSuccessMessage')) {
            $w('#authSuccessMessage').text = message;
            $w('#authSuccessMessage').show();
            
            // Auto-hide after 3 seconds
            setTimeout(() => {
                $w('#authSuccessMessage').hide();
            }, 3000);
        }
    }

    // Check if user is authenticated
    isAuthenticated() {
        return this.currentUser !== null && this.authToken !== null;
    }

    // Get current user
    getCurrentUser() {
        return this.currentUser;
    }

    // Get auth token for API calls
    getAuthToken() {
        return this.authToken;
    }

    // Make authenticated API call
    async authenticatedApiCall(endpoint, options = {}) {
        if (!this.isAuthenticated()) {
            throw new Error('User not authenticated');
        }

        const headers = {
            'Authorization': `Bearer ${this.authToken}`,
            'Content-Type': 'application/json',
            ...options.headers
        };

        return await fetch(`${this.apiBaseUrl}${endpoint}`, {
            ...options,
            headers
        });
    }
}

// Initialize authentication system
const authSystem = new FitFriendsAuth();

// Export for use in other files
export { 
    authSystem,
    FitFriendsAuth 
};

// Additional auth-related helper functions

// Require authentication for certain actions
function requireAuth(callback, errorMessage = 'Please login to continue') {
    return function(...args) {
        if (authSystem.isAuthenticated()) {
            return callback.apply(this, args);
        } else {
            authSystem.showAuthError(errorMessage);
            if ($w('#loginModal')) {
                $w('#loginModal').show();
            }
        }
    };
}

// Protected route handler
function protectedRoute(routeCallback) {
    if (authSystem.isAuthenticated()) {
        routeCallback();
    } else {
        // Redirect to login
        wixLocation.to('/');
        setTimeout(() => {
            if ($w('#loginModal')) {
                $w('#loginModal').show();
            }
        }, 100);
    }
}

export {
    requireAuth,
    protectedRoute
};