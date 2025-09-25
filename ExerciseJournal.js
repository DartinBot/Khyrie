/**
 * Exercise Journal Component
 * Comprehensive exercise logging with progressive overload tracking, form notes, and analytics
 */
class ExerciseJournal {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.currentUser = 'test_user_123'; // Would come from authentication
        this.selectedWorkoutType = 'strength';
        this.privacyLevel = 'private';
        this.currentSession = {
            exercises: [],
            sessionName: '',
            workoutDate: new Date().toISOString().split('T')[0],
            overallNotes: '',
            energyLevel: 5,
            motivationLevel: 5,
            tags: []
        };
        this.exerciseHistory = [];
        this.exerciseGoals = [];
        
        this.init();
    }

    init() {
        this.createExerciseJournalUI();
        this.bindEvents();
        this.loadExerciseHistory();
        this.loadExerciseGoals();
    }

    createExerciseJournalUI() {
        const container = document.getElementById('exercise-journal-container') || document.body;
        
        const journalHTML = `
            <div class="exercise-journal">
                <div class="journal-header">
                    <h2>📝 Exercise Journal</h2>
                    <p>Track your workouts with detailed sets, reps, weights, and personal insights</p>
                </div>

                <!-- Exercise Logging Section -->
                <div class="exercise-logging">
                    <h3>🏋️‍♂️ Log Today's Workout</h3>
                    
                    <div class="session-details">
                        <div class="detail-row">
                            <div class="detail-group">
                                <label>Session Name</label>
                                <input type="text" id="session-name" placeholder="e.g., 'Push Day A', 'Morning Cardio'" />
                            </div>
                            <div class="detail-group">
                                <label>Workout Type</label>
                                <select id="workout-type">
                                    <option value="strength">💪 Strength Training</option>
                                    <option value="cardio">🏃‍♂️ Cardio</option>
                                    <option value="flexibility">🧘‍♀️ Flexibility/Yoga</option>
                                    <option value="sport">⚽ Sport Specific</option>
                                </select>
                            </div>
                            <div class="detail-group">
                                <label>Date</label>
                                <input type="date" id="workout-date" value="${this.currentSession.workoutDate}" />
                            </div>
                        </div>
                    </div>

                    <div class="exercises-section">
                        <div class="exercises-header">
                            <h4>Exercises</h4>
                            <div class="exercise-actions">
                                <button class="add-exercise-btn" id="add-exercise-btn">➕ Add Exercise</button>
                                <button class="quick-add-btn" id="quick-add-btn">⚡ Quick Add</button>
                            </div>
                        </div>
                        
                        <div class="exercises-list" id="exercises-list">
                            <!-- Exercises will be added dynamically -->
                        </div>
                        
                        <div class="quick-exercises" id="quick-exercises" style="display: none;">
                            <h5>Popular Exercises</h5>
                            <div class="quick-buttons">
                                <button class="quick-exercise" data-exercise="Squat">Squat</button>
                                <button class="quick-exercise" data-exercise="Bench Press">Bench Press</button>
                                <button class="quick-exercise" data-exercise="Deadlift">Deadlift</button>
                                <button class="quick-exercise" data-exercise="Pull-ups">Pull-ups</button>
                                <button class="quick-exercise" data-exercise="Push-ups">Push-ups</button>
                                <button class="quick-exercise" data-exercise="Overhead Press">Overhead Press</button>
                            </div>
                        </div>
                    </div>

                    <div class="session-meta">
                        <div class="meta-row">
                            <div class="meta-group">
                                <label>Energy Level (1-10)</label>
                                <input type="range" id="energy-level" min="1" max="10" value="5" />
                                <span id="energy-display">5</span>
                            </div>
                            <div class="meta-group">
                                <label>Motivation Level (1-10)</label>
                                <input type="range" id="motivation-level" min="1" max="10" value="5" />
                                <span id="motivation-display">5</span>
                            </div>
                        </div>
                        
                        <div class="notes-group">
                            <label>Overall Session Notes</label>
                            <textarea id="session-notes" placeholder="How did the workout feel? Any insights, challenges, or achievements?"></textarea>
                        </div>
                        
                        <div class="tags-section">
                            <label>Tags</label>
                            <div class="tags-input">
                                <input type="text" id="tag-input" placeholder="Add tags (press Enter)" />
                                <div class="tags-list" id="tags-list"></div>
                            </div>
                        </div>
                        
                        <div class="privacy-controls">
                            <label>Share With</label>
                            <div class="privacy-options">
                                <button class="privacy-btn active" data-privacy="private">🔒 Private</button>
                                <button class="privacy-btn" data-privacy="family">👨‍👩‍👧‍👦 Family</button>
                                <button class="privacy-btn" data-privacy="friends">👫 Friends</button>
                                <button class="privacy-btn" data-privacy="public">🌍 Public</button>
                            </div>
                        </div>
                    </div>

                    <button class="log-session-btn" id="log-session-btn">📝 Log Workout Session</button>
                    <div id="journal-message"></div>
                </div>

                <!-- Exercise History & Analytics -->
                <div class="exercise-analytics">
                    <div class="analytics-tabs">
                        <button class="tab-btn active" data-tab="history">📈 History</button>
                        <button class="tab-btn" data-tab="goals">🎯 Goals</button>
                        <button class="tab-btn" data-tab="analytics">📊 Analytics</button>
                        <button class="tab-btn" data-tab="progress">🏆 Progress</button>
                    </div>

                    <div class="tab-content" id="history-tab">
                        <h3>Exercise History</h3>
                        <div class="history-filters">
                            <select id="exercise-filter">
                                <option value="">All Exercises</option>
                            </select>
                            <select id="period-filter">
                                <option value="7">Last 7 days</option>
                                <option value="30">Last 30 days</option>
                                <option value="90">Last 3 months</option>
                            </select>
                        </div>
                        <div class="history-list" id="history-list">
                            <!-- History entries will be populated here -->
                        </div>
                    </div>

                    <div class="tab-content" id="goals-tab" style="display: none;">
                        <h3>Exercise Goals</h3>
                        <div class="goal-form">
                            <h4>Set New Goal</h4>
                            <div class="goal-inputs">
                                <select id="goal-exercise">
                                    <option value="">Select Exercise</option>
                                </select>
                                <select id="goal-type">
                                    <option value="strength">💪 Strength Goal</option>
                                    <option value="endurance">🏃‍♂️ Endurance Goal</option>
                                    <option value="technique">🎯 Technique Goal</option>
                                </select>
                                <input type="number" id="goal-weight" placeholder="Target Weight (kg)" step="0.5" />
                                <input type="number" id="goal-reps" placeholder="Target Reps" />
                                <input type="date" id="goal-date" />
                                <button id="set-goal-btn">Set Goal</button>
                            </div>
                        </div>
                        <div class="goals-list" id="goals-list">
                            <!-- Goals will be displayed here -->
                        </div>
                    </div>

                    <div class="tab-content" id="analytics-tab" style="display: none;">
                        <h3>Performance Analytics</h3>
                        <div class="analytics-dashboard" id="analytics-dashboard">
                            <!-- Analytics charts and metrics -->
                        </div>
                    </div>

                    <div class="tab-content" id="progress-tab" style="display: none;">
                        <h3>Progressive Overload Tracking</h3>
                        <div class="progress-charts" id="progress-charts">
                            <!-- Progress visualization -->
                        </div>
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = journalHTML;
    }

    bindEvents() {
        // Exercise logging events
        document.getElementById('add-exercise-btn').addEventListener('click', () => this.addExercise());
        document.getElementById('quick-add-btn').addEventListener('click', () => this.toggleQuickExercises());
        document.getElementById('log-session-btn').addEventListener('click', () => this.logSession());
        
        // Quick exercise buttons
        document.querySelectorAll('.quick-exercise').forEach(btn => {
            btn.addEventListener('click', (e) => this.addQuickExercise(e.target.dataset.exercise));
        });
        
        // Range sliders
        document.getElementById('energy-level').addEventListener('input', (e) => {
            document.getElementById('energy-display').textContent = e.target.value;
        });
        
        document.getElementById('motivation-level').addEventListener('input', (e) => {
            document.getElementById('motivation-display').textContent = e.target.value;
        });
        
        // Tags input
        document.getElementById('tag-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.addTag();
            }
        });
        
        // Privacy controls
        document.querySelectorAll('.privacy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.privacy-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.privacyLevel = e.target.dataset.privacy;
            });
        });
        
        // Tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
        
        // Goal setting
        document.getElementById('set-goal-btn').addEventListener('click', () => this.setExerciseGoal());
    }

    addExercise(exerciseName = '') {
        const exerciseId = `exercise_${Date.now()}`;
        const exerciseHTML = `
            <div class="exercise-entry" data-exercise-id="${exerciseId}">
                <div class="exercise-header">
                    <input type="text" class="exercise-name" placeholder="Exercise name" value="${exerciseName}" />
                    <button class="remove-exercise" onclick="this.parentElement.parentElement.remove()">❌</button>
                </div>
                
                <div class="exercise-details">
                    <div class="sets-info">
                        <label>Number of Sets</label>
                        <input type="number" class="sets-count" value="3" min="1" max="10" onchange="this.parentElement.parentElement.parentElement.querySelector('.exercise-journal').updateSets(this)" />
                    </div>
                    
                    <div class="sets-table" id="sets-table-${exerciseId}">
                        <!-- Sets will be generated based on sets count -->
                    </div>
                    
                    <div class="exercise-notes">
                        <div class="notes-row">
                            <div class="notes-group">
                                <label>Form Notes</label>
                                <textarea class="form-notes" placeholder="Form cues, technique focus..."></textarea>
                            </div>
                            <div class="notes-group">
                                <label>Technique Focus</label>
                                <input type="text" class="technique-focus" placeholder="What did you work on?" />
                            </div>
                        </div>
                        <div class="pr-checkbox">
                            <label>
                                <input type="checkbox" class="personal-record" />
                                🏆 Personal Record
                            </label>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.getElementById('exercises-list').insertAdjacentHTML('beforeend', exerciseHTML);
        this.updateSetsTable(exerciseId, 3);
    }

    updateSetsTable(exerciseId, setsCount) {
        const table = document.getElementById(`sets-table-${exerciseId}`);
        let tableHTML = `
            <table class="sets-table">
                <thead>
                    <tr>
                        <th>Set</th>
                        <th>Reps</th>
                        <th>Weight (kg)</th>
                        <th>RPE (1-10)</th>
                        <th>Rest (sec)</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        for (let i = 1; i <= setsCount; i++) {
            tableHTML += `
                <tr>
                    <td>${i}</td>
                    <td><input type="number" class="reps" min="1" placeholder="12" /></td>
                    <td><input type="number" class="weight" step="0.5" placeholder="60" /></td>
                    <td><input type="number" class="rpe" min="1" max="10" placeholder="7" /></td>
                    <td><input type="number" class="rest" placeholder="90" /></td>
                </tr>
            `;
        }
        
        tableHTML += '</tbody></table>';
        table.innerHTML = tableHTML;
    }

    addQuickExercise(exerciseName) {
        this.addExercise(exerciseName);
        this.toggleQuickExercises();
    }

    toggleQuickExercises() {
        const quickSection = document.getElementById('quick-exercises');
        quickSection.style.display = quickSection.style.display === 'none' ? 'block' : 'none';
    }

    addTag() {
        const tagInput = document.getElementById('tag-input');
        const tag = tagInput.value.trim();
        
        if (tag && !this.currentSession.tags.includes(tag)) {
            this.currentSession.tags.push(tag);
            this.renderTags();
            tagInput.value = '';
        }
    }

    renderTags() {
        const tagsList = document.getElementById('tags-list');
        tagsList.innerHTML = this.currentSession.tags.map(tag => 
            `<span class="tag">${tag} <button onclick="this.parentElement.remove()">×</button></span>`
        ).join('');
    }

    async logSession() {
        try {
            document.getElementById('log-session-btn').textContent = '⏳ Logging...';
            
            const exercises = this.collectExerciseData();
            
            if (exercises.length === 0) {
                this.showMessage('❌ Please add at least one exercise', 'error');
                return;
            }

            const sessionData = {
                user_id: this.currentUser,
                workout_date: document.getElementById('workout-date').value,
                workout_type: document.getElementById('workout-type').value,
                session_name: document.getElementById('session-name').value,
                exercises: exercises,
                total_duration_minutes: null,
                overall_notes: document.getElementById('session-notes').value,
                energy_level: parseInt(document.getElementById('energy-level').value),
                motivation_level: parseInt(document.getElementById('motivation-level').value),
                share_with_groups: [],
                privacy_level: this.privacyLevel,
                tags: this.currentSession.tags
            };

            const response = await fetch(`${this.apiBase}/api/exercises/log`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(sessionData)
            });

            const result = await response.json();

            if (result.success) {
                this.showMessage(`✅ ${result.message}`, 'success');
                
                // Show personal records if any
                if (result.personal_records && result.personal_records.length > 0) {
                    const recordsMessage = result.personal_records.map(pr => 
                        `🏆 New PR in ${pr.exercise}: ${pr.new_max}kg (+${pr.improvement}kg)`
                    ).join('<br>');
                    this.showMessage(recordsMessage, 'success');
                }
                
                // Clear the form
                this.clearSession();
                
                // Refresh history
                setTimeout(() => {
                    this.loadExerciseHistory();
                }, 1000);
                
            } else {
                this.showMessage(`❌ Error: ${result.message}`, 'error');
            }
        } catch (error) {
            this.showMessage(`❌ Network error: ${error.message}`, 'error');
        } finally {
            document.getElementById('log-session-btn').textContent = '📝 Log Workout Session';
        }
    }

    collectExerciseData() {
        const exercises = [];
        
        document.querySelectorAll('.exercise-entry').forEach(entry => {
            const exerciseName = entry.querySelector('.exercise-name').value;
            if (!exerciseName) return;
            
            const setsCount = parseInt(entry.querySelector('.sets-count').value);
            const reps = [];
            const weights = [];
            const rpes = [];
            const restTimes = [];
            
            entry.querySelectorAll('.sets-table tbody tr').forEach(row => {
                const repInput = row.querySelector('.reps');
                const weightInput = row.querySelector('.weight');
                const rpeInput = row.querySelector('.rpe');
                const restInput = row.querySelector('.rest');
                
                if (repInput.value) {
                    reps.push(parseInt(repInput.value));
                    weights.push(parseFloat(weightInput.value) || 0);
                    rpes.push(parseInt(rpeInput.value) || 5);
                    restTimes.push(parseInt(restInput.value) || 90);
                }
            });
            
            if (reps.length > 0) {
                exercises.push({
                    exercise_name: exerciseName,
                    sets: setsCount,
                    reps: reps,
                    weight: weights,
                    rpe: rpes,
                    rest_time: restTimes,
                    form_notes: entry.querySelector('.form-notes').value,
                    technique_focus: entry.querySelector('.technique-focus').value,
                    personal_record: entry.querySelector('.personal-record').checked
                });
            }
        });
        
        return exercises;
    }

    clearSession() {
        document.getElementById('exercises-list').innerHTML = '';
        document.getElementById('session-name').value = '';
        document.getElementById('session-notes').value = '';
        document.getElementById('energy-level').value = 5;
        document.getElementById('motivation-level').value = 5;
        document.getElementById('energy-display').textContent = '5';
        document.getElementById('motivation-display').textContent = '5';
        this.currentSession.tags = [];
        this.renderTags();
    }

    async loadExerciseHistory() {
        try {
            const response = await fetch(`${this.apiBase}/api/exercises/history/${this.currentUser}`);
            const result = await response.json();
            
            if (result.success) {
                this.exerciseHistory = result.exercise_history;
                this.renderHistory();
                this.updateExerciseFilters();
            }
        } catch (error) {
            console.error('Error loading exercise history:', error);
        }
    }

    renderHistory() {
        const historyList = document.getElementById('history-list');
        
        if (this.exerciseHistory.length === 0) {
            historyList.innerHTML = `
                <div class="empty-state">
                    <h4>📝 Start Your Exercise Journal</h4>
                    <p>Log your first workout to begin tracking your progress!</p>
                </div>
            `;
            return;
        }
        
        const historyHTML = this.exerciseHistory.map(entry => `
            <div class="history-entry">
                <div class="entry-header">
                    <h4>${entry.session_name || 'Workout Session'}</h4>
                    <div class="entry-meta">
                        <span class="date">${new Date(entry.workout_date).toLocaleDateString()}</span>
                        <span class="type">${entry.workout_type}</span>
                    </div>
                </div>
                
                <div class="exercises-summary">
                    ${entry.exercises.map(ex => `
                        <div class="exercise-summary">
                            <strong>${ex.exercise_name}</strong>
                            <span>${ex.sets} sets × ${ex.reps.join('/')} reps</span>
                            ${ex.weight.length > 0 ? `<span>${Math.max(...ex.weight)}kg max</span>` : ''}
                        </div>
                    `).join('')}
                </div>
                
                ${entry.overall_notes ? `
                    <div class="entry-notes">
                        <p><em>${entry.overall_notes}</em></p>
                    </div>
                ` : ''}
                
                <div class="entry-stats">
                    <span>💪 Energy: ${entry.energy_level}/10</span>
                    <span>🔥 Motivation: ${entry.motivation_level}/10</span>
                    ${entry.personal_records && entry.personal_records.length > 0 ? 
                        `<span class="pr-badge">🏆 ${entry.personal_records.length} PR(s)</span>` : ''
                    }
                </div>
            </div>
        `).join('');
        
        historyList.innerHTML = historyHTML;
    }

    updateExerciseFilters() {
        const exerciseFilter = document.getElementById('exercise-filter');
        const goalExercise = document.getElementById('goal-exercise');
        
        const exercises = new Set();
        this.exerciseHistory.forEach(entry => {
            entry.exercises.forEach(ex => exercises.add(ex.exercise_name));
        });
        
        const exerciseOptions = Array.from(exercises).map(exercise => 
            `<option value="${exercise}">${exercise}</option>`
        ).join('');
        
        exerciseFilter.innerHTML = '<option value="">All Exercises</option>' + exerciseOptions;
        goalExercise.innerHTML = '<option value="">Select Exercise</option>' + exerciseOptions;
    }

    async loadExerciseGoals() {
        try {
            const response = await fetch(`${this.apiBase}/api/exercises/goals/${this.currentUser}`);
            const result = await response.json();
            
            if (result.success) {
                this.exerciseGoals = result.active_goals;
                this.renderGoals();
            }
        } catch (error) {
            console.error('Error loading exercise goals:', error);
        }
    }

    renderGoals() {
        const goalsList = document.getElementById('goals-list');
        
        if (this.exerciseGoals.length === 0) {
            goalsList.innerHTML = `
                <div class="empty-state">
                    <h4>🎯 Set Your First Exercise Goal</h4>
                    <p>Goals help you stay focused and track meaningful progress!</p>
                </div>
            `;
            return;
        }
        
        const goalsHTML = this.exerciseGoals.map(goal => `
            <div class="goal-entry">
                <div class="goal-header">
                    <h4>${goal.exercise_name}</h4>
                    <span class="goal-type">${goal.goal_type}</span>
                </div>
                
                <div class="goal-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${goal.progress_percentage}%"></div>
                    </div>
                    <span class="progress-text">${goal.progress_percentage}%</span>
                </div>
                
                <div class="goal-details">
                    ${goal.target_weight ? `<span>Target: ${goal.target_weight}kg</span>` : ''}
                    ${goal.target_reps ? `<span>Target: ${goal.target_reps} reps</span>` : ''}
                    ${goal.target_date ? `<span>By: ${new Date(goal.target_date).toLocaleDateString()}</span>` : ''}
                </div>
                
                ${goal.notes ? `<p class="goal-notes">${goal.notes}</p>` : ''}
            </div>
        `).join('');
        
        goalsList.innerHTML = goalsHTML;
    }

    async setExerciseGoal() {
        const exerciseName = document.getElementById('goal-exercise').value;
        const goalType = document.getElementById('goal-type').value;
        const targetWeight = document.getElementById('goal-weight').value;
        const targetReps = document.getElementById('goal-reps').value;
        const targetDate = document.getElementById('goal-date').value;
        
        if (!exerciseName) {
            this.showMessage('❌ Please select an exercise', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBase}/api/exercises/set-goal`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.currentUser,
                    exercise_name: exerciseName,
                    goal_type: goalType,
                    target_weight: targetWeight ? parseFloat(targetWeight) : null,
                    target_reps: targetReps ? parseInt(targetReps) : null,
                    target_date: targetDate || null,
                    current_max: 0,
                    notes: ""
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showMessage('✅ Exercise goal set successfully!', 'success');
                this.loadExerciseGoals();
                
                // Clear form
                document.getElementById('goal-weight').value = '';
                document.getElementById('goal-reps').value = '';
                document.getElementById('goal-date').value = '';
            } else {
                this.showMessage(`❌ Error: ${result.message}`, 'error');
            }
        } catch (error) {
            this.showMessage(`❌ Network error: ${error.message}`, 'error');
        }
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.style.display = 'none';
        });
        document.getElementById(`${tabName}-tab`).style.display = 'block';
        
        // Load tab-specific data
        if (tabName === 'analytics') {
            this.loadAnalytics();
        } else if (tabName === 'progress') {
            this.loadProgressCharts();
        }
    }

    async loadAnalytics() {
        try {
            const response = await fetch(`${this.apiBase}/api/exercises/analytics/${this.currentUser}`);
            const result = await response.json();
            
            if (result.success) {
                this.renderAnalytics(result.analytics);
            }
        } catch (error) {
            console.error('Error loading analytics:', error);
        }
    }

    renderAnalytics(analytics) {
        const dashboard = document.getElementById('analytics-dashboard');
        
        const analyticsHTML = `
            <div class="analytics-grid">
                <div class="analytics-card">
                    <h4>💪 Strength Trends</h4>
                    <p>Overall: ${analytics.strength_trends?.overall_trend || 'N/A'}</p>
                    <p>Monthly: ${analytics.strength_trends?.monthly_improvement || 'N/A'}</p>
                    <p>Strongest: ${analytics.strength_trends?.strongest_exercise || 'N/A'}</p>
                </div>
                
                <div class="analytics-card">
                    <h4>📊 Volume Analysis</h4>
                    <p>Last Month: ${analytics.volume_analysis?.total_volume_last_month || 0}kg</p>
                    <p>Trend: ${analytics.volume_analysis?.volume_trend || 'N/A'}</p>
                    <p>Avg Session: ${analytics.volume_analysis?.average_session_volume || 0}kg</p>
                </div>
                
                <div class="analytics-card">
                    <h4>📈 Consistency</h4>
                    <p>Sessions This Month: ${analytics.consistency_metrics?.sessions_this_month || 0}</p>
                    <p>Weekly Average: ${analytics.consistency_metrics?.average_sessions_per_week || 0}</p>
                    <p>Current Streak: ${analytics.consistency_metrics?.current_streak || 0}</p>
                </div>
                
                <div class="analytics-card insights">
                    <h4>💡 Insights</h4>
                    ${analytics.performance_insights?.map(insight => 
                        `<p>• ${insight}</p>`
                    ).join('') || '<p>Keep logging workouts for insights!</p>'}
                </div>
            </div>
        `;
        
        dashboard.innerHTML = analyticsHTML;
    }

    loadProgressCharts() {
        const progressCharts = document.getElementById('progress-charts');
        
        // Mock progress visualization - would integrate with chart library
        progressCharts.innerHTML = `
            <div class="progress-visualization">
                <h4>Progressive Overload Tracking</h4>
                <div class="chart-placeholder">
                    <p>📊 Interactive progress charts coming soon!</p>
                    <p>Track your strength gains over time with detailed visualizations.</p>
                </div>
                
                <div class="progress-highlights">
                    <div class="highlight">
                        <h5>🏆 Recent Achievements</h5>
                        <p>New deadlift PR: 140kg (+5kg)</p>
                        <p>Consistency streak: 12 days</p>
                    </div>
                    
                    <div class="highlight">
                        <h5>📈 Trending Up</h5>
                        <p>Squat volume +15% this month</p>
                        <p>Overall training frequency +20%</p>
                    </div>
                </div>
            </div>
        `;
    }

    showMessage(message, type = 'info') {
        const messageDiv = document.getElementById('journal-message');
        messageDiv.innerHTML = message;
        messageDiv.className = `message ${type}`;
        
        setTimeout(() => {
            messageDiv.innerHTML = '';
            messageDiv.className = 'message';
        }, 5000);
    }
}

// Initialize exercise journal when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const exerciseJournal = new ExerciseJournal();
    
    // Add global method for updating sets (called from inline onclick)
    window.updateSets = function(input) {
        const exerciseEntry = input.closest('.exercise-entry');
        const exerciseId = exerciseEntry.dataset.exerciseId;
        const setsCount = parseInt(input.value);
        exerciseJournal.updateSetsTable(exerciseId, setsCount);
    };
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ExerciseJournal;
}