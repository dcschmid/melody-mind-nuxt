<template>
  <div class="print:print-friendly mx-auto max-w-[var(--max-content-width)] p-4 text-center sm:p-8">
    <h1
      id="game-over-title"
      class="motion-safe:animate-fade-in mb-8 text-center text-3xl font-bold text-[rgb(var(--primary-color-rgb))] motion-reduce:animate-none sm:text-4xl"
    >
      {{ $t('game.gameOver.title') }}
    </h1>

    <!-- Player Rankings -->
    <div
      class="motion-safe:animate-fade-in-up mb-8 motion-safe:delay-100 motion-reduce:animate-none"
      role="region"
      aria-labelledby="rankings-title"
    >
      <h2
        id="rankings-title"
        class="mb-4 text-xl font-semibold text-[rgb(var(--secondary-color-rgb))] sm:mb-6 sm:text-2xl"
      >
        {{ $t('game.gameOver.rankings') }}
      </h2>
      <div class="flex flex-col gap-4 sm:gap-6">
        <div
          v-for="(player, index) in sortedPlayers"
          :key="player.name"
          class="flex flex-col items-center gap-4 rounded-lg bg-[rgb(var(--surface-color-rgb))] p-4 motion-safe:transition-transform motion-safe:duration-300 motion-reduce:transition-none sm:flex-row sm:items-stretch sm:p-6"
          :class="{
            'scale-105 bg-gradient-to-r from-[var(--color-gold-dark)] to-[var(--color-gold)] text-white':
              index === 0,
            'hover:shadow-md motion-safe:hover:scale-[1.02] motion-reduce:hover:scale-100':
              index !== 0,
          }"
          role="listitem"
          :aria-label="`${player.name}: ${$t('game.score')} ${player.score}, ${$t('game.gameOver.correctAnswers')} ${player.correctAnswers}`"
        >
          <div
            class="flex h-[44px] w-[44px] items-center justify-center rounded-full bg-[rgb(var(--surface-color-light-rgb))] text-base font-bold sm:text-lg"
            aria-hidden="true"
          >
            <Icon v-if="index === 0" name="material-symbols:trophy" size="32" class="text-white" />
            <Icon
              v-else-if="index === 1"
              name="material-symbols:military-tech"
              size="32"
              class="text-[var(--color-silver)]"
            />
            <Icon
              v-else-if="index === 2"
              name="material-symbols:stars"
              size="32"
              class="text-[var(--color-bronze)]"
            />
            <span v-else>{{ index + 1 }}</span>
          </div>
          <div class="flex-1 text-center sm:text-left">
            <div class="mb-2 text-lg font-bold sm:text-xl" :class="{ 'text-white': index === 0 }">
              {{ player.name }}
            </div>
            <div
              class="flex flex-col items-center justify-center gap-4 sm:flex-row sm:items-start sm:justify-start sm:gap-6"
            >
              <div class="flex flex-col gap-1">
                <div class="text-sm font-medium" :class="{ 'text-white': index === 0 }">
                  {{ $t('game.score') }}
                </div>
                <div
                  class="flex items-center gap-2 text-base font-semibold sm:text-lg"
                  :class="{ 'text-white': index === 0 }"
                >
                  <Icon
                    name="material-symbols:scoreboard"
                    size="24"
                    :class="{
                      'text-white': index === 0,
                      'text-[var(--primary-color-light)]': index !== 0,
                    }"
                  />
                  <span
                    :class="{
                      'text-white': index === 0,
                      'text-[var(--primary-color-light)]': index !== 0,
                    }"
                    >{{ player.score }}</span
                  >
                </div>
              </div>
              <div class="hidden h-6 w-px bg-[rgb(var(--surface-color-light-rgb))] sm:block" />
              <div class="flex flex-col gap-1">
                <div class="text-sm font-medium" :class="{ 'text-white': index === 0 }">
                  {{ $t('game.gameOver.correctAnswers') }}
                </div>
                <div
                  class="flex items-center gap-2 text-base font-semibold sm:text-lg"
                  :class="{ 'text-white': index === 0 }"
                >
                  <Icon
                    name="material-symbols:check-circle"
                    size="24"
                    :class="{
                      'text-white': index === 0,
                      'text-[var(--success-color)]': index !== 0,
                    }"
                  />
                  <span
                    :class="{
                      'text-white': index === 0,
                      'text-[var(--success-color)]': index !== 0,
                    }"
                  >
                    {{ player.correctAnswers }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div
      class="motion-safe:animate-fade-in-up mt-6 flex flex-col justify-center gap-3 motion-safe:delay-200 motion-reduce:animate-none sm:mt-8 sm:flex-row sm:gap-6"
      role="group"
      aria-label="Game actions"
    >
      <Button
        variant="primary"
        full-width
        class-name="sm:w-auto sm:min-w-[180px] h-[50px] min-h-[44px] gap-2"
        aria-label="Play again"
        @click="$emit('playAgain')"
      >
        <Icon name="material-symbols:replay" size="24" aria-hidden="true" />
        <span>{{ $t('game.gameOver.playAgain') }}</span>
      </Button>

      <NuxtLink :to="localePath('/')">
        <Button
          variant="secondary"
          full-width
          class-name="sm:w-auto sm:min-w-[180px] h-[50px] min-h-[44px] gap-2"
          aria-label="Back to main menu"
        >
          <Icon name="material-symbols:home" size="24" aria-hidden="true" />
          <span>{{ $t('game.gameOver.backToMenu') }}</span>
        </Button>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Button from '~/components/ui/Button.vue'

interface Player {
  name: string
  score: number
  correctAnswers: number
}

const props = defineProps<{
  players: Player[]
}>()

const localePath = useLocalePath()

// Sort players by score in descending order
const sortedPlayers = computed(() => {
  return [...props.players].sort((a, b) => b.score - a.score)
})

defineEmits(['playAgain'])
</script>

<style>
@tailwind utilities;

@layer utilities {
  /* Add the animation classes to Tailwind utilities layer */
  .animate-fade-in {
    animation: fade-in 0.5s ease-out;
  }

  .animate-fade-in-up {
    animation: fade-in-up 0.5s ease-out;
    animation-fill-mode: both;
  }

  .delay-100 {
    animation-delay: 0.1s;
  }

  .delay-200 {
    animation-delay: 0.2s;
  }

  @keyframes fade-in {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes fade-in-up {
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
</style>
