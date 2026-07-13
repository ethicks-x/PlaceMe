<script setup>
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'
import { useAuth } from '../../store/auth'

const { authState } = useAuth()

const isStudent = computed(() => authState.user?.role === 'student')

const form = ref({
  fullName: '',
  mobile: '',
  degree: '',
  graduationYear: '',
  cgpa: '',
  resumeUrl: '',
  skills: '',
  bio: '',
})
const isLoading = ref(true)
const isSaving = ref(false)
const error = ref('')
const successMessage = ref('')

onMounted(async () => {
  try {
    const { data } = await axios.get('/api/profile')
    form.value.fullName = data.fullName || ''
    form.value.mobile = data.mobile || ''
    form.value.degree = data.degree || ''
    form.value.graduationYear = data.graduationYear || ''
    form.value.cgpa = data.cgpa ?? ''
    form.value.resumeUrl = data.resumeUrl || ''
    form.value.skills = data.skills || ''
    form.value.bio = data.bio || ''
  } catch (err) {
    error.value = 'Could not load your profile.'
  } finally {
    isLoading.value = false
  }
})

const handleSave = async () => {
  error.value = ''
  successMessage.value = ''
  isSaving.value = true

  try {
    await axios.put('/api/profile', form.value)
    successMessage.value = 'Profile updated successfully.'
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to update profile.'
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <b-container class="profile-wrapper py-5" style="max-width: 600px">
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

      <template v-if="isStudent">
        <hr class="section-divider" />
        <h2 class="section-title">Academic &amp; Resume</h2>

        <div class="mb-3">
          <label class="form-label" for="profileDegree">Degree / Branch</label>
          <input
            id="profileDegree"
            type="text"
            class="form-control"
            v-model="form.degree"
            placeholder="e.g. B.Tech Computer Science"
          />
        </div>
        <div class="row">
          <div class="col-6 mb-3">
            <label class="form-label" for="profileGradYear">Graduation Year</label>
            <input
              id="profileGradYear"
              type="number"
              class="form-control"
              v-model="form.graduationYear"
              placeholder="2027"
            />
          </div>
          <div class="col-6 mb-3">
            <label class="form-label" for="profileCgpa">CGPA</label>
            <input
              id="profileCgpa"
              type="number"
              step="0.01"
              min="0"
              max="10"
              class="form-control"
              v-model="form.cgpa"
              placeholder="8.5"
            />
          </div>
        </div>
        <div class="mb-3">
          <label class="form-label" for="profileResume">Resume URL</label>
          <input
            id="profileResume"
            type="url"
            class="form-control"
            v-model="form.resumeUrl"
            placeholder="https://..."
          />
        </div>
        <div class="mb-3">
          <label class="form-label" for="profileSkills">Skills</label>
          <input
            id="profileSkills"
            type="text"
            class="form-control"
            v-model="form.skills"
            placeholder="Python, React, SQL"
          />
        </div>
        <div class="mb-3">
          <label class="form-label" for="profileBio">Bio</label>
          <textarea
            id="profileBio"
            class="form-control"
            rows="3"
            v-model="form.bio"
            placeholder="A short summary about yourself"
          ></textarea>
        </div>
      </template>

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

.section-divider {
  border-color: rgba(255, 255, 255, 0.1);
  margin: 2rem 0 1.5rem;
}
.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 1rem;
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
