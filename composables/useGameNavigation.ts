import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useThrottleFn } from '@vueuse/core'

/**
 * Interface for the game navigation options
 * @interface GameNavigationOptions
 * @property {Ref<any[]>} usedQuestions - Array of questions that have been used
 * @property {Ref<number>} maxQuestions - Maximum number of questions in the game
 * @property {Ref<boolean>} gameFinished - Flag indicating if the game is finished
 * @property {Ref<boolean>} showSolution - Flag indicating if the solution should be shown
 * @property {Function} [onReset] - Optional callback function to reset game state
 * @property {Function} [onNextQuestion] - Optional callback function to load next question
 */
interface GameNavigationOptions {
  usedQuestions: Ref<any[]>
  maxQuestions: Ref<number>
  gameFinished: Ref<boolean>
  showSolution: Ref<boolean>
  onReset?: () => void
  onNextQuestion?: () => void
}

/**
 * Composable for handling game navigation and scroll behavior
 * @param {GameNavigationOptions} options - Configuration options for game navigation
 * @returns {Object} Navigation utilities and state
 */
export function useGameNavigation(options: GameNavigationOptions) {
  const {
    usedQuestions,
    maxQuestions,
    gameFinished,
    showSolution,
    onReset,
    onNextQuestion
  } = options

  // Cache for media query result to avoid repeated DOM access
  let mediaQueryList: MediaQueryList | null = null
  const prefersReducedMotion = ref(false)

  // Cache for last scroll position to optimize animations
  const lastScrollPosition = ref(0)

  /**
   * Computed property that determines scroll behavior based on user preferences
   * Returns 'auto' if user prefers reduced motion, otherwise 'smooth'
   */
  const smoothScrollBehavior = computed(() =>
    prefersReducedMotion.value ? 'auto' : 'smooth'
  )

  /**
   * Throttled function to scroll to top of page
   * Uses requestAnimationFrame for smooth performance
   * @param {number} offset - Optional offset from top (default: 0)
   */
  const scrollToTop = useThrottleFn((offset = 0) => {
    lastScrollPosition.value = window.scrollY

    requestAnimationFrame(() => {
      window.scrollTo({
        top: offset,
        behavior: smoothScrollBehavior.value
      })
    })
  }, 16) // Throttled to ~60fps for performance

  /**
   * Computed property that checks if game is complete
   * @returns {boolean} True if all questions have been used
   */
  const isGameComplete = computed(() => {
    return usedQuestions.value.length >= maxQuestions.value
  })

  /**
   * Throttled function to handle navigation to next question
   * Includes state updates and scroll behavior
   */
  const nextQuestion = useThrottleFn(() => {
    if (isGameComplete.value) {
      gameFinished.value = true
      return
    }

    // Batch updates in microtask for better performance
    Promise.resolve().then(() => {
      showSolution.value = false
      onReset?.()
      onNextQuestion?.()
      scrollToTop()
    })
  }, 250) // Throttled to prevent rapid clicks

  /**
   * Lifecycle hooks for setup and cleanup
   * Sets up media query listener and handles cleanup
   */
  onMounted(() => {
    // Initialize media query listener
    mediaQueryList = window.matchMedia('(prefers-reduced-motion: reduce)')
    prefersReducedMotion.value = mediaQueryList.matches

    // Event handler for preference changes
    const updateMotionPreference = (e: MediaQueryListEvent) => {
      prefersReducedMotion.value = e.matches
    }

    mediaQueryList.addEventListener('change', updateMotionPreference)

    // Cleanup function to prevent memory leaks
    onUnmounted(() => {
      mediaQueryList?.removeEventListener('change', updateMotionPreference)
      mediaQueryList = null
    })
  })

  // Return public API
  return {
    scrollToTop,
    nextQuestion,
    smoothScrollBehavior,
    isGameComplete,
    lastScrollPosition
  }
} 
