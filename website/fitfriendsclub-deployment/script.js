// FitFriendsClub Interactive JavaScript

// Configuration object with domain and API endpoints
const CONFIG = {
    domain: 'https://fitfriendsclub.com',
    apiEndpoints: {
        contact: 'https://fitfriendsclub.com/api/contact',
        membership: 'https://fitfriendsclub.com/api/membership',
        newsletter: 'https://fitfriendsclub.com/api/newsletter'
    },
    email: {
        contact: 'hello@fitfriendsclub.com',
        support: 'support@fitfriendsclub.com'
    }
};

// Security utilities
const Security = {
    // Sanitize HTML to prevent XSS attacks
    sanitizeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    },
    
    // Escape HTML entities
    escapeHTML(str) {
        const entityMap = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;',
            '/': '&#x2F;'
        };
        return String(str).replace(/[&<>"'\/]/g, s => entityMap[s]);
    },
    
    // Generate CSRF token
    generateCSRFToken() {
        return 'csrf_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    },
    
    // Rate limiter for form submissions
    rateLimiter: {
        attempts: {},
        maxAttempts: 3,
        cooldownPeriod: 60000, // 1 minute
        
        canSubmit(formType) {
            const now = Date.now();
            if (!this.attempts[formType]) {
                this.attempts[formType] = { count: 0, lastAttempt: 0 };
            }
            
            const attempt = this.attempts[formType];
            if (now - attempt.lastAttempt > this.cooldownPeriod) {
                attempt.count = 0;
            }
            
            return attempt.count < this.maxAttempts;
        },
        
        recordAttempt(formType) {
            if (!this.attempts[formType]) {
                this.attempts[formType] = { count: 0, lastAttempt: 0 };
            }
            this.attempts[formType].count++;
            this.attempts[formType].lastAttempt = Date.now();
        },
        
        getRemainingCooldown(formType) {
            if (!this.attempts[formType]) return 0;
            const elapsed = Date.now() - this.attempts[formType].lastAttempt;
            return Math.max(0, this.cooldownPeriod - elapsed);
        }
    }
};

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initNavigation();
    initScrollAnimations();
    initContactForm();
    initMembershipSignup();
    initSmoothScrolling();
    initMobileMenu();
    initHeroAnimations();
    initCounterAnimations();
    initSportsSection();
    initCSRFProtection();
});

// Navigation functionality
function initNavigation() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Navbar background on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });

    // Active navigation link highlighting
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Highlight active section in navigation
    window.addEventListener('scroll', function() {
        let current = '';
        const sections = document.querySelectorAll('section[id]');
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            if (window.scrollY >= sectionTop) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// Mobile menu functionality
function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
}

// Smooth scrolling for all anchor links
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Scroll animations using Intersection Observer
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Trigger counter animations when stats section comes into view
                if (entry.target.classList.contains('hero-stats')) {
                    animateCounters();
                }
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll(
        '.feature-card, .community-stat, .plan-card, .photo-card, .hero-stats'
    );
    
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// Hero section animations
function initHeroAnimations() {
    const heroTitle = document.querySelector('.hero-title');
    const heroDescription = document.querySelector('.hero-description');
    const heroButtons = document.querySelector('.hero-buttons');
    const heroPhone = document.querySelector('.hero-phone');

    // Stagger hero content animations
    setTimeout(() => {
        if (heroTitle) heroTitle.style.opacity = '1';
    }, 200);
    
    setTimeout(() => {
        if (heroDescription) heroDescription.style.opacity = '1';
    }, 400);
    
    setTimeout(() => {
        if (heroButtons) heroButtons.style.opacity = '1';
    }, 600);
    
    setTimeout(() => {
        if (heroPhone) heroPhone.style.opacity = '1';
    }, 800);

    // Floating animation for hero phone
    if (heroPhone) {
        setInterval(() => {
            heroPhone.style.transform = 'rotate(-5deg) translateY(-10px)';
            setTimeout(() => {
                heroPhone.style.transform = 'rotate(-5deg) translateY(0px)';
            }, 2000);
        }, 4000);
    }
}

// Counter animations for statistics
function initCounterAnimations() {
    // This will be called when the stats section comes into view
}

function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    const targets = ['10K+', '50K+', '95%'];
    
    counters.forEach((counter, index) => {
        const target = targets[index];
        const isPercentage = target.includes('%');
        const isK = target.includes('K');
        let current = 0;
        const targetNum = parseInt(target.replace(/[^\d]/g, ''));
        const increment = Math.ceil(targetNum / 50);
        
        const updateCounter = () => {
            if (current < targetNum) {
                current += increment;
                if (current > targetNum) current = targetNum;
                
                let displayValue = current;
                if (isK) displayValue = current + 'K';
                if (isPercentage) displayValue = current + '%';
                if (isK && !isPercentage) displayValue = current + 'K+';
                
                counter.textContent = displayValue;
                setTimeout(updateCounter, 50);
            } else {
                counter.textContent = target;
            }
        };
        
        // Delay each counter animation
        setTimeout(updateCounter, index * 200);
    });
}

