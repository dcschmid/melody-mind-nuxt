<template>
  <NuxtLayout name="default" :show-header="true" :show-menu="true">
    <main
      id="main-content"
      class="mx-auto w-full max-w-[75rem] px-4 py-8 sm:px-6 md:px-8 md:py-12 print:print-friendly motion-reduce:transition-none"
    >
      <!-- Intro Section -->
      <section class="mb-10 md:mb-12">
        <h1
          tabindex="-1"
          class="mb-6 text-center text-2xl font-bold text-white leading-[1.4] sm:text-3xl md:mb-8 md:text-4xl"
        >
          {{ $t('gameHome.title') }}
        </h1>
        <p
          v-if="$t('gameHome.description')"
          class="mx-auto mb-6 max-w-3xl text-center text-base leading-[1.6] text-[#f0f0f0] md:text-lg"
        >
          {{ $t('gameHome.description') }}
        </p>
      </section>

      <!-- Search Section -->
      <section
        role="search"
        class="mx-auto mb-10 max-w-2xl md:mb-12"
        :aria-label="$t('gameHome.searchCategories')"
      >
        <SearchBar
          id="category-search"
          v-model="searchQuery"
          :placeholder="$t('gameHome.searchPlaceholder')"
        />
      </section>

      <!-- Categories Section -->
      <section role="region" aria-labelledby="categories-heading" class="mb-8">
        <h2 id="categories-heading" class="sr-only">
          {{ $t('gameHome.categoriesTitle') }}
        </h2>

        <!-- Empty State Message -->
        <div
          v-if="filteredCategories.length === 0"
          class="rounded-lg bg-[#141414] py-16 text-center shadow-sm dark:bg-[#1a1a1a]"
        >
          <Icon
            name="material-symbols:search-off-rounded"
            size="48"
            class="mb-4 text-[rgb(130,87,229)]"
            aria-hidden="true"
          />
          <p class="mb-2 text-lg font-medium text-white">
            {{ $t('gameHome.noResults') }}
          </p>
          <p class="text-base text-[#f0f0f0]">
            {{ $t('gameHome.tryAnotherSearch') }}
          </p>
          <button
            class="mt-6 min-h-[44px] rounded-full bg-[rgb(130,87,229)] px-6 py-2 text-white transition-colors duration-300 hover:bg-[#6d46c4] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgb(130,87,229)] focus-visible:ring-offset-2 motion-reduce:transition-none"
            :aria-label="$t('gameHome.clearSearch')"
            @click="searchQuery = ''"
          >
            {{ $t('common.clearSearch') }}
          </button>
        </div>

        <!-- Categories Grid -->
        <div
          v-else
          role="list"
          class="grid grid-cols-1 gap-6 sm:grid-cols-2 md:gap-8 lg:grid-cols-3"
        >
          <CategoryCard
            v-for="category in filteredCategories"
            :key="category.slug"
            :headline="category.headline"
            :image-url="category.imageUrl"
            :category-url="localePath(category.categoryUrl)"
            :is-playable="category.isPlayable"
            :intro-subline="category.introSubline"
            role="listitem"
            @select="navigateToCategory(category)"
          />
        </div>
      </section>
    </main>
  </NuxtLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRequestURL } from '#imports'

const router = useRouter()

const { searchQuery, filteredCategories, loadCategories } = useCategories()
const { locale, t } = useI18n()
const localePath = useLocalePath()
const url = useRequestURL()

// SEO Metadaten
useSeoMeta({
  title: computed(() => t('gameHome.title')),
  ogTitle: computed(() => t('gameHome.title')),
  description: computed(() => t('gameHome.description')),
  ogDescription: computed(() => t('gameHome.description')),
  ogType: 'website',
  robots: 'index, follow',
  viewport: 'width=device-width, initial-scale=1',
  twitterCard: 'summary_large_image',
  ogUrl: computed(() => url.href),
})

// Navigation zu einer Kategorie
const navigateToCategory = (category) => {
  if (category.isPlayable) {
    router.push(localePath(category.categoryUrl))
  }
}

// Kategorien beim Laden der Seite abrufen
onMounted(() => {
  loadCategories(locale.value)
  // Fokus auf die Überschrift setzen für bessere Accessibility
  document.querySelector('h1')?.focus()
})
</script>

<style scoped>
/* Zusätzliche Styles für Kontrast-Modus, die nicht mit Tailwind abgedeckt werden können */
@media (prefers-contrast: more) {
  h1,
  h2 {
    text-shadow: 0 0 1px rgba(0, 0, 0, 0.5);
  }
}
</style>
