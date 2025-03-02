<template>
  <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
    <main class="print:print-friendly mx-auto w-full max-w-[75rem] p-4 motion-reduce:transition-none md:p-8">
      <article class="mx-auto max-w-4xl">
        <h1 class="mb-8 text-center text-2xl font-bold leading-[1.4] text-[var(--color-primary)] md:text-3xl">
          {{ $t('legal.privacy.title') }}
        </h1>

        <section class="mb-8 rounded-lg bg-[var(--color-surface)] p-4 shadow transition-all duration-300 print:print-section md:p-8 motion-reduce:transition-none">
          <h2 class="mb-4 text-xl font-semibold leading-[1.4] text-[var(--color-primary)] md:text-2xl">
            {{ $t('legal.privacy.overview.title') }}
          </h2>
          <div class="mb-4 text-base leading-[1.6] text-[#f0f0f0]">
            <h3 class="my-4 text-lg font-semibold leading-[1.4] text-[var(--color-primary)] md:text-xl">
              {{ $t('legal.privacy.overview.general.title') }}
            </h3>
            <p>{{ $t('legal.privacy.overview.general.text') }}</p>
          </div>
        </section>

        <section class="mb-8 rounded-lg bg-[var(--color-surface)] p-4 shadow transition-all duration-300 print:print-section md:p-8 motion-reduce:transition-none">
          <h2 class="mb-4 text-xl font-semibold leading-[1.4] text-[var(--color-primary)] md:text-2xl">
            {{ $t('legal.privacy.dataCollection.title') }}
          </h2>
          <div class="mb-4 text-base leading-[1.6] text-[#f0f0f0]">
            <h3 class="my-4 text-lg font-semibold leading-[1.4] text-[var(--color-primary)] md:text-xl">
              {{ $t('legal.privacy.dataCollection.cookies.title') }}
            </h3>
            <p>{{ $t('legal.privacy.dataCollection.cookies.text') }}</p>

            <h3 class="my-4 text-lg font-semibold leading-[1.4] text-[var(--color-primary)] md:text-xl">
              {{ $t('legal.privacy.dataCollection.analytics.title') }}
            </h3>
            <p>{{ $t('legal.privacy.dataCollection.analytics.text') }}</p>

            <h3 class="my-4 text-lg font-semibold leading-[1.4] text-[var(--color-primary)] md:text-xl">
              {{ $t('legal.privacy.dataCollection.serverLogs.title') }}
            </h3>
            <p>{{ $t('legal.privacy.dataCollection.serverLogs.text') }}</p>
          </div>
        </section>

        <section class="mb-8 rounded-lg bg-[var(--color-surface)] p-4 shadow transition-all duration-300 print:print-section md:p-8 motion-reduce:transition-none">
          <h2 class="mb-4 text-xl font-semibold leading-[1.4] text-[var(--color-primary)] md:text-2xl">
            {{ $t('legal.privacy.gameData.title') }}
          </h2>
          <div class="mb-4 text-base leading-[1.6] text-[#f0f0f0]">
            <h3 class="my-4 text-lg font-semibold leading-[1.4] text-[var(--color-primary)] md:text-xl">
              {{ $t('legal.privacy.gameData.progress.title') }}
            </h3>
            <p>{{ $t('legal.privacy.gameData.progress.intro') }}</p>
            <ul class="my-2 list-disc pl-8 text-[#f0f0f0]">
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.gameData.progress.list.scores') }}
              </li>
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.gameData.progress.list.awards') }}
              </li>
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.gameData.progress.list.rankings') }}
              </li>
            </ul>
            <p>{{ $t('legal.privacy.gameData.progress.purpose') }}</p>

            <h3 class="my-4 text-lg font-semibold leading-[1.4] text-[var(--color-primary)] md:text-xl">
              {{ $t('legal.privacy.gameData.localStorage.title') }}
            </h3>
            <p>{{ $t('legal.privacy.gameData.localStorage.intro') }}</p>
            <ul class="my-2 list-disc pl-8 text-[#f0f0f0]">
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.gameData.localStorage.list.categories') }}
              </li>
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.gameData.localStorage.list.settings') }}
              </li>
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.gameData.localStorage.list.language') }}
              </li>
            </ul>
            <p>{{ $t('legal.privacy.gameData.localStorage.storage') }}</p>

            <h3 class="my-4 text-lg font-semibold leading-[1.4] text-[var(--color-primary)] md:text-xl">
              {{ $t('legal.privacy.gameData.session.title') }}
            </h3>
            <p>{{ $t('legal.privacy.gameData.session.intro') }}</p>
            <ul class="my-2 list-disc pl-8 text-[#f0f0f0]">
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.gameData.session.list.auth') }}
              </li>
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.gameData.session.list.progress') }}
              </li>
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.gameData.session.list.settings') }}
              </li>
            </ul>
          </div>
        </section>

        <section class="mb-8 rounded-lg bg-[var(--color-surface)] p-4 shadow transition-all duration-300 print:print-section md:p-8 motion-reduce:transition-none">
          <h2 class="mb-4 text-xl font-semibold leading-[1.4] text-[var(--color-primary)] md:text-2xl">
            {{ $t('legal.privacy.rights.title') }}
          </h2>
          <div class="mb-4 text-base leading-[1.6] text-[#f0f0f0]">
            <p>{{ $t('legal.privacy.rights.intro') }}</p>
            <ul class="my-2 list-disc pl-8 text-[#f0f0f0]">
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.rights.list.information') }}
              </li>
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.rights.list.correction') }}
              </li>
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.rights.list.restriction') }}
              </li>
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.rights.list.objection') }}
              </li>
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.rights.list.portability') }}
              </li>
            </ul>
          </div>
        </section>

        <section class="mb-8 rounded-lg bg-[var(--color-surface)] p-4 shadow transition-all duration-300 print:print-section md:p-8 motion-reduce:transition-none">
          <h2 class="mb-4 text-xl font-semibold leading-[1.4] text-[var(--color-primary)] md:text-2xl">
            {{ $t('legal.privacy.deletion.title') }}
          </h2>
          <div class="mb-4 text-base leading-[1.6] text-[#f0f0f0]">
            <p>{{ $t('legal.privacy.deletion.intro') }}</p>
            <ul class="my-2 list-disc pl-8 text-[#f0f0f0]">
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.deletion.list.highscores') }}
              </li>
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.deletion.list.results') }}
              </li>
              <li class="mb-2 leading-[1.6]">
                {{ $t('legal.privacy.deletion.list.account') }}
              </li>
            </ul>
            <p>{{ $t('legal.privacy.deletion.local') }}</p>
          </div>
        </section>

        <section class="mb-8 rounded-lg bg-[var(--color-surface)] p-4 shadow transition-all duration-300 print:print-section md:p-8 motion-reduce:transition-none">
          <h2 class="mb-4 text-xl font-semibold leading-[1.4] text-[var(--color-primary)] md:text-2xl">
            {{ $t('legal.privacy.contact.title') }}
          </h2>
          <div class="mb-4 text-base leading-[1.6] text-[#f0f0f0]">
            <p>{{ $t('legal.privacy.contact.text') }}</p>
            <p class="mt-small">
              <span class="font-semibold">{{ $t('legal.privacy.contact.emailLabel') }}:</span>
              <a
                href="mailto:{{ $t('legal.privacy.contact.emailAddress') }}"
                class="rounded text-[var(--color-primary)] transition-colors duration-300 hover:text-[var(--primary-color-dark)] hover:underline focus-visible:outline focus-visible:outline-offset-2 focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] print:print-link motion-reduce:transition-none"
              >
                {{ $t('legal.privacy.contact.emailAddress') }}
              </a>
            </p>
          </div>
        </section>
      </article>
    </main>
  </NuxtLayout>
