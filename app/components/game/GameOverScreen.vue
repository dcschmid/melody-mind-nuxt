<template>
    <div class="game-end-screen" role="main" aria-label="Game Over Screen">
        <div class="end-content">
            <div class="end-header">
                <h1 id="game-over-title" class="game-over-title">{{ t('game.gameOver.title') }}</h1>
                <div class="final-score-container" role="region" aria-labelledby="game-over-title">
                    <div class="score-circle" role="text" aria-label="Total Score">
                        <div class="score-inner">
                            <span class="points score-value" aria-label="Points">{{ totalPoints }}</span>
                            <span class="points-label score-label">{{ t('game.points_label') }}</span>
                        </div>
                    </div>
                    <div class="stats">
                        <div class="stat-item" role="text">
                            <span class="stat-label score-label">{{ t('game.gameOver.correctAnswers') }}</span>
                            <span class="stat-value score-value" aria-label="Correct Answers">{{ correctAnswers }} / {{ maxQuestions }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="earnedRecord || resultMessage" class="reward-section" :class="recordClass" role="region" aria-label="Achievement">
                <div v-if="earnedRecord" class="record-icon" role="img" :aria-label="recordIcon">
                    <Icon :name="recordIcon" size="64" aria-hidden="true" />
                </div>
                <p v-if="resultMessage" class="reward-text message" role="text">
                    {{ resultMessage }}
                </p>
            </div>

            <div class="share-section" role="region" aria-labelledby="share-title">
                <h2 id="share-title">{{ t('game.results.share.title') }}</h2>
                <div class="share-buttons" role="group" aria-label="Share options">
                    <button v-if="canShare" 
                        class="share-button share-api action-button" 
                        @click="shareViaAPI"
                        aria-label="Share score">
                        <Icon name="material-symbols:share" size="24" aria-hidden="true" />
                        <span>{{ t('game.results.share.buttons.share') }}</span>
                    </button>

                    <template v-else>
                        <button class="share-button copy action-button" 
                            @click="copyShareText"
                            aria-label="Text kopieren">
                            <Icon name="material-symbols:content-copy" size="24" aria-hidden="true" />
                            <span>{{ t('game.results.share.buttons.copy') }}</span>
                        </button>

                        <button class="share-button twitter action-button" 
                            @click="shareToTwitter"
                            aria-label="Share on Twitter">
                            <Icon name="mdi:twitter" size="24" aria-hidden="true" />
                            <span>{{ t('game.results.share.buttons.twitter') }}</span>
                        </button>

                        <button class="share-button telegram action-button" 
                            @click="shareToTelegram"
                            aria-label="Share on Telegram">
                            <Icon name="mdi:telegram" size="24" aria-hidden="true" />
                            <span>{{ t('game.results.share.buttons.telegram') }}</span>
                        </button>

                        <button class="share-button reddit action-button" 
                            @click="shareToReddit"
                            aria-label="Share on Reddit">
                            <Icon name="mdi:reddit" size="24" aria-hidden="true" />
                            <span>{{ t('game.results.share.buttons.reddit') }}</span>
                        </button>

                        <button v-if="isWhatsAppSupported" 
                            class="share-button whatsapp action-button" 
                            @click="shareToWhatsApp"
                            aria-label="Share on WhatsApp">
                            <Icon name="mdi:whatsapp" size="24" aria-hidden="true" />
                            <span>{{ t('game.results.share.buttons.whatsapp') }}</span>
                        </button>
                    </template>
                </div>
            </div>

            <div class="end-actions" role="navigation">
                <NuxtLink :to="localePath('/gamehome')" 
                    class="home-button action-button"
                    aria-label="Back to main menu">
                    <Icon name="material-symbols:home" size="36" aria-hidden="true" />
                    <span>{{ t('game.gameOver.backToMenu') }}</span>
                </NuxtLink>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const { t } = useI18n()
const route = useRoute()
const localePath = useLocalePath()
const { locale } = useI18n()
const { saveGameResults } = useGameResults()

const props = defineProps<{
    totalPoints: number
    correctAnswers: number
    maxQuestions: number
    earnedRecord: boolean
    recordIcon: string
    recordClass: string
    resultMessage: string
}>()

const isMobile = ref(false)
const canShare = ref(false)
const isWhatsAppSupported = ref(false)

// Hole den Username aus dem LocalStorage
const username = localStorage.getItem('username')
const category = route.params.category as string
const difficulty = route.params.difficulty as string

// Bestimme die LPs basierend auf den Punkten und der Schwierigkeit
const determineRecords = () => {
    const percentage = (props.correctAnswers / props.maxQuestions) * 100
    return {
        goldLP: percentage >= 90,
        silverLP: percentage >= 75 && percentage < 90,
        bronzeLP: percentage >= 60 && percentage < 75
    }
}

// Speichere das Ergebnis in der Datenbank
const saveScore = async () => {
    if (!username) return

    const { goldLP, silverLP, bronzeLP } = determineRecords()

    // Zuerst das Ergebnis mit der bestehenden Logik speichern
    await saveGameResults(
        category,
        props.totalPoints,
        props.correctAnswers,
        props.maxQuestions,
        props.correctAnswers === props.maxQuestions,
        difficulty
    )

    // Dann in Turso speichern
    try {
        await $fetch('/api/highscores', {
            method: 'POST',
            body: {
                username,
                points: props.totalPoints,
                category,
                difficulty,
                language: locale.value,
                goldLP,
                silverLP,
                bronzeLP
            }
        })
    } catch (error) {
        console.error('Failed to save score:', error)
    }
}

onMounted(() => {
    // Mobile und Share API Checks
    isMobile.value = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)
    canShare.value = !!navigator?.share
    if (isMobile.value) {
        isWhatsAppSupported.value = true
    }

    // Score speichern
    saveScore()
})

