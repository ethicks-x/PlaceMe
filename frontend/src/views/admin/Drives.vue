<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const drives = ref([]);
const isLoading = ref(true);
const error = ref("");
const statusFilter = ref("");
const actingId = ref(null);

const fetchDrives = async () => {
  isLoading.value = true;
  try {
    const { data } = await axios.get("/api/admin/drives", {
      params: { status: statusFilter.value || undefined },
    });
    drives.value = data;
  } catch (err) {
    error.value = "Could not load placement drives.";
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchDrives);

const runAction = async (driveId, action) => {
  error.value = "";
  actingId.value = driveId;
  try {
    await axios.post(`/api/admin/drives/${driveId}/${action}`);
    await fetchDrives();
  } catch (err) {
    error.value = err.response?.data?.message || "Action failed.";
  } finally {
    actingId.value = null;
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
    <h1 class="mb-4">Manage Placement Drives</h1>

    <div class="d-flex gap-3 mb-4 flex-wrap">
      <select class="form-select status-select" v-model="statusFilter" @change="fetchDrives">
        <option value="">All Statuses</option>
        <option value="Pending">Pending</option>
        <option value="Approved">Approved</option>
        <option value="Rejected">Rejected</option>
        <option value="Closed">Closed</option>
      </select>
    </div>

    <div v-if="isLoading" class="text-muted">Loading drives...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else-if="drives.length === 0" class="text-muted">No placement drives found.</div>

    <div v-else class="admin-card">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 admin-table">
          <thead>
            <tr>
              <th>Role</th>
              <th>Company</th>
              <th>Deadline</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="drive in drives" :key="drive.id">
              <td>{{ drive.jobTitle }}</td>
              <td>{{ drive.companyName }}</td>
              <td>{{ new Date(drive.deadline).toLocaleDateString() }}</td>
              <td>
                <span class="badge" :class="statusBadgeClass(drive.status)">{{ drive.status }}</span>
              </td>
              <td>
                <div class="d-flex gap-2 flex-wrap">
                  <button
                    v-if="drive.status !== 'Approved'"
                    class="btn btn-sm btn-approve"
                    :disabled="actingId === drive.id"
                    @click="runAction(drive.id, 'approve')"
                  >
                    Approve
                  </button>
                  <button
                    v-if="drive.status !== 'Rejected'"
                    class="btn btn-sm btn-reject"
                    :disabled="actingId === drive.id"
                    @click="runAction(drive.id, 'reject')"
                  >
                    Reject
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
.status-select {
  background-color: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #f8fafc !important;
  max-width: 240px;
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

.btn-approve,
.btn-reject {
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
</style>

