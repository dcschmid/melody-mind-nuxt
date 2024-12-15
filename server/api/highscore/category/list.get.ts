import { useTurso } from "~/lib/turso";

export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const category = query.category as string;
  const language = query.language as string;
  const client = useTurso();

  try {
    // Hole alle Scores für die Berechnung des User-Ranks
    const { rows: allScores } = await client.execute({
      sql: `
        SELECT hpc.*, u.name
        FROM highscore_per_category hpc
        JOIN user u ON hpc.user_id = u.id
        WHERE hpc.category = ?
        AND hpc.language = ?
        ORDER BY hpc.score DESC
      `,
      args: [category, language],
    });

    // Hole nur die Top 10 für die Anzeige
    const { rows: scores } = await client.execute({
      sql: `
        SELECT hpc.*, u.name
        FROM highscore_per_category hpc
        JOIN user u ON hpc.user_id = u.id
        WHERE hpc.category = ?
        AND hpc.language = ?
        ORDER BY hpc.score DESC
        LIMIT 10
      `,
      args: [category, language],
    });

    return { scores, allScores };
  } catch (error) {
    console.error("Database error:", error);
    throw createError({
      statusCode: 500,
      message: "Error fetching category highscores",
    });
  }
});
