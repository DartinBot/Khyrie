import React, { useState, useEffect } from 'react';
import './StrengthTraining.css';

const StrengthTraining = () => {
  const [strengthData, setStrengthData] = useState(null);
  const [selectedExercise, setSelectedExercise] = useState('ex_001');
  const [workoutProgram, setWorkoutProgram] = useState(null);
  const [currentSession, setCurrentSession] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const userId = 'user_001'; // In real app, get from auth context
  
  const exercises = [
    { id: 'ex_001', name: 'Squat', category: 'Legs' },
    { id: 'ex_002', name: 'Bench Press', category: 'Chest' },
    { id: 'deadlift', name: 'Deadlift', category: 'Back' },
    { id: 'overhead_press', name: 'Overhead Press', category: 'Shoulders' }
  ];

  useEffect(() => {
    loadStrengthData();
  }, [selectedExercise]);

  const loadStrengthData = async () => {
    try {
      setLoading(true);
      
      // Load strength standards
      const response = await fetch(`/api/advanced/strength/standards/${userId}/${selectedExercise}`);
      if (response.ok) {
        const data = await response.json();
        setStrengthData(data);
      }
    } catch (err) {
      console.error('Error loading strength data:', err);
    } finally {
      setLoading(false);
    }
  };

  const generateProgram = async () => {
    try {
      setLoading(true);
      
      const response = await fetch('/api/advanced/programs/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          goals: ['strength', 'muscle_gain'],
          available_days: 4,
          session_length: 75
        })
      });
      
      if (response.ok) {
        const program = await response.json();
        setWorkoutProgram(program);
      }
    } catch (err) {
      console.error('Error generating program:', err);
    } finally {
      setLoading(false);
    }
  };

  const startWorkout = () => {
    setCurrentSession({
      id: Date.now(),
      started_at: new Date().toISOString(),
      exercises: [],
      current_exercise: 0
    });
  };

  const StrengthStandardsCard = ({ data }) => {
    if (!data) return null;

    const getNextLevelProgress = () => {
      const nextGoal = data.next_goal;
      if (!nextGoal) return 100;
      
      return Math.min((data.ratio / nextGoal.target_ratio) * 100, 100);
    };

    const getLevelColor = (level) => {
      const colors = {
        'untrained': '#ff6b6b',
        'beginner': '#feca57',
        'novice': '#48dbfb',
        'intermediate': '#0abde3',
        'advanced': '#00d2d3',
        'elite': '#ff9ff3'
      };
      return colors[level] || '#666';
    };

    return (
      <div className="strength-standards-card">
        <h3>💪 Strength Standards - {exercises.find(e => e.id === selectedExercise)?.name}</h3>
        
        <div className="current-stats">
          <div className="stat-item">
            <label>Current 1RM</label>
            <span className="stat-value">{data.current_1rm} kg</span>
          </div>
          <div className="stat-item">
            <label>Bodyweight</label>
            <span className="stat-value">{data.bodyweight} kg</span>
          </div>
          <div className="stat-item">
            <label>Ratio</label>
            <span className="stat-value">{data.ratio}x</span>
          </div>
        </div>

        <div className="strength-level">
          <div className="level-badge" style={{ backgroundColor: getLevelColor(data.level) }}>
            {data.level.toUpperCase()}
          </div>
          <div className="percentile">
            {data.percentile}th percentile
          </div>
        </div>

        {data.next_goal && (
          <div className="next-goal">
            <h4>Next Goal: {data.next_goal.level.toUpperCase()}</h4>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${getNextLevelProgress()}%` }}
              ></div>
            </div>
            <p>
              Target: {data.next_goal.target_ratio}x bodyweight 
              ({Math.round(data.next_goal.percentage_to_goal)}% complete)
            </p>
          </div>
        )}

        <div className="standards-breakdown">
          <h4>All Standards (Bodyweight Multiples)</h4>
          <div className="standards-grid">
            {Object.entries(data.standards).map(([level, ratio]) => (
              <div 
                key={level} 
                className={`standard-item ${data.level === level ? 'current' : ''}`}
              >
                <span className="level-name">{level}</span>
                <span className="level-ratio">{ratio}x</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const WorkoutProgramCard = ({ program }) => {
    if (!program) return null;

    return (
      <div className="workout-program-card">
        <h3>🎯 AI Generated Program</h3>
        <div className="program-overview">
          <div className="program-stat">
            <label>Duration</label>
            <span>{program.duration_weeks} weeks</span>
          </div>
          <div className="program-stat">
            <label>Frequency</label>
            <span>{program.frequency_per_week}x per week</span>
          </div>
          <div className="program-stat">
            <label>Total Workouts</label>
            <span>{program.total_workouts}</span>
          </div>
        </div>
        
        <div className="program-actions">
          <button className="btn-primary" onClick={startWorkout}>
            🏋️ Start Workout
          </button>
          <button className="btn-secondary">
            📋 View Full Program
          </button>
        </div>
      </div>
    );
  };

  const CurrentWorkoutSession = ({ session }) => {
    if (!session) return null;

    const addSet = () => {
      // In real app, this would track sets and reps
      console.log('Adding set...');
    };

    return (
      <div className="current-workout-session">
        <h3>🔥 Current Workout Session</h3>
        <div className="session-timer">
          <span>Started: {new Date(session.started_at).toLocaleTimeString()}</span>
        </div>
        
        <div className="exercise-tracker">
          <div className="current-exercise">
            <h4>{exercises[0]?.name || 'Squat'}</h4>
            <div className="set-input-group">
              <input type="number" placeholder="Weight (kg)" className="weight-input" />
              <input type="number" placeholder="Reps" className="reps-input" />
              <button className="add-set-btn" onClick={addSet}>Add Set</button>
            </div>
          </div>
          
          <div className="completed-sets">
            <h5>Completed Sets:</h5>
            <div className="sets-list">
              <div className="set-item">Set 1: 100kg × 5 reps</div>
              <div className="set-item">Set 2: 105kg × 5 reps</div>
              <div className="set-item">Set 3: 110kg × 3 reps</div>
            </div>
          </div>
        </div>
        
        <div className="session-actions">
          <button className="btn-primary">Next Exercise</button>
          <button className="btn-secondary">Rest Timer</button>
          <button className="btn-danger">End Workout</button>
        </div>
      </div>
    );
  };

  return (
    <div className="strength-training">
      <header className="strength-header">
        <h1>💪 Strength Training Hub</h1>
        <p>Track progress, analyze standards, and optimize your strength</p>
      </header>

      {/* Exercise Selector */}
      <section className="exercise-selector">
        <h2>📊 Select Exercise</h2>
        <div className="exercise-tabs">
          {exercises.map(exercise => (
            <button
              key={exercise.id}
              className={`exercise-tab ${selectedExercise === exercise.id ? 'active' : ''}`}
              onClick={() => setSelectedExercise(exercise.id)}
            >
              {exercise.name}
              <span className="category">{exercise.category}</span>
            </button>
          ))}
        </div>
      </section>

      {loading && (
        <div className="loading-section">
          <div className="loading-spinner"></div>
          <p>Loading strength data...</p>
        </div>
      )}

      {/* Main Content Grid */}
      <div className="strength-grid">
        {/* Strength Standards */}
        <StrengthStandardsCard data={strengthData} />

        {/* Workout Program */}
        <div className="program-section">
          {workoutProgram ? (
            <WorkoutProgramCard program={workoutProgram} />
          ) : (
            <div className="generate-program-card">
              <h3>🎯 Generate AI Program</h3>
              <p>Create a personalized strength training program based on your goals and current level.</p>
              <button className="btn-primary" onClick={generateProgram} disabled={loading}>
                {loading ? 'Generating...' : '🤖 Generate Program'}
              </button>
            </div>
          )}
        </div>

        {/* Current Workout Session */}
        {currentSession ? (
          <CurrentWorkoutSession session={currentSession} />
        ) : (
          <div className="start-workout-card">
            <h3>🏋️ Quick Start Workout</h3>
            <p>Begin a strength training session with real-time tracking.</p>
            <button className="btn-primary" onClick={startWorkout}>
              Start Training Session
            </button>
          </div>
        )}

        {/* Progress Chart */}
        <div className="progress-chart-card">
          <h3>📈 Strength Progress</h3>
          <div className="chart-placeholder">
            <div className="chart-bar" style={{ height: '60%' }}>
              <span>Jan</span>
            </div>
            <div className="chart-bar" style={{ height: '70%' }}>
              <span>Feb</span>
            </div>
            <div className="chart-bar" style={{ height: '75%' }}>
              <span>Mar</span>
            </div>
            <div className="chart-bar" style={{ height: '85%' }}>
              <span>Apr</span>
            </div>
            <div className="chart-bar" style={{ height: '90%' }}>
              <span>May</span>
            </div>
          </div>
          <p>5-month progression overview</p>
        </div>

        {/* Calculator Tools */}
        <div className="calculator-tools">
          <h3>🧮 Training Calculators</h3>
          <div className="calculator-grid">
            <button className="calculator-btn">
              <span>📊</span>
              1RM Calculator
            </button>
            <button className="calculator-btn">
              <span>📈</span>
              Volume Calculator
            </button>
            <button className="calculator-btn">
              <span>⚖️</span>
              Plate Calculator
            </button>
            <button className="calculator-btn">
              <span>🎯</span>
              RPE Calculator
            </button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="quick-actions-card">
          <h3>⚡ Quick Actions</h3>
          <div className="action-buttons">
            <button className="action-btn">
              📝 Log Previous Workout
            </button>
            <button className="action-btn">
              📊 View Analytics
            </button>
            <button className="action-btn">
              🎯 Set New Goals
            </button>
            <button className="action-btn">
              👥 Share Progress
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StrengthTraining;