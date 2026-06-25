<script setup></script>

<template>
  <div class="landing-page-wrapper">
    <!-- Hero Section -->
    <b-container class="hero-section text-center">
      <b-row align-v="center">
        <b-col md="6" class="text-md-start">
          <h1 class="hero-title">Companies are just <span class="highlight">One-Click Away.</span></h1>
          <p class="hero-subtitle">
            Find your favorite jobs at your ease. No hussle, place where skills speak more.
          </p>
          <b-button size="lg" to="/login" class="btn-custom mt-3">Get Started</b-button>
        </b-col>
        <b-col md="6" class="mt-5 mt-md-0">
          <div class="hero-illustration">
            <AppLogoFull />
          </div>
        </b-col>
      </b-row>
    </b-container>

    <!-- Features Section -->
    <b-container class="features-section text-center">
      <h2 class="section-title">Features</h2>
      <p class="section-subtitle">Skills should be prioritized before anything else.</p>
      <b-row class="mt-5">
        <b-col md="4" class="mb-4">
          <div class="feature-card">
            <div class="feature-icon">
              <i class="bi bi-broadcast"></i>
            </div>
            <h3>Real-time Availability</h3>
            <p>
              Real-time management of the job postings with admin invigilation makes it convenient to get the job you need.
            </p>
          </div>
        </b-col>
        <b-col md="4" class="mb-4">
          <div class="feature-card">
            <div class="feature-icon">
              <i class="bi bi-calendar-check"></i>
            </div>
            <h3>Simple Connect</h3>
            <p>
              Simplified connection between the company and the student, makes it perfect for a workflow.
            </p>
          </div>
        </b-col>
        <b-col md="4" class="mb-4">
          <div class="feature-card">
            <div class="feature-icon">
              <i class="bi bi-shield-check"></i>
            </div>
            <h3>Secure & Simple</h3>
            <p>
              A unified and secure platform for both admins and users with role-based access
              control.
            </p>
          </div>
        </b-col>
      </b-row>
    </b-container>

    <!-- CTA Section -->
    <b-container class="cta-section text-center">
      <h2 class="section-title">Ready to top the charts?</h2>
      <p class="section-subtitle">Create an account today and publish your skills to the world.</p>
      <b-button size="lg" to="/signup" class="btn-custom mt-3">
        Sign Up for Free
        <i class="bi bi-arrow-right-short"></i>
      </b-button>
    </b-container>

    <!-- Footer -->
    <footer class="text-center py-4">
      <b-container>
        <p class="mb-0">&copy; 2026 Placement Workflow. Made by Sinchan.</p>
      </b-container>
    </footer>
  </div>
</template>

<style scoped>
@import url('bootstrap-icons/font/bootstrap-icons.css');

.landing-page-wrapper {
  font-family: 'Poppins', sans-serif;
  background: transparent;
  color: var(--text-color);
  overflow-x: hidden;
}

.hero-section,
.features-section,
.cta-section {
  padding: 80px 0;
  animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-title {
  font-size: clamp(2.5rem, 8vw, 5rem);
  font-weight: 700;
  line-height: 1.2;
  color: #fff;
}

.hero-title .highlight {
  color: var(--highlight-color);
}

.hero-subtitle {
  font-size: 1.6rem;
  color: var(--text-muted);
  margin-top: 1.5rem;
  max-width: 500px;
}

.hero-illustration svg {
  width: 100%;
  max-width: 850px;
  height: auto;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0px);
  }
}

.section-title {
  font-weight: 600;
  font-size: 3.5rem;
  margin-bottom: 1rem;
  color: #fff;
}

.section-subtitle {
  color: var(--text-muted);
  font-size: 1.5rem;
  max-width: 600px;
  margin: 0 auto 2rem auto;
}

.feature-card {
  background: var(--card-bg);
  padding: 40px 22px;
  border-radius: 15px;
  height: 100%;
  border: 1px solid rgba(40, 167, 69, 0.2);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  filter: brightness(2.5);
}

.feature-icon {
  font-size: 4rem;
  color: var(--highlight-color);
  margin-bottom: 1.5rem;
}

.feature-card h3 {
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #fff;
}

.feature-card p {
  font-size: 1.2rem;
  color: var(--text-muted);
}

.btn-custom {
  background: linear-gradient(135deg, var(--button-bg-start), var(--button-bg-end));
  padding: 12px 30px;
  border-radius: 50px;
  border: none;
  font-weight: 600;
  color: white;
  text-decoration: none;
  transition: all 0.4s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.btn-custom:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
  filter: brightness(1.15);
}

footer {
  background-color: rgba(0, 0, 0, 0.2);
  color: var(--text-muted);
  font-size: 0.9rem;
}
</style>
