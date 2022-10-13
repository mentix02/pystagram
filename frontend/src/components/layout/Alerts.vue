<template>
  <div class="row" v-if="alertStore.hasMessages">
    <div
      class="col-sm-12 col-md-4 offset-md-4"
      v-for="(alert, idx) in alertStore.messages"
    >
      <div
        :key="idx"
        class="alert alert-dismissible"
        :class="'alert-' + alert.level"
      >
        {{ alert.body }}
        <button
          type="button"
          class="btn-close"
          @click="alertStore.removeMessage(idx)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import useAlertStore from "@/stores/alert";

const alertStore = useAlertStore();
</script>
