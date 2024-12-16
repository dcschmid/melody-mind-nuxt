import { useTurso } from "~/lib/turso";

/**
 * API endpoint to fetch total highscores
 * Returns both top 10 scores and all scores for user ranking
 * @route GET /api/highscore/total/list
 * @param {string} language - The language filter for highscores
 * @returns {Object} Object containing scores and allScores arrays
 */
export default defineEventHandler(async (event) => {
  const { language } = getQuery(event) as { language: string };
  const client = useTurso();

  try {
    // Combined query for both datasets using UNION ALL for better performance
    const { rows } = await client.execute({
      sql: `
        WITH RankedScores AS (
          SELECT
            th.*,
            u.name,
            u.image as avatar_url,
            u.total_user_points as score,
            ROW_NUMBER() OVER (ORDER BY u.total_user_points DESC) as rank
          FROM user u
          LEFT JOIN total_highscore th ON th.user_id = u.id
          WHERE th.language = ?
        )
        SELECT * FROM RankedScores WHERE rank <= 10
        UNION ALL
        SELECT * FROM RankedScores WHERE rank > 10
        ORDER BY rank ASC
      `,
      args: [language],
    });

    // Split results into top 10 scores and all scores
    const scores = rows.slice(0, 10);
    const allScores = rows;

    return {
      scores,      // Top 10 scores for display
      allScores,   // All scores for user ranking calculation
      cached: false // Flag for future caching implementation
    };
  } catch (error) {
    console.error("Database error:", error);
    throw createError({
      statusCode: 500,
      message: "Error fetching highscores",
      cause: error
    });
  } finally {
     try {
      await client.close();
    } catch (error) {
      console.error("Fehler beim Schließen der Datenbankverbindung:", error);
    }  }
});
