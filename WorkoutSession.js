// Khyrie Workout Session JavaScript

class WorkoutSession {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.startTime = new Date();
        this.currentExerciseIndex = 0;
        this.currentSet = 1;
        this.completedSets = [];
        this.restTimer = null;
        this.sessionTimer = null;
        this.metronomeInterval = null;
        this.isResting = false;
        this.fabMenuOpen = false;
        
        // Default workout data - would be loaded from API
        this.workout = {
            id: 'upper-strength-001',
            name: 'Upper Body Strength Focus',
            exercises: [
                {
                    id: 'bench-press',
                    name: 'Bench Press',
                    targetMuscles: '🎯 Chest, Triceps, Shoulders',
                    type: '💪 Compound',
                    sets: 4,
                    reps: '6-8',
                    restTime: 120, // seconds
                    lastPerformed: { weight: 185, reps: 8 },
                    instructions: [
                        'Lie flat on bench with feet firmly planted',
                        'Grip bar slightly wider than shoulder width',
                        'Lower bar to chest with control',
                        'Press up explosively, keeping core tight'
                    ],
                    tips: [
                        'Keep shoulder blades retracted',
                        'Don\'t bounce the bar off your chest',
                        'Breathe out during the pressing motion'
                    ]
                },
                {
                    id: 'overhead-press',
                    name: 'Overhead Press',
                    targetMuscles: '🎯 Shoulders, Triceps, Core',
                    type: '💪 Compound',
                    sets: 3,
                    reps: '8-10',
                    restTime: 90,
                    lastPerformed: { weight: 135, reps: 9 }
                },
                {
                    id: 'incline-db-press',
                    name: 'Incline Dumbbell Press',
                    targetMuscles: '🎯 Upper Chest, Shoulders',
                    type: '💪 Compound',
                    sets: 3,
                    reps: '8-12',
                    restTime: 90,
                    lastPerformed: { weight: 70, reps: 10 }
                },
                {
                    id: 'dips',
                    name: 'Parallel Dips',
                    targetMuscles: '🎯 Chest, Triceps',
                    type: '💪 Compound',
                    sets: 3,
                    reps: '10-15',
                    restTime: 75,
                    lastPerformed: { weight: 'bodyweight', reps: 12 }
                },
                {
                    id: 'tricep-pushdown',
                    name: 'Tricep Pushdown',
                    targetMuscles: '🎯 Triceps',
                    type: '🎯 Isolation',
                    sets: 3,
                    reps: '12-15',
                    restTime: 60,
                    lastPerformed: { weight: 80, reps: 14 }
                },
                {
                    id: 'lateral-raise',
                    name: 'Lateral Raises',
                    targetMuscles: '🎯 Side Delts',
                    type: '🎯 Isolation',
                    sets: 3,
                    reps: '15-20',
                    restTime: 60,
                    lastPerformed: { weight: 20, reps: 18 }
                }
            ]
        };
        
