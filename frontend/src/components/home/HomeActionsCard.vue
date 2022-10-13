<template>
  <div class="card text-bg-light p-3 mb-3">
    <div class="btn-group">
      <router-link :to="{ name: 'create' }" class="btn btn-outline-dark">
        <i class="bi-plus-square-fill"></i>
      </router-link>
      <router-link :to="{ name: 'bookmarks' }" class="btn btn-outline-dark">
        <i class="bi-bookmark-fill"></i>
      </router-link>
    </div>
  </div>
</template>
