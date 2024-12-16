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
          email,
          image,
          total_user_points,
          won_lps
        FROM user
        WHERE id = ?
      `,
      args: [userId],
    });

    const userData = rows[0];
    console.log("Geladene Benutzerdaten:", userData); // Debug-Log

    return {
      name: userData.name,
      username: userData.username,
      email: userData.email,
      image: userData.image,
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