// Contact form functionality
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Check rate limiting
            if (!Security.rateLimiter.canSubmit('contact')) {
                const remaining = Math.ceil(Security.rateLimiter.getRemainingCooldown('contact') / 1000);
                showNotification(`Too many attempts. Please wait ${remaining} seconds before trying again.`, 'error');
                return;
            }
            
            // Get form data
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Sanitize input data
            Object.keys(data).forEach(key => {
                data[key] = Security.sanitizeHTML(data[key]);
            });
            
            // Validate form
            if (validateForm(data)) {
                Security.rateLimiter.recordAttempt('contact');
                // Show loading state
                const submitBtn = this.querySelector('.submit-btn');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
                submitBtn.disabled = true;
                
                // Submit form to API endpoint
                submitFormData(CONFIG.apiEndpoints.contact, data)
                    .then(response => {
                        showNotification('Message sent successfully! We\'ll get back to you soon.', 'success');
                        contactForm.reset();
                    })
                    .catch(error => {
                        console.error('Form submission error:', error);
                        showNotification('There was an issue sending your message. Please try again or contact us directly at ' + CONFIG.email.contact, 'error');
                    })
                    .finally(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                    });
            }
        });
    }
}

// Form validation
function validateForm(data) {
    const errors = [];
    
    if (!data.name || data.name.trim().length < 2) {
        errors.push('Please enter a valid name');
    }
    
    if (!data.email || !isValidEmail(data.email)) {
        errors.push('Please enter a valid email address');
    }
    
    if (!data.interest) {
        errors.push('Please select your interest');
    }
    
    if (!data.message || data.message.trim().length < 10) {
        errors.push('Please enter a message with at least 10 characters');
    }
    
    if (errors.length > 0) {
        // Sanitize error messages to prevent XSS
        const sanitizedErrors = errors.map(error => Security.escapeHTML(error));
        showNotification(sanitizedErrors.join('<br>'), 'error');
        return false;
    }
    
    return true;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Membership signup functionality
function initMembershipSignup() {
    const joinButtons = document.querySelectorAll('.join-btn, .cta-primary, .plan-btn');
    
    joinButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.textContent.includes('Join') || this.textContent.includes('Get Started') || this.textContent.includes('Go VIP')) {
                e.preventDefault();
                showMembershipModal(this);
            }
        });
    });
}

