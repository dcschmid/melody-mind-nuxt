<template>
    <div class="solution-container" role="region" :aria-label="isCorrectAnswer ? t('game.correct') : t('game.wrong')">
        <!-- Ergebnis-Banner -->
        <div class="result-banner" :class="{ 'correct': isCorrectAnswer }" role="alert">
            <div class="result-header">
                <Icon :name="isCorrectAnswer ? 'material-symbols:check-circle' : 'material-symbols:cancel'"
                    class="result-icon" :class="{ 'wrong': !isCorrectAnswer }" size="28" :aria-hidden="true" />
                <h2 id="result-status">{{ isCorrectAnswer ? t('game.correct') : t('game.wrong') }}</h2>
            </div>
            <div v-if="isCorrectAnswer" class="points-breakdown" aria-live="polite">
                <div class="points">
                    {{ t('game.points', { base: latestBonus.base, time: latestBonus.time }) }}
                </div>
            </div>
            <div v-else class="points" aria-live="polite">0 {{ t('game.points_label') }}</div>

            <div class="correct-answer">
                <span class="label" id="correct-answer-label">{{ t('game.correctAnswer') }}</span>
                <div class="text" aria-labelledby="correct-answer-label">{{ question.correctAnswer }}</div>
            </div>
        </div>

        <!-- Content Container -->
        <div class="content-wrapper">
            <!-- Album Info -->
            <article v-if="artist" class="album-box" aria-labelledby="album-title">
                <div class="cover-wrapper">
                    <img :src="artist.coverSrc" :alt="`Album Cover: ${artist.artist} - ${artist.album}`" loading="lazy"
                        decoding="async" />
                </div>
                <div class="player-info-wrapper">
                    <div class="audio-player" role="region" aria-label="Audio Player">
                        <button @click="togglePlay" class="play-button"
                            :disabled="!artist?.preview_link || !audioLoaded"
                            :title="isPlaying ? t('game.audio.pause') : t('game.audio.play')"
                            :aria-label="isPlaying ? t('game.audio.pause') : t('game.audio.play')" aria-pressed="false">
                            <Icon :name="isPlaying ? 'material-symbols:pause' : 'material-symbols:play-arrow'" size="36"
                                :aria-hidden="true" />
                        </button>
                        <div class="progress-bar" role="progressbar" :aria-valuenow="progress" aria-valuemin="0"
                            aria-valuemax="100" :aria-label="t('game.audio.progress')">
                            <div class="progress" :style="{ width: `${progress}%` }"
                                :class="{ 'buffering': isBuffering }"></div>
                        </div>
                    </div>
                    <div class="info">
                        <h3 id="album-title" class="artist">{{ artist.artist }}</h3>
                        <p class="album">{{ artist.album }}</p>
                        <p class="year">{{ artist.year }}</p>
                        <div class="music-links"
                            v-if="artist.spotify_link || artist.apple_music_link || artist.deezer_link" role="region"
                            :aria-label="t('game.links.listen_on')">
                            <h4 class="music-links-title" id="streaming-services-title">
                                {{ t('game.links.listen_on') }}
                                <Icon name="material-symbols:headphones" aria-hidden="true" />
                            </h4>
                            <div class="music-links-container" role="list" aria-labelledby="streaming-services-title">
                                <a v-if="artist.spotify_link" :href="artist.spotify_link" target="_blank"
                                    rel="noopener noreferrer" class="music-link spotify"
                                    :aria-label="t('game.links.spotify')" role="listitem">
                                    <Icon name="mdi:spotify" size="24" aria-hidden="true" />
                                    <span class="visually-hidden">{{ t('game.links.spotify') }}</span>
                                </a>
                                <a v-if="artist.apple_music_link" :href="artist.apple_music_link" target="_blank"
                                    rel="noopener noreferrer" class="music-link apple"
                                    :aria-label="t('game.links.apple')" role="listitem">
                                    <Icon name="mdi:apple" size="24" aria-hidden="true" />
                                    <span class="visually-hidden">{{ t('game.links.apple') }}</span>
                                </a>
                                <a v-if="artist.deezer_link" :href="artist.deezer_link" target="_blank"
                                    rel="noopener noreferrer" class="music-link deezer"
                                    :aria-label="t('game.links.deezer')" role="listitem">
                                    <Icon name="simple-icons:deezer" size="24" aria-hidden="true" />
                                    <span class="visually-hidden">{{ t('game.links.deezer') }}</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </article>
        </div>

        <!-- Trivia Section -->
        <div v-if="artist?.trivia" class="trivia-section" role="complementary" aria-labelledby="trivia-title">
            <h3 id="trivia-title">{{ t('game.trivia.title') }}</h3>
            <div class="trivia-content">
                {{ artist.trivia }}
            </div>
        </div>

        <button @click="$emit('next')" class="next-button" :aria-label="t('game.next')">
            <span>{{ t('game.next') }}</span>
            <Icon name="material-symbols:arrow-forward" size="48" :aria-hidden="true" />
        </button>
    </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Props {
    isCorrectAnswer: boolean
    latestBonus: {
        base: number
        time: number
    }
    question: {
        correctAnswer: string
    }
    artist: {
        coverSrc: string
        artist: string
        album: string
        year: string
        preview_link?: string
        trivia?: string
        spotify_link?: string
        apple_music_link?: string
        deezer_link?: string
    } | null
    isPlaying: boolean
    audioLoaded: boolean
    isBuffering: boolean
    progress: number
}

