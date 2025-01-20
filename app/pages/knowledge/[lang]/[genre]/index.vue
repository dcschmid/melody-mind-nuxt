<template>
  <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
    <div v-if="genre" class="knowledge-base">
        <div class="knowledge-content">
          <!-- Main Content -->
           <div class="knowledge-header">
            <h1>{{ genre.title }}</h1>
            <img :src="genre.image" :alt="genre.title" class="genre-image" />
          </div>

          <article class="main-content prose prose-invert">
            <ContentRenderer :value="genre" />
          </article>

          <!-- Music Links -->
          <div class="music-links" v-if="category?.spotifyPlaylist || category?.deezerPlaylist || category?.appleMusicPlaylist" role="region" :aria-label="$t('knowledge.playlists')">
            <div class="music-links-inner">
              <h4 class="music-links-title" id="streaming-services-title">
                <Icon name="material-symbols:headphones" aria-hidden="true" class="headphone-icon" />
                {{ $t('knowledge.playAndListen') }}
              </h4>
              <p class="music-links-description">
                {{ $t('knowledge.playlist.description', { genre: genre.title }) }}
              </p>

              <!-- Play Button -->
              <NuxtLink :to="gameUrl" class="play-button">
                <Icon name="material-symbols:play-arrow" aria-hidden="true" class="play-icon" />
                {{ $t('knowledge.playNow') }}
              </NuxtLink>

              <!-- Playlist Links -->
              <div class="music-links-container" role="list" aria-labelledby="streaming-services-title">
                <a v-if="category?.spotifyPlaylist" :href="category.spotifyPlaylist" 
                  target="_blank" rel="noopener noreferrer" 
                  class="music-link spotify" :aria-label="$t('knowledge.playlist.spotify')" 
                  role="listitem">
                  <Icon name="mdi:spotify" size="28" aria-hidden="true" />
                </a>
                <a v-if="category?.deezerPlaylist" :href="category.deezerPlaylist" 
                  target="_blank" rel="noopener noreferrer" 
                  class="music-link deezer" :aria-label="$t('knowledge.playlist.deezer')" 
                  role="listitem">
                  <Icon name="simple-icons:deezer" size="28" aria-hidden="true" />
                </a>
                <a v-if="category?.appleMusicPlaylist" :href="category.appleMusicPlaylist" 
                  target="_blank" rel="noopener noreferrer" 
                  class="music-link apple" :aria-label="$t('knowledge.playlist.apple')" 
                  role="listitem">
                  <Icon name="simple-icons:applemusic" size="28" aria-hidden="true" />
                </a>
              </div>
            </div>
          </div>
        </div>
    </div>
    <div v-else-if="error" class="container py-8">
      <p>{{ error }}</p>
    </div>
    <div v-else class="container py-8">
      <p>{{ $t('knowledge.loading') }}</p>
    </div>
  </NuxtLayout>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { queryContent, useRequestURL, useSeoMeta, useHead } from '#imports'

const route = useRoute()
const url = useRequestURL()

const genre = ref(null)
const category = ref(null)
const gameUrl = ref('')
const error = ref(null)

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
      newGenre.image?.startsWith('http') 
        ? newGenre.image 
        : `${url.origin}${newGenre.image}`
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
      'og:site_name': 'MelodyMind'
    })

    // Add structured data
    useHead({
      script: [
        {
          type: 'application/ld+json',
          children: computed(() => JSON.stringify({
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
              name: newGenre.author || 'MelodyMind'
            },
            publisher: {
              '@type': 'Organization',
              name: 'MelodyMind',
              logo: {
                '@type': 'ImageObject',
                url: `${url.origin}/images/logo.png`
              }
            },
            mainEntityOfPage: {
              '@type': 'WebPage',
              '@id': url.href
            }
          }))
        }
      ]
    })
  }
})

onMounted(loadContent)

watch(() => route.params, loadContent)
</script>

<style lang="scss">
.knowledge-base {
  min-height: 100vh;
  color: var(--text-color);

  .knowledge-header {
      text-align: center;

    img.genre-image {
      width: 100%;
      max-width: clamp(280px, 35vw, 400px);
      aspect-ratio: 1;
      object-fit: cover;
      border-radius: var(--border-radius);
      box-shadow: var(--box-shadow);
    }

    h1 {
      font-size: 3rem;
      color: var(--primary-color);
      font-weight: bold;
    }
  }

  .container {
    margin: 0 auto;
  }

  .knowledge-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--padding-large);
  }

  .main-content {
    width: 100%;
    color: var(--text-secondary);


    h2 {
      font-size: 2rem;
      color: var(--primary-color);
      margin: var(--padding-large) 0 var(--padding-medium);
    }

    h3 {
      font-size: 1.5rem;
      color: var(--primary-color);
      margin: var(--padding-medium) 0 var(--padding-small);
    }

    li {
      margin-bottom: var(--padding-small);
    }

    p {
      line-height: 1.8;
      margin-bottom: var(--padding-medium);
    }
  }

  .music-links {
    width: 100%;
    margin-bottom: var(--padding-large);
  }

  .music-links-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .music-links-title {
    display: flex;
    align-items: center;
    gap: var(--padding-small);
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: var(--padding-medium);
    color: var(--text-primary);
  }

  .headphone-icon {
    font-size: 1.8rem;
    color: var(--primary-color);
  }

  .music-links-description {
    color: var(--text-secondary);
    margin-bottom: var(--padding-large);
  }

  .play-button {
    display: inline-flex;
    align-items: center;
    gap: var(--padding-small);
    background-color: var(--primary-color);
    color: white;
    padding: 1rem 2rem;
    border-radius: var(--border-radius);
    font-size: 1.2rem;
    font-weight: bold;
    transition: all 0.3s ease;
    text-decoration: none;

    &:hover {
      transform: translateY(-2px);
      background-color: var(--primary-color-dark);
      box-shadow: var(--box-shadow);
    }

    .play-icon {
      font-size: 1.5rem;
    }
  }

  .music-links-container {
    display: flex;
    justify-content: center;
    gap: var(--padding-large);
    margin-top: var(--padding-medium);
  }

  .music-link {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: var(--background-color);
    transition: all 0.3s ease;
    border: 2px solid transparent;

    &:hover {
      transform: translateY(-2px);
      box-shadow: var(--box-shadow);
    }

    &.spotify {
      color: #1db954;
      border-color: #1db954;

      &:hover {
        background-color: #1db954;
        color: white;
      }
    }

    &.deezer {
      color: #00b6f0;
      border-color: #00b6f0;

      &:hover {
        background-color: #00b6f0;
        color: white;
      }
    }

    &.apple {
      color: var(--text-primary);
      border-color: var(--text-primary);

      &:hover {
        background: linear-gradient(145deg, #fc3c44 0%, #ff2d55 100%);
        border-color: transparent;
        color: white;
      }
    }
  }
}

@media (max-width: 768px) {
  .knowledge-base {
    .knowledge-header {
      padding: var(--padding-medium);
      
      h1 {
        font-size: 2.5rem;
      }
    }

    .main-content,
    .music-links {
      padding: var(--padding-medium);
    }

    .music-links-container {
      gap: var(--padding-medium);
    }

    .music-link {
      width: 50px;
      height: 50px;
    }
  }
}
</style>