        this.init();
    }

    async init() {
        console.log('🏋️‍♂️ Starting workout session:', this.sessionId);
        
        // Initialize UI
        this.updateWorkoutDisplay();
        this.updateExerciseDisplay();
        this.startSessionTimer();
        this.setupEventListeners();
        
        // Register for background sync if available
        if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
            this.registerBackgroundSync();
        }
        
        // Prevent screen sleep during workout
        this.requestWakeLock();
        
        console.log('✅ Workout session initialized');
    }

    generateSessionId() {
        return 'workout_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    updateWorkoutDisplay() {
        document.getElementById('workout-name').textContent = this.workout.name;
        document.getElementById('total-exercises').textContent = this.workout.exercises.length;
        this.updateProgress();
    }

    updateExerciseDisplay() {
        const exercise = this.getCurrentExercise();
        if (!exercise) return;

        // Update exercise info
        document.getElementById('exercise-name').textContent = exercise.name;
        document.getElementById('target-muscles').textContent = exercise.targetMuscles;
        document.getElementById('exercise-type').textContent = exercise.type;
        document.getElementById('current-exercise').textContent = this.currentExerciseIndex + 1;

        // Update previous record
        const recordEl = document.querySelector('.previous-record span');
        if (exercise.lastPerformed) {
            const { weight, reps } = exercise.lastPerformed;
            recordEl.textContent = `Last: ${weight === 'bodyweight' ? 'Bodyweight' : weight + ' lbs'} × ${reps} reps`;
        }

        // Update exercise visual
        this.updateExerciseVisual(exercise);

        // Reset set tracking
        this.currentSet = 1;
        this.completedSets = [];
        this.updateSetsDisplay();
        this.updateSetInput();
        this.updateNavigationButtons();
    }

    updateExerciseVisual(exercise) {
        const gifEl = document.getElementById('exercise-gif');
        const placeholderEl = document.getElementById('exercise-placeholder');
        
        // Try to load exercise GIF
        gifEl.src = `/images/exercises/${exercise.id}.gif`;
        gifEl.style.display = 'block';
        placeholderEl.style.display = 'none';
        
        // Fallback to placeholder if GIF fails
        gifEl.onerror = () => {
            gifEl.style.display = 'none';
            placeholderEl.style.display = 'flex';
            placeholderEl.querySelector('span').textContent = exercise.name;
        };
    }

    updateProgress() {
        const progressPercent = ((this.currentExerciseIndex + 1) / this.workout.exercises.length) * 100;
        document.getElementById('workout-progress').style.width = `${progressPercent}%`;
    }

    updateSetsDisplay() {
        const setsGrid = document.getElementById('sets-grid');
        setsGrid.innerHTML = this.completedSets.map((set, index) => `
            <div class="completed-set">
                <div class="set-details">
                    <div class="set-number-badge">${index + 1}</div>
                    <span>${set.weight === 'bodyweight' ? 'BW' : set.weight + ' lbs'}</span>
                    <span>×</span>
                    <span>${set.reps} reps</span>
                </div>
                <div class="set-difficulty">
                    ${this.getDifficultyEmoji(set.difficulty)}
                </div>
            </div>
        `).join('');
    }

    updateSetInput() {
        const exercise = this.getCurrentExercise();
        document.getElementById('current-set').textContent = this.currentSet;
        
        // Pre-populate with last set's values or previous record
        const weightInput = document.getElementById('weight-input');
        const repsInput = document.getElementById('reps-input');
        
        if (this.completedSets.length > 0) {
            const lastSet = this.completedSets[this.completedSets.length - 1];
            weightInput.value = lastSet.weight === 'bodyweight' ? '' : lastSet.weight;
            repsInput.value = lastSet.reps;
        } else if (exercise.lastPerformed) {
            weightInput.value = exercise.lastPerformed.weight === 'bodyweight' ? '' : exercise.lastPerformed.weight;
            repsInput.value = exercise.lastPerformed.reps;
        }
        
        // Focus on weight input for quick entry
        weightInput.focus();
    }

    updateNavigationButtons() {
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        
        prevBtn.disabled = this.currentExerciseIndex === 0;
        
        if (this.currentExerciseIndex === this.workout.exercises.length - 1) {
            nextBtn.textContent = 'Finish Workout →';
        } else {
            nextBtn.textContent = 'Next Exercise →';
        }
    }

    getCurrentExercise() {
        return this.workout.exercises[this.currentExerciseIndex];
    }

    getDifficultyEmoji(difficulty) {
        switch (difficulty) {
            case 'easy': return '😌';
            case 'moderate': return '😤';
            case 'hard': return '🔥';
            default: return '😤';
        }
    }

    setupEventListeners() {
        // Difficulty selector
        document.querySelectorAll('.difficulty-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.difficulty-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
            });
        });

        // Input validation and formatting
        const weightInput = document.getElementById('weight-input');
        const repsInput = document.getElementById('reps-input');
        
        weightInput.addEventListener('input', this.formatWeightInput);
        repsInput.addEventListener('input', this.formatRepsInput);
        
        // Enter key handling
        weightInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') repsInput.focus();
        });
        
        repsInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addSet();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboardShortcuts.bind(this));
        
        // Screen wake lock handling
        document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this));
        
        // Haptic feedback for mobile
        if ('vibrate' in navigator) {
            document.querySelectorAll('button').forEach(btn => {
                btn.addEventListener('click', () => {
                    navigator.vibrate(10); // Subtle haptic feedback
                });
            });
        }
    }

    formatWeightInput(e) {
        let value = e.target.value.replace(/[^\d.]/g, '');
        if (value) {
            const num = parseFloat(value);
            if (num > 0) {
                e.target.value = num.toString();
            }
        }
    }

    formatRepsInput(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value) {
            const num = parseInt(value);
            if (num > 0 && num <= 100) {
                e.target.value = num.toString();
            } else if (num > 100) {
                e.target.value = '100';
            }
        }
    }

    handleKeyboardShortcuts(e) {
        // Space bar to complete set
        if (e.code === 'Space' && !e.target.matches('input')) {
            e.preventDefault();
            this.addSet();
        }
        
        // Arrow keys for navigation
        if (e.code === 'ArrowLeft' && e.ctrlKey) {
            e.preventDefault();
            this.previousExercise();
        }
        
        if (e.code === 'ArrowRight' && e.ctrlKey) {
            e.preventDefault();
            this.nextExercise();
        }
    }

    async addSet() {
        const weightInput = document.getElementById('weight-input');
        const repsInput = document.getElementById('reps-input');
        const difficultyBtn = document.querySelector('.difficulty-btn.active');
        
        const weight = weightInput.value || 'bodyweight';
        const reps = parseInt(repsInput.value);
        const difficulty = difficultyBtn ? difficultyBtn.dataset.difficulty : 'moderate';
        
        if (!reps || reps <= 0) {
            this.showToast('Please enter a valid number of reps', 'error');
            repsInput.focus();
            return;
        }
        
        // Add haptic feedback
        this.triggerHapticFeedback();
        
        // Create set object
        const set = {
            setNumber: this.currentSet,
            weight: weight === 'bodyweight' ? 'bodyweight' : parseFloat(weight),
            reps: reps,
            difficulty: difficulty,
            timestamp: new Date().toISOString()
        };
        
        this.completedSets.push(set);
        this.currentSet++;
        
        // Update displays
        this.updateSetsDisplay();
        this.clearInputs();
        
        // Check if exercise is complete
        const exercise = this.getCurrentExercise();
        if (this.completedSets.length >= exercise.sets) {
            this.completeExercise();
        } else {
            // Start rest timer
            this.startRestTimer(exercise.restTime);
        }
        
        // Save progress
        this.saveProgress();
        
        this.showToast('Set completed! 💪', 'success');
    }

    clearInputs() {
        document.getElementById('weight-input').value = '';
        document.getElementById('reps-input').value = '';
        // Keep difficulty selection for next set
    }

    async completeExercise() {
        const exercise = this.getCurrentExercise();
        
        // Check for personal records
        const prs = this.checkForPersonalRecords(exercise);
        if (prs.length > 0) {
            this.celebratePersonalRecords(prs);
        }
        
        // Auto-advance to next exercise after short delay
        setTimeout(() => {
            if (this.currentExerciseIndex < this.workout.exercises.length - 1) {
                this.nextExercise();
            } else {
                this.completeWorkout();
            }
        }, 2000);
    }

    checkForPersonalRecords(exercise) {
        const prs = [];
        
        this.completedSets.forEach(set => {
            if (exercise.lastPerformed) {
                // Check for weight PR
                if (set.weight !== 'bodyweight' && exercise.lastPerformed.weight !== 'bodyweight') {
                    if (set.weight > exercise.lastPerformed.weight) {
                        prs.push({ type: 'weight', value: set.weight });
                    }
                }
                
                // Check for reps PR at same weight
                if (set.weight === exercise.lastPerformed.weight && set.reps > exercise.lastPerformed.reps) {
                    prs.push({ type: 'reps', value: set.reps, weight: set.weight });
                }
            }
        });
        
        return prs;
    }

    celebratePersonalRecords(prs) {
        prs.forEach(pr => {
            let message = '';
            if (pr.type === 'weight') {
                message = `New Weight PR: ${pr.value} lbs! 🔥`;
            } else if (pr.type === 'reps') {
                message = `New Rep PR: ${pr.value} reps at ${pr.weight} lbs! 💪`;
            }
            
            this.showToast(message, 'success', 5000);
            
            // Extra haptic feedback for PR
            if ('vibrate' in navigator) {
                navigator.vibrate([100, 50, 100, 50, 200]);
            }
        });
    }

    startRestTimer(seconds) {
        if (this.isResting) return;
        
        this.isResting = true;
        let timeLeft = seconds;
        
        const restCard = document.getElementById('rest-timer-card');
        const timeDisplay = document.getElementById('rest-time');
        const progressCircle = document.getElementById('timer-progress-circle');
        const nextSetNum = document.getElementById('next-set-number');
        
        // Show rest timer
        restCard.style.display = 'flex';
        nextSetNum.textContent = this.currentSet;
        
        // Calculate circle circumference for progress
        const circumference = 2 * Math.PI * 45; // radius is 45
        progressCircle.style.strokeDasharray = circumference;
        
        this.restTimer = setInterval(() => {
            timeLeft--;
            
            // Update display
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            timeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            // Update progress circle
            const progress = timeLeft / seconds;
            const offset = circumference * (1 - progress);
            progressCircle.style.strokeDashoffset = offset;
            
            // Vibrate on last 3 seconds
            if (timeLeft <= 3 && timeLeft > 0 && 'vibrate' in navigator) {
                navigator.vibrate(200);
            }
            
            if (timeLeft <= 0) {
                this.completeRestTimer();
            }
        }, 1000);
    }

    completeRestTimer() {
        this.clearRestTimer();
        this.showToast('Rest complete! Ready for next set 💪', 'success');
        
        // Strong vibration for rest completion
        if ('vibrate' in navigator) {
            navigator.vibrate([300, 100, 300]);
        }
        
        // Focus on weight input for next set
        document.getElementById('weight-input').focus();
    }

    clearRestTimer() {
        if (this.restTimer) {
            clearInterval(this.restTimer);
            this.restTimer = null;
        }
        
        this.isResting = false;
        document.getElementById('rest-timer-card').style.display = 'none';
    }

    pauseRestTimer() {
        if (this.restTimer) {
            clearInterval(this.restTimer);
            this.restTimer = null;
            this.showToast('Rest timer paused', 'info');
        }
    }

    skipRest() {
        this.completeRestTimer();
    }

    addRestTime(seconds) {
        // Add time to current rest timer
        const timeDisplay = document.getElementById('rest-time');
        const currentTime = timeDisplay.textContent.split(':');
        const currentSeconds = parseInt(currentTime[0]) * 60 + parseInt(currentTime[1]);
        const newTime = currentSeconds + seconds;
        
        // Update display immediately
        const minutes = Math.floor(newTime / 60);
        const secs = newTime % 60;
        timeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        
        this.showToast(`Added ${seconds} seconds to rest timer`, 'info');
    }

    nextExercise() {
        if (this.currentExerciseIndex < this.workout.exercises.length - 1) {
            this.currentExerciseIndex++;
            this.updateExerciseDisplay();
            this.updateProgress();
            this.clearRestTimer();
            
            // Scroll to top smoothly
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            this.completeWorkout();
        }
    }

    previousExercise() {
        if (this.currentExerciseIndex > 0) {
            this.currentExerciseIndex--;
            this.updateExerciseDisplay();
            this.updateProgress();
            this.clearRestTimer();
            
            // Scroll to top smoothly
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    completeWorkout() {
        this.clearRestTimer();
        this.stopSessionTimer();
        
        // Calculate workout statistics
        const endTime = new Date();
        const duration = Math.round((endTime - this.startTime) / 1000 / 60); // minutes
        const totalSets = this.workout.exercises.reduce((total, ex) => total + ex.sets, 0);
        const completedSetsTotal = this.completedSets.length;
        const totalVolume = this.calculateTotalVolume();
        const prCount = this.getTotalPRCount();
        
        // Update summary modal
        document.getElementById('total-duration').textContent = this.formatDuration(duration * 60);
        document.getElementById('exercises-completed').textContent = `${this.workout.exercises.length} of ${this.workout.exercises.length}`;
        document.getElementById('total-volume').textContent = `${totalVolume.toLocaleString()} lbs`;
        document.getElementById('pr-count').textContent = prCount > 0 ? `${prCount} PRs! 🔥` : 'No PRs today';
        
        // Show completion modal
        document.getElementById('complete-modal').classList.add('active');
        
        // Celebrate with haptics
        if ('vibrate' in navigator) {
            navigator.vibrate([200, 100, 200, 100, 400]);
        }
    }

    calculateTotalVolume() {
        return this.completedSets.reduce((total, set) => {
            if (set.weight === 'bodyweight') {
                return total + (180 * set.reps); // Assume 180 lbs bodyweight
            }
            return total + (set.weight * set.reps);
        }, 0);
    }

    getTotalPRCount() {
        // This would be calculated based on stored PR data
        return Math.floor(Math.random() * 3); // Mock data
    }

    formatDuration(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }

    startSessionTimer() {
        this.sessionTimer = setInterval(() => {
            const elapsed = Math.floor((new Date() - this.startTime) / 1000);
            document.getElementById('session-timer').textContent = this.formatDuration(elapsed);
        }, 1000);
    }

    stopSessionTimer() {
        if (this.sessionTimer) {
            clearInterval(this.sessionTimer);
            this.sessionTimer = null;
        }
    }

    // Quick action methods
    adjustWeight(amount) {
        const weightInput = document.getElementById('weight-input');
        const currentWeight = parseFloat(weightInput.value) || 0;
        const newWeight = Math.max(0, currentWeight + amount);
        weightInput.value = newWeight > 0 ? newWeight : '';
        this.showToast(`Weight adjusted to ${newWeight} lbs`, 'info');
    }

    repeatLastSet() {
        if (this.completedSets.length === 0) {
            this.showToast('No previous set to repeat', 'warning');
            return;
        }
        
        const lastSet = this.completedSets[this.completedSets.length - 1];
        document.getElementById('weight-input').value = lastSet.weight === 'bodyweight' ? '' : lastSet.weight;
        document.getElementById('reps-input').value = lastSet.reps;
        
        // Set difficulty
        document.querySelectorAll('.difficulty-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.difficulty === lastSet.difficulty);
        });
        
        this.showToast('Previous set loaded', 'success');
    }

    toggleMetronome() {
        if (this.metronomeInterval) {
            clearInterval(this.metronomeInterval);
            this.metronomeInterval = null;
            this.showToast('Metronome stopped', 'info');
        } else {
            // 60 BPM metronome for controlled reps
            this.metronomeInterval = setInterval(() => {
                if ('vibrate' in navigator) {
                    navigator.vibrate(50);
                }
            }, 1000);
            this.showToast('Metronome started (60 BPM)', 'success');
        }
    }

    // FAB menu methods
    toggleFabMenu() {
        this.fabMenuOpen = !this.fabMenuOpen;
        const fab = document.getElementById('main-fab');
        const menu = document.getElementById('fab-menu');
        
        fab.classList.toggle('active', this.fabMenuOpen);
        menu.classList.toggle('active', this.fabMenuOpen);
    }

    takeNote() {
        const note = prompt('Add a note for this exercise:');
        if (note && note.trim()) {
            // Save note with current exercise
            this.showToast('Note saved!', 'success');
        }
        this.toggleFabMenu();
    }

    recordForm() {
        this.showToast('Form recording feature coming soon!', 'info');
        this.toggleFabMenu();
    }

    shareSet() {
        const exercise = this.getCurrentExercise();
        const lastSet = this.completedSets[this.completedSets.length - 1];
        
        if (!lastSet) {
            this.showToast('Complete a set first!', 'warning');
            this.toggleFabMenu();
            return;
        }
        
        const shareText = `Just completed: ${exercise.name} - ${lastSet.weight === 'bodyweight' ? 'Bodyweight' : lastSet.weight + ' lbs'} × ${lastSet.reps} reps! 💪`;
        
        if (navigator.share) {
            navigator.share({
                title: 'Workout Progress',
                text: shareText,
                url: window.location.href
            });
        } else {
            navigator.clipboard.writeText(shareText);
            this.showToast('Set details copied to clipboard!', 'success');
        }
        
        this.toggleFabMenu();
    }

    // Exercise guide methods
    showExerciseGuide() {
        const exercise = this.getCurrentExercise();
        document.getElementById('guide-exercise-name').textContent = exercise.name;
        
        if (exercise.instructions) {
            document.getElementById('exercise-instructions').innerHTML = 
                exercise.instructions.map(instruction => `<li>${instruction}</li>`).join('');
        }
        
        if (exercise.tips) {
            document.getElementById('exercise-tips').innerHTML = 
                exercise.tips.map(tip => `<li>${tip}</li>`).join('');
        }
        
        document.getElementById('guide-modal').classList.add('active');
    }

    closeExerciseGuide() {
        document.getElementById('guide-modal').classList.remove('active');
    }

    // Workout completion methods
    async saveWorkout() {
        try {
            const workoutData = {
                sessionId: this.sessionId,
                workoutId: this.workout.id,
                startTime: this.startTime,
                endTime: new Date(),
                exercises: this.workout.exercises.map((exercise, index) => ({
                    exerciseId: exercise.id,
                    name: exercise.name,
                    sets: index === this.currentExerciseIndex ? this.completedSets : []
                }))
            };
            
            const response = await fetch('/api/workouts/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(workoutData)
            });
            
            if (response.ok) {
                this.showToast('Workout saved successfully!', 'success');
                setTimeout(() => window.location.href = '/dashboard', 2000);
            } else {
                throw new Error('Save failed');
            }
        } catch (error) {
            console.error('Error saving workout:', error);
            // Queue for offline sync
            this.queueForSync(workoutData);
            this.showToast('Workout queued for sync', 'warning');
        }
    }

    shareWorkout() {
        const duration = Math.round((new Date() - this.startTime) / 1000 / 60);
        const shareText = `Just completed: ${this.workout.name} in ${duration} minutes! 💪 #KhyrieFitness`;
        
        if (navigator.share) {
            navigator.share({
                title: 'Workout Complete',
                text: shareText,
                url: window.location.href
            });
        } else {
            navigator.clipboard.writeText(shareText);
            this.showToast('Workout summary copied!', 'success');
        }
    }

    // Utility methods
    triggerHapticFeedback() {
        if ('vibrate' in navigator) {
            navigator.vibrate(25);
        }
    }

    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 100px;
            left: 50%;
            transform: translateX(-50%);
            background: ${type === 'success' ? '#48bb78' : type === 'error' ? '#f56565' : type === 'warning' ? '#ed8936' : '#4299e1'};
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            animation: toastSlideIn 0.3s ease;
            font-weight: 500;
            max-width: 300px;
            text-align: center;
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'toastSlideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    async requestWakeLock() {
        try {
            if ('wakeLock' in navigator) {
                this.wakeLock = await navigator.wakeLock.request('screen');
                console.log('Screen wake lock activated');
            }
        } catch (error) {
            console.log('Wake lock not supported or failed:', error);
        }
    }

    handleVisibilityChange() {
        if (this.wakeLock && document.visibilityState === 'visible') {
            this.requestWakeLock();
        }
    }

    async registerBackgroundSync() {
        const registration = await navigator.serviceWorker.ready;
        registration.sync.register('workout-sync');
    }

    queueForSync(data) {
        const syncData = JSON.parse(localStorage.getItem('workoutSyncQueue') || '[]');
        syncData.push(data);
        localStorage.setItem('workoutSyncQueue', JSON.stringify(syncData));
    }

    saveProgress() {
        const progress = {
            sessionId: this.sessionId,
            currentExerciseIndex: this.currentExerciseIndex,
            completedSets: this.completedSets,
            timestamp: new Date().toISOString()
        };
        
        localStorage.setItem('workoutProgress', JSON.stringify(progress));
    }
}

