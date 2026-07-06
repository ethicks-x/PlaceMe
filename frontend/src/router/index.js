import { createWebHistory, createRouter } from "vue-router";
import { useAuth } from "../store/auth";

import HomeView from "../views/home.vue";
import AboutView from "../views/about.vue";
import LoginView from "../views/login.vue";
import DashboardView from "../views/user/Dashboard.vue";
import ProfileView from "../views/user/Profile.vue";
import DrivesView from "../views/user/Drives.vue";
import ApplicationsView from "../views/user/Applications.vue";

import CompanyRegisterView from "../views/company/Register.vue";
import CompanyPendingView from "../views/company/Pending.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/about", component: AboutView },
  { path: "/login", name: "login", component: LoginView },
  { path: "/signup", component: LoginView },
  { path: "/dashboard", component: DashboardView, meta: { requiresAuth: true } },
  { path: "/profile", component: ProfileView, meta: { requiresAuth: true } },
  { path: "/drives", component: DrivesView, meta: { requiresAuth: true } },
  { path: "/applications", component: ApplicationsView, meta: { requiresAuth: true } },
  { path: "/company/register", component: CompanyRegisterView },
  { path: "/company/pending", component: CompanyPendingView, meta: { requiresAuth: true } },
];

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to) => {
  const { authState } = useAuth();
  if (to.meta.requiresAuth && !authState.isAuthenticated) {
    return { path: "/login" };
  }
});
