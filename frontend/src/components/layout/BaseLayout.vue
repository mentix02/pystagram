<template>
  <Navigation />
  <Alerts />
  <Progress />
  <main class="container">
    <slot />
  </main>
</template>

<script setup lang="ts">
import Alerts from "@/components/layout/Alerts.vue";
import Progress from "@/components/layout/Progress.vue";
import Navigation from "@/components/layout/Navigation.vue";
</script>
