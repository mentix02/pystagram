import useAuthStore from "@/stores/auth";
import configureEndpoint from "@/api/host";
import type { Post } from "@/api/types/post";

const BASE_URl = configureEndpoint("api/v1/feed");

export const getFeedPosts = async (): Promise<Post[]> => {
  let response: Response;
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) {
    throw new Error("User is not authenticated.");
  }

  try {
    response = await fetch(`${BASE_URl}/`, {
      headers: { Authorization: `Token ${authStore.token}` },
    });
  } catch (error) {
    throw new Error("Network error.");
  }

  if (response.ok) {
    return await response.json();
  } else {
    throw new Error("Failed to fetch posts.");
  }
};
