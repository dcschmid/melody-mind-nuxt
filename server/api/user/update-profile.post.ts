import { defineEventHandler, readBody } from "h3";
import { useTurso } from "~/lib/turso";

export default defineEventHandler(async (event) => {
  try {
    const { userId, name, username, email } = await readBody(event);
    const db = useTurso();

    if (!userId) {
      throw createError({
        statusCode: 400,
        message: "UserId ist erforderlich",
      });
    }

    await db.execute({
      sql: `UPDATE user
                  SET name = ?, username = ?, email = ?
                  WHERE id = ?`,
      args: [name || "", username || "", email || "", userId.toString()],
    });

    return {
      id: userId,
      name,
      username,
      email,
    };
  } catch (error) {
    console.error("Fehler beim Aktualisieren des Profils:", error);
    throw createError({
      statusCode: 500,
      message: "Fehler beim Aktualisieren des Profils",
    });
  }
});
