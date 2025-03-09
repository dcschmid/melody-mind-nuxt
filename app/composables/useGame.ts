/**
 * Game composable that combines Pinia stores
 * Provides a unified API for game functionality
 */

import { storeToRefs } from 'pinia'
import { useGameStore } from '../stores/gameStore'
import { useQuestionsStore } from '../stores/questionsStore'
import { useApiClient } from './useApiClient'

export const useGame = () => {
  // Initialize stores
  const gameStore = useGameStore()
  const questionsStore = useQuestionsStore()
  const { saveHighscore } = useApiClient()

  // Extract reactive state with storeToRefs
  const {
    showSolution,
    isCorrectAnswer,
    gameFinished,
    totalPoints,
    points,
    formattedPoints,
    isAnimating,
    showBonus,
    latestBonus,
    allQuestionsCorrect,
    completionPercentage,
    correctAnswers, // Hinzufügen von correctAnswers aus dem Store
  } = storeToRefs(gameStore)

  const { currentQuestion, currentOptions, maxQuestions } = storeToRefs(questionsStore)

  /**
   * Initialize a new game
   */
  const startGame = async (category: string, difficulty: string) => {
    // Reset game state
    gameStore.resetGameState()

    // Initialize question store
    questionsStore.init(category, difficulty)

    // Initialize game store with the correct number of questions
    gameStore.initGame(questionsStore.maxQuestions)

    // Load questions
    await questionsStore.loadQuestions()
  }

  /**
   * Check an answer and update game state
   */
  const checkAnswer = (selectedAnswer: string) => {
    const isCorrect = currentQuestion.value?.correctAnswer === selectedAnswer

    // Update game state
    gameStore.setAnswer(isCorrect)

    // Calculate points if answer is correct
    if (isCorrect) {
      const basePoints = 100
      const timeBonus = 50 // This could be calculated based on elapsed time
      gameStore.updatePoints(basePoints, timeBonus)
    }

    return isCorrect
  }

  /**
   * Move to the next question
   */
  const nextQuestion = async () => {
    // Check if the game is finished
    if (gameStore.correctAnswers >= questionsStore.maxQuestions) {
      gameStore.finishGame()
      return true
    }

    // Prepare for next question
    gameStore.prepareNextQuestion()
    await questionsStore.selectRandomQuestion()

    return false
  }

  /**
   * End the game and save the score
   */
  const endGame = async (category: string, language: string, difficulty: string) => {
    // Mark game as finished
    gameStore.finishGame()

    // Determine reward based on completion percentage
    let reward: 'gold' | 'silver' | 'bronze' | 'none' = 'none'

    if (completionPercentage.value >= 90) {
      reward = 'gold'
    } else if (completionPercentage.value >= 70) {
      reward = 'silver'
    } else if (completionPercentage.value >= 50) {
      reward = 'bronze'
    }

    // Save score to API
    const { error } = await saveHighscore({
      points: points.value,
      category,
      difficulty,
      language,
      goldLP: reward === 'gold',
      silverLP: reward === 'silver',
      bronzeLP: reward === 'bronze',
    })

    if (error) {
      console.error('Failed to save score:', error)
    }

    return { success: !error, reward }
  }

  /**
   * Clean up resources
   */
  const cleanupGame = () => {
    questionsStore.clearStore()
  }

  return {
    // State references
    showSolution,
    isCorrectAnswer,
    gameFinished,
    totalPoints,
    points,
    formattedPoints,
    isAnimating,
    showBonus,
    latestBonus,
    currentQuestion,
    currentOptions,
    maxQuestions,
    allQuestionsCorrect,
    completionPercentage,
    correctAnswers,

    // Actions
    startGame,
    checkAnswer,
    nextQuestion,
    endGame,
    cleanupGame,
  }
}
