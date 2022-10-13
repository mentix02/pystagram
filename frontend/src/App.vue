<template>
  <BaseLayout>
    <router-view />
  </BaseLayout>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";

import BaseLayout from "@/components/layout/BaseLayout.vue";
</script>
