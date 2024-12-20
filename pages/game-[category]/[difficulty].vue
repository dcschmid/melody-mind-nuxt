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
                                @select-answer="selectAnswer"
                                @use-fifty-fifty="useFiftyFiftyJoker(currentQuestion)"
                                @use-audience="useAudienceJoker(currentQuestion)"
                                @use-phone="usePhoneJoker(currentQuestion)" />
                        </div>
                        <!-- Solution View -->
                        <GameSolutionView 
                            v-else-if="currentQuestion"
                            :key="'solution'"
                            :is-correct-answer="isCorrectAnswer"
                            :latest-bonus="latestBonus"
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
@mixin section-heading {
    font-size: clamp(1.2rem, 3.5vw, 1.5rem);
    color: var(--text-color);
    text-align: center;
    margin-bottom: var(--padding-medium);
}

.game-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--padding-small);
    padding: 0 var(--padding-small);

    .header-left {
        text-align: left;

        h1 {
            font-size: clamp(1.2rem, 4vw, 1.8rem);
            color: var(--text-color);
            margin: 0;
            margin-bottom: var(--padding-small);
        }

        .round-counter {
            font-size: clamp(1.1rem, 3.5vw, 1.5rem);
            color: var(--text-color);
            margin: 0;
            font-weight: 600;
        }
    }

    .header-right {
        display: flex;
        align-items: flex-start;
        font-size: clamp(1.2rem, 3vw, 1.8rem);
    }
}

.difficulty {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-medium);
    box-shadow: var(--box-shadow);
    border: 1px solid rgb(255 255 255 / 10%);
}

.question {
    h2 {
        font-size: clamp(1.2rem, 3.5vw, 1.5rem);
        text-align: center;
        margin-bottom: var(--padding-medium);
    }
}

.options {
    display: flex;
    flex-direction: column;
    gap: var(--padding-small);
    width: 100%;
    margin-bottom: var(--padding-medium);
}

.option-button {
    position: relative;
    overflow: hidden;
    isolation: isolate;
    font-weight: 600;
    font-size: clamp(1rem, 2.5vw, 1.25rem);
    padding: var(--padding-small) var(--padding-medium);

    &::before {
        content: '';
        position: absolute;
        inset: 0;
        background: var(--highlight-color);
        opacity: 0;
        transition: opacity var(--transition-speed);
        z-index: -1;
    }

    &:hover::before,
    &:focus-visible::before {
        opacity: 0.2;
    }

    &:hover {
        transform: translateY(-2px);
        box-shadow: var(--box-shadow-hover);
    }
}

.jokers-section {
    display: flex;
    flex-direction: column;
    align-items: center;

    .joker-buttons {
        display: flex;
        gap: var(--padding-medium);
        margin: var(--padding-small) 0;

        @media (width >=768px) {
            gap: var(--padding-large);
        }
    }

    @media (width >=768px) {
        margin: 0;
    }
}

.joker-button {
    border-radius: 50%;
    background: var(--primary-color);
    transition: all var(--transition-speed);
    padding: 1rem;

    .icon {
        transition: color var(--transition-speed);
    }

    &:not(:disabled):hover {
        transform: translateY(-2px);
        background: var(--highlight-color);
    }

    &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    &.disabled {
        opacity: 0.5;
        cursor: not-allowed;
        background: var(--surface-color);
        border: 1px solid rgb(255 255 255 / 10%);
        color: rgb(255 255 255 / 50%);
    }
}

.joker-count {
    font-size: clamp(0.875rem, 3vw, 1rem);
    color: var(--text-color);
    opacity: 0.8;
}

