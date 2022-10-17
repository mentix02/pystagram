<template>
  <!-- horizontal scrolling avatar list -->
  <div
    v-if="!loading && users.length > 0"
    class="d-flex flex-row flex-nowrap overflow-auto"
  >
    <div
      :key="user.username"
      v-for="user in users"
      class="d-flex flex-column align-items-center mx-2"
    >
      <a :href="`/profile/${user.username}`">
        <img
          :src="user.avatar"
          class="rounded-circle"
          width="50"
          height="50"
          :alt="`${user.first_name} ${user.last_name}`"
        />
      </a>
      <span class="text-muted">{{ user.username }}</span>
    </div>
  </div>
  <div v-else-if="loading" class="d-flex justify-content-center">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div v-else>
    <span class="text-muted">No stories found.</span>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

import useAlertStore from "@/stores/alert";
import type { User } from "@/api/types/auth";
import { getActiveStoryFollowing } from "@/api/story";

const alertStore = useAlertStore();
const users = ref<User[]>([]);
const loading = ref<boolean>(true);

onMounted(async () => {
  try {
    users.value = await getActiveStoryFollowing();
  } catch (error: any) {
    alertStore.alertDangerMsg(error.message);
  } finally {
    loading.value = false;
  }
});
</script>
