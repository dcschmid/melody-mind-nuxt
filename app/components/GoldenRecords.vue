<template>
  <RulesSection id="golden-lps">
    <template #title>
      <span
        class="mb-8 block text-center text-xl leading-tight font-bold text-[rgb(var(--text-color-rgb))] print:text-black"
      >
        {{ $t('gameRules.goldenRecords.title') }}
      </span>
    </template>

    <!-- Einführungstext mit hervorgehobenen Elementen -->
    <p
      class="mx-auto mb-6 max-w-prose text-base leading-relaxed text-[rgb(var(--text-color-rgb))] print:text-black"
      aria-live="polite"
    >
      <i18n-t keypath="gameRules.goldenRecords.intro" tag="span">
        <template #0>
          <span class="font-semibold text-[rgb(var(--primary-color-rgb))] motion-safe:transition-colors motion-safe:duration-300 print:text-black print:underline print:font-bold">
          </span>
        </template>
      </i18n-t>
    </p>

    <!-- Auflistung der Belohnungen mit verbesserten Zugänglichkeitsattributen -->
    <RulesList :title="$t('gameRules.goldenRecords.rewardsListTitle')" class="mb-8 print:mb-6">
      <li
        v-for="(difficulty, index) in ['easy', 'medium', 'hard']"
        :key="difficulty"
        class="group mb-3 last:mb-0 print:mb-2"
      >
        <span
          class="text-base leading-normal text-[rgb(var(--text-secondary-color-rgb))] group-focus-within:text-[rgb(var(--text-color-rgb))] group-hover:text-[rgb(var(--text-color-rgb))] motion-safe:transition-colors motion-safe:duration-300 print:text-black"
          :aria-label="$t(`gameRules.goldenRecords.rewards.${difficulty}AccessibleLabel`)"
        >
          {{ $t(`gameRules.goldenRecords.rewards.${difficulty}`) }}
        </span>

        <!-- Badge für den Schwierigkeitsgrad -->
        <span
          class="ml-2 inline-flex items-center rounded-full px-2 py-1 text-xs font-medium print:border print:border-black"
          :class="{
            'bg-[rgba(var(--success-color-rgb),0.2)] text-[rgb(var(--success-color-rgb))] print:bg-white print:text-black':
              difficulty === 'easy',
            'bg-[rgba(var(--highlight-color-rgb),0.2)] text-[rgb(var(--highlight-color-rgb))] print:bg-white print:text-black':
              difficulty === 'medium',
            'bg-[rgba(var(--error-color-rgb),0.2)] text-[rgb(var(--error-color-rgb))] print:bg-white print:text-black':
              difficulty === 'hard',
          }"
          aria-hidden="true"
        >
          {{ $t(`gameRules.difficultyLevels.levels.${difficulty}.title`) }}
        </span>
      </li>
    </RulesList>

    <!-- Zusätzlicher Abschlusshinweis mit besserer Erkennbarkeit -->
    <div
      class="mx-auto max-w-prose rounded-lg border border-[rgba(var(--primary-color-rgb),0.2)] bg-[rgba(var(--surface-color-rgb),0.6)] p-4 text-center backdrop-blur-xs print:border-2 print:border-black print:bg-white"
      role="note"
      aria-label="Wichtiger Hinweis"
    >
      <p class="mb-0 text-base leading-relaxed text-[rgb(var(--text-color-rgb))] print:text-black">
        <Icon
          name="material-symbols:info-outline"
          class="mr-1 inline-block text-[rgb(var(--primary-color-rgb))] print:text-black"
          aria-hidden="true"
        />
        {{ $t('gameRules.goldenRecords.note') }}
      </p>
    </div>
  </RulesSection>
</template>

<script setup>
// Keine spezielle Logik erforderlich
</script>

<style lang="scss" scoped>
/* Unterstützung für hohen Kontrast-Modus */
@media (prefers-contrast: more) {
  span[class*='text-[rgb(var(--primary-color-rgb))]'] {
    background-color: black !important;
    color: white !important;
    border-radius: 0.125rem !important;
    padding: 0.125rem 0.25rem !important;
  }

  [role='note'] {
    background-color: black !important;
    border: 3px solid white !important;
  }

  .group:hover span,
  .group:focus-within span {
    color: white !important;
  }

  [class*='rounded-full'] {
    border: 2px solid white !important;
  }

  [class*='bg-[rgba(var'] {
    background-color: black !important;
    color: white !important;
  }
}
</style>
