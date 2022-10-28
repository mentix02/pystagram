<template>
  <form class="row" @submit.prevent="handleSignUp">
    <div class="text-center">
      <img alt="logo" width="72" height="72" class="mb-4" src="/favicon.png" />
      <h1 class="h3 mb-3 fw-normal">Sign up</h1>
    </div>

    <div class="col-12 col-lg-4 offset-lg-4">
      <div class="input-group mb-3">
        <span class="input-group-text">@</span>
        <div class="form-floating">
          <input
            required
            type="text"
            id="username"
            ref="usernameInput"
            class="form-control"
            placeholder="Username"
            autocomplete="username"
            @blur="handleUsernameBlur"
            v-model="userData.username"
            :class="{
              'is-valid': usernameIsValid,
              'is-invalid': usernameIsInvalid,
            }"
          />
          <label for="username">Username</label>
          <div class="invalid-feedback" v-if="usernameIsInvalid">
            Username is already taken.
          </div>
          <div class="valid-feedback" v-if="usernameIsValid">
            Username is available.
          </div>
        </div>
      </div>
    </div>
    <div class="col-12 col-lg-4 offset-lg-4">
      <div class="form-floating mb-3">
        <input
          required
          id="name"
          type="text"
          placeholder="Name"
          autocomplete="name"
          class="form-control"
          v-model="userData.name"
        />
        <label for="name">Name</label>
      </div>
    </div>
    <div class="col-12 col-lg-4 offset-lg-4">
      <div class="form-floating mb-3">
        <input
          required
          id="email"
          type="email"
          placeholder="Email"
          autocomplete="email"
          class="form-control"
          v-model="userData.email"
        />
        <label for="email">Email</label>
      </div>
    </div>
    <div class="col-12 col-lg-2 offset-lg-4">
      <div class="form-floating mb-3">
        <input
          required
          id="password"
          type="password"
          class="form-control"
          placeholder="Password"
          v-model="userData.password"
          autocomplete="current-password"
        />
        <label for="password">Password</label>
      </div>
    </div>
    <div class="col-12 col-lg-2">
      <div class="form-floating mb-3">
        <input
          required
          type="password"
          id="passwordConfirm"
          class="form-control"
          placeholder="Password"
          autocomplete="current-password"
          v-model="userData.confirm_password"
          :class="{ 'is-invalid': confirmPasswordNotMatch }"
        />
        <label for="passwordConfirm">Confirm Password</label>
        <div
          style="display: block"
          class="invalid-feedback"
          v-if="confirmPasswordNotMatch"
        >
          Passwords do not match.
        </div>
      </div>
    </div>
    <div class="col-12 col-lg-4 offset-lg-4 mb-3">
      <label for="avatar" class="form-label">Avatar</label>
      <input
        id="avatar"
        type="file"
        accept="image/*"
        placeholder="Avatar"
        class="form-control"
        @change.prevent="onFileChange"
      />
    </div>
    <div class="col-12 col-lg-4 offset-lg-4">
      <button class="w-100 btn btn-lg btn-primary" type="submit">
        Sign up
      </button>
      <div class="text-center">
        <p class="mt-5 mb-3 text-muted">&copy; 2022–2022</p>
      </div>
    </div>
  </form>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { ref, watch, reactive, computed, onMounted } from "vue";

import useAuthStore from "@/stores/auth";
import useAlertStore from "@/stores/alert";
import useLoaderStore from "@/stores/loader";
import { setDocumentTitle } from "@/views/utils";
import type { SignUpData } from "@/api/types/auth";
import { signUpUser, checkUsernameAvailability } from "@/api/auth";

const router = useRouter();
const authStore = useAuthStore();
const alertStore = useAlertStore();
const loaderStore = useLoaderStore();

const usernameInput = ref<HTMLInputElement>();
const usernameIsValid = ref<boolean>(false);
const usernameIsInvalid = ref<boolean>(false);

const handleUsernameBlur = async () => {
  if (userData.username.length === 0) return;
  const isAvailable = await checkUsernameAvailability(userData.username);
  usernameIsValid.value = isAvailable;
  usernameIsInvalid.value = !isAvailable;
};

const userData = reactive<SignUpData>({
  bio: "",
  name: "",
  email: "",
  username: "",
  password: "",
  avatar: undefined,
  confirm_password: "",
});

const confirmPasswordNotMatch = computed<boolean>(
  () =>
    userData.confirm_password.length > 0 &&
    userData.password !== userData.confirm_password
);

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  userData.avatar = target.files?.[0];
};

const handleSignUp = async () => {
  if (confirmPasswordNotMatch.value) return;

  try {
    loaderStore.start();
    const tokenResponse = await signUpUser(userData);
    authStore.login(tokenResponse);
    alertStore.alertSuccessMsg("Signed up successfully.");
  } catch (error: any) {
    alertStore.alertDangerMsg(error.message);
  } finally {
    loaderStore.stop();
  }
};

watch(
  () => authStore.isAuthenticated,
  async () => {
    if (authStore.isAuthenticated) await router.push({ name: "home" });
  }
);

onMounted(() => {
  setDocumentTitle("Sign Up");
  usernameInput.value?.focus();
});
</script>
