<template>
  <NuxtLayout :show-header="false" :show-menu="false">
    <main
      class="relative flex min-h-screen items-center justify-center overflow-hidden bg-[var(--color-background)] p-4 md:p-8"
      aria-labelledby="welcome-title"
    >
      <div class="mx-auto w-full max-w-7xl text-center">
        <div class="mb-8 flex justify-center">
          <LanguagePicker />
        </div>
        <h1
          id="welcome-title"
          class="mb-4 text-3xl leading-tight font-bold text-[var(--color-primary)]"
        >
          {{ $t('welcome.title') }}
        </h1>
        <p
          class="mx-auto mb-8 max-w-3xl text-base leading-relaxed text-[var(--color-text-secondary)] md:text-lg"
        >
          {{ $t('intro') }}
        </p>
        <NuxtLinkLocale
          to="/gamehome"
          class="text-md inline-block min-h-[44px] rounded-lg bg-[var(--color-primary)] px-6 py-3 font-semibold text-[var(--color-text-dark)] shadow-md transition-all duration-300 hover:-translate-y-1 hover:bg-[var(--secondary-color-dark)] hover:shadow-lg focus-visible:ring-3 focus-visible:ring-[var(--color-primary)] focus-visible:ring-offset-4 focus-visible:ring-offset-[var(--color-background)] focus-visible:outline-none active:translate-y-0 motion-reduce:transform-none motion-reduce:transition-none md:w-auto md:px-6 md:py-3"
          :aria-label="$t('welcome.start')"
        >
          {{ $t('welcome.start') }}
        </NuxtLinkLocale>
      </div>
    </main>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { useRequestURL } from '#imports'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const url = useRequestURL()

// SEO Meta Tags
useSeoMeta({
  title: computed(() => t('welcome.title')),
  description: computed(() => t('welcome.seo.description')),
  ogTitle: computed(() => t('welcome.title')),
  ogDescription: computed(() => t('welcome.seo.description')),
  ogType: 'website',
  robots: 'index, follow',
  viewport: 'width=device-width, initial-scale=1',
  twitterCard: 'summary_large_image',
  ogUrl: computed(() => url.href),
})

// JSON-LD
useJsonld({
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: computed(() => t('welcome.title')).value,
  description: computed(() => t('welcome.seo.description')).value,
  url: url.href,
  potentialAction: {
    '@type': 'SearchAction',
    target: {
      '@type': 'EntryPoint',
      urlTemplate: `${url.origin}/search?q={search_term_string}`,
    },
    query: 'required name=search_term_string',
  },
})
</script>