.game-end-screen {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--padding-large);

    .end-content {
        background: var(--surface-color);
        border-radius: var(--border-radius);
        padding: var(--padding-large);
        box-shadow: var(--box-shadow);
        border: 1px solid rgb(255 255 255 / 10%);
        max-width: 600px;
        width: 100%;
        animation: slideUp 0.5s var(--transition-bounce);
    }

    .end-header {
        text-align: center;
        margin-bottom: var(--padding-large);

        h2 {
            font-size: clamp(1.5rem, 5vw, 2.5rem);
            margin-bottom: var(--padding-large);
            background: linear-gradient(to right, var(--primary-color), var(--highlight-color));
            -webkit-background-clip: text;
            color: transparent;
        }
    }

    .final-score-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--padding-large);

        @media (min-width: 768px) {
            flex-direction: row;
            justify-content: center;
        }
    }

    .score-circle {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary-color), var(--highlight-color));
        padding: 4px;
        animation: pulse 2s infinite;

        .score-inner {
            width: 100%;
            height: 100%;
            background: var(--surface-color);
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .points {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(to right, var(--primary-color), var(--highlight-color));
            -webkit-background-clip: text;
            color: transparent;
        }

        .points-label {
            font-size: var(--body-font-size);
            color: var(--text-color);
        }
    }

    .stats {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);

        .stat-item {
            background: rgb(255 255 255 / 5%);
            padding: var(--padding-medium);
            border-radius: var(--border-radius);
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .stat-label {
            font-size: 0.9rem;
            opacity: 0.7;
        }

        .stat-value {
            font-size: 1.2rem;
            font-weight: 600;
        }
    }

    .reward-section {
        text-align: center;
        margin: var(--padding-large) 0;
        padding: var(--padding-large);
        border-radius: var(--border-radius);
        background: rgb(255 255 255 / 5%);

        &.gold {
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 215, 0, 0.2));
        }

        &.silver {
            background: linear-gradient(135deg, rgba(192, 192, 192, 0.1), rgba(192, 192, 192, 0.2));
        }

        &.bronze {
            background: linear-gradient(135deg, rgba(205, 127, 50, 0.1), rgba(205, 127, 50, 0.2));
        }

        .record-icon {
            margin-bottom: var(--padding-medium);

            .icon {
                filter: drop-shadow(0 0 8px currentColor);
            }
        }

        .reward-text {
            font-size: 1.1rem;
            line-height: 1.6;
        }
    }

    .end-actions {
        display: flex;
        justify-content: center;
        margin-top: var(--padding-large);

        .home-button {
            background: var(--primary-color);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: var(--padding-small);
            padding: var(--padding-medium) var(--padding-large);
            font-size: 1.1rem;
            font-weight: 600;
            transition: all var(--transition-speed);
            border-radius: var(--border-radius);

            &:hover {
                background: var(--primary-dark);
                transform: translateY(-2px);
                box-shadow: var(--box-shadow-hover);
            }
        }
    }

    .share-section {
        margin-top: var(--padding-large);
        text-align: center;

        h3 {
            margin-bottom: var(--padding-medium);
            font-size: 1.2rem;
        }

        .share-buttons {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            justify-content: center;
        }

        .share-button {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 0.5rem;
            color: white;
            cursor: pointer;
            transition: opacity 0.2s;

            &:hover {
                opacity: 0.9;
            }

            &.twitter {
                background-color: #1DA1F2;
            }

            &.telegram {
                background-color: #0088cc;
            }

            &.reddit {
                background-color: #ff4500;
            }

            &.whatsapp {
                background-color: #25D366;
            }

            &.share-api {
                background-color: #666;
            }
        }
    }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(var(--primary-color-rgb), 0.4);
    }

    70% {
        box-shadow: 0 0 0 10px rgba(var(--primary-color-rgb), 0);
    }

    100% {
        box-shadow: 0 0 0 0 rgba(var(--primary-color-rgb), 0);
    }
}

.audience-help {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-large);
    margin: var(--padding-medium) 0;

    h3 {
        font-size: clamp(1.2rem, 3.5vw, 1.5rem);
        margin-bottom: var(--padding-medium);
        text-align: center;
    }

    .audience-bars {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);
        margin: 0 auto;
    }

    .bar-item {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .option-label {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 4px;
    }

    .option-text {
        font-size: 1.25rem;
    }

    .percentage-text {
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .bar-container {
        background: rgb(255 255 255 / 8%);
        border-radius: 4px;
        height: 12px;
        overflow: hidden;
    }

    .bar {
        height: 100%;
        transition: width 1s ease;

        &.high {
            background-color: var(--success-color);
        }

        &.medium {
            background-color: var(--primary-color);
        }

        &.low {
            background-color: var(--error-color);
        }
    }
}

.phone-expert {
    margin: var(--padding-medium) 0;

    h3 {
        @include section-heading;
    }

    .expert-message {
        background: rgb(255 255 255 / 5%);
        border-radius: var(--border-radius);
        padding: var(--padding-medium);
        border: 1px solid rgb(255 255 255 / 10%);
    }

    .expert-header {
        display: flex;
        align-items: center;
        gap: var(--padding-small);
        margin-bottom: var(--padding-medium);
        padding-bottom: var(--padding-small);
        border-bottom: 1px solid rgb(255 255 255 / 10%);

        .phone-icon {
            font-size: clamp(1.5rem, 4vw, 2rem);
            color: var(--primary-color);
        }

        .expert-name {
            font-size: clamp(1.1rem, 3vw, 1.3rem);
            font-weight: 600;
            color: var(--text-color);
        }
    }

    .message-content {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);
    }

    .confidence-bar-container {
        display: flex;
        flex-direction: column;
        gap: var(--padding-small);
    }

    .confidence-bar {
        background: rgb(255 255 255 / 10%);
        border-radius: var(--border-radius);
        height: 8px;
        overflow: hidden;
        position: relative;

        .confidence-level {
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: var(--confidence);
            transition: width 1s var(--transition-bounce);
        }

        &.high .confidence-level {
            background: linear-gradient(90deg, var(--success-color), var(--highlight-color));
        }

        &.medium .confidence-level {
            background: linear-gradient(90deg, var(--primary-color), var(--highlight-color));
        }

        &.low .confidence-level {
            background: linear-gradient(90deg, var(--error-color), var(--secondary-color));
        }
    }
}

