<script setup>
import { computed, onMounted, ref } from "vue";
import axios from "axios";

const applications = ref([]);
const isLoading = ref(true);
const error = ref("");
const search = ref("");

const filteredApplications = computed(() => {
  const query = search.value.trim().toLowerCase();
  if (!query) return applications.value;
  return applications.value.filter(
    appl =>
      appl.companyName.toLowerCase().includes(query) ||
      appl.jobTitle.toLowerCase().includes(query) ||
      appl.status.toLowerCase().includes(query),
  );
});

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

const statusClass = status =>
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

    <template v-else>
      <input
        type="text"
        class="form-control search-input mb-4"
        placeholder="Search by company, role, or status"
        v-model="search"
      />

      <div v-if="filteredApplications.length === 0" class="text-muted">
        No applications match your search.
      </div>

      <div v-else class="applications-card">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0 applications-table">
            <thead>
              <tr>
                <th>Company</th>
                <th>Role</th>
                <th>Applied On</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="appl in filteredApplications" :key="appl.id">
                <td>{{ appl.companyName }}</td>
                <td>{{ appl.jobTitle }}</td>
                <td>{{ new Date(appl.appliedDate).toLocaleDateString() }}</td>
                <td>
                  <span class="badge" :class="statusClass(appl.status)">{{ appl.status }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </b-container>
</template>

<style scoped>
.search-input {
  background-color: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #f8fafc !important;
  padding: 0.85rem 1rem;
  border-radius: 0.5rem;
  max-width: 420px;
}
.search-input::placeholder {
  color: #64748b;
}
.applications-card {
  background: rgba(30, 41, 59, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  overflow: hidden;
}
.applications-table {
  --bs-table-bg: transparent;
  --bs-table-color: #f8fafc;
  --bs-table-hover-bg: rgba(56, 189, 248, 0.08);
  --bs-table-hover-color: #f8fafc;
  --bs-table-border-color: rgba(255, 255, 255, 0.08);
}
.applications-table thead th {
  background: rgba(15, 23, 42, 0.6);
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.05rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.applications-table tbody td {
  padding: 1rem 1.5rem;
}
.applications-table tbody tr:last-child td {
  border-bottom: none;
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