// Global functions for HTML onclick handlers
let workoutSession = null;

function toggleWorkoutMenu() {
    // Show workout menu options
    workoutSession.showToast('Workout menu coming soon!', 'info');
}

function showExerciseGuide() {
    workoutSession.showExerciseGuide();
}

function closeExerciseGuide() {
    workoutSession.closeExerciseGuide();
}

function addSet() {
    workoutSession.addSet();
}

function pauseRestTimer() {
    workoutSession.pauseRestTimer();
}

function skipRest() {
    workoutSession.skipRest();
}

function addRestTime(seconds) {
    workoutSession.addRestTime(seconds);
}

function nextExercise() {
    workoutSession.nextExercise();
}

function previousExercise() {
    workoutSession.previousExercise();
}

function toggleFabMenu() {
    workoutSession.toggleFabMenu();
}

function takeNote() {
    workoutSession.takeNote();
}

function recordForm() {
    workoutSession.recordForm();
}

function shareSet() {
    workoutSession.shareSet();
}

function adjustWeight(amount) {
    workoutSession.adjustWeight(amount);
}

function repeatLastSet() {
    workoutSession.repeatLastSet();
}

function toggleMetronome() {
    workoutSession.toggleMetronome();
}

function saveWorkout() {
    workoutSession.saveWorkout();
}

function shareWorkout() {
    workoutSession.shareWorkout();
}

// Initialize workout session when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    workoutSession = new WorkoutSession();
});

// Add CSS animations for toasts
const style = document.createElement('style');
style.textContent = `
    @keyframes toastSlideIn {
        from { 
            opacity: 0;
            transform: translateX(-50%) translateY(-20px);
        }
        to { 
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }
    
    @keyframes toastSlideOut {
        from { 
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
        to { 
            opacity: 0;
            transform: translateX(-50%) translateY(-20px);
        }
    }
`;
document.head.appendChild(style);