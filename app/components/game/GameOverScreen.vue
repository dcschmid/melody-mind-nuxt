<template>
  <div
    class="motion-safe:animate-fade-in print:print-friendly mx-auto flex min-h-[calc(100vh-var(--header-height))] w-full flex-col items-center justify-start p-4 sm:justify-center sm:p-6"
    data-testid="game-over-screen"
    role="main"
    aria-label="Game Over Screen"
  >
    <div class="flex w-full max-w-[var(--max-content-width)] flex-col gap-6 text-center sm:gap-8">
      <div class="flex flex-col items-center">
        <h1 id="game-over-title" class="mb-8 text-center text-3xl font-bold sm:text-4xl" data-testid="game-over-title">
          {{ t('game.gameOver.title') }}
        </h1>
        <div
          class="mt-3 flex flex-col items-center gap-3 sm:mt-6 sm:gap-6"
          role="region"
          aria-labelledby="game-over-title"
        >
          <div
            class="relative flex h-[clamp(120px,30vw,200px)] w-[clamp(120px,30vw,200px)] items-center justify-center rounded-full border-2 border-[rgb(var(--primary-color-rgb))] bg-[rgb(var(--surface-color-rgb))] shadow-sm hover:scale-105 hover:shadow-md focus:outline-none focus-visible:ring-4 focus-visible:ring-[rgb(var(--highlight-color-rgb))] focus-visible:ring-offset-4 motion-safe:transition-transform motion-safe:duration-300 motion-safe:ease-[var(--transition-bounce)] motion-reduce:transform-none motion-reduce:transition-none"
            data-testid="score-circle"
            role="text"
            aria-label="Total Score"
          >
            <div
              class="absolute inset-[4px] rounded-full border-2 border-[rgb(var(--surface-color-light-rgb))]"
            />
            <div class="flex flex-col items-center gap-1">
              <span
                class="text-2xl font-bold text-[rgb(var(--primary-color-rgb))] sm:text-3xl"
                data-testid="total-points"
                aria-label="Points"
                >{{ totalPoints }}</span
              >
              <span class="text-sm text-[rgb(var(--secondary-color-rgb))] sm:text-base">{{
                t('game.points_label')
              }}</span>
            </div>
          </div>
          <div class="flex flex-col items-center">
            <div class="flex flex-col gap-1" role="text">
              <span class="text-sm text-[rgb(var(--secondary-color-rgb))] sm:text-base">{{
                t('game.gameOver.correctAnswers')
              }}</span>
              <span
                class="text-xl font-bold text-[rgb(var(--primary-color-rgb))] sm:text-2xl"
                aria-label="Correct Answers"
                >{{ correctAnswers }} / {{ maxQuestions }}</span
              >
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="earnedRecord || resultMessage"
        class="my-4 flex w-full flex-col items-center gap-3 rounded-lg border-2 bg-[rgb(var(--surface-color-rgb))] p-6 shadow-sm sm:my-6 sm:gap-6"
        data-testid="achievement-region"
        :class="[
          recordClass === 'new-record'
            ? 'border-[var(--success-color)] bg-[color-mix(in_srgb,rgb(var(--surface-color-rgb))_95%,var(--success-color))]'
            : 'border-[rgb(var(--primary-color-rgb))]',
        ]"
        role="region"
        aria-label="Achievement"
      >
        <div
          v-if="earnedRecord"
          class="text-3xl leading-tight text-[var(--success-color)]"
          role="img"
          :aria-label="recordIcon"
        >
          <Icon :name="recordIcon" size="64" aria-hidden="true" />
        </div>
        <p v-if="resultMessage" class="mb-6 text-center text-sm sm:text-base" role="text">
          {{ resultMessage }}
        </p>
      </div>

      <div class="mt-4 sm:mt-6" role="region" aria-labelledby="share-title">
        <h2
          id="share-title"
          class="mb-3 text-base font-semibold text-[rgb(var(--text-color-rgb))] sm:mb-6 sm:text-lg"
        >
          {{ t('game.results.share.title') }}
        </h2>
        <div
          class="mt-3 flex flex-col gap-3 px-3 sm:mt-6 sm:flex-row sm:flex-wrap sm:justify-center sm:gap-6 sm:px-0"
          role="group"
          aria-label="Share options"
          data-testid="share-options"
        >
          <Button
            v-if="canShare"
            variant="primary"
            full-width
            class-name="sm:w-auto sm:min-w-44 h-12 gap-2 min-h-[44px]"
            aria-label="Share score"
            @click="shareViaAPI"
          >
            <Icon name="material-symbols:share" size="24" aria-hidden="true" />
            <span>{{ t('game.results.share.buttons.share') }}</span>
          </Button>

          <template v-else>
            <Button
              variant="secondary"
              full-width
              class-name="sm:w-auto sm:min-w-44 h-12 gap-2 min-h-[44px]"
              aria-label="Text kopieren"
              @click="copyShareText"
            >
              <Icon name="material-symbols:content-copy" size="24" aria-hidden="true" />
              <span>{{ t('game.results.share.buttons.copy') }}</span>
            </Button>

            <Button
              variant="secondary"
              full-width
              class-name="sm:w-auto sm:min-w-44 h-12 gap-2 min-h-[44px]"
              aria-label="Share on Twitter"
              @click="shareToTwitter"
            >
              <Icon name="mdi:twitter" size="24" aria-hidden="true" />
              <span>{{ t('game.results.share.buttons.twitter') }}</span>
            </Button>

            <Button
              variant="secondary"
              full-width
              class-name="sm:w-auto sm:min-w-44 h-12 gap-2 min-h-[44px]"
              aria-label="Share on Telegram"
              @click="shareToTelegram"
            >
              <Icon name="mdi:telegram" size="24" aria-hidden="true" />
              <span>{{ t('game.results.share.buttons.telegram') }}</span>
            </Button>

            <Button
              variant="secondary"
              full-width
              class-name="sm:w-auto sm:min-w-44 h-12 gap-2 min-h-[44px]"
              aria-label="Share on Reddit"
              @click="shareToReddit"
            >
              <Icon name="mdi:reddit" size="24" aria-hidden="true" />
              <span>{{ t('game.results.share.buttons.reddit') }}</span>
            </Button>

            <Button
              v-if="isWhatsAppSupported"
              variant="secondary"
              full-width
              class-name="sm:w-auto sm:min-w-44 h-12 gap-2 min-h-[44px]"
              aria-label="Share on WhatsApp"
              @click="shareToWhatsApp"
            >
              <Icon name="mdi:whatsapp" size="24" aria-hidden="true" />
              <span>{{ t('game.results.share.buttons.whatsapp') }}</span>
            </Button>
          </template>
        </div>
      </div>

      <div class="mt-6 px-3 sm:mt-8 sm:px-0" role="navigation">
        <NuxtLink
          :to="localePath('/gamehome')"
          data-testid="back-to-menu"
          class="inline-flex h-12 min-h-[44px] items-center justify-center gap-2 rounded-lg bg-[rgb(var(--primary-color-rgb))] px-6 py-2 font-medium text-white transition-colors duration-300 hover:bg-[var(--primary-color-dark)] focus:outline-none focus-visible:ring-4 focus-visible:ring-[rgb(var(--highlight-color-rgb))] focus-visible:ring-offset-4 motion-reduce:transition-none"
          aria-label="Back to main menu"
        >
          <Icon name="material-symbols:home" size="36" aria-hidden="true" />
          <span>{{ t('game.gameOver.backToMenu') }}</span>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Button from '~/components/ui/Button.vue'

const { t } = useI18n()
const route = useRoute()
const localePath = useLocalePath()
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

const category = route.params.category as string
const difficulty = route.params.difficulty as string

const saveScore = async () => {
  await saveGameResults(
    category,
    props.totalPoints,
    props.correctAnswers,
    props.maxQuestions,
    props.correctAnswers === props.maxQuestions,
    difficulty
  )
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
    difficulty: route.params.difficulty,
  })

  text +=
    ' ' +
    t('game.results.share.message.stats', {
      correct: props.correctAnswers,
      total: props.maxQuestions,
    })

  // Füge die Challenge-URL hinzu
  const shareUrl = getShareUrl()
  text +=
    ' ' +
    t('game.results.share.message.challenge', {
      url: shareUrl,
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
  window.open(
    `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`
  )
}

const shareToTelegram = () => {
  const text = getShareText()
  const url = getShareUrl()
  window.open(
    `https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`
  )
}

const shareToReddit = () => {
  const text = getShareText()
  const url = getShareUrl()
  window.open(
    `https://reddit.com/submit?url=${encodeURIComponent(url)}&title=${encodeURIComponent(text)}`
  )
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
      url: getShareUrl(),
    })
  } catch (err) {
    console.error('Error sharing:', err)
  }
}
</script>