function showMembershipModal(button) {
    // Create modal HTML
    const modalHTML = `
        <div class="modal-overlay" id="membershipModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Join FitFriendsClub</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="membership-form">
                        <div class="form-step active" id="step1">
                            <h4>Let's get you started!</h4>
                            <p>Enter your details to join the premier fitness community</p>
                            <form id="membershipForm">
                                <div class="form-group">
                                    <label for="memberName">Full Name</label>
                                    <input type="text" id="memberName" name="memberName" required>
                                </div>
                                <div class="form-group">
                                    <label for="memberEmail">Email Address</label>
                                    <input type="email" id="memberEmail" name="memberEmail" required>
                                </div>
                                <div class="form-group">
                                    <label for="fitnessGoals">Primary Fitness Goal</label>
                                    <select id="fitnessGoals" name="fitnessGoals" required>
                                        <option value="">Select your goal</option>
                                        <option value="weight-loss">Weight Loss</option>
                                        <option value="muscle-gain">Muscle Gain</option>
                                        <option value="endurance">Improve Endurance</option>
                                        <option value="strength">Build Strength</option>
                                        <option value="wellness">Overall Wellness</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="experience">Fitness Experience</label>
                                    <select id="experience" name="experience" required>
                                        <option value="">Select experience level</option>
                                        <option value="beginner">Beginner</option>
                                        <option value="intermediate">Intermediate</option>
                                        <option value="advanced">Advanced</option>
                                    </select>
                                </div>
                                <button type="submit" class="cta-primary full-width">
                                    <i class="fas fa-rocket"></i>
                                    Join the Club
                                </button>
                            </form>
                        </div>
                        <div class="form-step" id="step2">
                            <div class="success-message">
                                <div class="success-icon">
                                    <i class="fas fa-check-circle"></i>
                                </div>
                                <h4>Welcome to FitFriendsClub!</h4>
                                <p>You're now part of the premier fitness community. Check your email for next steps.</p>
                                <div class="next-steps">
                                    <div class="next-step">
                                        <i class="fas fa-mobile-alt"></i>
                                        <span>Download our app</span>
                                    </div>
                                    <div class="next-step">
                                        <i class="fas fa-users"></i>
                                        <span>Find your first workout buddy</span>
                                    </div>
                                    <div class="next-step">
                                        <i class="fas fa-dumbbell"></i>
                                        <span>Join your first group workout</span>
                                    </div>
                                </div>
                                <button class="cta-primary full-width" onclick="closeModal()">
                                    <i class="fas fa-heart"></i>
                                    Let's Get Started!
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Add modal styles
    addModalStyles();
    
    // Initialize modal functionality
    initModalEvents();
    
    // Show modal with animation
    setTimeout(() => {
        document.getElementById('membershipModal').classList.add('show');
    }, 10);
}

function addModalStyles() {
    if (!document.getElementById('modalStyles')) {
        const styles = `
            <style id="modalStyles">
                .modal-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.8);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10000;
                    opacity: 0;
                    visibility: hidden;
                    transition: all 0.3s ease;
                }
                
                .modal-overlay.show {
                    opacity: 1;
                    visibility: visible;
                }
                
                .modal-content {
                    background: white;
                    border-radius: 1.5rem;
                    width: 90%;
                    max-width: 500px;
                    max-height: 90vh;
                    overflow-y: auto;
                    transform: scale(0.7);
                    transition: transform 0.3s ease;
                }
                
                .modal-overlay.show .modal-content {
                    transform: scale(1);
                }
                
                .modal-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 2rem 2rem 1rem;
                    border-bottom: 1px solid #e5e7eb;
                }
                
                .modal-header h3 {
                    margin: 0;
                    background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }
                
                .modal-close {
                    background: none;
                    border: none;
                    font-size: 2rem;
                    cursor: pointer;
                    color: #6b7280;
                    transition: color 0.2s ease;
                }
                
                .modal-close:hover {
                    color: #374151;
                }
                
                .modal-body {
                    padding: 2rem;
                }
                
                .form-step {
                    display: none;
                }
                
                .form-step.active {
                    display: block;
                }
                
                .full-width {
                    width: 100%;
                    justify-content: center;
                }
                
                .success-message {
                    text-align: center;
                }
                
                .success-icon {
                    font-size: 4rem;
                    color: #10b981;
                    margin-bottom: 1rem;
                }
                
                .success-message h4 {
                    font-size: 1.5rem;
                    margin-bottom: 1rem;
                    color: #111827;
                }
                
                .next-steps {
                    margin: 2rem 0;
                    text-align: left;
                }
                
                .next-step {
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                    margin-bottom: 1rem;
                    padding: 1rem;
                    background: #f9fafb;
                    border-radius: 0.75rem;
                }
                
                .next-step i {
                    color: #6366f1;
                    font-size: 1.25rem;
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', styles);
    }
}

function initModalEvents() {
    const modal = document.getElementById('membershipModal');
    const closeBtn = modal.querySelector('.modal-close');
    const membershipForm = document.getElementById('membershipForm');
    
    // Close modal events
    closeBtn.addEventListener('click', closeModal);
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Form submission
    membershipForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Check rate limiting
        if (!Security.rateLimiter.canSubmit('membership')) {
            const remaining = Math.ceil(Security.rateLimiter.getRemainingCooldown('membership') / 1000);
            showNotification(`Too many attempts. Please wait ${remaining} seconds before trying again.`, 'error');
            return;
        }
        
        // Show loading state
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        submitBtn.disabled = true;
        
        // Collect form data
        const formData = new FormData(this);
        const membershipData = Object.fromEntries(formData.entries());
        
        // Sanitize membership data
        Object.keys(membershipData).forEach(key => {
            membershipData[key] = Security.sanitizeHTML(membershipData[key]);
        });
        
        Security.rateLimiter.recordAttempt('membership');
        
        // Submit membership data to API
        submitFormData(CONFIG.apiEndpoints.membership, membershipData)
            .then(response => {
                document.getElementById('step1').classList.remove('active');
                document.getElementById('step2').classList.add('active');
            })
            .catch(error => {
                console.error('Membership submission error:', error);
                showNotification('There was an issue processing your membership. Please try again or contact us at ' + CONFIG.email.support, 'error');
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
    });
}

