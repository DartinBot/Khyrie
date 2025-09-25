import React, { useState, useEffect } from 'react';
import './SharedWorkout.css';

const SharedWorkout = () => {
  const [workoutName, setWorkoutName] = useState('');
  const [workoutType, setWorkoutType] = useState('strength');
  const [difficulty, setDifficulty] = useState('intermediate');
  const [estimatedDuration, setEstimatedDuration] = useState(60);
  const [description, setDescription] = useState('');
  const [exercises, setExercises] = useState([]);
  const [shareWithGroups, setShareWithGroups] = useState([]);
  const [userGroups, setUserGroups] = useState([]);
  const [tags, setTags] = useState([]);
  const [currentTag, setCurrentTag] = useState('');
  
  // Mock user ID - would come from authentication
  const userId = 'user123';

  useEffect(() => {
    loadUserGroups();
  }, []);

  const loadUserGroups = async () => {
    try {
      const response = await fetch(`/api/groups/user/${userId}`);
      const data = await response.json();
      setUserGroups(data.user_groups || []);
    } catch (error) {
      console.error('Error loading user groups:', error);
    }
  };

  const addExercise = () => {
    setExercises([...exercises, {
      name: '',
      sets: 3,
      reps: 12,
      weight: '',
      duration: '',
      rest_seconds: 60,
      notes: ''
    }]);
  };

  const updateExercise = (index, field, value) => {
    const updatedExercises = exercises.map((exercise, i) => {
      if (i === index) {
        return { ...exercise, [field]: value };
      }
      return exercise;
    });
    setExercises(updatedExercises);
  };

  const removeExercise = (index) => {
    setExercises(exercises.filter((_, i) => i !== index));
  };

  const addTag = () => {
    if (currentTag.trim() && !tags.includes(currentTag.trim())) {
      setTags([...tags, currentTag.trim()]);
      setCurrentTag('');
    }
  };

  const removeTag = (tagToRemove) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!workoutName || exercises.length === 0) {
      alert('Please provide a workout name and at least one exercise.');
      return;
    }

    try {
      const response = await fetch('/api/workouts/shared/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          creator_id: userId,
          workout_name: workoutName,
          workout_type: workoutType,
          exercises: exercises,
          share_with_groups: shareWithGroups,
          difficulty: difficulty,
          estimated_duration: estimatedDuration,
          description: description,
          tags: tags
        })
      });

      const result = await response.json();
      
      if (result.workout_created) {
        alert('Shared workout created successfully!');
        // Reset form
        setWorkoutName('');
        setDescription('');
        setExercises([]);
        setShareWithGroups([]);
        setTags([]);
      } else {
        alert('Error creating workout: ' + (result.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error creating shared workout:', error);
      alert('Error creating workout. Please try again.');
    }
  };

  const popularExercises = {
    strength: [
      'Bench Press', 'Squat', 'Deadlift', 'Overhead Press', 'Pull-ups',
      'Push-ups', 'Dumbbell Rows', 'Lunges', 'Dips', 'Bicep Curls'
    ],
    cardio: [
      'Running', 'Cycling', 'Rowing', 'Jump Rope', 'Burpees',
      'Mountain Climbers', 'High Knees', 'Jumping Jacks', 'Sprint Intervals'
    ],
    yoga: [
      'Downward Dog', 'Warrior I', 'Warrior II', 'Child\'s Pose', 'Cat-Cow',
      'Plank', 'Tree Pose', 'Triangle Pose', 'Cobra', 'Bridge'
    ],
    flexibility: [
      'Hamstring Stretch', 'Quad Stretch', 'Shoulder Stretch', 'Hip Flexor Stretch',
      'Calf Stretch', 'Chest Stretch', 'Back Stretch', 'Neck Stretch'
    ]
  };

  const addPopularExercise = (exerciseName) => {
    const newExercise = {
      name: exerciseName,
      sets: workoutType === 'strength' ? 3 : 1,
      reps: workoutType === 'strength' ? 12 : 1,
      weight: '',
      duration: workoutType === 'cardio' ? 300 : '', // 5 minutes for cardio
      rest_seconds: workoutType === 'strength' ? 60 : 30,
      notes: ''
    };
    setExercises([...exercises, newExercise]);
  };

  return (
    <div className="shared-workout-creator">
      <div className="creator-header">
        <h2>Create Shared Workout</h2>
        <p>Build a workout to share with your family and friends</p>
      </div>

      <form onSubmit={handleSubmit} className="workout-form">
        {/* Basic Information */}
        <div className="form-section">
          <h3>Basic Information</h3>
          <div className="form-grid">
            <div className="form-group">
              <label>Workout Name *</label>
              <input
                type="text"
                value={workoutName}
                onChange={(e) => setWorkoutName(e.target.value)}
                placeholder="e.g., Family Morning Strength"
                required
              />
            </div>

            <div className="form-group">
              <label>Type</label>
              <select value={workoutType} onChange={(e) => setWorkoutType(e.target.value)}>
                <option value="strength">Strength Training</option>
                <option value="cardio">Cardio</option>
                <option value="yoga">Yoga</option>
                <option value="hiit">HIIT</option>
                <option value="flexibility">Flexibility</option>
                <option value="mixed">Mixed</option>
              </select>
            </div>

            <div className="form-group">
              <label>Difficulty</label>
              <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            <div className="form-group">
              <label>Estimated Duration (minutes)</label>
              <input
                type="number"
                value={estimatedDuration}
                onChange={(e) => setEstimatedDuration(parseInt(e.target.value))}
                min="15"
                max="180"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe the workout goals, focus areas, or any special instructions..."
              rows="3"
            />
          </div>
        </div>

        {/* Share Settings */}
        <div className="form-section">
          <h3>Share With Groups</h3>
          <div className="groups-selection">
            {userGroups.map((group) => (
              <label key={group.group_id} className="group-checkbox">
                <input
                  type="checkbox"
                  checked={shareWithGroups.includes(group.group_id)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setShareWithGroups([...shareWithGroups, group.group_id]);
                    } else {
                      setShareWithGroups(shareWithGroups.filter(id => id !== group.group_id));
                    }
                  }}
                />
                <div className="group-info">
                  <div className="group-name">{group.name}</div>
                  <div className="group-details">{group.member_count} members • {group.type}</div>
                </div>
              </label>
            ))}
          </div>
        </div>

        {/* Exercise Builder */}
        <div className="form-section">
          <div className="section-header">
            <h3>Exercises</h3>
            <button type="button" className="add-exercise-btn" onClick={addExercise}>
              + Add Exercise
            </button>
          </div>

          {/* Popular Exercises */}
          <div className="popular-exercises">
            <h4>Quick Add Popular Exercises:</h4>
            <div className="exercise-chips">
              {popularExercises[workoutType]?.map((exercise, index) => (
                <button
                  key={index}
                  type="button"
                  className="exercise-chip"
                  onClick={() => addPopularExercise(exercise)}
                >
                  {exercise}
                </button>
              ))}
            </div>
          </div>

          {/* Exercise List */}
          <div className="exercises-list">
            {exercises.map((exercise, index) => (
              <div key={index} className="exercise-item">
                <div className="exercise-header">
                  <span className="exercise-number">{index + 1}</span>
                  <input
                    type="text"
                    placeholder="Exercise name"
                    value={exercise.name}
                    onChange={(e) => updateExercise(index, 'name', e.target.value)}
                    className="exercise-name-input"
                  />
                  <button
                    type="button"
                    className="remove-exercise"
                    onClick={() => removeExercise(index)}
                  >
                    ✕
                  </button>
                </div>

                <div className="exercise-details">
                  {workoutType === 'strength' && (
                    <>
                      <div className="detail-group">
                        <label>Sets</label>
                        <input
                          type="number"
                          value={exercise.sets}
                          onChange={(e) => updateExercise(index, 'sets', parseInt(e.target.value))}
                          min="1"
                        />
                      </div>
                      <div className="detail-group">
                        <label>Reps</label>
                        <input
                          type="number"
                          value={exercise.reps}
                          onChange={(e) => updateExercise(index, 'reps', parseInt(e.target.value))}
                          min="1"
                        />
                      </div>
                      <div className="detail-group">
                        <label>Weight</label>
                        <input
                          type="text"
                          value={exercise.weight}
                          onChange={(e) => updateExercise(index, 'weight', e.target.value)}
                          placeholder="e.g., 135 lbs, BW"
                        />
                      </div>
                    </>
                  )}

                  {(workoutType === 'cardio' || workoutType === 'yoga' || workoutType === 'hiit') && (
                    <div className="detail-group">
                      <label>Duration (seconds)</label>
                      <input
                        type="number"
                        value={exercise.duration}
                        onChange={(e) => updateExercise(index, 'duration', parseInt(e.target.value))}
                        min="10"
                      />
                    </div>
                  )}

                  <div className="detail-group">
                    <label>Rest (seconds)</label>
                    <input
                      type="number"
                      value={exercise.rest_seconds}
                      onChange={(e) => updateExercise(index, 'rest_seconds', parseInt(e.target.value))}
                      min="0"
                    />
                  </div>

                  <div className="detail-group full-width">
                    <label>Notes</label>
                    <input
                      type="text"
                      value={exercise.notes}
                      onChange={(e) => updateExercise(index, 'notes', e.target.value)}
                      placeholder="Form cues, modifications, etc."
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>

          {exercises.length === 0 && (
            <div className="no-exercises">
              <p>No exercises added yet. Click "Add Exercise" or select from popular exercises above.</p>
            </div>
          )}
        </div>

        {/* Tags */}
        <div className="form-section">
          <h3>Tags</h3>
          <div className="tags-input">
            <div className="tags-list">
              {tags.map((tag, index) => (
                <span key={index} className="tag">
                  {tag}
                  <button type="button" onClick={() => removeTag(tag)}>✕</button>
                </span>
              ))}
            </div>
            <div className="add-tag">
              <input
                type="text"
                value={currentTag}
                onChange={(e) => setCurrentTag(e.target.value)}
                placeholder="Add tag (e.g., upper-body, family-friendly)"
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
              />
              <button type="button" onClick={addTag}>Add</button>
            </div>
          </div>
        </div>

        {/* Submit */}
        <div className="form-actions">
          <button type="submit" className="submit-btn">
            Create Shared Workout
          </button>
          <div className="workout-summary">
            <p>{exercises.length} exercises • ~{estimatedDuration} minutes • {shareWithGroups.length} groups</p>
          </div>
        </div>
      </form>
    </div>
  );
};

export default SharedWorkout;