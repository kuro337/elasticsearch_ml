interface Score {
  post_id: string;
  score: number;
}

export function generateScoresCard(scores: Score[]): string {
  let scoresList = "";

  scores.forEach((score) => {
    scoresList += `
      <div class="score-field">
        <span class="score-id">${score.post_id}</span>
        <span class="score-value">${score.score}</span>
      </div>`;
  });

  const cardHtml = `
    <div class="card score-card">
      ${scoresList}
    </div>
  `;

  return cardHtml;
}
