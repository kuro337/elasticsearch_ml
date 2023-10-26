import { Post } from "../entity/models/post";
import { Score } from "../entity/models/score";

export function sortPostsByScores(posts: Post[], scores: Score[]): Post[] {
  return posts.sort((a, b) => {
    const scoreA =
      scores.find((score) => score.post_id === a.post_id)?.score || 0;
    const scoreB =
      scores.find((score) => score.post_id === b.post_id)?.score || 0;
    return scoreB - scoreA;
  });
}
