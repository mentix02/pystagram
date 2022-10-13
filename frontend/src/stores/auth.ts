import { defineStore, acceptHMRUpdate } from "pinia";

import type { User, TokenResponse } from "@/api/types/auth";

type AuthState = {
  user?: User;
  token?: string;
};

const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({
    user: undefined,
    token: undefined,
  }),

  getters: {
    isAuthenticated(): boolean {
      return !!this.token;
    },
  },

  actions: {
    logout() {
      this.$reset();
    },
    login(tokenResponse: TokenResponse) {
      const { auth_token, ...user } = tokenResponse;
      this.$patch({
        user: { ...user },
        token: auth_token,
      });
    },
  },

  persist: {
    enabled: true,
    strategies: [{ storage: localStorage }],
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}

export default useAuthStore;
