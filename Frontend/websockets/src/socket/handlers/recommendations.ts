import { sortPostsByScores } from "../../utils/sort_posts";

export function handleRecommendationResponse(event: MessageEvent<any>) {
  console.log("Received Message from Backend:");

  if (typeof event.data === "string" && !event.data.trim().startsWith("{")) {
    console.log("Received Plain String from Backend:", event.data);
    return;
  }

  try {
    const data = JSON.parse(event.data);
    console.log("Data Parsed");

    if (data && data.data && data.data.action) {
      switch (data.data.action) {
        case "getTopPosts":
          let sortedPosts = data.data.results.posts || [];

          if (data.data.results.scores) {
            sortedPosts = sortPostsByScores(
              sortedPosts,
              data.data.results.scores
            );
          }

          const postsEvent = new CustomEvent("topPostsReceived", {
            detail: sortedPosts,
          });
          document.dispatchEvent(postsEvent);

          if (data.data.results.scores) {
            const scoresEvent = new CustomEvent("postScoresReceived", {
              detail: data.data.results.scores,
            });
            document.dispatchEvent(scoresEvent);
          }
          break;

        default:
          console.log("Unknown action or data not in expected format");
      }
    } else {
      console.log("Data format is not as expected");
    }
  } catch (error) {
    console.error("Error parsing message as JSON:", error);
  }
}
