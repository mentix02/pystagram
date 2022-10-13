import useAuthStore from "@/stores/auth";
import configureEndpoint from "@/api/host";

const BASE_URl = configureEndpoint("api/v1/like");

export const toggleLike = async (
  post_id: number,
  is_liked: boolean = false
) => {
  let response: Response;
  const formData = new FormData();
  const authStore = useAuthStore();
  const url = is_liked ? `${BASE_URl}/delete/${post_id}/` : `${BASE_URl}/like/`;

  formData.set("post_id", post_id.toString());

  if (!authStore.isAuthenticated) {
    throw new Error("User is not authenticated.");
  }

  try {
    response = await fetch(url, {
      method: is_liked ? "DELETE" : "POST",
      body: is_liked ? undefined : formData,
      headers: { Authorization: `Token ${authStore.token}` },
    });
  } catch (error) {
    throw new Error("Network error.");
  }

  if (response.ok) {
    return await response.json();
  } else {
    throw new Error("Something went wrong.");
  }
};
