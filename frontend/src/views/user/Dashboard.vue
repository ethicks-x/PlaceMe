<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import { useAuth } from "../../store/auth";

const { authState } = useAuth();

const dashboard = ref(null);
const isLoading = ref(true);
const error = ref("");

onMounted(async () => {
  try {
    const { data } = await axios.get("/api/dashboard");
    dashboard.value = data;
  } catch (err) {
    error.value = "Could not load your dashboard right now.";
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <b-container class="dashboard-wrapper py-5">
    <h1 class="mb-4">Welcome back, {{ authState.user?.fullName || "Student" }}</h1>

    <div v-if="isLoading" class="text-muted">Loading dashboard...</div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <b-row v-else-if="dashboard">
      <b-col md="3" class="mb-4">
        <div class="stat-card">
          <div class="stat-value">{{ dashboard.applications.total }}</div>
          <div class="stat-label">Total Applications</div>
        </div>
      </b-col>
      <b-col md="3" class="mb-4">
        <div class="stat-card">
          <div class="stat-value">{{ dashboard.applications.statusCounts.shortlisted }}</div>
          <div class="stat-label">Shortlisted</div>
        </div>
      </b-col>
      <b-col md="3" class="mb-4">
        <div class="stat-card">
          <div class="stat-value">{{ dashboard.applications.statusCounts.selected }}</div>
          <div class="stat-label">Selected</div>
        </div>
      </b-col>
      <b-col md="3" class="mb-4">
        <div class="stat-card">
          <div class="stat-value">{{ dashboard.openDrives }}</div>
          <div class="stat-label">Open Drives</div>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<style scoped>
.stat-card {
  background: rgba(30, 41, 59, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem;
  text-align: center;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #38bdf8;
}

.stat-label {
  color: #94a3b8;
  margin-top: 0.5rem;
}
</style>

