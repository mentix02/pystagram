import { blikeFactory, BlikeType } from "@/api/blike";

const { createBlike, removeBlike } = blikeFactory(BlikeType.BOOKMARK);

const createBookmark = createBlike;
const removeBookmark = removeBlike;

export { createBookmark, removeBookmark };
