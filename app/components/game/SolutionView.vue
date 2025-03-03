<template>
  <div
    class="print:print-friendly mx-auto flex w-full flex-col gap-6 py-6"
    role="region"
    :aria-label="isCorrectAnswer ? t('game.correct') : t('game.wrong')"
  >
    <!-- Ergebnis-Banner -->
    <div
      class="rounded-lg border-2 bg-[rgb(var(--surface-color-rgb))] p-6 shadow-md motion-safe:transition-all motion-safe:duration-300 motion-safe:ease-out motion-reduce:transition-none"
      :class="{
        'border-[rgb(var(--success-color-rgb))]': isCorrectAnswer,
        'border-[rgb(var(--error-color-rgb))]': !isCorrectAnswer,
      }"
      role="alert"
    >
      <div class="mb-6 flex items-center justify-center gap-3">
        <Icon
          :name="isCorrectAnswer ? 'material-symbols:check-circle' : 'material-symbols:cancel'"
          class="text-3xl"
          :class="
            isCorrectAnswer
              ? 'text-[rgb(var(--success-color-rgb))]'
              : 'text-[rgb(var(--error-color-rgb))]'
          "
          :aria-hidden="true"
        />
        <h2
          id="result-status"
          class="m-0 text-[clamp(2rem,2.5vw+1.5rem,2.5rem)] leading-tight font-bold text-[rgb(var(--text-color-rgb))]"
        >
          {{ isCorrectAnswer ? t('game.correct') : t('game.wrong') }}
        </h2>
      </div>
      <div
        class="mb-6 text-[clamp(1.5rem,1.7vw+1rem,1.75rem)] leading-normal text-[rgb(var(--text-color-rgb))]"
        aria-live="polite"
      >
        {{ isCorrectAnswer ? '100' : '0' }} {{ t('game.points_label') }}
      </div>

      <div
        class="mt-6 rounded-lg border border-[rgb(var(--border-color-rgb))] bg-[rgb(var(--surface-color-light-rgb))] p-4"
      >
        <span
          id="correct-answer-label"
          class="mb-2 block text-base font-semibold text-[rgb(var(--text-color-rgb))]"
        >
          {{ t('game.correctAnswer') }}
        </span>
        <div
          class="text-base leading-normal font-medium text-[rgb(var(--text-color-rgb))]"
          aria-labelledby="correct-answer-label"
        >
          {{ question.correctAnswer }}
        </div>
      </div>
    </div>

    <!-- Content Container -->
    <div>
      <!-- Album Info -->
      <article
        v-if="artist"
        class="flex flex-col gap-4 rounded-lg border-2 border-[rgb(var(--surface-color-light-rgb))] bg-[rgb(var(--surface-color-rgb))] p-4 shadow-md md:grid md:grid-cols-[minmax(200px,300px)_1fr] md:gap-8 md:p-8"
        aria-labelledby="album-title"
      >
        <div
          class="mx-auto aspect-square w-full max-w-[300px] overflow-hidden rounded-lg bg-[rgb(var(--surface-color-light-rgb))]"
        >
          <UnLazyImage
            :src="artist.coverSrc"
            :alt="`Album Cover: ${artist.artist} - ${artist.album}`"
            loading="lazy"
            width="300"
            height="300"
            format="webp"
            quality="80"
            sizes="(max-width: 768px) 100vw, 300px"
            class="h-full w-full object-cover hover:scale-105 motion-safe:transition-transform motion-safe:duration-300 motion-safe:ease-out motion-reduce:transition-none"
            fetchpriority="high"
          />
        </div>
        <div class="flex flex-col gap-4">
          <div class="flex items-center gap-4" role="region" aria-label="Audio Player">
            <Button
              :disabled="!artist?.preview_link || !audioLoaded"
              :title="isPlaying ? t('game.audio.pause') : t('game.audio.play')"
              :aria-label="isPlaying ? t('game.audio.pause') : t('game.audio.play')"
              aria-pressed="false"
              variant="primary"
              class-name="min-w-[3rem] min-h-[3rem] rounded-full p-0 flex items-center justify-center motion-safe:transition-all motion-safe:duration-300 motion-safe:ease-out hover:scale-105 focus:ring-[3px] focus:ring-[rgb(var(--focus-color-rgb))] focus:ring-offset-2 motion-reduce:transition-none"
              @click="togglePlay"
            >
              <Icon
                :name="isPlaying ? 'material-symbols:pause' : 'material-symbols:play-arrow'"
                class="text-3xl"
                :aria-hidden="true"
              />
            </Button>
            <div
              class="relative h-2 flex-1 overflow-hidden rounded-full bg-[rgb(var(--surface-color-light-rgb))]"
              role="progressbar"
              :aria-valuenow="progress"
              aria-valuemin="0"
              aria-valuemax="100"
              :aria-label="t('game.audio.progress')"
            >
              <div
                class="h-full rounded-full bg-[rgb(var(--primary-color-rgb))] motion-safe:transition-[width] motion-safe:duration-300 motion-safe:ease-linear motion-reduce:transition-none"
                :class="{ 'opacity-50': isBuffering }"
                :style="{ width: `${progress}%` }"
              />
            </div>
          </div>
          <div>
            <h3
              id="album-title"
              class="m-0 mb-2 text-[clamp(1.75rem,2vw+1.25rem,2rem)] leading-tight font-bold text-[rgb(var(--text-color-rgb))]"
            >
              {{ artist.artist }}
            </h3>
            <p class="m-0 mb-2 text-base leading-normal text-[rgb(var(--text-color-rgb))]">
              {{ artist.album }}
            </p>
            <p class="m-0 mb-4 text-base text-[rgb(var(--text-secondary-color-rgb))]">
              {{ artist.year }}
            </p>
            <div
              v-if="artist.spotify_link || artist.apple_music_link || artist.deezer_link"
              class="mt-6"
              role="region"
              :aria-label="t('game.links.listen_on')"
            >
              <h4
                id="streaming-services-title"
                class="m-0 mb-2 flex items-center gap-2 text-base font-medium text-[rgb(var(--text-color-rgb))]"
              >
                {{ t('game.links.listen_on') }}
                <Icon name="material-symbols:headphones" aria-hidden="true" />
              </h4>
              <div class="mt-2 flex gap-4" role="list" aria-labelledby="streaming-services-title">
                <Button
                  v-if="artist.spotify_link"
                  as="a"
                  :href="artist.spotify_link"
                  target="_blank"
                  rel="noopener noreferrer"
                  :aria-label="t('game.links.spotify')"
                  role="listitem"
                  variant="icon"
                  class-name="min-w-[3rem] min-h-[3rem] bg-[rgb(var(--surface-color-light-rgb))] rounded-full motion-safe:transition-all motion-safe:duration-300 motion-safe:ease-out hover:translate-y-[-2px] hover:shadow-lg focus:ring-[3px] focus:ring-[rgb(var(--focus-color-rgb))] focus:ring-offset-2 motion-reduce:transition-none"
                >
                  <Icon name="mdi:spotify" class="text-2xl" aria-hidden="true" />
                  <span class="sr-only">{{ t('game.links.spotify') }}</span>
                </Button>
                <Button
                  v-if="artist.apple_music_link"
                  as="a"
                  :href="artist.apple_music_link"
                  target="_blank"
                  rel="noopener noreferrer"
                  :aria-label="t('game.links.apple')"
                  role="listitem"
                  variant="icon"
                  class-name="min-w-[3rem] min-h-[3rem] bg-[rgb(var(--surface-color-light-rgb))] rounded-full motion-safe:transition-all motion-safe:duration-300 motion-safe:ease-out hover:translate-y-[-2px] hover:shadow-lg focus:ring-[3px] focus:ring-[rgb(var(--focus-color-rgb))] focus:ring-offset-2 motion-reduce:transition-none"
                >
                  <Icon name="mdi:apple" class="text-2xl" aria-hidden="true" />
                  <span class="sr-only">{{ t('game.links.apple') }}</span>
                </Button>
                <Button
                  v-if="artist.deezer_link"
                  as="a"
                  :href="artist.deezer_link"
                  target="_blank"
                  rel="noopener noreferrer"
                  :aria-label="t('game.links.deezer')"
                  role="listitem"
                  variant="icon"
                  class-name="min-w-[3rem] min-h-[3rem] bg-[rgb(var(--surface-color-light-rgb))] rounded-full motion-safe:transition-all motion-safe:duration-300 motion-safe:ease-out hover:translate-y-[-2px] hover:shadow-lg focus:ring-[3px] focus:ring-[rgb(var(--focus-color-rgb))] focus:ring-offset-2 motion-reduce:transition-none"
                >
                  <Icon name="simple-icons:deezer" class="text-2xl" aria-hidden="true" />
                  <span class="sr-only">{{ t('game.links.deezer') }}</span>
                </Button>
              </div>
            </div>
          </div>
        </div>
      </article>
    </div>

    <!-- Trivia Section -->
    <div
      v-if="artist?.trivia"
      class="rounded-lg border-2 border-[rgb(var(--surface-color-light-rgb))] bg-[rgb(var(--surface-color-rgb))] p-6 shadow-md"
      role="complementary"
      aria-labelledby="trivia-title"
    >
      <h3
        id="trivia-title"
        class="m-0 mb-4 text-[clamp(1.75rem,2vw+1.25rem,2rem)] leading-tight font-bold text-[rgb(var(--text-color-rgb))]"
      >
        {{ t('game.trivia.title') }}
      </h3>
      <div class="text-base leading-relaxed text-[rgb(var(--text-color-rgb))]">
        {{ artist.trivia }}
      </div>
    </div>

    <Button
      :aria-label="t('game.next')"
      variant="primary"
      class-name="w-fit min-h-[3rem] flex items-center justify-center gap-2 mx-auto my-6 p-4 text-base font-medium motion-safe:transition-all motion-safe:duration-300 motion-safe:ease-out hover:translate-y-[-2px] hover:shadow-lg focus:ring-[3px] focus:ring-[rgb(var(--focus-color-rgb))] focus:ring-offset-2 motion-reduce:transition-none"
      @click="$emit('next')"
    >
      <Icon name="i-mdi:play-outline" class="text-3xl" :aria-hidden="true" />
      <span>{{ t('game.next') }}</span>
    </Button>
  </div>
</template>

<script setup lang="ts">
import { useThrottleFn } from '@vueuse/core'
import { computed, onBeforeUnmount, onMounted, ref, shallowRef, watch } from 'vue'
import { useI18n } from 'vue-i18n'
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
const thumbHash = computed(() =>
  props.artist?.coverSrc ? getThumbHash(props.artist.coverSrc) : undefined
)

// Watch für Änderungen der Props
watch(
  () => props.audioLoaded,
  (val) => (audioLoaded.value = val)
)
watch(
  () => props.isPlaying,
  (val) => (isPlaying.value = val)
)
watch(
  () => props.isBuffering,
  (val) => (isBuffering.value = val)
)
watch(
  () => props.progress,
  (val) => (progress.value = val)
)

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
