/**
 * Game state management composable
 * Handles points, answers, and game progression
 */

import { ref, computed, toRefs } from 'vue'

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
}

// Constants
const BONUS_DISPLAY_DURATION = 2000 // Duration to show bonus points (in ms)
const INITIAL_BONUS: BonusPoints = Object.freeze({ base: 0, time: 0, total: 0 })
const INITIAL_STATE: GameState = Object.freeze({
  showSolution: false,
  isCorrectAnswer: false,
  gameFinished: false,
  correctAnswers: 0,
  totalPoints: 0,
  points: 0,
  isAnimating: false,
  showBonus: false,
  latestBonus: INITIAL_BONUS,
})

/**
 * Main game state composable
 * @param maxQuestions - Maximum number of questions in the game
 */
export function useGameState(maxQuestions: number) {
  // Timer reference for cleanup
  let bonusTimer: NodeJS.Timeout | null = null

  // Initialize reactive game state
  const state = ref<GameState>(structuredClone(INITIAL_STATE))

  // Computed properties
  const formattedPoints = computed(() => state.value.points.toLocaleString())
  const allQuestionsCorrect = computed(() => state.value.correctAnswers === maxQuestions)

  /**
   * Updates points and handles bonus point animation
   * @param basePoints - Base points to award
   * @param timeBonus - Time-based bonus points
   */
  const updatePoints = (basePoints: number, timeBonus: number) => {
    if (bonusTimer) {
      clearTimeout(bonusTimer)
    }

    const total = basePoints + timeBonus

    const updates = {
      latestBonus: { base: basePoints, time: timeBonus, total },
      showBonus: true,
      isAnimating: true,
      points: state.value.points + total,
    }
    Object.assign(state.value, updates)
    state.value.totalPoints = state.value.points

    bonusTimer = setTimeout(() => {
      state.value.showBonus = false
      state.value.isAnimating = false
    }, BONUS_DISPLAY_DURATION)
  }

  /**
   * Increments the correct answers counter
   */
  const incrementCorrectAnswers = () => {
    state.value.correctAnswers++
  }

  /**
   * Sets the answer state and updates correct answers if needed
   * @param isCorrect - Whether the answer was correct
   */
  const setAnswer = (isCorrect: boolean) => {
    state.value.isCorrectAnswer = isCorrect
    state.value.showSolution = true
    if (isCorrect) {
      incrementCorrectAnswers()
    }
  }

  /**
   * Marks the game as finished
   */
  const finishGame = () => {
    state.value.gameFinished = true
  }

  /**
   * Resets the game state to initial values
   */
  const resetGameState = () => {
    cleanup()
    state.value = structuredClone(INITIAL_STATE)
  }

  /**
   * Cleans up timers and resources
   * Should be called on component unmount
   */
  const cleanup = () => {
    if (bonusTimer) {
      clearTimeout(bonusTimer)
    }
  }

  /**
   * Bereitet den State für die nächste Frage vor
   */
  const prepareNextQuestion = () => {
    state.value.showSolution = false
    state.value.isCorrectAnswer = false
    state.value.showBonus = false
    state.value.isAnimating = false

    if (bonusTimer) {
      clearTimeout(bonusTimer)
      bonusTimer = null
    }
  }

  return {
    // Reactive state properties
    ...toRefs(state.value),

    // Computed properties
    formattedPoints,
    allQuestionsCorrect,

    // Methods
    updatePoints,
    setAnswer,
    finishGame,
    resetGameState,
    incrementCorrectAnswers,
    cleanup,
    prepareNextQuestion,
  }
}
