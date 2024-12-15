import { useTurso } from "~/lib/turso";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const language = query.language as string;
  const client = useTurso();

  try {
    // Hole alle einzigartigen Kategorien aus der highscore_per_category Tabelle
    const { rows: categories } = await client.execute({
      sql: `
        SELECT DISTINCT category as slug
        FROM highscore_per_category
        WHERE language = ?
        ORDER BY category ASC
      `,
      args: [language],
    });

    // Get category data using fs
    const __dirname = dirname(fileURLToPath(import.meta.url));
    const categoriesPath = join(__dirname, `../../json/${language}_categories.json`);
    const categoriesData = JSON.parse(readFileSync(categoriesPath, "utf-8"));

    // Ergänze die Namen der Kategorien
    const categoriesWithNames = categories.map(cat => ({
      ...cat,
      name: categoriesData.find((c: any) => c.slug === cat.slug)?.headline || cat.slug
    }));

    return {
      categories: categoriesWithNames,
    };
  } catch (error) {
    console.error("Database error:", error);
    throw createError({
      statusCode: 500,
      message: "Error fetching categories",
    });
  }
});
