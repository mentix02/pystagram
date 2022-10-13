<template>
  <form class="row" @submit.prevent="handlePostCreation">
    <div class="col-12 col-md-6 col-lg-6 col-xl-4 offset-xl-2">
      <h3>Create Post</h3>
      <div class="mb-3">
        <label for="caption" class="form-label">Caption</label>
        <textarea
          required
          id="caption"
          v-model="caption"
          ref="captionInput"
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <label for="image" class="form-label">Images</label>
        <input
          required
          multiple
          id="image"
          type="file"
          accept="image/*"
          class="form-control"
          @change.prevent="onFileChange"
        />
      </div>
      <div class="d-grid">
        <button type="submit" class="btn btn-outline-dark">Post Images</button>
      </div>
    </div>
    <div class="col-12 col-md-6 col-lg-6 col-xl-4">
      <h3>Preview Post</h3>
      <p v-if="previewImages.length === 0">No images selected.</p>
      <PostCard :post="post" v-else />
    </div>
  </form>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { ref, computed, onMounted } from "vue";

import { createPost } from "@/api/post";
import useAuthStore from "@/stores/auth";
import useAlertStore from "@/stores/alert";
import useLoaderStore from "@/stores/loader";
import PostCard from "@/components/PostCard.vue";
import { setDocumentTitle } from "@/views/utils";
import type { Image, Post } from "@/api/types/post";

const router = useRouter();
const authStore = useAuthStore();
const alertStore = useAlertStore();
const loaderStore = useLoaderStore();

const caption = ref("");
const files = ref<File[]>([]);
const captionInput = ref<HTMLInputElement>();

const previewImages = computed<Image[]>(() =>
  files.value.map((file) => ({
    file: URL.createObjectURL(file),
  }))
);
const post = computed<Post>(() => ({
  id: 0,
  like_count: 0,
  is_liked: false,
  comment_count: 0,
  user: authStore.user!,
  caption: caption.value,
  images: previewImages.value,
  timestamp: "a few moments ago",
}));

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const fileArr = Array.from(target.files || []);

  loaderStore.start();
  if (fileArr.length > 5) {
    alertStore.alertWarningMsg("Please select only 5 images.");
  } else if (fileArr.length === 0) {
    alertStore.alertWarningMsg("Please select at least 1 image.");
  } else {
    files.value = fileArr;
  }
  loaderStore.stop();
};

const handlePostCreation = async () => {
  try {
    loaderStore.start();
    await createPost(files.value, caption.value);
    alertStore.alertSuccessMsg("Post created successfully.");
    await router.push({ name: "home" });
  } catch (err: any) {
    alertStore.alertDangerMsg(err.message);
  } finally {
    loaderStore.stop();
  }
};

onMounted(() => {
  setDocumentTitle("Create Post");
  captionInput.value?.focus();
});
</script>
