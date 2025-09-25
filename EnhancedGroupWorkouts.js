import React, { useState, useEffect } from 'react';
import './EnhancedGroupWorkouts.css';

const EnhancedGroupWorkouts = () => {
  const [activeTab, setActiveTab] = useState('schedule');
  const [userLocation, setUserLocation] = useState(null);
  const [userRole, setUserRole] = useState('participant');
  const [groupId, setGroupId] = useState('group_123');
  const [userId, setUserId] = useState('user_456');
  
  // Schedule state
  const [scheduleData, setScheduleData] = useState({
    title: '',
    description: '',
    workout_id: '',
    schedule_type: 'one_time',
    start_datetime: '',
    end_datetime: '',
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    max_participants: null,
    registration_required: false,
    location: {
      name: '',
      address: '',
      latitude: null,
      longitude: null,
      location_type: 'virtual',
      capacity: null,
      amenities: [],
      access_instructions: '',
      safety_notes: ''
    },
    video_session: {
      provider: 'jitsi',
      recording_enabled: false,
      screen_sharing_enabled: true,
      chat_enabled: true,
      max_participants: 100
    },
    reminder_settings: {
      email_reminder: true,
      push_notification: true,
      reminder_times: [24, 2]
    }
  });

  const [nearbyWorkouts, setNearbyWorkouts] = useState([]);
  const [groupSchedule, setGroupSchedule] = useState([]);
  const [videoSession, setVideoSession] = useState(null);
  const [permissions, setPermissions] = useState({});

  useEffect(() => {
    // Get user location for nearby workouts
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy
          });
        },
        (error) => {
          console.error('Error getting location:', error);
        }
      );
    }

    // Load user permissions and group schedule
    loadUserPermissions();
    loadGroupSchedule();
  }, [groupId, userId]);

  useEffect(() => {
    if (userLocation && activeTab === 'nearby') {
      loadNearbyWorkouts();
    }
  }, [userLocation, activeTab]);

  const loadUserPermissions = async () => {
    try {
      const response = await fetch(`/api/groups/enhanced/permissions/${groupId}/${userId}`);
      const data = await response.json();
      if (data.permissions) {
        setPermissions(data.permissions);
        setUserRole(data.role);
      }
    } catch (error) {
      console.error('Error loading permissions:', error);
    }
  };

  const loadGroupSchedule = async () => {
    try {
      const response = await fetch(`/api/groups/enhanced/schedule/${groupId}?days_ahead=30`);
      const data = await response.json();
      setGroupSchedule(data.schedules || []);
    } catch (error) {
      console.error('Error loading schedule:', error);
    }
  };

  const loadNearbyWorkouts = async () => {
    if (!userLocation) return;
    
    try {
      const response = await fetch(
        `/api/groups/enhanced/nearby?latitude=${userLocation.latitude}&longitude=${userLocation.longitude}&radius=10`
      );
      const data = await response.json();
      setNearbyWorkouts(data.nearby_workouts || []);
    } catch (error) {
      console.error('Error loading nearby workouts:', error);
    }
  };

  const createWorkoutSchedule = async () => {
    if (!permissions.can_schedule_workouts) {
      alert('You do not have permission to schedule workouts');
      return;
    }

    try {
      const response = await fetch('/api/groups/enhanced/schedule', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          group_id: groupId,
          creator_id: userId,
          ...scheduleData
        })
      });

      const result = await response.json();
      
      if (result.success) {
        alert('Workout scheduled successfully!');
        loadGroupSchedule();
        // Reset form
        setScheduleData({
          ...scheduleData,
          title: '',
          description: '',
          start_datetime: '',
          end_datetime: ''
        });
      } else {
        alert(result.error || 'Failed to schedule workout');
      }
    } catch (error) {
      console.error('Error creating schedule:', error);
      alert('Error creating schedule');
    }
  };

  const checkInToWorkout = async (scheduleId) => {
    if (!userLocation) {
      alert('Location access required for check-in');
      return;
    }

    try {
      const response = await fetch('/api/groups/enhanced/checkin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          schedule_id: scheduleId,
          user_id: userId,
          location: userLocation
        })
      });

      const result = await response.json();
      
      if (result.success) {
        alert(result.message);
        loadGroupSchedule();
      } else {
        alert(result.error || 'Check-in failed');
      }
    } catch (error) {
      console.error('Error checking in:', error);
      alert('Error during check-in');
    }
  };

  const startVideoSession = async (scheduleId) => {
    if (!permissions.can_start_video_calls) {
      alert('You do not have permission to start video calls');
      return;
    }

    try {
      const response = await fetch('/api/groups/enhanced/video/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          schedule_id: scheduleId,
          host_id: userId
        })
      });

      const result = await response.json();
      
      if (result.success) {
        setVideoSession(result.video_session);
        // Open video session in new window
        window.open(result.video_session.meeting_url, '_blank');
      } else {
        alert(result.error || 'Failed to start video session');
      }
    } catch (error) {
      console.error('Error starting video session:', error);
      alert('Error starting video session');
    }
  };

  const formatDateTime = (isoString) => {
    return new Date(isoString).toLocaleString();
  };

  const getRoleBadgeColor = (role) => {
    const colors = {
      owner: '#ff6b35',
      trainer: '#f7931e',
      moderator: '#4ecdc4',
      participant: '#45b7d1',
      guest: '#96ceb4'
    };
    return colors[role] || '#999';
  };

  return (
    <div className="enhanced-group-workouts">
      <div className="header">
        <h1>Enhanced Group Workouts</h1>
        <div className="role-badge" style={{ backgroundColor: getRoleBadgeColor(userRole) }}>
          {userRole.charAt(0).toUpperCase() + userRole.slice(1)}
        </div>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'schedule' ? 'active' : ''}`}
          onClick={() => setActiveTab('schedule')}
        >
          Schedule Workout
        </button>
        <button 
          className={`tab ${activeTab === 'calendar' ? 'active' : ''}`}
          onClick={() => setActiveTab('calendar')}
        >
          Group Calendar
        </button>
        <button 
          className={`tab ${activeTab === 'nearby' ? 'active' : ''}`}
          onClick={() => setActiveTab('nearby')}
        >
          Nearby Workouts
        </button>
        <button 
          className={`tab ${activeTab === 'video' ? 'active' : ''}`}
          onClick={() => setActiveTab('video')}
        >
          Virtual Sessions
        </button>
      </div>

      <div className="tab-content">
        {/* Schedule Workout Tab */}
        {activeTab === 'schedule' && (
          <div className="schedule-workout">
            {!permissions.can_schedule_workouts ? (
              <div className="permission-notice">
                <p>You need Trainer or higher permissions to schedule workouts.</p>
                <p>Contact a group owner or trainer for access.</p>
              </div>
            ) : (
              <div className="schedule-form">
                <h2>Create Advanced Workout Schedule</h2>
                
                <div className="form-row">
                  <div className="form-group">
                    <label>Workout Title</label>
                    <input
                      type="text"
                      value={scheduleData.title}
                      onChange={(e) => setScheduleData({...scheduleData, title: e.target.value})}
                      placeholder="Morning HIIT Session"
                    />
                  </div>
                  <div className="form-group">
                    <label>Schedule Type</label>
                    <select
                      value={scheduleData.schedule_type}
                      onChange={(e) => setScheduleData({...scheduleData, schedule_type: e.target.value})}
                    >
                      <option value="one_time">One Time</option>
                      <option value="recurring_daily">Daily</option>
                      <option value="recurring_weekly">Weekly</option>
                      <option value="recurring_monthly">Monthly</option>
                    </select>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Start Date & Time</label>
                    <input
                      type="datetime-local"
                      value={scheduleData.start_datetime}
                      onChange={(e) => setScheduleData({...scheduleData, start_datetime: e.target.value})}
                    />
                  </div>
                  <div className="form-group">
                    <label>End Date & Time</label>
                    <input
                      type="datetime-local"
                      value={scheduleData.end_datetime}
                      onChange={(e) => setScheduleData({...scheduleData, end_datetime: e.target.value})}
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    value={scheduleData.description}
                    onChange={(e) => setScheduleData({...scheduleData, description: e.target.value})}
                    placeholder="Describe the workout and any special instructions..."
                  />
                </div>

                <div className="location-section">
                  <h3>Location Settings</h3>
                  <div className="form-row">
                    <div className="form-group">
                      <label>Location Type</label>
                      <select
                        value={scheduleData.location.location_type}
                        onChange={(e) => setScheduleData({
                          ...scheduleData,
                          location: {...scheduleData.location, location_type: e.target.value}
                        })}
                      >
                        <option value="virtual">Virtual Only</option>
                        <option value="physical">Physical Location</option>
                        <option value="hybrid">Hybrid (Virtual + Physical)</option>
                      </select>
                    </div>
                    {scheduleData.location.location_type !== 'virtual' && (
                      <div className="form-group">
                        <label>Location Name</label>
                        <input
                          type="text"
                          value={scheduleData.location.name}
                          onChange={(e) => setScheduleData({
                            ...scheduleData,
                            location: {...scheduleData.location, name: e.target.value}
                          })}
                          placeholder="Central Park, Gym A, etc."
                        />
                      </div>
                    )}
                  </div>

                  {scheduleData.location.location_type !== 'virtual' && (
                    <div className="form-group">
                      <label>Address</label>
                      <input
                        type="text"
                        value={scheduleData.location.address}
                        onChange={(e) => setScheduleData({
                          ...scheduleData,
                          location: {...scheduleData.location, address: e.target.value}
                        })}
                        placeholder="123 Main St, City, State"
                      />
                    </div>
                  )}
                </div>

                <div className="video-section">
                  <h3>Video Session Settings</h3>
                  <div className="form-row">
                    <div className="form-group">
                      <label>Video Provider</label>
                      <select
                        value={scheduleData.video_session.provider}
                        onChange={(e) => setScheduleData({
                          ...scheduleData,
                          video_session: {...scheduleData.video_session, provider: e.target.value}
                        })}
                      >
                        <option value="jitsi">Jitsi Meet (Free)</option>
                        <option value="zoom">Zoom</option>
                        <option value="google_meet">Google Meet</option>
                        <option value="teams">Microsoft Teams</option>
                      </select>
                    </div>
                    <div className="form-group">
                      <label>Max Participants</label>
                      <input
                        type="number"
                        value={scheduleData.max_participants || ''}
                        onChange={(e) => setScheduleData({...scheduleData, max_participants: e.target.value ? parseInt(e.target.value) : null})}
                        placeholder="Unlimited"
                      />
                    </div>
                  </div>

                  <div className="checkbox-group">
                    <label>
                      <input
                        type="checkbox"
                        checked={scheduleData.video_session.recording_enabled}
                        onChange={(e) => setScheduleData({
                          ...scheduleData,
                          video_session: {...scheduleData.video_session, recording_enabled: e.target.checked}
                        })}
                      />
                      Enable Recording
                    </label>
                    <label>
                      <input
                        type="checkbox"
                        checked={scheduleData.video_session.screen_sharing_enabled}
                        onChange={(e) => setScheduleData({
                          ...scheduleData,
                          video_session: {...scheduleData.video_session, screen_sharing_enabled: e.target.checked}
                        })}
                      />
                      Allow Screen Sharing
                    </label>
                    <label>
                      <input
                        type="checkbox"
                        checked={scheduleData.registration_required}
                        onChange={(e) => setScheduleData({...scheduleData, registration_required: e.target.checked})}
                      />
                      Require Registration
                    </label>
                  </div>
                </div>

                <button className="create-schedule-btn" onClick={createWorkoutSchedule}>
                  Create Workout Schedule
                </button>
              </div>
            )}
          </div>
        )}

        {/* Group Calendar Tab */}
        {activeTab === 'calendar' && (
          <div className="group-calendar">
            <h2>Upcoming Group Workouts</h2>
            <div className="schedule-list">
              {groupSchedule.length === 0 ? (
                <p>No upcoming workouts scheduled.</p>
              ) : (
                groupSchedule.map((workout, index) => (
                  <div key={index} className="workout-card">
                    <div className="workout-header">
                      <h3>{workout.title}</h3>
                      <span className="workout-type">{workout.location_type}</span>
                    </div>
                    <div className="workout-details">
                      <p><strong>When:</strong> {formatDateTime(workout.start_datetime)}</p>
                      <p><strong>Location:</strong> {workout.location_name}</p>
                      {workout.has_video && (
                        <p><strong>Video:</strong> {workout.video_provider}</p>
                      )}
                    </div>
                    <div className="workout-actions">
                      {workout.location_type !== 'virtual' && (
                        <button 
                          className="checkin-btn"
                          onClick={() => checkInToWorkout(workout.schedule_id)}
                        >
                          📍 Check In
                        </button>
                      )}
                      {workout.has_video && permissions.can_start_video_calls && (
                        <button 
                          className="video-btn"
                          onClick={() => startVideoSession(workout.schedule_id)}
                        >
                          🎥 Start Video
                        </button>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {/* Nearby Workouts Tab */}
        {activeTab === 'nearby' && (
          <div className="nearby-workouts">
            <h2>Nearby Group Workouts</h2>
            {!userLocation ? (
              <p>Enable location access to find nearby workouts.</p>
            ) : (
              <div className="nearby-list">
                {nearbyWorkouts.length === 0 ? (
                  <p>No nearby workouts found within 10km.</p>
                ) : (
                  nearbyWorkouts.map((workout, index) => (
                    <div key={index} className="nearby-card">
                      <div className="distance-badge">
                        {workout.distance_km}km away
                      </div>
                      <h3>{workout.title}</h3>
                      <p><strong>When:</strong> {formatDateTime(workout.start_datetime)}</p>
                      <p><strong>Location:</strong> {workout.location_name}</p>
                      <p><strong>Address:</strong> {workout.address}</p>
                      {workout.amenities && workout.amenities.length > 0 && (
                        <p><strong>Amenities:</strong> {workout.amenities.join(', ')}</p>
                      )}
                      <button className="join-btn">Request to Join</button>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        )}

        {/* Virtual Sessions Tab */}
        {activeTab === 'video' && (
          <div className="virtual-sessions">
            <h2>Virtual Workout Sessions</h2>
            
            {videoSession && (
              <div className="active-session">
                <h3>Active Session</h3>
                <div className="session-details">
                  <p><strong>Provider:</strong> {videoSession.provider}</p>
                  <p><strong>Meeting ID:</strong> {videoSession.meeting_id}</p>
                  {videoSession.password && (
                    <p><strong>Password:</strong> {videoSession.password}</p>
                  )}
                  <a 
                    href={videoSession.meeting_url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="join-video-btn"
                  >
                    Join Video Session
                  </a>
                </div>
              </div>
            )}

            <div className="video-features">
              <h3>Video Session Features</h3>
              <ul>
                <li>✅ HD Video & Audio</li>
                <li>✅ Screen Sharing for Workout Demonstrations</li>
                <li>✅ Real-time Chat for Support</li>
                <li>✅ Session Recording (when enabled)</li>
                <li>✅ Breakout Rooms for Small Groups</li>
                <li>✅ Mobile & Desktop Compatible</li>
              </ul>
            </div>

            <div className="provider-info">
              <h3>Supported Video Providers</h3>
              <div className="providers">
                <div className="provider">
                  <strong>Jitsi Meet</strong>
                  <p>Free, open-source, no account required</p>
                </div>
                <div className="provider">
                  <strong>Zoom</strong>
                  <p>Professional meetings with advanced features</p>
                </div>
                <div className="provider">
                  <strong>Google Meet</strong>
                  <p>Integrated with Google services</p>
                </div>
                <div className="provider">
                  <strong>Microsoft Teams</strong>
                  <p>Enterprise-grade with collaboration tools</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EnhancedGroupWorkouts;