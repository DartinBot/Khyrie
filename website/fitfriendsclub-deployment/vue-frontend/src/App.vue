<template>
  <div id="app">
    <!-- This fixes the original error: Can't resolve '@/components/Header.vue' -->
    <Header 
      :brand-name="appName"
      @join-clicked="handleJoinClick"
    />
    
    <main class="main-content">
      <section class="hero">
        <div class="hero-content">
          <h1 class="hero-title">{{ heroTitle }}</h1>
          <p class="hero-subtitle">{{ heroSubtitle }}</p>
          <div class="hero-buttons">
            <button class="btn-primary large" @click="handleGetStarted">
              Get Started
            </button>
            <button class="btn-secondary large" @click="handleLearnMore">
              Learn More
            </button>
          </div>
        </div>
        <div class="hero-image">
          <div class="fitness-icon">💪</div>
        </div>
      </section>

      <section class="features" id="workouts">
        <div class="container">
          <h2 class="section-title">Features</h2>
          <div class="features-grid">
            <div class="feature-card" v-for="feature in features" :key="feature.id">
              <div class="feature-icon">{{ feature.icon }}</div>
              <h3 class="feature-title">{{ feature.title }}</h3>
              <p class="feature-description">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <section class="cta-section" id="community">
        <div class="container">
          <h2 class="cta-title">Ready to Start Your Fitness Journey?</h2>
          <p class="cta-description">Join thousands of fitness enthusiasts today</p>
          <button class="btn-primary large" @click="handleJoinClick">
            Join FitFriendsClub Now
          </button>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="container">
        <p>&copy; 2025 {{ appName }}. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import Header from '@/components/Header.vue'

export default {
  name: 'App',
  components: {
    Header  // This resolves the import error
  },
  setup() {
    const appName = ref('FitFriendsClub')
    const heroTitle = ref('Find Your Fitness Community')
    const heroSubtitle = ref('Connect with workout partners, join group activities, and achieve your fitness goals together.')
    
    const features = reactive([
      {
        id: 1,
        icon: '🏋️',
        title: 'Personal Workouts',
        description: 'Track your individual fitness progress and set personal goals.'
      },
      {
        id: 2,
        icon: '👥',
        title: 'Group Workouts',
        description: 'Join or create group workout sessions with like-minded people.'
      },
      {
        id: 3,
        icon: '📊',
        title: 'Progress Tracking',
        description: 'Monitor your fitness journey with detailed analytics and insights.'
      },
      {
        id: 4,
        icon: '🤝',
        title: 'Find Partners',
        description: 'Connect with workout buddies who share your fitness interests.'
      }
    ])

    const handleJoinClick = () => {
      console.log('Join button clicked!')
      // Add your join logic here
    }

    const handleGetStarted = () => {
      console.log('Get started clicked!')
      // Add navigation logic here
    }

    const handleLearnMore = () => {
      console.log('Learn more clicked!')
      // Add learn more logic here
    }

    return {
      appName,
      heroTitle,
      heroSubtitle,
      features,
      handleJoinClick,
      handleGetStarted,
      handleLearnMore
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  margin-top: 70px; /* Account for fixed header */
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  display: flex;
  align-items: center;
  min-height: 500px;
}

.hero-content {
  flex: 1;
  max-width: 600px;
}

.hero-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.fitness-icon {
  font-size: 8rem;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

/* Buttons */
.btn-primary, .btn-secondary {
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 25px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: linear-gradient(135deg, #ff6b6b, #ff5722);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-primary:hover, .btn-secondary:hover {
  transform: translateY(-2px);
}

.btn-primary:hover {
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
}

.large {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
}

/* Features Section */
.features {
  padding: 4rem 2rem;
  background: #f8f9fa;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: #333;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.feature-description {
  color: #666;
  line-height: 1.6;
}

/* CTA Section */
.cta-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  text-align: center;
}

.cta-title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.cta-description {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

/* Footer */
.footer {
  background: #333;
  color: white;
  padding: 2rem;
  text-align: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero {
    flex-direction: column;
    text-align: center;
    padding: 2rem 1rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-buttons {
    justify-content: center;
  }

  .fitness-icon {
    font-size: 4rem;
    margin-top: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .section-title, .cta-title {
    font-size: 2rem;
  }
}
</style>