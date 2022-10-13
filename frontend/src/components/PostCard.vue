<template>
  <div class="card">
    <div class="card-header" style="padding-bottom: 2px">
      <a href="#">
        <img
          :src="post.user.avatar"
          class="card-user-avatar"
          :alt="`${post.user.first_name} ${post.user.last_name}`"
        />
      </a>
      <span class="mx-2">
        <a href="#" class="text-dark">
          {{ post.user.username }}
        </a>
      </span>
    </div>
    <img
      :alt="post.caption"
      :src="post.images[0].file"
      class="card-img-top img-fluid"
    />
    <div class="card-body">
      <p class="card-text">
        {{ post.caption }}
        <br />
        <span class="text-muted"> {{ post.timestamp }} </span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { toggleLike } from "@/api/like";
import useAlertStore from "@/stores/alert";
import type { Post } from "@/api/types/post";

const alertStore = useAlertStore();

const { post } = withDefaults(
  defineProps<{ post: Post; disabled?: boolean }>(),
  { disabled: false }
);

const handleLikeClickUiUpdate = () => {
  if (post.is_liked) {
    post.like_count -= 1;
  } else {
    post.like_count += 1;
  }
  post.is_liked = !post.is_liked;
};

const handleLikeClick = async () => {
  handleLikeClickUiUpdate();
  try {
    await toggleLike(post.id);
  } catch (err: any) {
    alertStore.alertDangerMsg(err.message);
    // revert UI update
    handleLikeClickUiUpdate();
  }
};
</script>

<style scoped>
.card-user-avatar {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  vertical-align: middle;
}
</style>
