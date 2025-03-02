<template>
  <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
    <main class="print:print-friendly mx-auto w-full max-w-[75rem] motion-reduce:transition-none">
      <article class="p-4 md:p-8">
        <h1
          class="mb-8 text-center text-2xl leading-[1.4] font-bold text-[var(--color-primary)] md:text-3xl"
        >
          {{ $t('gameRules.title') }}
        </h1>

        <section aria-labelledby="overview" class="mb-8">
          <h2
            id="overview"
            class="mb-4 text-xl leading-[1.4] font-semibold text-[var(--color-primary)] md:text-2xl"
          >
            {{ $t('gameRules.overview.title') }}
          </h2>
          <p class="text-base leading-[1.6] text-white">
            {{ $t('gameRules.overview.text') }}
          </p>
        </section>

        <section aria-labelledby="difficulty-levels" class="mb-8">
          <h2
            id="difficulty-levels"
            class="mb-4 text-xl leading-[1.4] font-semibold text-[var(--color-primary)] md:text-2xl"
          >
            {{ $t('gameRules.difficultyLevels.title') }}
          </h2>

          <p class="mb-4 text-base leading-[1.6] text-white">
            {{ $t('gameRules.difficultyLevels.intro') }}
          </p>

          <ul class="mb-4 list-disc pl-8">
            <li class="mb-2 text-base leading-[1.6] text-[#f0f0f0]">
              <strong class="font-semibold text-white">{{
                $t('gameRules.difficultyLevels.levels.easy.title')
              }}</strong
              >:
              {{ $t('gameRules.difficultyLevels.levels.easy.description') }}
            </li>
            <li class="mb-2 text-base leading-[1.6] text-[#f0f0f0]">
              <strong class="font-semibold text-white">{{
                $t('gameRules.difficultyLevels.levels.medium.title')
              }}</strong
              >:
              {{ $t('gameRules.difficultyLevels.levels.medium.description') }}
            </li>
            <li class="mb-0 text-base leading-[1.6] text-[#f0f0f0]">
              <strong class="font-semibold text-white">{{
                $t('gameRules.difficultyLevels.levels.hard.title')
              }}</strong
              >:
              {{ $t('gameRules.difficultyLevels.levels.hard.description') }}
            </li>
          </ul>

          <p class="mb-4 text-base leading-[1.6] text-[#f0f0f0]">
            {{ $t('gameRules.difficultyLevels.titles.intro') }}
          </p>

          <ul class="mb-4 list-disc pl-8">
            <li class="mb-2 text-base leading-[1.6] text-[#f0f0f0]">
              <strong class="font-semibold text-white">{{
                $t('gameRules.difficultyLevels.titles.novice.title')
              }}</strong
              >:
              {{ $t('gameRules.difficultyLevels.titles.novice.description') }}
            </li>
            <li class="mb-2 text-base leading-[1.6] text-[#f0f0f0]">
              <strong class="font-semibold text-white">{{
                $t('gameRules.difficultyLevels.titles.master.title')
              }}</strong
              >:
              {{ $t('gameRules.difficultyLevels.titles.master.description') }}
            </li>
            <li class="mb-0 text-base leading-[1.6] text-[#f0f0f0]">
              <strong class="font-semibold text-white">{{
                $t('gameRules.difficultyLevels.titles.legend.title')
              }}</strong
              >:
              {{ $t('gameRules.difficultyLevels.titles.legend.description') }}
            </li>
          </ul>
        </section>

        <section aria-labelledby="points-system" class="mb-8">
          <h2
            id="points-system"
            class="mb-4 text-xl leading-[1.4] font-semibold text-[var(--color-primary)] md:text-2xl"
          >
            {{ $t('gameRules.pointsSystem.title') }}
          </h2>

          <ul class="mb-4 list-disc pl-8">
            <li class="mb-2 text-base leading-[1.6] text-[#f0f0f0]">
              {{ $t('gameRules.pointsSystem.rules.0') }}
            </li>
            <li class="mb-0 text-base leading-[1.6] text-[#f0f0f0]">
              {{ $t('gameRules.pointsSystem.rules.1') }}
            </li>
          </ul>
        </section>

        <section aria-labelledby="golden-lps" class="mb-8">
          <h2
            id="golden-lps"
            class="mb-4 text-xl leading-[1.4] font-semibold text-[var(--color-primary)] md:text-2xl"
          >
            {{ $t('gameRules.goldenRecords.title') }}
          </h2>

          <p class="mb-4 text-base leading-[1.6] text-[#f0f0f0]">
            {{ $t('gameRules.goldenRecords.intro') }}
          </p>

          <ul class="mb-4 list-disc pl-8">
            <li class="mb-2 text-base leading-[1.6] text-[#f0f0f0]">
              <strong class="font-semibold text-white">{{
                $t('gameRules.goldenRecords.rewards.easy')
              }}</strong>
            </li>
            <li class="mb-2 text-base leading-[1.6] text-[#f0f0f0]">
              <strong class="font-semibold text-white">{{
                $t('gameRules.goldenRecords.rewards.medium')
              }}</strong>
            </li>
            <li class="mb-0 text-base leading-[1.6] text-[#f0f0f0]">
              <strong class="font-semibold text-white">{{
                $t('gameRules.goldenRecords.rewards.hard')
              }}</strong>
            </li>
          </ul>
        </section>

        <section aria-labelledby="rankings" class="mb-8">
          <h2
            id="rankings"
            class="mb-4 text-xl leading-[1.4] font-semibold text-[var(--color-primary)] md:text-2xl"
          >
            {{ $t('gameRules.rankings.title') }}
          </h2>

          <p class="mb-4 text-base leading-[1.6] text-[#f0f0f0]">
            {{ $t('gameRules.rankings.text') }}
          </p>

          <ul class="mb-4 list-disc pl-8">
            <li class="mb-2 text-base leading-[1.6] text-[#f0f0f0]">
              {{ $t('gameRules.rankings.lists.0') }}
            </li>
            <li class="mb-0 text-base leading-[1.6] text-[#f0f0f0]">
              {{ $t('gameRules.rankings.lists.1') }}
            </li>
          </ul>
        </section>

        <section aria-labelledby="tips-tricks" class="mb-0">
          <h2
            id="tips-tricks"
            class="mb-4 text-xl leading-[1.4] font-semibold text-[var(--color-primary)] md:text-2xl"
          >
            {{ $t('gameRules.tipsAndTricks.title') }}
          </h2>

          <ul class="mb-4 list-disc pl-8">
            <li class="mb-2 text-base leading-[1.6] text-[#f0f0f0]">
              {{ $t('gameRules.tipsAndTricks.tips.0') }}
            </li>
            <li class="mb-2 text-base leading-[1.6] text-[#f0f0f0]">
              {{ $t('gameRules.tipsAndTricks.tips.1') }}
            </li>
            <li class="mb-2 text-base leading-[1.6] text-[#f0f0f0]">
              {{ $t('gameRules.tipsAndTricks.tips.2') }}
            </li>
            <li class="mb-0 text-base leading-[1.6] text-[#f0f0f0]">
              {{ $t('gameRules.tipsAndTricks.tips.3') }}
            </li>
          </ul>
        </section>
      </article>
    </main>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { useRequestURL } from '#imports'
