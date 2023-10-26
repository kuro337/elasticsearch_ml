import { User } from "../entity/models/user";

export function generateUserCard(user: User): string {
  console.log("Received User: ", user);

  const cardStyles = `
  border: 1px solid #555;
  padding: 15px;
  margin: 10px;
  background-color: #222;
  font-family: "Lato", sans-serif;
  color: #fff;
  display: flex;
  flex-direction: column;
`;

  const fieldStyles = `
  margin-bottom: 10px;
  display: flex;
`;

  const keyStyles = `
  width: 100px;
`;

  const cardHtml = `
<div style="${cardStyles}">
  <div style="${fieldStyles}"><span style="${keyStyles}">Username:</span> ${user.username}</div>
  <div style="${fieldStyles}"><span style="${keyStyles}">Name:</span> ${user.first_name} ${user.last_name}</div>
  <div style="${fieldStyles}"><span style="${keyStyles}">Email:</span> ${user.email}</div>
  <div style="${fieldStyles}"><span style="${keyStyles}">Gender:</span> ${user.gender}</div>
  <div style="${fieldStyles}"><span style="${keyStyles}">Country:</span> ${user.country}</div>
  <div style="${fieldStyles}"><span style="${keyStyles}">Age:</span> ${user.age}</div>
</div>
`;

  return cardHtml;
}
