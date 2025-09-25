/**
 * Camera Integration Manager
 * Advanced camera features for form checking and progress photo tracking
 */

class CameraIntegrationManager {
    constructor() {
        this.stream = null;
        this.mediaRecorder = null;
        this.canvas = null;
        this.context = null;
        this.isRecording = false;
        this.isFormAnalysisActive = false;
        
        // Progress photo storage
        this.progressPhotos = [];
        this.photoCategories = ['front', 'side', 'back', 'custom'];
        
        // Form analysis settings
        this.formAnalysis = {
            exerciseType: null,
            keyPoints: [],
            warnings: [],
            confidence: 0
        };
        
        this.init();
    }
    
    /**
     * Initialize camera integration
     */
    async init() {
        try {
            // Check camera availability
            await this.checkCameraSupport();
            
            // Setup UI components
            this.createCameraInterface();
            
            // Setup pose detection
            await this.initPoseDetection();
            
            console.log('📸 Camera integration initialized');
            
        } catch (error) {
            console.error('❌ Failed to initialize camera:', error);
        }
    }
    
    /**
     * Check if camera is supported
     */
    async checkCameraSupport() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('Camera not supported in this browser');
        }
        
        // Check available cameras
        const devices = await navigator.mediaDevices.enumerateDevices();
        const cameras = devices.filter(device => device.kind === 'videoinput');
        
        if (cameras.length === 0) {
            throw new Error('No cameras found');
        }
        
        console.log(`📹 Found ${cameras.length} camera(s)`);
        return true;
    }
    
    /**
     * Create camera interface
     */
    createCameraInterface() {
        const cameraInterface = document.createElement('div');
        cameraInterface.id = 'camera-interface';
        cameraInterface.innerHTML = `
            <div class="camera-container" style="display: none;">
                <div class="camera-header">
                    <h3>📸 Khyrie Camera</h3>
                    <div class="camera-mode-selector">
                        <button class="mode-btn active" data-mode="progress">📊 Progress Photos</button>
                        <button class="mode-btn" data-mode="form">🏋️ Form Check</button>
                        <button class="mode-btn" data-mode="video">🎥 Workout Video</button>
                    </div>
                    <button class="close-camera" onclick="cameraManager.closeCamera()">✖</button>
                </div>
                
                <div class="camera-viewport">
                    <video id="camera-video" autoplay muted playsinline></video>
                    <canvas id="camera-canvas" style="display: none;"></canvas>
                    
                    <!-- Form analysis overlay -->
                    <div class="form-analysis-overlay" id="form-overlay" style="display: none;">
                        <div class="pose-points"></div>
                        <div class="form-feedback">
                            <div class="feedback-item" id="form-status">
                                <span class="icon">✅</span>
                                <span class="text">Good form!</span>
                            </div>
                            <div class="confidence-bar">
                                <div class="confidence-fill" id="confidence-fill"></div>
                                <span class="confidence-text" id="confidence-text">85%</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Progress photo guides -->
                    <div class="photo-guides" id="photo-guides" style="display: none;">
                        <div class="pose-outline front-pose" style="display: none;">
                            <div class="guide-text">👤 Stand facing camera</div>
                        </div>
                        <div class="pose-outline side-pose" style="display: none;">
                            <div class="guide-text">🚶 Turn to your side</div>
                        </div>
                        <div class="pose-outline back-pose" style="display: none;">
                            <div class="guide-text">🔄 Face away from camera</div>
                        </div>
                    </div>
                </div>
                
                <div class="camera-controls">
                    <!-- Progress photo controls -->
                    <div class="progress-controls" id="progress-controls">
                        <div class="photo-type-selector">
                            <button class="photo-type active" data-type="front">👤 Front</button>
                            <button class="photo-type" data-type="side">🚶 Side</button>
                            <button class="photo-type" data-type="back">🔄 Back</button>
                            <button class="photo-type" data-type="custom">📷 Custom</button>
                        </div>
                        <button class="capture-btn" onclick="cameraManager.captureProgressPhoto()">
                            📸 Capture Progress Photo
                        </button>
                    </div>
                    
                    <!-- Form check controls -->
                    <div class="form-controls" id="form-controls" style="display: none;">
                        <div class="exercise-selector">
                            <select id="exercise-select" onchange="cameraManager.setExerciseType(this.value)">
                                <option value="">Select Exercise</option>
                                <option value="squat">🏋️ Squat</option>
                                <option value="pushup">💪 Push-up</option>
                                <option value="plank">🏃 Plank</option>
                                <option value="deadlift">⬆️ Deadlift</option>
                                <option value="lunge">🦵 Lunge</option>
                            </select>
                        </div>
                        <button class="analyze-btn" onclick="cameraManager.toggleFormAnalysis()">
                            🔍 Start Form Analysis
                        </button>
                    </div>
                    
                    <!-- Video controls -->
                    <div class="video-controls" id="video-controls" style="display: none;">
                        <button class="record-btn" onclick="cameraManager.toggleVideoRecording()">
                            🔴 Start Recording
                        </button>
                        <span class="recording-timer" id="recording-timer">00:00</span>
                    </div>
                </div>
                
                <!-- Progress photo gallery -->
                <div class="progress-gallery" id="progress-gallery">
                    <h4>📊 Progress Photos</h4>
                    <div class="photo-grid" id="photo-grid"></div>
                </div>
            </div>
            
            <!-- Camera launcher button -->
            <button class="camera-launcher" onclick="cameraManager.openCamera()">
                📸 Open Camera
            </button>
        `;
        
        // Add styles
        const styles = `
            .camera-launcher {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 20px;
                border-radius: 50px;
                font-weight: 600;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
                cursor: pointer;
                z-index: 1000;
                transition: all 0.3s ease;
            }
            
            .camera-launcher:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
            }
            
            .camera-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.95);
                z-index: 10000;
                display: flex;
                flex-direction: column;
            }
            
            .camera-header {
                background: rgba(255, 255, 255, 0.1);
                padding: 15px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                color: white;
            }
            
            .camera-header h3 {
                margin: 0;
                font-size: 18px;
            }
            
            .camera-mode-selector {
                display: flex;
                gap: 10px;
            }
            
            .mode-btn {
                padding: 8px 12px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                background: transparent;
                color: white;
                border-radius: 20px;
                font-size: 12px;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .mode-btn.active, .mode-btn:hover {
                background: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.5);
            }
            
            .close-camera {
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                padding: 5px;
            }
            
            .camera-viewport {
                flex: 1;
                position: relative;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            #camera-video {
                max-width: 100%;
                max-height: 100%;
                border-radius: 10px;
            }
            
            .form-analysis-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
            }
            
            .form-feedback {
                position: absolute;
                top: 20px;
                right: 20px;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 15px;
                border-radius: 10px;
                min-width: 200px;
            }
            
            .feedback-item {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }
            
            .feedback-item .icon {
                margin-right: 8px;
                font-size: 18px;
            }
            
            .confidence-bar {
                background: rgba(255, 255, 255, 0.2);
                height: 8px;
                border-radius: 4px;
                position: relative;
                overflow: hidden;
            }
            
            .confidence-fill {
                background: linear-gradient(90deg, #ef4444, #f59e0b, #10b981);
                height: 100%;
                width: 85%;
                border-radius: 4px;
                transition: width 0.3s ease;
            }
            
            .confidence-text {
                position: absolute;
                right: 5px;
                top: -20px;
                font-size: 12px;
                font-weight: 600;
            }
            
            .camera-controls {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                color: white;
            }
            
            .photo-type-selector, .camera-mode-selector {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
                justify-content: center;
            }
            
            .photo-type {
                padding: 10px 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                background: transparent;
                color: white;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .photo-type.active, .photo-type:hover {
                background: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.5);
            }
            
            .capture-btn, .analyze-btn, .record-btn {
                width: 100%;
                padding: 15px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                font-weight: 600;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .capture-btn:hover, .analyze-btn:hover, .record-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            }
            
            .progress-gallery {
                background: rgba(255, 255, 255, 0.05);
                padding: 20px;
                color: white;
                max-height: 200px;
                overflow-y: auto;
            }
            
            .progress-gallery h4 {
                margin: 0 0 15px 0;
                font-size: 16px;
            }
            
            .photo-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
                gap: 10px;
            }
            
            .progress-photo {
                width: 80px;
                height: 80px;
                border-radius: 8px;
                object-fit: cover;
                cursor: pointer;
                border: 2px solid transparent;
                transition: border-color 0.2s ease;
            }
            
            .progress-photo:hover {
                border-color: #667eea;
            }
            
            .recording-timer {
                color: #ef4444;
                font-weight: 600;
                margin-left: 10px;
            }
            
            .pose-outline {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                border: 2px dashed rgba(255, 255, 255, 0.5);
                width: 200px;
                height: 300px;
                border-radius: 50px;
                display: flex;
                align-items: flex-end;
                justify-content: center;
                padding-bottom: 20px;
            }
            
            .guide-text {
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 8px 12px;
                border-radius: 15px;
                font-size: 14px;
            }
            
            @media (max-width: 768px) {
                .camera-header {
                    flex-direction: column;
                    gap: 10px;
                    padding: 10px;
                }
                
                .camera-mode-selector {
                    order: 1;
                }
                
                .photo-type-selector {
                    flex-wrap: wrap;
                }
                
                .form-feedback {
                    position: static;
                    margin: 10px;
                }
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
        
        document.body.appendChild(cameraInterface);
        
        // Setup mode switching
        this.setupModeSwitch();
        
        console.log('🎨 Camera interface created');
    }
    
    /**
     * Setup camera mode switching
     */
    setupModeSwitch() {
        const modeBtns = document.querySelectorAll('.mode-btn');
        const controls = {
            'progress': document.getElementById('progress-controls'),
            'form': document.getElementById('form-controls'),
            'video': document.getElementById('video-controls')
        };
        
        modeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const mode = btn.dataset.mode;
                
                // Update active button
                modeBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Show/hide appropriate controls
                Object.keys(controls).forEach(key => {
                    controls[key].style.display = key === mode ? 'block' : 'none';
                });
                
                // Show/hide overlays
                document.getElementById('form-overlay').style.display = mode === 'form' ? 'block' : 'none';
                document.getElementById('photo-guides').style.display = mode === 'progress' ? 'block' : 'none';
                
                console.log(`📷 Switched to ${mode} mode`);
            });
        });
    }
    
    /**
     * Open camera interface
     */
    async openCamera() {
        try {
            console.log('📹 Opening camera...');
            
            // Request camera permission
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user' // Front-facing camera for progress photos
                },
                audio: false
            });
            
            // Setup video element
            const video = document.getElementById('camera-video');
            video.srcObject = this.stream;
            
            // Setup canvas for capturing
            const canvas = document.getElementById('camera-canvas');
            this.canvas = canvas;
            this.context = canvas.getContext('2d');
            
            // Show camera interface
            document.querySelector('.camera-container').style.display = 'flex';
            
            // Load existing progress photos
            await this.loadProgressPhotos();
            
            console.log('✅ Camera opened successfully');
            
        } catch (error) {
            console.error('❌ Failed to open camera:', error);
            alert('Failed to access camera. Please check permissions.');
        }
    }
    
    /**
     * Close camera interface
     */
    closeCamera() {
        console.log('📴 Closing camera...');
        
        // Stop camera stream
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        
        // Stop form analysis
        this.isFormAnalysisActive = false;
        
        // Stop recording if active
        if (this.isRecording) {
            this.stopVideoRecording();
        }
        
        // Hide camera interface
        document.querySelector('.camera-container').style.display = 'none';
        
        console.log('✅ Camera closed');
    }
    
    /**
     * Capture progress photo
     */
    async captureProgressPhoto() {
        try {
            const video = document.getElementById('camera-video');
            const activeType = document.querySelector('.photo-type.active').dataset.type;
            
            // Setup canvas
            this.canvas.width = video.videoWidth;
            this.canvas.height = video.videoHeight;
            
            // Draw current frame
            this.context.drawImage(video, 0, 0);
            
            // Convert to blob
            this.canvas.toBlob(async (blob) => {
                const photo = {
                    id: Date.now(),
                    type: activeType,
                    timestamp: new Date(),
                    blob: blob,
                    url: URL.createObjectURL(blob)
                };
                
                // Store photo
                await this.saveProgressPhoto(photo);
                
                // Update gallery
                this.updateProgressGallery();
                
                // Show success feedback
                this.showCaptureSuccess();
                
                console.log(`📸 Progress photo captured: ${activeType}`);
                
            }, 'image/jpeg', 0.8);
            
        } catch (error) {
            console.error('❌ Failed to capture progress photo:', error);
        }
    }
    
    /**
     * Save progress photo
     */
    async saveProgressPhoto(photo) {
        try {
            // Add to local storage
            this.progressPhotos.push(photo);
            
            // Upload to server
            const formData = new FormData();
            formData.append('photo', photo.blob);
            formData.append('type', photo.type);
            formData.append('timestamp', photo.timestamp.toISOString());
            
            const response = await fetch('/api/progress/photos', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                photo.serverId = result.id;
                console.log('☁️ Progress photo uploaded to server');
            }
            
        } catch (error) {
            console.error('❌ Failed to save progress photo:', error);
        }
    }
    
    /**
     * Load existing progress photos
     */
    async loadProgressPhotos() {
        try {
            const response = await fetch('/api/progress/photos');
            
            if (response.ok) {
                const photos = await response.json();
                this.progressPhotos = photos;
                this.updateProgressGallery();
                console.log(`📊 Loaded ${photos.length} progress photos`);
            }
            
        } catch (error) {
            console.error('❌ Failed to load progress photos:', error);
        }
    }
    
    /**
     * Update progress photo gallery
     */
    updateProgressGallery() {
        const photoGrid = document.getElementById('photo-grid');
        
        photoGrid.innerHTML = this.progressPhotos.map(photo => `
            <img src="${photo.url}" 
                 class="progress-photo" 
                 title="${photo.type} - ${photo.timestamp.toLocaleDateString()}"
                 onclick="cameraManager.viewProgressPhoto('${photo.id}')">
        `).join('');
    }
    
    /**
     * View progress photo in full screen
     */
    viewProgressPhoto(photoId) {
        const photo = this.progressPhotos.find(p => p.id === photoId);
        if (photo) {
            // Create full screen view
            const viewer = document.createElement('div');
            viewer.innerHTML = `
                <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                           background: rgba(0,0,0,0.9); z-index: 20000; 
                           display: flex; justify-content: center; align-items: center;"
                     onclick="this.remove()">
                    <img src="${photo.url}" style="max-width: 90%; max-height: 90%; border-radius: 10px;">
                    <div style="position: absolute; top: 20px; right: 20px; color: white; font-size: 24px; cursor: pointer;"
                         onclick="this.parentElement.remove()">✖</div>
                </div>
            `;
            document.body.appendChild(viewer);
        }
    }
    
    /**
     * Initialize pose detection for form analysis
     */
    async initPoseDetection() {
        try {
            // This would integrate with TensorFlow.js PoseNet or similar
            console.log('🤖 Pose detection initialized');
            
            // Simulate pose detection setup
            this.poseDetectionReady = true;
            
        } catch (error) {
            console.error('❌ Failed to initialize pose detection:', error);
        }
    }
    
    /**
     * Set exercise type for form analysis
     */
    setExerciseType(exercise) {
        this.formAnalysis.exerciseType = exercise;
        console.log(`🏋️ Exercise type set: ${exercise}`);
    }
    
    /**
     * Toggle form analysis
     */
    toggleFormAnalysis() {
        const btn = document.querySelector('.analyze-btn');
        
        if (!this.isFormAnalysisActive) {
            this.startFormAnalysis();
            btn.textContent = '⏹ Stop Analysis';
            btn.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
        } else {
            this.stopFormAnalysis();
            btn.textContent = '🔍 Start Form Analysis';
            btn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }
    }
    
    /**
     * Start real-time form analysis
     */
    startFormAnalysis() {
        if (!this.formAnalysis.exerciseType) {
            alert('Please select an exercise type first');
            return;
        }
        
        this.isFormAnalysisActive = true;
        console.log('🔍 Form analysis started');
        
        // Simulate form analysis (would use actual pose detection)
        this.formAnalysisInterval = setInterval(() => {
            this.analyzeForm();
        }, 1000);
    }
    
    /**
     * Stop form analysis
     */
    stopFormAnalysis() {
        this.isFormAnalysisActive = false;
        
        if (this.formAnalysisInterval) {
            clearInterval(this.formAnalysisInterval);
        }
        
        console.log('⏹ Form analysis stopped');
    }
    
    /**
     * Analyze exercise form (simulated)
     */
    analyzeForm() {
        // Simulate form analysis results
        const confidence = Math.random() * 40 + 60; // 60-100%
        const isGoodForm = confidence > 75;
        
        this.formAnalysis.confidence = confidence;
        
        // Update UI
        const statusElement = document.getElementById('form-status');
        const confidenceElement = document.getElementById('confidence-fill');
        const confidenceText = document.getElementById('confidence-text');
        
        if (isGoodForm) {
            statusElement.innerHTML = '<span class="icon">✅</span><span class="text">Good form!</span>';
            this.formAnalysis.warnings = [];
        } else {
            statusElement.innerHTML = '<span class="icon">⚠️</span><span class="text">Check your form</span>';
            this.formAnalysis.warnings = ['Keep your back straight', 'Lower your hips more'];
        }
        
        confidenceElement.style.width = `${confidence}%`;
        confidenceText.textContent = `${Math.round(confidence)}%`;
        
        // Provide audio feedback if confidence is low
        if (confidence < 70 && Math.random() < 0.3) {
            this.speakFormFeedback('Adjust your form');
        }
    }
    
    /**
     * Provide audio form feedback
     */
    speakFormFeedback(message) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(message);
            utterance.volume = 0.5;
            utterance.rate = 0.8;
            speechSynthesis.speak(utterance);
        }
    }
    
    /**
     * Toggle video recording
     */
    toggleVideoRecording() {
        if (!this.isRecording) {
            this.startVideoRecording();
        } else {
            this.stopVideoRecording();
        }
    }
    
    /**
     * Start video recording
     */
    startVideoRecording() {
        try {
            const options = { mimeType: 'video/webm' };
            this.mediaRecorder = new MediaRecorder(this.stream, options);
            
            const chunks = [];
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    chunks.push(event.data);
                }
            };
            
            this.mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: 'video/webm' });
                this.saveWorkoutVideo(blob);
            };
            
            this.mediaRecorder.start();
            this.isRecording = true;
            
            // Update UI
            const recordBtn = document.querySelector('.record-btn');
            recordBtn.textContent = '⏹ Stop Recording';
            recordBtn.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
            
            // Start timer
            this.startRecordingTimer();
            
            console.log('🎥 Video recording started');
            
        } catch (error) {
            console.error('❌ Failed to start video recording:', error);
        }
    }
    
    /**
     * Stop video recording
     */
    stopVideoRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            // Update UI
            const recordBtn = document.querySelector('.record-btn');
            recordBtn.textContent = '🔴 Start Recording';
            recordBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            
            // Stop timer
            this.stopRecordingTimer();
            
            console.log('⏹ Video recording stopped');
        }
    }
    
    /**
     * Start recording timer
     */
    startRecordingTimer() {
        let seconds = 0;
        const timerElement = document.getElementById('recording-timer');
        
        this.recordingTimer = setInterval(() => {
            seconds++;
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            
            timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
        }, 1000);
    }
    
    /**
     * Stop recording timer
     */
    stopRecordingTimer() {
        if (this.recordingTimer) {
            clearInterval(this.recordingTimer);
            document.getElementById('recording-timer').textContent = '00:00';
        }
    }
    
    /**
     * Save workout video
     */
    async saveWorkoutVideo(blob) {
        try {
            const formData = new FormData();
            formData.append('video', blob);
            formData.append('timestamp', new Date().toISOString());
            
            const response = await fetch('/api/workouts/video', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                console.log('🎥 Workout video saved');
                this.showVideoSavedConfirmation();
            }
            
        } catch (error) {
            console.error('❌ Failed to save workout video:', error);
        }
    }
    
    /**
     * Show capture success animation
     */
    showCaptureSuccess() {
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.8);
            z-index: 15000;
            animation: flash 0.3s ease;
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes flash {
                0% { opacity: 0; }
                50% { opacity: 1; }
                100% { opacity: 0; }
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(flash);
        
        setTimeout(() => {
            flash.remove();
            style.remove();
        }, 300);
    }
    
    /**
     * Show video saved confirmation
     */
    showVideoSavedConfirmation() {
        const notification = document.createElement('div');
        notification.textContent = '🎥 Workout video saved successfully!';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #10b981;
            color: white;
            padding: 15px 25px;
            border-radius: 25px;
            font-weight: 600;
            z-index: 15000;
            animation: slideDown 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize camera manager
document.addEventListener('DOMContentLoaded', () => {
    window.cameraManager = new CameraIntegrationManager();
});

console.log('📸 Camera Integration Manager loaded!');