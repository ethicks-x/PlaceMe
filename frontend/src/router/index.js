import { createWebHistory, createRouter } from 'vue-router'

import HomeView from '../views/home.vue'
import AboutView from '../views/about.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/about', component: AboutView },
]

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})
