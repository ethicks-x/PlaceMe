<script setup>
  import { onMounted, ref } from "vue";
  import axios from "axios";
  import { router } from "../../router";

  const isLoading = ref(true);
  const loadError = ref("");

  const form = ref({
    jobTitle: "",
    jobDesc: "",
    eligibility: "",
    minCgpa: "",
    eligibleGraduationYear: "",
    deadline: "",
  });
  const isSubmitting = ref(false);
  const formError = ref("");
  const formSuccess = ref("");
  const todayDate = new Date().toISOString().split("T")[0];

  onMounted(async () => {
    try {
      const { data } = await axios.get("/api/company/status");
      if (data.approvalStatus !== "approved") {
        router.replace("/company/pending");
        return;
      }
    } catch (err) {
      loadError.value = "Could not load your company details.";
    } finally {
      isLoading.value = false;
    }
  });

  const handleCreate = async () => {
    formError.value = "";
    formSuccess.value = "";

    if (form.value.deadline < todayDate) {
      formError.value = "The application deadline must be in the future.";
      return;
    }

    isSubmitting.value = true;

    try {
      await axios.post("/api/company/drives", {
        jobTitle: form.value.jobTitle,
        jobDesc: form.value.jobDesc,
        eligibility: form.value.eligibility,
        minCgpa: form.value.minCgpa || null,
        eligibleGraduationYear: form.value.eligibleGraduationYear || null,
        deadline: new Date(form.value.deadline).toISOString(),
      });
      formSuccess.value = "Drive submitted for admin approval.";
      form.value = {
        jobTitle: "",
        jobDesc: "",
        eligibility: "",
        minCgpa: "",
        eligibleGraduationYear: "",
        deadline: "",
      };
    } catch (err) {
      formError.value = err.response?.data?.message || "Failed to create drive.";
    } finally {
      isSubmitting.value = false;
    }
  };
</script>

<template>
  <b-container class="py-5" style="max-width: 700px">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="mb-0">Post a New Drive</h1>
      <router-link to="/company/dashboard" class="switch-link"
        >&larr; Back to Dashboard</router-link
      >
    </div>

    <div v-if="isLoading" class="text-muted">Loading...</div>
    <div v-else-if="loadError" class="alert alert-danger">{{ loadError }}</div>

    <div v-else class="form-card">
      <div v-if="formError" class="alert alert-danger py-2">{{ formError }}</div>
      <div
        v-if="formSuccess"
        class="alert alert-success py-2 d-flex justify-content-between align-items-center"
      >
        <span>{{ formSuccess }}</span>
        <router-link to="/company/dashboard" class="switch-link"
          >View your drives &rarr;</router-link
        >
      </div>

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
        <div class="row">
          <div class="col-6 mb-3">
            <label class="form-label">Minimum CGPA</label>
            <input
              type="number"
              step="0.1"
              min="0"
              max="10"
              class="form-control"
              v-model="form.minCgpa"
              placeholder="e.g. 7.5"
            />
          </div>
          <div class="col-6 mb-3">
            <label class="form-label">Eligible Graduation Year</label>
            <input
              type="number"
              class="form-control"
              v-model="form.eligibleGraduationYear"
              placeholder="e.g. 2026"
            />
          </div>
        </div>
        <div class="mb-3">
          <label class="form-label">Application Deadline</label>
          <input
            type="date"
            class="form-control"
            v-model="form.deadline"
            :min="todayDate"
            required
          />
        </div>
        <button type="submit" class="btn btn-custom" :disabled="isSubmitting">
          Submit for Approval
        </button>
      </form>
    </div>
  </b-container>
</template>

<style scoped>
  .form-card {
    background: rgba(30, 41, 59, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    padding: 1.5rem;
  }

  .switch-link {
    color: #38bdf8;
    text-decoration: none;
    font-weight: 500;
  }
  .switch-link:hover {
    color: #34d399;
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
</style>