const props = defineProps<Props>()
const emit = defineEmits<{
    (e: 'togglePlay'): void
    (e: 'next'): void
}>()

const togglePlay = () => {
    emit('togglePlay')
}

// Debug log to check if trivia exists
onMounted(() => {
    console.log('Artist data:', props.artist)
})
</script>

<style lang="scss" scoped>
.solution-container {
    display: flex;
    flex-direction: column;
    gap: var(--padding-medium);
    width: 100%;
    margin: 0 auto;

    .result-banner {
        background-color: var(--surface-color);
        border-radius: var(--border-radius);
        padding: var(--padding-medium);
        box-shadow: var(--box-shadow);
        transition: transform 0.3s ease;

        &.correct {
            animation: pulse 0.5s ease-out;
        }

        .result-header {
            display: flex;
            align-items: center;
            gap: var(--padding-small);
            margin-bottom: var(--padding-small);

            .result-icon {
                color: var(--success-color);
                transition: color 0.3s ease;

                &.wrong {
                    color: var(--error-color);
                }
            }

            h2 {
                margin: 0;
                font-size: clamp(1.5rem, 3vw, 2rem);
            }
        }

        .points,
        .points-breakdown {
            font-size: clamp(1rem, 2vw, 1.25rem);
            margin-bottom: var(--padding-medium);
        }

        .correct-answer {
            .label {
                display: block;
                font-weight: bold;
                margin-bottom: var(--padding-small);
                color: var(--text-secondary);
            }

            .text {
                font-size: clamp(1.1rem, 2.2vw, 1.35rem);
                color: var(--text-primary);
            }
        }
    }

    .content-wrapper {
        .album-box {
            display: grid;
            grid-template-columns: 1fr;
            gap: var(--padding-medium);
            background-color: var(--surface-color);
            border-radius: var(--border-radius);
            padding: var(--padding-medium);
            box-shadow: var(--box-shadow);

            @media (min-width: 768px) {
                grid-template-columns: minmax(200px, 300px) 1fr;
                align-items: start;
            }

            .cover-wrapper {
                width: 100%;
                aspect-ratio: 1;
                border-radius: var(--border-radius);
                overflow: hidden;
                box-shadow: var(--box-shadow);

                img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    transition: transform 0.3s ease;

                    &:hover {
                        transform: scale(1.02);
                    }
                }
            }

            .player-info-wrapper {
                display: flex;
                flex-direction: column;
                gap: var(--padding-medium);

                .audio-player {
                    display: flex;
                    align-items: center;
                    gap: var(--padding-small);

                    .play-button {
                        @include button-primary;
                        width: 48px;
                        height: 48px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        padding: 0;

                        &:disabled {
                            opacity: 0.5;
                            cursor: not-allowed;
                        }
                    }

                    .progress-bar {
                        flex: 1;
                        height: 8px;
                        background-color: var(--surface-secondary);
                        border-radius: 4px;
                        overflow: hidden;

                        .progress {
                            height: 100%;
                            background-color: var(--primary-color);
                            transition: width 0.3s linear;

                            &.buffering {
                                animation: buffering 1s infinite linear;
                            }
                        }
                    }
                }

                .info {
                    .artist {
                        font-size: clamp(1.25rem, 2.5vw, 1.5rem);
                        font-weight: bold;
                        color: var(--text-primary);
                        margin: 0 0 0.5rem;
                    }

                    .album {
                        font-size: clamp(1rem, 2vw, 1.25rem);
                        color: var(--text-secondary);
                        margin: 0 0 0.25rem;
                    }

                    .year {
                        font-size: clamp(0.875rem, 1.5vw, 1rem);
                        color: var(--text-tertiary);
                        margin: 0;
                    }

                    .music-links {
                        display: flex;
                        flex-direction: column;
                        gap: var(--padding-small);
                        margin-top: var(--padding-small);

                        .music-links-title {
                            font-size: clamp(1rem, 2vw, 1.25rem);
                            color: var(--text-secondary);
                            margin-bottom: var(--padding-small);
                            display: flex;
                            align-items: center;
                            gap: var(--padding-small);
                        }

                        .music-links-container {
                            display: flex;
                            gap: var(--padding-small);
                        }

                        .music-link {
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            width: 36px;
                            height: 36px;
                            border-radius: 50%;
                            background: var(--surface-color-light);
                            color: var(--text-secondary);
                            transition: all 0.2s ease;
                            position: relative;

                            &:hover,
                            &:focus {
                                transform: scale(1.1);
                                outline: 2px solid var(--color-primary);
                                outline-offset: 2px;
                            }

                            &:focus-visible {
                                outline: 3px solid var(--color-primary);
                                outline-offset: 2px;
                            }

                            &.spotify:hover,
                            &.spotify:focus {
                                background: #1DB954;
                                color: white;
                            }

                            &.apple:hover,
                            &.apple:focus {
                                background: #FA243C;
                                color: white;
                            }

                            &.deezer:hover,
                            &.deezer:focus {
                                background: #FF0092;
                                color: white;
                            }
                        }
                    }
                }
            }
        }
    }

    .trivia-section {
        background-color: var(--surface-color);
        border-radius: var(--border-radius);
        padding: var(--padding-medium);
        box-shadow: var(--box-shadow);

        h3 {
            margin: 0 0 var(--padding-small);
            font-size: clamp(1.25rem, 2.5vw, 1.5rem);
            color: var(--primary-color);
        }

        .trivia-content {
            font-size: var(--body-font-size);
            line-height: var(--line-height-body);
            color: var(--text-secondary);
            white-space: pre-line;
        }
    }

    .next-button {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: var(--padding-small);
        background-color: var(--primary-color);
        color: var(--button-text-color);
        border: none;
        border-radius: var(--border-radius);
        padding: var(--padding-small) var(--padding-medium);
        font-size: var(--button-font-size);
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        max-width: 200px;
        margin: 0 auto;

        &:hover {
            background-color: var(--button-hover-color);
            transform: translateY(-2px);
        }

        &:focus-visible {
            outline: 3px solid var(--focus-outline-color);
            outline-offset: 2px;
        }

        &:active {
            transform: translateY(1px);
        }
    }
}

.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

@keyframes pulse {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.02);
    }

    100% {
        transform: scale(1);
    }
}

@keyframes buffering {
    0% {
        transform: translateX(-100%);
    }

    100% {
        transform: translateX(100%);
    }
}
</style>
