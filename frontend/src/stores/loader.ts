import { defineStore, acceptHMRUpdate } from "pinia";

type LoaderState = {
  loading: boolean;
};

const useLoaderStore = defineStore("loader", {
  state: (): LoaderState => ({
    loading: false,
  }),

  actions: {
    start() {
      this.loading = true;
    },
    stop() {
      this.loading = false;
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useLoaderStore, import.meta.hot));
}

export default useLoaderStore;
