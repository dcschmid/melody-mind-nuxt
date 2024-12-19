<template>
    <NuxtLayout name="default" :show-header="false" :show-menu="false">
        <main>
            <Transition name="slide" mode="out-in">
                <!-- Game Content -->
                <div v-if="!gameFinished" class="game-content" :key="'game'">
                    <Transition name="slide" mode="out-in">
                        <!-- Question View -->
                        <div v-if="!showSolution" :key="'question'">
                            <div class="game-header">
                                <div class="header-left">
                                    <h1>{{ currentCategoryData?.name || category }}</h1>
                                    <p class="round-counter">{{ t('game.round', {
                                        current: usedQuestions.length, max:
                                            maxQuestions
                                    }) }}</p>
                                </div>
                                <div class="header-right">
                                    <div class="points-display">
                                        <div class="points-container">
                                            <span class="points" :class="{ 'points-update': isAnimating }">
                                                {{ formattedPoints }}
                                            </span>
                                            <span class="points-label">{{ t('game.points_label') }}</span>
                                        </div>
                                        <transition name="bonus">
                                            <div v-if="showBonus" class="bonus-indicator">
                                                <div class="bonus-total">+{{ latestBonus.base }}</div>
                                                <div class="bonus-breakdown">
                                                    <span class="time">+{{ latestBonus.time }} Bonus</span>
                                                </div>
                                            </div>
                                        </transition>
                                    </div>
                                </div>
                            </div>

                            <div v-if="currentQuestion" class="question-container">
                                <!-- Frage -->
                                <div class="question">
                                    <h2>{{ currentQuestion.question }}</h2>
                                </div>

                                <!-- Antwortmöglichkeiten -->
                                <div class="options">
                                    <button v-for="(option, index) in currentOptions" :key="index"
                                        class="button option-button"
                                        :class="{ 'hidden': hiddenOptions.includes(option) }"
                                        @click="selectAnswer(option)"
                                        :disabled="showSolution || hiddenOptions.includes(option)">
                                        {{ option }}
                                    </button>
                                </div>

                                <!-- Telefonjoker Antwort -->
                                <div v-if="phoneExpertOpinion" class="phone-expert">
                                    <h3>{{ t('game.expert.title') }}</h3>
                                    <div class="expert-message">
                                        <div class="expert-header">
                                            <Icon name="material-symbols:phone" class="phone-icon" />
                                            <span class="expert-name">{{ phoneExpertOpinion.expert }}</span>
                                        </div>
                                        <div class="message-content">
                                            <p class="expert-answer">{{ phoneExpertOpinion.message }}</p>
                                            <div class="confidence-bar-container">
                                                <div class="confidence-bar"
                                                    :style="{ '--confidence': phoneExpertConfidence + '%' }" :class="{
                                                        'high': phoneExpertConfidence >= 80,
                                                        'medium': phoneExpertConfidence >= 60 && phoneExpertConfidence < 80,
                                                        'low': phoneExpertConfidence < 60
                                                    }">
                                                    <div class="confidence-level"></div>
                                                </div>
                                                <span class="confidence-text">{{ phoneExpertConfidence }}% {{
                                                    t('game.confidence') }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Publikumsjoker Ergebnis -->
                                <div v-if="Object.keys(audienceHelp).length > 0" class="audience-help">
                                    <h3>{{ t('game.audienceOpinion') }}</h3>
                                    <div class="audience-bars">
                                        <div v-for="(percentage, option) in audienceHelp" :key="option"
                                            class="bar-item">
                                            <div class="option-label">
                                                <div class="option-text">{{ option }}</div>
                                                <div class="percentage-text">{{ percentage }}%</div>
                                            </div>
                                            <div class="bar-container">
                                                <div class="bar" :style="{ width: `${percentage}%` }" :class="{
                                                    'high': percentage >= 70,
                                                    'medium': percentage >= 40 && percentage < 70,
                                                    'low': percentage < 40
                                                }">
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Joker Section -->
                                <div class="jokers-section">
                                    <div class="joker-buttons">
                                        <!-- 50:50 Joker -->
                                        <button class="button joker-button" @click="useFiftyFiftyJoker(currentQuestion)"
                                            :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                                            :aria-label="$t('game.jokers.fiftyFifty')"
                                            :class="{ 'disabled': remainingJokers === 0 || jokerUsedForCurrentQuestion }">
                                            <Icon name="material-symbols:balance" size="30" />
                                        </button>

                                        <!-- Publikumsjoker -->
                                        <button class="button joker-button" @click="useAudienceJoker(currentQuestion)"
                                            :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                                            :aria-label="$t('game.jokers.audience')"
                                            :class="{ 'disabled': remainingJokers === 0 || jokerUsedForCurrentQuestion }">
                                            <Icon name="formkit:people" size="30" />
                                        </button>

                                        <!-- Telefonjoker -->
                                        <button class="button joker-button" @click="usePhoneJoker(currentQuestion)"
                                            :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                                            :aria-label="$t('game.jokers.phone')"
                                            :class="{ 'disabled': remainingJokers === 0 || jokerUsedForCurrentQuestion }">
                                            <Icon name="gg:phone" size="30" />
                                        </button>
                                    </div>
                                    <span class="joker-count">{{ t('game.jokers.remaining', { count: remainingJokers })
                                        }}</span>
                                </div>
                            </div>
                        </div>
                        <!-- Solution View -->
                        <div v-else :key="'solution'" class="solution-container">
                            <!-- Ergebnis-Banner -->
                            <div class="result-banner" :class="{ 'correct': isCorrectAnswer }">
                                <div class="result-header">
                                    <Icon
                                        :name="isCorrectAnswer ? 'material-symbols:check-circle' : 'material-symbols:cancel'"
                                        class="result-icon" size="28" />
                                    <h2>{{ isCorrectAnswer ? t('game.correct') : t('game.wrong') }}</h2>
                                </div>
                                <div v-if="isCorrectAnswer" class="points-breakdown">
                                    <div class="points">
                                        {{ t('game.points', { base: latestBonus.base, time: latestBonus.time }) }}
                                    </div>
                                </div>
                                <div v-else class="points"> 0 {{ t('game.points_label') }}</div>

                                <div class="correct-answer">
                                    <span class="label">{{ t('game.correctAnswer') }}</span>
                                    <div class="text">{{ currentQuestion.correctAnswer }}</div>
                                </div>
                            </div>

                            <!-- Content Container -->
                            <div class="content-wrapper">

                                <!-- Album Info -->
                                <div v-if="currentArtist" class="album-box">
                                    <div class="cover-wrapper">
                                        <img :src="currentArtist.coverSrc"
                                            :alt="`${currentArtist.artist} - ${currentArtist.album}`" />
                                    </div>
                                    <div class="player-info-wrapper">
                                        <div class="audio-player">
                                            <button @click="togglePlay" class="play-button"
                                                :disabled="!currentArtist?.preview_link"
                                                :title="currentArtist?.preview_link ? (isPlaying ? t('game.audio.pause') : t('game.audio.play')) : t('game.audio.noAudio')">
                                                <Icon
                                                    :name="isPlaying ? 'material-symbols:pause' : 'material-symbols:play-arrow'"
                                                    size="36" />
                                            </button>
                                            <div class="progress-bar">
                                                <div class="progress"
                                                    :style="{ width: `${(currentTime / duration) * 100}%` }">
                                                </div>
                                            </div>
                                        </div>
                                        <div class="info">
                                            <p class="artist">{{ t('game.album.artist') }}: {{ currentArtist.artist }}
                                            </p>
                                            <p class="year">{{ t('game.album.year') }}: {{ currentArtist.year }}</p>
                                        </div>
                                    </div>
                                    <div class="streaming-links">
                                        <a v-if="currentArtist.spotify_link" :href="currentArtist.spotify_link"
                                            target="_blank" class="stream-link spotify"
                                            :title="$t('game.streaming.spotify')">
                                            <Icon name="mdi:spotify" size="36" />
                                        </a>
                                        <a v-if="currentArtist.apple_music_link" :href="currentArtist.apple_music_link"
                                            target="_blank" class="stream-link apple"
                                            :title="$t('game.streaming.apple')">
                                            <Icon name="mdi:apple" size="36" />
                                        </a>
                                        <a v-if="currentArtist.deezer_link" :href="currentArtist.deezer_link"
                                            target="_blank" class="stream-link deezer"
                                            :title="$t('game.streaming.deezer')">
                                            <Icon name="simple-icons:deezer" size="36" />
                                        </a>
                                    </div>
                                </div>

                                <!-- Trivia Information -->
                                <div class="trivia-box">
                                    <h3>{{ t('game.didYouKnow') }}</h3>
                                    <p>{{ currentQuestion.trivia }}</p>
                                </div>

                                <button @click="nextQuestion" class="next-button">
                                    <span>{{ t('game.nextQuestion') }}</span>
                                    <Icon name="material-symbols:arrow-forward" />
                                </button>
                            </div>
                        </div>
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
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { authClient } from '~/lib/auth-client'
import { useJokers } from '~/composables/useJokers'
import { useAudioPlayer } from '~/composables/useAudioPlayer'
import { useShare } from '~/composables/useShare'
import { useGameState } from '~/composables/useGameState'
import { useQuestions } from '~/composables/useQuestions'
import { useArtist } from '~/composables/useArtist'
import { useGameResults } from '~/composables/useGameResults'

