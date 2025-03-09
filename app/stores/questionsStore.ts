/**
 * Questions management store using Pinia
 * Handles loading, caching, and selecting questions
 */

import { defineStore } from 'pinia'
import { useI18n } from 'vue-i18n'

// Type definitions for the quiz structure
interface Question {
  question: string
  options: string[]
  correctAnswer: string
}

interface Artist {
  questions: {
    [key: string]: Question[] // Dictionary of difficulty levels to question arrays
  }
}

// Fisher-Yates (Knuth) shuffle algorithm for better randomization
const shuffleArray = <T>(array: T[]): T[] => {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    const temp = shuffled[i]!
    shuffled[i] = shuffled[j]!
    shuffled[j] = temp
  }
  return shuffled
}

/**
 * Simple memoization function to cache results of pure functions
 * @param fn The function to memoize
 * @returns Memoized version of the function
 */
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

// Memoized function to shuffle options for better performance
const memoizedShuffleOptions = memoize((options: string[]): string[] => {
  return shuffleArray<string>(options)
})

export const useQuestionsStore = defineStore('questions', {
  state: () => ({
    currentQuestion: null as Question | null,
    questions: [] as Question[],
    usedQuestions: [] as number[],
    currentOptions: [] as string[],
    category: '',
    difficulty: '',
    // Cache system to store loaded questions and prevent unnecessary API calls
    questionsCache: new Map<string, Question[]>(),
  }),

  getters: {
    /**
     * Compute the maximum number of questions based on difficulty level
     */
    maxQuestions: (state) => {
      switch (state.difficulty) {
        case 'easy':
          return 10
        case 'medium':
          return 15
        case 'hard':
          return 20
        default:
          return 10
      }
    },

    /**
     * Get current locale for loading questions
     */
    localeValue(): string {
      const { locale } = useI18n()
      return (locale.value ?? 'en') as string
    },

    /**
     * Generate a cache key based on category, difficulty and locale
     */
    cacheKey(): string {
      return `${this.category}-${this.difficulty}-${this.localeValue}`
    },
  },

  actions: {
    /**
     * Initialize the store with category and difficulty
     */
    init(category: string, difficulty: string) {
      this.category = category
      this.difficulty = difficulty
      this.usedQuestions = []
      this.currentQuestion = null
      this.currentOptions = []
    },

    /**
     * Shuffle options for a question
     */
    shuffleOptions(question: Question): string[] {
      if (!question?.options?.length) return []
      return memoizedShuffleOptions(question.options)
    },

    /**
     * Loads questions from JSON files based on category and difficulty
     * Uses caching to improve performance on subsequent loads
     */
    async loadQuestions() {
      try {
        // Check cache
        if (this.questionsCache.has(this.cacheKey)) {
          this.questions = this.questionsCache.get(this.cacheKey)!
          await this.selectRandomQuestion()
          return
        }

        const response = await import(
          /* webpackChunkName: "questions-[request]" */
          `~/json/genres/${this.localeValue}/${this.category}.json`
        )

        const allQuestions = response.default.reduce((acc: Question[], artist: Artist) => {
          const difficultyQuestions = artist.questions[this.difficulty] || []
          return [...acc, ...difficultyQuestions]
        }, [])

        if (allQuestions.length === 0) {
          throw new Error(
            `No questions found for category ${this.category} and difficulty ${this.difficulty}`
          )
        }

        // Set cache
        const shuffledQuestions = shuffleArray([...allQuestions])
        this.questionsCache.set(this.cacheKey, shuffledQuestions)
        this.questions = shuffledQuestions
        await this.selectRandomQuestion()
      } catch (error) {
        console.error('Error loading questions:', error)
        throw error
      }
    },

    /**
     * Selects a random question that hasn't been used yet
     * Resets used questions when all questions have been shown
     * Updates currentQuestion and shuffles its options
     */
    async selectRandomQuestion() {
      if (!this.questions || this.questions.length === 0) return

      const availableIndices = Array.from({ length: this.questions.length }, (_, i) => i).filter(
        (i) => !this.usedQuestions.includes(i)
      )

      if (availableIndices.length === 0) {
        this.usedQuestions = []
        return this.selectRandomQuestion()
      }

      const randomIndex = availableIndices[Math.floor(Math.random() * availableIndices.length)]
      if (typeof randomIndex !== 'number') return

      const question = this.questions[randomIndex]

      if (!question) return

      this.usedQuestions.push(randomIndex)
      this.currentQuestion = {
        ...question,
        correctAnswer: question.correctAnswer,
      }

      if (this.currentQuestion) {
        this.currentOptions = this.shuffleOptions(this.currentQuestion)
      }
    },

    /**
     * Clear the cache and reset the store
     */
    clearStore() {
      this.questionsCache.clear()
      this.questions = []
      this.usedQuestions = []
      this.currentQuestion = null
      this.currentOptions = []
    },
  },
})
