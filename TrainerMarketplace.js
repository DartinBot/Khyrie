import React, { useState, useEffect } from 'react';
import './TrainerMarketplace.css';

const TrainerMarketplace = () => {
  const [activeTab, setActiveTab] = useState('browse');
  const [userType, setUserType] = useState('client'); // 'client', 'trainer', or 'new_trainer'
  const [trainers, setTrainers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchFilters, setSearchFilters] = useState({
    specialization: '',
    service_type: '',
    max_price: '',
    min_rating: 3,
    online_only: false,
    in_person_only: false,
    sort_by: 'rating'
  });

  // Trainer registration form state
  const [trainerForm, setTrainerForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    bio: '',
    experience_years: 1,
    hourly_rate_min: 50,
    hourly_rate_max: 150,
    specializations: [],
    certifications: [],
    languages: ['English'],
    availability_schedule: {}
  });

  // Service creation form state
  const [serviceForm, setServiceForm] = useState({
    service_type: 'personal_training',
    title: '',
    description: '',
    duration_minutes: 60,
    price: 75,
    max_participants: 1,
    requirements: '',
    equipment_needed: [],
    online_available: true,
    in_person_available: true,
    location_radius_km: 10
  });

  const [bookingForm, setBookingForm] = useState({
    trainer_id: '',
    service_id: '',
    session_date: '',
    session_notes: ''
  });

  const serviceTypes = [
    { value: 'personal_training', label: '1-on-1 Personal Training' },
    { value: 'group_class', label: 'Group Fitness Class' },
    { value: 'nutrition_coaching', label: 'Nutrition Coaching' },
    { value: 'online_consultation', label: 'Online Consultation' },
    { value: 'program_design', label: 'Custom Program Design' },
    { value: 'form_analysis', label: 'Form Analysis & Correction' },
    { value: 'wellness_coaching', label: 'Wellness & Lifestyle Coaching' },
    { value: 'specialized_training', label: 'Specialized Training' }
  ];

  const specializations = [
    'Weight Loss', 'Muscle Building', 'Strength Training', 'Cardio/Endurance',
    'Yoga', 'Pilates', 'CrossFit', 'Bodybuilding', 'Powerlifting', 'Sports Training',
    'Rehabilitation', 'Senior Fitness', 'Youth Training', 'Nutrition', 'Wellness Coaching'
  ];

  useEffect(() => {
    if (activeTab === 'browse') {
      searchTrainers();
    }
  }, [activeTab, searchFilters]);

  const searchTrainers = async () => {
    setLoading(true);
    try {
      const queryParams = new URLSearchParams();
      
      Object.entries(searchFilters).forEach(([key, value]) => {
        if (value !== '' && value !== false && value !== null) {
          queryParams.append(key, value.toString());
        }
      });

      const response = await fetch(`/api/trainers/search?${queryParams}`);
      const data = await response.json();
      
      if (data.success) {
        setTrainers(data.trainers);
      }
    } catch (error) {
      console.error('Error searching trainers:', error);
    }
    setLoading(false);
  };

  const registerTrainer = async () => {
    try {
      const registrationData = {
        ...trainerForm,
        user_id: `user_${Date.now()}`, // In real app, get from authentication
        certifications: trainerForm.certifications.map(cert => ({
          type: 'personal_trainer',
          name: cert,
          organization: 'Certified Organization',
          issue_date: new Date().toISOString().split('T')[0]
        }))
      };

      const response = await fetch('/api/trainers/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(registrationData)
      });

      const result = await response.json();
      
      if (result.success) {
        alert('Trainer registration submitted successfully! You will receive an email when your application is reviewed.');
        setActiveTab('browse');
        setUserType('trainer');
      } else {
        alert(`Registration failed: ${result.error}`);
      }
    } catch (error) {
      console.error('Error registering trainer:', error);
      alert('Registration error. Please try again.');
    }
  };

  const bookSession = async (trainerId, serviceId) => {
    try {
      const bookingData = {
        client_user_id: `user_${Date.now()}`, // In real app, get from authentication
        trainer_id: trainerId,
        service_id: serviceId,
        session_date: bookingForm.session_date,
        session_notes: bookingForm.session_notes
      };

      const response = await fetch('/api/trainers/book-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bookingData)
      });

      const result = await response.json();
      
      if (result.success) {
        alert(`Session booked successfully! Total: $${result.total_price}. Please complete payment to confirm.`);
        setBookingForm({ trainer_id: '', service_id: '', session_date: '', session_notes: '' });
      } else {
        alert(`Booking failed: ${result.error}`);
      }
    } catch (error) {
      console.error('Error booking session:', error);
      alert('Booking error. Please try again.');
    }
  };

  const addSpecialization = (spec) => {
    if (!trainerForm.specializations.includes(spec)) {
      setTrainerForm({
        ...trainerForm,
        specializations: [...trainerForm.specializations, spec]
      });
    }
  };

  const removeSpecialization = (spec) => {
    setTrainerForm({
      ...trainerForm,
      specializations: trainerForm.specializations.filter(s => s !== spec)
    });
  };

  const renderTrainerCard = (trainer) => (
    <div key={trainer.trainer_id} className="trainer-card">
      <div className="trainer-header">
        <div className="trainer-avatar">
          {trainer.profile_image_url ? (
            <img src={trainer.profile_image_url} alt={trainer.name} />
          ) : (
            <div className="avatar-placeholder">
              {trainer.name.split(' ').map(n => n[0]).join('')}
            </div>
          )}
        </div>
        <div className="trainer-info">
          <h3>{trainer.name}</h3>
          <div className="trainer-rating">
            <span className="stars">{'★'.repeat(Math.floor(trainer.rating))}{'☆'.repeat(5-Math.floor(trainer.rating))}</span>
            <span className="rating-text">{trainer.rating.toFixed(1)} ({trainer.total_reviews} reviews)</span>
          </div>
          <p className="experience">{trainer.experience_years} years experience • {trainer.total_sessions} sessions</p>
          <p className="price-range">{trainer.hourly_rate_range}/hour</p>
        </div>
      </div>
      
      <div className="trainer-details">
        <p className="bio">{trainer.bio}</p>
        
        <div className="specializations">
          {trainer.specializations.slice(0, 3).map((spec, index) => (
            <span key={index} className="spec-tag">{spec}</span>
          ))}
          {trainer.specializations.length > 3 && (
            <span className="spec-more">+{trainer.specializations.length - 3} more</span>
          )}
        </div>
        
        <div className="trainer-features">
          <span className="feature">📱 Online Sessions</span>
          <span className="feature">🏃 In-Person Training</span>
          <span className="feature">🗣️ {trainer.languages.join(', ')}</span>
        </div>
        
        <div className="availability">
          <span className="availability-indicator">🟢 {trainer.availability_preview}</span>
        </div>
      </div>
      
      <div className="trainer-actions">
        <button 
          className="book-btn primary"
          onClick={() => {
            setBookingForm({
              ...bookingForm,
              trainer_id: trainer.trainer_id,
              session_date: new Date(Date.now() + 86400000).toISOString().slice(0, 16) // Tomorrow
            });
            setActiveTab('book');
          }}
        >
          Book Session
        </button>
        <button className="view-btn secondary">View Profile</button>
      </div>
    </div>
  );

  return (
    <div className="trainer-marketplace">
      <div className="header">
        <h1>💪 Khyrie Trainer Marketplace</h1>
        <div className="user-type-toggle">
          <button 
            className={`toggle-btn ${userType === 'client' ? 'active' : ''}`}
            onClick={() => setUserType('client')}
          >
            Find a Trainer
          </button>
          <button 
            className={`toggle-btn ${userType === 'trainer' ? 'active' : ''}`}
            onClick={() => setUserType('trainer')}
          >
            Trainer Dashboard
          </button>
          <button 
            className={`toggle-btn ${userType === 'new_trainer' ? 'active' : ''}`}
            onClick={() => setUserType('new_trainer')}
          >
            Become a Trainer
          </button>
        </div>
      </div>

      <div className="marketplace-content">
        {userType === 'client' && (
          <div className="client-view">
            <div className="search-filters">
              <h3>Find Your Perfect Trainer</h3>
              <div className="filter-row">
                <div className="filter-group">
                  <label>Specialization</label>
                  <select 
                    value={searchFilters.specialization}
                    onChange={(e) => setSearchFilters({...searchFilters, specialization: e.target.value})}
                  >
                    <option value="">All Specializations</option>
                    {specializations.map(spec => (
                      <option key={spec} value={spec.toLowerCase()}>{spec}</option>
                    ))}
                  </select>
                </div>
                
                <div className="filter-group">
                  <label>Service Type</label>
                  <select 
                    value={searchFilters.service_type}
                    onChange={(e) => setSearchFilters({...searchFilters, service_type: e.target.value})}
                  >
                    <option value="">All Services</option>
                    {serviceTypes.map(type => (
                      <option key={type.value} value={type.value}>{type.label}</option>
                    ))}
                  </select>
                </div>
                
                <div className="filter-group">
                  <label>Max Price ($/hour)</label>
                  <input 
                    type="number"
                    value={searchFilters.max_price}
                    onChange={(e) => setSearchFilters({...searchFilters, max_price: e.target.value})}
                    placeholder="Any"
                  />
                </div>
                
                <div className="filter-group">
                  <label>Min Rating</label>
                  <select 
                    value={searchFilters.min_rating}
                    onChange={(e) => setSearchFilters({...searchFilters, min_rating: parseFloat(e.target.value)})}
                  >
                    <option value="0">Any Rating</option>
                    <option value="3">3+ Stars</option>
                    <option value="4">4+ Stars</option>
                    <option value="4.5">4.5+ Stars</option>
                  </select>
                </div>
              </div>
              
              <div className="filter-checkboxes">
                <label>
                  <input 
                    type="checkbox"
                    checked={searchFilters.online_only}
                    onChange={(e) => setSearchFilters({...searchFilters, online_only: e.target.checked})}
                  />
                  Online Sessions Only
                </label>
                <label>
                  <input 
                    type="checkbox"
                    checked={searchFilters.in_person_only}
                    onChange={(e) => setSearchFilters({...searchFilters, in_person_only: e.target.checked})}
                  />
                  In-Person Training Only
                </label>
              </div>
            </div>

            <div className="trainers-grid">
              {loading ? (
                <div className="loading">Finding the best trainers for you...</div>
              ) : trainers.length > 0 ? (
                trainers.map(renderTrainerCard)
              ) : (
                <div className="no-results">
                  <h3>No trainers found</h3>
                  <p>Try adjusting your search filters to find more trainers in your area.</p>
                </div>
              )}
            </div>
          </div>
        )}

        {userType === 'new_trainer' && (
          <div className="trainer-registration">
            <div className="registration-header">
              <h2>Join the Khyrie Trainer Network</h2>
              <p>Share your expertise, build your client base, and earn money on your terms</p>
            </div>

            <div className="benefits-section">
              <div className="benefit">
                <span className="benefit-icon">💰</span>
                <h4>Earn 85% Commission</h4>
                <p>Keep more of what you earn with our industry-leading commission rate</p>
              </div>
              <div className="benefit">
                <span className="benefit-icon">📱</span>
                <h4>Full Platform Support</h4>
                <p>Scheduling, payments, client management - all handled for you</p>
              </div>
              <div className="benefit">
                <span className="benefit-icon">🌐</span>
                <h4>Online & In-Person</h4>
                <p>Offer services both virtually and at your preferred locations</p>
              </div>
              <div className="benefit">
                <span className="benefit-icon">📊</span>
                <h4>Business Analytics</h4>
                <p>Track earnings, client progress, and grow your business</p>
              </div>
            </div>

            <form className="trainer-form">
              <div className="form-section">
                <h3>Personal Information</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label>First Name *</label>
                    <input 
                      type="text"
                      value={trainerForm.first_name}
                      onChange={(e) => setTrainerForm({...trainerForm, first_name: e.target.value})}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Last Name *</label>
                    <input 
                      type="text"
                      value={trainerForm.last_name}
                      onChange={(e) => setTrainerForm({...trainerForm, last_name: e.target.value})}
                      required
                    />
                  </div>
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label>Email *</label>
                    <input 
                      type="email"
                      value={trainerForm.email}
                      onChange={(e) => setTrainerForm({...trainerForm, email: e.target.value})}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Phone</label>
                    <input 
                      type="tel"
                      value={trainerForm.phone}
                      onChange={(e) => setTrainerForm({...trainerForm, phone: e.target.value})}
                    />
                  </div>
                </div>
              </div>

              <div className="form-section">
                <h3>Professional Information</h3>
                <div className="form-group">
                  <label>Bio *</label>
                  <textarea 
                    value={trainerForm.bio}
                    onChange={(e) => setTrainerForm({...trainerForm, bio: e.target.value})}
                    placeholder="Tell potential clients about your experience, training philosophy, and what makes you unique..."
                    rows="4"
                    required
                  />
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label>Years of Experience *</label>
                    <input 
                      type="number"
                      min="0"
                      max="50"
                      value={trainerForm.experience_years}
                      onChange={(e) => setTrainerForm({...trainerForm, experience_years: parseInt(e.target.value)})}
                      required
                    />
                  </div>
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label>Hourly Rate Range ($/hour)</label>
                    <div className="rate-inputs">
                      <input 
                        type="number"
                        min="10"
                        max="500"
                        value={trainerForm.hourly_rate_min}
                        onChange={(e) => setTrainerForm({...trainerForm, hourly_rate_min: parseFloat(e.target.value)})}
                        placeholder="Min"
                      />
                      <span>to</span>
                      <input 
                        type="number"
                        min="10"
                        max="500"
                        value={trainerForm.hourly_rate_max}
                        onChange={(e) => setTrainerForm({...trainerForm, hourly_rate_max: parseFloat(e.target.value)})}
                        placeholder="Max"
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div className="form-section">
                <h3>Specializations</h3>
                <div className="specializations-selector">
                  <div className="available-specs">
                    {specializations.map(spec => (
                      <button 
                        key={spec}
                        type="button"
                        className={`spec-btn ${trainerForm.specializations.includes(spec) ? 'selected' : ''}`}
                        onClick={() => trainerForm.specializations.includes(spec) ? 
                          removeSpecialization(spec) : addSpecialization(spec)
                        }
                      >
                        {spec}
                      </button>
                    ))}
                  </div>
                </div>
                
                {trainerForm.specializations.length > 0 && (
                  <div className="selected-specs">
                    <h4>Selected Specializations:</h4>
                    <div className="selected-list">
                      {trainerForm.specializations.map(spec => (
                        <span key={spec} className="selected-spec">
                          {spec} 
                          <button type="button" onClick={() => removeSpecialization(spec)}>×</button>
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="form-actions">
                <button 
                  type="button"
                  className="register-btn primary"
                  onClick={registerTrainer}
                  disabled={!trainerForm.first_name || !trainerForm.last_name || !trainerForm.email || !trainerForm.bio}
                >
                  Submit Application
                </button>
              </div>
            </form>
          </div>
        )}

        {activeTab === 'book' && bookingForm.trainer_id && (
          <div className="booking-form">
            <h3>Book Training Session</h3>
            <div className="form-group">
              <label>Session Date & Time</label>
              <input 
                type="datetime-local"
                value={bookingForm.session_date}
                onChange={(e) => setBookingForm({...bookingForm, session_date: e.target.value})}
                min={new Date().toISOString().slice(0, 16)}
                required
              />
            </div>
            
            <div className="form-group">
              <label>Session Notes (Optional)</label>
              <textarea 
                value={bookingForm.session_notes}
                onChange={(e) => setBookingForm({...bookingForm, session_notes: e.target.value})}
                placeholder="Any specific goals, preferences, or notes for your trainer..."
                rows="3"
              />
            </div>
            
            <div className="booking-actions">
              <button 
                className="confirm-booking-btn primary"
                onClick={() => bookSession(bookingForm.trainer_id, 'service_default')}
              >
                Confirm Booking
              </button>
              <button 
                className="cancel-booking-btn secondary"
                onClick={() => setActiveTab('browse')}
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TrainerMarketplace;