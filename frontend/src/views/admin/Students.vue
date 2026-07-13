<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const students = ref([])
const isLoading = ref(true)
const error = ref('')
const search = ref('')
const actingId = ref(null)

const fetchStudents = async () => {
  isLoading.value = true
  try {
    const { data } = await axios.get('/api/admin/students', {
      params: { search: search.value || undefined },
    })
    students.value = data
  } catch (err) {
    error.value = 'Could not load students.'
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchStudents)

const toggleActive = async student => {
  error.value = ''
  actingId.value = student.id
  try {
    await axios.post(
      `/api/admin/students/${student.id}/${student.isActive ? 'deactivate' : 'activate'}`,
    )
    await fetchStudents()
  } catch (err) {
    error.value = err.response?.data?.message || 'Action failed.'
  } finally {
    actingId.value = null
  }
}
</script>

<template>
  <b-container class="py-5">
    <h1 class="mb-4">Manage Students</h1>

    <div class="d-flex gap-3 mb-4 flex-wrap">
      <input
        type="text"
        class="form-control search-input"
        placeholder="Search by name, email, or mobile"
        v-model="search"
        @keyup.enter="fetchStudents"
      />
      <button class="btn btn-custom" @click="fetchStudents">Search</button>
    </div>

    <div v-if="isLoading" class="text-muted">Loading students...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else-if="students.length === 0" class="text-muted">No students found.</div>

    <div v-else class="admin-card">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 admin-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Mobile</th>
              <th>Account</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in students" :key="student.id">
              <td>{{ student.fullName }}</td>
              <td>{{ student.email }}</td>
              <td>{{ student.mobile }}</td>
              <td>
                <span class="badge" :class="student.isActive ? 'badge-approved' : 'badge-rejected'">
                  {{ student.isActive ? 'Active' : 'Deactivated' }}
                </span>
              </td>
              <td>
                <button
                  class="btn btn-sm btn-toggle"
                  :disabled="actingId === student.id"
                  @click="toggleActive(student)"
                >
                  {{ student.isActive ? 'Deactivate' : 'Activate' }}
                </button>
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

.badge {
  font-weight: 600;
  padding: 0.4rem 0.75rem;
}
.badge-approved {
  background-color: rgba(52, 211, 153, 0.2);
  color: #34d399;
}
.badge-rejected {
  background-color: rgba(248, 113, 113, 0.2);
  color: #f87171;
}

.btn-toggle {
  font-weight: 600;
  border: none;
  white-space: nowrap;
  background-color: rgba(148, 163, 184, 0.2);
  color: #94a3b8;
}
.btn-toggle:hover:not(:disabled) {
  background-color: rgba(148, 163, 184, 0.35);
}
</style>
