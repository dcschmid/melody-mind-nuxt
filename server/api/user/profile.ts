import { useTurso } from "~/lib/turso";

export default defineEventHandler(async (event) => {
  const { userId } = await readBody(event);
  const client = useTurso();

  try {
    const { rows } = await client.execute({
      sql: `
        SELECT
          name,
          username,
          total_user_points,
          won_lps
        FROM user
        WHERE id = ?
      `,
      args: [userId],
    });

    const userData = rows[0];

    return {
      name: userData.name,
      username: userData.username,
      totalPoints: Number(userData.total_user_points),
      wonLPs: typeof userData.won_lps === "string" ? JSON.parse(userData.won_lps) : [],
    };
  } catch (error) {
    console.error("Database error:", error);
    throw createError({
      statusCode: 500,
      message: String(error),
    });
  }
});
