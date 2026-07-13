import { createWebHistory, createRouter } from 'vue-router'
import { useAuth } from '../store/auth'

import AdminDashboardView from '../views/admin/Dashboard.vue'
import AdminCompaniesView from '../views/admin/Companies.vue'
import AdminStudentsView from '../views/admin/Students.vue'
import AdminDrivesView from '../views/admin/Drives.vue'

import HomeView from '../views/home.vue'
import AboutView from '../views/about.vue'
import LoginView from '../views/login.vue'
import DashboardView from '../views/user/Dashboard.vue'
import ProfileView from '../views/user/Profile.vue'
import DrivesView from '../views/user/Drives.vue'
import ApplicationsView from '../views/user/Applications.vue'

import CompanyDashboardView from '../views/company/Dashboard.vue'
import CompanyRegisterView from '../views/company/Register.vue'
import CompanyPendingView from '../views/company/Pending.vue'
import CompanyApplicantsView from '../views/company/Applicants.vue'
import CompanyPostDriveView from '../views/company/PostDrive.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/about', component: AboutView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/signup', component: LoginView },
  { path: '/dashboard', component: DashboardView, meta: { requiresAuth: true } },
  { path: '/profile', component: ProfileView, meta: { requiresAuth: true } },
  { path: '/drives', component: DrivesView, meta: { requiresAuth: true } },
  { path: '/applications', component: ApplicationsView, meta: { requiresAuth: true } },
  { path: '/company/register', component: CompanyRegisterView },
  { path: '/company/pending', component: CompanyPendingView, meta: { requiresAuth: true } },
  { path: '/company/dashboard', component: CompanyDashboardView, meta: { requiresAuth: true } },
  { path: '/company/drives/new', component: CompanyPostDriveView, meta: { requiresAuth: true } },
  {
    path: '/company/drives/:id/applicants',
    component: CompanyApplicantsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin',
    component: AdminDashboardView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/companies',
    component: AdminCompaniesView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/students',
    component: AdminStudentsView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/drives',
    component: AdminDrivesView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
]

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach(to => {
  const { authState } = useAuth()
  if (to.meta.requiresAuth && !authState.isAuthenticated) {
    return { path: '/login' }
  }
  if (to.meta.requiresAdmin && authState.user?.role !== 'admin') {
    return { path: '/dashboard' }
  }
})
