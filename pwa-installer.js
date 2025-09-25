/**
 * 📲 PWA Installation Manager
 * Smart prompts and installation handling for Khyrie mobile app
 */

class PWAInstallationManager {
    constructor() {
        this.deferredPrompt = null;
        this.isInstalled = false;
        this.installPromptShown = false;
        this.userDismissedCount = 0;
        this.maxDismissals = 3;
        
        this.init();
    }
    
    /**
     * Initialize PWA installation features
     */
    init() {
        // Check if app is already installed
        this.checkInstallationStatus();
        
        // Listen for installation events
        this.setupInstallationListeners();
        
        // Create installation UI
        this.createInstallationPrompts();
        
        // Smart timing for install prompts
        this.setupSmartPrompting();
        
        console.log('📱 PWA Installation Manager initialized');
    }
    
    /**
     * Check current installation status
     */
    checkInstallationStatus() {
        // Check if running as installed PWA
        if (window.matchMedia('(display-mode: standalone)').matches) {
            this.isInstalled = true;
            console.log('✅ App is running as installed PWA');
            return;
        }
        
        // Check if running in iOS Safari with PWA meta tag
        if (window.navigator.standalone === true) {
            this.isInstalled = true;
            console.log('✅ App is running as iOS PWA');
            return;
        }
        
        // Check localStorage for previous installation
        const installStatus = localStorage.getItem('khyrie-pwa-installed');
        if (installStatus === 'true') {
            this.isInstalled = true;
        }
        
        // Get dismissal count from localStorage
        this.userDismissedCount = parseInt(localStorage.getItem('khyrie-install-dismissed') || '0');
    }
    
    /**
     * Setup installation event listeners
     */
    setupInstallationListeners() {
        // Listen for beforeinstallprompt event (Android/Chrome)
        window.addEventListener('beforeinstallprompt', (e) => {
            console.log('📥 Install prompt available');
            
            // Prevent automatic prompt
            e.preventDefault();
            
            // Store the event for later use
            this.deferredPrompt = e;
            
            // Show our custom install prompt
            this.showCustomInstallPrompt();
        });
        
        // Listen for app installation
        window.addEventListener('appinstalled', (e) => {
            console.log('🎉 PWA was installed successfully');
            
            this.isInstalled = true;
            localStorage.setItem('khyrie-pwa-installed', 'true');
            
            // Hide install prompts
            this.hideInstallPrompts();
            
            // Show success message
            this.showInstallSuccessMessage();
            
            // Track installation event
            this.trackInstallationEvent('installed');
        });
        
        // Listen for display mode changes
        window.matchMedia('(display-mode: standalone)').addEventListener('change', (e) => {
            if (e.matches) {
                this.isInstalled = true;
                localStorage.setItem('khyrie-pwa-installed', 'true');
                this.hideInstallPrompts();
            }
        });
    }
    
    /**
     * Create installation prompt UI elements
     */
    createInstallationPrompts() {
        // Create install banner
        this.createInstallBanner();
        
        // Create floating install button
        this.createFloatingInstallButton();
        
        // Create bottom sheet install prompt
        this.createBottomSheetPrompt();
        
        // Create iOS install instructions
        this.createIOSInstructions();
    }
    
