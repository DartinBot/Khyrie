// Backend API Configuration
const API_BASE_URL = 'http://localhost:5000';

// API Helper Functions
class FitFriendsAPI {
    constructor() {
        this.token = localStorage.getItem('auth_token');
        this.user = JSON.parse(localStorage.getItem('user_data') || '{}');
    }

    // Set authentication headers
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        return headers;
    }

    // User Authentication
    async register(userData) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/register`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(userData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.token = data.token;
                this.user = data.user;
                localStorage.setItem('auth_token', this.token);
                localStorage.setItem('user_data', JSON.stringify(this.user));
                return { success: true, data };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error. Please try again.' };
        }
    }

    async login(credentials) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/login`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(credentials)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.token = data.token;
                this.user = data.user;
                localStorage.setItem('auth_token', this.token);
                localStorage.setItem('user_data', JSON.stringify(this.user));
                return { success: true, data };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error. Please try again.' };
        }
    }

    logout() {
        this.token = null;
        this.user = {};
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_data');
    }

    // User Profile
    async getProfile() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/profile`, {
                headers: this.getHeaders()
            });
            
            const data = await response.json();
            
            if (response.ok) {
                return { success: true, data: data.user };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error. Please try again.' };
        }
    }

    // Workouts
    async getWorkouts() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/workouts`, {
                headers: this.getHeaders()
            });
            
            const data = await response.json();
            
            if (response.ok) {
                return { success: true, data: data.workouts };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error. Please try again.' };
        }
    }

    async createWorkout(workoutData) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/workouts`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(workoutData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                return { success: true, data };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error. Please try again.' };
        }
    }

    // Group Workouts
    async getGroupWorkouts() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/group-workouts`, {
                headers: this.getHeaders()
            });
            
            const data = await response.json();
            
            if (response.ok) {
                return { success: true, data: data.group_workouts };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error. Please try again.' };
        }
    }

    async createGroupWorkout(workoutData) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/group-workouts`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(workoutData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                return { success: true, data };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error. Please try again.' };
        }
    }

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.token;
    }

    // Get current user
    getCurrentUser() {
        return this.user;
    }
}

// Initialize API instance
const api = new FitFriendsAPI();

// Enhanced Authentication UI Functions
function showAuthModal(type = 'login') {
    const modalHTML = `
        <div class="auth-modal-overlay" id="authModal">
            <div class="auth-modal-content">
                <div class="auth-modal-header">
                    <h3 id="authModalTitle">${type === 'login' ? 'Welcome Back!' : 'Join FitFriendsClub'}</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="auth-modal-body">
                    <div class="auth-tabs">
                        <button class="auth-tab ${type === 'login' ? 'active' : ''}" data-type="login">Login</button>
                        <button class="auth-tab ${type === 'register' ? 'active' : ''}" data-type="register">Sign Up</button>
                    </div>
                    
                    <form id="authForm" class="auth-form">
                        <div id="loginFields" style="display: ${type === 'login' ? 'block' : 'none'}">
                            <div class="form-group">
                                <label for="loginUsername">Username or Email</label>
                                <input type="text" id="loginUsername" name="username" required>
                            </div>
                            <div class="form-group">
                                <label for="loginPassword">Password</label>
                                <input type="password" id="loginPassword" name="password" required>
                            </div>
                            <button type="submit" class="cta-primary full-width auth-submit-btn">
                                <i class="fas fa-sign-in-alt"></i>
                                Sign In
                            </button>
                        </div>
                        
                        <div id="registerFields" style="display: ${type === 'register' ? 'block' : 'none'}">
                            <div class="form-group">
                                <label for="registerUsername">Username</label>
                                <input type="text" id="registerUsername" name="username" required>
                            </div>
                            <div class="form-group">
                                <label for="registerEmail">Email</label>
                                <input type="email" id="registerEmail" name="email" required>
                            </div>
                            <div class="form-group">
                                <label for="registerPassword">Password</label>
                                <input type="password" id="registerPassword" name="password" required>
                            </div>
                            <div class="form-group">
                                <label for="registerFullName">Full Name</label>
                                <input type="text" id="registerFullName" name="full_name" required>
                            </div>
                            <div class="form-group">
                                <label for="registerFitnessGoal">Fitness Goal</label>
                                <select id="registerFitnessGoal" name="fitness_goal" required>
                                    <option value="">Select your goal</option>
                                    <option value="weight-loss">Weight Loss</option>
                                    <option value="muscle-gain">Muscle Gain</option>
                                    <option value="endurance">Improve Endurance</option>
                                    <option value="strength">Build Strength</option>
                                    <option value="wellness">Overall Wellness</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="registerExperience">Experience Level</label>
                                <select id="registerExperience" name="experience_level" required>
                                    <option value="">Select experience</option>
                                    <option value="beginner">Beginner</option>
                                    <option value="intermediate">Intermediate</option>
                                    <option value="advanced">Advanced</option>
                                </select>
                            </div>
                            <button type="submit" class="cta-primary full-width auth-submit-btn">
                                <i class="fas fa-user-plus"></i>
                                Create Account
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Add modal styles
    addAuthModalStyles();
    
    // Initialize modal events
    initAuthModalEvents();
    
    // Show modal
    setTimeout(() => {
        document.getElementById('authModal').classList.add('show');
    }, 10);
}

