import { db } from '~/lib/turso'

export default defineEventHandler(async () => {
  try {
    const { rows } = await db.execute(`
      SELECT username as name, total_score as score
      FROM users
      ORDER BY total_score DESC
      LIMIT 100
    `)

    return {
      scores: rows.map((row, index) => ({
        ...row,
        rank: index + 1
      }))
    }
  } catch (error) {
    console.error('Error fetching total highscores:', error)
    throw createError({
      statusCode: 500,
      message: 'Failed to fetch highscores'
    })
  }
})
