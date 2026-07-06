<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import { useAuth } from "../../store/auth";

const { authState } = useAuth();

const form = ref({ fullName: "", mobile: "" });
const isLoading = ref(true);
const isSaving = ref(false);
const error = ref("");
const successMessage = ref("");

onMounted(async () => {
  try {
    const { data } = await axios.get("/api/profile");
    form.value.fullName = data.fullName || "";
    form.value.mobile = data.mobile || "";
  } catch (err) {
    error.value = "Could not load your profile.";
  } finally {
    isLoading.value = false;
  }
});

const handleSave = async () => {
  error.value = "";
  successMessage.value = "";
  isSaving.value = true;

  try {
    await axios.put("/api/profile", form.value);
    successMessage.value = "Profile updated successfully.";
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to update profile.";
  } finally {
    isSaving.value = false;
  }
};
</script>

<template>
  <b-container class="profile-wrapper py-5" style="max-width: 500px">
    <h1 class="mb-4">My Profile</h1>

    <div v-if="isLoading" class="text-muted">Loading profile...</div>

    <form v-else @submit.prevent="handleSave">
      <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
      <div v-if="successMessage" class="alert alert-success py-2">{{ successMessage }}</div>

      <div class="mb-3">
        <label class="form-label">Email</label>
        <input type="email" class="form-control" :value="authState.user?.email" disabled />
      </div>
      <div class="mb-3">
        <label class="form-label">Full Name</label>
        <input type="text" class="form-control" v-model="form.fullName" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Mobile</label>
        <input type="text" class="form-control" v-model="form.mobile" required />
      </div>

      <button type="submit" class="btn btn-custom" :disabled="isSaving">Save Changes</button>
    </form>
  </b-container>
</template>

<style scoped>
.form-control {
  background-color: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #f8fafc !important;
  padding: 0.85rem 1rem;
  border-radius: 0.5rem;
}
.form-control:disabled {
  opacity: 0.6;
}
.form-label {
  color: #94a3b8;
}

.btn-custom {
  background-color: #38bdf8;
  color: #020617;
  font-weight: 700;
  padding: 0.85rem 1.75rem;
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
</style>

