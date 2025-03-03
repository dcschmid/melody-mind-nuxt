<template>
  <section
    class="mb-10 flex w-full flex-col items-center gap-8 print:px-0 print:text-black"
    aria-labelledby="difficulty-heading"
  >
    <!-- Game Mode Selection -->
    <div class="mb-2 flex flex-col items-center gap-4">
      <h2
        id="difficulty-heading"
        class="text-center text-[clamp(1.75rem,2.2vw+1rem,2rem)] font-bold text-[rgb(130,87,229)] contrast-more:underline contrast-more:decoration-[rgb(130,87,229)] contrast-more:underline-offset-4 print:text-xl print:text-black"
      >
        {{ $t('category.difficulty.title') }}
      </h2>

      <!-- Mode Toggle Buttons -->
      <div
        class="flex flex-wrap justify-center gap-4"
        role="radiogroup"
        aria-label="$t('category.mode.select')"
      >
        <Button
          variant="secondary"
          :class="
            !isMultiplayer
              ? 'bg-[rgb(130,87,229)] text-white ring-2 ring-[rgb(130,87,229)]'
              : 'bg-[#f0f0f0] text-[#333] ring-2 ring-[#f0f0f0]'
          "
          :aria-pressed="!isMultiplayer"
          :aria-checked="!isMultiplayer"
          role="radio"
          :aria-label="$t('category.mode.singleplayer')"
          class-name="min-h-[3rem] min-w-[8rem] text-md font-medium motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none"
          @click="isMultiplayer = false"
        >
          <Icon
            name="mdi:account"
            size="24"
            aria-hidden="true"
            class="mr-2 motion-safe:transition-transform motion-safe:duration-300 motion-safe:group-hover:scale-110 motion-reduce:transform-none"
          />
          <span>{{ $t('category.mode.singleplayer') }}</span>
        </Button>

        <Button
          variant="secondary"
          :class="
            isMultiplayer
              ? 'bg-[rgb(130,87,229)] text-white ring-2 ring-[rgb(130,87,229)]'
              : 'bg-[#f0f0f0] text-[#333] ring-2 ring-[#f0f0f0]'
          "
          :aria-pressed="isMultiplayer"
          :aria-checked="isMultiplayer"
          role="radio"
          :aria-label="$t('category.mode.multiplayer')"
          class-name="min-h-[3rem] min-w-[8rem] text-md font-medium motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none group"
          @click="isMultiplayer = true"
        >
          <Icon
            name="mdi:account-group"
            size="24"
            aria-hidden="true"
            class="mr-2 motion-safe:transition-transform motion-safe:duration-300 motion-safe:group-hover:scale-110 motion-reduce:transform-none"
          />
          <span>{{ $t('category.mode.multiplayer') }}</span>
        </Button>
      </div>
    </div>

    <!-- Difficulty Selection Buttons -->
    <div
      class="grid w-full max-w-2xl grid-cols-1 gap-4 px-4 sm:grid-cols-3 print:grid-cols-3 print:gap-2"
      role="group"
      aria-labelledby="difficulty-heading"
    >
      <NuxtLink
        v-for="difficulty in ['easy', 'medium', 'hard']"
        :key="difficulty"
        v-slot="{ navigate }"
        :to="getDifficultyPath(difficulty)"
        custom
      >
        <Button
          variant="primary"
          :aria-label="$t(`category.difficulty.${difficulty}.label`)"
          class-name="min-h-[3.5rem] w-full text-md font-semibold
                        motion-safe:transition-all motion-safe:duration-300 motion-safe:hover:translate-y-[-0.25rem] motion-safe:hover:shadow-lg
                        motion-safe:active:translate-y-[-0.125rem] motion-safe:active:shadow-md
                        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgb(130,87,229)] focus-visible:ring-offset-4
                        motion-reduce:transform-none motion-reduce:transition-none
                        print:border print:border-gray-300 print:shadow-none print:text-black
                        group"
          @click="navigate"
        >
          <Icon
            :name="getDifficultyIcon(difficulty)"
            size="28"
            aria-hidden="true"
            class="mr-2 motion-safe:transition-transform motion-safe:duration-300 motion-safe:group-hover:scale-125 motion-reduce:transform-none"
          />
          <span>{{ $t(`category.difficulty.${difficulty}`) }}</span>
        </Button>
      </NuxtLink>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Button from '~/components/ui/Button.vue'

const props = defineProps<{
  categorySlug: string
}>()

const { t } = useI18n()
const localePath = useLocalePath()
const isMultiplayer = ref(false)

/**
 * Generiert den Pfad zur Schwierigkeitsstufe basierend auf dem ausgewählten Spielmodus
 * @param difficulty - Die Schwierigkeitsstufe ('easy', 'medium', 'hard')
 * @returns Der lokalisierte Pfad zur Spielseite
 */
const getDifficultyPath = (difficulty: string) => {
  const basePath = isMultiplayer.value ? '/multiplayer/game-' : '/game-'
  return localePath(`${basePath}${props.categorySlug}/${difficulty}`)
}

/**
 * Gibt das passende Icon für die Schwierigkeitsstufe zurück
 * @param difficulty - Die Schwierigkeitsstufe ('easy', 'medium', 'hard')
 * @returns Der Name des Icons
 */
const getDifficultyIcon = (difficulty: string): string => {
  switch (difficulty) {
    case 'easy':
      return 'mdi:star-outline'
    case 'medium':
      return 'mdi:star-half-full'
    case 'hard':
      return 'mdi:star'
    default:
      return 'mdi:play-outline'
  }
}
</script>

<style>
/* High contrast mode support */
@media (prefers-contrast: more) {
  #difficulty-heading {
    text-decoration: underline !important;
    text-decoration-color: rgb(130, 87, 229) !important;
    text-underline-offset: 4px !important;
  }

  button {
    outline: 2px solid currentColor !important;
    outline-offset: 2px !important;
  }
}

/* Print styles */
@media print {
  section {
    padding: 0 !important;
    color: black !important;
  }

  h2 {
    font-size: 18pt !important;
    color: black !important;
    margin-bottom: 12pt !important;
  }

  button {
    border: 1px solid #333 !important;
    color: black !important;
    background: white !important;
  }

  p {
    font-size: 12pt !important;
    line-height: 1.5 !important;
    color: black !important;
  }
}
</style>
