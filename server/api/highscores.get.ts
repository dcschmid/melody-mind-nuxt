import { useTurso } from '../utils/turso'

export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const language: string = (query.language as string) || 'de'
  const db = useTurso()

  try {
    const sql = `
      WITH RankedScores AS (
        SELECT
          id,
          username,
          points,
          category,
          difficulty,
          language,
          gold_lp,
          silver_lp,
          bronze_lp,
          ROW_NUMBER() OVER (
            PARTITION BY category, difficulty
            ORDER BY points DESC
          ) as rank
        FROM highscores
        WHERE language = ?
      )
      SELECT *
      FROM RankedScores
      WHERE rank <= 10
      ORDER BY category ASC, difficulty ASC, points DESC
    `

     const result = await db.execute({
      sql,
      args: [language]
    })

    const rows = result.rows || []

    return rows.map(row => ({
      id: row.id,
      username: row.username,
      points: row.points,
      category: row.category,
      difficulty: row.difficulty,
      language: row.language,
      goldLp: row.gold_lp === 1,
      silverLp: row.silver_lp === 1,
      bronzeLp: row.bronze_lp === 1,
      rank: row.rank
    }))
  } catch (error) {
    throw createError({
      statusCode: 500,
      message: 'Failed to fetch highscores',
      cause: error
    })
  }
})
