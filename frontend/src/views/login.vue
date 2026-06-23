<script setup>
import { computed, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";
import { router } from "../router";
import { useAuth } from "../store/auth";
import axios from "axios";

// useRoute provides access to the current route object
const route = useRoute();
const { login } = useAuth();

// This computed property determines which tab should be active
// based on the URL path. It makes the component reactive to URL changes.
const activeTab = computed(() => {
  // Assuming your routes are named 'login' and 'register'
  if (route.path.includes("/signup")) {
    return "signup";
  }
  return "login";
});

// FORM HANDLING
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

  // Reset any previous errors
  errors.value.login = "";
  isLoading.value = true;

  try {
    await login({
      email: loginForm.value.email,
      password: loginForm.value.password,
      rememberMe: loginForm.value.rememberMe,
    });
    // Redirect happens inside the login action
  } catch (err) {
    errors.value.login = err.message || "An error occurred.";
  } finally {
    isLoading.value = false;
  }
};

const handleSignup = async () => {
  console.log("Signing up with:", signupForm.value);

  const res = await axios.post("/api/auth/register", {
    full_name: signupForm.value.name,
    email: signupForm.value.email,
    mobile: signupForm.value.mobile,
    password: signupForm.value.password,
    confirmPassword: signupForm.value.confirmPassword,
  });

  if (res.status === 201) {
    const data = res.data;

    // Redirect to the login page or show a success message
    router.push("/login");
    errors.value.signup = ""; // Clear any previous signup errors
    console.log("Signup successful:", data);
  } else {
    const error = res.data;
    errors.value.signup = error.message || "Signup failed. Please try again.";
    console.error("Signup failed:", error);
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
          <form @submit.prevent="handleLogin">
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
          <form @submit.prevent="handleSignup">
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
                type="number"
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
                required
              />
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
            <button type="submit" class="btn btn-custom">Sign Up</button>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>
