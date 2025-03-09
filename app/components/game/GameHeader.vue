<template>
  <div
    class="flex flex-col gap-4 rounded-xl border-2 border-[rgb(30,30,30)] bg-[rgb(20,20,20)] p-4 text-center shadow-sm motion-safe:transition-all motion-safe:duration-300 sm:flex-row sm:items-center sm:justify-between sm:p-4 sm:px-6 sm:text-left print:border print:border-gray-300 print:bg-white print:text-black print:shadow-none"
    data-testid="game-header"
    role="banner"
  >
    <div class="flex flex-col">
      <h1
        id="category-name"
        class="m-0 text-[clamp(2rem,2.7vw+1rem,2.25rem)] leading-[1.4] font-bold tracking-[0.025em] text-white contrast-more:underline contrast-more:underline-offset-8 print:text-black"
        data-testid="category-name"
      >
        {{ categoryName }}
      </h1>
      <p
        class="mt-2 text-[clamp(1.25rem,1.2vw+1rem,1.5rem)] leading-[1.6] font-medium text-white contrast-more:text-white print:text-black"
        data-testid="round-text"
        aria-live="polite"
      >
        {{ roundText }}
      </p>
    </div>
    <div class="relative text-center sm:text-right">
      <div
        class="flex flex-col items-center gap-2 sm:items-end"
        role="status"
        aria-live="polite"
        aria-atomic="true"
      >
        <span
          class="text-[clamp(2rem,2.7vw+1rem,2.25rem)] leading-[1.4] font-semibold tracking-[0.025em] text-[rgb(130,87,229)] motion-safe:transition-transform motion-safe:duration-300 motion-reduce:transition-none print:text-black"
          :class="{ 'scale-110 text-success': isAnimating }"
        >
          {{ formattedPoints }}
        </span>
        <span
          class="text-[clamp(1.25rem,1.2vw+1rem,1.5rem)] leading-[1.6] font-medium text-white contrast-more:text-white print:text-black"
        >
          {{ t('game.points_label') }}
        </span>
      </div>
      <transition
        enter-active-class="motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none"
        leave-active-class="motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none"
        enter-from-class="opacity-0 translate-y-[-0.625rem]"
        leave-to-class="opacity-0 translate-y-[-0.625rem]"
        mode="out-in"
      >
        <div
          v-if="showBonus"
          class="absolute bottom-[-3.75rem] left-1/2 z-[400] min-w-[7.5rem] -translate-x-1/2 transform rounded-xl border-2 border-success bg-[rgb(20,20,20)] p-4 text-center text-[clamp(1.25rem,1.2vw+1rem,1.5rem)] whitespace-nowrap text-white shadow-sm sm:top-[-3.75rem] sm:right-0 sm:bottom-auto sm:left-auto sm:transform-none print:hidden"
          data-testid="bonus-indicator"
          role="alert"
        >
          <div
            class="text-[clamp(1.5rem,1.7vw+1rem,1.75rem)] leading-[1.6] font-bold text-success"
          >
            +{{ latestBonus.base }}
          </div>
          <div class="mt-2 text-[clamp(1.25rem,1.2vw+1rem,1.5rem)] leading-[1.6] text-[#f0f0f0]">
            <span class="time">+{{ latestBonus.time }} Bonus</span>
          </div>
        </div>
      </transition>
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
  showBonus: boolean
  latestBonus: {
    base: number
    time: number
  }
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
