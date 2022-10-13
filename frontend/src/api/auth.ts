import configureEndpoint from "@/api/host";
import type { Credentials, TokenResponse, SignUpData } from "@/api/types/auth";

const BASE_URl = configureEndpoint("api/v1/user");

export const checkUsernameAvailability = async (
  username: string
): Promise<boolean> => {
  let response: Response;
  const url = `${BASE_URl}/username-availability/?username=${username}`;
  try {
    response = await fetch(url);
  } catch (error) {
    throw new Error("Network error.");
  }
  if (response.ok) {
    const data = await response.json();
    return data.available;
  } else {
    throw new Error("Network error.");
  }
};

export const signUpUser = async (
  signUpData: SignUpData
): Promise<TokenResponse> => {
  let response: Response;
  const formData = new FormData();
  const url = `${BASE_URl}/create/`;

  formData.set("bio", signUpData.bio);
  formData.set("name", signUpData.name);
  formData.set("email", signUpData.email);
  formData.set("avatar", signUpData.avatar!);
  formData.set("username", signUpData.username);
  formData.set("password", signUpData.password);

  try {
    response = await fetch(url, {
      method: "POST",
      body: formData,
    });
  } catch (error) {
    throw new Error("Network error.");
  }

  if (response.ok) {
    return await response.json();
  } else {
    throw new Error(`Error: ${JSON.stringify(await response.json())}`);
  }
};

export const getTokenResponse = async (
  credentials: Credentials
): Promise<TokenResponse> => {
  let response: Response;
  const formData = new FormData();
  const { username, password } = credentials;

  formData.set("username", username);
  formData.set("password", password);

  try {
    response = await fetch(`${BASE_URl}/token/`, {
      method: "POST",
      body: formData,
    });
  } catch (error) {
    throw new Error("Unable to connect to server. Network error.");
  }

  if (response.ok) {
    return (await response.json()) as TokenResponse;
  } else {
    throw new Error("Invalid credentials.");
  }
};
