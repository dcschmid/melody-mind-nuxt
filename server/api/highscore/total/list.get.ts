import { useTurso } from "~/lib/turso";

export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const language = query.language as string;
  const client = useTurso();

  try {
    // Hole alle Scores für die Berechnung des User-Ranks
    const { rows: allScores } = await client.execute({
      sql: `
        SELECT th.*, u.name, u.total_user_points as score
        FROM user u
        LEFT JOIN total_highscore th ON th.user_id = u.id
        WHERE th.language = ?
        ORDER BY u.total_user_points DESC
      `,
      args: [language],
    });

    // Hole nur die Top 10 für die Anzeige
    const { rows: scores } = await client.execute({
      sql: `
        SELECT th.*, u.name, u.total_user_points as score
        FROM user u
        LEFT JOIN total_highscore th ON th.user_id = u.id
        WHERE th.language = ?
        ORDER BY u.total_user_points DESC
        LIMIT 10
      `,
      args: [language],
    });

    return { scores, allScores };
  } catch (error) {
    console.error("Database error:", error);
    throw createError({
      statusCode: 500,
      message: "Error fetching highscores",
    });
  }
});
