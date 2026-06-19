import { createWebHistory, createRouter } from "vue-router";

import HomeView from "../views/home.vue";
import AboutView from "../views/about.vue";
import LoginView from "../views/login.vue";

const routes = [
    { path: "/", component: HomeView },
    { path: "/about", component: AboutView },
    { path: "/login", component: LoginView },
    { path: "/signup", component: LoginView },
];

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});
