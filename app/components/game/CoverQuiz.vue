<template>
  <div class="mx-auto flex w-full max-w-4xl flex-col items-center gap-6">
    <!-- Timer and Score Display -->
    <div class="mb-4 flex w-full items-center justify-between">
      <div class="text-2xl font-bold">{{ t('game.round') }}: {{ currentRound }}/10</div>
      <div class="text-2xl font-bold text-[var(--color-primary)]">{{ remainingTime }}s</div>
      <div class="text-2xl font-bold">{{ t('game.score') }}: {{ formattedPoints }}</div>
    </div>

    <!-- Album Cover Display with Puzzle Effect -->
    <div class="relative mx-auto aspect-square w-full max-w-md">
      <!-- Übergang/Ladeanzeige zwischen Runden -->
      <div
        v-if="isLoading"
        class="absolute inset-0 z-20 flex items-center justify-center rounded-lg bg-black"
      >
        <div class="border-primary h-16 w-16 animate-spin rounded-full border-4 border-t-4"></div>
      </div>

      <div
        v-if="currentAlbum"
        class="grid h-full w-full grid-cols-6 grid-rows-6 gap-0.5 overflow-hidden rounded-lg"
        :style="{ opacity: isLoading ? 0 : 1 }"
      >
        <div
          v-for="(_, index) in 36"
          :key="index"
          class="puzzle-piece relative overflow-hidden"
          :style="{
            opacity: revealedPieces[index] ? 1 : 0,
            transform: revealedPieces[index] ? 'scale(1)' : 'scale(0.8) rotate(10deg)',
          }"
        >
          <div
            class="absolute inset-0 bg-cover bg-center"
            :style="{
              backgroundImage:
                currentAlbum && currentAlbum.coverSrc ? `url('${currentAlbum.coverSrc}')` : 'none',
              backgroundSize: '600%',
              backgroundPosition: `${(index % 6) * 20}% ${Math.floor(index / 6) * 20}%`,
            }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Answer Buttons -->
    <div class="mt-4 grid w-full grid-cols-1 gap-4 md:grid-cols-2">
      <button
        v-for="option in currentOptions"
        :key="option.artist + option.album"
        @click="checkAnswer(option)"
        :disabled="showSolution || gameFinished"
        :class="[
          'rounded-lg p-4 font-medium text-white transition-all duration-200',
          {
            'bg-[var(--color-primary)] hover:bg-[var(--color-primary-dark)]':
              !showSolution || option !== currentAlbum,
            'bg-green-600': showSolution && option === currentAlbum,
            'bg-red-600': showSolution && selectedOption === option && option !== currentAlbum,
            'opacity-70': showSolution || gameFinished,
          },
        ]"
      >
        {{ option.artist }} - {{ option.album }} ({{ option.year }})
      </button>
    </div>

    <!-- Next Button / Game Over -->
    <div v-if="showSolution || gameFinished" class="mt-4 flex w-full justify-center">
      <button
        v-if="!gameFinished"
        @click="nextRound"
        class="rounded-lg bg-[var(--color-primary)] px-6 py-3 font-medium text-white transition-all duration-200 hover:bg-[var(--color-primary-dark)]"
      >
        {{ t('game.next') }}
      </button>
      <div v-else class="text-center">
        <h2 class="mb-4 text-2xl font-bold">{{ t('game.finished') }}</h2>
        <p class="mb-4 text-xl">{{ t('game.final_score') }}: {{ formattedPoints }}</p>
        <button
          @click="handleRestart"
          class="rounded-lg bg-[var(--color-primary)] px-6 py-3 font-medium text-white transition-all duration-200 hover:bg-[var(--color-primary-dark)]"
        >
          {{ t('game.play_again') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useGameStore } from '~/stores/gameStore'

// Define interface for album data
interface Album {
  artist: string
  album: string
  year: string
  coverSrc: string
}

const props = defineProps<{
  category: string
}>()

const emit = defineEmits<{
  restart: []
}>()

const { t } = useI18n()
const gameStore = useGameStore()
const { showSolution, gameFinished, formattedPoints } = storeToRefs(gameStore)

// Game state variables
const currentRound = ref(1)
const remainingTime = ref(60)
const currentAlbum = ref<Album | null>(null)
const currentOptions = ref<Album[]>([])
const selectedOption = ref<Album | null>(null)
const timer = ref<number | null>(null)
const puzzleInterval = ref<number | null>(null)
const revealedPieces = ref<boolean[]>(Array(36).fill(false))
const usedAlbumIds = ref<Set<string>>(new Set())
const allAlbums = ref<Album[]>([]) // Cache for all loaded albums
const previousAlbumId = ref<string | null>(null) // ID of the last displayed album
const isLoading = ref<boolean>(true) // State variable for loading process

/**
 * Loads album data from the category JSON file
 * Returns cached data if already loaded
 */
const loadAlbums = async (): Promise<Album[]> => {
  if (allAlbums.value.length > 0) {
    return allAlbums.value // Use cache if already loaded
  }

  try {
    const { locale } = useI18n()
    const response = await import(`~/json/genres/${locale.value}/${props.category}.json`)
    const loadedAlbums = response.default.map(
      (item: any): Album => ({
        artist: item.artist,
        album: item.album,
        year: item.year,
        coverSrc: item.coverSrc,
      })
    )

    allAlbums.value = loadedAlbums // Store in cache
    console.log(`All albums loaded: ${loadedAlbums.length}`)
    return loadedAlbums
  } catch (error) {
    console.error('Error loading albums:', error)
    return []
  }
}

/**
 * Creates a unique identifier for an album
 */
const getAlbumId = (album: Album): string => {
  return `${album.artist}-${album.album}`
}

/**
 * Selects 4 random albums and sets one as the correct answer
 * Ensures no repeated albums between rounds
 */
const selectRandomAlbums = async (): Promise<void> => {
  // Set loading state to hide previous album
  isLoading.value = true

  const albums = await loadAlbums()
  if (albums.length < 4) {
    console.error('Not enough albums to play')
    return
  }

  // If we've used too many albums and don't have enough left
  if (usedAlbumIds.value.size > albums.length - 4) {
    console.warn(`Too many albums used (${usedAlbumIds.value.size}), resetting`)
    usedAlbumIds.value.clear()
  }

  // Filter out already used albums
  const availableAlbums = albums.filter((album) => !usedAlbumIds.value.has(getAlbumId(album)))

  console.log(`Available albums: ${availableAlbums.length} out of ${albums.length} total`)

  // Use available albums if there are at least 4, otherwise use all albums
  const albumPool = availableAlbums.length >= 4 ? availableAlbums : albums

  // Better shuffling with Fisher-Yates algorithm
  const shuffledPool = [...albumPool]
  for (let i = shuffledPool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffledPool[i]!, shuffledPool[j]!] = [shuffledPool[j]!, shuffledPool[i]!]
  }

  // Select the first 4 albums for options
  const selectedOptions = shuffledPool.slice(0, 4)

  // Choose a random index for the correct answer
  const correctIndex = Math.floor(Math.random() * 4)
  const correctAnswer = selectedOptions[correctIndex]

  if (!correctAnswer) {
    console.error('Failed to select correct answer')
    return
  }

  // Check if the album is really new
  const newAlbumId = getAlbumId(correctAnswer)
  if (previousAlbumId.value === newAlbumId) {
    console.warn('Same album selected as before! Trying another shuffle...')
    return selectRandomAlbums() // Recursive call for another attempt
  }

  // Store the ID of the current album
  previousAlbumId.value = newAlbumId

  // Mark this album as used
  usedAlbumIds.value.add(newAlbumId)

  // Reset and update game state variables
  revealedPieces.value = Array(36).fill(false)

  // Preload the image before removing loading state
  const img = new Image()
  img.src = correctAnswer.coverSrc
  img.onload = () => {
    // Set new values only after the image is loaded
    currentOptions.value = selectedOptions
    currentAlbum.value = correctAnswer

    // Timeout to ensure DOM has been updated
    setTimeout(() => {
      isLoading.value = false
    }, 200)
  }

  img.onerror = (error) => {
    console.error('Error loading image:', error)
    isLoading.value = false
  }

  console.log(`Round ${currentRound.value}: ${correctAnswer.artist} - ${correctAnswer.album}`)
  console.log(`Cover URL: ${correctAnswer.coverSrc}`)
  console.log(`Used albums: ${usedAlbumIds.value.size}`)
}

