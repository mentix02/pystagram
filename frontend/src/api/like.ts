import { blikeFactory, BlikeType } from "@/api/blike";

const { createBlike: createLike, removeBlike: removeLike } = blikeFactory(
  BlikeType.LIKE
);

export { createLike, removeLike };