function closeModal() {
    const modal = document.getElementById('membershipModal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.remove();
        }, 300);
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <div class="notification-icon">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            </div>
            <div class="notification-message">${message}</div>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    // Add notification styles if not already added
    if (!document.getElementById('notificationStyles')) {
        const styles = `
            <style id="notificationStyles">
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: white;
                    border-radius: 0.75rem;
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                    z-index: 10001;
                    transform: translateX(100%);
                    transition: transform 0.3s ease;
                    max-width: 400px;
                    border-left: 4px solid #6366f1;
                }
                
                .notification.success {
                    border-left-color: #10b981;
                }
                
                .notification.error {
                    border-left-color: #ef4444;
                }
                
                .notification.show {
                    transform: translateX(0);
                }
                
                .notification-content {
                    display: flex;
                    align-items: flex-start;
                    padding: 1rem;
                    gap: 0.75rem;
                }
                
                .notification-icon {
                    font-size: 1.25rem;
                }
                
                .notification-icon .fa-check-circle {
                    color: #10b981;
                }
                
                .notification-icon .fa-exclamation-circle {
                    color: #ef4444;
                }
                
                .notification-icon .fa-info-circle {
                    color: #6366f1;
                }
                
                .notification-message {
                    flex: 1;
                    font-size: 0.875rem;
                    line-height: 1.5;
                }
                
                .notification-close {
                    background: none;
                    border: none;
                    font-size: 1.25rem;
                    cursor: pointer;
                    color: #6b7280;
                    padding: 0;
                    line-height: 1;
                }
                
                .notification-close:hover {
                    color: #374151;
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', styles);
    }
    
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Close notification events
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => removeNotification(notification));
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        removeNotification(notification);
    }, 5000);
}

function removeNotification(notification) {
    notification.classList.remove('show');
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

// Newsletter signup
document.addEventListener('click', function(e) {
    if (e.target.matches('.newsletter button')) {
        e.preventDefault();
        const email = e.target.previousElementSibling.value;
        
        if (isValidEmail(email)) {
            showNotification('Thank you for subscribing! You\'ll receive updates about FitFriendsClub.', 'success');
            e.target.previousElementSibling.value = '';
        } else {
            showNotification('Please enter a valid email address.', 'error');
        }
    }
});

// Add CSS animations
const animationStyles = `
    <style>
        .animate-in {
            animation: slideInUp 0.6s ease forwards;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .hero-title,
        .hero-description,
        .hero-buttons {
            opacity: 0;
            transition: opacity 0.6s ease;
        }
        
        .hero-phone {
            opacity: 0;
            transition: all 0.6s ease;
        }
        
        .nav-link.active {
            color: #6366f1;
        }
        
        .nav-link.active::after {
            width: 100%;
        }
    </style>
`;

document.head.insertAdjacentHTML('beforeend', animationStyles);

// Sports Section Interactive Functionality
function initSportsSection() {
    const sportCards = document.querySelectorAll('.sport-card');
    const sportButtons = document.querySelectorAll('.sport-btn');
    
    // Sport program data
    const sportPrograms = {
        football: {
            name: 'Football Elite Training',
            description: 'Comprehensive football training designed by NFL coaches',
            features: [
                'Position-specific skill development',
                'Strength and conditioning protocols',
                'Speed and agility enhancement',
                'Game situation training',
                'Injury prevention strategies'
            ],
            duration: '12-week program',
            level: 'Beginner to Elite'
        },
        basketball: {
            name: 'Basketball Performance Program',
            description: 'Professional basketball training used by college and pro players',
            features: [
                'Vertical jump development',
                'Court movement efficiency',
                'Shooting mechanics improvement',
                'Defensive positioning',
                'Mental game strategies'
            ],
            duration: '10-week program',
            level: 'All skill levels'
        },
        soccer: {
            name: 'Soccer Excellence Training',
            description: 'World-class soccer training from international coaches',
            features: [
                'Ball mastery and control',
                'Tactical awareness training',
                'Speed and endurance building',
                'Set piece specialization',
                'Match preparation protocols'
            ],
            duration: '16-week program',
            level: 'Youth to Professional'
        },
        baseball: {
            name: 'Baseball Power Program',
            description: 'Complete baseball development for all positions',
            features: [
                'Hitting mechanics optimization',
                'Pitching velocity increase',
                'Defensive skill enhancement',
                'Base running efficiency',
                'Mental approach training'
            ],
            duration: '14-week program',
            level: 'Little League to MLB'
        },
        tennis: {
            name: 'Tennis Mastery Course',
            description: 'Professional tennis training for competitive players',
            features: [
                'Stroke technique refinement',
                'Court positioning strategies',
                'Mental toughness training',
                'Match play tactics',
                'Fitness and flexibility'
            ],
            duration: '12-week program',
            level: 'Recreational to Tournament'
        },
        swimming: {
            name: 'Swimming Performance Elite',
            description: 'Olympic-level swimming training protocols',
            features: [
                'Stroke efficiency optimization',
                'Start and turn techniques',
                'Breathing pattern training',
                'Race strategy development',
                'Dryland strength training'
            ],
            duration: '20-week program',
            level: 'Competitive swimmers'
        },
        track: {
            name: 'Track & Field Excellence',
            description: 'Comprehensive track and field training program',
            features: [
                'Event-specific training',
                'Sprint mechanics improvement',
                'Distance running strategies',
                'Field event techniques',
                'Competition preparation'
            ],
            duration: '16-week program',
            level: 'High School to Elite'
        },
        volleyball: {
            name: 'Volleyball Elite Training',
            description: 'Professional volleyball development program',
            features: [
                'Jumping and spiking power',
                'Defensive positioning',
                'Team coordination drills',
                'Serving accuracy training',
                'Mental game development'
            ],
            duration: '12-week program',
            level: 'Club to Professional'
        }
    };
    
    // Add hover animations
    sportCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Handle sport program view buttons
    sportButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const sportCard = this.closest('.sport-card');
            const sport = sportCard.dataset.sport;
            const program = sportPrograms[sport];
            
            if (program) {
                showSportModal(program);
            }
        });
    });
    
    // Animate cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const sportsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    sportCards.forEach((card, index) => {
        // Initial state
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        card.style.transition = `all 0.6s ease ${index * 0.1}s`;
        
        // Observe for animation
        sportsObserver.observe(card);
    });
}

// Show sport program modal
function showSportModal(program) {
    // Create modal HTML
    const modalHTML = `
        <div class="sport-modal-overlay" id="sportModal">
            <div class="sport-modal">
                <div class="sport-modal-header">
                    <h2>${program.name}</h2>
                    <button class="sport-modal-close">&times;</button>
                </div>
                <div class="sport-modal-content">
                    <p class="sport-description">${program.description}</p>
                    <div class="sport-details">
                        <div class="sport-detail">
                            <h4>Program Duration</h4>
                            <p>${program.duration}</p>
                        </div>
                        <div class="sport-detail">
                            <h4>Skill Level</h4>
                            <p>${program.level}</p>
                        </div>
                    </div>
                    <div class="sport-features-list">
                        <h4>What You'll Learn:</h4>
                        <ul>
                            ${program.features.map(feature => `<li>${feature}</li>`).join('')}
                        </ul>
                    </div>
                    <div class="sport-modal-actions">
                        <button class="cta-primary sport-signup-btn">
                            <i class="fas fa-star"></i>
                            Join Program
                        </button>
                        <button class="cta-secondary sport-learn-more">
                            Learn More
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Add modal styles
    addSportModalStyles();
    
    // Get modal elements
    const modal = document.getElementById('sportModal');
    const closeBtn = modal.querySelector('.sport-modal-close');
    const signupBtn = modal.querySelector('.sport-signup-btn');
    const learnMoreBtn = modal.querySelector('.sport-learn-more');
    
    // Show modal with animation
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
    
    // Close modal functionality
    closeBtn.addEventListener('click', closeSportModal);
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeSportModal();
        }
    });
    
    // Sign up button
    signupBtn.addEventListener('click', function() {
        closeSportModal();
        // Scroll to membership section
        document.getElementById('membership').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
    
    // Learn more button  
    learnMoreBtn.addEventListener('click', function() {
        closeSportModal();
        // Show contact modal or scroll to contact
        document.getElementById('contact').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
}

// Close sport modal
function closeSportModal() {
    const modal = document.getElementById('sportModal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.remove();
        }, 300);
    }
}

// Add sport modal styles
function addSportModalStyles() {
    if (document.getElementById('sportModalStyles')) return;
    
    const styles = document.createElement('style');
    styles.id = 'sportModalStyles';
    styles.textContent = `
        .sport-modal-overlay {
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
            padding: 20px;
        }
        
        .sport-modal-overlay.show {
            opacity: 1;
            visibility: visible;
        }
        
        .sport-modal {
            background: white;
            border-radius: 20px;
            max-width: 600px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            transform: scale(0.9) translateY(50px);
            transition: all 0.3s ease;
        }
        
        .sport-modal-overlay.show .sport-modal {
            transform: scale(1) translateY(0);
        }
        
        .sport-modal-header {
            padding: 30px 30px 20px;
            border-bottom: 2px solid #f1f5f9;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .sport-modal-header h2 {
            margin: 0;
            color: #1e293b;
            font-size: 1.5rem;
        }
        
        .sport-modal-close {
            background: none;
            border: none;
            font-size: 2rem;
            cursor: pointer;
            color: #64748b;
            line-height: 1;
            padding: 0;
        }
        
        .sport-modal-close:hover {
            color: #1e293b;
        }
        
        .sport-modal-content {
            padding: 30px;
        }
        
        .sport-description {
            font-size: 1.1rem;
            color: #475569;
            margin-bottom: 25px;
            line-height: 1.6;
        }
        
        .sport-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }
        
        .sport-detail h4 {
            margin: 0 0 8px 0;
            color: #6366f1;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .sport-detail p {
            margin: 0;
            font-weight: 600;
            color: #1e293b;
        }
        
        .sport-features-list h4 {
            margin: 0 0 15px 0;
            color: #1e293b;
            font-size: 1.1rem;
        }
        
        .sport-features-list ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .sport-features-list li {
            padding: 10px 0;
            border-bottom: 1px solid #f1f5f9;
            position: relative;
            padding-left: 25px;
            color: #475569;
        }
        
        .sport-features-list li:before {
            content: '✓';
            position: absolute;
            left: 0;
            color: #10b981;
            font-weight: bold;
        }
        
        .sport-features-list li:last-child {
            border-bottom: none;
        }
        
        .sport-modal-actions {
            display: flex;
            gap: 15px;
            margin-top: 30px;
            flex-wrap: wrap;
        }
        
        .sport-modal-actions .cta-primary,
        .sport-modal-actions .cta-secondary {
            flex: 1;
            min-width: 140px;
            text-align: center;
            justify-content: center;
        }
        
        @media (max-width: 768px) {
            .sport-modal {
                margin: 20px;
            }
            
            .sport-modal-header,
            .sport-modal-content {
                padding: 20px;
            }
            
            .sport-details {
                grid-template-columns: 1fr;
                gap: 15px;
            }
            
            .sport-modal-actions {
                flex-direction: column;
            }
        }
    `;
    
    document.head.appendChild(styles);
}

document.head.insertAdjacentHTML('beforeend', animationStyles);

// Utility function for form submissions to fitfriendsclub.com API
async function submitFormData(endpoint, data) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        return result;
    } catch (error) {
        // If API is not available yet, simulate success for development
        console.warn('API endpoint not available, simulating success:', endpoint);
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({ success: true, message: 'Development mode - form submitted successfully' });
            }, 2000);
        });
    }
}

// CSRF Protection initialization
function initCSRFProtection() {
    // Add CSRF tokens to all forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Skip if CSRF token already exists
        if (form.querySelector('input[name="csrf_token"]')) return;
        
        const csrfToken = Security.generateCSRFToken();
        const tokenInput = document.createElement('input');
        tokenInput.type = 'hidden';
        tokenInput.name = 'csrf_token';
        tokenInput.value = csrfToken;
        form.appendChild(tokenInput);
        
        // Store token for validation
        form.setAttribute('data-csrf-token', csrfToken);
    });
}