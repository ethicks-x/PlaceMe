import { createApp } from "vue";
import { router } from "./router";
import axios from "axios";
import { createBootstrap } from "bootstrap-vue-next";
import { useAuth } from "./store/auth";

// Add the necessary CSS
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-next/dist/bootstrap-vue-next.css";
import "bootstrap-icons/font/bootstrap-icons.css";

import App from "./App.vue";

axios.defaults.baseURL = `http://${window.location.hostname}:6969`;
axios.defaults.withCredentials = true;

const { initAuth } = useAuth();

async function StartApp() {
  await initAuth();

  const app = createApp(App);

  app.use(createBootstrap());
  app.use(router);

  await router.isReady();
  app.mount("#app");
}

StartApp();