definePageMeta({
    middleware: 'auth'
})

const session = authClient.useSession()
const route = useRoute()
const { t, locale } = useI18n()
const category = route.params.category as string
const difficulty = route.params.difficulty as string

// Fragen-Logik aus der Composable
const {
    currentQuestion,
    currentOptions,
    maxQuestions,
    usedQuestions,
    loadQuestions,
    selectRandomQuestion
} = useQuestions(category, difficulty)

onMounted(() => {
    loadQuestions()
})

// Dynamischer Import der Kategorien basierend auf der aktuellen Sprache
const categories = await import(`~/json/${locale.value}_categories.json`)
const currentCategoryData = categories.default.find((cat: any) => cat.slug === category)

const {
    remainingJokers,
    jokerUsedForCurrentQuestion,
    audienceHelp,
    hiddenOptions,
    phoneExpertOpinion,
    phoneExpertConfidence,
    useFiftyFiftyJoker,
    useAudienceJoker,
    usePhoneJoker,
    resetJokers
} = useJokers(difficulty)

const gameState = useGameState(maxQuestions.value)

const {
    showSolution,
    isCorrectAnswer,
    gameFinished,
    correctAnswers,
    totalPoints,
    formattedPoints,
    isAnimating,
    showBonus,
    latestBonus,
    updatePoints,
    setAnswer,
    finishGame: completeGame,
    allQuestionsCorrect,
} = gameState

