<template>
  <div
    class="print:bg-whit flex flex-row justify-between gap-4 rounded-xl border-2 border-[rgb(30,30,30)] bg-[rgb(20,20,20)] p-4 text-center shadow-sm"
    data-testid="game-header"
    role="banner"
  >
    <div class="flex flex-col">
      <h1
        id="category-name"
        class="m-0 text-base leading-[1.4] font-bold tracking-[0.025em] text-white"
        data-testid="category-name"
      >
        {{ categoryName }}
      </h1>
      <p
        class="mt-2 text-base leading-[1.6] font-medium text-white"
        data-testid="round-text"
        aria-live="polite"
      >
        {{ roundText }}
      </p>
    </div>
    <div class="relative text-center">
      <div
        class="flex flex-col items-center gap-2"
        role="status"
        aria-live="polite"
        aria-atomic="true"
      >
        <span
          class="text-base leading-[1.4] font-semibold tracking-[0.025em] text-[rgb(130,87,229)]"
          :class="{ 'text-success scale-110': isAnimating }"
        >
          {{ formattedPoints }}
        </span>
        <span class="text-base leading-[1.6] font-medium text-white">
          {{ t('game.points_label') }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps<{
  categoryName: string
  currentRound: number
  maxRounds: number
  points: number
  isAnimating: boolean
}>()

const roundText = computed(() => {
  return t('game.round', {
    aktuell: props.currentRound,
    max: props.maxRounds,
  })
})

const formattedPoints = computed(() => {
  return new Intl.NumberFormat(undefined, {
    maximumFractionDigits: 0,
  }).format(props.points)
})
</script>

<style>
/* High contrast mode support */
@media (prefers-contrast: more) {
  #category-name {
    text-decoration: underline !important;
    text-underline-offset: 8px !important;
    text-decoration-thickness: 2px !important;
  }

  .text-success {
    color: #007c28 !important; /* Noch dunkleres Grün für besseren Kontrast (AAA) */
    font-weight: bold !important;
  }

  .text-\[#f0f0f0\] {
    color: white !important;
  }
}

/* Print styles */
@media print {
  div[role='banner'] {
    border: 1px solid #ddd !important;
    background: white !important;
    color: black !important;
    box-shadow: none !important;
    padding: 1rem !important;
  }

  h1,
  p,
  span {
    color: black !important;
  }

  h1 {
    font-size: 18pt !important;
    margin-bottom: 8pt !important;
  }

  p,
  span {
    font-size: 12pt !important;
    line-height: 1.5 !important;
  }

  div[role='alert'] {
    display: none !important;
  }
}
</style>
