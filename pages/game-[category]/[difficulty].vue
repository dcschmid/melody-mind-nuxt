<template>
    <NuxtLayout name="default" :show-header="false" :show-menu="false">
        <main>
            <Transition name="slide" mode="out-in">
                <!-- Game Content -->
                <div v-if="!gameFinished" class="game-content" :key="'game'">
                    <Transition name="slide" mode="out-in">
                        <!-- Question View -->
                        <div v-if="!showSolution" :key="'question'">
                            <GameHeader :category-name="currentCategoryData?.name || category"
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
                        <GameSolutionView v-else-if="currentQuestion" :key="'solution'"
                            :is-correct-answer="isCorrectAnswer" :latest-bonus="latestBonus" :question="currentQuestion"
                            :artist="currentArtist" :is-playing="isPlaying" :audio-loaded="audioLoaded"
                            :is-buffering="isBuffering" :progress="progress" @toggle-play="togglePlay"
                            @next="nextQuestion" />
                    </Transition>
                </div>
                <!-- Game Over Screen -->
                <div v-else class="game-end-screen" :key="'gameover'">
                    <div class="end-content">
                        <div class="end-header">
                            <h2>{{ t('game.gameOver.title') }}</h2>
                            <div class="final-score-container">
                                <div class="score-circle">
                                    <div class="score-inner">
                                        <span class="points">{{ totalPoints }}</span>
                                        <span class="points-label">{{ t('game.points_label') }}</span>
                                    </div>
                                </div>
                                <div class="stats">
                                    <div class="stat-item">
                                        <span class="stat-label">{{ t('game.gameOver.correctAnswers') }}</span>
                                        <span class="stat-value">{{ correctAnswers }} / {{ maxQuestions }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="reward-section" :class="recordClass">
                            <div class="record-icon">
                                <Icon v-if="earnedRecord" :name="recordIcon" size="64" />
                            </div>
                            <p class="reward-text">
                                {{ resultMessage }}
                            </p>
                        </div>

                        <!-- Im Game Over Screen, nach der final-score-container div -->
                        <div class="share-section">
                            <h3>{{ t('game.results.share.title') }}</h3>
                            <div class="share-buttons">
                                <button class="share-button twitter"
                                    @click="shareToTwitter({ totalPoints, correctAnswers, maxQuestions })">
                                    <Icon name="mdi:twitter" size="24" />
                                    <span>{{ t('game.results.share.buttons.twitter') }}</span>
                                </button>

                                <button class="share-button telegram"
                                    @click="shareToTelegram({ totalPoints, correctAnswers, maxQuestions })">
                                    <Icon name="mdi:telegram" size="24" />
                                    <span>{{ t('game.results.share.buttons.telegram') }}</span>
                                </button>

                                <button class="share-button reddit"
                                    @click="shareToReddit({ totalPoints, correctAnswers, maxQuestions })">
                                    <Icon name="mdi:reddit" size="24" />
                                    <span>{{ t('game.results.share.buttons.reddit') }}</span>
                                </button>

                                <button v-if="isMobile" class="share-button whatsapp"
                                    @click="shareToWhatsApp({ totalPoints, correctAnswers, maxQuestions })">
                                    <Icon name="mdi:whatsapp" size="24" />
                                    <span>{{ t('game.results.share.buttons.whatsapp') }}</span>
                                </button>

                                <button v-if="canShare" class="share-button share-api"
                                    @click="shareViaAPI({ totalPoints, correctAnswers, maxQuestions })">
                                    <Icon name="material-symbols:share" size="24" />
                                    <span>{{ t('game.results.share.buttons.share') }}</span>
                                </button>
                            </div>
                        </div>

                        <div class="end-actions">
                            <NuxtLink :to="$localePath('gamehome')" class="button home-button">
                                <Icon name="material-symbols:home" size="36" />
                                <span>{{ t('game.gameOver.backToMenu') }}</span>
                            </NuxtLink>
                        </div>
                    </div>
                </div>
            </Transition>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { authClient } from '~/lib/auth-client'

// Require authentication to access this page
definePageMeta({ middleware: 'auth' })

// Initialize core utilities
const session = authClient.useSession()
const route = useRoute()
const { t, locale } = useI18n()

// --- Route Parameters ---
// Extract category and difficulty from URL parameters
const category = route.params.category as string
const difficulty = route.params.difficulty as string

// --- Load Category Data ---
// Import category data based on current locale
const categories = await import(`~/json/${locale.value}_categories.json`)
const currentCategoryData = categories.default.find((cat: any) => cat.slug === category)

// --- Initialize Game Composables ---
// Core game mechanics
const questions = useQuestions(category, difficulty)     // Question management
const jokers = useJokers(difficulty)                    // Lifeline/joker system
const gameState = useGameState(questions.maxQuestions.value)  // Game state tracking
const { points } = gameState
const artist = useArtist()                             // Artist/music info handling
const timeBonus = useTimeBonus()                       // Time-based bonus system

// Game rewards and achievements
const gameRewards = useGameRewards({
    allQuestionsCorrect: gameState.allQuestionsCorrect,
    correctAnswers: gameState.correctAnswers,
    maxQuestions: questions.maxQuestions
})

// Audio playback management
const gameAudio = useGameAudio()

// Results and scoring system
const gameResults = useGameResults({
    thresholds: { gold: 1, silver: 0.75, bronze: 0.5 }
})

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
watch(() => questions.usedQuestions.value.length, (newLength) => {
    if (newLength > questions.maxQuestions.value) {
        gameState.finishGame()
        // Save final game results
        gameResults.saveGameResults(
            category,
            gameState.totalPoints.value,
            gameState.correctAnswers.value,
            questions.maxQuestions.value,
            gameState.allQuestionsCorrect.value,
            session.value?.data?.user?.id
        )
    }
})

// Cleanup audio when leaving page
onBeforeRouteLeave(() => {
    gameAudio.cleanup()
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
    phoneExpertConfidence,
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
    formattedPoints,   // Formatted score display
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

// Rewards and sharing exports
const { recordIcon, recordClass } = gameRewards          // Achievement indicators
const { resultMessage, earnedRecord } = gameResults      // Game results
const { isMobile, canShare, shareViaAPI, shareToTwitter,
    shareToWhatsApp, shareToTelegram, shareToReddit } = sharing  // Sharing options
</script>

<style lang="scss" scoped>
.game-content {
    margin: 0 auto;
    padding: 2rem;

    .question {
        background: var(--surface-color);
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        margin-top: 3rem;
        margin-bottom: 2rem;
        text-align: center;

        h2 {
            font-size: 1.5rem;
            color: var(--text-color);
            margin-bottom: 1rem;
        }
    }

    .options {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 2rem;

        button {
            background: linear-gradient(145deg, var(--surface-color), var(--surface-color-dark));
            border: 2px solid var(--border-color);
            border-radius: 0.75rem;
            padding: 1rem 1.5rem;
            font-size: 1.1rem;
            color: var(--text-color);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;

            &:hover:not(:disabled) {
                transform: translateY(-2px);
                border-color: var(--primary-color);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);

                &::before {
                    opacity: 1;
                }
            }

            &::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.05), transparent);
                opacity: 0;
                transition: opacity 0.3s ease;
            }

            &:disabled {
                opacity: 0.7;
                cursor: not-allowed;
            }
        }
    }

    .jokers {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 2rem;
        padding: 1rem;
        background: var(--surface-color-light);
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);

        .joker-button {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
            padding: 1rem;
            width: 100px;
            height: 100px;
            border-radius: 1rem;
            background: linear-gradient(145deg, var(--surface-color), var(--surface-color-dark));
            border: 2px solid var(--border-color);
            transition: all 0.3s ease;

            .icon {
                font-size: 2rem;
                color: var(--primary-color);
                transition: transform 0.3s ease;
            }

            .label {
                font-size: 0.8rem;
                color: var(--text-color-light);
                text-align: center;
                transition: color 0.3s ease;
            }

            &:hover:not(:disabled) {
                transform: translateY(-3px);
                border-color: var(--primary-color);
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);

                .icon {
                    transform: scale(1.1);
                    color: var(--primary-color-light);
                }

                .label {
                    color: var(--text-color);
                }
            }

            &:disabled {
                opacity: 0.6;
                cursor: not-allowed;

                .icon {
                    color: var(--text-color-lighter);
                }

                .label {
                    color: var(--text-color-lighter);
                }
            }
        }
    }

    .jokers-remaining {
        text-align: center;
        margin-top: 1rem;
        font-size: 0.9rem;
        color: var(--text-color-light);
    }
}

// Ensure smooth transitions
.slide-enter-active,
.slide-leave-active {
    transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
    opacity: 0;
    transform: translateX(20px);
}
</style>
