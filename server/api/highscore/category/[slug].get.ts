import { db } from '~/lib/turso'

export default defineEventHandler(async (event) => {
  const slug = getRouterParam(event, 'slug')

  if (!['pop', 'rock', 'rap', 'klassik'].includes(slug)) {
    throw createError({
      statusCode: 400,
      message: 'Invalid category'
    })
  }

  try {
    const { rows } = await db.execute({
      sql: `
        SELECT username as name, category_score as score
        FROM user_category_scores
        JOIN users ON user_category_scores.user_id = users.id
        WHERE category = ?
        ORDER BY category_score DESC
        LIMIT 100
      `,
      args: [slug]
    })

    return {
      scores: rows.map((row, index) => ({
        ...row,
        rank: index + 1
      }))
    }
  } catch (error) {
    console.error(`Error fetching highscores for category ${slug}:`, error)
    throw createError({
      statusCode: 500,
      message: 'Failed to fetch category highscores'
    })
  }
})
