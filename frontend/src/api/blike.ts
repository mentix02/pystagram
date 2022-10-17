import useAuthStore from "@/stores/auth";
import configureEndpoint from "@/api/host";

const BASE_URl = configureEndpoint("api/v1");

export enum BlikeType {
  LIKE = "like",
  BOOKMARK = "bookmark",
}

export const blikeFactory = (blikeType: BlikeType) => {
  const createBlike = async (post_id: number): Promise<boolean> => {
    let response: Response;
    const formData = new FormData();
    const authStore = useAuthStore();

    formData.set("post_id", post_id.toString());

    if (!authStore.isAuthenticated)
      throw new Error("User is not authenticated.");

    try {
      response = await fetch(`${BASE_URl}/${blikeType}/create/`, {
        method: "POST",
        body: formData,
        headers: { Authorization: `Token ${authStore.token}` },
      });
    } catch (error) {
      throw new Error("Network error.");
    }

    if (response.ok) return true;
    else throw new Error("Something went wrong.");
  };

  const removeBlike = async (post_id: number): Promise<boolean> => {
    let response: Response;
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated)
      throw new Error("User is not authenticated.");

    try {
      response = await fetch(`${BASE_URl}/${blikeType}/delete/${post_id}/`, {
        method: "DELETE",
        headers: { Authorization: `Token ${authStore.token}` },
      });
    } catch (error) {
      throw new Error("Network error.");
    }

    if (response.ok) return true;
    else throw new Error("Something went wrong.");
  };

  return { createBlike, removeBlike };
};
