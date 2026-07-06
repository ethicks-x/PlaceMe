<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const companies = ref([]);
const isLoading = ref(true);
const error = ref("");
const search = ref("");
const statusFilter = ref("");
const actingId = ref(null);

const fetchCompanies = async () => {
  isLoading.value = true;
  try {
    const { data } = await axios.get("/api/admin/companies", {
      params: { search: search.value || undefined, status: statusFilter.value || undefined },
    });
    companies.value = data;
  } catch (err) {
    error.value = "Could not load companies.";
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchCompanies);

const runAction = async (companyId, action) => {
  error.value = "";
  actingId.value = companyId;
  try {
    await axios.post(`/api/admin/companies/${companyId}/${action}`);
    await fetchCompanies();
  } catch (err) {
    error.value = err.response?.data?.message || "Action failed.";
  } finally {
    actingId.value = null;
  }
};

const statusBadgeClass = (status) =>
  ({
    pending: "badge-pending",
    approved: "badge-approved",
    rejected: "badge-rejected",
  })[status] || "badge-pending";
</script>

<template>
  <b-container class="py-5">
    <h1 class="mb-4">Manage Companies</h1>

    <div class="d-flex gap-3 mb-4 flex-wrap">
      <input
        type="text"
        class="form-control search-input"
        placeholder="Search by company name"
        v-model="search"
        @keyup.enter="fetchCompanies"
      />
      <select class="form-select status-select" v-model="statusFilter" @change="fetchCompanies">
        <option value="">All Statuses</option>
        <option value="pending">Pending</option>
        <option value="approved">Approved</option>
        <option value="rejected">Rejected</option>
      </select>
      <button class="btn btn-custom" @click="fetchCompanies">Search</button>
    </div>

    <div v-if="isLoading" class="text-muted">Loading companies...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else-if="companies.length === 0" class="text-muted">No companies found.</div>

    <div v-else class="admin-card">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 admin-table">
          <thead>
            <tr>
              <th>Company</th>
              <th>Contact</th>
              <th>Status</th>
              <th>Account</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="company in companies" :key="company.id">
              <td>
                <div class="fw-bold">{{ company.companyName }}</div>
                <a :href="company.website" target="_blank" rel="noopener" class="switch-link small">{{
                  company.website
                }}</a>
              </td>
              <td>
                <div>{{ company.email }}</div>
                <div class="text-muted small">{{ company.hrContact }}</div>
              </td>
              <td>
                <span class="badge" :class="statusBadgeClass(company.approvalStatus)">{{
                  company.approvalStatus
                }}</span>
              </td>
              <td>
                <span class="badge" :class="company.isActive ? 'badge-approved' : 'badge-rejected'">
                  {{ company.isActive ? "Active" : "Deactivated" }}
                </span>
              </td>
              <td>
                <div class="d-flex gap-2 flex-wrap">
                  <button
                    v-if="company.approvalStatus !== 'approved'"
                    class="btn btn-sm btn-approve"
                    :disabled="actingId === company.id"
                    @click="runAction(company.id, 'approve')"
                  >
                    Approve
                  </button>
                  <button
                    v-if="company.approvalStatus !== 'rejected'"
                    class="btn btn-sm btn-reject"
                    :disabled="actingId === company.id"
                    @click="runAction(company.id, 'reject')"
                  >
                    Reject
                  </button>
                  <button
                    class="btn btn-sm btn-toggle"
                    :disabled="actingId === company.id"
                    @click="runAction(company.id, company.isActive ? 'deactivate' : 'activate')"
                  >
                    {{ company.isActive ? "Deactivate" : "Activate" }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </b-container>
</template>

<style scoped>
.search-input,
.status-select {
  background-color: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #f8fafc !important;
  max-width: 320px;
}
.search-input::placeholder {
  color: #64748b;
}

.btn-custom {
  background-color: #38bdf8;
  color: #020617;
  font-weight: 700;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 0.5rem;
}
.btn-custom:hover {
  background-color: #34d399;
}

.admin-card {
  background: rgba(30, 41, 59, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  overflow: hidden;
}

.admin-table {
  --bs-table-bg: transparent;
  --bs-table-color: #f8fafc;
  --bs-table-hover-bg: rgba(56, 189, 248, 0.08);
  --bs-table-hover-color: #f8fafc;
  --bs-table-border-color: rgba(255, 255, 255, 0.08);
}
.admin-table thead th {
  background: rgba(15, 23, 42, 0.6);
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.admin-table tbody td {
  padding: 1rem 1.5rem;
}
.admin-table tbody tr:last-child td {
  border-bottom: none;
}

.switch-link {
  color: #38bdf8;
  text-decoration: none;
}
.switch-link:hover {
  color: #34d399;
}

.badge {
  text-transform: capitalize;
  font-weight: 600;
  padding: 0.4rem 0.75rem;
}
.badge-pending {
  background-color: rgba(250, 204, 21, 0.2);
  color: #facc15;
}
.badge-approved {
  background-color: rgba(52, 211, 153, 0.2);
  color: #34d399;
}
.badge-rejected {
  background-color: rgba(248, 113, 113, 0.2);
  color: #f87171;
}

.btn-approve,
.btn-reject,
.btn-toggle {
  font-weight: 600;
  border: none;
  white-space: nowrap;
}
.btn-approve {
  background-color: rgba(52, 211, 153, 0.2);
  color: #34d399;
}
.btn-approve:hover:not(:disabled) {
  background-color: rgba(52, 211, 153, 0.35);
}
.btn-reject {
  background-color: rgba(248, 113, 113, 0.2);
  color: #f87171;
}
.btn-reject:hover:not(:disabled) {
  background-color: rgba(248, 113, 113, 0.35);
}
.btn-toggle {
  background-color: rgba(148, 163, 184, 0.2);
  color: #94a3b8;
}
.btn-toggle:hover:not(:disabled) {
  background-color: rgba(148, 163, 184, 0.35);
}
</style>

