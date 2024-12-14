// server/api/user/update-score.post.ts

import { useTurso } from "~/lib/turso";

interface LP {
  genre: string;
  language: string;
  type: 'gold' | 'silver' | 'bronze';
  earnedAt: string;
}

export default defineEventHandler(async (event) => {
  const { userId, pointsToAdd, newLP, category, language } = await readBody(event);
  const client = useTurso();

  try {
    // Get category data
    const categories = await import(`~/json/${language}_categories.json`)
    const genreName = categories.default.find((cat: any) => cat.slug === category)?.name || category

    const { rows: [user] } = await client.execute({
      sql: 'SELECT won_lps, total_user_points FROM user WHERE id = ?',
      args: [userId]
    })

    // Parse existing LPs or initialize empty array
    const currentLPs: LP[] = user?.won_lps ? JSON.parse(user.won_lps as string) : []
    const currentPoints = Number(user?.total_user_points || 0)
    const newTotalPoints = currentPoints + pointsToAdd

    if (newLP) {
      // Add new LP with metadata
      currentLPs.push({
        genre: genreName,
        language,
        type: newLP,
        earnedAt: new Date().toISOString()
      })
    }

    await client.execute({
      sql: `UPDATE user
            SET total_user_points = ?,
                won_lps = ?
            WHERE id = ?`,
      args: [newTotalPoints, JSON.stringify(currentLPs), userId]
    })

    return { success: true }

  } catch (error: any) {
    console.error('Database error:', error)
    throw createError({
      statusCode: 500,
      message: `Database error: ${error.message}`
    })
  }
});