.confidence-text {
    font-size: clamp(0.9rem, 2.5vw, 1rem);
    color: var(--text-color);
    opacity: 0.8;
    text-align: right;
}

.trivia-box {
    background: var(--background-secondary);
    border-radius: 12px;
    margin-top: 2rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    h3 {
        color: var(--primary-color);
        margin: 0 0 12px 0;
        font-size: 1.2em;
        text-align: center;
    }

    p {
        margin: 0;
        line-height: 1.6;
        color: var(--text-color);
        font-size: 1em;
    }
}

.points-display {
    position: relative;
    display: flex;
    align-items: center;
    gap: var(--padding-small);
}

.points-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.points {
    font-size: clamp(1.2rem, 3vw, 1.8rem);
    font-weight: bold;
    color: var(--text-color);
    transition: transform 0.3s ease;

    &.points-update {
        transform: scale(1.2);
        color: var(--highlight-color);
    }
}

.points-label {
    font-size: var(--body-font-size);
    color: var(--text-color);
}

.bonus-indicator {
    position: absolute;
    top: -40px;
    right: 0;
    background: rgba(0, 0, 0, 0.8);
    padding: 8px 12px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);

    .bonus-total {
        color: #FFD700;
        font-weight: bold;
        font-size: 1.2em;
        text-align: center;
        margin-bottom: 4px;
    }

    .bonus-breakdown {
        display: flex;
        gap: 8px;
        font-size: 0.8em;

        .time {
            color: var(--highlight-color);
        }
    }
}

.points-breakdown {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 12px;
    margin: 12px 0;

    .points-row {
        display: flex;
        justify-content: space-between;
        padding: 4px 0;

        &:not(:last-child) {
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        &.total {
            font-weight: bold;
            font-size: 1.1em;
            margin-top: 4px;
            padding-top: 8px;
            border-top: 2px solid rgba(255, 255, 255, 0.2);
        }
    }
}

.bonus-enter-active,
.bonus-leave-active {
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.bonus-enter-from {
    opacity: 0;
    transform: translateY(20px) scale(0.8);
}

.bonus-leave-to {
    opacity: 0;
    transform: translateY(-20px) scale(0.8);
}

.points-update {
    animation: pointsPulse 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes pointsPulse {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.2);
        color: var(--highlight-color);
    }

    100% {
        transform: scale(1);
    }
}

// Slide transition
.slide-enter-active,
.slide-leave-active {
    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-enter-from {
    opacity: 0;
    transform: translateX(30px);
}

.slide-leave-to {
    opacity: 0;
    transform: translateX(-30px);
}

// Optional: Add some base styling to prevent layout shifts
.game-content,
.game-end-screen {
    position: relative;
    min-height: 400px; /* Adjust based on your content */
}

.share-section {
    margin-top: var(--padding-large);
    text-align: center;

    h3 {
        margin-bottom: var(--padding-medium);
        font-size: 1.2rem;
    }

    .share-buttons {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        justify-content: center;
    }

    .share-button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.5rem;
        color: white;
        cursor: pointer;
        transition: opacity 0.2s;

        &:hover {
            opacity: 0.9;
        }

        &.twitter {
            background-color: #1DA1F2;
        }

        &.telegram {
            background-color: #0088cc;
        }

        &.reddit {
            background-color: #ff4500;
        }

        &.whatsapp {
            background-color: #25D366;
        }

        &.share-api {
            background-color: #666;
        }
    }
}

.phone-expert {
    margin: var(--padding-medium) 0;

    h3 {
        @include section-heading;
    }

    .expert-message {
        background: rgb(255 255 255 / 5%);
        border-radius: var(--border-radius);
        padding: var(--padding-medium);
        border: 1px solid rgb(255 255 255 / 10%);
    }

    .expert-header {
        display: flex;
        align-items: center;
        gap: var(--padding-small);
        margin-bottom: var(--padding-medium);
        padding-bottom: var(--padding-small);
        border-bottom: 1px solid rgb(255 255 255 / 10%);

        .phone-icon {
            font-size: clamp(1.5rem, 4vw, 2rem);
            color: var(--primary-color);
        }

        .expert-name {
            font-size: clamp(1.1rem, 3vw, 1.3rem);
            font-weight: 600;
            color: var(--text-color);
        }
    }

    .message-content {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);
    }

    .confidence-bar-container {
        display: flex;
        flex-direction: column;
        gap: var(--padding-small);
        margin: var(--padding-medium) 0;
    }

    .confidence-bar {
        background: rgb(255 255 255 / 10%);
        border-radius: var(--border-radius);
        height: 8px;
        overflow: hidden;
        position: relative;

        .confidence-level {
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: var(--confidence);
            transition: width 1s var(--transition-bounce);
        }

        &.high .confidence-level {
            background: linear-gradient(90deg, var(--success-color), var(--highlight-color));
        }

        &.medium .confidence-level {
            background: linear-gradient(90deg, var(--primary-color), var(--highlight-color));
        }

        &.low .confidence-level {
            background: linear-gradient(90deg, var(--error-color), var(--secondary-color));
        }
    }
}

