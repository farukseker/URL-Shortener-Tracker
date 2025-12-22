import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import App from './App.vue'
import router from './router'

axios.defaults.baseURL = import.meta.env.VITE_API_URL

axios.interceptors.request.use(config => {
    config.headers["x-api-key"] = import.meta.env.VITE_ADMIN_TOKEN;
    return config;
})


const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('Icon', FontAwesomeIcon)

app.mount('#app')
