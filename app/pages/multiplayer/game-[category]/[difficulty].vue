<template>
  <NuxtLayout name="default" :show-header="false" :show-menu="false">
    <main class="min-h-screen w-full">
      <Transition name="slide" mode="out-in" class="motion-reduce:transition-none">
        <!-- Player Setup -->
        <div
          v-if="!gameStarted"
          :key="'setup'"
          class="mx-auto my-8 max-w-4xl rounded-md bg-[var(--color-surface)] p-6 shadow-md"
          aria-labelledby="setup-title"
        >
          <h2
            id="setup-title"
            class="mb-6 text-center text-xl leading-tight font-bold text-[var(--color-primary)] md:text-2xl"
          >
            {{ t('multiplayer.setup.title') }}
          </h2>
          <div class="mb-6 flex justify-center gap-4">
            <button
              v-for="count in [2, 3, 4]"
              :key="count"
              type="button"
              :class="[
                playerCount === count
                  ? 'bg-[var(--color-primary)] text-white'
                  : 'bg-transparent text-[var(--color-primary)]',
                'min-h-[44px] cursor-pointer rounded-md border border-[var(--color-primary)] px-4 py-2 transition-colors focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] focus-visible:ring-offset-2 focus-visible:outline-none motion-reduce:transition-none',
              ]"
              @click="playerCount = count"
              :aria-pressed="playerCount === count"
              :aria-label="`${count} ${t('multiplayer.setup.players')}`"
            >
              {{ count }} {{ t('multiplayer.setup.players') }}
            </button>
          </div>
          <div class="mb-6 flex flex-col gap-4">
            <div v-for="n in playerCount" :key="n" class="flex flex-col gap-2">
              <label class="font-medium text-[var(--color-primary)]" :for="`player-${n}`">
                {{ t('multiplayer.setup.playerName', { number: n }) }}
              </label>
              <input
                :id="`player-${n}`"
                v-model="playerNames[n - 1]"
                type="text"
                :placeholder="t('multiplayer.setup.enterName')"
                class="min-h-[44px] rounded-md border border-[var(--color-surface-light)] bg-[var(--color-background)] px-3 py-2 text-base text-[var(--color-primary)] focus:border-[var(--color-primary)] focus:ring-2 focus:ring-[var(--color-primary)] focus:outline-none"
                required
              />
            </div>
          </div>
          <button
            type="button"
            class="min-h-[44px] w-full cursor-pointer rounded-md border-none bg-[var(--color-primary)] px-4 py-3 text-base font-bold text-white transition-all hover:-translate-y-0.5 hover:bg-[var(--color-primary-dark)] hover:shadow-md focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] focus-visible:ring-offset-2 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:transform-none disabled:hover:shadow-none motion-reduce:transform-none motion-reduce:transition-none"
            :disabled="!canStartGame"
            @click="startGame"
            aria-label="Start multiplayer game"
          >
            {{ t('multiplayer.setup.startGame') }}
          </button>
        </div>

        <!-- Game Content -->
        <div v-else-if="!gameFinished" :key="'game'" class="mx-auto max-w-4xl px-4">
          <div class="mb-6">
            <div
              class="mb-4 flex flex-wrap justify-center gap-2 p-2 sm:flex-col md:flex-row"
              role="status"
              aria-label="Player scores"
            >
              <div
                v-for="(player, index) in players"
                :key="index"
                :class="[
                  currentPlayerIndex === index
                    ? 'bg-[var(--color-primary)] shadow-md'
                    : 'bg-[var(--color-surface)]',
                  'flex min-h-[44px] w-full items-center gap-4 rounded-full px-4 py-2 transition-colors motion-reduce:transition-none sm:w-auto',
                ]"
                :aria-current="currentPlayerIndex === index ? 'true' : 'false'"
              >
                <span
                  class="text-base leading-normal font-semibold"
                  :class="{
                    'text-white': currentPlayerIndex === index,
                    'text-[var(--color-primary)]': currentPlayerIndex !== index,
                  }"
                >
                  {{ player.name }}
                </span>
                <div class="ml-auto flex items-center gap-2">
                  <span
                    class="flex items-center gap-1"
                    :class="{
                      'text-white': currentPlayerIndex === index,
                      'text-[var(--color-primary)]': currentPlayerIndex !== index,
                    }"
                    :aria-label="`Score: ${player.score}`"
                  >
                    <Icon name="material-symbols:stars" aria-hidden="true" />
                    {{ player.score }}
                  </span>
                  <span
                    class="text-sm"
                    :class="{
                      'text-white': currentPlayerIndex === index,
                      'text-[var(--color-secondary)]': currentPlayerIndex !== index,
                    }"
                    :aria-label="`Round ${playerRounds[index]} of ${roundsPerPlayer}`"
                  >
                    {{ playerRounds[index] }}/{{ roundsPerPlayer }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <Transition name="slide" mode="out-in" class="motion-reduce:transition-none">
            <!-- Question View -->
            <div v-if="!showSolution" :key="'question'">
              <GameQuestionView
                v-if="currentQuestion"
                :question="currentQuestion"
                :current-options="currentOptions"
                :hidden-options="hiddenOptions"
                :disabled="showSolution"
                :remaining-jokers="0"
                :joker-used-for-current-question="true"
                :phone-expert-opinion="null"
                :audience-opinion="null"
                @select-answer="selectAnswer"
              />
            </div>

            <!-- Solution View -->
            <SolutionView
              v-else-if="currentQuestion"
              :key="'solution'"
              :is-correct-answer="isCorrectAnswer"
              :current-round="usedQuestions.length"
              :max-rounds="maxQuestions"
              :question="currentQuestion"
              :artist="currentArtist"
              :is-playing="isPlaying"
              :audio-loaded="audioLoaded"
              :is-buffering="isBuffering"
              :progress="progress"
              :current-player-name="currentPlayer?.name || ''"
              @toggle-play="togglePlay"
              @next="nextTurn"
            />
          </Transition>
        </div>

        <!-- Game Over Screen -->
        <MultiplayerGameOverScreen
          v-else
          :key="'gameover'"
          :players="players"
          :max-questions="maxQuestions"
          @play-again="startGame"
        />
      </Transition>
    </main>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { useRoute, useSeoMeta } from '#imports'
import { computed, nextTick, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import MultiplayerGameOverScreen from '~/components/game/MultiplayerGameOverScreen.vue'
import SolutionView from '~/components/game/SolutionView.vue'

// Import composables
import { useArtist } from '~/composables/useArtist'
import { useGameAudio } from '~/composables/useGameAudio'
import { useGameNavigation } from '~/composables/useGameNavigation'
import { useGameState } from '~/composables/useGameState'
import { useJokers } from '~/composables/useJokers'
import { useQuestions } from '~/composables/useQuestions'

// Initialize core utilities
const route = useRoute()
const { t, locale } = useI18n()

// --- Route Parameters ---
const category = route.params.category as string
const difficulty = route.params.difficulty as string

// --- Load Category Data ---
// Define category type
interface CategoryData {
  categoryUrl: string
  headline: string
  imageUrl: string
  introSubline: string
  isPlayable: boolean
  slug: string
  text: string
  spotifyPlaylist?: string
  deezerPlaylist?: string
  appleMusicPlaylist?: string
  knowledgeUrl?: string
  name?: string // Falls 'name' in einigen Kategorien verwendet wird
}

// Import category data based on current locale
const categories = await import(`~/json/${locale.value}_categories.json`)
const currentCategoryData = ref(categories.default.find((cat: CategoryData) => cat.slug === category))

// --- Multiplayer State ---
const gameStarted = ref(false)
const playerCount = ref(2)
const playerNames = ref<string[]>(['', '', '', ''])
const currentPlayerIndex = ref(0)
const currentRound = ref(1)
const players = ref<Array<{ name: string; score: number; correctAnswers: number }>>([])

const currentPlayer = computed(() => {
  if (players.value.length === 0 || currentPlayerIndex.value >= players.value.length) {
    return { name: '', score: 0, correctAnswers: 0 }
  }
  return players.value[currentPlayerIndex.value]
})
const canStartGame = computed(() => {
  const activeNames = playerNames.value.slice(0, playerCount.value)
  return activeNames.every((name) => name.trim() !== '')
})

// --- Initialize Game Composables ---
const questions = useQuestions(category, difficulty) // Question management
const jokers = useJokers(difficulty) // Lifeline/joker system
const gameState = useGameState(questions.maxQuestions.value) // Game state tracking
const artist = useArtist() // Artist/music info handling
// Destrukturiere die Rückgabewerte von useGameAudio
const { isPlaying, audioLoaded, isBuffering, progress, togglePlay, handleArtistChange } =
  useGameAudio() // Audio playback management

// Navigation utilities
const { scrollToTop } = useGameNavigation({
  usedQuestions: questions.usedQuestions,
  maxQuestions: questions.maxQuestions,
  gameFinished: gameState.gameFinished,
  showSolution: gameState.showSolution,
})

// --- Game State ---
const roundsPerPlayer = computed(() =>
  difficulty === 'easy' ? 10 : difficulty === 'medium' ? 15 : 20
)
const playerRounds = ref(new Array(4).fill(0)) // Track rounds for each player

const gameFinished = computed(
  () => playerRounds.value[currentPlayerIndex.value] >= roundsPerPlayer.value
)
const showSolution = computed(() => gameState.showSolution.value)
const isCorrectAnswer = computed(() => gameState.isCorrectAnswer.value)

// --- Computed Properties ---
const currentQuestion = computed(() => questions.currentQuestion.value)
const currentOptions = computed(() => questions.currentOptions.value)
const hiddenOptions = computed(() => jokers.hiddenOptions.value)
const currentArtist = computed(() => artist.currentArtist.value)
const usedQuestions = computed(() => questions.usedQuestions.value)
const maxQuestions = computed(() => questions.maxQuestions.value)

// --- Game Logic ---
const startGame = () => {
  // Initialize players
  players.value = playerNames.value
    .slice(0, playerCount.value)
    .map((name) => ({ name, score: 0, correctAnswers: 0 }))

  // Reset player rounds
  playerRounds.value = new Array(playerCount.value).fill(0)

  // Start game
  gameStarted.value = true
  currentRound.value = 1
  questions.loadQuestions()
}

const nextTurn = async () => {
  // Increment rounds for current player
  playerRounds.value[currentPlayerIndex.value]++
  currentRound.value++

  // Check if current player has finished their rounds
  if (playerRounds.value[currentPlayerIndex.value] >= roundsPerPlayer.value) {
    // Find next player who hasn't finished their rounds
    let nextPlayerFound = false
    for (let i = 1; i < playerCount.value; i++) {
      const nextIndex = (currentPlayerIndex.value + i) % playerCount.value
      if (playerRounds.value[nextIndex] < roundsPerPlayer.value) {
        currentPlayerIndex.value = nextIndex
        nextPlayerFound = true
        break
      }
    }

    // If no next player found, game is over
    if (!nextPlayerFound) {
      gameState.gameFinished.value = true
      return
    }
  } else {
    // Move to next player
    currentPlayerIndex.value = (currentPlayerIndex.value + 1) % playerCount.value

    // Skip players who have finished their rounds
    while (playerRounds.value[currentPlayerIndex.value] >= roundsPerPlayer.value) {
      currentPlayerIndex.value = (currentPlayerIndex.value + 1) % playerCount.value
    }
  }

  // Get a new question for the next player
  await questions.selectRandomQuestion()
  gameState.showSolution.value = false
  gameState.isCorrectAnswer.value = false
  scrollToTop()
}

const selectAnswer = async (selectedAnswer: string) => {
  if (gameState.showSolution.value) return
  if (!questions.currentQuestion.value) return

  const isCorrect = selectedAnswer === questions.currentQuestion.value.correctAnswer
  gameState.setAnswer(isCorrect)

  if (isCorrect) {
    // Fixed points for correct answer in multiplayer
    const points = 100
    const currentPlayer = players.value[currentPlayerIndex.value]
    if (currentPlayer) {
      currentPlayer.score += points
      currentPlayer.correctAnswers++
    }
  }

  await artist.loadCurrentArtist(category, difficulty, questions.currentQuestion)
  await nextTick()
  scrollToTop()
}

// --- SEO Meta Tags ---
useSeoMeta({
  title: computed(() =>
    t('multiplayer.meta.title', {
      category: currentCategoryData.value?.name || category,
      difficulty: difficulty,
    })
  ),
  description: computed(() =>
    t('multiplayer.meta.description', {
      category: currentCategoryData.value?.name || category,
      difficulty: difficulty,
    })
  ),
  ogTitle: computed(() =>
    t('multiplayer.meta.title', {
      category: currentCategoryData.value?.name || category,
      difficulty: difficulty,
    })
  ),
  ogDescription: computed(() =>
    t('multiplayer.meta.description', {
      category: currentCategoryData.value?.name || category,
      difficulty: difficulty,
    })
  ),
  ogType: 'website',
  robots: 'noindex, follow',
})

// --- Watchers & Lifecycle Hooks ---
watch(
  () => artist.currentArtist.value,
  (newArtist) => {
    if (newArtist) {
      handleArtistChange(newArtist)
    }
  }
)
</script>

<style>
/* High contrast mode support */
@media (prefers-contrast: more) {
  h1,
  h2,
  h3,
  h4 {
    text-decoration: underline !important;
    text-underline-offset: 4px !important;
  }

  a,
  button {
    outline: 2px solid currentColor !important;
    outline-offset: 2px !important;
    text-decoration: underline !important;
  }

  [class*='bg-[var(--color-primary)]'] {
    background-color: black !important;
    color: white !important;
    border: 2px solid white !important;
  }

  input,
  select {
    border: 2px solid black !important;
  }
}

/* Print styles */
@media print {
  main {
    background-color: white !important;
    color: black !important;
  }

  h1,
  h2,
  h3,
  h4 {
    color: black !important;
    font-size: 14pt !important;
    font-weight: bold !important;
    margin-bottom: 10pt !important;
  }

  p,
  span {
    color: black !important;
    font-size: 12pt !important;
  }

  button,
  input {
    border: 1px solid #000 !important;
    color: black !important;
    background-color: white !important;
  }

  .shadow-md,
  .shadow-lg {
    box-shadow: none !important;
  }

  /* Hide non-essential elements when printing */
  [role='status'] {
    margin-bottom: 20pt !important;
    border: 1px solid #000 !important;
    padding: 10pt !important;
  }
}
</style>
