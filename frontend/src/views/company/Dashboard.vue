<script setup>
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'
import { router } from '../../router'

defineOptions({
  name: 'CompanyDashboard',
})

const company = ref(null)
const drives = ref([])
const isLoading = ref(true)
const error = ref('')
const search = ref('')

const filteredDrives = computed(() => {
  const query = search.value.trim().toLowerCase()
  if (!query) return drives.value
  return drives.value.filter(
    drive =>
      drive.jobTitle.toLowerCase().includes(query) || drive.status.toLowerCase().includes(query),
  )
})

const fetchDrives = async () => {
  try {
    const { data } = await axios.get('/api/company/drives')
    drives.value = data
  } catch (err) {
    error.value = 'Could not load your drives.'
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  try {
    const { data } = await axios.get('/api/company/status')
    if (data.approvalStatus !== 'approved') {
      router.replace('/company/pending')
      return
    }
    company.value = data
    await fetchDrives()
  } catch (err) {
    error.value = 'Could not load your company details.'
  } finally {
    isLoading.value = false
  }
})

const statusBadgeClass = status =>
  ({
    Pending: 'badge-pending',
    Approved: 'badge-approved',
    Rejected: 'badge-rejected',
    Closed: 'badge-closed',
  })[status] || 'badge-pending'
</script>

<template>
  <b-container class="py-5">
    <h1 class="mb-4">Company Dashboard</h1>

    <div v-if="isLoading" class="text-muted">Loading...</div>
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <template v-else-if="company">
      <div class="details-card mb-5">
        <h3 class="mb-3">Company Details</h3>
        <dl class="details-grid mb-0">
          <dt>Company Name</dt>
          <dd>{{ company.companyName }}</dd>
          <dt>Website</dt>
          <dd>
            <a :href="company.website" target="_blank" rel="noopener" class="switch-link">{{
              company.website
            }}</a>
          </dd>
          <dt>HR Contact</dt>
          <dd>{{ company.hrContact }}</dd>
          <dt>Approval Status</dt>
          <dd>
            <span class="badge badge-approved">{{ company.approvalStatus }}</span>
          </dd>
        </dl>
      </div>
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h3 class="mb-0">Your Drives</h3>
        <router-link to="/company/drives/new" class="btn btn-custom">Post a New Drive</router-link>
      </div>

      <div v-if="drives.length === 0" class="text-muted">You haven't posted any drives yet.</div>

      <template v-else>
        <input
          type="text"
          class="form-control search-input mb-3"
          placeholder="Search by role or status"
          v-model="search"
        />

        <div v-if="filteredDrives.length === 0" class="text-muted">
          No drives match your search.
        </div>

        <div v-else class="admin-card">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0 admin-table">
              <thead>
                <tr>
                  <th>Role</th>
                  <th>Deadline</th>
                  <th>Status</th>
                  <th>Applicants</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                <tr v-for="drive in filteredDrives" :key="drive.id">
                  <td>{{ drive.jobTitle }}</td>
                  <td>{{ new Date(drive.deadline).toLocaleDateString() }}</td>
                  <td>
                    <span class="badge" :class="statusBadgeClass(drive.status)">{{
                      drive.status
                    }}</span>
                  </td>
                  <td>{{ drive.applicantCount }}</td>
                  <td>
                    <router-link :to="`/company/drives/${drive.id}/applicants`" class="switch-link">
                      View Applicants
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </template>

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
                <span class="badge" :class="statusBadgeClass(drive.status)">{{
                  drive.status
                }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
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
.details-card,
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

.btn-custom {
  background-color: #38bdf8;
  color: #020617;
  font-weight: 700;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  border: none;
  text-decoration: none;
  display: inline-block;
}
.btn-custom:hover:not(:disabled) {
  background-color: #34d399;
  color: #020617;
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
