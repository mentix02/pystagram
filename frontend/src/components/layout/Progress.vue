<template>
  <div class="row mb-3" v-if="loaderStore.loading">
    <div class="col-sm-12 col-md-4 offset-md-4">
      <div class="progress">
        <div
          role="progressbar"
          :aria-valuemin="0"
          :aria-valuemax="100"
          :aria-valuenow="progress"
          :style="{ width: progress + '%' }"
          class="progress-bar progress-bar-striped bg-dark progress-bar-animated"
        >
          {{ progress }}%
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import useLoaderStore from "@/stores/loader";

const interval = ref<number>();
const progress = ref<number>(0);

const loaderStore = useLoaderStore();

// initiate pseudo progress bar which stops before 99%
watch(
  () => loaderStore.loading,
  (loading) => {
    if (loading) {
      interval.value = setInterval(() => {
        progress.value += 1;
        if (progress.value >= 99) {
          clearInterval(interval.value);
        }
      }, 25);
    } else {
      progress.value = 0;
      clearInterval(interval.value);
    }
  }
);
</script>
