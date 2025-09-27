<template>
  <header class="header">
    <nav class="navbar">
      <div class="nav-brand">
        <h1 class="brand-title">{{ brandName }}</h1>
      </div>
      <ul class="nav-menu" :class="{ 'nav-menu-active': isMenuOpen }">
        <li class="nav-item">
          <a href="#home" class="nav-link" @click="closeMenu">Home</a>
        </li>
        <li class="nav-item">
          <a href="#workouts" class="nav-link" @click="closeMenu">Workouts</a>
        </li>
        <li class="nav-item">
          <a href="#community" class="nav-link" @click="closeMenu">Community</a>
        </li>
        <li class="nav-item">
          <a href="#profile" class="nav-link" @click="closeMenu">Profile</a>
        </li>
        <li class="nav-item">
          <button class="btn-primary" @click="handleJoinClick">Join Now</button>
        </li>
      </ul>
      <div class="hamburger" @click="toggleMenu">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </div>
    </nav>
  </header>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Header',
  props: {
    brandName: {
      type: String,
      default: 'FitFriendsClub'
    }
  },
  setup(props, { emit }) {
    const isMenuOpen = ref(false)

    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value
    }

    const closeMenu = () => {
      isMenuOpen.value = false
    }

    const handleJoinClick = () => {
      emit('join-clicked')
      closeMenu()
    }

    return {
      isMenuOpen,
      toggleMenu,
      closeMenu,
      handleJoinClick
    }
  }
}
</script>

<style scoped>
.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  position: relative;
}

.nav-brand .brand-title {
  color: white;
  font-size: 1.8rem;
  font-weight: bold;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.nav-menu {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  align-items: center;
  gap: 2rem;
}

.nav-item {
  position: relative;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 0;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  color: #f0f8ff;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: #f0f8ff;
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

.btn-primary {
  background: linear-gradient(135deg, #ff6b6b, #ff5722);
  color: white;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 25px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
}

.hamburger {
  display: none;
  flex-direction: column;
  cursor: pointer;
  padding: 4px;
}

.bar {
  width: 25px;
  height: 3px;
  background-color: white;
  margin: 3px 0;
  transition: 0.3s;
  border-radius: 3px;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .hamburger {
    display: flex;
  }

  .nav-menu {
    position: fixed;
    left: -100%;
    top: 70px;
    flex-direction: column;
    background: rgba(102, 126, 234, 0.95);
    width: 100%;
    text-align: center;
    transition: 0.3s;
    box-shadow: 0 10px 27px rgba(0, 0, 0, 0.05);
    backdrop-filter: blur(10px);
    padding: 2rem 0;
    gap: 1rem;
  }

  .nav-menu-active {
    left: 0;
  }

  .nav-item {
    margin: 1rem 0;
  }

  .hamburger.active .bar:nth-child(2) {
    opacity: 0;
  }

  .hamburger.active .bar:nth-child(1) {
    transform: translateY(8px) rotate(45deg);
  }

  .hamburger.active .bar:nth-child(3) {
    transform: translateY(-8px) rotate(-45deg);
  }
}

/* Animation for smooth appearance */
.header {
  animation: slideDown 0.5s ease-out;
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
  }
  to {
    transform: translateY(0);
  }
}
</style>