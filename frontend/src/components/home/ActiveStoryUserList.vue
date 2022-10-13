<template>
  <!-- horizontal scrolling avatar list -->
  <div class="d-flex flex-row flex-nowrap overflow-auto">
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
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import type { User } from "@/api/types/auth";
import { getActiveStoryFollowing } from "@/api/story";

const users = ref<User[]>([]);

onMounted(async () => {
  users.value = await getActiveStoryFollowing();
});
</script>
