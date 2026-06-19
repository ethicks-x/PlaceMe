import { createApp } from 'vue'
import { router } from './router'
import { createBootstrap } from 'bootstrap-vue-next'

// Add the necessary CSS
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

import App from './App.vue'

async function StartApp() {
    const app = createApp(App)

    app.use(createBootstrap());
    app.use(router);

    await router.isReady();
    app.mount('#app');
}

StartApp();
