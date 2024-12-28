import { useTurso } from '../utils/turso'

export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const language: string = (query.language as string) || 'de'

  console.log('API: Received request with query:', query)
  console.log('API: Using language:', language)

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

    console.log('API: Executing SQL query:', sql.trim())
    console.log('API: Query parameters:', [language])

    const result = await db.execute({
      sql,
      args: [language]
    })

    const rows = result.rows || []
    
    console.log('API: Query results:', {
      totalRows: rows.length,
      categories: [...new Set(rows.map(row => row.category))],
      difficulties: [...new Set(rows.map(row => row.difficulty))],
      firstRow: rows[0],
      lastRow: rows[rows.length - 1]
    })

    return rows.map(row => ({
      id: row.id,
      username: row.username,
      points: row.points,
      category: row.category,
      difficulty: row.difficulty,
      language: row.language,
      gold_lp: row.gold_lp,
      silver_lp: row.silver_lp,
      bronze_lp: row.bronze_lp,
      rank: row.rank
    }))
  } catch (error) {
    console.error('API: Database error:', error)
    throw createError({
      statusCode: 500,
      message: 'Failed to fetch highscores',
      cause: error
    })
  }
})
