import { computed, type Ref } from 'vue'

/**
 * Configuration interface for game rewards
 */
interface GameRewardsConfig {
  /** Flag indicating if all questions were answered correctly */
  allQuestionsCorrect: Ref<boolean>
  /** Number of correctly answered questions */
  correctAnswers: Ref<number>
  /** Total number of questions in the game */
  maxQuestions: Ref<number>
  /** Optional threshold values for different achievement levels */
  thresholds?: {
    /** Threshold for gold achievement (default: 1.0 = 100%) */
    readonly gold: number
    /** Threshold for silver achievement (default: 0.75 = 75%) */
    readonly silver: number
    /** Threshold for bronze achievement (default: 0.5 = 50%) */
    readonly bronze: number
  }
}

// Define constants outside the function for better performance and type safety
/**
 * Mapping of achievement levels to their corresponding icon names
 */
const ICONS = {
  GOLD: 'material-symbols:album-gold',
  SILVER: 'material-symbols:album-silver',
  BRONZE: 'material-symbols:album-bronze',
} as const

/**
 * Mapping of achievement levels to their corresponding CSS classes
 */
const CLASSES = {
  GOLD: 'gold',
  SILVER: 'silver',
  BRONZE: 'bronze',
} as const

/**
 * Composable for managing game rewards and achievements
 *
 * @param config - Configuration object containing game state and thresholds
 * @returns Object containing computed properties for reward icons and classes
 *
 * @example
 * ```ts
 * const { recordIcon, recordClass } = useGameRewards({
 *   allQuestionsCorrect: ref(true),
 *   correctAnswers: ref(10),
 *   maxQuestions: ref(10)
 * })
 * ```
 */
export const useGameRewards = ({
  allQuestionsCorrect,
  correctAnswers,
  maxQuestions,
  thresholds = {
    gold: 1,
    silver: 0.75,
    bronze: 0.5,
  },
}: GameRewardsConfig) => {
  /**
   * Computes the achievement level based on game performance
   * Caches the calculation to avoid redundant computations
   */
  const getAchievementLevel = computed(() => {
    const ratio = correctAnswers.value / maxQuestions.value

    if (allQuestionsCorrect.value) return 'GOLD'
    if (ratio >= thresholds.silver) return 'SILVER'
    if (ratio >= thresholds.bronze) return 'BRONZE'
    return ''
  })

  /**
   * Returns the appropriate icon name for the current achievement level
   */
  const recordIcon = computed(() => ICONS[getAchievementLevel.value as keyof typeof ICONS] || '')

  /**
   * Returns the appropriate CSS class for the current achievement level
   */
  const recordClass = computed(() => CLASSES[getAchievementLevel.value as keyof typeof CLASSES] || '')

  return {
    recordIcon,
    recordClass,
  }
}
