export type Credentials = {
  username: string;
  password: string;
};

export type User = {
  avatar: string;
  username: string;
  last_name: string;
  first_name: string;
};

export type SignUpData = {
  bio: string;
  name: string;
  email: string;
  avatar?: File;
  username: string;
  password: string;
  confirm_password: string;
};

export type TokenResponse = {
  avatar: string;
  username: string;
  last_name: string;
  first_name: string;

  auth_token: string;
};
