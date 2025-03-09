import type { Ref } from 'vue'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

/**
 * Interface representing an artist with their metadata and associated questions
 */
export interface Artist {
  artist: string
  album: string
  coverSrc: string
  preview_link?: string
  spotify_link?: string
  apple_music_link?: string
  deezer_link?: string
  year: string
  trivia?: string
  questions: {
    [key: string]: Question[] // Questions organized by difficulty level
  }
}

/**
 * Interface representing a single question and its correct answer
 */
export interface Question {
  question: string
  correctAnswer: string
  trivia?: string
}

/**
 * Composable for managing artist data and related operations
 * @returns {Object} Object containing currentArtist ref and loadCurrentArtist function
 */
export function useArtist() {
  const { locale } = useI18n()
  const currentArtist = ref<Artist | null>(null)

  // Cache to store loaded JSON files and prevent redundant network requests
  const artistCache = new Map<string, Artist[]>()

  /**
   * Loads and finds the artist associated with the current question
   * @param {string} category - The music genre/category
   * @param {string} difficulty - The difficulty level of the question
   * @param {Ref<Question | null>} currentQuestion - Reference to the current question
   * @returns {Promise<null>} Returns null if no artist is found or an error occurs
   */
  const loadCurrentArtist = async (
    category: string,
    difficulty: string,
    currentQuestion: Ref<Question | null>
  ) => {
    if (!currentQuestion.value) return null

    try {
      // Generate cache key based on locale and category
      const cacheKey = `${locale.value}/${category}`
      let artists: Artist[]

      // Check if data exists in cache, if not, load and cache it
      if (artistCache.has(cacheKey)) {
        artists = artistCache.get(cacheKey)!
      } else {
        const response = await import(`~/json/genres/${locale.value}/${category}.json`)
        artists = response.default
        artistCache.set(cacheKey, artists)
      }

      // Find the artist that matches the current question
      const foundArtist = artists.find((artist) => {
        const questions = artist.questions[difficulty]
        if (!questions) return false

        // Check if any question in the difficulty level matches the current question
        const matchingQuestion = questions.find(
          (q) =>
            q.question === currentQuestion.value?.question &&
            q.correctAnswer === currentQuestion.value?.correctAnswer
        )

        // If we found a matching question, add its trivia to the artist data
        if (matchingQuestion) {
          // Explizite Typkonversion und stellen sicher, dass trivia immer einen String-Wert hat
          const trivia: string = matchingQuestion.trivia ?? ''
          artist.trivia = trivia
          return true
        }

        return false
      })

      // Process image paths correctly before assigning to currentArtist
      if (foundArtist) {
        // Stellen sicher, dass coverSrc immer ein String ist und nicht undefined
        if (typeof foundArtist.coverSrc === 'string') {
          // Ensure coverSrc path is absolute and formatted correctly
          foundArtist.coverSrc = foundArtist.coverSrc.startsWith('/')
            ? foundArtist.coverSrc
            : `/${foundArtist.coverSrc}`

          // Remove any query parameters from image URL
          if (foundArtist.coverSrc.includes('?')) {
            foundArtist.coverSrc = foundArtist.coverSrc.split('?')[0]
          }
        } else {
          // Falls coverSrc undefined ist, setzen wir einen Fallback-Wert
          foundArtist.coverSrc = '/images/default-cover.jpg'
        }
      }

      currentArtist.value = foundArtist || null
    } catch (error) {
      console.error('Error loading artist:', error)
      currentArtist.value = null
    }
  }

  return {
    currentArtist,
    loadCurrentArtist,
  }
}
