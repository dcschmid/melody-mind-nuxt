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
                    <UnLazyImage :src="artist.coverSrc" 
                        :alt="`Album Cover: ${artist.artist} - ${artist.album}`" 
                        loading="lazy"
                        width="300"
                        height="300"
                        format="webp"
                        quality="80"
                        sizes="(max-width: 768px) 100vw, 300px"
                        class="album-cover"
                        fetchpriority="high" />
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
import { ref, onMounted, onBeforeUnmount, watch, shallowRef, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useThrottleFn } from '@vueuse/core'
import { useThumbHash } from '~/composables/useThumbHash'

const { t } = useI18n()
const { getThumbHash } = useThumbHash()

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
    (e: 'update:isPlaying', value: boolean): void
    (e: 'update:audioLoaded', value: boolean): void
    (e: 'update:isBuffering', value: boolean): void
    (e: 'update:progress', value: number): void
    (e: 'next'): void
}>()

// Optimierte Audio-Player Variablen
const audio = shallowRef<HTMLAudioElement | null>(null)
const progressUpdateInterval = ref<number | null>(null)
const updateProgressThrottled = useThrottleFn(() => {
    if (audio.value) {
        progress.value = (audio.value.currentTime / audio.value.duration) * 100
    }
}, 100)

const audioLoaded = ref(props.audioLoaded)
const isPlaying = ref(props.isPlaying)
const isBuffering = ref(props.isBuffering)
const progress = ref(props.progress)

// ThumbHash für das Cover-Bild abrufen
const thumbHash = computed(() => props.artist?.coverSrc ? getThumbHash(props.artist.coverSrc) : undefined)

// Watch für Änderungen der Props
watch(() => props.audioLoaded, (val) => audioLoaded.value = val)
watch(() => props.isPlaying, (val) => isPlaying.value = val)
watch(() => props.isBuffering, (val) => isBuffering.value = val)
watch(() => props.progress, (val) => progress.value = val)

// Lazy load audio
onMounted(() => {
    if (props.artist?.preview_link) {
        audio.value = new Audio(props.artist.preview_link)
        audio.value.addEventListener('loadeddata', () => {
            audioLoaded.value = true
        })
        audio.value.addEventListener('timeupdate', updateProgressThrottled)
        audio.value.addEventListener('ended', () => {
            isPlaying.value = false
            progress.value = 0
        })
    }
})

onBeforeUnmount(() => {
    if (audio.value) {
        audio.value.pause()
        audio.value.src = ''
    }
})

