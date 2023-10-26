import { Post } from "../entity/models/post";
export function generatePostCard(post: Post): string {
  const cardStyles = `
    border: 1px solid #555;
    padding: 15px;
    margin: 10px;
    background-color: #111;
    font-family: "Lato", sans-serif;
    font-size: 0.75rem;
    color: #ddd;
    display: flex;
    flex-direction: column;
  `;

  const fieldStyles = `
    margin-bottom: 10px;
    display: flex;
  `;

  const keyStyles = `
    width: 120px;
  `;

  const cardHtml = `
    <div style="${cardStyles}">
      <div style="${fieldStyles}"><span style="${keyStyles}">Post:</span> ${post.post_id}</div>
      <div style="${fieldStyles}"><span style="${keyStyles}">Lang:</span> ${post.lang}</div>
      <div style="${fieldStyles}"><span style="${keyStyles}">Title:</span> ${post.title}</div>
      <div style="${fieldStyles}"><span style="${keyStyles}">Short Title:</span> ${post.short_title}</div>
      <div style="${fieldStyles}"><span style="${keyStyles}">Description:</span> ${post.description}</div>
      <div style="${fieldStyles}"><span style="${keyStyles}">Author:</span> ${post.author}</div>
      <div style="${fieldStyles}"><span style="${keyStyles}">Tags:</span> ${post.tags}</div>
    </div>
  `;

  return cardHtml;
}
