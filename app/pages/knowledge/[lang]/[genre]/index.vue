<template>
  <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
    <div v-if="genre" class="min-h-screen text-white">
      <div class="mx-auto flex max-w-4xl flex-col items-center gap-8">
        <!-- Main Content -->
        <div class="text-center text-base">
          <h1 class="mb-6 text-3xl leading-tight font-bold text-[var(--color-primary)]">
            {{ genre.title }}
          </h1>
          <UnLazyImage
            :src="genre.image"
            :alt="genre.title"
            class="mx-auto aspect-square w-full max-w-[300px] rounded object-cover shadow"
            :thumbhash="thumbHash"
            auto-sizes
            loading="lazy"
          />

          <div class="mt-6 text-base leading-[1.6]">
            {{ genre.description }}
          </div>
        </div>

        <article class="prose prose-invert print:prose-black w-full print:text-black">
          <ContentRenderer :value="genre" />
        </article>

        <!-- Music Links -->
        <div
          v-if="
            category?.spotifyPlaylist || category?.deezerPlaylist || category?.appleMusicPlaylist
          "
          class="mb-8 w-full print:hidden"
          role="region"
          :aria-label="$t('knowledge.playlists')"
        >
          <div>
            <h4
              id="streaming-services-title"
              class="mb-6 flex items-center gap-2 text-2xl leading-tight font-bold text-[var(--color-primary)]"
            >
              <Icon name="material-symbols:headphones" aria-hidden="true" />
              {{ $t('knowledge.playAndListen') }}
            </h4>
            <p class="mb-8 text-base leading-normal text-gray-300">
              {{ $t('knowledge.playlist.description', { genre: genre.title }) }}
            </p>

            <!-- Playlist Links -->
            <div
              class="perspective-1000 mt-6 flex justify-center gap-8"
              role="list"
              aria-labelledby="streaming-services-title"
            >
              <a
                v-if="category?.spotifyPlaylist"
                :href="category.spotifyPlaylist"
                target="_blank"
                rel="noopener noreferrer"
                class="relative flex h-16 min-h-[44px] w-16 items-center justify-center overflow-hidden rounded border border-white/10 backdrop-blur-sm transition-all duration-300 ease-in-out hover:translate-y-[-4px] hover:shadow-lg focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white motion-reduce:transform-none motion-reduce:transition-none"
                :aria-label="$t('knowledge.playlist.spotify')"
                role="listitem"
              >
                <span
                  class="absolute inset-0 bg-gradient-to-br from-[#1DB954] via-[#1ed760] to-[#25f971] opacity-85 transition-all duration-300 ease-out hover:opacity-100 motion-reduce:transition-none"
                />
                <Icon
                  name="mdi:spotify"
                  size="28"
                  aria-hidden="true"
                  class="relative z-[1] text-black drop-shadow-sm transition-all duration-300 ease-in-out hover:scale-110 hover:drop-shadow-md motion-reduce:transform-none motion-reduce:transition-none"
                />
              </a>
              <a
                v-if="category?.deezerPlaylist"
                :href="category.deezerPlaylist"
                target="_blank"
                rel="noopener noreferrer"
                class="relative flex h-16 min-h-[44px] w-16 items-center justify-center overflow-hidden rounded border border-white/10 backdrop-blur-sm transition-all duration-300 ease-in-out hover:translate-y-[-4px] hover:shadow-lg focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white motion-reduce:transform-none motion-reduce:transition-none"
                :aria-label="$t('knowledge.playlist.deezer')"
                role="listitem"
              >
                <span
                  class="absolute inset-0 bg-gradient-to-br from-[var(--color-primary)] via-[var(--color-primary-light)] to-[var(--color-highlight)] opacity-85 transition-all duration-300 ease-out hover:opacity-100 motion-reduce:transition-none"
                />
                <Icon
                  name="simple-icons:deezer"
                  size="28"
                  aria-hidden="true"
                  class="relative z-[1] text-black drop-shadow-sm transition-all duration-300 ease-in-out hover:scale-110 hover:drop-shadow-md motion-reduce:transform-none motion-reduce:transition-none"
                />
              </a>
              <a
                v-if="category?.appleMusicPlaylist"
                :href="category.appleMusicPlaylist"
                target="_blank"
                rel="noopener noreferrer"
                class="relative flex h-16 min-h-[44px] w-16 items-center justify-center overflow-hidden rounded border border-white/10 backdrop-blur-sm transition-all duration-300 ease-in-out hover:translate-y-[-4px] hover:shadow-lg focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white motion-reduce:transform-none motion-reduce:transition-none"
                :aria-label="$t('knowledge.playlist.apple')"
                role="listitem"
              >
                <span
                  class="absolute inset-0 bg-gradient-to-br from-[var(--color-error)] via-[var(--color-error-dark)] to-[#ff6b7f] opacity-85 transition-all duration-300 ease-out hover:opacity-100 motion-reduce:transition-none"
                />
                <Icon
                  name="simple-icons:applemusic"
                  size="28"
                  aria-hidden="true"
                  class="relative z-[1] text-black drop-shadow-sm transition-all duration-300 ease-in-out hover:scale-110 hover:drop-shadow-md motion-reduce:transform-none motion-reduce:transition-none"
                />
              </a>
            </div>

            <!-- Play Button -->
            <NuxtLink
              v-if="genre.isPlayable"
              :to="gameUrl"
              class="mx-auto mt-6 flex min-h-[44px] w-auto items-center gap-2 rounded bg-gradient-to-br from-[var(--color-primary)] via-[var(--color-primary-light)] to-[var(--color-highlight)] p-2 text-sm font-bold text-black no-underline shadow transition-all duration-300 ease-in-out hover:scale-105 hover:shadow-lg focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white active:scale-95 motion-reduce:transform-none motion-reduce:transition-none"
            >
              <Icon name="i-mdi:play-outline" size="48" :aria-hidden="true" />
              {{ $t('knowledge.playNow') }}
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="error" class="container p-8 text-center text-white">
      <p class="text-lg">
        {{ error }}
      </p>
    </div>
    <div v-else class="container p-8 text-center text-white">
      <p class="text-lg">
        {{ $t('knowledge.loading') }}
      </p>
    </div>
  </NuxtLayout>