const { currentArtist, loadCurrentArtist } = useArtist()

// Konstanten für Zeitbonus
const BASE_POINTS = 50
const MAX_TIME_BONUS = 100 // Erhöht auf 100
const TIME_LIMIT = 30000 // 30 Sekunden für maximalen Bonus

const questionStartTime = ref(0)

// Starte Timer wenn Frage angezeigt wird
const startQuestionTimer = () => {
    questionStartTime.value = Date.now()
}

const calculateTimeBonus = () => {
    const timeElapsed = Date.now() - questionStartTime.value
    const timePercentage = Math.max(0, 1 - (timeElapsed / TIME_LIMIT))
    const timeBonus = Math.floor(timePercentage * MAX_TIME_BONUS)
    return timeBonus
}

const pointsDisplay = ref<any>(null)

// Funktion zum Scrollen nach oben
const scrollToTop = () => {
    window.scrollTo({
        top: 0,
        behavior: smoothScrollBehavior.value
    })
}

// Bei der Antwortauswahl
const selectAnswer = async (selectedAnswer: string) => {
    if (showSolution.value) return

    const isCorrect = selectedAnswer === currentQuestion.value.correctAnswer
    setAnswer(isCorrect)

    if (isCorrect) {
        const timeBonus = calculateTimeBonus()
        updatePoints(BASE_POINTS, timeBonus)
    }

    await loadCurrentArtist(category, difficulty, currentQuestion)
    await nextTick()
    scrollToTop()
}

const nextQuestion = () => {
    if (usedQuestions.value.length >= maxQuestions.value) {
        gameFinished.value = true
        return
    }

    showSolution.value = false
    resetJokers()
    selectRandomQuestion()
    scrollToTop()
}

// Initial Timer starten
onMounted(() => {
    startQuestionTimer()
    scrollToTop()
})

// Optional: Für Nutzer, die reduced motion bevorzugen
const smoothScrollBehavior = computed(() => {
    const mediaQuery = window?.matchMedia('(prefers-reduced-motion: reduce)')
    return mediaQuery?.matches ? 'auto' : 'smooth'
})

const recordIcon = computed(() => {
    if (allQuestionsCorrect.value) return 'material-symbols:album-gold'
    if (correctAnswers.value >= (maxQuestions.value * 0.75)) return 'material-symbols:album-silver'
    if (correctAnswers.value >= (maxQuestions.value * 0.5)) return 'material-symbols:album-bronze'
    return ''
})

const recordClass = computed(() => {
    if (allQuestionsCorrect.value) return 'gold'
    if (correctAnswers.value >= (maxQuestions.value * 0.75)) return 'silver'
    if (correctAnswers.value >= (maxQuestions.value * 0.5)) return 'bronze'
    return ''
})

const {
    isPlaying,
    currentTime,
    duration,
    togglePlay,
    loadAudio
} = useAudioPlayer()

// Wenn sich currentArtist ändert, lade neue Audio
watch(() => currentArtist.value, (newArtist) => {
    if (newArtist?.preview_link) {
        loadAudio(newArtist.preview_link)
    }
}, { immediate: true })


const { resultMessage, earnedRecord, saveGameResults } = useGameResults({
  thresholds: {
    gold: 1,
    silver: 0.75,
    bronze: 0.5
  }
})