const togglePlay = async () => {
    if (!audio.value || !props.artist?.preview_link) return
    
    try {
        if (isPlaying.value) {
            await audio.value.pause()
            isPlaying.value = false
            emit('update:isPlaying', isPlaying.value)
        } else {
            await audio.value.play()
            isPlaying.value = true
            emit('update:isPlaying', isPlaying.value)
        }
    } catch (error) {
        console.error('Playback error:', error)
        audioLoaded.value = false
        emit('update:audioLoaded', audioLoaded.value)
    }
}
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.solution-container {
    display: flex;
    flex-direction: column;
    gap: var(--padding-small);
    width: 100%;
    max-width: min(100%, 800px);
    margin: 0 auto;
    padding: var(--padding-small);

    @media (min-width: 640px) {
        padding: var(--padding-medium);
        gap: var(--padding-large);
    }

    .result-banner {
        background-color: var(--surface-color);
        border-radius: var(--border-radius);
        padding: var(--padding-small);
        box-shadow: var(--box-shadow);
        border: 2px solid var(--surface-color-light);
        transition: transform 0.3s ease;

        @media (min-width: 375px) {
            padding: var(--padding-medium);
        }

        @media (min-width: 640px) {
            padding: var(--padding-large);
        }

        &.correct {
            animation: pulse 0.5s ease-out;
            border-color: var(--success-color);
        }

        .result-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: var(--padding-small);
            margin-bottom: var(--padding-small);
            flex-wrap: wrap;

            @media (min-width: 375px) {
                gap: var(--padding-medium);
                margin-bottom: var(--padding-medium);
            }

            @media (min-width: 640px) {
                justify-content: flex-start;
                flex-wrap: nowrap;
            }

            .result-icon {
                color: var(--success-color);
                font-size: 1.5rem;
                transition: color 0.3s ease;

                @media (min-width: 375px) {
                    font-size: 2rem;
                }

                &.wrong {
                    color: var(--error-color);
                }
            }

            h2 {
                margin: 0;
                font-size: clamp(1.25rem, 3vw, 2.25rem);
                font-weight: 600;
                line-height: 1.4;
                color: var(--text-color);
                text-align: center;

                @media (min-width: 640px) {
                    text-align: left;
                }
            }
        }

        .points,
        .points-breakdown {
            font-size: clamp(1rem, 2vw, 1.5rem);
            margin-bottom: var(--padding-small);
            line-height: 1.6;
            color: var(--text-color);
            text-align: center;

            @media (min-width: 375px) {
                margin-bottom: var(--padding-medium);
            }

            @media (min-width: 640px) {
                text-align: left;
            }
        }

        .correct-answer {
            margin-top: var(--padding-small);
            padding: var(--padding-small);
            background-color: var(--surface-color-light);
            border-radius: var(--border-radius);
            border: 1px solid var(--surface-border);
            text-align: center;

            @media (min-width: 375px) {
                margin-top: var(--padding-medium);
                padding: var(--padding-medium);
            }

            @media (min-width: 640px) {
                text-align: left;
            }

            .label {
                display: block;
                font-size: 1.1rem;
                font-weight: 600;
                color: var(--text-color);
                margin-bottom: var(--padding-small);

                @media (min-width: 375px) {
                    font-size: 1.25rem;
                }
            }

            .text {
                font-size: 1.1rem;
                line-height: 1.6;
                color: var(--text-color);
                font-weight: 500;

                @media (min-width: 375px) {
                    font-size: 1.25rem;
                }

                @media (min-width: 640px) {
                    font-size: 1.5rem;
                }
            }
        }
    }

    .content-wrapper {
        .album-box {
            display: flex;
            flex-direction: column;
            gap: var(--padding-small);
            background-color: var(--surface-color);
            padding: var(--padding-small);
            border-radius: var(--border-radius);
            border: 2px solid var(--surface-color-light);
            box-shadow: var(--box-shadow);

            @media (min-width: 375px) {
                gap: var(--padding-medium);
                padding: var(--padding-medium);
            }

            @media (min-width: 768px) {
                display: grid;
                grid-template-columns: minmax(200px, 300px) 1fr;
                gap: var(--padding-large);
                padding: var(--padding-large);
            }

            .cover-wrapper {
                width: 100%;
                max-width: 300px;
                margin: 0 auto;
                aspect-ratio: 1;
                background-color: var(--surface-color-light);
                border-radius: var(--border-radius);
                overflow: hidden;
                will-change: transform;

                .album-cover {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    transform: translateZ(0);
                    backface-visibility: hidden;
                    transition: transform 0.3s ease;

                    &:hover {
                        transform: scale(1.05);
                    }
                }
            }

            .player-info-wrapper {
                display: flex;
                flex-direction: column;
                gap: var(--padding-small);
                text-align: center;

                @media (min-width: 375px) {
                    gap: var(--padding-medium);
                }

                @media (min-width: 768px) {
                    text-align: left;
                    gap: var(--padding-large);
                }

                .audio-player {
                    display: flex;
                    align-items: center;
                    gap: var(--padding-small);
                    justify-content: center;

                    @media (min-width: 375px) {
                        gap: var(--padding-medium);
                    }

                    @media (min-width: 768px) {
                        justify-content: flex-start;
                    }

                    .play-button {
                        @include button-primary;
                        min-width: 48px;
                        min-height: 48px;
                        border-radius: 50%;
                        padding: 0;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border: 2px solid transparent;
                        transition: all 0.3s ease;

                        @media (min-width: 375px) {
                            min-width: 64px;
                            min-height: 64px;
                        }

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
                        height: 6px;
                        background-color: var(--surface-color-light);
                        border-radius: 3px;
                        overflow: hidden;
                        position: relative;

                        @media (min-width: 375px) {
                            height: 8px;
                            border-radius: 4px;
                        }

                        .progress {
                            height: 100%;
                            background-color: var(--primary-color);
                            border-radius: inherit;
                            transition: width 0.1s linear;

                            &.buffering {
                                opacity: 0.7;
                            }
                        }
                    }
                }

                .info {
                    .artist {
                        font-size: clamp(1.1rem, 2.5vw, 1.75rem);
                        font-weight: 600;
                        color: var(--text-color);
                        margin: 0 0 var(--padding-small);
                        line-height: 1.4;
                    }

                    .album {
                        font-size: clamp(1rem, 2vw, 1.5rem);
                        color: var(--text-color);
                        margin: 0 0 var(--padding-small);
                        line-height: 1.4;
                    }

                    .year {
                        font-size: 1rem;
                        color: var(--text-secondary);
                        margin: 0 0 var(--padding-small);

                        @media (min-width: 375px) {
                            font-size: 1.1rem;
                            margin: 0 0 var(--padding-medium);
                        }
                    }

                    .music-links {
                        margin-top: var(--padding-small);

                        @media (min-width: 375px) {
                            margin-top: var(--padding-medium);
                        }

                        .music-links-title {
                            font-size: 1.1rem;
                            font-weight: 500;
                            color: var(--text-color);
                            margin: 0 0 var(--padding-small);
                            display: flex;
                            align-items: center;
                            gap: var(--padding-small);
                            justify-content: center;

                            @media (min-width: 375px) {
                                font-size: 1.25rem;
                            }

                            @media (min-width: 768px) {
                                justify-content: flex-start;
                            }
                        }

                        .music-links-container {
                            display: flex;
                            gap: var(--padding-small);
                            margin-top: var(--padding-small);
                            justify-content: center;

                            @media (min-width: 375px) {
                                gap: var(--padding-medium);
                            }

                            @media (min-width: 768px) {
                                justify-content: flex-start;
                            }

                            .music-link {
                                @include button-secondary;
                                min-width: 40px;
                                min-height: 40px;
                                border-radius: var(--border-radius);
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                border: 2px solid transparent;
                                transition: all 0.3s ease;

                                @media (min-width: 375px) {
                                    min-width: 48px;
                                    min-height: 48px;
                                }

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
        padding: var(--padding-small);
        border: 2px solid var(--surface-color-light);
        box-shadow: var(--box-shadow);
        text-align: center;

        @media (min-width: 375px) {
            padding: var(--padding-medium);
        }

        @media (min-width: 640px) {
            padding: var(--padding-large);
            text-align: left;
        }

        h3 {
            font-size: clamp(1.25rem, 2.5vw, 1.75rem);
            font-weight: 600;
            color: var(--text-color);
            margin: 0 0 var(--padding-small);
            line-height: 1.4;

            @media (min-width: 375px) {
                margin: 0 0 var(--padding-medium);
            }
        }

        .trivia-content {
            font-size: 1rem;
            line-height: 1.6;
            color: var(--text-color);

            @media (min-width: 375px) {
                font-size: 1.1rem;
            }

            @media (min-width: 640px) {
                font-size: 1.25rem;
            }
        }
    }
}

.next-button {
    @include button-primary;
    width: 100%;
    min-height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--padding-small);
    margin-top: var(--padding-small);
    padding: var(--padding-small);
    font-size: clamp(1.1rem, 2.5vw, 1.75rem);
    font-weight: 500;
    border: 2px solid transparent;
    transition: all 0.3s ease;

    @media (min-width: 375px) {
        min-height: 80px;
        gap: var(--padding-medium);
        margin-top: var(--padding-medium);
        padding: var(--padding-medium);
    }

    @media (min-width: 640px) {
        min-height: 100px;
        padding: var(--padding-medium) var(--padding-large);
    }

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
