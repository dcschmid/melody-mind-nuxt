// server/api/highscore/total.post.ts

import { useTurso } from "../../../lib/turso";
import { nanoid } from "nanoid";

export default defineEventHandler(async (event) => {
  const { userId, score, language } = await readBody(event);
  const client = useTurso();

  try {
    // Validiere den Score
    const numericScore = Number(score);
    if (!Number.isFinite(numericScore)) {
      throw createError({
        statusCode: 400,
        message: "Invalid score value",
      });
    }

    const {
      rows: [existingScore],
    } = await client.execute({
      sql: "SELECT score FROM total_highscore WHERE user_id = ? AND language = ?",
      args: [userId, language],
    });

    // Validiere den existierenden Score und berechne die Summe
    const existingScoreNum = existingScore?.score ? Number(existingScore.score) : 0;
    if (!Number.isFinite(existingScoreNum)) {
      throw createError({
        statusCode: 500,
        message: "Invalid existing score in database",
      });
    }

    const totalScore = existingScoreNum + numericScore;

    if (existingScore) {
      await client.execute({
        sql: "UPDATE total_highscore SET score = ? WHERE user_id = ? AND language = ?",
        args: [totalScore, userId, language],
      });
    } else {
      await client.execute({
        sql: "INSERT INTO total_highscore (id, user_id, score, language) VALUES (?, ?, ?, ?)",
        args: [nanoid(), userId, numericScore, language],
      });
    }

    return { success: true };
  } catch (error: any) {
    console.error("Database error:", error);
    throw createError({
      statusCode: error.statusCode || 500,
      message: error.message || "Database error",
    });
  }
});
