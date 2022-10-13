<template>
  <div class="container">
    <header
      class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom"
    >
      <router-link
        id="logo"
        :to="{ name: 'home' }"
        class="d-flex align-items-center col-md-3 mb-2 mb-md-0 text-dark text-decoration-none"
      >
        Pystagram
      </router-link>

      <div class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
        <div class="input-group">
          <input type="search" class="form-control" placeholder="Search" />
          <button type="button" class="btn btn-outline-secondary">
            <i class="bi-search"></i>
          </button>
        </div>
      </div>

      <div class="col-md-3 text-end">
        <template v-if="authStore.isAuthenticated">
          <router-link
            :to="{ name: 'home' }"
            class="btn btn-link link-dark me-2"
          >
            <i class="bi-house-fill"></i>
          </router-link>
          <router-link
            :to="{ name: 'explore' }"
            class="btn btn-link link-dark me-2"
          >
            <i class="bi-compass-fill"></i>
          </router-link>
          <router-link
            :to="{ name: 'notifications' }"
            class="btn btn-link link-dark me-2"
          >
            <i class="bi-heart-fill"></i>
          </router-link>
          <router-link
            :to="{
              name: 'profile',
              params: { username: authStore.user?.username },
            }"
            class="btn btn-link link-dark me-2"
          >
            <i class="bi-person-fill"></i>
          </router-link>
        </template>
        <template v-else>
          <router-link
            :to="{ name: 'login' }"
            class="btn btn-outline-dark me-2"
          >
            Log in
          </router-link>
          <router-link :to="{ name: 'signup' }" class="btn btn-dark">
            Sign up
          </router-link>
        </template>
      </div>
    </header>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from "vue-router";

import useAuthStore from "@/stores/auth";

const authStore = useAuthStore();
</script>

<style scoped>
#logo {
  font-size: 35px;
  font-family: Billabong, cursive;
}
</style>
