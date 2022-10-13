import type { User } from "@/api/types/auth";

export type Image = {
  readonly file: string;
};

export type Post = {
  readonly user: User;

  readonly id: number;
  readonly timestamp: string;

  caption: string;
  images: Image[];
  is_liked: boolean;
  like_count: number;
  comment_count: number;
};
