// server/api/highscore/total.post.ts

import { useTurso } from "~/lib/turso";
import { nanoid } from "nanoid";

export default defineEventHandler(async (event) => {
  const { userId, points, language } = await readBody(event);
  const client = useTurso();

  try {
    const { rows: [existingScore] } = await client.execute({
      sql: "SELECT score FROM total_highscore WHERE user_id = ? AND language = ?",
      args: [userId, language],
    });

    if (!existingScore?.score || existingScore.score < points) {
      if (existingScore) {
        await client.execute({
          sql: "UPDATE total_highscore SET score = ? WHERE user_id = ? AND language = ?",
          args: [points, userId, language],
        });
      } else {
        await client.execute({
          sql: `INSERT INTO total_highscore
                (id, user_id, score, language)
                VALUES (?, ?, ?, ?)`,
          args: [nanoid(), userId, points, language],
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
