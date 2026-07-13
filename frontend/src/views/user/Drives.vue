<script setup>
import { computed, onMounted, ref } from "vue";
import axios from "axios";

const drives = ref([]);
const isLoading = ref(true);
const error = ref("");
const applyingId = ref(null);
const applyError = ref("");
const search = ref("");
const profileComplete = ref(true);
const missingProfileFields = ref([]);

const filteredDrives = computed(() => {
  const query = search.value.trim().toLowerCase();
  if (!query) return drives.value;
  return drives.value.filter(
    (drive) =>
      drive.jobTitle.toLowerCase().includes(query) ||
      drive.companyName.toLowerCase().includes(query) ||
      drive.eligibility.toLowerCase().includes(query),
  );
});

const fetchDrives = async () => {
  try {
    const { data } = await axios.get("/api/drives");
    drives.value = data;
  } catch (err) {
    error.value = "Could not load placement drives.";
  } finally {
    isLoading.value = false;
  }
};

const fetchProfileStatus = async () => {
  try {
    const { data } = await axios.get("/api/profile");
    profileComplete.value = data.profileComplete !== false;
    missingProfileFields.value = data.missingProfileFields || [];
  } catch (err) {
    profileComplete.value = true;
  }
};

onMounted(() => {
  fetchDrives();
  fetchProfileStatus();
});

const applyToDrive = async (driveId) => {
  applyError.value = "";
  applyingId.value = driveId;

  try {
    await axios.post(`/api/drives/${driveId}/apply`);
    await fetchDrives();
  } catch (err) {
    applyError.value = err.response?.data?.message || "Failed to apply.";
  } finally {
    applyingId.value = null;
  }
};
</script>

<template>
  <b-container class="drives-wrapper py-5">
    <h1 class="mb-4">Placement Drives</h1>

    <div v-if="isLoading" class="text-muted">Loading drives...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else-if="drives.length === 0" class="text-muted">
      No open placement drives right now.
    </div>

    <div v-else>
      <div v-if="!profileComplete" class="alert alert-warning profile-notice py-3 mb-4">
        <strong>Complete your profile to apply.</strong>
        Missing: {{ missingProfileFields.join(", ") }}.
        <router-link to="/profile" class="ms-1">Update your profile &rarr;</router-link>
      </div>


      <input
        type="text"
        class="form-control search-input mb-4"
        placeholder="Search by role, company, or eligibility"
        v-model="search"
      />
      <div v-if="applyError" class="alert alert-danger py-2">{{ applyError }}</div>

      <div v-if="filteredDrives.length === 0" class="text-muted">
        No drives match your search.
      </div>

      <div v-for="drive in filteredDrives" :key="drive.id" class="drive-card mb-3">
        <div class="d-flex justify-content-between align-items-start flex-wrap gap-3">
          <div>
            <h3 class="mb-1">{{ drive.jobTitle }}</h3>
            <p class="company-name mb-2">{{ drive.companyName }}</p>
            <p class="mb-1">{{ drive.jobDesc }}</p>
            <p class="mb-1"><strong>Eligibility:</strong> {{ drive.eligibility }}</p>
            <p class="mb-1" v-if="drive.minCgpa !== null || drive.eligibleGraduationYear !== null">
              <strong>Requirements:</strong>
              <span v-if="drive.minCgpa !== null">Min CGPA {{ drive.minCgpa }}</span>
              <span v-if="drive.minCgpa !== null && drive.eligibleGraduationYear !== null"> &middot; </span>
              <span v-if="drive.eligibleGraduationYear !== null"
                >{{ drive.eligibleGraduationYear }} batch only</span
              >
            </p>
            <p class="mb-1">
              <strong>Deadline:</strong> {{ new Date(drive.deadline).toLocaleDateString() }}
            </p>
            <p v-if="profileComplete && !drive.isEligible && !drive.hasApplied" class="mb-0 ineligible-note">
              {{ drive.ineligibleReason }}
            </p>
          </div>
          <button
            class="btn btn-custom"
            :disabled="drive.hasApplied || drive.isExpired || !profileComplete || !drive.isEligible || applyingId === drive.id"
            :title="!profileComplete ? 'Complete your profile before applying' : drive.ineligibleReason || ''"
            @click="applyToDrive(drive.id)"
          >
            <span v-if="drive.hasApplied">Applied</span>
            <span v-else-if="drive.isExpired">Closed</span>
            <span v-else-if="!profileComplete">Complete profile first</span>
            <span v-else-if="!drive.isEligible">Ineligible</span>
            <span v-else-if="applyingId === drive.id">Applying...</span>
            <span v-else>Apply</span>
          </button>
        </div>
      </div>
    </div>
  </b-container>
</template>

<style scoped>

.profile-notice {
  background-color: rgba(250, 204, 21, 0.12);
  border: 1px solid rgba(250, 204, 21, 0.35);
  color: #facc15;
}

.profile-notice a {
  color: #38bdf8;
  font-weight: 600;
  text-decoration: none;
}

.profile-notice a:hover {
  color: #34d399;
}

.ineligible-note {
  color: #f87171;
  font-size: 0.85rem;
  font-weight: 600;
}

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

.drive-card {
  background: rgba(30, 41, 59, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem;
}

.company-name {
  color: #94a3b8;
}

.btn-custom {
  background-color: #38bdf8;
  color: #020617;
  font-weight: 700;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  border: none;
  white-space: nowrap;
}
.btn-custom:hover:not(:disabled) {
  background-color: #34d399;
}
.btn-custom:disabled {
  background-color: #64748b;
  color: #94a3b8;
}
</style>

