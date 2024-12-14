// server/api/highscore/category.post.ts

import { useTurso } from "~/lib/turso";
import { nanoid } from "nanoid";

export default defineEventHandler(async (event) => {
  const { userId, category, points, language } = await readBody(event);
  const client = useTurso();

  try {
    // Check if a better score exists
    const { rows: [existingScore] } = await client.execute({
      sql: `SELECT score
            FROM highscore_per_category
            WHERE user_id = ? AND category = ? AND language = ?`,
      args: [userId, category, language],
    });

    if (!existingScore?.score || existingScore.score < points) {
      // Update if exists, insert if not
      if (existingScore) {
        await client.execute({
          sql: `UPDATE highscore_per_category
                SET score = ?
                WHERE user_id = ? AND category = ? AND language = ?`,
          args: [points, userId, category, language],
        });
      } else {
        await client.execute({
          sql: `INSERT INTO highscore_per_category
                (id, user_id, category, score, language)
                VALUES (?, ?, ?, ?, ?)`,
          args: [nanoid(), userId, category, points, language],
        });
      }
    }

    return { success: true };
  } catch (error) {
    console.error("Database error:", error);
    throw createError({
      statusCode: 500,
      message: "Internal server error",
    });
  }
});