import { useI18n } from 'vue-i18n'

definePageMeta({})

const { t } = useI18n()
const url = useRequestURL()

useSeoMeta({
  title: computed(() => t('seo.gameRules.title')),
  ogTitle: computed(() => t('seo.gameRules.title')),
  description: computed(() => t('seo.gameRules.description')),
  ogDescription: computed(() => t('seo.gameRules.description')),
  ogUrl: url.href,
  ogType: 'website',
  robots: 'index, follow',
  viewport: 'width=device-width, initial-scale=1',
})
</script>

<!-- Tailwind CSS classes are used directly in the template -->
<style>
/* Print-specific styles that can't be easily handled with Tailwind classes */
@media print {
  h1 {
    font-size: 24px !important;
  }
  h2 {
    font-size: 20px !important;
  }
  li {
    font-size: 14px !important;
  }
  main,
  article {
    padding: 0 !important;
    box-shadow: none !important;
  }
}

/* Unterstützung für hohen Kontrast */
@media (prefers-contrast: more) {
  h1,
  h2 {
    text-shadow: 0 0 1px rgba(0, 0, 0, 0.5);
  }

  strong {
    font-weight: 700 !important;
  }

  ul {
    border-left: 2px solid currentColor !important;
  }
}

/* Unterstützung für reduzierten Bewegungsmodus wird durch Tailwind-Klassen abgedeckt */
</style>
