<template>
  <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
    <div v-if="genre" class="knowledge-base">
        <div class="knowledge-content">
          <!-- Main Content -->
           <div class="knowledge-header">
            <h1>{{ genre.title }}</h1>
            <UnLazyImage 
              :src="genre.image" 
              :alt="genre.title" 
              class="genre-image"
              :thumbhash="thumbHash"
              auto-sizes
              loading="lazy"
            />

            <div class="">
              {{genre.description}}
            </div>
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

              <!-- Play Button -->
              <NuxtLink v-if="genre.isPlayable" :to="gameUrl" class="play-button">
                <Icon name="i-mdi:play-outline" size="48" :aria-hidden="true" />
                {{ $t('knowledge.playNow') }}
              </NuxtLink>
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
import { useThumbHash } from '~/composables/useThumbHash'

const route = useRoute()
const url = useRequestURL()

const genre = ref(null)
const category = ref(null)
const gameUrl = ref('')
const error = ref(null)

const { getThumbHash } = useThumbHash()

// ThumbHash für das Genre-Bild abrufen
const thumbHash = computed(() => genre.value?.image ? getThumbHash(genre.value.image) : undefined)

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
        padding: var(--padding-medium);
        font-size: var(--font-size-responsive-md);

        .genre-image {
            width: 100%;
            max-width: 300px;
            aspect-ratio: 1;
            object-fit: cover;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            transition: transform var(--transition-speed) var(--transition-bounce);

            &:hover {
                transform: scale(1.02);
                box-shadow: var(--box-shadow-hover);
            }
        }

        h1 {
            font-size: var(--font-size-responsive-3xl);
            color: var(--primary-color);
            font-weight: var(--font-weight-bold);
            line-height: var(--line-height-tight);
            margin-bottom: var(--padding-medium);
        }
    }

    .knowledge-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--padding-large);
        max-width: var(--content-width);
        margin: 0 auto;
        padding: var(--padding-medium);
    }

    .main-content {
        width: 100%;
        color: var(--text-secondary);

        h2 {
            font-size: var(--font-size-responsive-2xl);
            color: var(--primary-color);
            font-weight: var(--font-weight-semibold);
            margin: var(--padding-large) 0 var(--padding-medium);
            line-height: var(--line-height-tight);
        }

        h3 {
            font-size: var(--font-size-responsive-xl);
            color: var (--primary-color);
            font-weight: var(--font-weight-semibold);
            margin: var(--padding-medium) 0 var(--padding-small);
            line-height: var(--line-height-tight);
        }

        p {
            font-size: var(--font-size-responsive-md);
            line-height: var(--line-height-relaxed);
            margin-bottom: var(--padding-medium);
            hyphens: auto;
        }
    }

    .music-links {
        width: 100%;
        margin-bottom: var(--padding-large);

        .music-links-title {
            display: flex;
            align-items: center;
            gap: var(--padding-small);
            font-size: var(--font-size-responsive-2xl);
            font-weight: var(--font-weight-bold);
            color: var(--primary-color);
            margin-bottom: var(--padding-medium);
            line-height: var(--line-height-tight);
        }

        .music-links-description {
            font-size: var(--font-size-responsive-md);
            color: var(--text-secondary);
            margin-bottom: var(--padding-large);
            line-height: var(--line-height-normal);
        }

        .music-links-container {
            display: flex;
            justify-content: center;
            gap: var(--padding-large);
            margin-top: var(--padding-medium);
            perspective: 1000px;
        }

        .music-link {
            display: flex;
            justify-content: center;
            align-items: center;
            width: var(--min-touch-target);
            height: var(--min-touch-target);
            border-radius: var(--border-radius);
            transition: all var(--transition-speed) var(--transition-bounce);
            position: relative;
            backdrop-filter: var(--overlay-blur);
            border: 1px solid rgb(255 255 255 / 10%);
            overflow: hidden;
            
            &::before {
                content: '';
                position: absolute;
                inset: 0;
                opacity: 0.85;
                transition: all var(--transition-speed) ease;
            }
        
            &.spotify::before {
                background: linear-gradient(135deg, #1DB954 0%, #1ed760 50%, #25f971 100%);
                box-shadow: var(--box-shadow);
            }
        
            &.deezer::before {
                background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-color-light) 50%, var(--highlight-color) 100%);
                box-shadow: var(--box-shadow);
            }
        
            &.apple::before {
                background: linear-gradient(135deg, var(--error-color) 0%, var(--error-color-dark) 50%, #ff6b7f 100%);
                box-shadow: var(--box-shadow);
            }
        
            .iconify {
                position: relative;
                z-index: 1;
                color: var(--text-color-dark);
                width: 32px;
                height: 32px;
                filter: drop-shadow(0 2px 4px rgb(0 0 0 / 20%));
                transition: all var(--transition-speed) var(--transition-bounce);
            }
        
            &:hover {
                transform: translateY(-4px);
                box-shadow: var(--box-shadow-hover);
                
                &::before {
                    opacity: 1;
                }
        
                .icon {
                    transform: scale(1.1);
                    filter: drop-shadow(0 4px 8px rgb(0 0 0 / 30%));
                }
            }
        
            &:active {
                transform: translateY(-2px);
            }
        
            &:focus-visible {
                outline: var(--focus-outline-width) solid var(--focus-outline-color);
                outline-offset: var(--focus-outline-offset);
            }
        }
    }

    .play-button {
        @include button-primary;
        display: flex;
        align-items: center;
        gap: var(--padding-small);
        min-height: var(--min-touch-target);
        padding: var(--padding-small);
        font-size: var(--font-size-responsive-sm);
        font-weight: var(--font-weight-bold);
        margin-top: var(--padding-medium);
        text-decoration: none;
        color: var(--text-color-dark);
        margin:  var(--padding-medium) auto;
        width: auto;
    }
}

@media (prefers-reduced-motion: reduce) {
    .knowledge-base {
        .genre-image,
        .music-link,
        .play-button {
            transition: none;
            transform: none;
        }
    }

    .music-link {
        transition: none;

        &:hover {
            transform: none;

            .icon {
                transform: none;
            }

            &::before {
                transform: none;
            }
        }
    }
}

@media (width <= 768px) {
    .knowledge-base {
        .knowledge-header {
            padding: var(--padding-medium);
            
            h1 {
                font-size: var(--font-size-responsive-2xl);
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
            width: var(--min-touch-target);
            height: var(--min-touch-target);

            .icon {
                width: 28px;
                height: 28px;
            }
        }
    }
}
</style>