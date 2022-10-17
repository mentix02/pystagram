import { blikeFactory, BlikeType } from "@/api/blike";

const { createBlike, removeBlike } = blikeFactory(BlikeType.LIKE);

const createLike = createBlike;
const removeLike = removeBlike;

export { createLike, removeLike };
