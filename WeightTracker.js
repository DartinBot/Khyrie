/**
 * Weight Tracker Component
 * Handles weight logging, history, analytics, and family challenges
 */
class WeightTracker {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.currentUser = 'test_user_123'; // Would come from authentication
        this.selectedUnit = 'kg';
        this.privacyLevel = 'family';
        this.shareWithGroups = ['family_group_1'];
        this.weightHistory = [];
        
        this.init();
    }

    init() {
        this.createWeightTrackerUI();
        this.bindEvents();
        this.loadWeightHistory();
    }

    createWeightTrackerUI() {
        const container = document.getElementById('weight-tracker-container') || 
                         document.createElement('div');
        container.id = 'weight-tracker-container';
        
        container.innerHTML = `
            <div class="weight-tracker">
                <h2>📊 Weight Tracking</h2>
                
                <div class="weight-input-section">
                    <div class="weight-input-group">
                        <label for="weight-input">Current Weight</label>
                        <input type="number" 
                               id="weight-input" 
                               class="weight-input" 
                               placeholder="75.5" 
                               step="0.1" 
                               min="0" 
                               max="500">
                        <div class="unit-selector">
                            <button class="unit-btn active" data-unit="kg">kg</button>
                            <button class="unit-btn" data-unit="lbs">lbs</button>
                        </div>
                    </div>
                    
                    <div class="weight-input-group">
                        <label for="goal-weight">Goal Weight</label>
                        <input type="number" 
                               id="goal-weight" 
                               class="weight-input" 
                               placeholder="70.0" 
                               step="0.1" 
                               min="0" 
                               max="500">
                        <div style="margin-top: 10px; text-align: center; font-size: 0.9em;">
                            <span id="goal-difference">Set your goal weight</span>
                        </div>
                    </div>
                    
                    <div class="weight-notes">
                        <label for="weight-notes-input">Notes (Optional)</label>
                        <textarea id="weight-notes-input" 
                                  placeholder="Morning weigh-in after workout, feeling great!"></textarea>
                    </div>
                </div>

                <div class="privacy-controls">
                    <h4>Share With</h4>
                    <div class="privacy-options">
                        <button class="privacy-btn active" data-privacy="family">👨‍👩‍👧‍👦 Family</button>
                        <button class="privacy-btn" data-privacy="friends">👫 Friends</button>
                        <button class="privacy-btn" data-privacy="private">🔒 Private</button>
                        <button class="privacy-btn" data-privacy="public">🌍 Community</button>
                    </div>
                </div>

                <button class="log-weight-btn" id="log-weight-btn">
                    📝 Log Weight
                </button>
                
                <div id="weight-message"></div>
            </div>

            <div class="weight-history">
                <h3>📈 Weight History & Analytics</h3>
                
                <div class="weight-stats" id="weight-stats">
                    <!-- Stats will be populated dynamically -->
                </div>
                
                <div class="weight-chart-container" id="weight-chart">
                    <div class="chart-placeholder">
                        <h4>📊 Weight Progress Chart</h4>
                        <p>Log your first weight entry to see your progress chart</p>
                    </div>
                </div>
                
                <div class="weight-entries" id="weight-entries">
                    <!-- Weight entries will be populated here -->
                </div>
            </div>

            <div class="family-weight-section">
                <h3>👨‍👩‍👧‍👦 Family Weight Progress</h3>
                <div class="family-members" id="family-members">
                    <!-- Family member weight data -->
                </div>
            </div>

            <div class="weight-challenges">
                <h3>🏆 Weight Challenges</h3>
                <div id="weight-challenges-list">
                    <!-- Active weight challenges -->
                </div>
            </div>
        `;

        // Insert into DOM if not already present
        if (!document.getElementById('weight-tracker-container')) {
            document.body.appendChild(container);
        }
    }

    bindEvents() {
        // Unit selector
        document.querySelectorAll('.unit-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.unit-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.selectedUnit = e.target.dataset.unit;
                this.updateGoalDifference();
            });
        });

        // Privacy selector
        document.querySelectorAll('.privacy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.privacy-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.privacyLevel = e.target.dataset.privacy;
            });
        });

        // Goal weight calculation
        document.getElementById('weight-input').addEventListener('input', () => {
            this.updateGoalDifference();
        });

        document.getElementById('goal-weight').addEventListener('input', () => {
            this.updateGoalDifference();
        });

        // Log weight button
        document.getElementById('log-weight-btn').addEventListener('click', () => {
            this.logWeight();
        });
    }

    updateGoalDifference() {
        const currentWeight = parseFloat(document.getElementById('weight-input').value);
        const goalWeight = parseFloat(document.getElementById('goal-weight').value);
        const differenceSpan = document.getElementById('goal-difference');

        if (currentWeight && goalWeight) {
            const difference = currentWeight - goalWeight;
            const absValue = Math.abs(difference);
            
            if (difference > 0) {
                differenceSpan.innerHTML = `📉 ${absValue.toFixed(1)} ${this.selectedUnit} to lose`;
                differenceSpan.style.color = '#dc3545';
            } else if (difference < 0) {
                differenceSpan.innerHTML = `📈 ${absValue.toFixed(1)} ${this.selectedUnit} to gain`;
                differenceSpan.style.color = '#28a745';
            } else {
                differenceSpan.innerHTML = `🎯 At goal weight!`;
                differenceSpan.style.color = '#007bff';
            }
        } else {
            differenceSpan.innerHTML = 'Set your goal weight';
            differenceSpan.style.color = '#6c757d';
        }
    }

    async logWeight() {
        const weight = parseFloat(document.getElementById('weight-input').value);
        const notes = document.getElementById('weight-notes-input').value;
        const goalWeight = parseFloat(document.getElementById('goal-weight').value);
        
        if (!weight) {
            this.showMessage('Please enter your weight', 'error');
            return;
        }

        const weightData = {
            user_id: this.currentUser,
            weight: weight,
            unit: this.selectedUnit,
            notes: notes,
            goal_weight: goalWeight || null,
            share_with_groups: this.shareWithGroups,
            privacy_level: this.privacyLevel
        };

        try {
            document.getElementById('log-weight-btn').textContent = '⏳ Logging...';
            
            const response = await fetch(`${this.apiBase}/api/weight/log`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(weightData)
            });

            const result = await response.json();

            if (result.success) {
                this.showMessage(`✅ Weight logged successfully! ${result.message}`, 'success');
                document.querySelector('.weight-tracker').classList.add('weight-logged');
                
                // Clear form
                document.getElementById('weight-input').value = '';
                document.getElementById('weight-notes-input').value = '';
                
                // Refresh history
                setTimeout(() => {
                    this.loadWeightHistory();
                    document.querySelector('.weight-tracker').classList.remove('weight-logged');
                }, 600);
                
            } else {
                this.showMessage(`❌ Error: ${result.message}`, 'error');
            }
        } catch (error) {
            this.showMessage(`❌ Network error: ${error.message}`, 'error');
        } finally {
            document.getElementById('log-weight-btn').textContent = '📝 Log Weight';
        }
    }

    async loadWeightHistory() {
        try {
            const response = await fetch(`${this.apiBase}/api/weight/history/${this.currentUser}`);
            const data = await response.json();
            
            if (data.success) {
                this.weightHistory = data.weight_entries;
                this.renderWeightHistory();
                this.renderWeightStats(data.analytics);
                this.renderChart();
            }
        } catch (error) {
            console.error('Failed to load weight history:', error);
        }
    }

    renderWeightHistory() {
        const entriesContainer = document.getElementById('weight-entries');
        
        if (this.weightHistory.length === 0) {
            entriesContainer.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #6c757d;">
                    <h4>📝 No weight entries yet</h4>
                    <p>Log your first weight to start tracking progress!</p>
                </div>
            `;
            return;
        }

        const entriesHTML = this.weightHistory.map((entry, index) => {
            const prevEntry = this.weightHistory[index + 1];
            let changeHTML = '<span class="entry-change neutral">First entry</span>';
            
            if (prevEntry) {
                const change = entry.weight - prevEntry.weight;
                const changeClass = change > 0 ? 'positive' : change < 0 ? 'negative' : 'neutral';
                const changeIcon = change > 0 ? '📈' : change < 0 ? '📉' : '➡️';
                const changeText = change !== 0 ? `${changeIcon} ${Math.abs(change).toFixed(1)} ${entry.unit}` : '➡️ No change';
                changeHTML = `<span class="entry-change ${changeClass}">${changeText}</span>`;
            }
            
            return `
                <div class="weight-entry">
                    <div class="entry-date">
                        📅 ${new Date(entry.logged_at).toLocaleDateString()}
                        <br>
                        <small>${new Date(entry.logged_at).toLocaleTimeString()}</small>
                        ${entry.notes ? `<br><em>"${entry.notes}"</em>` : ''}
                    </div>
                    <div class="entry-weight">
                        ${entry.weight} ${entry.unit}
                    </div>
                    ${changeHTML}
                </div>
            `;
        }).join('');

        entriesContainer.innerHTML = entriesHTML;
    }

    renderWeightStats(analytics) {
        const statsContainer = document.getElementById('weight-stats');
        
        if (!analytics || this.weightHistory.length === 0) {
            statsContainer.innerHTML = '';
            return;
        }

        statsContainer.innerHTML = `
            <div class="stat-card">
                <div class="stat-value">${analytics.current_weight.toFixed(1)}</div>
                <div class="stat-label">Current Weight</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: ${analytics.total_change >= 0 ? '#dc3545' : '#28a745'}">
                    ${analytics.total_change >= 0 ? '+' : ''}${analytics.total_change.toFixed(1)}
                </div>
                <div class="stat-label">Total Change</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${analytics.entries_count}</div>
                <div class="stat-label">Total Entries</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${analytics.streak_days}</div>
                <div class="stat-label">Day Streak</div>
            </div>
        `;
    }

    renderChart() {
        const chartContainer = document.getElementById('weight-chart');
        
        if (this.weightHistory.length < 2) {
            chartContainer.innerHTML = `
                <div class="chart-placeholder">
                    <h4>📊 Weight Progress Chart</h4>
                    <p>Add more weight entries to see your progress chart</p>
                </div>
            `;
            return;
        }

        // Simple ASCII-style chart for demonstration
        const weights = this.weightHistory.slice().reverse().map(entry => entry.weight);
        const dates = this.weightHistory.slice().reverse().map(entry => 
            new Date(entry.logged_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
        );

        const minWeight = Math.min(...weights);
        const maxWeight = Math.max(...weights);
        const range = maxWeight - minWeight || 1;

        let chartHTML = '<div style="padding: 20px;">';
        chartHTML += '<div style="display: flex; align-items: end; height: 200px; gap: 10px; margin-bottom: 20px;">';
        
        weights.forEach((weight, index) => {
            const height = ((weight - minWeight) / range) * 180 + 20;
            const isLatest = index === weights.length - 1;
            chartHTML += `
                <div style="
                    flex: 1; 
                    height: ${height}px; 
                    background: ${isLatest ? 'linear-gradient(45deg, #007bff, #00c6ff)' : 'linear-gradient(45deg, #6c757d, #adb5bd)'};
                    border-radius: 4px 4px 0 0;
                    position: relative;
                    display: flex;
                    align-items: end;
                    justify-content: center;
                    color: white;
                    font-size: 0.8em;
                    font-weight: bold;
                ">
                    ${weight}
                </div>
            `;
        });
        
        chartHTML += '</div>';
        chartHTML += '<div style="display: flex; gap: 10px; font-size: 0.8em; color: #6c757d;">';
        dates.forEach(date => {
            chartHTML += `<div style="flex: 1; text-align: center;">${date}</div>`;
        });
        chartHTML += '</div></div>';

        chartContainer.innerHTML = chartHTML;
    }

    showMessage(message, type) {
        const messageContainer = document.getElementById('weight-message');
        messageContainer.innerHTML = `<div class="${type}-message">${message}</div>`;
        
        setTimeout(() => {
            messageContainer.innerHTML = '';
        }, 5000);
    }

    // Load demo family data
    loadFamilyData() {
        const familyContainer = document.getElementById('family-members');
        
        // Demo family data
        const familyData = [
            { name: 'Dad', weight: '85.2 kg', trend: 'down', change: '-2.1 kg this month' },
            { name: 'Mom', weight: '62.8 kg', trend: 'stable', change: 'Maintaining goal weight' },
            { name: 'You', weight: '75.5 kg', trend: 'down', change: '-1.5 kg this month' },
            { name: 'Sister', weight: '58.3 kg', trend: 'up', change: '+0.8 kg this month' }
        ];

        const familyHTML = familyData.map(member => `
            <div class="member-card">
                <div class="member-name">${member.name}</div>
                <div class="member-weight">${member.weight}</div>
                <div class="member-trend ${member.trend}">${member.change}</div>
            </div>
        `).join('');

        familyContainer.innerHTML = familyHTML;
    }

    // Load demo challenges
    loadWeightChallenges() {
        const challengesContainer = document.getElementById('weight-challenges-list');
        
        const challenges = [
            {
                title: 'Family Weight Loss Challenge',
                progress: 65,
                goal: 'Lose 20 kg combined as a family',
                current: '13 kg lost so far'
            },
            {
                title: 'Consistency Challenge',
                progress: 80,
                goal: 'Log weight 5 times this week',
                current: '4 out of 5 days completed'
            }
        ];

        const challengesHTML = challenges.map(challenge => `
            <div class="challenge-card">
                <div class="challenge-title">${challenge.title}</div>
                <div class="challenge-progress">
                    <div class="challenge-progress-bar" style="width: ${challenge.progress}%"></div>
                </div>
                <div class="challenge-stats">
                    <span>${challenge.current}</span>
                    <span>${challenge.progress}%</span>
                </div>
            </div>
        `).join('');

        challengesContainer.innerHTML = challengesHTML;
    }
}

// Initialize weight tracker when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const weightTracker = new WeightTracker();
    
    // Load demo data
    setTimeout(() => {
        weightTracker.loadFamilyData();
        weightTracker.loadWeightChallenges();
    }, 1000);
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WeightTracker;
}