</template>

<script setup>
import { queryContent, useHead, useRequestURL, useSeoMeta } from '#imports'
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useThumbHash } from '~/composables/useThumbHash'

const route = useRoute()
const url = useRequestURL()

const genre = ref(null)
const category = ref(null)
const gameUrl = ref('')
const error = ref(null)

const { getThumbHash } = useThumbHash()

// ThumbHash für das Genre-Bild abrufen
const thumbHash = computed(() => (genre.value?.image ? getThumbHash(genre.value.image) : undefined))

const loadContent = async () => {
  try {
    error.value = null
    const { lang, genre: genreSlug } = route.params

    // Try to load the specific content
    const content = await queryContent()
      .where({ _path: `/knowledge/${lang}/${genreSlug}` })
      .findOne()

    if (!content) {
      throw new Error(`Content not found at path: /knowledge/${lang}/${genreSlug}`)
    }

    genre.value = content

    // Set category from content metadata
    if (genre.value && genre.value.category) {
      category.value = genre.value.category
    }

    // Set the game URL
    if (category.value) {
      gameUrl.value = `/${lang}/${genreSlug}`
    }
  } catch (err) {
    error.value = err.message || 'Content not found'
  }
}

// SEO Meta Tags
watch(genre, (newGenre) => {
  if (newGenre) {
    // Konvertiere relative Bild-URL zu absoluter URL
    const absoluteImageUrl = computed(() =>
      newGenre.image?.startsWith('http') ? newGenre.image : `${url.origin}${newGenre.image}`
    )

    useSeoMeta({
      title: computed(() => `${newGenre.title} - MelodyMind`),
      description: computed(() => newGenre.description),
      ogTitle: computed(() => `${newGenre.title} - MelodyMind`),
      ogDescription: computed(() => newGenre.description),
      ogType: 'article',
      ogImage: absoluteImageUrl,
      ogUrl: computed(() => url.href),
      twitterCard: 'summary_large_image',
      twitterTitle: computed(() => `${newGenre.title} - MelodyMind`),
      twitterDescription: computed(() => newGenre.description),
      twitterImage: absoluteImageUrl,
      canonical: computed(() => url.href),
      keywords: computed(() => newGenre.keywords?.join(', ')),
      author: computed(() => newGenre.author || 'MelodyMind'),
      'article:published_time': computed(() => newGenre.createdAt),
      'article:modified_time': computed(() => newGenre.updatedAt),
      'og:locale': computed(() => newGenre.locale),
      'og:site_name': 'MelodyMind',
    })

    // Add structured data
    useHead({
      script: [
        {
          type: 'application/ld+json',
          children: computed(() =>
            JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'Article',
              headline: newGenre.title,
              description: newGenre.description,
              image: absoluteImageUrl.value,
              datePublished: newGenre.createdAt,
              dateModified: newGenre.updatedAt,
              keywords: newGenre.keywords,
              inLanguage: newGenre.locale,
              author: {
                '@type': 'Organization',
                name: newGenre.author || 'MelodyMind',
              },
              publisher: {
                '@type': 'Organization',
                name: 'MelodyMind',
                logo: {
                  '@type': 'ImageObject',
                  url: `${url.origin}/images/logo.png`,
                },
              },
              mainEntityOfPage: {
                '@type': 'WebPage',
                '@id': url.href,
              },
            })
          ),
        },
      ],
    })
  }
})

onMounted(loadContent)

watch(() => route.params, loadContent)
</script>

<style>
/* High contrast mode support */
@media (prefers-contrast: more) {
  article h1,
  article h2,
  article h3,
  article h4 {
    text-decoration: underline !important;
    text-underline-offset: 4px !important;
  }

  a,
  button {
    outline: 2px solid currentColor !important;
    outline-offset: 2px !important;
    text-decoration: underline !important;
    font-weight: 700 !important;
  }
}

/* Print styles */
@media print {
  article {
    color: #000 !important;
  }

  h1,
  h2,
  h3,
  h4 {
    color: #000 !important;
    font-size: 14pt !important;
    font-weight: bold !important;
    margin-bottom: 0.5rem !important;
  }

  p {
    color: #000 !important;
    font-size: 12pt !important;
  }

  img {
    max-width: 200px !important;
    margin: 1rem auto !important;
  }
}
</style>
