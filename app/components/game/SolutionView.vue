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
                <div class="points-inline">
                    {{ t('game.points', { Basis: latestBonus.base, Zeit: latestBonus.time }) }}
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
import { onMounted, watch } from 'vue'
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
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.solution-container {
    display: flex;
    flex-direction: column;
    gap: var(--padding-large);
    width: 100%;
    max-width: min(100%, 800px);
    margin: 0 auto;
    padding: var(--padding-medium);

    .result-banner {
        background-color: var(--surface-color);
        border-radius: var(--border-radius);
        padding: var(--padding-large);
        box-shadow: var(--box-shadow);
        border: 2px solid var(--surface-color-light);
        transition: transform 0.3s ease;

        &.correct {
            animation: pulse 0.5s ease-out;
            border-color: var(--success-color);
        }

        .result-header {
            display: flex;
            align-items: center;
            gap: var(--padding-medium);
            margin-bottom: var(--padding-medium);

            .result-icon {
                color: var(--success-color);
                font-size: 2rem;
                transition: color 0.3s ease;

                &.wrong {
                    color: var(--error-color);
                }
            }

            h2 {
                margin: 0;
                font-size: clamp(1.75rem, 3vw, 2.25rem);
                font-weight: 600;
                line-height: 1.4;
                color: var(--text-color);
            }
        }

        .points,
        .points-breakdown {
            font-size: clamp(1.25rem, 2vw, 1.5rem);
            margin-bottom: var(--padding-medium);
            line-height: 1.6;
            color: var(--text-color);
        }

        .points-breakdown {
            margin: var(--padding-medium) 0;

            .points-inline {
                display: inline-flex;
                align-items: flex-start;
                font-size: 1.75rem;
                font-weight: 600;
                color: var(--text-color);
            }
        }

        .correct-answer {
            margin-top: var(--padding-medium);
            padding: var(--padding-medium);
            background-color: var(--surface-color-light);
            border-radius: var(--border-radius);
            border: 1px solid var(--surface-border);

            .label {
                display: block;
                font-size: 1.25rem;
                font-weight: 600;
                color: var(--text-color);
                margin-bottom: var(--padding-small);
            }

            .text {
                font-size: 1.5rem;
                line-height: 1.6;
                color: var(--text-color);
                font-weight: 500;
            }
        }
    }

    .content-wrapper {
        .album-box {
            display: grid;
            grid-template-columns: 1fr;
            gap: var(--padding-large);
            background-color: var(--surface-color);
            padding: var(--padding-large);
            border-radius: var(--border-radius);
            border: 2px solid var(--surface-color-light);
            box-shadow: var(--box-shadow);

            @media (min-width: 768px) {
                grid-template-columns: minmax(200px, 300px) 1fr;
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
                }
            }

            .player-info-wrapper {
                display: flex;
                flex-direction: column;
                gap: var(--padding-large);

                .audio-player {
                    display: flex;
                    align-items: center;
                    gap: var(--padding-medium);

                    .play-button {
                        @include button-primary;
                        min-width: 64px;
                        min-height: 64px;
                        border-radius: 50%;
                        padding: 0;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border: 2px solid transparent;
                        transition: all 0.3s ease;

                        &:hover:not(:disabled) {
                            transform: scale(1.05);
                            border-color: var(--highlight-color);
                        }

                        &:focus-visible {
                            outline: none;
                            box-shadow: 0 0 0 3px var(--focus-outline-color);
                            border-color: var(--highlight-color);
                        }

                        &:disabled {
                            opacity: 0.7;
                            cursor: not-allowed;
                        }
                    }

                    .progress-bar {
                        flex: 1;
                        height: 8px;
                        background-color: var(--surface-color-light);
                        border-radius: 4px;
                        overflow: hidden;
                        position: relative;

                        .progress {
                            height: 100%;
                            background-color: var(--primary-color);
                            border-radius: 4px;
                            transition: width 0.1s linear;

                            &.buffering {
                                opacity: 0.7;
                            }
                        }
                    }
                }

                .info {
                    .artist {
                        font-size: clamp(1.5rem, 2.5vw, 1.75rem);
                        font-weight: 600;
                        color: var(--text-color);
                        margin: 0 0 var(--padding-small);
                        line-height: 1.4;
                    }

                    .album {
                        font-size: clamp(1.25rem, 2vw, 1.5rem);
                        color: var(--text-color);
                        margin: 0 0 var(--padding-small);
                        line-height: 1.4;
                    }

                    .year {
                        font-size: 1.25rem;
                        color: var(--text-secondary);
                        margin: 0 0 var(--padding-medium);
                    }

                    .music-links {
                        margin-top: var(--padding-medium);

                        .music-links-title {
                            font-size: 1.25rem;
                            font-weight: 500;
                            color: var(--text-color);
                            margin: 0 0 var(--padding-small);
                            display: flex;
                            align-items: center;
                            gap: var(--padding-small);
                        }

                        .music-links-container {
                            display: flex;
                            gap: var(--padding-medium);
                            margin-top: var(--padding-small);

                            .music-link {
                                @include button-secondary;
                                min-width: 48px;
                                min-height: 48px;
                                border-radius: var(--border-radius);
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                border: 2px solid transparent;
                                transition: all 0.3s ease;

                                &:hover {
                                    transform: translateY(-2px);
                                    border-color: var(--highlight-color);
                                }

                                &:focus-visible {
                                    outline: none;
                                    box-shadow: 0 0 0 3px var(--focus-outline-color);
                                    border-color: var(--highlight-color);
                                }
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
        padding: var(--padding-large);
        border: 2px solid var(--surface-color-light);
        box-shadow: var(--box-shadow);

        h3 {
            font-size: clamp(1.5rem, 2.5vw, 1.75rem);
            font-weight: 600;
            color: var(--text-color);
            margin: 0 0 var(--padding-medium);
            line-height: 1.4;
        }

        .trivia-content {
            font-size: 1.25rem;
            line-height: 1.6;
            color: var(--text-color);
        }
    }
}

.next-button {
    @include button-primary;
    width: 100%;
    min-height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--padding-medium);
    margin-top: var(--padding-medium);
    padding: var(--padding-medium) var(--padding-large);
    font-size: clamp(1.5rem, 2.5vw, 1.75rem);
    font-weight: 500;
    border: 2px solid transparent;
    transition: all 0.3s ease;

    &:hover {
        transform: translateY(-2px);
        border-color: var(--highlight-color);
    }

    &:focus-visible {
        outline: none;
        box-shadow: 0 0 0 3px var(--focus-outline-color);
        border-color: var(--highlight-color);
    }

    span {
        line-height: 1.4;
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
</style>
