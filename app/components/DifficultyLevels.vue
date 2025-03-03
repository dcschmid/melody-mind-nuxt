<template>
  <section
    id="difficulty-levels"
    class="mx-auto w-full max-w-7xl px-4 py-16 sm:px-6 lg:px-8 print:py-8"
    :aria-labelledby="sectionTitleId"
    role="region"
  >
    <!-- Sektions-Überschrift -->
    <h2
      :id="sectionTitleId"
      class="mb-8 text-center text-2xl font-bold leading-tight text-[rgb(var(--text-color-rgb))] md:text-3xl print:text-black print:text-2xl"
    >
      {{ t('gameRules.difficultyLevels.title') }}
    </h2>

    <!-- Einführungstext -->
    <p
      :id="introTextId"
      class="mx-auto mb-12 max-w-prose text-center text-base leading-relaxed text-[rgb(var(--text-color-rgb))] md:text-lg print:text-black print:mb-8"
      aria-live="polite"
    >
      {{ t('gameRules.difficultyLevels.intro') }}
    </p>

    <!-- Schwierigkeitsstufen Grid -->
    <div
      class="mb-16 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 print:mb-10 print:gap-4"
      role="list"
      :aria-labelledby="introTextId"
    >
      <!-- Einzelne Schwierigkeitsstufe -->
      <div
        v-for="level in difficultyLevels"
        :key="level"
        role="listitem"
        class="group/card relative overflow-hidden rounded-xl bg-[rgb(var(--surface-color-rgb))] p-6 shadow-md ring-2 motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none hover:shadow-lg focus-within:ring-4 focus-within:ring-[rgb(var(--focus-color-rgb))] print:shadow-none print:border print:border-gray-300 print:p-4"
        :class="{
          'ring-green-600 dark:ring-green-500 print:ring-green-800': level === 'easy',
          'ring-amber-600 dark:ring-amber-500 print:ring-amber-800': level === 'medium',
          'ring-red-600 dark:ring-red-500 print:ring-red-800': level === 'hard',
        }"
      >
        <!-- Decorative background pattern (purely decorative) -->
        <div
          aria-hidden="true"
          class="absolute inset-0 -z-10 bg-gradient-to-br opacity-5 motion-reduce:hidden print:hidden"
          :class="{
            'from-green-300 to-green-100': level === 'easy',
            'from-amber-300 to-amber-100': level === 'medium',
            'from-red-300 to-red-100': level === 'hard',
          }"
        ></div>

        <!-- Schwierigkeitsstufen-Header -->
        <div class="mb-4 flex items-center gap-4">
          <span
            class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-[rgb(var(--surface-light-color-rgb))] text-xl shadow-sm print:bg-white print:border print:border-gray-300"
            :class="{
              'text-green-600 dark:text-green-500 print:text-green-800': level === 'easy',
              'text-amber-600 dark:text-amber-500 print:text-amber-800': level === 'medium',
              'text-red-600 dark:text-red-500 print:text-red-800': level === 'hard',
            }"
            aria-hidden="true"
          >
            <Icon :name="difficultyIcons[level]" class="h-6 w-6" />
          </span>

          <h3
            :id="`${level}-title`"
            class="text-xl font-semibold leading-tight text-[rgb(var(--text-color-rgb))] print:text-black"
          >
            {{ t(`gameRules.difficultyLevels.levels.${level}.title`) }}
          </h3>
        </div>

        <!-- Beschreibung -->
        <p
          class="text-base leading-relaxed text-[rgb(var(--text-secondary-color-rgb))] print:text-black"
          :aria-labelledby="`${level}-title`"
        >
          {{ t(`gameRules.difficultyLevels.levels.${level}.description`) }}
        </p>
      </div>
    </div>

    <!-- Einführungstext für Titel -->
    <p
      :id="titlesIntroId"
      class="mx-auto mb-12 max-w-prose text-center text-base leading-relaxed text-[rgb(var(--text-color-rgb))] md:text-lg print:text-black print:mb-8"
      aria-live="polite"
    >
      {{ t('gameRules.difficultyLevels.titles.intro') }}
    </p>

    <!-- Erfolge/Titel Grid -->
    <div
      class="mb-16 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 print:mb-10 print:gap-4"
      role="list"
      :aria-labelledby="titlesIntroId"
    >
      <!-- Einzelner Titel -->
      <div
        v-for="title in achievementTitles"
        :key="title"
        role="listitem"
        class="group/card relative overflow-hidden rounded-xl bg-[rgb(var(--surface-color-rgb))] p-6 shadow-md ring-2 motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none hover:shadow-lg focus-within:ring-4 focus-within:ring-[rgb(var(--focus-color-rgb))] print:shadow-none print:border print:border-gray-300 print:p-4"
        :class="{
          'ring-amber-700 dark:ring-amber-600 print:ring-amber-800': title === 'novice',
          'ring-slate-400 dark:ring-slate-300 print:ring-slate-700': title === 'master',
          'ring-amber-400 dark:ring-amber-300 print:ring-amber-600': title === 'legend',
        }"
      >
        <!-- Decorative background pattern (purely decorative) -->
        <div
          aria-hidden="true"
          class="absolute inset-0 -z-10 bg-gradient-to-br opacity-5 motion-reduce:hidden print:hidden"
          :class="{
            'from-amber-700 to-amber-500': title === 'novice',
            'from-slate-400 to-slate-200': title === 'master',
            'from-amber-400 to-amber-200': title === 'legend',
          }"
        ></div>

        <!-- Titel-Header -->
        <div class="mb-4 flex items-center gap-4">
          <span
            class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-[rgb(var(--surface-light-color-rgb))] text-xl shadow-sm print:bg-white print:border print:border-gray-300"
            :class="{
              'text-amber-700 dark:text-amber-600 print:text-amber-800': title === 'novice',
              'text-slate-500 dark:text-slate-400 print:text-slate-700': title === 'master',
              'text-amber-500 dark:text-amber-400 print:text-amber-600': title === 'legend',
            }"
            aria-hidden="true"
          >
            <Icon :name="achievementIcons[title]" class="h-6 w-6" />
          </span>

          <h3
            :id="`${title}-title`"
            class="text-xl font-semibold leading-tight text-[rgb(var(--text-color-rgb))] print:text-black"
          >
            {{ t(`gameRules.difficultyLevels.titles.${title}.title`) }}
          </h3>
        </div>

        <!-- Beschreibung -->
        <p
          class="text-base leading-relaxed text-[rgb(var(--text-secondary-color-rgb))] print:text-black"
          :aria-labelledby="`${title}-title`"
        >
          {{ t(`gameRules.difficultyLevels.titles.${title}.description`) }}
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t } = useI18n()

