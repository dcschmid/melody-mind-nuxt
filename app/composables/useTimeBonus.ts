import { ref, computed } from 'vue'

/**
 * Time Bonus Composable
 * Manages a time-based bonus point system for quiz/game questions.
 *
 * @param options Configuration object with the following properties:
 * @param {number} options.basePoints - Base points awarded for answering (default: 50)
 * @param {number} options.maxTimeBonus - Maximum possible time bonus points (default: 100)
 * @param {number} options.timeLimit - Time limit in milliseconds (default: 30000)
 *
 * @returns {Object} An object containing the following methods:
 *   - startTimer: Starts the timer for the current question
 *   - calculateBonus: Calculates the total points including time bonus
 */
export const useTimeBonus = (
  options = {
    basePoints: 50,
    maxTimeBonus: 100,
    timeLimit: 30000,
  }
) => {
  // Store option values in constants for better performance
  const TIME_LIMIT = options.timeLimit
  const BASE_POINTS = options.basePoints
  const MAX_BONUS = options.maxTimeBonus

  /**
   * Stores the timestamp when the question timer started
   * @type {Ref<number>}
   */
  const questionStartTime = ref(0)

  /**
   * Computed property that calculates the elapsed time since the question started
   * Returns 0 if the timer hasn't been started yet
   */
  const timeElapsed = computed(() =>
    questionStartTime.value ? Date.now() - questionStartTime.value : 0
  )

  /**
   * Starts the timer by setting the current timestamp
   */
  const startTimer = () => {
    questionStartTime.value = Date.now()
  }

  /**
   * Calculates the bonus points based on elapsed time
   * @returns {Object} Object containing:
   *   - base: Base points for the question
   *   - time: Additional points from time bonus
   *   - total: Sum of base points and time bonus
   */
  const calculateBonus = () => {
    const timePercentage = Math.max(0, 1 - timeElapsed.value / TIME_LIMIT)
    const timeBonus = Math.floor(timePercentage * MAX_BONUS)
    return {
      base: BASE_POINTS,
      time: timeBonus,
      total: BASE_POINTS + timeBonus,
    }
  }

  return {
    startTimer,
    calculateBonus,
  }
}
