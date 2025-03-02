<!--
  Game page component for Melody Mind
  Displays the game interface based on category and difficulty
  Implements WCAG AAA accessibility standards and responsive design
  @author Daniel Schmid
  @version 1.0.0
-->

<template>
  <NuxtLayout name="default" :show-header="false" :show-menu="false">
    <main
      id="main-content"
      class="min-h-screen bg-[var(--color-background)] p-4 motion-reduce:transition-none sm:p-6 lg:p-8 print:p-0"
      aria-live="polite"
      aria-atomic="true"
    >
      <Transition
        enter-active-class="transition-all duration-300 ease-out motion-reduce:transition-none"
        enter-from-class="opacity-0 translate-x-4"
        enter-to-class="opacity-100 translate-x-0"
        leave-active-class="transition-all duration-300 ease-in motion-reduce:transition-none"
        leave-from-class="opacity-100 translate-x-0"
        leave-to-class="opacity-0 translate-x-4"
        mode="out-in"
      >
        <!-- Game Content -->
        <div
          v-if="!gameFinished"
          :key="'game'"
          class="mx-auto w-full max-w-3xl print:max-w-full"
          aria-label="Game in progress"
        >
          <Transition
            enter-active-class="transition-all duration-300 ease-out motion-reduce:transition-none"
            enter-from-class="opacity-0 translate-y-4"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition-all duration-300 ease-in motion-reduce:transition-none"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 translate-y-4"
            mode="out-in"
          >
            <!-- Question View -->
            <div
              v-if="!showSolution"
              :key="'question'"
              class="space-y-6 motion-reduce:animate-none"
            >
              <GameHeader
                :category-name="currentCategoryData.value?.name || category"
                :current-round="usedQuestions.length"
                :max-rounds="maxQuestions"
                :points="points"
                :is-animating="isAnimating"
                :show-bonus="showBonus"
                :latest-bonus="latestBonus"
                class="mb-6"
              />

              <GameQuestionView
                v-if="currentQuestion"
                :question="currentQuestion"
                :current-options="currentOptions"
                :hidden-options="hiddenOptions"
                :disabled="showSolution"
                :remaining-jokers="remainingJokers"
                :joker-used-for-current-question="jokerUsedForCurrentQuestion"
                :phone-expert-opinion="phoneExpertOpinion"
                :audience-opinion="audienceHelp"
                class="overflow-hidden rounded-xl shadow-lg"
                @select-answer="selectAnswer"
                @use-fifty-fifty="useFiftyFiftyJoker(currentQuestion)"
                @use-audience="useAudienceJoker(currentQuestion)"
                @use-phone="usePhoneJoker(currentQuestion)"
              />
            </div>
            <!-- Solution View -->
            <SolutionView
              v-else-if="currentQuestion"
              :key="'solution'"
              :is-correct-answer="isCorrectAnswer"
              :latest-bonus="latestBonus"
              :current-round="usedQuestions.length"
              :max-rounds="maxQuestions"
              :question="currentQuestion"
              :artist="currentArtist"
              :is-playing="isPlaying"
              :audio-loaded="audioLoaded"
              :is-buffering="isBuffering"
              :progress="progress"
              class="overflow-hidden rounded-xl shadow-lg motion-reduce:animate-none"
              @toggle-play="togglePlay"
              @next="nextQuestion"
            />
          </Transition>
        </div>
        <!-- Game Over Screen -->
        <GameOverScreen
          v-else
          :key="'gameover'"
          :total-points="totalPoints"
          :correct-answers="correctAnswers"
          :max-questions="maxQuestions"
          :earned-record="currentReward !== 'none'"
          :record-icon="recordIcon"
          :record-class="recordClass"
          :result-message="currentResultMessage"
          class="mx-auto max-w-3xl overflow-hidden rounded-xl shadow-lg motion-reduce:animate-none print:border print:border-gray-300 print:shadow-none"
          aria-label="Game over screen"
        />
      </Transition>
    </main>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { useJsonld, useRequestURL, useRoute, useSeoMeta } from '#imports'
