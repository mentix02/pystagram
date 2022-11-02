<template>
  <div class="row">
    <div class="col-12 col-md-8 order-last order-md-first">
      <div class="row">
        <div
          v-for="post in posts"
          v-if="posts.length !== 0"
          class="col-12 col-md-8 offset-md-2"
        >
          <PostCard :key="post.id" :post="post" />
        </div>
        <div
          class="col-12 col-md-8 offset-md-2"
          v-else-if="posts.length === 0 && !loaderStore.loading"
        >
          <h3>No posts to show.</h3>
          <p class="text-muted">
            <router-link :to="{ name: 'create' }">Post an image</router-link> to
            see it here. Maybe follow some users to see their posts.
          </p>
        </div>
      </div>
    </div>
    <div class="col-12 col-md-4 order-first order-md-last">
      <HomeActionsCard />
      <div class="card text-bg-light p-3">
        <h5 class="card-title">
          Stories
          <router-link to="/" class="btn">
            <i class="bi bi-plus-square-fill" />
          </router-link>
        </h5>
        <ActiveStoryUserList />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

import { getFeedPosts } from "@/api/feed";
import useAlertStore from "@/stores/alert";
import useLoaderStore from "@/stores/loader";
import type { Post } from "@/api/types/post";
import { setDocumentTitle } from "@/views/utils";

import PostCard from "@/components/PostCard.vue";
import HomeActionsCard from "@/components/home/HomeActionsCard.vue";
import ActiveStoryUserList from "@/components/home/ActiveStoryUserList.vue";

const alertStore = useAlertStore();
const loaderStore = useLoaderStore();

const posts = ref<Post[]>([]);

onMounted(async () => {
  try {
    loaderStore.start();
    posts.value = await getFeedPosts();
  } catch (err: any) {
    alertStore.alertDangerMsg(err.message);
  } finally {
    loaderStore.stop();
  }
  setDocumentTitle("Home");
});
</script>
