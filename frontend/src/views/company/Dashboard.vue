<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const drives = ref([]);
const isLoading = ref(true);
const error = ref("");

const form = ref({ jobTitle: "", jobDesc: "", eligibility: "", deadline: "" });
const isSubmitting = ref(false);
const formError = ref("");
const formSuccess = ref("");

const fetchDrives = async () => {
  try {
    const { data } = await axios.get("/api/company/drives");
    drives.value = data;
  } catch (err) {
    error.value = "Could not load your drives.";
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchDrives);

const handleCreate = async () => {
  formError.value = "";
  formSuccess.value = "";
  isSubmitting.value = true;

  try {
    await axios.post("/api/company/drives", {
      jobTitle: form.value.jobTitle,
      jobDesc: form.value.jobDesc,
      eligibility: form.value.eligibility,
      deadline: new Date(form.value.deadline).toISOString(),
    });
    formSuccess.value = "Drive submitted for admin approval.";
    form.value = { jobTitle: "", jobDesc: "", eligibility: "", deadline: "" };
    await fetchDrives();
  } catch (err) {
    formError.value = err.response?.data?.message || "Failed to create drive.";
  } finally {
    isSubmitting.value = false;
  }
};

const statusBadgeClass = (status) =>
  ({
    Pending: "badge-pending",
    Approved: "badge-approved",
    Rejected: "badge-rejected",
    Closed: "badge-closed",
  })[status] || "badge-pending";
</script>

<template>
  <b-container class="py-5">
    <h1 class="mb-4">Company Dashboard</h1>

    <div class="form-card mb-5">
      <h3 class="mb-3">Post a New Drive</h3>

      <div v-if="formError" class="alert alert-danger py-2">{{ formError }}</div>
      <div v-if="formSuccess" class="alert alert-success py-2">{{ formSuccess }}</div>

      <form @submit.prevent="handleCreate">
        <div class="mb-3">
          <label class="form-label">Job Title</label>
          <input type="text" class="form-control" v-model="form.jobTitle" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Job Description</label>
          <textarea class="form-control" rows="3" v-model="form.jobDesc" required></textarea>
        </div>
        <div class="mb-3">
          <label class="form-label">Eligibility Criteria</label>
          <input type="text" class="form-control" v-model="form.eligibility" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Application Deadline</label>
          <input type="date" class="form-control" v-model="form.deadline" required />
        </div>
        <button type="submit" class="btn btn-custom" :disabled="isSubmitting">
          Submit for Approval
        </button>
      </form>
    </div>

    <h3 class="mb-3">Your Drives</h3>
    <div v-if="isLoading" class="text-muted">Loading drives...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else-if="drives.length === 0" class="text-muted">
      You haven't posted any drives yet.
    </div>

    <div v-else class="admin-card">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 admin-table">
          <thead>
            <tr>
              <th>Role</th>
              <th>Deadline</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="drive in drives" :key="drive.id">
              <td>{{ drive.jobTitle }}</td>
              <td>{{ new Date(drive.deadline).toLocaleDateString() }}</td>
              <td>
                <span class="badge" :class="statusBadgeClass(drive.status)">{{ drive.status }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </b-container>
</template>

<style scoped>
.form-card,
.admin-card {
  background: rgba(30, 41, 59, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem;
}
.admin-card {
  padding: 0;
  overflow: hidden;
}

.form-control,
textarea.form-control {
  background-color: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #f8fafc !important;
  padding: 0.85rem 1rem;
  border-radius: 0.5rem;
}
.form-label {
  color: #94a3b8;
}

.btn-custom {
  background-color: #38bdf8;
  color: #020617;
  font-weight: 700;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  border: none;
}
.btn-custom:hover:not(:disabled) {
  background-color: #34d399;
}
.btn-custom:disabled {
  background-color: #64748b;
  color: #94a3b8;
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

.badge {
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
.badge-closed {
  background-color: rgba(148, 163, 184, 0.2);
  color: #94a3b8;
}
</style>