const getShareText = () => {
    let text = t('game.results.share.message.intro', {
        points: props.totalPoints,
        category: route.params.category,
        difficulty: route.params.difficulty
    })

    text += ' ' + t('game.results.share.message.stats', {
        correct: props.correctAnswers,
        total: props.maxQuestions
    })

    // Füge die Challenge-URL hinzu
    const shareUrl = getShareUrl()
    text += ' ' + t('game.results.share.message.challenge', {
        url: shareUrl
    })

    return text
}

const getShareUrl = () => {
    return window.location.href
}

const copyShareText = async () => {
    const text = getShareText()
    try {
        await navigator.clipboard.writeText(text)
        // Optional: Show success message
    } catch (err) {
        console.error('Failed to copy text:', err)
    }
}

const shareToTwitter = () => {
    const text = getShareText()
    const url = getShareUrl()
    window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`)
}

const shareToTelegram = () => {
    const text = getShareText()
    const url = getShareUrl()
    window.open(`https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`)
}

const shareToReddit = () => {
    const text = getShareText()
    const url = getShareUrl()
    window.open(`https://reddit.com/submit?url=${encodeURIComponent(url)}&title=${encodeURIComponent(text)}`)
}

const shareToWhatsApp = () => {
    const text = getShareText()
    window.open(`https://wa.me/?text=${encodeURIComponent(text)}`)
}

const shareViaAPI = async () => {
    try {
        await navigator.share({
            title: t('game.gameOver.title'),
            text: getShareText(),
            url: getShareUrl()
        })
    } catch (err) {
        console.error('Error sharing:', err)
    }
}
</script>

<style scoped lang="scss">
@use "sass:color";
@use "@/assets/scss/mixins" as *;

.game-end-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    margin: 0 auto;
    min-height: calc(100vh - var(--header-height));
    animation: fadeIn 0.5s ease-out;
    padding: var(--padding-small);

    @media (min-width: 640px) {
        justify-content: center;
        padding: var(--padding-medium);
    }
}

.end-content {
    width: 100%;
    max-width: min(100%, 600px);
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: var(--padding-medium);

    @media (min-width: 640px) {
        gap: var(--padding-large);
    }
}

.end-header {
    h1.game-over-title {
        font-size: var(--font-size-responsive-2xl);
        font-weight: 700;
        text-align: center;
        margin-bottom: var(--padding-large);
    }
}

.final-score-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--padding-small);
    margin-top: var(--padding-small);

    @media (min-width: 640px) {
        gap: var(--padding-medium);
        margin-top: var(--padding-medium);
    }
}

