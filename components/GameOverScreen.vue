<template>
    <div class="game-end-screen">
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

            <div class="share-section">
                <h3>{{ t('game.results.share.title') }}</h3>
                <div class="share-buttons">
                    <button v-if="canShare" class="share-button share-api" @click="shareViaAPI">
                        <Icon name="material-symbols:share" size="24" />
                        <span>{{ t('game.results.share.buttons.share') }}</span>
                    </button>

                    <template v-else>
                        <button class="share-button twitter" @click="shareToTwitter">
                            <Icon name="mdi:twitter" size="24" />
                            <span>{{ t('game.results.share.buttons.twitter') }}</span>
                        </button>

                        <button class="share-button telegram" @click="shareToTelegram">
                            <Icon name="mdi:telegram" size="24" />
                            <span>{{ t('game.results.share.buttons.telegram') }}</span>
                        </button>

                        <button class="share-button reddit" @click="shareToReddit">
                            <Icon name="mdi:reddit" size="24" />
                            <span>{{ t('game.results.share.buttons.reddit') }}</span>
                        </button>

                        <button v-if="isWhatsAppSupported" class="share-button whatsapp" @click="shareToWhatsApp">
                            <Icon name="mdi:whatsapp" size="24" />
                            <span>{{ t('game.results.share.buttons.whatsapp') }}</span>
                        </button>
                    </template>
                </div>
            </div>

            <div class="end-actions">
                <NuxtLink :to="localePath('/gamehome')" class="home-button">
                    <Icon name="material-symbols:home" size="36" />
                    <span>{{ t('game.gameOver.backToMenu') }}</span>
                </NuxtLink>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const { t } = useI18n()
const localePath = useLocalePath()

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

onMounted(() => {
    // Prüfe ob es ein mobiles Gerät ist
    isMobile.value = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)
    
    // Prüfe ob der Browser die Web Share API unterstützt
    canShare.value = !!navigator?.share
    
    // Prüfe ob WhatsApp installiert ist (nur auf Mobilgeräten möglich)
    if (isMobile.value) {
        isWhatsAppSupported.value = true // Wir nehmen an, dass WhatsApp auf Mobilgeräten verfügbar ist
    }
})

const getShareText = () => {
    let text = t('game.results.share.message.intro', {
        points: props.totalPoints
    })
    
    text += ' ' + t('game.results.share.message.stats', {
        correct: props.correctAnswers,
        total: props.maxQuestions
    })
    
    // Füge die Challenge-URL hinzu
    text += ' ' + t('game.results.share.message.challenge', {
        url: window.location.href
    })
    
    return text
}

const getShareUrl = () => {
    return window.location.href
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
    justify-content: center;
    padding: var(--padding-large);
    width: var(--content-width);
    margin: 0 auto;
    min-height: calc(100vh - var(--header-height));
    animation: fadeIn 0.5s ease-out;

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
}

.end-content {
    width: 100%;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: var(--padding-large);
}

.end-header {
    h2 {
        font-size: var(--header-font-size);
        font-weight: bold;
        background: linear-gradient(135deg, var(--primary-color), var(--highlight-color));
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 8s ease infinite;
        margin: 0;
    }

    @keyframes gradientShift {

        0%,
        100% {
            filter: hue-rotate(0deg);
        }

        50% {
            filter: hue-rotate(30deg);
        }
    }
}

.final-score-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--padding-medium);
}

.score-circle {
    width: clamp(150px, 35vw, 220px);
    height: clamp(150px, 35vw, 220px);
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, var(--surface-color), color-mix(in srgb, var(--background-color) 90%, var(--primary-color)));
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow:
        var(--box-shadow),
        inset 0 2px 15px rgba(255, 255, 255, 0.1),
        0 0 30px rgba(187, 134, 252, 0.15);
    transition: all var(--transition-speed) var(--transition-bounce);
    position: relative;

    &::after {
        content: '';
        position: absolute;
        inset: 4px;
        border-radius: 50%;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }

    &:hover {
        transform: scale(1.05) rotate(5deg);
        box-shadow:
            var(--box-shadow-hover),
            inset 0 2px 20px rgba(255, 255, 255, 0.15),
            0 0 40px rgba(187, 134, 252, 0.2);
    }
}

.score-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(var(--padding-small) / 2);
    transform: scale(0.95);
    animation: pulseIn 0.6s var(--transition-bounce) forwards;

    @keyframes pulseIn {
        0% {
            transform: scale(0.95);
            opacity: 0;
        }

        70% {
            transform: scale(1.05);
        }

        100% {
            transform: scale(1);
            opacity: 1;
        }
    }

    .points {
        font-size: clamp(2.5rem, 7vw, 4rem);
        font-weight: bold;
        color: var(--primary-color);
        text-shadow: 0 0 20px rgba(187, 134, 252, 0.3);
        margin: 0;
    }

    .points-label {
        font-size: var(--body-font-size);
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        opacity: 0.9;
    }
}

