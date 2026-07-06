import { createWebHistory, createRouter } from "vue-router";

import HomeView from "../views/home.vue";
import AboutView from "../views/about.vue";
import LoginView from "../views/login.vue";
import DashboardView from "../views/user/Dashboard.vue";
import { useAuth } from "../store/auth";

const routes = [
  { path: "/", component: HomeView },
  { path: "/about", component: AboutView },
  { path: "/login", component: LoginView },
  { path: "/signup", component: LoginView },
  { path: "/dashboard", component: DashboardView, meta: { requiresAuth: true } },
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
