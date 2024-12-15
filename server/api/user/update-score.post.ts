import { useTurso } from "../../../lib/turso";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

interface LP {
  genre: string;
  language: string;
  type: "gold" | "silver" | "bronze";
  earnedAt: string;
}

export default defineEventHandler(async (event) => {
  const { userId, pointsToAdd, newLP, category, language } = await readBody(event);
  const client = useTurso();

  try {
    // Get category data using fs
    const __dirname = dirname(fileURLToPath(import.meta.url));
    const categoriesPath = join(__dirname, `../../json/${language}_categories.json`);
    const categoriesData = JSON.parse(readFileSync(categoriesPath, "utf-8"));
    const genreName = categoriesData.find((cat: any) => cat.slug === category)?.name || category;

    const {
      rows: [user],
    } = await client.execute({
      sql: "SELECT won_lps, total_user_points FROM user WHERE id = ?",
      args: [userId],
    });

    if (!user) {
      throw createError({
        statusCode: 404,
        message: "User not found",
      });
    }

    // Parse existing LPs or initialize empty array
    let currentLPs: LP[] = [];
    try {
      currentLPs = user.won_lps ? JSON.parse(user.won_lps as string) : [];
      // Stelle sicher, dass es ein Array ist
      if (!Array.isArray(currentLPs)) {
        currentLPs = [];
      }
    } catch (e) {
      console.error("Error parsing won_lps:", e);
      currentLPs = [];
    }

    // Validiere pointsToAdd
    const numericPointsToAdd = Number(pointsToAdd);
    if (!Number.isFinite(numericPointsToAdd)) {
      throw createError({
        statusCode: 400,
        message: "Invalid points value",
      });
    }

    const currentPoints = Number(user?.total_user_points || 0);
    const newTotalPoints = currentPoints + numericPointsToAdd;

    if (newLP) {
      // Add new LP with metadata
      currentLPs.push({
        genre: genreName,
        language,
        type: newLP,
        earnedAt: new Date().toISOString(),
      });
    }

    await client.execute({
      sql: `UPDATE user
            SET total_user_points = ?,
                won_lps = ?
            WHERE id = ?`,
      args: [newTotalPoints, JSON.stringify(currentLPs), userId],
    });

    return { success: true };
  } catch (error: any) {
    console.error("Database error:", error);
    throw createError({
      statusCode: error.statusCode || 500,
      message: error.message || "Database error",
    });
  }
});
