// router/index.js
import FormServiceRequest from "@/views/FormServiceRequest.vue";
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";
import Service from "@/views/Service.vue";
import ServiceDetail from "@/views/ServiceDetail.vue";
import { createRouter, createWebHistory } from "vue-router";
import ServiceRequest from "@/views/ServiceRequest.vue";
import ServiceNote from "@/views/ServiceNote.vue";
import BarChart from "@/components/charts/Bar.vue";
import LineChart from "@/components/charts/Line.vue";
import RadarChart from "@/components/charts/Radar.vue";
import DoughnutChart from "@/components/charts/Doughnut.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/service",
    name: "Service",
    component: Service,
  },
  {
    path: "/service/detail/:id",
    name: "ServiceDetail",
    component: ServiceDetail,
  },
  {
    path: "/service/request/:id",
    name: "FormServiceRequest",
    component: FormServiceRequest,
  },
  {
    path: "/chart/bar",
    name: "BarChart",
    component: BarChart,
  },
  {
    path: "/chart/line",
    name: "LineChart",
    component: LineChart,
  },
  {
    path: "/chart/radar",
    name: "RadarChart",
    component: RadarChart,
  },
  {
    path: "/chart/doughnut",
    name: "DoughnutChart",
    component: DoughnutChart,
  },
  {
    path: "/request/",
    name: "ServiceRequest",
    component: ServiceRequest,
  },
  {
    path: "/request/notes/:id",
    name: "ServiceNote",
    component: ServiceNote,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;