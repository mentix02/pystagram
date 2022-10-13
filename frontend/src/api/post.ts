import useAuthStore from "@/stores/auth";
import configureEndpoint from "@/api/host";
import type { Post } from "@/api/types/post";

const BASE_URl = configureEndpoint("api/v1/post");

export const createPost = async (
  images: File[],
  caption: string
): Promise<Post> => {
  let response: Response;
  const formData = new FormData();
  const authStore = useAuthStore();

  formData.set("caption", caption);

  for (const image of images) {
    formData.append("images", image);
  }

  try {
    response = await fetch(`${BASE_URl}/create/`, {
      method: "POST",
      body: formData,
      headers: { Authorization: `Token ${authStore.token}` },
    });
  } catch (error) {
    throw new Error("Network error.");
  }

  if (response.ok) {
    return await response.json();
  } else {
    console.error(response);
    throw new Error("Cannot create post at this time.");
  }
};