</template>

<script setup>
import { useSeoMeta } from '#imports'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// SEO Meta Tags
useSeoMeta({
  title: computed(() => t('legal.privacy.meta.title')),
  description: computed(() => t('legal.privacy.meta.description')),
  ogTitle: computed(() => t('legal.privacy.meta.title')),
  ogDescription: computed(() => t('legal.privacy.meta.description')),
  ogType: 'website',
  robots: 'noindex, follow', // Legal pages should not be indexed
})
</script>

<!-- Alle Styles werden durch Tailwind-Utility-Klassen direkt im HTML definiert -->
<!-- Die print-spezifischen Klassen wurden in main.css definiert -->

<style>
/* Unterstützung für hohen Kontrast */
@media (prefers-contrast: more) {
  h1,
  h2,
  h3 {
    text-shadow: 0 0 1px rgba(0, 0, 0, 0.5);
  }

  strong,
  .font-semibold {
    font-weight: 700 !important;
  }

  ul {
    border-left: 2px solid currentColor !important;
  }

  a {
    text-decoration: underline !important;
    font-weight: 700 !important;
  }

  section {
    border: 1px solid currentColor !important;
  }
}

/* Unterstützung für reduzierten Bewegungsmodus */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}

/* Print-specific styles that can't be easily handled with Tailwind classes */
@media print {
  h1 {
    font-size: 24px !important;
    color: black !important;
  }
  h2 {
    font-size: 20px !important;
    color: black !important;
  }
  h3 {
    font-size: 18px !important;
    color: black !important;
  }
  p, li {
    font-size: 14px !important;
    color: black !important;
  }
  section {
    page-break-inside: avoid;
    border-bottom: 1px solid #ddd;
    padding-bottom: 1em !important;
    margin-bottom: 1em !important;
  }
  a {
    text-decoration: underline !important;
    color: #000 !important;
  }
}
</style>
