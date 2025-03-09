import { computed, onUnmounted } from 'vue'
import { useQuestionsStore } from '../stores/questionsStore'

// Type definitions for the quiz structure
// Exported for use in other components
export interface Question {
  question: string
  options: string[]
  correctAnswer: string
}

// Type definition for question structure only
// Dictionary structure is now handled by the store

// Shuffle algorithm now implemented directly in the store

// Shuffle and memoization now implemented in the store

/**
 * Legacy composable that uses the new Pinia store internally
 * This provides backward compatibility for existing components
 * New components should use the Pinia store directly
 */
export const useQuestions = (category: string, difficulty: string) => {
  // Use the Pinia store internally
  const questionsStore = useQuestionsStore()

  // Initialize the store with the provided category and difficulty
  questionsStore.init(category, difficulty)
  // Create refs from store values for backward compatibility
  const currentQuestion = computed(() => questionsStore.currentQuestion)
  const questions = computed(() => questionsStore.questions)
  const usedQuestions = computed(() => questionsStore.usedQuestions)
  const currentOptions = computed(() => questionsStore.currentOptions)

  // Maximum questions based on difficulty level
  const maxQuestions = computed(() => questionsStore.maxQuestions)

  /**
   * Delegate shuffling options to the store - now handled directly by the store
   */

  /**
   * Loads questions from JSON files based on category and difficulty
   * Delegates to the Pinia store implementation
   */
  const loadQuestions = async () => {
    try {
      await questionsStore.loadQuestions()
    } catch (error) {
      console.error('Error loading questions:', error)
      throw error
    }
  }

  /**
   * Selects a random question that hasn't been used yet
   * Delegates to the Pinia store implementation
   */
  const selectRandomQuestion = async () => {
    await questionsStore.selectRandomQuestion()
  }

  // Cleanup when component is unmounted
  onUnmounted(() => {
    questionsStore.clearStore()
  })

  return {
    // Return computed refs for backward compatibility
    currentQuestion,
    questions,
    usedQuestions,
    currentOptions,
    maxQuestions,
    // Return store methods
    loadQuestions,
    selectRandomQuestion,
    // Add a reference to the store for advanced usage
    store: questionsStore
  }
}

// Memoization is now handled by the Pinia store
// This code is kept for reference but marked as unused to avoid linting issues
/*
function memoize<TArgs extends unknown[], TReturn>(fn: (...args: TArgs) => TReturn) {
  const cache = new Map<string, TReturn>()
  return (...args: TArgs): TReturn => {
    const key = JSON.stringify(args)
    const cachedResult = cache.get(key)
    if (cachedResult !== undefined) {
      return cachedResult
    }

    const result = fn(...args)
    cache.set(key, result)
    return result
  }
}
*/