/**
 * Starts the round timer and puzzle piece reveal animation
 */
const startTimer = () => {
  remainingTime.value = 60

  // Reset puzzle pieces
  revealedPieces.value = Array(36).fill(false)

  // Set and type the timer correctly
  if (timer.value) clearInterval(timer.value)
  timer.value = setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value--
    } else {
      handleTimeout()
    }
  }, 1000) as unknown as number

  // Gradually reveal puzzle pieces in random order
  const revealOrder = shuffleArray<number>([...Array(36).keys()])
  let pieceIndex = 0

  if (puzzleInterval.value) clearInterval(puzzleInterval.value)
  puzzleInterval.value = setInterval(() => {
    if (pieceIndex < revealOrder.length && revealOrder[pieceIndex] !== undefined) {
      const index = revealOrder[pieceIndex]!
      if (index >= 0 && index < 36) {
        revealedPieces.value[index] = true
      }
      pieceIndex++
    } else {
      if (puzzleInterval.value) clearInterval(puzzleInterval.value)
    }
  }, 1200) as unknown as number
}

/**
 * Fisher-Yates shuffle algorithm with improved typing
 * Creates a randomized copy of the input array
 */
const shuffleArray = <T,>(array: T[]): T[] => {
  const result = [...array]
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    // Type-safe exchange
    if (result[i] !== undefined && result[j] !== undefined) {
      const temp = result[i]!
      result[i] = result[j]!
      result[j] = temp
    }
  }
  return result
}