import { computed, nextTick, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import GameOverScreen from '~/components/game/GameOverScreen.vue'
import SolutionView from '~/components/game/SolutionView.vue'

// Initialize core utilities
const route = useRoute()
const { t, locale } = useI18n()
const url = useRequestURL()

// --- Route Parameters ---
// Extract category and difficulty from URL parameters
const category = route.params.category as string
const difficulty = route.params.difficulty as string

// --- Load Category Data ---
// Import category data based on current locale
const categories = await import(`~/json/${locale.value}_categories.json`)
const currentCategoryData = ref(categories.default.find((cat: any) => cat.slug === category))

// SEO Meta Tags
useSeoMeta({
  title: computed(() =>
    t('game.meta.title', {
      category: currentCategoryData.value?.name || category,
      difficulty: difficulty,
    })
  ),
  description: computed(() =>
    t('game.meta.description', {
      category: currentCategoryData.value?.name || category,
      difficulty: difficulty,
    })
  ),
  ogTitle: computed(() =>
    t('game.meta.title', {
      category: currentCategoryData.value?.name || category,
      difficulty: difficulty,
    })
  ),
  ogDescription: computed(() =>
    t('game.meta.description', {
      category: currentCategoryData.value?.name || category,
      difficulty: difficulty,
    })
  ),
  ogType: 'website',
  robots: 'noindex, follow', // Spiel-Seiten sollten nicht indexiert werden
})

// JSON-LD
useJsonld({
  '@context': 'https://schema.org',
  '@type': 'VideoGame',
  name: t('game.meta.title', {
    category: route.params.category,
    difficulty: route.params.difficulty,
  }),
  description: t('game.meta.description', {
    category: route.params.category,
    difficulty: route.params.difficulty,
  }),
  url: url.href,
  genre: 'Music Quiz',
  gamePlatform: 'Web Browser',
  applicationCategory: 'Game',
  gameItem: {
    '@type': 'Thing',
    name: route.params.category,
    description: t('game.meta.description', {
      category: route.params.category,
      difficulty: route.params.difficulty,
    }),
  },
  audience: {
    '@type': 'Audience',
    audienceType: 'Music Enthusiasts',
  },
})

// --- Initialize Game Composables ---
// Core game mechanics
const questions = useQuestions(category, difficulty) // Question management
const jokers = useJokers(difficulty) // Lifeline/joker system
const gameState = useGameState(questions.maxQuestions.value) // Game state tracking
const { points } = gameState
const artist = useArtist() // Artist/music info handling
const timeBonus = useTimeBonus() // Time-based bonus system
const gameScore = useGameScore()
const { resultMessage, earnedRecord, calculateReward, getResultMessage, saveGameResults } =
  useGameResults()

// Audio playback management
const gameAudio = useGameAudio()

// Social sharing functionality
const sharing = useShare({ currentCategoryData: currentCategoryData.value, category, difficulty })

// Navigation utilities
const { scrollToTop } = useGameNavigation({
  usedQuestions: questions.usedQuestions,
  maxQuestions: questions.maxQuestions,
  gameFinished: gameState.gameFinished,
  showSolution: gameState.showSolution,
})

// --- Game Logic ---
/**
 * Handles progression to the next question
 * - Selects a new random question
 * - Resets game state
 * - Resets jokers
 * - Starts time bonus timer
 * - Scrolls to top of page
 */
const nextQuestion = async () => {
  await questions.selectRandomQuestion()
  gameState.prepareNextQuestion()
  jokers.resetJokerForQuestion()
  timeBonus.startTimer()
  scrollToTop()
}

/**
 * Handles answer selection
 * @param selectedAnswer - The answer chosen by the player
 *
 * - Validates if answer can be processed
 * - Checks answer correctness
 * - Updates game state and points
 * - Loads artist information if needed
 * - Handles UI updates
 */
const selectAnswer = async (selectedAnswer: string) => {
  if (gameState.showSolution.value) return
  if (!questions.currentQuestion.value) return

  const isCorrect = selectedAnswer === questions.currentQuestion.value.correctAnswer
  gameState.setAnswer(isCorrect)

  if (isCorrect) {
    const bonus = timeBonus.calculateBonus()
    gameState.updatePoints(bonus.base, bonus.time)
  }

  await artist.loadCurrentArtist(category, difficulty, questions.currentQuestion)
  await nextTick()
  scrollToTop()
}

// --- Watchers & Lifecycle Hooks ---
// Initialize questions on component mount
onMounted(() => {
  questions.loadQuestions()
})

// Handle artist changes for audio playback
watch(() => artist.currentArtist.value, gameAudio.handleArtistChange)

// Monitor game completion
watch(
  () => questions.usedQuestions.value.length,
  async (newLength) => {
    if (newLength > questions.maxQuestions.value) {
      // Set game as finished to show end screen
      gameState.finishGame()
    }
  }
)

// Cleanup audio when leaving page
onBeforeRouteLeave(() => {
  gameAudio.cleanup()
})

// --- Computed Properties for Game Over Screen ---
const currentReward = computed(() => {
  return calculateReward(
    gameState.correctAnswers.value,
    questions.maxQuestions.value,
    gameState.allQuestionsCorrect.value
  )
})

const currentResultMessage = computed(() => {
  const reward = calculateReward(
    gameState.correctAnswers.value,
    questions.maxQuestions.value,
    gameState.allQuestionsCorrect.value
  )
  return getResultMessage(reward)
})

const recordIcon = computed(() => {
  switch (currentReward.value) {
    case 'gold':
      return 'material-symbols:workspace-premium'
    case 'silver':
      return 'material-symbols:stars'
    case 'bronze':
      return 'material-symbols:military-tech'
    default:
      return ''
  }
})

const recordClass = computed(() => {
  return currentReward.value !== 'none' ? 'new-record' : ''
})

// --- Template Exports ---
// Destructure and export required properties for the template
const {
  currentQuestion, // Current active question
  currentOptions, // Available answer options
  maxQuestions, // Total questions in game
  usedQuestions, // Questions already answered
} = questions

// Joker/Lifeline system exports
const {
  remainingJokers,
  jokerUsedForCurrentQuestion,
  audienceHelp,
  hiddenOptions,
  phoneExpertOpinion,
  useFiftyFiftyJoker,
  useAudienceJoker,
  usePhoneJoker,
} = jokers

// Game state exports
const {
  showSolution, // Whether to show answer
  isCorrectAnswer, // If last answer was correct
  gameFinished, // Game completion status
  correctAnswers, // Total correct answers
  totalPoints, // Total score
  isAnimating, // Animation state
  showBonus, // Bonus display state
  latestBonus, // Latest bonus earned
} = gameState

// Audio player exports
const {
  isPlaying, // Playback state
  audioLoaded, // Audio loading state
  isBuffering, // Buffer state
  progress, // Playback progress
  togglePlay, // Play/pause function
} = gameAudio

const { currentArtist } = artist // Current artist information
</script>

<style>
/* Custom animations with Tailwind */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* High Contrast Mode Support */
@media (forced-colors: active) {
  button {
    border: 2px solid ButtonText !important;
    background-color: Canvas !important;
    color: ButtonText !important;
  }

  button:focus {
    outline: 2px solid ButtonText !important;
    outline-offset: 2px !important;
  }

  button:hover:not(:disabled) {
    background-color: Highlight !important;
    color: HighlightText !important;
  }

  a {
    text-decoration: underline !important;
  }
}

/* Increased contrast mode */
@media (prefers-contrast: more) {
  button {
    border: 2px solid currentColor !important;
    font-weight: 700 !important;
  }

  button:focus {
    outline: 3px solid currentColor !important;
    outline-offset: 3px !important;
  }

  h1,
  h2,
  h3,
  h4 {
    text-decoration: underline !important;
    text-underline-offset: 4px !important;
  }

  a {
    text-decoration: underline !important;
    font-weight: 700 !important;
  }
}

/* Print mode styling */
@media print {
  .game-header {
    border-bottom: 1px solid #000 !important;
    margin-bottom: 1rem !important;
    padding-bottom: 0.5rem !important;
  }

  button,
  .joker-button {
    display: none !important;
  }

  * {
    color: #000 !important;
    background-color: #fff !important;
    font-size: 12pt !important;
  }

  h1,
  h2,
  h3 {
    font-size: 14pt !important;
    font-weight: bold !important;
    margin-bottom: 0.5rem !important;
  }
}
</style>
