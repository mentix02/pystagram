<template>
  <!-- block button to log out -->
  <div class="row justify-content-center text-center">
    <div class="col-sm-12 col-md-4">
      <div class="d-grid">
        <button class="btn btn-outline-danger" @click="logout">Sign Out</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";

import useAuthStore from "@/stores/auth";
import useAlertStore from "@/stores/alert";

const router = useRouter();
const authStore = useAuthStore();
const alertStore = useAlertStore();

const logout = () => {
  authStore.logout();
  alertStore.alertSuccessMsg("Successfully logged out.");
  router.push({ name: "login" });
};
</script>