/**
 * Handles timeout when the timer reaches zero
 */
const handleTimeout = () => {
  if (timer.value) clearInterval(timer.value)
  if (puzzleInterval.value) clearInterval(puzzleInterval.value)
  if (!showSolution.value) {
    checkAnswer(null)
  }
}

/**
 * Checks if the selected album is correct
 * Awards points based on remaining time
 */
const checkAnswer = (selected: Album | null) => {
  if (showSolution.value || gameFinished.value) return

  selectedOption.value = selected
  const isCorrect = selected === currentAlbum.value

  if (timer.value) clearInterval(timer.value)
  if (puzzleInterval.value) clearInterval(puzzleInterval.value)

  // Reveal all puzzle pieces
  revealedPieces.value = Array(36).fill(true)

  // Calculate points based on remaining time
  if (isCorrect) {
    const timeBonus = Math.floor(remainingTime.value * 1.5)
    const basePoints = 100
    gameStore.updatePoints(basePoints, timeBonus)
    gameStore.incrementCorrectAnswers()
  }

  gameStore.setAnswer(isCorrect)
}

/**
 * Advances to the next round or finishes the game
 */
const nextRound = async () => {
  if (currentRound.value >= 10) {
    gameStore.finishGame()
    return
  }

  // Increase round counter and prepare next question
  currentRound.value++
  selectedOption.value = null
  gameStore.prepareNextQuestion()

  // Set loading state before loading new data
  isLoading.value = true

  // Stop all timers before starting a new one
  if (timer.value) clearInterval(timer.value)
  if (puzzleInterval.value) clearInterval(puzzleInterval.value)

  // Select a new album and start the timer
  await selectRandomAlbums()
  startTimer()
}

/**
 * Reset the game state and start a new game
 */
const resetGame = async () => {
  // Clear any existing timers
  if (timer.value) clearInterval(timer.value)
  if (puzzleInterval.value) clearInterval(puzzleInterval.value)

  // Reset game state variables
  currentRound.value = 1
  remainingTime.value = 60
  currentAlbum.value = null
  selectedOption.value = null
  revealedPieces.value = Array(36).fill(false)
  isLoading.value = true

  // Reset store state
  gameStore.resetGameState()
  gameStore.initGame(10)

  // Clear history of used albums to get fresh options
  usedAlbumIds.value.clear()
  previousAlbumId.value = null

  // Start new game
  await selectRandomAlbums()
  startTimer()
}

/**
 * Handle restart event from Play Again button
 */
const handleRestart = async () => {
  console.log('Restarting game...')
  await resetGame()
}

// Component lifecycle hooks
onMounted(async () => {
  // Initialize game state
  await resetGame()
})

onBeforeUnmount(() => {
  if (timer.value) clearInterval(timer.value)
  if (puzzleInterval.value) clearInterval(puzzleInterval.value)
})
</script>

<style scoped>
.puzzle-piece {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  backface-visibility: hidden;
  transform-origin: center;
  box-shadow: 0 0 1px rgba(0, 0, 0, 0.2); /* Dünnerer Rand für kleinere Teile */
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.border-primary {
  border-color: var(--color-primary);
  border-top-color: transparent;
}
</style>
