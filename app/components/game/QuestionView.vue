<template>
  <div
    class="print:print-friendly mx-auto flex w-full flex-col gap-6 py-6"
    role="main"
    :aria-label="t('game.aria.quizQuestion')"
  >
    <!-- Frage -->
    <div
      class="rounded-lg border-2 border-[rgb(var(--surface-color-light-rgb))] bg-[rgb(var(--surface-color-rgb))] p-6 shadow-md md:p-8"
      role="region"
      aria-labelledby="question-text"
    >
      <h1
        id="question-text"
        class="mb-4 text-center text-[clamp(1.5rem,1.7vw+1rem,1.75rem)] leading-normal font-bold text-[rgb(var(--text-color-rgb))]"
      >
        {{ question.question }}
      </h1>
    </div>

    <!-- Antwortmöglichkeiten -->
    <div class="w-full" role="group" :aria-label="t('game.aria.answerOptions')">
      <TransitionGroup v-bind="transitionGroupProps">
        <Button
          v-for="(option, index) in currentOptions"
          v-show="!hiddenOptions.includes(option)"
          :key="option"
          :disabled="disabled || hiddenOptions.includes(option)"
          :aria-label="t('game.selectAnswer', { answer: option })"
          :aria-hidden="hiddenOptions.includes(option)"
          :aria-disabled="disabled || hiddenOptions.includes(option)"
          :tabindex="hiddenOptions.includes(option) ? -1 : 0"
          :data-index="index + 1"
          variant="secondary"
          full-width
          class-name="min-h-[3rem] py-4 text-[clamp(1.5rem,1.7vw+1rem,1.75rem)] font-semibold leading-normal text-center border-2 border-transparent motion-safe:transition-all motion-safe:duration-300 motion-safe:ease-out relative hover:translate-y-[-2px] hover:border-[rgb(var(--highlight-color-rgb))] hover:shadow-lg focus:ring-[3px] focus:ring-[rgb(var(--focus-color-rgb))] focus:ring-offset-2 motion-reduce:transition-none"
          @click="$emit('select-answer', option)"
        >
          <span>{{ option }}</span>
          <span class="sr-only">{{ t('game.option', { number: index + 1 }) }}</span>
        </Button>
      </TransitionGroup>
    </div>

    <!-- Telefonjoker Antwort -->
    <div
      v-if="phoneExpertOpinion"
      class="my-4 rounded-lg border-2 border-[rgb(var(--surface-color-light-rgb))] bg-[rgb(var(--surface-color-rgb))] p-6 shadow-md"
      role="region"
      :aria-label="t('game.aria.expertAdvice')"
      aria-labelledby="expert-title"
    >
      <h2
        id="expert-title"
        class="mb-4 text-[clamp(1.75rem,2vw+1.25rem,2rem)] leading-tight font-bold tracking-wide text-[rgb(var(--text-color-rgb))]"
      >
        {{ t('game.expert.title') }}
      </h2>
      <div>
        <div class="mb-4 flex items-center gap-3">
          <div
            class="flex h-10 w-10 items-center justify-center rounded-full bg-[rgb(var(--primary-color-light-rgb))] text-[rgb(var(--primary-color-dark-rgb))]"
          >
            <Icon name="material-symbols:call" class="text-2xl" aria-hidden="true" />
          </div>
          <span
            class="text-[clamp(1.5rem,1.7vw+1rem,1.75rem)] font-semibold text-[rgb(var(--text-color-rgb))]"
            >{{ phoneExpertOpinion.expert }}</span
          >
        </div>
        <div
          class="bg-opacity-30 rounded-lg border border-[rgb(var(--border-color-rgb))] bg-[rgb(var(--surface-color-light-rgb))] p-4"
        >
          <p class="mb-6 text-[clamp(1.5rem,1.7vw+1rem,1.75rem)] leading-relaxed">
            {{ phoneExpertOpinion.message }}
          </p>
          <div
            class="mb-2"
            role="progressbar"
            :aria-valuenow="phoneExpertConfidence"
            aria-valuemin="0"
            aria-valuemax="100"
            :aria-label="t('game.expert.confidence', { value: phoneExpertConfidence })"
          >
            <div
              class="h-3 overflow-hidden rounded-full bg-[rgb(var(--surface-color-light-rgb))] shadow-md"
            >
              <div
                :class="[
                  'h-full motion-safe:transition-[width] motion-safe:duration-300 motion-safe:ease-out motion-reduce:transition-none',
                  phoneExpertConfidence > 70
                    ? 'bg-[rgb(var(--success-color-rgb))]'
                    : phoneExpertConfidence > 40
                      ? 'bg-[rgb(var(--highlight-color-rgb))]'
                      : 'bg-[rgb(var(--error-color-rgb))]',
                ]"
                :style="{ width: phoneExpertConfidence + '%' }"
              />
            </div>
            <span
              class="mt-2 block text-base font-medium text-[rgb(var(--text-secondary-color-rgb))]"
            >
              {{ t('game.expert.confidence', { value: phoneExpertConfidence }) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Publikumsjoker Antwort -->
    <div
      v-if="audienceOpinion && Object.keys(audienceOpinion).length > 0"
      class="my-4 rounded-lg border-2 border-[rgb(var(--surface-color-light-rgb))] bg-[rgb(var(--surface-color-rgb))] p-6 shadow-md"
      role="region"
      :aria-label="t('game.aria.audienceOpinion')"
      aria-labelledby="audience-title"
    >
      <h2
        id="audience-title"
        class="mb-6 text-[clamp(1.75rem,2vw+1.25rem,2rem)] leading-tight font-bold tracking-wide text-[rgb(var(--text-color-rgb))]"
      >
        {{ t('game.jokers.audience.title') }}
      </h2>
      <div class="flex flex-col gap-5">
        <div
          v-for="(percentage, option) in audienceOpinion"
          :key="option"
          class="flex items-center gap-3"
          role="progressbar"
          :aria-valuenow="percentage"
          aria-valuemin="0"
          aria-valuemax="100"
          :aria-label="t('game.jokers.audience.result', { option, percentage })"
        >
          <div class="w-16 font-semibold text-[rgb(var(--text-color-rgb))]" aria-hidden="true">
            {{ option }}
          </div>
          <div
            class="h-[44px] flex-1 overflow-hidden rounded-full bg-[rgb(var(--surface-color-light-rgb))] shadow-md"
          >
            <div
              class="h-full rounded-full bg-[rgb(var(--primary-color-rgb))] motion-safe:transition-[width] motion-safe:duration-300 motion-safe:ease-out motion-reduce:transition-none"
              :style="{ width: percentage + '%' }"
            />
          </div>
          <div
            class="w-16 text-right text-[clamp(1.5rem,1.7vw+1rem,1.75rem)] font-semibold text-[rgb(var(--text-color-rgb))]"
            aria-hidden="true"
          >
            {{ percentage }}%
          </div>
        </div>
      </div>
    </div>

    <!-- Joker -->
    <div
      class="my-6 flex w-full flex-col items-center gap-5"
      role="group"
      :aria-label="t('game.jokers.title')"
    >
      <h2 class="sr-only">
        {{ t('game.jokers.title') }}
      </h2>
      <div class="flex flex-wrap justify-center gap-6">
        <Button
          :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
          :aria-label="t('game.jokers.fiftyFifty.ariaLabel')"
          :aria-disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
          variant="icon"
          class-name="min-w-[3.5rem] min-h-[3.5rem] p-3 bg-[rgb(var(--surface-color-light-rgb))] rounded-full motion-safe:transition-all motion-safe:duration-300 motion-safe:ease-out hover:translate-y-[-2px] hover:shadow-lg focus:ring-[3px] focus:ring-[rgb(var(--focus-color-rgb))] focus:ring-offset-2 motion-reduce:transition-none"
          @click="$emit('use-fifty-fifty')"
        >
          <Icon
            name="material-symbols:balance"
            class="text-2xl text-[rgb(var(--text-color-rgb))]"
            aria-hidden="true"
          />
        </Button>
        <Button
          :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
          :aria-label="t('game.jokers.audience.ariaLabel')"
          :aria-disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
          variant="icon"
          class-name="min-w-[3.5rem] min-h-[3.5rem] p-3 bg-[rgb(var(--surface-color-light-rgb))] rounded-full motion-safe:transition-all motion-safe:duration-300 motion-safe:ease-out hover:translate-y-[-2px] hover:shadow-lg focus:ring-[3px] focus:ring-[rgb(var(--focus-color-rgb))] focus:ring-offset-2 motion-reduce:transition-none"
          @click="$emit('use-audience')"
        >
          <Icon
            name="material-symbols:group"
            class="text-2xl text-[rgb(var(--text-color-rgb))]"
            aria-hidden="true"
          />
        </Button>
        <Button
          :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
          :aria-label="t('game.jokers.phone.ariaLabel')"
          :aria-disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
          variant="icon"
          class-name="min-w-[3.5rem] min-h-[3.5rem] p-3 bg-[rgb(var(--surface-color-light-rgb))] rounded-full motion-safe:transition-all motion-safe:duration-300 motion-safe:ease-out hover:translate-y-[-2px] hover:shadow-lg focus:ring-[3px] focus:ring-[rgb(var(--focus-color-rgb))] focus:ring-offset-2 motion-reduce:transition-none"
          @click="$emit('use-phone')"
        >
          <Icon
            name="tabler:phone"
            class="text-2xl text-[rgb(var(--text-color-rgb))]"
            aria-hidden="true"
          />
        </Button>
      </div>
      <p
        class="text-center text-base font-medium text-[rgb(var(--text-secondary-color-rgb))]"
        role="status"
        aria-live="polite"
      >
        {{ t('game.jokers.remainingCount', { count: remainingJokers }) }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, shallowRef } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Optimiere Props mit shallowRef für komplexe Objekte
const props = defineProps<{
  question: {
    question: string
    correctAnswer: string
    options: string[]
  }
  currentOptions: string[]
  hiddenOptions: string[]
  disabled: boolean
  remainingJokers: number
  jokerUsedForCurrentQuestion: boolean
  phoneExpertOpinion: {
    expert: string
    message: string
    confidence: number
  } | null
  audienceOpinion: Record<string, number> | null
}>()

// Memoize computed properties
const phoneExpertConfidence = computed(() => props.phoneExpertOpinion?.confidence ?? 0)

// Optimiere Transitions
const transitionGroupProps = shallowRef({
  name: 'fade-shrink',
  tag: 'div',
  class: 'grid grid-cols-1 gap-4 mx-auto w-full',
  moveClass:
    'motion-safe:transition-transform motion-safe:duration-normal motion-safe:ease-[var(--transition-bounce)]',
})

defineEmits<{
  'select-answer': [answer: string]
  'use-fifty-fifty': []
  'use-audience': []
  'use-phone': []
}>()
</script>

<style>
@tailwind utilities;

@layer utilities {
  .fade-shrink-move,
  .fade-shrink-enter-active,
  .fade-shrink-leave-active {
    transition: all var(--transition-speed) var(--transition-bounce);
  }

  .fade-shrink-enter-from,
  .fade-shrink-leave-to {
    opacity: 0;
    transform: scale(0.9);
  }

  .fade-shrink-leave-active {
    position: absolute;
  }
}

/* Reduced motion preferences are handled via Tailwind's motion-reduce utilities */
</style>
