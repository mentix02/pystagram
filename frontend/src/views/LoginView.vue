<template>
  <div class="text-center">
    <div class="form-signin w-100 m-auto">
      <form @submit.prevent="handleLogin">
        <img
          alt="logo"
          width="72"
          height="72"
          class="mb-4"
          src="/favicon.png"
        />

        <h1 class="h3 mb-3 fw-normal">Sign in</h1>

        <div class="form-floating">
          <input
            required
            type="text"
            id="username"
            ref="usernameInput"
            class="form-control"
            placeholder="Username"
            autocomplete="username"
            v-model="credentials.username"
          />
          <label for="username">Username</label>
        </div>
        <div class="form-floating">
          <input
            required
            id="password"
            type="password"
            class="form-control"
            placeholder="Password"
            v-model="credentials.password"
            autocomplete="current-password"
          />
          <label for="password">Password</label>
        </div>

        <div class="checkbox mb-3">
          <label>
            <input type="checkbox" value="remember-me" /> Remember me
          </label>
        </div>
        <button class="w-100 btn btn-lg btn-primary" type="submit">
          Sign in
        </button>
        <p class="mt-5 mb-3 text-muted">&copy; 2022–2022</p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import { ref, watch, reactive, onMounted } from "vue";

import useAuthStore from "@/stores/auth";
import useAlertStore from "@/stores/alert";
import useLoaderStore from "@/stores/loader";
import { getTokenResponse } from "@/api/auth";
import { setDocumentTitle } from "@/views/utils";
import type { Credentials } from "@/api/types/auth";

const credentials = reactive<Credentials>({
  username: "",
  password: "",
});

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const alertStore = useAlertStore();
const loaderStore = useLoaderStore();
const usernameInput = ref<HTMLInputElement>();

watch(
  () => authStore.isAuthenticated,
  (isAuthenticated) => {
    if (isAuthenticated) {
      const redirect = route.query.redirect as string;
      if (redirect) {
        router.push(redirect);
      } else {
        router.push({ name: "home" });
      }
    }
  }
);

const handleLogin = async () => {
  loaderStore.start();
  try {
    const tokenResponse = await getTokenResponse(credentials);
    alertStore.alertSuccessMsg(`Welcome back, ${credentials.username}!`);
    authStore.login(tokenResponse);
  } catch (err: any) {
    alertStore.alertDangerMsg(err.message);
  } finally {
    loaderStore.stop();
  }
};

onMounted(() => {
  setDocumentTitle("Login");
  usernameInput.value?.focus();
});
</script>

<style scoped>
@import "styles/auth.css";
</style>
