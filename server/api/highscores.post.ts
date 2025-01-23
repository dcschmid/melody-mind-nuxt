import { useTurso } from '../utils/turso';

interface Highscore {
  username: string;
  points: number;
  category: string;
  difficulty: string;
  language: string;
  gold_lp: boolean;
  silver_lp: boolean;
  bronze_lp: boolean;
}

export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  const { username, points, category, difficulty, language, goldLP, silverLP, bronzeLP } = body;

  if (!username || points === undefined || !category || !difficulty || !language) {
    throw createError({
      statusCode: 400,
      message: 'Missing required fields',
    });
  }

  const db = useTurso();

  try {
    // Prüfen, ob bereits ein Eintrag existiert
    const existingScore = await db.execute({
      sql: `SELECT * FROM highscores 
            WHERE username = ? 
            AND category = ? 
            AND difficulty = ?
            AND language = ?`,
      args: [username, category, difficulty, language],
    });

    if (existingScore.rows.length > 0) {
      const row = existingScore.rows[0];
      const currentScore: Highscore = {
        username: row.username as string,
        points: row.points as number,
        category: row.category as string,
        difficulty: row.difficulty as string,
        language: row.language as string,
        gold_lp: Boolean(row.gold_lp),
        silver_lp: Boolean(row.silver_lp),
        bronze_lp: Boolean(row.bronze_lp)
      };
      
      // Only update if the new score is higher than the existing one
      const newTotalPoints = points > currentScore.points ? points : currentScore.points;
      await db.execute({
        sql: `UPDATE highscores 
              SET points = ?, 
                  gold_lp = CASE 
                    WHEN ? = true THEN true 
                    ELSE gold_lp 
                  END,
                  silver_lp = CASE 
                    WHEN ? = true THEN true 
                    ELSE silver_lp 
                  END,
                  bronze_lp = CASE 
                    WHEN ? = true THEN true 
                    ELSE bronze_lp 
                  END,
                  updated_at = CURRENT_TIMESTAMP
              WHERE username = ? AND category = ? AND difficulty = ? AND language = ?`,
        args: [newTotalPoints, goldLP, silverLP, bronzeLP, username, category, difficulty, language],
      });
      return { status: 'updated', message: 'Score updated successfully' };
    }

    // Neuen Eintrag erstellen
    await db.execute({
      sql: `INSERT INTO highscores (username, points, category, difficulty, language, gold_lp, silver_lp, bronze_lp, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)`,
      args: [username, points, category, difficulty, language, goldLP, silverLP, bronzeLP],
    });

    return { status: 'created', message: 'Score saved successfully' };
  } catch (error) {
    console.error('Error saving score:', error);
    throw createError({
      statusCode: 500,
      message: 'Failed to save score',
    });
  }
});
