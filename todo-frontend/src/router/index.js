import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Dashboard from "../views/Dashboard.vue";
import Register from "../views/Register.vue";

// ✅ Step 1: Handle Google redirect before router guard
if (window.location.search.includes("access=") && window.location.search.includes("refresh=")) {
  const params = new URLSearchParams(window.location.search);
  const access = params.get("access");
  const refresh = params.get("refresh");
  const email = params.get("email");
  const name = params.get("name");
  const picture = params.get("picture");

  if (access && refresh) {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    localStorage.setItem("user_email", email || "");
    localStorage.setItem("user_name", name || "");
    localStorage.setItem("user_picture", picture || "");

    // ✅ Clean URL so query params disappear
    window.history.replaceState({}, document.title, "/");
  }
}

// ✅ Step 2: Define routes
const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/",
    name: "Dashboard",
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
];

// ✅ Step 3: Create router
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ✅ Step 4: Global navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");

  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else if (to.path === "/login" && token) {
    next("/");
  } else {
    next();
  }
});

export default router;
