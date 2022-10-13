import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import SignUpView from "@/views/SignUpView.vue";

import useAuthStore from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/signup",
      name: "signup",
      component: SignUpView,
    },
    {
      path: "/explore",
      name: "explore",
      component: () => import("@/views/ExploreView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/notifications",
      name: "notifications",
      meta: { requiresAuth: true },
      component: () => import("@/views/NotificationsView.vue"),
    },
    {
      path: "/profile/:username",
      name: "profile",
      component: () => import("@/views/ProfileView.vue"),
    },
    {
      path: "/bookmarks",
      name: "bookmarks",
      meta: { requiresAuth: true },
      component: () => import("@/views/BookmarksView.vue"),
    },
    {
      path: "/create",
      name: "create",
      meta: { requiresAuth: true },
      component: () => import("@/views/CreatePostView.vue"),
    },
  ],
});

router.beforeEach((to, _) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: "login", query: { redirect: to.fullPath } };
  } else if (
    (to.name === "login" || to.name === "signup") &&
    authStore.isAuthenticated
  ) {
    return { name: "home" };
  }

  return true;
});

export default router;
