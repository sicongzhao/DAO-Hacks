import { createWebHistory, createRouter } from "vue-router";
import Home from "../components/Home.vue";
import DAO from "../components/DAO.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/dao/:daoid",
    name: "Dao",
    component: DAO,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;