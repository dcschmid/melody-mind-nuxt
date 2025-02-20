<template>
    <NuxtLayout name="default" :show-header="false" :show-menu="false">
        <main>
            <Transition name="slide" mode="out-in">
                <!-- Game Content -->
                <div v-if="!gameFinished" class="game-content" :key="'game'">
                    <Transition name="slide" mode="out-in">
                        <!-- Question View -->
                        <div v-if="!showSolution" :key="'question'">
                            <GameHeader :category-name="currentCategoryData.value?.name || category"
                                :current-round="usedQuestions.length" :max-rounds="maxQuestions" :points="points"
                                :is-animating="isAnimating" :show-bonus="showBonus" :latest-bonus="latestBonus" />

                            <GameQuestionView v-if="currentQuestion" :question="currentQuestion"
                                :current-options="currentOptions" :hidden-options="hiddenOptions"
                                :disabled="showSolution" :remaining-jokers="remainingJokers"
                                :joker-used-for-current-question="jokerUsedForCurrentQuestion"
                                :phone-expert-opinion="phoneExpertOpinion" :audience-opinion="audienceHelp"
                                @select-answer="selectAnswer" @use-fifty-fifty="useFiftyFiftyJoker(currentQuestion)"
                                @use-audience="useAudienceJoker(currentQuestion)"
                                @use-phone="usePhoneJoker(currentQuestion)" />
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
                            @toggle-play="togglePlay"
                            @next="nextQuestion"
                        />
                    </Transition>
                </div>
                <!-- Game Over Screen -->
                <GameOverScreen v-else :total-points="totalPoints" :correct-answers="correctAnswers"
                    :max-questions="maxQuestions" :earned-record="currentReward !== 'none'" :record-icon="recordIcon"
                    :record-class="recordClass" :result-message="currentResultMessage" :key="'gameover'" />
            </Transition>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { watch, nextTick, computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSeoMeta, useRequestURL, useRoute, useJsonld } from '#imports'
import GameOverScreen from '~/components/game/GameOverScreen.vue';
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
    title: computed(() => t('game.meta.title', { 
        category: currentCategoryData.value?.name || category,
        difficulty: difficulty 
    })),
    description: computed(() => t('game.meta.description', { 
        category: currentCategoryData.value?.name || category,
        difficulty: difficulty 
    })),
    ogTitle: computed(() => t('game.meta.title', { 
        category: currentCategoryData.value?.name || category,
        difficulty: difficulty 
    })),
    ogDescription: computed(() => t('game.meta.description', { 
        category: currentCategoryData.value?.name || category,
        difficulty: difficulty 
    })),
    ogType: 'website',
    robots: 'noindex, follow' // Spiel-Seiten sollten nicht indexiert werden
})

// JSON-LD
useJsonld({
    '@context': 'https://schema.org',
    '@type': 'VideoGame',
    name: t('game.meta.title', { 
        category: route.params.category, 
        difficulty: route.params.difficulty 
    }),
    description: t('game.meta.description', { 
        category: route.params.category, 
        difficulty: route.params.difficulty 
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
            difficulty: route.params.difficulty 
        })
    },
    audience: {
        '@type': 'Audience',
        audienceType: 'Music Enthusiasts'
    },
})

// --- Initialize Game Composables ---
// Core game mechanics
const questions = useQuestions(category, difficulty)     // Question management
const jokers = useJokers(difficulty)                    // Lifeline/joker system
const gameState = useGameState(questions.maxQuestions.value)  // Game state tracking
const { points } = gameState
const artist = useArtist()                             // Artist/music info handling
const timeBonus = useTimeBonus()                       // Time-based bonus system
const gameScore = useGameScore()
const { resultMessage, earnedRecord, calculateReward, getResultMessage, saveGameResults } = useGameResults()

// Audio playback management
const gameAudio = useGameAudio()

// Social sharing functionality
const sharing = useShare({ currentCategoryData, category, difficulty })

// Navigation utilities
const { scrollToTop } = useGameNavigation({
    usedQuestions: questions.usedQuestions,
    maxQuestions: questions.maxQuestions,
    gameFinished: gameState.gameFinished,
    showSolution: gameState.showSolution
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
watch(() => questions.usedQuestions.value.length, async (newLength) => {
    if (newLength > questions.maxQuestions.value) {
        // Set game as finished to show end screen
        gameState.finishGame()
    }
})

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
        case 'gold': return 'material-symbols:workspace-premium'
        case 'silver': return 'material-symbols:stars'
        case 'bronze': return 'material-symbols:military-tech'
        default: return ''
    }
})