    /**
     * Create install banner at top of page
     */
    createInstallBanner() {
        const banner = document.createElement('div');
        banner.id = 'pwa-install-banner';
        banner.className = 'pwa-install-banner';
        banner.innerHTML = `
            <div class="install-banner-content">
                <div class="install-banner-icon">📱</div>
                <div class="install-banner-text">
                    <div class="install-banner-title">Install Khyrie App</div>
                    <div class="install-banner-subtitle">Get the full mobile experience</div>
                </div>
                <div class="install-banner-actions">
                    <button class="install-btn-primary" onclick="pwaInstaller.triggerInstall()">
                        Install
                    </button>
                    <button class="install-btn-close" onclick="pwaInstaller.dismissBanner()">
                        ✕
                    </button>
                </div>
            </div>
        `;
        
        // Add CSS styles
        const bannerStyles = `
            .pwa-install-banner {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 16px;
                z-index: 10000;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                transform: translateY(-100%);
                transition: transform 0.3s ease;
            }
            
            .pwa-install-banner.show {
                transform: translateY(0);
            }
            
            .install-banner-content {
                display: flex;
                align-items: center;
                gap: 12px;
                max-width: 400px;
                margin: 0 auto;
            }
            
            .install-banner-icon {
                font-size: 24px;
            }
            
            .install-banner-text {
                flex: 1;
            }
            
            .install-banner-title {
                font-weight: 600;
                font-size: 14px;
                line-height: 1.2;
            }
            
            .install-banner-subtitle {
                font-size: 12px;
                opacity: 0.9;
                line-height: 1.2;
            }
            
            .install-banner-actions {
                display: flex;
                gap: 8px;
                align-items: center;
            }
            
            .install-btn-primary {
                background: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.3);
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .install-btn-primary:hover {
                background: rgba(255,255,255,0.3);
            }
            
            .install-btn-close {
                background: none;
                border: none;
                color: white;
                font-size: 16px;
                cursor: pointer;
                padding: 4px;
                opacity: 0.8;
            }
            
            .install-btn-close:hover {
                opacity: 1;
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = bannerStyles;
        document.head.appendChild(styleSheet);
        
        document.body.prepend(banner);
    }
    
    /**
     * Create floating install button
     */
    createFloatingInstallButton() {
        const floatingBtn = document.createElement('div');
        floatingBtn.id = 'pwa-floating-install';
        floatingBtn.className = 'pwa-floating-install';
        floatingBtn.innerHTML = `
            <button class="floating-install-btn" onclick="pwaInstaller.showBottomSheet()">
                <span class="floating-install-icon">⬇️</span>
                <span class="floating-install-text">Install App</span>
            </button>
        `;
        
        const floatingStyles = `
            .pwa-floating-install {
                position: fixed;
                bottom: 100px;
                right: 20px;
                z-index: 9999;
                opacity: 0;
                transform: translateY(20px) scale(0.9);
                transition: all 0.3s ease;
            }
            
            .pwa-floating-install.show {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
            
            .floating-install-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 16px;
                border-radius: 25px;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.2s ease;
            }
            
            .floating-install-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
            }
            
            .floating-install-icon {
                font-size: 16px;
            }
            
            .floating-install-text {
                font-size: 14px;
            }
        `;
        
        const floatingStyleSheet = document.createElement('style');
        floatingStyleSheet.textContent = floatingStyles;
        document.head.appendChild(floatingStyleSheet);
        
        document.body.appendChild(floatingBtn);
    }
    
    /**
     * Create bottom sheet install prompt
     */
    createBottomSheetPrompt() {
        const bottomSheet = document.createElement('div');
        bottomSheet.id = 'pwa-bottom-sheet';
        bottomSheet.className = 'pwa-bottom-sheet';
        bottomSheet.innerHTML = `
            <div class="bottom-sheet-backdrop" onclick="pwaInstaller.hideBottomSheet()"></div>
            <div class="bottom-sheet-content">
                <div class="bottom-sheet-header">
                    <div class="bottom-sheet-icon">🏋️‍♂️</div>
                    <h3 class="bottom-sheet-title">Install Khyrie App</h3>
                    <p class="bottom-sheet-subtitle">Get the full mobile experience with offline access, push notifications, and more!</p>
                </div>
                
                <div class="bottom-sheet-features">
                    <div class="feature-item">
                        <span class="feature-icon">📱</span>
                        <span class="feature-text">Native mobile experience</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">🔄</span>
                        <span class="feature-text">Works offline</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">🔔</span>
                        <span class="feature-text">Push notifications</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">📸</span>
                        <span class="feature-text">Camera integration</span>
                    </div>
                </div>
                
                <div class="bottom-sheet-actions">
                    <button class="bottom-sheet-btn-primary" onclick="pwaInstaller.triggerInstall()">
                        <span class="btn-icon">⬇️</span>
                        Install Now
                    </button>
                    <button class="bottom-sheet-btn-secondary" onclick="pwaInstaller.hideBottomSheet()">
                        Maybe Later
                    </button>
                </div>
            </div>
        `;
        
        const bottomSheetStyles = `
            .pwa-bottom-sheet {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: 15000;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
            }
            
            .pwa-bottom-sheet.show {
                opacity: 1;
                visibility: visible;
            }
            
