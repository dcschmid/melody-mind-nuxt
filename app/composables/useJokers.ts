import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { generateExpertOpinion, type ExpertResponse } from '~/constants/expertResponses'

/**
 * Type definition for difficulty levels
 */
type Difficulty = 'easy' | 'medium' | 'hard'

/**
 * Predefined joker counts for each difficulty level
 */
const JOKER_COUNTS: Record<Difficulty, number> = {
  easy: 3,
  medium: 5,
  hard: 7,
} as const

/**
 * Helper function to generate random numbers within a range
 */
const getRandomInRange = (min: number, max: number) =>
  Math.floor(Math.random() * (max - min + 1)) + min

/**
 * Composable for managing game jokers (lifelines)
 * @param difficulty - Game difficulty level ("easy" | "medium" | "hard")
 * @returns Object containing joker state and functions
 */
export function useJokers(difficulty: string) {
  const { locale } = useI18n()

  /**
   * Better typing for difficulty
   */
  type Difficulty = 'easy' | 'medium' | 'hard'

  const totalJokers = JOKER_COUNTS[difficulty as Difficulty] ?? 3

  /**
   * Interface for Question
   */
  interface Question {
    options: string[]
    correctAnswer: string
  }

  /**
   * Joker Status
   */
  const remainingJokers = ref(totalJokers)
  const jokerUsedForCurrentQuestion = ref(false)

  /**
   * Joker Results
   */
  const audienceHelp = ref<{ [key: string]: number }>({})
  const hiddenOptions = ref<string[]>([])
  const phoneExpertOpinion = ref<ExpertResponse | null>(null)
  const phoneExpertConfidence = ref(0)

  /**
   * Audience Help Joker
   * Generates a realistic distribution of audience votes with bias towards correct answer
   * @param currentQuestion - Current question object containing options and correct answer
   */
  const useAudienceJoker = (currentQuestion: Question) => {
    if (!canUseJoker()) return

    const correctIndex = currentQuestion.options.indexOf(currentQuestion.correctAnswer)
    const distribution = new Array(currentQuestion.options.length)

    // Direkte Array-Manipulation statt map
    for (let i = 0; i < distribution.length; i++) {
      distribution[i] =
        i === correctIndex
          ? getRandomInRange(50, 80) // 50-80% für richtige Antwort
          : getRandomInRange(0, 20) // 0-20% für falsche Antworten
    }

    // Optimierte Summenberechnung
    let total = 0
    for (let i = 0; i < distribution.length; i++) {
      total += distribution[i]
    }

    // Optimierte Objekt-Erstellung
    const result: Record<string, number> = {}
    for (let i = 0; i < currentQuestion.options.length; i++) {
      result[currentQuestion.options[i]] = Math.round((distribution[i] / total) * 100)
    }
    audienceHelp.value = result

    useJoker()
  }

  /**
   * 50:50 Joker
   * Removes two wrong answers from the options
   * @param currentQuestion - Current question object containing options and correct answer
   */
  const useFiftyFiftyJoker = (currentQuestion: Question) => {
    if (!canUseJoker()) return

    const wrongOptions = []
    for (const option of currentQuestion.options) {
      if (option !== currentQuestion.correctAnswer) {
        wrongOptions.push(option)
      }
    }

    for (let i = wrongOptions.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[wrongOptions[i], wrongOptions[j]] = [wrongOptions[j], wrongOptions[i]]
    }

    hiddenOptions.value = wrongOptions.slice(0, 2)
    useJoker()
  }

  /**
   * Helper Functions
   */
  const canUseJoker = () => remainingJokers.value > 0 && !jokerUsedForCurrentQuestion.value
  const useJoker = () => {
    remainingJokers.value--
    jokerUsedForCurrentQuestion.value = true
  }

  /**
   * Phone Joker
   * Generates an expert opinion with varying confidence levels
   * @param currentQuestion - Current question object containing options and correct answer
   */
  const usePhoneJoker = (currentQuestion: Question) => {
    if (!canUseJoker()) return

    const expertResponse = generateExpertOpinion(
      currentQuestion.correctAnswer,
      currentQuestion.options,
      locale.value
    )

    phoneExpertOpinion.value = {
      expert: expertResponse.expert,
      message: expertResponse.message,
      confidence: expertResponse.confidence,
    }
    phoneExpertConfidence.value = expertResponse.confidence

    useJoker()
  }

  /**
   * Resets all joker states for a new question
   */
  const resetJokers = () => {
    jokerUsedForCurrentQuestion.value = false
    audienceHelp.value = {}
    hiddenOptions.value = []
    phoneExpertOpinion.value = null
    phoneExpertConfidence.value = 0
  }

  /**
   * Reset the joker state for a new question
   * This function:
   * - Resets the joker usage flag for the current question
   * - Clears the audience help results
   * - Clears the phone expert's opinion
   * - Clears any hidden options from the 50:50 joker
   *
   * Should be called whenever a new question is presented to the player
   * to ensure all jokers are available again (if the player has remaining jokers)
   */
  const resetJokerForQuestion = () => {
    jokerUsedForCurrentQuestion.value = false // Allow joker usage for new question
    audienceHelp.value = {} // Clear audience poll results
    phoneExpertOpinion.value = null // Clear expert's previous response
    hiddenOptions.value = [] // Clear hidden options from 50:50
  }

  return {
    /**
     * State
     */
    remainingJokers, // Number of jokers left
    jokerUsedForCurrentQuestion, // Whether a joker was used for current question
    audienceHelp, // Audience vote distribution
    hiddenOptions, // Options hidden by 50:50 joker
    phoneExpertOpinion, // Expert's response
    phoneExpertConfidence, // Expert's confidence level

    /**
     * Methods
     */
    useFiftyFiftyJoker, // Activates 50:50 joker
    useAudienceJoker, // Activates audience help
    usePhoneJoker, // Activates phone joker
    resetJokers, // Resets joker state
    resetJokerForQuestion,
  }
}
