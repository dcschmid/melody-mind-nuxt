/**
 * Game state management store using Pinia
 * Handles points, answers, and game progression
 */

import { defineStore } from 'pinia'

/** Represents bonus point structure for scoring */
interface BonusPoints {
  base: number // Base points earned
  time: number // Time-based bonus points
  total: number // Total points (base + time)
}

/** Main game state interface */
interface GameState {
  showSolution: boolean // Controls solution visibility
  isCorrectAnswer: boolean // Tracks if current answer is correct
  gameFinished: boolean // Indicates if game is complete
  correctAnswers: number // Count of correct answers
  totalPoints: number // Accumulated total points
  points: number // Current points
  isAnimating: boolean // Controls point animation state
  showBonus: boolean // Controls bonus points display
  latestBonus: BonusPoints // Latest bonus points earned
  maxQuestions: number // Maximum number of questions in the game
}

// Constants
const BONUS_DISPLAY_DURATION = 2000 // Duration to show bonus points (in ms)
const INITIAL_BONUS: BonusPoints = { base: 0, time: 0, total: 0 }

/**
 * Main game state store
 */
export const useGameStore = defineStore('game', {
  state: (): GameState => ({
    showSolution: false,
    isCorrectAnswer: false,
    gameFinished: false,
    correctAnswers: 0,
    totalPoints: 0,
    points: 0,
    isAnimating: false,
    showBonus: false,
    latestBonus: INITIAL_BONUS,
    maxQuestions: 10, // Default value, will be updated when initialized
  }),

  getters: {
    /**
     * Return formatted points with locale-specific formatting
     */
    formattedPoints: (state) => state.points.toLocaleString(),

    /**
     * Check if all questions were answered correctly
     */
    allQuestionsCorrect: (state) => state.correctAnswers === state.maxQuestions,

    /**
     * Calculate completion percentage
     */
    completionPercentage: (state) =>
      state.maxQuestions > 0 ? (state.correctAnswers / state.maxQuestions) * 100 : 0
  },

  actions: {
    /**
     * Initialize the game with a specific number of questions
     */
    initGame(maxQuestions: number) {
      this.maxQuestions = maxQuestions
      this.resetGameState()
    },

    /**
     * Updates points and handles bonus point animation
     * @param basePoints - Base points to award
     * @param timeBonus - Time-based bonus points
     */
    updatePoints(basePoints: number, timeBonus: number) {
      const total = basePoints + timeBonus

      this.latestBonus = { base: basePoints, time: timeBonus, total }
      this.showBonus = true
      this.isAnimating = true
      this.points += total
      this.totalPoints = this.points

      // Schedule hiding the bonus display
      setTimeout(() => {
        this.showBonus = false
        this.isAnimating = false
      }, BONUS_DISPLAY_DURATION)
    },

    /**
     * Increments the correct answers counter
     */
    incrementCorrectAnswers() {
      this.correctAnswers++
    },

    /**
     * Sets the answer state and updates correct answers if needed
     * @param isCorrect - Whether the answer was correct
     */
    setAnswer(isCorrect: boolean) {
      this.isCorrectAnswer = isCorrect
      this.showSolution = true
      if (isCorrect) {
        this.incrementCorrectAnswers()
      }
    },

    /**
     * Marks the game as finished
     */
    finishGame() {
      this.gameFinished = true
    },

    /**
     * Resets the game state to initial values
     */
    resetGameState() {
      this.showSolution = false
      this.isCorrectAnswer = false
      this.gameFinished = false
      this.correctAnswers = 0
      this.totalPoints = 0
      this.points = 0
      this.isAnimating = false
      this.showBonus = false
      this.latestBonus = { ...INITIAL_BONUS }
    },

    /**
     * Prepares the state for the next question
     */
    prepareNextQuestion() {
      this.showSolution = false
      this.isCorrectAnswer = false
      this.showBonus = false
      this.isAnimating = false
    }
  }
})
