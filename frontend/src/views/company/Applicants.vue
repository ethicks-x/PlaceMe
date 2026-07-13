<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const driveId = route.params.id;

const drive = ref(null);
const applicants = ref([]);
const isLoading = ref(true);
const error = ref("");
const actingId = ref(null);
const actionError = ref("");
const search = ref("");

const filteredApplicants = computed(() => {
  const query = search.value.trim().toLowerCase();
  if (!query) return applicants.value;
  return applicants.value.filter(
    applicant =>
      applicant.studentName.toLowerCase().includes(query) ||
      applicant.studentEmail.toLowerCase().includes(query) ||
      applicant.status.toLowerCase().includes(query),
  );
});

const selectedApplicant = ref(null);
const showModal = ref(false);

const viewApplicant = applicant => {
  selectedApplicant.value = applicant;
  showModal.value = true;
};

const fetchApplicants = async () => {
  try {
    const { data } = await axios.get(`/api/company/drives/${driveId}/applicants`);
    drive.value = data.drive;
    applicants.value = data.applicants;
  } catch (err) {
    error.value = err.response?.data?.message || "Could not load applicants.";
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchApplicants);

const updateStatus = async (applicantId, status) => {
  actionError.value = "";
  actingId.value = applicantId;
  try {
    await axios.put(`/api/company/applications/${applicantId}/status`, { status });
    await fetchApplicants();
  } catch (err) {
    actionError.value = err.response?.data?.message || "Failed to update status.";
  } finally {
    actingId.value = null;
  }
};

const statusBadgeClass = status =>
  ({
    applied: "badge-applied",
    shortlisted: "badge-shortlisted",
    selected: "badge-selected",
    rejected: "badge-rejected",
  })[status] || "badge-applied";
</script>

<template>
  <b-container class="py-5">
    <div v-if="isLoading" class="text-muted">Loading applicants...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <template v-else-if="drive">
      <h1 class="mb-1">Applicants</h1>
      <p class="text-muted mb-4">{{ drive.jobTitle }}</p>

      <div v-if="actionError" class="alert alert-danger py-2">{{ actionError }}</div>

      <div v-if="applicants.length === 0" class="text-muted">
        No one has applied to this drive yet.
      </div>

      <template v-else>
        <input
          type="text"
          class="form-control search-input mb-3"
          placeholder="Search by name, email, or status"
          v-model="search"
        />

        <div v-if="filteredApplicants.length === 0" class="text-muted">
          No applicants match your search.
        </div>
        <div v-else class="admin-card">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0 admin-table">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Contact</th>
                  <th>Applied On</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="applicant in filteredApplicants" :key="applicant.id">
                  <td>
                    <button class="btn-link-name" @click="viewApplicant(applicant)">
                      {{ applicant.studentName }}
                    </button>
                  </td>
                  <td>
                    <div>{{ applicant.studentEmail }}</div>
                    <div class="text-muted small">{{ applicant.studentMobile }}</div>
                  </td>
                  <td>{{ new Date(applicant.appliedDate).toLocaleDateString() }}</td>
                  <td>
                    <span class="badge" :class="statusBadgeClass(applicant.status)">{{
                      applicant.status
                    }}</span>
                  </td>
                  <td>
                    <div class="d-flex gap-2 flex-wrap">
                      <button
                        v-if="applicant.status !== 'shortlisted'"
                        class="btn btn-sm btn-shortlist"
                        :disabled="actingId === applicant.id"
                        @click="updateStatus(applicant.id, 'shortlisted')"
                      >
                        Shortlist
                      </button>
                      <button
                        v-if="applicant.status !== 'selected'"
                        class="btn btn-sm btn-select"
                        :disabled="actingId === applicant.id"
                        @click="updateStatus(applicant.id, 'selected')"
                      >
                        Select
                      </button>
                      <button
                        v-if="applicant.status !== 'rejected'"
                        class="btn btn-sm btn-reject"
                        :disabled="actingId === applicant.id"
                        @click="updateStatus(applicant.id, 'rejected')"
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
      </template>
    </template>
    <b-modal v-model="showModal" title="Applicant Details" no-footer>
      <div v-if="selectedApplicant" class="applicant-detail">
        <h3 class="mb-1">{{ selectedApplicant.studentName }}</h3>
        <p class="text-muted mb-3">
          {{ selectedApplicant.studentEmail }} &middot; {{ selectedApplicant.studentMobile }}
        </p>

        <dl class="detail-grid">
          <dt>Degree / Branch</dt>
          <dd>{{ selectedApplicant.degree || "Not provided" }}</dd>
          <dt>Graduation Year</dt>
          <dd>{{ selectedApplicant.graduationYear || "Not provided" }}</dd>
          <dt>CGPA</dt>
          <dd>{{ selectedApplicant.cgpa ?? "Not provided" }}</dd>
          <dt>Skills</dt>
          <dd>{{ selectedApplicant.skills || "Not provided" }}</dd>
          <dt>Resume</dt>
          <dd>
            <a
              v-if="selectedApplicant.resumeUrl"
              :href="selectedApplicant.resumeUrl"
              target="_blank"
              rel="noopener"
              class="switch-link"
              >View Resume</a
            >
            <span v-else>Not provided</span>
          </dd>
          <dt>Applied On</dt>
          <dd>{{ new Date(selectedApplicant.appliedDate).toLocaleDateString() }}</dd>
          <dt>Status</dt>
          <dd>
            <span class="badge" :class="statusBadgeClass(selectedApplicant.status)">{{
              selectedApplicant.status
            }}</span>
          </dd>
        </dl>

        <div v-if="selectedApplicant.bio" class="mt-3">
          <h4 class="bio-heading">Bio</h4>
          <p class="mb-0">{{ selectedApplicant.bio }}</p>
        </div>
      </div>
    </b-modal>
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
.btn-link-name {
  background: none;
  border: none;
  padding: 0;
  color: #38bdf8;
  font-weight: 600;
  text-decoration: underline;
  cursor: pointer;
}
.btn-link-name:hover {
  color: #34d399;
}

.detail-grid {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 0.5rem 1.5rem;
  margin-bottom: 0;
}
.detail-grid dt {
  color: #94a3b8;
  font-weight: 500;
}
.detail-grid dd {
  margin: 0;
}

.bio-heading {
  font-size: 1rem;
  font-weight: 700;
  color: #94a3b8;
  margin-bottom: 0.5rem;
}

.switch-link {
  color: #38bdf8;
  text-decoration: none;
}
.switch-link:hover {
  color: #34d399;
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

.btn-shortlist,
.btn-select,
.btn-reject {
  font-weight: 600;
  border: none;
  white-space: nowrap;
}
.btn-shortlist {
  background-color: rgba(250, 204, 21, 0.2);
  color: #facc15;
}
.btn-shortlist:hover:not(:disabled) {
  background-color: rgba(250, 204, 21, 0.35);
}
.btn-select {
  background-color: rgba(52, 211, 153, 0.2);
  color: #34d399;
}
.btn-select:hover:not(:disabled) {
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
