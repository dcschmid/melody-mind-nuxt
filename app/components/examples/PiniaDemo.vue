<template>
  <div class="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white">
      Pinia Store Demo
    </h2>

    <!-- Game State Section -->
    <div class="mb-6">
      <h3 class="text-xl font-semibold mb-3 text-gray-800 dark:text-gray-100">
        Game State
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white dark:bg-gray-700 p-4 rounded-md shadow">
          <div class="flex justify-between items-center mb-2">
            <span class="font-medium text-gray-700 dark:text-gray-300">Punkte:</span>
            <span class="font-bold text-xl text-gray-900 dark:text-white">{{ formattedPoints }}</span>
          </div>
          <div class="flex justify-between items-center mb-2">
            <span class="font-medium text-gray-700 dark:text-gray-300">Richtige Antworten:</span>
            <span class="font-bold text-gray-900 dark:text-white">{{ correctAnswers }} / {{ maxQuestions }}</span>
          </div>
          <div class="mt-4">
            <div class="relative pt-1">
              <div class="flex mb-2 items-center justify-between">
                <div>
                  <span class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-green-600 bg-green-200">
                    Fortschritt
                  </span>
                </div>
                <div class="text-right">
                  <span class="text-xs font-semibold inline-block text-green-600">
                    {{ Math.round(completionPercentage) }}%
                  </span>
                </div>
              </div>
              <div class="overflow-hidden h-2 mb-4 text-xs flex rounded bg-green-200">
                <div
                  :style="{ width: `${completionPercentage}%` }"
                  class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-green-500 transition-all duration-300 ease-in-out"
                  role="progressbar"
                  :aria-valuenow="Math.round(completionPercentage)"
                  aria-valuemin="0"
                  aria-valuemax="100"
                ></div>
              </div>
            </div>
          </div>
          <div class="flex space-x-2 mt-4">
            <button
              @click="addPoints"
              class="px-4 py-2 bg-green-500 hover:bg-green-600 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:outline-none text-white rounded-md transition-colors duration-200 min-h-[44px]">
              + Punkte
            </button>
            <button
              @click="incrementAnswer"
              class="px-4 py-2 bg-blue-500 hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none text-white rounded-md transition-colors duration-200 min-h-[44px]">
              + Richtige Antwort
            </button>
            <button
              @click="resetGame"
              class="px-4 py-2 bg-red-500 hover:bg-red-600 focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:outline-none text-white rounded-md transition-colors duration-200 min-h-[44px]">
              Reset
            </button>
          </div>
        </div>

        <!-- Current Question Section -->
        <div class="bg-white dark:bg-gray-700 p-4 rounded-md shadow">
          <h4 class="font-semibold text-lg mb-3 text-gray-800 dark:text-gray-100">
          Frage
        </h4>
          <div v-if="currentQuestion" class="mb-4">
            <p class="text-gray-700 dark:text-gray-300 mb-3">
            {{ currentQuestion.question }}
          </p>
            <div class="space-y-2">
              <button
                v-for="(option, index) in currentOptions"
                :key="index"
                @click="checkAnswer(option)"
                class="w-full text-left px-4 py-2 bg-gray-100 dark:bg-gray-600 hover:bg-gray-200 dark:hover:bg-gray-500 focus:ring-2 focus:ring-gray-400 focus:outline-none rounded-md transition-colors duration-200 text-gray-800 dark:text-gray-200 min-h-[44px]">
                {{ option }}
              </button>
            </div>
          </div>
          <div v-else class="mb-4 text-gray-700 dark:text-gray-300">
            Lade Fragen...
          </div>
          <div class="mt-4">
            <button
              @click="loadNewQuestion"
              class="w-full px-4 py-2 bg-indigo-500 hover:bg-indigo-600 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:outline-none text-white rounded-md transition-colors duration-200 min-h-[44px]">
              Neue Frage laden
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useGameStore } from '~/app/stores/gameStore'
import { useQuestionsStore } from '~/app/stores/questionsStore'

// Initialize stores
const gameStore = useGameStore()
const questionsStore = useQuestionsStore()

// Destructure store state with storeToRefs (maintains reactivity)
const {
  formattedPoints,
  correctAnswers,
  maxQuestions
} = storeToRefs(gameStore)

const {
  currentQuestion,
  currentOptions
} = storeToRefs(questionsStore)

// Computed properties
const completionPercentage = computed(() => {
  return (correctAnswers.value / maxQuestions.value) * 100 || 0
})

// Initialize on component mount
onMounted(async () => {
  // Initialize game with 10 questions
  gameStore.initGame(10)

  // Initialize questions
  questionsStore.init('pop', 'easy')

  try {
    // Try to load questions (might fail in demo mode)
    await questionsStore.loadQuestions()
  } catch {
    console.warn('Demo mode: Could not load actual questions')

    // Set mock data for demo purposes
    questionsStore.$patch({
      currentQuestion: {
        question: 'Welcher Künstler hat "Thriller" veröffentlicht?',
        options: ['Michael Jackson', 'Madonna', 'Prince', 'Whitney Houston'],
        correctAnswer: 'Michael Jackson'
      },
      currentOptions: ['Michael Jackson', 'Madonna', 'Prince', 'Whitney Houston']
    })
  }
})

// Actions
const addPoints = () => {
  gameStore.updatePoints(100, 50)
}

const incrementAnswer = () => {
  gameStore.incrementCorrectAnswers()
}

const checkAnswer = (selectedAnswer) => {
  const isCorrect = currentQuestion.value?.correctAnswer === selectedAnswer
  gameStore.setAnswer(isCorrect)

  if (isCorrect) {
    gameStore.updatePoints(100, 50)
  }
}

const loadNewQuestion = async () => {
  gameStore.prepareNextQuestion()

  try {
    await questionsStore.selectRandomQuestion()
  } catch {
    console.warn('Demo mode: Using mock question')
    // Keep using the same question in demo mode
  }
}

const resetGame = () => {
  gameStore.resetGameState()
  questionsStore.clearStore()

  // Re-initialize with mock data for demo
  questionsStore.$patch({
    currentQuestion: {
      question: 'Welcher Künstler hat "Thriller" veröffentlicht?',
      options: ['Michael Jackson', 'Madonna', 'Prince', 'Whitney Houston'],
      correctAnswer: 'Michael Jackson'
    },
    currentOptions: ['Michael Jackson', 'Madonna', 'Prince', 'Whitney Houston']
  })
}
</script>