.stats {
    .stat-item {
        display: flex;
        flex-direction: column;
        gap: calc(var(--padding-small) / 2);
        animation: slideUp 0.5s ease-out forwards;
        animation-delay: 0.2s;
        opacity: 0;

        @keyframes slideUp {
            from {
                transform: translateY(20px);
                opacity: 0;
            }

            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        .stat-label {
            font-size: var(--body-font-size);
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .stat-value {
            font-size: calc(var(--button-font-size) * 1.2);
            font-weight: bold;
            color: var(--text-color);
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
        }
    }
}

.reward-section {
    margin: 0 auto;
    padding: var(--padding-medium);
    border-radius: var(--border-radius);
    background: linear-gradient(165deg,
            color-mix(in srgb, var(--surface-color) 98%, var(--primary-color)),
            var(--surface-color));
    max-width: var(--max-line-length);
    box-shadow: var(--box-shadow);
    border: 1px solid rgba(255, 255, 255, 0.05);
    backdrop-filter: var(--overlay-blur);
    animation: fadeScale 0.6s ease-out forwards;
    animation-delay: 0.3s;
    opacity: 0;

    @keyframes fadeScale {
        from {
            transform: scale(0.95);
            opacity: 0;
        }

        to {
            transform: scale(1);
            opacity: 1;
        }
    }

    &.new-record {
        background: linear-gradient(165deg,
                color-mix(in srgb, var(--surface-color) 85%, var(--success-color)),
                color-mix(in srgb, var(--surface-color) 95%, var(--success-color)));
        border: 1px solid color-mix(in srgb, var(--success-color) 30%, transparent);
    }

    .record-icon {
        margin-bottom: var(--padding-small);
        color: var(--success-color);
        filter: drop-shadow(0 0 10px rgba(0, 230, 118, 0.3));
        animation: bounce 2s infinite;

        @keyframes bounce {

            0%,
            100% {
                transform: translateY(0);
            }

            50% {
                transform: translateY(-10px);
            }
        }
    }

    .reward-text {
        font-size: calc(var(--body-font-size) * 1.1);
        line-height: var(--line-height-body);
        color: var(--text-color);
        letter-spacing: var(--spacing-text);
        margin: 0;
    }
}

.share-section {
    margin-top: var(--padding-medium);
    animation: fadeIn 0.5s ease-out forwards;
    animation-delay: 0.4s;
    opacity: 0;

    h3 {
        font-size: calc(var(--button-font-size) * 1.2);
        margin-bottom: var(--padding-medium);
        color: var(--text-color);
        font-weight: 600;
    }
}

.share-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
    margin-top: 1rem;
}

.share-button {
    display: inline-flex;
    align-items: center;
    gap: calc(var(--padding-small) / 2);
    padding: var(--padding-small) var(--padding-medium);
    border-radius: var(--border-radius);
    border: none;
    cursor: pointer;
    font-size: var(--body-font-size);
    font-weight: 600;
    min-height: var(--min-touch-target);
    transition: all var(--transition-speed) var(--transition-bounce);
    position: relative;
    overflow: hidden;

    &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(rgba(255, 255, 255, 0.1), transparent);
        transform: translateY(-100%);
        transition: transform 0.3s ease;
    }

    &:hover {
        transform: translateY(-2px);
        box-shadow: var(--box-shadow-hover);

        &::before {
            transform: translateY(0);
        }
    }

    &:active {
        transform: translateY(1px);
    }

    &:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }

    &.twitter {
        background: #1DA1F2;
        color: white;
    }

    &.telegram {
        background: #0088cc;
        color: white;
    }

    &.reddit {
        background: #FF4500;
        color: white;
    }

    &.whatsapp {
        background: #25D366;
        color: white;

        &:hover {
            background-color: color.adjust(#25D366, $lightness: -10%);
        }
    }

    &.share-api {
        background: var(--primary-color);
        color: var(--button-text-color);

        &:hover {
            background: var(--button-hover-color);
        }
    }

    span {
        position: relative;
        z-index: 1;
    }
}

.end-actions {
    margin-top: var(--padding-large);
    animation: fadeIn 0.5s ease-out forwards;
    animation-delay: 0.5s;
    opacity: 0;

    .home-button {
        display: inline-flex;
        align-items: center;
        gap: var(--padding-small);
        padding: var(--padding-small) var(--padding-medium);
        border-radius: var(--border-radius);
        background: var(--primary-color);
        color: var(--button-text-color);
        text-decoration: none;
        font-weight: 600;
        min-height: var(--min-touch-target);
        transition: all var(--transition-speed) var(--transition-bounce);
        box-shadow: var(--box-shadow);
        position: relative;
        overflow: hidden;

        &::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(rgba(255, 255, 255, 0.2), transparent);
            transform: translateY(-100%);
            transition: transform 0.3s ease;
        }

        &:hover {
            transform: translateY(-2px);
            box-shadow: var(--box-shadow-hover);
            background: var(--button-hover-color);

            &::before {
                transform: translateY(0);
            }
        }

        &:active {
            transform: translateY(1px);
        }

        &:focus-visible {
            outline: var(--focus-outline-width) solid var(--focus-outline-color);
            outline-offset: var(--focus-outline-offset);
        }
    }
}

@media (max-width: 640px) {
    .game-end-screen {
        padding: var(--padding-medium);
    }

    .share-buttons {
        flex-direction: column;
        align-items: stretch;
        gap: var(--padding-small);
    }

    .share-button {
        justify-content: center;
    }
}
</style>