            .bottom-sheet-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(4px);
            }
            
            .bottom-sheet-content {
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                background: white;
                border-radius: 20px 20px 0 0;
                padding: 24px;
                max-height: 80vh;
                overflow-y: auto;
                transform: translateY(100%);
                transition: transform 0.3s ease;
            }
            
            .pwa-bottom-sheet.show .bottom-sheet-content {
                transform: translateY(0);
            }
            
            .bottom-sheet-header {
                text-align: center;
                margin-bottom: 24px;
            }
            
            .bottom-sheet-icon {
                font-size: 48px;
                margin-bottom: 12px;
            }
            
            .bottom-sheet-title {
                margin: 0 0 8px 0;
                font-size: 24px;
                font-weight: 700;
                color: #1a202c;
            }
            
            .bottom-sheet-subtitle {
                margin: 0;
                color: #4a5568;
                font-size: 16px;
                line-height: 1.5;
            }
            
            .bottom-sheet-features {
                margin-bottom: 32px;
            }
            
            .feature-item {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 16px;
            }
            
            .feature-icon {
                font-size: 20px;
                width: 32px;
                text-align: center;
            }
            
            .feature-text {
                font-size: 16px;
                color: #2d3748;
                font-weight: 500;
            }
            
            .bottom-sheet-actions {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .bottom-sheet-btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 16px 24px;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                transition: all 0.2s ease;
            }
            
            .bottom-sheet-btn-primary:hover {
                transform: translateY(-1px);
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
            }
            
            .bottom-sheet-btn-secondary {
                background: transparent;
                color: #4a5568;
                border: 2px solid #e2e8f0;
                padding: 14px 24px;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .bottom-sheet-btn-secondary:hover {
                border-color: #cbd5e0;
                color: #2d3748;
            }
        `;
        
        const bottomSheetStyleSheet = document.createElement('style');
        bottomSheetStyleSheet.textContent = bottomSheetStyles;
        document.head.appendChild(bottomSheetStyleSheet);
        
        document.body.appendChild(bottomSheet);
    }
    
    /**
     * Create iOS installation instructions
     */
    createIOSInstructions() {
        const iosInstructions = document.createElement('div');
        iosInstructions.id = 'pwa-ios-instructions';
        iosInstructions.className = 'pwa-ios-instructions';
        iosInstructions.innerHTML = `
            <div class="ios-instructions-backdrop" onclick="pwaInstaller.hideIOSInstructions()"></div>
            <div class="ios-instructions-content">
                <div class="ios-instructions-header">
                    <h3 class="ios-instructions-title">Install Khyrie App</h3>
                    <p class="ios-instructions-subtitle">Follow these steps to install on your iPhone:</p>
                </div>
                
                <div class="ios-instructions-steps">
                    <div class="ios-step">
                        <div class="ios-step-number">1</div>
                        <div class="ios-step-content">
                            <div class="ios-step-text">Tap the Share button</div>
                            <div class="ios-step-icon">📤</div>
                        </div>
                    </div>
                    
                    <div class="ios-step">
                        <div class="ios-step-number">2</div>
                        <div class="ios-step-content">
                            <div class="ios-step-text">Scroll down and tap "Add to Home Screen"</div>
                            <div class="ios-step-icon">➕</div>
                        </div>
                    </div>
                    
                    <div class="ios-step">
                        <div class="ios-step-number">3</div>
                        <div class="ios-step-content">
                            <div class="ios-step-text">Tap "Add" to install Khyrie</div>
                            <div class="ios-step-icon">✅</div>
                        </div>
                    </div>
                </div>
                
                <div class="ios-instructions-actions">
                    <button class="ios-instructions-btn" onclick="pwaInstaller.hideIOSInstructions()">
                        Got it!
                    </button>
                </div>
            </div>
        `;
        
        const iosStyles = `
            .pwa-ios-instructions {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: 15000;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
            }
            
            .pwa-ios-instructions.show {
                opacity: 1;
                visibility: visible;
            }
            
            .ios-instructions-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(4px);
            }
            
            .ios-instructions-content {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                border-radius: 16px;
                padding: 24px;
                max-width: 320px;
                width: 90%;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            }
            
            .ios-instructions-title {
                margin: 0 0 8px 0;
                font-size: 20px;
                font-weight: 700;
                text-align: center;
                color: #1a202c;
            }
            
            .ios-instructions-subtitle {
                margin: 0 0 24px 0;
                text-align: center;
                color: #4a5568;
                font-size: 14px;
            }
            
            .ios-step {
                display: flex;
                align-items: center;
                gap: 16px;
                margin-bottom: 20px;
            }
            
            .ios-step-number {
                width: 32px;
                height: 32px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                font-size: 14px;
                flex-shrink: 0;
            }
            
            .ios-step-content {
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .ios-step-text {
                color: #2d3748;
                font-size: 14px;
                font-weight: 500;
                line-height: 1.4;
            }
            
            .ios-step-icon {
                font-size: 20px;
            }
            
            .ios-instructions-btn {
                width: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 14px 24px;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                margin-top: 8px;
                transition: all 0.2s ease;
            }
            
            .ios-instructions-btn:hover {
                transform: translateY(-1px);
                box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
            }
        `;
        
        const iosStyleSheet = document.createElement('style');
        iosStyleSheet.textContent = iosStyles;
        document.head.appendChild(iosStyleSheet);
        
        document.body.appendChild(iosInstructions);
    }
    
    /**
     * Setup smart prompting based on user behavior
     */
    setupSmartPrompting() {
        // Don't show prompts if already installed or dismissed too many times
        if (this.isInstalled || this.userDismissedCount >= this.maxDismissals) {
            return;
        }
        
        // Show prompt after user engagement
        let engagementScore = 0;
        const engagementThreshold = 3;
        
        // Track page views
        engagementScore++;
        
        // Track time spent on site
        setTimeout(() => {
            engagementScore++;
            this.checkPromptConditions(engagementScore, engagementThreshold);
        }, 30000); // 30 seconds
        
        // Track interactions
        let interactionCount = 0;
        const trackInteraction = () => {
            interactionCount++;
            if (interactionCount >= 3) {
                engagementScore++;
                this.checkPromptConditions(engagementScore, engagementThreshold);
                // Remove listeners after threshold met
                document.removeEventListener('click', trackInteraction);
                document.removeEventListener('touchstart', trackInteraction);
            }
        };
        
        document.addEventListener('click', trackInteraction);
        document.addEventListener('touchstart', trackInteraction);
    }
    
    /**
     * Check if conditions are met to show install prompt
     */
    checkPromptConditions(engagementScore, threshold) {
        if (engagementScore >= threshold && !this.installPromptShown && !this.isInstalled) {
            // Detect platform and show appropriate prompt
            if (this.isIOS()) {
                this.showIOSInstructions();
            } else if (this.deferredPrompt) {
                this.showCustomInstallPrompt();
            } else {
                this.showFloatingButton();
            }
            
            this.installPromptShown = true;
        }
    }
    
    /**
     * Show custom install prompt
     */
    showCustomInstallPrompt() {
        const banner = document.getElementById('pwa-install-banner');
        if (banner && !this.isInstalled) {
            banner.classList.add('show');
            
            // Add top padding to body to account for banner
            document.body.style.paddingTop = '60px';
        }
    }
    
    /**
     * Show floating install button
     */
    showFloatingButton() {
        const floatingBtn = document.getElementById('pwa-floating-install');
        if (floatingBtn && !this.isInstalled) {
            floatingBtn.classList.add('show');
        }
    }
    
    /**
     * Show bottom sheet install prompt
     */
    showBottomSheet() {
        const bottomSheet = document.getElementById('pwa-bottom-sheet');
        if (bottomSheet) {
            bottomSheet.classList.add('show');
            
            // Prevent body scrolling
            document.body.style.overflow = 'hidden';
        }
    }
    
    /**
     * Hide bottom sheet
     */
    hideBottomSheet() {
        const bottomSheet = document.getElementById('pwa-bottom-sheet');
        if (bottomSheet) {
            bottomSheet.classList.remove('show');
            
            // Restore body scrolling
            document.body.style.overflow = '';
        }
    }
    
    /**
     * Show iOS installation instructions
     */
    showIOSInstructions() {
        const instructions = document.getElementById('pwa-ios-instructions');
        if (instructions) {
            instructions.classList.add('show');
            
            // Prevent body scrolling
            document.body.style.overflow = 'hidden';
        }
    }
    
    /**
     * Hide iOS instructions
     */
    hideIOSInstructions() {
        const instructions = document.getElementById('pwa-ios-instructions');
        if (instructions) {
            instructions.classList.remove('show');
            
            // Restore body scrolling
            document.body.style.overflow = '';
        }
    }
    
    /**
     * Trigger native install prompt
     */
    async triggerInstall() {
        if (!this.deferredPrompt) {
            // If no native prompt available, show instructions
            if (this.isIOS()) {
                this.showIOSInstructions();
            } else {
                // Show manual installation instructions for other browsers
                this.showBottomSheet();
            }
            return;
        }
        
        try {
            // Show native install prompt
            const result = await this.deferredPrompt.prompt();
            
            console.log(`Install prompt result: ${result.outcome}`);
            
            // Track the user's response
            this.trackInstallationEvent(result.outcome);
            
            if (result.outcome === 'accepted') {
                console.log('✅ User accepted the install prompt');
            } else {
                console.log('❌ User dismissed the install prompt');
                this.incrementDismissalCount();
            }
            
            // Clear the deferred prompt
            this.deferredPrompt = null;
            this.hideInstallPrompts();
            
        } catch (error) {
            console.error('❌ Error triggering install prompt:', error);
        }
    }
    
    /**
     * Dismiss install banner
     */
    dismissBanner() {
        const banner = document.getElementById('pwa-install-banner');
        if (banner) {
            banner.classList.remove('show');
            document.body.style.paddingTop = '';
        }
        
        this.incrementDismissalCount();
        this.trackInstallationEvent('dismissed');
    }
    
    /**
     * Hide all install prompts
     */
    hideInstallPrompts() {
        const banner = document.getElementById('pwa-install-banner');
        const floatingBtn = document.getElementById('pwa-floating-install');
        const bottomSheet = document.getElementById('pwa-bottom-sheet');
        
        if (banner) {
            banner.classList.remove('show');
            document.body.style.paddingTop = '';
        }
        
        if (floatingBtn) {
            floatingBtn.classList.remove('show');
        }
        
        if (bottomSheet) {
            bottomSheet.classList.remove('show');
        }
    }
    
    /**
     * Show installation success message
     */
    showInstallSuccessMessage() {
        const successMessage = document.createElement('div');
        successMessage.className = 'install-success-message';
        successMessage.innerHTML = `
            <div class="success-content">
                <div class="success-icon">🎉</div>
                <div class="success-text">
                    <div class="success-title">Khyrie App Installed!</div>
                    <div class="success-subtitle">You can now access it from your home screen</div>
                </div>
            </div>
        `;
        
        const successStyles = `
            .install-success-message {
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
                padding: 16px 20px;
                border-radius: 12px;
                box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
                z-index: 10000;
                animation: slideInSuccess 0.5s ease;
            }
            
            .success-content {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .success-icon {
                font-size: 24px;
            }
            
            .success-title {
                font-weight: 600;
                font-size: 14px;
            }
            
            .success-subtitle {
                font-size: 12px;
                opacity: 0.9;
            }
            
            @keyframes slideInSuccess {
                from {
                    transform: translate(-50%, -100%);
                    opacity: 0;
                }
                to {
                    transform: translate(-50%, 0);
                    opacity: 1;
                }
            }
        `;
        
        const successStyleSheet = document.createElement('style');
        successStyleSheet.textContent = successStyles;
        document.head.appendChild(successStyleSheet);
        
        document.body.appendChild(successMessage);
        
        // Remove success message after 5 seconds
        setTimeout(() => {
            successMessage.remove();
            successStyleSheet.remove();
        }, 5000);
    }
    
    /**
     * Increment dismissal count
     */
    incrementDismissalCount() {
        this.userDismissedCount++;
        localStorage.setItem('khyrie-install-dismissed', this.userDismissedCount.toString());
        
        // If user has dismissed too many times, don't show prompts for 30 days
        if (this.userDismissedCount >= this.maxDismissals) {
            const dismissDate = new Date();
            dismissDate.setDate(dismissDate.getDate() + 30);
            localStorage.setItem('khyrie-install-suppress-until', dismissDate.toISOString());
        }
    }
    
    /**
     * Check if running on iOS
     */
    isIOS() {
        const userAgent = window.navigator.userAgent;
        return /iPad|iPhone|iPod/.test(userAgent) || 
               (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    }
    
    /**
     * Track installation events for analytics
     */
    trackInstallationEvent(eventType) {
        // Track with your analytics service
        if (window.gtag) {
            window.gtag('event', 'pwa_install', {
                event_category: 'PWA',
                event_label: eventType,
                value: 1
            });
        }
        
        console.log(`📊 Install event tracked: ${eventType}`);
    }
}

// Initialize PWA Installation Manager
document.addEventListener('DOMContentLoaded', () => {
    window.pwaInstaller = new PWAInstallationManager();
});

console.log('📲 PWA Installation Manager loaded!');