// Unique IDs für ARIA-Attribute
const sectionTitleId = 'difficulty-levels-title'
const introTextId = 'difficulty-levels-intro'
const titlesIntroId = 'achievement-titles-intro'

// Schwierigkeitsgrade und Errungenschaften
const difficultyLevels = ['easy', 'medium', 'hard'] as const
const achievementTitles = ['novice', 'master', 'legend'] as const

// Icons für Schwierigkeitsgrade
const difficultyIcons = {
  easy: 'material-symbols:stars-outline',
  medium: 'material-symbols:stars',
  hard: 'material-symbols:stars-rounded',
} as const

// Icons für Errungenschaften
const achievementIcons = {
  novice: 'material-symbols:military-tech-outline',
  master: 'material-symbols:military-tech',
  legend: 'material-symbols:military-tech-rounded',
} as const
</script>

<style scoped>
/* Verbesserte Zugänglichkeit für hohen Kontrast */
@media (prefers-contrast: more) {
  section {
    border: 1px solid black !important;
    padding: 2rem !important;
  }

  h2, h3 {
    color: black !important;
    font-weight: bold !important;
    text-decoration: underline !important;
  }

  p {
    color: black !important;
  }

  div[role="listitem"] {
    border: 3px solid black !important;
    background-color: white !important;
    color: black !important;
  }

  [class*="text-green"],
  [class*="text-amber"],
  [class*="text-red"],
  [class*="text-slate"] {
    color: black !important;
  }

  span[aria-hidden="true"] {
    border: 2px solid black !important;
    background-color: white !important;
  }
}

/* Print-Optimierung */
@media print {
  section {
    page-break-inside: avoid !important;
  }

  div[role="list"] {
    page-break-before: auto !important;
  }

  div[role="listitem"] {
    break-inside: avoid !important;
    margin-bottom: 1rem !important;
  }
}
</style>
