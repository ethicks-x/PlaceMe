<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const drives = ref([]);
const isLoading = ref(true);
const error = ref("");
const applyingId = ref(null);
const applyError = ref("");

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

onMounted(fetchDrives);

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
      <div v-if="applyError" class="alert alert-danger py-2">{{ applyError }}</div>

      <div v-for="drive in drives" :key="drive.id" class="drive-card mb-3">
        <div class="d-flex justify-content-between align-items-start flex-wrap gap-3">
          <div>
            <h3 class="mb-1">{{ drive.jobTitle }}</h3>
            <p class="company-name mb-2">{{ drive.companyName }}</p>
            <p class="mb-1">{{ drive.jobDesc }}</p>
            <p class="mb-1"><strong>Eligibility:</strong> {{ drive.eligibility }}</p>
            <p class="mb-0">
              <strong>Deadline:</strong> {{ new Date(drive.deadline).toLocaleDateString() }}
            </p>
          </div>
          <button
            class="btn btn-custom"
            :disabled="drive.hasApplied || drive.isExpired || applyingId === drive.id"
            @click="applyToDrive(drive.id)"
          >
            <span v-if="drive.hasApplied">Applied</span>
            <span v-else-if="drive.isExpired">Closed</span>
            <span v-else-if="applyingId === drive.id">Applying...</span>
            <span v-else>Apply</span>
          </button>
        </div>
      </div>
    </div>
  </b-container>
</template>

<style scoped>
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

