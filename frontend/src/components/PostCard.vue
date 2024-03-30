<template>
  <div class="card mt-sm-3 my-lg-3">
    <div class="card-header" style="padding-bottom: 2px">
      <img
        :src="post.user.avatar"
        class="card-user-avatar"
        :alt="`${post.user.first_name} ${post.user.last_name}`"
      />
      <span class="mx-2">
        <router-link
          class="text-dark"
          :to="{
            name: 'profile',
            params: { username: post.user.username },
          }"
        >
          {{ post.user.username }}
        </router-link>
      </span>
    </div>
    <img
      :alt="post.caption"
      :src="post.images[0].file"
      @dblclick="handleLikeClick"
      class="card-img-top img-fluid"
    />
    <div class="card-body">
      <div>
        <div class="float-start">
          <div class="btn-group">
            <button
              class="btn"
              :disabled="disabled"
              @click="handleLikeClick"
              :class="{ 'text-danger': post.is_liked }"
            >
              <i
                class="bi"
                :class="{
                  'bi-heart': !post.is_liked,
                  'bi-heart-fill': post.is_liked,
                }"
              />
            </button>
            <button class="btn" :disabled="disabled">
              <i class="bi bi-chat" />
            </button>
            <button class="btn" :disabled="disabled">
              <i class="bi bi-send" />
            </button>
          </div>
        </div>
        <div class="float-end">
          <button class="btn" :disabled="disabled">
            <i class="bi bi-bookmark" />
          </button>
        </div>
      </div>
      <br />
      <br />
      <p class="card-text">
        <router-link
          class="text-dark"
          :to="{ name: 'profile', params: { username: post.user.username } }"
        >
          <b>{{ post.user.username }}</b>
        </router-link>
        {{ post.caption }}
        <span class="text-muted float-end">
          {{ post.comment_count }} comments
        </span>
        <br />
        <span class="text-muted"> {{ post.timestamp }} </span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import useAlertStore from "@/stores/alert";
import type { Post } from "@/api/types/post";
import { createLike, removeLike } from "@/api/like";
import { createBookmark, removeBookmark } from "@/api/bookmark";

const alertStore = useAlertStore();

const props = withDefaults(defineProps<{ post: Post; disabled?: boolean }>(), {
  disabled: false,
});

const handleLikeClickUiUpdate = () => {
  if (props.post.is_liked) {
    props.post.like_count -= 1;
  } else {
    props.post.like_count += 1;
  }
  props.post.is_liked = !props.post.is_liked;
};

const handleLikeClick = async (e: Event) => {
  if (props.disabled) return;
  try {
    if (props.post.is_liked) {
      if (e.type === "dblclick") return;
      await removeLike(props.post.id);
    } else {
      await createLike(props.post.id);
    }
    handleLikeClickUiUpdate();
  } catch (error: any) {
    alertStore.alertDangerMsg(error.message);
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