.confidence-text {
    font-size: clamp(0.9rem, 2.5vw, 1rem);
    color: var(--text-color);
    opacity: 0.8;
    text-align: right;
}

.trivia-box {
    background: var(--background-secondary);
    border-radius: 12px;
    margin-top: 2rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    h3 {
        color: var(--primary-color);
        margin: 0 0 12px 0;
        font-size: 1.2em;
        text-align: center;
    }

    p {
        margin: 0;
        line-height: 1.6;
        color: var(--text-color);
        font-size: 1em;
    }
}

.points-display {
    position: relative;
    display: flex;
    align-items: center;
    gap: var(--padding-small);
}

.points-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.points {
    font-size: clamp(1.2rem, 3vw, 1.8rem);
    font-weight: bold;
    color: var(--text-color);
    transition: transform 0.3s ease;

    &.points-update {
        transform: scale(1.2);
        color: var(--highlight-color);
    }
}

.points-label {
    font-size: var(--body-font-size);
    color: var(--text-color);
}

.bonus-indicator {
    position: absolute;
    top: -40px;
    right: 0;
    background: rgba(0, 0, 0, 0.8);
    padding: 8px 12px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);

    .bonus-total {
        color: #FFD700;
        font-weight: bold;
        font-size: 1.2em;
        text-align: center;
        margin-bottom: 4px;
    }

    .bonus-breakdown {
        display: flex;
        gap: 8px;
        font-size: 0.8em;

        .time {
            color: var(--highlight-color);
        }
    }
}

.points-breakdown {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 12px;
    margin: 12px 0;

    .points-row {
        display: flex;
        justify-content: space-between;
        padding: 4px 0;

        &:not(:last-child) {
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        &.total {
            font-weight: bold;
            font-size: 1.1em;
            margin-top: 4px;
            padding-top: 8px;
            border-top: 2px solid rgba(255, 255, 255, 0.2);
        }
    }
}

.bonus-enter-active,
.bonus-leave-active {
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.bonus-enter-from {
    opacity: 0;
    transform: translateY(20px) scale(0.8);
}

.bonus-leave-to {
    opacity: 0;
    transform: translateY(-20px) scale(0.8);
}

.points-update {
    animation: pointsPulse 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes pointsPulse {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.2);
        color: var(--highlight-color);
    }

    100% {
        transform: scale(1);
    }
}

// Slide transition
.slide-enter-active,
.slide-leave-active {
    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-enter-from {
    opacity: 0;
    transform: translateX(30px);
}

.slide-leave-to {
    opacity: 0;
    transform: translateX(-30px);
}

// Optional: Add some base styling to prevent layout shifts
.game-content,
.game-end-screen {
    position: relative;
    min-height: 400px; /* Adjust based on your content */
}

.share-section {
    margin-top: var(--padding-large);
    text-align: center;

    h3 {
        margin-bottom: var(--padding-medium);
        font-size: 1.2rem;
    }

    .share-buttons {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        justify-content: center;
    }

    .share-button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.5rem;
        color: white;
        cursor: pointer;
        transition: opacity 0.2s;

        &:hover {
            opacity: 0.9;
        }

        &.twitter {
            background-color: #1DA1F2;
        }

        &.telegram {
            background-color: #0088cc;
        }

        &.reddit {
            background-color: #ff4500;
        }

        &.whatsapp {
            background-color: #25D366;
        }

        &.share-api {
            background-color: #666;
        }
    }
}
</style>
