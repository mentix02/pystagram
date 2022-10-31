import { blikeFactory, BlikeType } from "@/api/blike";

const { createBlike: createBookmark, removeBlike: removeBookmark } =
  blikeFactory(BlikeType.BOOKMARK);

export { createBookmark, removeBookmark };