.score-circle {
    width: clamp(120px, 30vw, 200px);
    height: clamp(120px, 30vw, 200px);
    border-radius: 50%;
    background: var(--surface-color);
    border: 2px solid var(--primary-color);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--box-shadow);
    transition: all var(--transition-speed) var(--transition-bounce);
    position: relative;

    &::after {
        content: '';
        position: absolute;
        inset: 4px;
        border-radius: 50%;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }

    @media (hover: hover) and (prefers-reduced-motion: no-preference) {
        &:hover {
            transform: scale(1.05);
            box-shadow: var(--box-shadow-hover);
        }
    }
}

.score-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(var(--padding-small) / 2);

    .points.score-value {
        font-size: var(--font-size-responsive-xl);
        font-weight: 700;
        color: var(--primary-color);
    }

    .points-label.score-label {
        font-size: var(--font-size-responsive-md);
        color: var(--text-secondary);
    }
}

.stats {
    .stat-item {
        display: flex;
        flex-direction: column;
        gap: calc(var(--padding-small) / 2);

        .stat-label.score-label {
            font-size: var(--font-size-responsive-md);
            color: var(--text-secondary);
        }

        .stat-value.score-value {
            font-size: var(--font-size-responsive-xl);
            font-weight: 700;
            color: var(--primary-color);
        }
    }
}

.reward-section {
    margin: var(--padding-small) auto;
    padding: var(--padding-medium);
    border-radius: var(--border-radius);
    background: var(--surface-color);
    border: 2px solid var(--primary-color);
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--padding-small);

    @media (min-width: 640px) {
        margin: var(--padding-medium) auto;
        gap: var(--padding-medium);
    }

    &.new-record {
        border-color: var(--success-color);
        background: color-mix(in srgb, var(--surface-color) 95%, var(--success-color));
    }

    .record-icon {
        margin-bottom: 0;
        color: var(--success-color);
        font-size: clamp(2rem, 6vw, 3rem);
        line-height: 1;
    }

    .reward-text.message {
        font-size: var(--font-size-responsive-sm);
        text-align: center;
        margin-bottom: var(--padding-large);
    }
}

.share-section {
    margin-top: var(--padding-small);

    @media (min-width: 640px) {
        margin-top: var(--padding-medium);
    }

    h2 {
        font-size: clamp(1.1rem, 4vw, 1.3rem);
        margin-bottom: var(--padding-small);
        color: var(--text-color);
        font-weight: 600;

        @media (min-width: 640px) {
            margin-bottom: var(--padding-medium);
        }
    }
}

.share-buttons {
    display: flex;
    flex-direction: column;
    gap: var(--padding-small);
    margin-top: var(--padding-small);
    padding: 0 var(--padding-small);

    @media (min-width: 640px) {
        flex-direction: row;
        flex-wrap: wrap;
        gap: var(--padding-medium);
        justify-content: center;
        margin-top: var(--padding-medium);
        padding: 0;
    }
}

.share-button.action-button {
    @include button-secondary;
    width: 100%;
    justify-content: center;
    gap: var(--padding-small);
    font-size: var(--font-size-base);

    &.copy {
        background-color: var(--color-secondary);
        color: var(--color-white);
        
        &:hover {
            background-color: var(--color-secondary-dark);
        }
    }

    &.share-api {
        @include button-primary;
    }

    &:focus-visible {
        outline: 3px solid var(--focus-outline-color);
        outline-offset: 2px;
    }
}

.end-actions {
    margin-top: var(--padding-medium);
    padding: 0 var(--padding-small);

    @media (min-width: 640px) {
        margin-top: var(--padding-large);
        padding: 0;
    }

    .home-button.action-button {
        @include button-primary;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: var(--padding-small);
        width: auto;
        min-height: 48px;
        font-size: var(--font-size-base);

        @media (min-width: 640px) {
            width: auto;
            min-width: 200px;
        }

        &:focus-visible {
            outline: 3px solid var(--focus-outline-color);
            outline-offset: 2px;
        }
    }
}

@media (prefers-reduced-motion: reduce) {
    .game-end-screen,
    .score-inner,
    .stat-item,
    .reward-section,
    .share-section,
    .end-actions {
        animation: none;
    }

    .record-icon {
        animation: none;
    }

    .score-circle:hover {
        transform: none;
    }
}
</style>
