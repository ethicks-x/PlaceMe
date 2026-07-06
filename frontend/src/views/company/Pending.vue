<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const status = ref(null);
const isLoading = ref(true);
const error = ref("");

onMounted(async () => {
  try {
    const { data } = await axios.get("/api/company/status");
    status.value = data;
  } catch (err) {
    error.value = "Could not load your company status.";
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <b-container class="pending-wrapper py-5" style="max-width: 600px">
    <div v-if="isLoading" class="text-muted">Loading...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else class="status-card text-center">
      <template v-if="status.approvalStatus === 'pending'">
        <i class="bi bi-hourglass-split status-icon status-pending"></i>
        <h1 class="mb-3">Application Under Review</h1>
        <p class="text-muted">
          Thanks for registering <strong>{{ status.companyName }}</strong
          >. An admin will review your details shortly. You'll be able to post placement drives
          once approved.
        </p>
      </template>

      <template v-else-if="status.approvalStatus === 'approved'">
        <i class="bi bi-check-circle status-icon status-approved"></i>
        <h1 class="mb-3">You're Approved!</h1>
        <p class="text-muted">
          <strong>{{ status.companyName }}</strong> has been approved. Company tools are coming
          soon.
        </p>
      </template>

      <template v-else>
        <i class="bi bi-x-circle status-icon status-rejected"></i>
        <h1 class="mb-3">Application Rejected</h1>
        <p class="text-muted">{{ status.remarks }}</p>
      </template>
    </div>
  </b-container>
</template>

<style scoped>
.status-card {
  background: rgba(30, 41, 59, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 3rem 2rem;
}

.status-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  display: inline-block;
}
.status-pending {
  color: #facc15;
}
.status-approved {
  color: #34d399;
}
.status-rejected {
  color: #f87171;
}
</style>