function addAuthModalStyles() {
    if (document.getElementById('authModalStyles')) return;
    
    const styles = document.createElement('style');
    styles.id = 'authModalStyles';
    styles.textContent = `
        .auth-modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }
        
        .auth-modal-overlay.show {
            opacity: 1;
            visibility: visible;
        }
        
        .auth-modal-content {
            background: white;
            border-radius: 1.5rem;
            width: 90%;
            max-width: 450px;
            max-height: 90vh;
            overflow-y: auto;
            transform: scale(0.7);
            transition: transform 0.3s ease;
        }
        
        .auth-modal-overlay.show .auth-modal-content {
            transform: scale(1);
        }
        
        .auth-tabs {
            display: flex;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .auth-tab {
            flex: 1;
            padding: 1rem;
            border: none;
            background: none;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .auth-tab.active {
            background: #6366f1;
            color: white;
        }
        
        .auth-form {
            padding: 2rem;
        }
        
        .auth-submit-btn {
            margin-top: 1rem;
        }
    `;
    
    document.head.appendChild(styles);
}

function initAuthModalEvents() {
    const modal = document.getElementById('authModal');
    const closeBtn = modal.querySelector('.modal-close');
    const authForm = document.getElementById('authForm');
    const authTabs = document.querySelectorAll('.auth-tab');
    
    // Close modal
    closeBtn.addEventListener('click', closeAuthModal);
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeAuthModal();
        }
    });
    
    // Tab switching
    authTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const type = this.dataset.type;
            switchAuthTab(type);
        });
    });
    
    // Form submission
    authForm.addEventListener('submit', handleAuthSubmit);
}

function switchAuthTab(type) {
    const loginFields = document.getElementById('loginFields');
    const registerFields = document.getElementById('registerFields');
    const title = document.getElementById('authModalTitle');
    const tabs = document.querySelectorAll('.auth-tab');
    
    tabs.forEach(tab => {
        tab.classList.toggle('active', tab.dataset.type === type);
    });
    
    if (type === 'login') {
        loginFields.style.display = 'block';
        registerFields.style.display = 'none';
        title.textContent = 'Welcome Back!';
    } else {
        loginFields.style.display = 'none';
        registerFields.style.display = 'block';
        title.textContent = 'Join FitFriendsClub';
    }
}

async function handleAuthSubmit(e) {
    e.preventDefault();
    
    const submitBtn = e.target.querySelector('.auth-submit-btn');
    const originalText = submitBtn.innerHTML;
    const activeTab = document.querySelector('.auth-tab.active').dataset.type;
    
    // Show loading
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    submitBtn.disabled = true;
    
    try {
        let result;
        
        if (activeTab === 'login') {
            const formData = new FormData(e.target);
            const credentials = {
                username: formData.get('username'),
                password: formData.get('password')
            };
            
            result = await api.login(credentials);
        } else {
            const formData = new FormData(e.target);
            const userData = {
                username: formData.get('username'),
                email: formData.get('email'),
                password: formData.get('password'),
                full_name: formData.get('full_name'),
                fitness_goal: formData.get('fitness_goal'),
                experience_level: formData.get('experience_level')
            };
            
            result = await api.register(userData);
        }
        
        if (result.success) {
            showNotification(`${activeTab === 'login' ? 'Login' : 'Registration'} successful! Welcome to FitFriendsClub!`, 'success');
            closeAuthModal();
            updateUIForAuthenticatedUser();
        } else {
            showNotification(result.error, 'error');
        }
    } catch (error) {
        showNotification('Something went wrong. Please try again.', 'error');
    }
    
    // Restore button
    submitBtn.innerHTML = originalText;
    submitBtn.disabled = false;
}

function closeAuthModal() {
    const modal = document.getElementById('authModal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.remove();
        }, 300);
    }
}

function updateUIForAuthenticatedUser() {
    if (api.isAuthenticated()) {
        const user = api.getCurrentUser();
        
        // Update navigation
        const loginBtns = document.querySelectorAll('[onclick*="showAuthModal"]');
        loginBtns.forEach(btn => {
            btn.innerHTML = `<i class="fas fa-user"></i> ${user.full_name}`;
            btn.onclick = () => showUserMenu();
        });
        
        // Show authenticated content
        showNotification(`Welcome back, ${user.full_name}!`, 'success');
    }
}

function showUserMenu() {
    // Create user dropdown menu
    console.log('User menu clicked');
    // This can be expanded to show user dashboard, logout, etc.
}

// Initialize authentication state on page load
document.addEventListener('DOMContentLoaded', function() {
    updateUIForAuthenticatedUser();
});

// Export for global use
window.FitFriendsAPI = api;
window.showAuthModal = showAuthModal;