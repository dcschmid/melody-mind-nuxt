import { useTurso } from "~/lib/turso";

/**
 * API endpoint to fetch category-specific highscores
 * Returns both top 10 scores and all scores for user ranking within a category
 * @route GET /api/highscore/category/list
 * @param {string} category - The category identifier
 * @param {string} language - The language filter for highscores
 * @returns {Object} Object containing scores and allScores arrays
 */
export default defineEventHandler(async (event) => {
  const { category, language } = getQuery(event) as { category: string; language: string };
  const client = useTurso();

  try {
    // Combined query for both datasets using UNION ALL for better performance
    const { rows } = await client.execute({
      sql: `
        WITH RankedScores AS (
          SELECT
            hpc.*,
            u.name,
            u.image as avatar_url,
            ROW_NUMBER() OVER (ORDER BY hpc.score DESC) as rank
          FROM highscore_per_category hpc
          JOIN user u ON hpc.user_id = u.id
          WHERE hpc.category = ?
          AND hpc.language = ?
        )
        SELECT * FROM RankedScores WHERE rank <= 10
        UNION ALL
        SELECT * FROM RankedScores WHERE rank > 10
        ORDER BY rank ASC
      `,
      args: [category, language],
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
      message: "Error fetching category highscores",
      cause: error
    });
  } finally {
    try {
      await client.close();
    } catch (error) {
      console.error("Fehler beim Schließen der Datenbankverbindung:", error);
    }
  }
});
