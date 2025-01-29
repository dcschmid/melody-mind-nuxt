export const useGameScore = () => {
  const saveGameScore = async (
    category: string,
    points: number,
    reward: "gold" | "silver" | "bronze" | "none",
    language: string,
    difficulty: string,
  ) => {
    try {
      const response = await fetch('/api/highscores', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          points,
          category,
          difficulty,
          language,
          goldLP: reward === 'gold',
          silverLP: reward === 'silver',
          bronzeLP: reward === 'bronze'
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