// Bei Spielende beide Funktionen aufrufen
watch(() => usedQuestions.value.length, (newLength) => {
    if (newLength >= maxQuestions.value) {
        completeGame()
        saveGameResults(
            category,
            totalPoints.value,
            correctAnswers.value,
            maxQuestions.value,
            allQuestionsCorrect.value,
            session.value?.data?.user?.id
        )
    }
})

const {
    isMobile,
    canShare,
    shareViaAPI,
    shareToTwitter,
    shareToWhatsApp,
    shareToTelegram,
    shareToReddit
} = useShare({
    currentCategoryData,
    category,
    difficulty
})

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


/* Add scoped styles here */
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

.solution-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.content-wrapper {
    background: var(--background-secondary);
    border-radius: 16px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.result-banner {
    background: var(--error-color, #ff4757);
    color: white;
    padding: 16px;
    border-radius: 8px;
    text-align: center;
    margin-bottom: 20px;
    margin-left: auto;
    margin-right: auto;

    .result-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;

        h2 {
            margin: 0;
            font-size: 1.125em;
        }

        .result-icon {
            flex-shrink: 0;
        }
    }

    .points {
        font-size: 1.1em;
        opacity: 0.9;
        margin-bottom: 8px;
    }

    .correct-answer {
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid rgba(255, 255, 255, 0.2);

        .label {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 6px;
            display: block;
        }

        .text {
            font-size: 1em;
            font-weight: 500;
        }
    }

    &.correct {
        background: #0D7A3D;
    }
}

.answer-box {
    background: white;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

    .label {
        display: block;
        color: var(--text-secondary);
        margin-bottom: 8px;
        font-size: 0.9em;
    }

    .text {
        color: var(--text-primary);
        font-size: 1.2em;
        font-weight: 600;
    }
}

.album-box {
    max-width: 320px;
    margin: 0 auto 20px;

    .cover-wrapper {
        position: relative;
        margin-bottom: 8px;

        img {
            width: 100%;
            height: auto;
            border-radius: 4px;
            display: block;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
    }

    .player-info-wrapper {
        padding: 0 4px;
    }

    .audio-player {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 4px;
        margin: 8px 0;

        .play-button {
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 50%;
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            padding: 0;

            &:hover:not(:disabled) {
                background: var(--primary-dark);
                transform: scale(1.05);
            }

            &:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
        }

        .progress-bar {
            flex-grow: 1;
            height: 4px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 2px;
            overflow: hidden;
            cursor: pointer;
            position: relative;

            &:hover {
                height: 6px;
                margin: -1px 0;
            }

            .progress {
                height: 100%;
                background: var(--primary-color);
                transition: width 0.1s linear;
                position: absolute;
                left: 0;
                top: 0;
            }
        }
    }

    .info {
        text-align: center;
        color: white;

        h3 {
            margin: 0 0 2px 0;
            font-size: 0.9em;
            font-weight: 600;
        }

        .artist {
            margin: 0 0 1px 0;
            font-size: 0.8em;
            opacity: 0.9;
        }

        .year {
            margin: 0;
            font-size: 0.75em;
            opacity: 0.7;
        }
    }

    .streaming-links {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);

        .stream-link {
            color: rgba(255, 255, 255, 0.7);
            transition: all 0.2s ease;
            padding: 6px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;

            &:hover {
                color: white;
                transform: translateY(-1px);
            }

            .icon {
                width: 20px;
                height: 20px;
            }

            &.spotify:hover {
                color: #1DB954;
            }

            &.apple:hover {
                color: #FA57C1;
            }

            &.deezer:hover {
                color: #FF0092;
            }
        }
    }
}

.trivia-box {
    background: var(--background-secondary);
    border-radius: 12px;
    margin-top: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    h3 {
        color: var(--primary-color);
        margin: 0 0 12px 0;
        font-size: 1.2em;
    }

    p {
        margin: 0;
        line-height: 1.6;
        color: var(--text-color);
        font-size: 1em;
    }
}

.play-button {
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);

    &:hover {
        transform: scale(1.05);
        background: var(--primary-dark);
    }
}

.trivia-box {
    background: white;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

    h3 {
        @include section-heading;
    }

    p {
        margin: 0;
        line-height: 1.6;
        color: var(--text-secondary);
        font-size: 1.1em;
    }
}

.next-button {
    width: 100%;
    padding: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-size: 1.2em;
    font-weight: 600;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    &:hover {
        background: var(--primary-dark);
        transform: translateY(-2px);
    }

    .icon {
        font-size: 24px;
    }
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
            font-size: 1rem;
            opacity: 0.8;
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

            .high & {
                background: linear-gradient(90deg, var(--success-color), var(--highlight-color));
            }

            .medium & {
                background: linear-gradient(90deg, var(--primary-color), var(--highlight-color));
            }

            .low & {
                background: linear-gradient(90deg, var(--error-color), var(--secondary-color));
            }
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
    min-height: 400px; // Adjust based on your content
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
