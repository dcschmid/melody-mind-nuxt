import { useTurso } from '../utils/turso'

export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const language: string = (query.language as string) || 'de'

  const db = useTurso()

  try {
    const result = await db.execute({
      sql: `
        WITH RankedScores AS (
          SELECT *,
                 ROW_NUMBER() OVER (PARTITION BY category ORDER BY points DESC) as rank
          FROM highscores
          WHERE language = ?
        )
        SELECT * FROM RankedScores
        WHERE rank <= 10
        ORDER BY category ASC, points DESC
      `,
      args: [language]
    })


    return result.rows || []
  } catch (error) {
    throw createError({
      statusCode: 500,
      message: 'Failed to fetch highscores',
    })
  }
})
