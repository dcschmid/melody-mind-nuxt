export const useGameScore = () => {
  const saveGameScore = async (
    category: string,
    difficulty: string,
    correctAnswers: number,
    totalQuestions: number,
    allCorrect: boolean,
    userId: string | null = null
  ) => {
    try {
      const response = await fetch('/api/game/save-score', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          category,
          difficulty,
          correctAnswers,
          totalQuestions,
          allCorrect,
          userId
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to save score')
      }

      return await response.json()
    } catch (error) {
      console.error('Error saving game score:', error)
      throw error
    }
  }

  return {
    saveGameScore,
  }
}
