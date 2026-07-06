<script setup>
import { ref } from "vue";
import { useAuth } from "../../store/auth";

const { registerCompany } = useAuth();

const form = ref({
  companyName: "",
  website: "",
  hrContact: "",
  hrMobile: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const isLoading = ref(false);
const error = ref("");

const handleSubmit = async () => {
  error.value = "";

  if (form.value.password !== form.value.confirmPassword) {
    error.value = "Passwords do not match.";
    return;
  }

  isLoading.value = true;
  try {
    await registerCompany({
      companyName: form.value.companyName,
      website: form.value.website,
      hrContact: form.value.hrContact,
      hrMobile: form.value.hrMobile,
      email: form.value.email,
      password: form.value.password,
    });
  } catch (err) {
    error.value = err.response?.data?.message || "Registration failed. Please try again.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <main class="d-grid h-100 p-4 overflow-auto" style="place-items: center">
    <div class="form-container">
      <h2 class="text-white mb-4">Register Your Company</h2>

      <div v-if="error" class="alert alert-danger py-2 d-flex gap-3" role="alert">
        <i class="bi bi-exclamation-triangle"></i>
        {{ error }}
      </div>

      <form @submit.prevent="handleSubmit" autocomplete="off">
        <div class="mb-3">
          <input
            type="text"
            class="form-control"
            id="companyName"
            placeholder="Company Name"
            v-model="form.companyName"
            required
          />
        </div>
        <div class="mb-3">
          <input
            type="url"
            class="form-control"
            id="companyWebsite"
            placeholder="Company Website"
            v-model="form.website"
            required
          />
        </div>
        <div class="mb-3">
          <input
            type="text"
            class="form-control"
            id="hrContact"
            placeholder="HR Contact Name"
            v-model="form.hrContact"
            required
          />
        </div>
        <div class="mb-3">
          <input
            type="text"
            class="form-control"
            id="hrMobile"
            placeholder="HR Mobile Number"
            v-model="form.hrMobile"
            required
          />
        </div>
        <div class="mb-3">
          <input
            type="email"
            class="form-control"
            id="companyEmail"
            placeholder="Email Address"
            v-model="form.email"
            required
          />
        </div>
        <div class="mb-3">
          <input
            type="password"
            class="form-control"
            id="companyPassword"
            placeholder="Create Password"
            v-model="form.password"
            autocomplete="off"
            required
          />
        </div>
        <div class="mb-3">
          <input
            type="password"
            class="form-control"
            id="companyConfirmPassword"
            placeholder="Confirm Password"
            v-model="form.confirmPassword"
            required
          />
        </div>

        <button type="submit" class="btn btn-custom" :disabled="isLoading">
          Register Company
        </button>
      </form>

      <p class="text-center mt-3 mb-0">
        <router-link to="/login" class="switch-link">Are you a student? Login here</router-link>
      </p>
    </div>
  </main>
</template>

<style scoped>
.form-container {
  background: rgba(30, 41, 59, 0.65);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1.25rem;
  padding: 2.5rem;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.form-control {
  background-color: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #f8fafc !important;
  padding: 0.85rem 1rem;
  border-radius: 0.5rem;
}
.form-control::placeholder {
  color: #64748b;
}
.form-control:focus {
  background-color: rgba(15, 23, 42, 0.95) !important;
  border-color: #38bdf8 !important;
  box-shadow: 0 0 0 0.25rem rgba(56, 189, 248, 0.25) !important;
}

.btn-custom {
  background-color: #38bdf8;
  color: #020617;
  font-weight: 700;
  font-size: 1.1rem;
  padding: 0.85rem;
  width: 100%;
  border-radius: 0.5rem;
  border: none;
  margin-top: 0.5rem;
}
.btn-custom:hover:not(:disabled) {
  background-color: #34d399;
}
.btn-custom:disabled {
  background-color: #64748b;
  color: #94a3b8;
}

.switch-link {
  color: #38bdf8;
  text-decoration: none;
  font-weight: 500;
}
.switch-link:hover {
  color: #34d399;
}

h2 {
  font-weight: 800;
  text-align: center;
}
</style>