const recordClass = computed(() => {
    return currentReward.value !== 'none' ? 'new-record' : ''
})

// --- Template Exports ---
// Destructure and export required properties for the template
const {
    currentQuestion,    // Current active question
    currentOptions,     // Available answer options
    maxQuestions,       // Total questions in game
    usedQuestions      // Questions already answered
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
    usePhoneJoker
} = jokers

// Game state exports
const {
    showSolution,      // Whether to show answer
    isCorrectAnswer,   // If last answer was correct
    gameFinished,      // Game completion status
    correctAnswers,    // Total correct answers
    totalPoints,       // Total score
    isAnimating,       // Animation state
    showBonus,         // Bonus display state
    latestBonus        // Latest bonus earned
} = gameState

// Audio player exports
const {
    isPlaying,         // Playback state
    audioLoaded,       // Audio loading state
    isBuffering,       // Buffer state
    progress,          // Playback progress
    togglePlay         // Play/pause function
} = gameAudio

const { currentArtist } = artist  // Current artist information
</script>

<style lang="scss" scoped>
.game-content {
    margin: 0 auto;

    .question {
        background: var(--surface-color);
        padding: var(--padding-large);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);
        margin: var(--padding-large) 0;
        text-align: center;

        h2 {
            font-size: var(--font-size-responsive-2xl);
            font-weight: var(--font-weight-bold);
            color: var(--text-color);
            margin-bottom: var(--padding-medium);
            line-height: var(--line-height-tight);
        }
    }

    .options {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);
        margin-bottom: var(--padding-large);

        button {
            background: var(--surface-color);
            border: var(--border-width) solid var(--surface-color-light);
            border-radius: var(--border-radius);
            padding: var(--padding-medium);
            font-size: var(--font-size-responsive-md);
            color: var(--text-color);
            transition: all var(--transition-speed) var(--transition-bounce);
            position: relative;
            overflow: hidden;

            &:hover:not(:disabled) {
                transform: translateY(-2px);
                border-color: var(--primary-color);
                box-shadow: var(--box-shadow-hover);
            }

            &:disabled {
                opacity: var(--opacity-disabled);
                cursor: not-allowed;
            }
        }
    }

    .jokers {
        display: flex;
        justify-content: center;
        gap: var(--padding-medium);
        margin-top: var(--padding-large);
        padding: var(--padding-medium);
        background: var(--surface-color-light);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);

        .joker-button {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: var(--padding-small);
            padding: var(--padding-medium);
            min-width: var(--min-touch-target);
            min-height: var(--min-touch-target);
            border-radius: var(--border-radius);
            background: var(--surface-color);
            border: var(--border-width) solid var(--surface-color-light);
            transition: all var(--transition-speed) var(--transition-bounce);

            .icon {
                font-size: var(--font-size-responsive-xl);
                color: var(--primary-color);
                transition: transform var(--transition-speed) var(--transition-bounce);
            }

            .label {
                font-size: var(--font-size-base);
                color: var(--text-secondary);
                text-align: center;
            }

            &:hover:not(:disabled) {
                transform: translateY(-2px);
                border-color: var(--primary-color);
                box-shadow: var(--box-shadow-hover);

                .icon {
                    transform: scale(1.1);
                    color: var(--primary-color-light);
                }

                .label {
                    color: var(--text-color);
                }
            }

            &:disabled {
                opacity: var(--opacity-disabled);
                cursor: not-allowed;
            }
        }
    }

    .jokers-remaining {
        text-align: center;
        margin-top: var(--padding-medium);
        font-size: var(--font-size-base);
        color: var(--text-secondary);
    }
}

.next-button {
    display: flex;
    justify-content: center;
    align-items: center;
    width: auto;
    min-width: var(--min-touch-target);
    margin: var(--padding-medium) auto;
    padding: var(--padding-medium) var(--padding-large);
    font-size: var(--font-size-responsive-md);
    font-weight: var(--font-weight-semibold);
    
    .button-text {
        font-size: var(--font-size-responsive-md);
        margin-right: var(--padding-small);
    }
}

// Transitions
.slide-enter-active,
.slide-leave-active {
    transition: all var(--transition-speed) var(--transition-bounce);
}

.slide-enter-from,
.slide-leave-to {
    opacity: 0;
    transform: translateX(20px);
}

@media (prefers-reduced-motion: reduce) {
    .game-content button,
    .joker-button,
    .next-button,
    .slide-enter-active,
    .slide-leave-active {
        transition: none;
        transform: none;
    }
}
</style>
