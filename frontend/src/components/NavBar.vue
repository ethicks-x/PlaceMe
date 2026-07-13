<script setup>
  import { computed } from "vue";
  import { useAuth } from "../store/auth";

  const props = defineProps({
    role: {
      type: String,
      default: "guest",
    },
  });

  const { logout } = useAuth();
</script>

<template>
  <b-navbar toggleable="lg" class="custom-navbar px-4 py-2">
    <b-navbar-brand to="/" class="navbar-brand-custom">
      <span class="brand-accent">Place</span>Me
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="nav-links">
        <template v-if="role === 'student'">
          <b-nav-item to="/dashboard">Dashboard</b-nav-item>
          <b-nav-item to="/drives">Drives</b-nav-item>
          <b-nav-item to="/applications">My Applications</b-nav-item>
        </template>
        <b-nav-item v-else-if="role === 'company'" to="/company/dashboard">Dashboard</b-nav-item>
        <template v-else-if="role === 'admin'">
          <b-nav-item to="/admin">Overview</b-nav-item>
          <b-nav-item to="/admin/companies">Companies</b-nav-item>
          <b-nav-item to="/admin/students">Students</b-nav-item>
          <b-nav-item to="/admin/drives">Drives</b-nav-item>
        </template>
        <template v-else>
          <b-nav-item to="/">Home</b-nav-item>
          <b-nav-item to="/about">About</b-nav-item>
        </template>
      </b-navbar-nav>

      <b-navbar-nav class="ms-auto align-items-lg-center gap-3">
        <b-nav-form class="d-flex align-items-center" v-if="role !== 'guest'">
          <b-form-input size="sm" class="me-2 search-input" placeholder="Search"></b-form-input>
          <b-button size="sm" variant="outline-light" class="search-btn" type="submit">
            <i-bi-search />
          </b-button>
        </b-nav-form>

        <b-nav-item-dropdown right class="custom-dropdown" v-if="props.role !== 'guest'">
          <template #button-content>
            <i-bi-person-circle class="me-2" />
          </template>
          <b-dropdown-item to="/profile">Profile</b-dropdown-item>
          <b-dropdown-item href="/" @click.prevent="logout">Logout</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-button
          size="md"
          variant="outline-light"
          class="login-btn"
          href="/login"
          v-if="props.role === 'guest'"
          >Login</b-button
        >
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<style scoped>
  /* Navbar style */
  .custom-navbar {
    background: rgba(15, 23, 42, 0.75) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    min-height: 9vh;
    top: 0;
    z-index: 1030;
    display: flex;
    align-items: center;
  }

  /* Logo Styling */
  .navbar-brand-custom {
    color: #f8fafc !important;
    font-weight: 700;
    font-size: 2.7rem;
    letter-spacing: -0.5px;
  }
  .brand-accent {
    color: #38bdf8;
  }

  /* Nav links colors */
  :deep(.nav-link) {
    color: #94a3b8 !important;
    font-weight: 500;
    font-size: 1.1rem;
    padding: 0 1rem;
    transition: color 0.2s ease;
  }
  :deep(.nav-link:hover),
  :deep(.nav-link:focus) {
    color: #38bdf8 !important;
  }

  /* Search Input */
  .search-input {
    font-size: 1rem;
    background-color: #0f172a !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f8fafc !important;
  }
  .search-input::placeholder {
    font-size: 1rem;
    color: #64748b;
  }

  /* Login Button */
  .login-btn {
    border-color: #38bdf8 !important;
    color: #38bdf8 !important;
  }

  .login-btn:hover {
    background-color: #38bdf8 !important;
    color: #020617 !important;
  }

  /* Search Button */
  .search-btn {
    font-size: 0.9rem;
    border-color: #38bdf8 !important;
    color: #38bdf8 !important;
  }
  .search-btn:hover {
    background-color: #38bdf8 !important;
    color: #020617 !important;
  }

  /* Dropdown Menu alignment modifications */
  :deep(.custom-dropdown) {
    display: flex;
    align-items: center;
  }
  :deep(.dropdown-menu) {
    background-color: #0f172a !important;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  :deep(.dropdown-item) {
    font-size: 1.1rem;
    color: #94a3b8 !important;
  }
  :deep(.dropdown-item:hover) {
    background-color: rgba(56, 189, 248, 0.1) !important;
    color: #38bdf8 !important;
  }
</style>
