<template>
    <div class="solution-container" role="region" :aria-label="isCorrectAnswer ? t('game.correct') : t('game.wrong')">
        <!-- Ergebnis-Banner -->
        <div class="result-banner" :class="{ 'correct': isCorrectAnswer }" role="alert">
            
            <div class="result-header">
                <Icon :name="isCorrectAnswer ? 'material-symbols:check-circle' : 'material-symbols:cancel'"
                    class="result-icon" :class="{ 'wrong': !isCorrectAnswer }" size="28" :aria-hidden="true" />
                <h2 id="result-status">{{ isCorrectAnswer ? t('game.correct') : t('game.wrong') }}</h2>
            </div>
            <div class="points" aria-live="polite">
                {{ isCorrectAnswer ? '100' : '0' }} {{ t('game.points_label') }}
            </div>

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
            <Icon name="i-mdi:play-outline" size="48" :aria-hidden="true" />
            <span>{{ t('game.next') }}</span>
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

<style scoped lang="scss">
@use '@/assets/scss/mixins' as *;

.solution-container {
    display: flex;
    flex-direction: column;
    gap: var(--padding-medium);
    width: 100%;
    margin: 0 auto;
    padding: var(--padding-medium) 0;

    .result-banner {
        background-color: var(--surface-color);
        border-radius: var(--border-radius);
        padding: var(--padding-medium);
        box-shadow: var(--box-shadow);
        border: 2px solid var(--surface-color-light);
        transition: all var(--transition-speed) var(--transition-bounce);

        &.correct {
            animation: pulse var(--transition-speed) var(--transition-bounce);
            border-color: var(--success-color);
        }

        .result-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: var(--padding-small);
            margin-bottom: var(--padding-medium);

            .result-icon {
                color: var(--success-color);
                font-size: var(--font-size-responsive-xl);

                &.wrong {
                    color: var(--error-color);
                }
            }

            h2 {
                margin: 0;
                font-size: var(--font-size-responsive-xl);
                font-weight: var(--font-weight-bold);
                line-height: var(--line-height-tight);
                color: var(--text-color);
            }
        }

        .points,
        .points-breakdown {
            font-size: var(--font-size-responsive-md);
            margin-bottom: var(--padding-medium);
            line-height: var(--line-height-normal);
            color: var(--text-color);
        }

        .correct-answer {
            margin-top: var(--padding-medium);
            padding: var(--padding-medium) 0;
            background-color: var(--surface-color-light);
            border-radius: var(--border-radius);
            border: 1px solid var(--surface-color-light);

            .label {
                display: block;
                font-size: var(--font-size-base);
                font-weight: var(--font-weight-semibold);
                color: var(--text-color);
                margin-bottom: var(--padding-small);
            }

            .text {
                font-size: var(--font-size-base);
                line-height: var(--line-height-normal);
                color: var(--text-color);
                font-weight: var(--font-weight-medium);
            }
        }
    }

    .content-wrapper {
        .album-box {
            display: flex;
            flex-direction: column;
            gap: var(--padding-medium);
            background-color: var(--surface-color);
            padding: var(--padding-medium) 0;
            border-radius: var(--border-radius);
            border: 2px solid var(--surface-color-light);
            box-shadow: var(--box-shadow);

            @media (width >= 768px) {
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

                .album-cover {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    transition: transform var(--transition-speed) var(--transition-bounce);

                    &:hover {
                        transform: scale(1.05);
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
                    gap: var(--padding-medium);

                    .play-button {
                        @include button-primary;
                        min-width: var(--min-touch-target);
                        min-height: var(--min-touch-target);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        transition: all var(--transition-speed) var(--transition-bounce);
                        padding:0;

                        &:hover:not(:disabled) {
                            transform: scale(1.05);
                            border-color: var(--highlight-color);
                        }

                        &:focus-visible {
                            outline: var(--focus-outline-width) solid var(--focus-outline-color);
                            outline-offset: var(--focus-outline-offset);
                        }

                        &:disabled {
                            opacity: var(--opacity-disabled);
                        }
                    }

                    .progress-bar {
                        flex: 1;
                        height: 8px;
                        background-color: var(--surface-color-light);
                        border-radius: calc(var(--border-radius) / 2);
                        overflow: hidden;
                        position: relative;

                        .progress {
                            height: 100%;
                            background-color: var(--primary-color);
                            border-radius: inherit;
                            transition: width var(--transition-speed) linear;

                            &.buffering {
                                opacity: var(--opacity-disabled);
                            }
                        }
                    }
                }

                .info {
                    .artist {
                        font-size: var(--font-size-responsive-lg);
                        font-weight: var(--font-weight-semibold);
                        color: var(--text-color);
                        margin: 0 0 var(--padding-small);
                        line-height: var(--line-height-tight);
                    }

                    .album {
                        font-size: var(--font-size-base);
                        color: var(--text-color);
                        margin: 0 0 var(--padding-small);
                        line-height: var(--line-height-normal);
                    }

                    .year {
                        font-size: var(--font-size-base);
                        color: var(--text-secondary);
                        margin: 0 0 var(--padding-medium);
                    }

                    .music-links {
                        margin-top: var(--padding-medium);

                        .music-links-title {
                            font-size: var(--font-size-base);
                            font-weight: var(--font-weight-medium);
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
                                min-width: var(--min-touch-target);
                                min-height: var(--min-touch-target);
                                border-radius: var(--border-radius);
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                transition: all var(--transition-speed) var(--transition-bounce);

                                &:hover {
                                    transform: translateY(-2px);
                                    box-shadow: var(--box-shadow-hover);
                                }

                                &:focus-visible {
                                    outline: var(--focus-outline-width) solid var(--focus-outline-color);
                                    outline-offset: var(--focus-outline-offset);
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
        padding: var(--padding-medium);
        border: 2px solid var(--surface-color-light);
        box-shadow: var(--box-shadow);

        h3 {
            font-size: var(--font-size-responsive-lg);
            font-weight: var(--font-weight-semibold);
            color: var(--text-color);
            margin: 0 0 var(--padding-medium);
            line-height: var(--line-height-tight);
        }

        .trivia-content {
            font-size: var(--font-size-base);
            line-height: var(--line-height-relaxed);
            color: var(--text-color);
        }
    }
}

.next-button {
    @include button-primary;
    width: fit-content;
    min-height: var(--min-touch-target);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--padding-small);
    margin: var(--padding-medium) auto;
    padding: var(--padding-medium);
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-medium);
    transition: all var(--transition-speed) var(--transition-bounce);
    color: var(--text-color-dark);

    &:hover {
        transform: translateY(-2px);
        box-shadow: var(--box-shadow-hover);
    }

    &:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }
}

@media (prefers-reduced-motion: reduce) {
    .solution-container,
    .album-cover,
    .play-button,
    .music-link,
    .next-button {
        transition: none;
        animation: none;
        transform: none;
    }
}

.visually-hidden {
    @include sr-only;
}
</style>
