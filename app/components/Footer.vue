<template>
  <footer
    class="border-t border-[rgb(var(--border-color-rgb))] bg-[rgb(var(--surface-color-rgb))] py-12 print:border-t-2 print:border-black print:bg-white print:py-6"
    role="contentinfo"
  >
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4 print:gap-4">
        <!-- Logo und Kurzbeschreibung -->
        <div class="flex flex-col space-y-4">
          <div class="flex items-center">
            <Icon
              name="material-symbols:music-note"
              class="mr-2 h-6 w-6 text-[rgb(var(--primary-color-rgb))] print:text-black"
              aria-hidden="true"
            />
            <span class="text-lg font-bold text-[rgb(var(--text-color-rgb))] print:text-black"
              >Melody Mind</span
            >
          </div>
          <p class="text-base text-[rgb(var(--text-secondary-color-rgb))] print:text-black">
            {{ $t('footer.description') }}
          </p>
        </div>

        <!-- Interne Links -->
        <div>
          <h2
            class="mb-4 text-base font-semibold text-[rgb(var(--text-color-rgb))] print:font-bold print:text-black"
          >
            {{ $t('footer.links') }}
          </h2>
          <ul class="space-y-3">
            <li v-for="(link, index) in footerLinks" :key="index">
              <NuxtLink
                :to="localePath(link.to)"
                class="inline-flex items-center text-base text-[rgb(var(--text-secondary-color-rgb))] hover:text-[rgb(var(--primary-color-rgb))] focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[rgb(var(--focus-color-rgb))] motion-safe:transition-colors motion-safe:duration-300 print:text-black print:underline"
              >
                {{ $t(link.title) }}
              </NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Externe Links -->
        <div>
          <h2
            class="mb-4 text-base font-semibold text-[rgb(var(--text-color-rgb))] print:font-bold print:text-black"
          >
            {{ $t('footer.resources') }}
          </h2>
          <ul class="space-y-3">
            <li v-for="(externalLink, index) in externalLinks" :key="`ext-${index}`">
              <a
                :href="externalLink.url"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center text-base text-[rgb(var(--text-secondary-color-rgb))] hover:text-[rgb(var(--primary-color-rgb))] focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[rgb(var(--focus-color-rgb))] motion-safe:transition-colors motion-safe:duration-300 print:text-black print:underline"
                :aria-label="`${$t(externalLink.title)} (${$t('common.opensInNewTab')})`"
              >
                {{ $t(externalLink.title) }}
                <Icon
                  name="heroicons:arrow-top-right-on-square"
                  class="ml-1 h-4 w-4 print:text-black"
                  aria-hidden="true"
                />
                <span class="sr-only">{{ $t('common.opensInNewTab') }}</span>
              </a>
            </li>
          </ul>
        </div>

        <!-- Sprachauswahl -->
        <div>
          <h2
            class="mb-4 text-base font-semibold text-[rgb(var(--text-color-rgb))] print:font-bold print:text-black"
          >
            {{ $t('common.selectLanguage') }}
          </h2>
          <div class="flex flex-wrap gap-2">
            <NuxtLink
              v-for="locale in availableLocales"
              :key="locale"
              :to="switchLocalePath(locale)"
              class="inline-flex items-center rounded-md border border-[rgb(var(--border-color-rgb))] bg-[rgb(var(--surface-light-color-rgb))] px-3 py-2 text-sm text-[rgb(var(--text-color-rgb))] hover:bg-[rgb(var(--surface-hover-color-rgb))] focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[rgb(var(--focus-color-rgb))] motion-safe:transition-colors motion-safe:duration-300 print:border-black print:bg-white print:text-black"
              :aria-label="$t('languages.' + locale)"
              :aria-current="$i18n.locale === locale ? 'true' : undefined"
            >
              {{ $t('languages.' + locale) }}
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- Trennlinie -->
      <div
        class="my-8 h-px w-full bg-[rgb(var(--border-color-rgb))] print:my-4 print:h-0.5 print:bg-black"
        aria-hidden="true"
      ></div>

      <!-- Copyright und Social Media -->
      <div class="flex flex-col items-center justify-between gap-4 sm:flex-row">
        <p class="text-base text-[rgb(var(--text-secondary-color-rgb))] print:text-black">
          &copy; {{ new Date().getFullYear() }} Melody Mind. {{ $t('footer.allRightsReserved') }}
        </p>

        <!-- Social Media Links -->
        <div class="flex space-x-4 print:hidden">
          <a
            v-for="(social, index) in socialLinks"
            :key="index"
            :href="social.url"
            target="_blank"
            rel="noopener noreferrer"
            class="flex h-10 w-10 items-center justify-center rounded-full bg-[rgb(var(--surface-light-color-rgb))] text-[rgb(var(--text-secondary-color-rgb))] hover:bg-[rgb(var(--primary-light-color-rgb))] hover:text-[rgb(var(--primary-color-rgb))] focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[rgb(var(--focus-color-rgb))] motion-safe:transition-colors motion-safe:duration-300"
            :aria-label="social.name + ' ' + $t('common.opensInNewTab')"
          >
            <Icon :name="social.icon" class="h-5 w-5" aria-hidden="true" />
            <span class="sr-only">{{ social.name }} ({{ $t('common.opensInNewTab') }})</span>
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { useI18n, useLocalePath, useSwitchLocalePath } from '#i18n'

// Importieren Sie die localePath-Funktion
const localePath = useLocalePath()
const switchLocalePath = useSwitchLocalePath()
const { availableLocales } = useI18n()

// Definieren Sie hier Ihre Footer-Links
const footerLinks = [
  { title: 'footer.privacy', to: '/privacy' },
  { title: 'footer.terms', to: '/terms' },
  { title: 'footer.imprint', to: '/imprint' },
  { title: 'footer.gameRules', to: '/game-rules' },
]

// Externe Links
const externalLinks = [
  { title: 'footer.github', url: 'https://github.com/dcschmid/melody-mind-nuxt' },
  { title: 'footer.documentation', url: 'https://docs.example.com' },
]

// Social Media Links
const socialLinks = [
  { name: 'GitHub', icon: 'mdi:github', url: 'https://github.com/dcschmid/melody-mind-nuxt' },
  { name: 'Twitter', icon: 'mdi:twitter', url: 'https://twitter.com' },
  { name: 'Instagram', icon: 'mdi:instagram', url: 'https://instagram.com' },
]
</script>

<style scoped>
/* Verbesserte Zugänglichkeit für hohen Kontrast */
@media (prefers-contrast: more) {
  footer {
    background-color: black !important;
    border-top: 3px solid white !important;
  }

  a,
  h2,
  p {
    color: white !important;
  }

  a {
    text-decoration: underline !important;
    outline: 2px solid white !important;
    outline-offset: 2px !important;
    padding: 2px !important;
  }

  a:focus,
  a:hover {
    background-color: white !important;
    color: black !important;
    outline-width: 3px !important;
  }

  div[class*='h-px'] {
    background-color: white !important;
    height: 3px !important;
  }

  [class*='rounded'] {
    border: 2px solid white !important;
  }
}

/* Print-Optimierung */
@media print {
  footer {
    page-break-inside: avoid !important;
    border-top: 2px solid black !important;
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
  }

  a {
    text-decoration: underline !important;
    color: black !important;
  }

  h2 {
    font-weight: bold !important;
    font-size: 1rem !important;
  }

  p {
    font-size: 0.9rem !important;
  }
}
</style>
