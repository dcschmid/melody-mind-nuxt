<template>
  <div>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
      <div
        class="min-h-screen bg-[var(--color-surface)] p-4 text-white motion-reduce:transition-none md:p-8"
      >
        <CategoryIntro :category="currentCategory || null" />

        <article
          v-if="currentCategory"
          :data-category="currentCategory?.slug"
          aria-labelledby="difficulty-heading"
          class="mx-auto flex max-w-4xl flex-col items-center gap-8 md:gap-12"
        >
          <CategoryCover
            :image-url="currentCategory.imageUrl"
            :headline="currentCategory.headline"
          />

          <p class="mx-auto max-w-prose text-center text-base leading-[1.6] text-gray-300">
            {{ currentCategory.text }}
          </p>

          <CategoryDifficultySelector :category-slug="currentCategory.slug" />

          <section
            class="mx-auto my-6 flex w-full max-w-3xl flex-col items-center gap-6 print:hidden"
            aria-labelledby="playlist-section-title"
          >
            <h2
              id="playlist-section-title"
              class="flex items-center justify-center gap-2 text-xl font-semibold text-[var(--color-primary)]"
            >
              <Icon name="material-symbols:library-music" aria-hidden="true" class="h-6 w-6" />
              {{ t('category.combined.title') }}
            </h2>

            <p class="max-w-2xl text-center text-base text-gray-300">
              {{ t('category.combined.description', { genre: currentCategory.headline }) }}
            </p>

            <div class="mt-4 flex w-full flex-col gap-8">
              <!-- Music streaming services links -->
              <div
                v-if="
                  currentCategory.spotifyPlaylist ||
                  currentCategory.deezerPlaylist ||
                  currentCategory.appleMusicPlaylist
                "
                role="list"
                aria-labelledby="streaming-services-title"
                class="flex flex-wrap justify-center gap-6 print:hidden"
              >
                <a
                  v-if="currentCategory.spotifyPlaylist"
                  :href="currentCategory.spotifyPlaylist"
                  target="_blank"
                  rel="noopener noreferrer"
                  :aria-label="t('category.playlist.spotify')"
                  role="listitem"
                  class="flex h-16 min-h-[44px] w-16 items-center justify-center rounded-full bg-[#1DB954] text-white shadow hover:shadow-md focus:outline-none focus-visible:ring-4 focus-visible:ring-[#1DB954]/50"
                >
                  <Icon name="mdi:spotify" class="h-16 w-16" aria-hidden="true" />
                </a>

                <a
                  v-if="currentCategory.deezerPlaylist"
                  :href="currentCategory.deezerPlaylist"
                  target="_blank"
                  rel="noopener noreferrer"
                  :aria-label="t('category.playlist.deezer')"
                  role="listitem"
                  class="flex h-16 min-h-[44px] w-16 items-center justify-center rounded-full bg-[#00C7F2] text-white shadow hover:shadow-md focus:outline-none focus-visible:ring-4 focus-visible:ring-[#00C7F2]/50"
                >
                  <Icon name="simple-icons:deezer" class="h-8 w-8" aria-hidden="true" />
                </a>

                <a
                  v-if="currentCategory.appleMusicPlaylist"
                  :href="currentCategory.appleMusicPlaylist"
                  target="_blank"
                  rel="noopener noreferrer"
                  :aria-label="t('category.playlist.apple')"
                  role="listitem"
                  class="flex h-16 min-h-[44px] w-16 items-center justify-center rounded-full bg-[#FA243C] text-white shadow hover:shadow-md focus:outline-none focus-visible:ring-4 focus-visible:ring-[#FA243C]/50"
                >
                  <Icon name="simple-icons:applemusic" class="h-8 w-8" aria-hidden="true" />
                </a>
              </div>

              <!-- Knowledge link -->
              <div v-if="currentCategory.knowledgeUrl" class="mt-4 flex justify-center">
                <NuxtLink
                  :to="localePath(`${currentCategory.knowledgeUrl}`)"
                  :aria-label="t('category.knowledge.link', { genre: currentCategory.headline })"
                  class="group flex min-h-[44px] items-center gap-3 rounded-lg bg-[var(--color-primary)] px-6 py-3 text-white shadow-md hover:bg-[var(--color-primary-dark)] hover:shadow-lg focus:outline-none focus-visible:ring-4 focus-visible:ring-[var(--color-primary)]/50"
                >
                  <Icon
                    name="material-symbols:menu-book"
                    aria-hidden="true"
                    class="h-6 w-6 group-hover:scale-110 motion-reduce:transform-none"
                  />
                  <span class="font-medium">{{ t('category.knowledge.title') }}</span>
                </NuxtLink>
              </div>
            </div>
          </section>
        </article>
      </div>
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
import { useHead, useLocalePath, useSeoMeta } from '#imports'
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'

interface Category {
  slug: string
  headline: string
  introSubline: string
  imageUrl: string
  text: string
  spotifyPlaylist: string
  deezerPlaylist: string
  appleMusicPlaylist: string
  knowledgeUrl: string
}

const { t, locale } = useI18n()
const route = useRoute()
const localePath = useLocalePath()
const categories = ref<Category[]>([])
const hasUsername = ref(false)

const currentCategory = computed(() => {
  return categories.value.find((cat) => cat.slug === route.params.category)
})

useHead({
  title: computed(() =>
    currentCategory.value ? `${currentCategory.value.headline} - Melody Mind` : 'Melody Mind'
  ),
  meta: [
    {
      name: 'description',
      content: computed(() => (currentCategory.value ? currentCategory.value.text : '')),
    },
  ],
})

watch(
  () => currentCategory.value,
  (category) => {
    if (category) {
      useSeoMeta({
        title: computed(() => `${category.headline} - Melody Mind`),
        description: computed(() => category.introSubline),
        ogTitle: computed(() => `${category.headline} - Melody Mind`),
        ogDescription: computed(() => category.introSubline),
        ogType: 'website',
        ogImage: computed(() => category.imageUrl),
        twitterCard: 'summary_large_image',
        twitterImage: computed(() => category.imageUrl),
      })
    }
  },
  { immediate: true }
)

const loadCategories = async () => {
  const cacheKey = `categories_${locale.value}`

  if (categories.value.length > 0) return

  const cached = sessionStorage.getItem(cacheKey)
  if (cached) {
    categories.value = JSON.parse(cached)
    return
  }

  try {
    const data = await import(`../json/${locale.value}_categories.json`)
    categories.value = data.default
    sessionStorage.setItem(cacheKey, JSON.stringify(data.default))
  } catch (error) {
    console.error('Fehler beim Laden der Kategorien:', error)
    categories.value = []
  }
}

onMounted(() => {
  const storedUsername = localStorage.getItem('username')
  if (storedUsername) {
    hasUsername.value = true
  }
  loadCategories()
})
</script>

<style>
/* High contrast mode support */
@media (prefers-contrast: more) {
  a,
  button {
    outline: 2px solid currentColor !important;
    outline-offset: 2px !important;
    text-decoration: underline !important;
    font-weight: 700 !important;
  }

  h2 {
    text-decoration: underline;
    text-underline-offset: 4px;
  }
}

/* Print styles */
@media print {
  article {
    gap: 1rem !important;
  }

  p {
    color: #000 !important;
    font-size: 12pt !important;
  }

  h2 {
    color: #000 !important;
    font-size: 14pt !important;
    font-weight: bold !important;
    margin-bottom: 0.5rem !important;
  }
}
</style>

<!-- No scoped styles needed as we're using Tailwind CSS classes -->
