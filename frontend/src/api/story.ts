import useAuthStore from "@/stores/auth";
import configureEndpoint from "@/api/host";
import type { User } from "@/api/types/auth";

const BASE_URl = configureEndpoint("api/v1/story");

export const getActiveStoryFollowing = async (): Promise<User[]> => {
  let response: Response;
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) throw new Error("User is not authenticated");

  try {
    response = await fetch(`${BASE_URl}/active-story-following/`, {
      headers: { Authorization: `Token ${authStore.token}` },
    });
  } catch (err) {
    throw new Error("Network error.");
  }

  if (response.ok) {
    return await response.json();
  } else {
    throw new Error("Cannot fetch stories at this time.");
  }
};
