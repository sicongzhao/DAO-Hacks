import { createApp } from 'vue'
import App from './App.vue'
import store from "./store/store"
import './assets/tailwind.css'
import router from './router'
import HistogramSlider from "vue3-histogram-slider";
import "vue3-histogram-slider/dist/histogram-slider.css";


createApp(App).use(store).use(router).component(HistogramSlider.name, HistogramSlider).mount('#app')