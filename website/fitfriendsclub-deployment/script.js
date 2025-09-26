// FitFriendsClub Interactive JavaScript

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
            
            // Get form data
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Validate form
            if (validateForm(data)) {
                // Show loading state
                const submitBtn = this.querySelector('.submit-btn');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
                submitBtn.disabled = true;
                
                // Simulate form submission (replace with actual API call)
                setTimeout(() => {
                    showNotification('Message sent successfully! We\'ll get back to you soon.', 'success');
                    contactForm.reset();
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 2000);
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
        showNotification(errors.join('<br>'), 'error');
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
        
        // Show loading state
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        submitBtn.disabled = true;
        
        // Simulate processing
        setTimeout(() => {
            document.getElementById('step1').classList.remove('active');
            document.getElementById('step2').classList.add('active');
        }, 2000);
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