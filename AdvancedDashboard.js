import React, { useState, useEffect } from 'react';
import './AdvancedDashboard.css';

const AdvancedDashboard = () => {
  const [userStats, setUserStats] = useState(null);
  const [workoutTrends, setWorkoutTrends] = useState(null);
  const [aiRecommendations, setAiRecommendations] = useState(null);
  const [injuryRisk, setInjuryRisk] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const userId = 'user_001'; // In real app, get from auth context

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load user analytics
      const analyticsResponse = await fetch(`/api/advanced/analytics/user/${userId}?days=30`);
      if (analyticsResponse.ok) {
        const analytics = await analyticsResponse.json();
        setUserStats(analytics);
      }

      // Load workout trends
      const trendsResponse = await fetch(`/api/advanced/analytics/trends/${userId}?days=90`);
      if (trendsResponse.ok) {
        const trends = await trendsResponse.json();
        setWorkoutTrends(trends);
      }

      // Load AI recommendations
      const aiResponse = await fetch(`/api/advanced/ai/recommendations/${userId}`);
      if (aiResponse.ok) {
        const ai = await aiResponse.json();
        setAiRecommendations(ai);
      }

      // Load injury risk assessment
      const riskResponse = await fetch(`/api/advanced/injury/risk/${userId}`);
      if (riskResponse.ok) {
        const risk = await riskResponse.json();
        setInjuryRisk(risk);
      }

    } catch (err) {
      console.error('Error loading dashboard data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, subtitle, trend, color = 'blue' }) => (
    <div className={`stat-card stat-card-${color}`}>
      <div className="stat-header">
        <h3>{title}</h3>
        {trend && (
          <span className={`trend trend-${trend > 0 ? 'up' : 'down'}`}>
            {trend > 0 ? '↗' : '↘'} {Math.abs(trend)}%
          </span>
        )}
      </div>
      <div className="stat-value">{value}</div>
      {subtitle && <div className="stat-subtitle">{subtitle}</div>}
    </div>
  );

  const RecommendationCard = ({ recommendation }) => (
    <div className={`recommendation-card priority-${recommendation.priority || 'medium'}`}>
      <div className="recommendation-header">
        <span className="recommendation-type">{recommendation.type}</span>
        <span className="confidence">
          {Math.round((recommendation.confidence || 0.8) * 100)}% confidence
        </span>
      </div>
      <h4>{recommendation.title}</h4>
      <p>{recommendation.description}</p>
      <button className="action-btn">Take Action</button>
    </div>
  );

  const TrendChart = ({ data, title }) => {
    if (!data) return null;
    
    const direction = data.direction;
    const iconMap = {
      'increasing': '📈',
      'decreasing': '📉',
      'stable': '➡️'
    };

    return (
      <div className="trend-chart">
        <h4>{title}</h4>
        <div className="trend-display">
          <span className="trend-icon">{iconMap[direction]}</span>
          <span className="trend-text">{direction.toUpperCase()}</span>
          <span className="trend-slope">Slope: {data.slope?.toFixed(2) || 'N/A'}</span>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading your fitness analytics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <h3>⚠️ Error Loading Dashboard</h3>
        <p>{error}</p>
        <button onClick={loadDashboardData} className="retry-btn">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="advanced-dashboard">
      <header className="dashboard-header">
        <h1>🎯 Khyrie Fitness Dashboard</h1>
        <p>AI-Powered Fitness Analytics & Insights</p>
        <button onClick={loadDashboardData} className="refresh-btn">
          🔄 Refresh Data
        </button>
      </header>

      {/* Quick Stats Grid */}
      <section className="stats-grid">
        <StatCard
          title="Total Workouts"
          value={userStats?.workout_stats?.total_workouts || 0}
          subtitle="Last 30 days"
          color="blue"
        />
        <StatCard
          title="Average Volume"
          value={`${userStats?.workout_stats?.avg_volume_kg?.toFixed(1) || 0} kg`}
          subtitle="Per workout"
          color="green"
        />
        <StatCard
          title="Consistency"
          value={`${workoutTrends?.consistency?.workout_frequency?.toFixed(1) || 0}`}
          subtitle="Workouts/week"
          trend={5}
          color="purple"
        />
        <StatCard
          title="Injury Risk"
          value={injuryRisk?.risk_level || 'Unknown'}
          subtitle={`Score: ${injuryRisk?.risk_score || 0}/100`}
          color={injuryRisk?.risk_level === 'Low' ? 'green' : 
                 injuryRisk?.risk_level === 'Moderate' ? 'yellow' : 'red'}
        />
      </section>

      {/* Trends Section */}
      <section className="trends-section">
        <h2>📊 Workout Trends</h2>
        <div className="trends-grid">
          <TrendChart 
            data={workoutTrends?.volume_trend} 
            title="Training Volume"
          />
          <TrendChart 
            data={workoutTrends?.rpe_trend} 
            title="Perceived Exertion (RPE)"
          />
        </div>
      </section>

      {/* AI Recommendations */}
      <section className="recommendations-section">
        <h2>🤖 AI Recommendations</h2>
        <div className="recommendations-grid">
          {aiRecommendations?.recommendations?.map((rec, index) => (
            <RecommendationCard key={index} recommendation={rec} />
          )) || (
            <p>No recommendations available</p>
          )}
        </div>
      </section>

      {/* Injury Risk Assessment */}
      <section className="risk-assessment">
        <h2>⚠️ Injury Risk Assessment</h2>
        <div className="risk-card">
          <div className={`risk-level risk-${injuryRisk?.risk_level?.toLowerCase()}`}>
            <h3>Risk Level: {injuryRisk?.risk_level || 'Unknown'}</h3>
            <div className="risk-score">
              Score: {injuryRisk?.risk_score || 0}/100
            </div>
          </div>
          
          {injuryRisk?.risk_factors?.length > 0 && (
            <div className="risk-factors">
              <h4>Risk Factors:</h4>
              <ul>
                {injuryRisk.risk_factors.map((factor, index) => (
                  <li key={index}>{factor}</li>
                ))}
              </ul>
            </div>
          )}
          
          {injuryRisk?.recommendations?.length > 0 && (
            <div className="prevention-recommendations">
              <h4>Prevention Recommendations:</h4>
              <ul>
                {injuryRisk.recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </section>

      {/* Recent Workouts */}
      <section className="recent-workouts">
        <h2>💪 Recent Activity</h2>
        <div className="activity-timeline">
          {userStats?.recent_sessions?.map((session, index) => (
            <div key={index} className="activity-item">
              <div className="activity-date">
                {new Date(session.date).toLocaleDateString()}
              </div>
              <div className="activity-details">
                <h4>{session.type || 'Workout Session'}</h4>
                <p>Volume: {session.total_volume_kg}kg | Duration: {session.duration}min</p>
                <p>RPE: {session.rpe_score}/10</p>
              </div>
            </div>
          )) || (
            <p>No recent workouts found</p>
          )}
        </div>
      </section>

      {/* Action Buttons */}
      <section className="action-center">
        <h2>🎯 Quick Actions</h2>
        <div className="action-buttons">
          <button className="action-btn primary">
            🏋️ Start New Workout
          </button>
          <button className="action-btn secondary">
            📈 View Detailed Analytics
          </button>
          <button className="action-btn secondary">
            🎯 Generate New Program
          </button>
          <button className="action-btn secondary">
            👥 Social Features
          </button>
        </div>
      </section>
    </div>
  );
};

export default AdvancedDashboard;