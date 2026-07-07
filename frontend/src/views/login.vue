<script setup>
import { computed, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";
import { router } from "../router";
import { useAuth } from "../store/auth";
import axios from "axios";

const route = useRoute();
const { login, signup } = useAuth();

// trying out some UX
const isPasswordFocused = ref(false);
const passwordCriteria = computed(() => {
    const p = signupForm.value.password || "";
    return {
        length: p.length >= 8,
        uppercase: /[A-Z]/.test(p),
        number: /[0-9]/.test(p),
        special: /[^A-Za-z0-9]/.test(p)
    };
});

// This computed property determines which tab should be active
// based on the URL path. It makes the component reactive to URL changes.
const activeTab = computed(() => {
  if (route.path.includes("/signup")) {
    return "signup";
  }
  return "login";
});

const loginForm = ref({
  email: "",
  password: "",
  rememberMe: false,
});

const signupForm = ref({
  name: "",
  email: "",
  mobile: "",
  password: "",
  confirmPassword: "",
});

const isLoading = ref(false);

const errors = ref({
  login: "",
  signup: "",
});

const handleLogin = async () => {
  console.log("Logging in with:", loginForm.value);

  errors.value.login = "";
  isLoading.value = true;

  try {
    await login({
      email: loginForm.value.email,
      password: loginForm.value.password,
      rememberMe: loginForm.value.rememberMe,
    });
  } catch (err) {
    errors.value.login = err.response?.data?.message || "Could not log in.";
  } finally {
    isLoading.value = false;
  }
};

const handleSignup = async () => {
  console.log("Signing up with:", signupForm.value);
  errors.value.signup = ""
  isLoading.value = true;
  if (signupForm.value.password !== signupForm.value.confirmPassword) {
    errors.value.signup = "Passwords do not match."
    return;
  }

  try {
    await signup({
        full_name: signupForm.value.name,
        email: signupForm.value.email,
        mobile: signupForm.value.mobile,
        password: signupForm.value.password,
        confirmPassword: signupForm.value.confirmPassword,
    });
  } catch (err) {
    errors.value.signup = err.response?.data?.message || "Signup Failed. Please try again.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <main class="d-grid h-100 p-4 overflow-auto" style="place-items: center">
    <div class="form-container">
      <!-- Tab Navigation -->
      <ul class="nav nav-tabs" id="myTab" role="tablist">
        <li class="nav-item" role="presentation">
          <router-link to="/login" class="nav-link" :class="{ active: activeTab === 'login' }"
            >Login</router-link
          >
        </li>
        <li class="nav-item" role="presentation">
          <router-link to="/signup" class="nav-link" :class="{ active: activeTab === 'signup' }"
            >Sign Up</router-link
          >
        </li>
      </ul>

      <!-- Errors -->
      <div
        v-if="errors.login && activeTab === 'login'"
        class="alert alert-danger py-2 d-flex gap-3"
        role="alert"
      >
        <i class="bi bi-exclamation-triangle"></i>
        {{ errors.login }}
      </div>
      <div
        v-if="errors.signup && activeTab === 'signup'"
        class="alert alert-danger py-2 d-flex gap-3"
        role="alert"
      >
        <i class="bi bi-exclamation-triangle"></i>
        {{ errors.signup }}
      </div>

      <!-- Tab Content -->
      <div class="tab-content" id="myTabContent">
        <!-- Login Pane -->
        <div
          v-if="activeTab === 'login'"
          class="tab-pane fade show active"
          id="login-tab-pane"
          key="login-form"
        >
          <h2 class="text-white">Welcome Back!</h2>
          <form @submit.prevent="handleLogin" autocomplete="off">
            <div class="mb-3">
              <input
                type="email"
                class="form-control"
                id="loginEmail"
                placeholder="Email Address"
                v-model="loginForm.email"
                required
              />
            </div>
            <div class="mb-3">
              <input
                type="password"
                class="form-control"
                id="loginPassword"
                placeholder="Password"
                v-model="loginForm.password"
                required
              />
            </div>
            <div class="d-flex justify-content-between align-items-center mb-4">
              <div class="form-check">
                <input
                  type="checkbox"
                  class="form-check-input"
                  id="rememberMe"
                  v-model="loginForm.rememberMe"
                />
                <label class="form-check-label" for="rememberMe">Remember Me</label>
              </div>
              <div class="form-text">
                <a href="#">Forgot Password?</a>
              </div>
            </div>
            <button type="submit" class="btn btn-custom" :disabled="isLoading">Login</button>
          </form>
        </div>

        <!-- Sign Up Pane -->
        <div
          v-else-if="activeTab === 'signup'"
          class="tab-pane fade show active"
          id="signup-tab-pane"
          key="signup-form"
        >
          <h2 class="text-white">Create Account</h2>
          <form @submit.prevent="handleSignup" autocomplete="off">
            <div class="mb-3">
              <input
                type="text"
                class="form-control"
                id="signupName"
                placeholder="Full Name"
                v-model="signupForm.name"
                required
              />
            </div>
            <div class="mb-3">
              <input
                type="email"
                class="form-control"
                id="signupEmail"
                placeholder="Email Address"
                v-model="signupForm.email"
                required
              />
            </div>
            <div class="mb-3">
              <input
                type="text"
                class="form-control"
                id="signupMobile"
                placeholder="Mobile"
                v-model="signupForm.mobile"
                required
              />
            </div>
            <div class="mb-3">
              <input
                type="password"
                class="form-control"
                id="signupPassword"
                placeholder="Create Password"
                v-model="signupForm.password"
                autocomplete="off"
                @focus="isPasswordFocused = true"
                @blur="isPasswordFocused = false"
                required
              />
            </div>
            <div v-if="isPasswordFocused || signupForm.password.length > 0" 
                 class="password-info-box mt-2 p-3"
            >
                <p class="mb-2 text-white fw-bold" style="font-size: 0.9rem;">Password must contain:</p>
                <ul class="list-unstyled mb-0 criteria-list">
                  <li :class="passwordCriteria.length ? 'text-success fw-bold' : 'text-muted'">
                    <i class="bi me-1" :class="passwordCriteria.length ? 'bi-check-circle-fill' : 'bi-circle'"></i>
                    At least 8 characters
                  </li>
                  <li :class="passwordCriteria.uppercase ? 'text-success fw-bold' : 'text-muted'">
                    <i class="bi me-1" :class="passwordCriteria.uppercase ? 'bi-check-circle-fill' : 'bi-circle'"></i>
                    One uppercase letter
                  </li>
                  <li :class="passwordCriteria.number ? 'text-success fw-bold' : 'text-muted'">
                    <i class="bi me-1" :class="passwordCriteria.number ? 'bi-check-circle-fill' : 'bi-circle'"></i>
                    One number
                  </li>
                  <li :class="passwordCriteria.special ? 'text-success fw-bold' : 'text-muted'">
                    <i class="bi me-1" :class="passwordCriteria.special ? 'bi-check-circle-fill' : 'bi-circle'"></i>
                    One special character
                  </li>
                </ul>
              </div>
            <div class="mb-3">
              <input
                type="password"
                class="form-control"
                id="confirmPassword"
                placeholder="Confirm Password"
                v-model="signupForm.confirmPassword"
                required
              />
            </div>
            <button type="submit" class="btn btn-custom" :disabled="isLoading">Sign Up</button>
          </form>
        </div>
      </div>
      <p>
        <router-link to="/company/register" class="switch-link">
            Represent a company?
        </router-link>
      </p>
    </div>
  </main>
</template>

<style scoped>
    /* Form Container */
    .form-container {
      background: rgba(30, 41, 59, 0.65); /* Matches Surface Level slate */
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 1.25rem;
      padding: 2.5rem;
      width: 100%;
      max-width: 450px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); /* Deep shadow to pop off the background */
    }

    /* Sleek Tab Navigation */
    .nav-tabs {
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      margin-bottom: 2rem;
      border-radius: 0;
      display: flex;
      justify-content: space-between;
    }
    .nav-tabs .nav-item {
      width: 50%;
      text-align: center;
    }
    .nav-tabs .nav-link {
      color: #94A3B8;
      border: none;
      background: transparent;
      font-weight: 600;
      font-size: 1.1rem;
      padding: 0.75rem 1.5rem;
      transition: all 0.3s ease;
      border-bottom: 2px solid transparent;
    }
    .nav-tabs .nav-link:hover {
      color: #F8FAFC;
      border-color: transparent;
    }
    .nav-tabs .nav-link.active {
      color: #38BDF8;
      background: transparent;
      border-bottom: 2px solid #38BDF8;
    }

    /* Dark Mode Form Inputs */
    .form-control {
      background-color: rgba(15, 23, 42, 0.6) !important;
      border: 1px solid rgba(255, 255, 255, 0.1) !important;
      color: #F8FAFC !important;
      padding: 0.85rem 1rem;
      border-radius: 0.5rem;
      transition: all 0.2s ease;
    }
    .form-control::placeholder {
      color: #64748B;
    }
    .form-control:focus {
      background-color: rgba(15, 23, 42, 0.95) !important;
      border-color: #38BDF8 !important;
      box-shadow: 0 0 0 0.25rem rgba(56, 189, 248, 0.25) !important; /* Blue glow on focus */
    }

    /* High-Conversion Primary Button */
    .btn-custom {
      background-color: #38BDF8;
      color: #020617; /* Very dark blue/black text for contrast */
      font-weight: 700;
      font-size: 1.1rem;
      padding: 0.85rem;
      width: 100%;
      border-radius: 0.5rem;
      border: none;
      transition: all 0.3s ease;
      margin-top: 1rem;
    }
    .btn-custom:hover:not(:disabled) {
      background-color: #34D399; /* Smoothly transitions to Success Mint Green! */
      transform: translateY(-2px);
      box-shadow: 0 10px 15px -3px rgba(52, 211, 153, 0.3);
    }
    .btn-custom:disabled {
      background-color: #64748B;
      color: #94A3B8;
      cursor: not-allowed;
    }

    /* Checkbox & Links */
    .form-check-label {
      color: #94A3B8;
      cursor: pointer;
    }
    .form-check-input {
      background-color: rgba(15, 23, 42, 0.6);
      border-color: rgba(255, 255, 255, 0.2);
      cursor: pointer;
    }
    .form-check-input:checked {
      background-color: #38BDF8;
      border-color: #38BDF8;
    }
    .form-text a {
      color: #38BDF8;
      text-decoration: none;
      font-weight: 500;
      transition: color 0.2s ease;
    }
    .form-text a:hover {
      color: #34D399;
    }

    .switch-link {
        color: #38BDF8;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    .switch-link:hover {
        color: #34D399;
    }

    /* Criteria List */
    .password-info-box {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 0.5rem;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
      
      animation: slideDownFade 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      transform-origin: top; 
    }

    @keyframes slideDownFade {
      0% { 
        opacity: 0; 
        transform: translateY(-10px) scaleY(0.95); 
      }
      100% { 
        opacity: 1; 
        transform: translateY(0) scaleY(1); 
      }
    }

    /* The Success Nudge (For the text lines) */
    .criteria-list li {
      font-size: 0.85rem;
      margin-bottom: 0.4rem;
      display: flex;
      align-items: center;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      transform: translateX(0);
    }

    .criteria-list .text-success {
      color: #34D399 !important;
      transform: translateX(6px); /* Nudges the text to the right when completed */
    }

    .criteria-list .text-muted {
      color: #64748B !important;
    }

    /* The Checkmark Pop (For the icons) */
    .criteria-list li i {
      font-size: 1.1rem;
      transition: all 0.2s ease;
      display: inline-block; 
    }

    .criteria-list .text-success i {
      animation: checkPop 0.45s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }

    @keyframes checkPop {
      0% { 
        transform: scale(1); 
      }
      40% { 
        transform: scale(1.5) rotate(-10deg); 
        color: #F8FAFC; /* Flashes bright white at the peak of the pop */
      }
      100% { 
        transform: scale(1) rotate(0deg); 
      }
    }

    /* Typography */
    h2 {
      font-weight: 800;
      margin-bottom: 1.5rem;
      letter-spacing: -0.5px;
      text-align: center;
    }
</style>
