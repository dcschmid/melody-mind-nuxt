<template>
  <NuxtLayout name="default" :show-header="true" :show-menu="true">
    <main
      id="main-content"
      class="print:print-friendly mx-auto w-full max-w-[75rem] p-4 motion-reduce:transition-none md:p-8"
    >
      <section class="mb-8">
        <h1
          tabindex="-1"
          class="mb-8 text-center text-3xl leading-[1.4] font-bold text-[var(--color-primary)]"
        >
          {{ $t('knowledge.title') }}
        </h1>
        <p
          v-if="$t('knowledge.description')"
          class="text-md mx-auto mb-8 max-w-3xl text-center leading-[1.6] text-white"
        >
          {{ $t('knowledge.description') }}
        </p>
      </section>

      <section class="mb-8" role="search">
        <SearchBar
          id="knowledge-search"
          v-model="searchQuery"
          :placeholder="$t('gameHome.searchPlaceholder')"
          class="mx-auto w-full max-w-3xl md:max-w-md lg:max-w-lg xl:max-w-3xl"
        />
      </section>

      <section role="region" aria-labelledby="categories-heading" class="mt-8">
        <h2 id="categories-heading" class="sr-only">
          {{ $t('knowledge.overview') }}
        </h2>
        <div role="list" class="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 md:gap-6">
          <CategoryCard
            v-for="item in filteredKnowledgeItems"
            :key="item._path"
            :headline="item.title"
            :image-url="item.image"
            :category-url="
              localePath(
                `/knowledge/${item._file.split('/')[1]}/${item._file.split('/').pop().replace('.md', '')}`
              )
            "
            :intro-subline="item.description"
            :is-playable="true"
            role="listitem"
            class="animate-fadeIn"
            @select="navigateToKnowledge(item)"
          />
        </div>
      </section>
    </main>
  </NuxtLayout>
</template>

<script setup>
import { queryContent, useAsyncData, useRequestURL } from '#imports'
import { computed, ref, unref } from 'vue'
import { useRouter } from 'vue-router'

const searchQuery = ref('')
const router = useRouter()
const { locale, t } = useI18n()
const localePath = useLocalePath()
const url = useRequestURL()

// SEO Meta Tags
const metaTitle = computed(() => t('knowledge.meta.title'))
const metaDescription = computed(() => t('knowledge.meta.description'))

useSeoMeta({
  title: metaTitle,
  description: metaDescription,
  ogTitle: metaTitle,
  ogDescription: metaDescription,
  ogType: 'website',
  robots: 'index, follow',
  viewport: 'width=device-width, initial-scale=1',
  twitterCard: 'summary_large_image',
  ogUrl: url.href,
})

// Fetch knowledge articles using Nuxt Content
const { data: knowledgeItems } = await useAsyncData('knowledge', () =>
  queryContent('knowledge', locale.value).find()
)

const filteredKnowledgeItems = computed(() => {
  if (!searchQuery.value || !knowledgeItems.value) return knowledgeItems.value || []
  const query = searchQuery.value.toLowerCase()
  return knowledgeItems.value.filter(
    (item) =>
      item.title?.toLowerCase().includes(query) || item.description?.toLowerCase().includes(query)
  )
})

// JSON-LD
const jsonLdData = computed(() => ({
  '@context': 'https://schema.org',
  '@type': 'CollectionPage',
  name: unref(metaTitle),
  description: unref(metaDescription),
  url: url.href,
  mainEntity: {
    '@type': 'ItemList',
    itemListElement: (knowledgeItems.value || []).map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      item: {
        '@type': 'Article',
        name: item.title,
        description: item.description,
        url: localePath(
          `/knowledge/${item._file.split('/')[1]}/${item._file.split('/').pop().replace('.md', '')}`
        ),
      },
    })),
  },
}))

useJsonld(() => unref(jsonLdData))

const navigateToKnowledge = (item) => {
  const lang = item._file.split('/')[1]
  const filename = item._file.split('/').pop().replace('.md', '')
  const path = `/knowledge/${lang}/${filename}`
  router.push(localePath(path))
}
</script>

<style>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@layer utilities {
  .animate-fadeIn {
    animation: fadeIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  }
}

/* Unterstützung für reduzierten Bewegungsmodus */
@media (prefers-reduced-motion: reduce) {
  .animate-fadeIn {
    animation: none !important;
    transform: none !important;
  }
}

/* Unterstützung für hohen Kontrast */
@media (prefers-contrast: more) {
  h1 {
    text-shadow: 0 0 1px rgba(0, 0, 0, 0.5);
  }

  .grid > div {
    border: 1px solid currentColor;
  }
}

/* Print-specific styles */
@media print {
  h1 {
    font-size: 24px !important;
    color: black !important;
  }

  p {
    font-size: 14px !important;
    color: black !important;
  }

  .grid {
    display: block !important;
  }

  .grid > div {
    margin-bottom: 1em !important;
    page-break-inside: avoid;
    border: 1px solid #ddd;
  }
}
</style>
