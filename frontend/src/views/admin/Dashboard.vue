<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const stats = ref(null);
const isLoading = ref(true);
const error = ref("");

onMounted(async () => {
  try {
    const { data } = await axios.get("/api/admin/stats");
    stats.value = data;
  } catch (err) {
    error.value = "Could not load statistics.";
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <b-container class="py-5">
    <h1 class="mb-4">Admin Overview</h1>

    <div v-if="isLoading" class="text-muted">Loading statistics...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <b-row class="mb-4">
        <b-col md="3" class="mb-4">
          <div class="stat-card">
            <div class="stat-value">{{ stats.totalStudents }}</div>
            <div class="stat-label">Total Students</div>
          </div>
        </b-col>
        <b-col md="3" class="mb-4">
          <div class="stat-card">
            <div class="stat-value">{{ stats.totalCompanies }}</div>
            <div class="stat-label">Total Companies</div>
          </div>
        </b-col>
        <b-col md="3" class="mb-4">
          <div class="stat-card">
            <div class="stat-value">{{ stats.totalApplications }}</div>
            <div class="stat-label">Total Applications</div>
          </div>
        </b-col>
        <b-col md="3" class="mb-4">
          <div class="stat-card">
            <div class="stat-value">{{ stats.placementRate }}%</div>
            <div class="stat-label">Placement Rate</div>
          </div>
        </b-col>
      </b-row>

      <b-row>
        <b-col md="4" class="mb-4">
          <div class="breakdown-card">
            <h3 class="mb-3">Companies</h3>
            <div
              class="breakdown-row"
              v-for="(count, status) in stats.companiesByStatus"
              :key="status"
            >
              <span class="text-capitalize">{{ status }}</span>
              <span class="fw-bold">{{ count }}</span>
            </div>
            <router-link to="/admin/companies" class="switch-link d-block mt-3"
              >Manage Companies &rarr;</router-link
            >
          </div>
        </b-col>
        <b-col md="4" class="mb-4">
          <div class="breakdown-card">
            <h3 class="mb-3">Drives</h3>
            <div
              class="breakdown-row"
              v-for="(count, status) in stats.drivesByStatus"
              :key="status"
            >
              <span>{{ status }}</span>
              <span class="fw-bold">{{ count }}</span>
            </div>
            <router-link to="/admin/drives" class="switch-link d-block mt-3"
              >Manage Drives &rarr;</router-link
            >
          </div>
        </b-col>
        <b-col md="4" class="mb-4">
          <div class="breakdown-card">
            <h3 class="mb-3">Applications</h3>
            <div
              class="breakdown-row"
              v-for="(count, status) in stats.applicationsByStatus"
              :key="status"
            >
              <span class="text-capitalize">{{ status }}</span>
              <span class="fw-bold">{{ count }}</span>
            </div>
            <router-link to="/admin/students" class="switch-link d-block mt-3"
              >Manage Students &rarr;</router-link
            >
          </div>
        </b-col>
      </b-row>
    </div>
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

.breakdown-card {
  background: rgba(30, 41, 59, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem;
  height: 100%;
}
.breakdown-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.breakdown-row:last-of-type {
  border-bottom: none;
}
.switch-link {
  color: #38bdf8;
  text-decoration: none;
  font-weight: 500;
}
.switch-link:hover {
  color: #34d399;
}
</style>

