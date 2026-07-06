<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const applications = ref([]);
const isLoading = ref(true);
const error = ref("");

onMounted(async () => {
  try {
    const { data } = await axios.get("/api/applications");
    applications.value = data;
  } catch (err) {
    error.value = "Could not load your applications.";
  } finally {
    isLoading.value = false;
  }
});

const statusClass = (status) =>
  ({
    applied: "badge-applied",
    shortlisted: "badge-shortlisted",
    selected: "badge-selected",
    rejected: "badge-rejected",
  })[status] || "badge-applied";
</script>

<template>
  <b-container class="applications-wrapper py-5">
    <h1 class="mb-4">My Applications</h1>

    <div v-if="isLoading" class="text-muted">Loading applications...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else-if="applications.length === 0" class="text-muted">
      You haven't applied to any drives yet.
    </div>

    <table v-else class="table applications-table">
      <thead>
        <tr>
          <th>Company</th>
          <th>Role</th>
          <th>Applied On</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="appl in applications" :key="appl.id">
          <td>{{ appl.companyName }}</td>
          <td>{{ appl.jobTitle }}</td>
          <td>{{ new Date(appl.appliedDate).toLocaleDateString() }}</td>
          <td><span class="badge" :class="statusClass(appl.status)">{{ appl.status }}</span></td>
        </tr>
      </tbody>
    </table>
  </b-container>
</template>

<style scoped>
.applications-table {
  color: #f8fafc;
}
.applications-table :deep(th) {
  color: #94a3b8;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.applications-table :deep(td) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  vertical-align: middle;
}

.badge {
  text-transform: capitalize;
  font-weight: 600;
  padding: 0.4rem 0.75rem;
}
.badge-applied {
  background-color: rgba(56, 189, 248, 0.2);
  color: #38bdf8;
}
.badge-shortlisted {
  background-color: rgba(250, 204, 21, 0.2);
  color: #facc15;
}
.badge-selected {
  background-color: rgba(52, 211, 153, 0.2);
  color: #34d399;
}
.badge-rejected {
  background-color: rgba(248, 113, 113, 0.2);
  color: #f87171;
}
</style>

