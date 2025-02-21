<template>
    <div>
        <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
            <div class="categoryPage">
                <CategoryIntro :category="currentCategory || null" />

                <article class="category" :data-category="currentCategory?.slug" aria-labelledby="difficulty-heading"
                    v-if="currentCategory">
                    <CategoryCover :image-url="currentCategory.imageUrl" :headline="currentCategory.headline" />

                    <p class="category-text">{{ currentCategory.text }}</p>

                    <CategoryDifficultySelector v-if="hasUsername" :categorySlug="currentCategory.slug" />

                    <div class="category-links">
                        <h4 class="section-title">
                            <Icon name="material-symbols:library-music" aria-hidden="true" class="section-icon" />
                            {{ t('category.combined.title') }}
                        </h4>
                        <p class="section-description">
                            {{ t('category.combined.description', { genre: currentCategory.headline }) }}
                        </p>

                        <div class="links-container">
                            <div class="music-links-container" role="list" aria-labelledby="streaming-services-title"
                                v-if="currentCategory.spotifyPlaylist || currentCategory.deezerPlaylist || currentCategory.appleMusicPlaylist">
                                <a v-if="currentCategory.spotifyPlaylist" :href="currentCategory.spotifyPlaylist"
                                    target="_blank" rel="noopener noreferrer" class="music-link spotify"
                                    :aria-label="t('category.playlist.spotify')" role="listitem">
                                    <Icon name="mdi:spotify" class="icon" aria-hidden="true" />
                                </a>
                                <a v-if="currentCategory.deezerPlaylist" :href="currentCategory.deezerPlaylist" 
                                    target="_blank" rel="noopener noreferrer" class="music-link deezer"
                                    :aria-label="t('category.playlist.deezer')" role="listitem">
                                    <Icon name="simple-icons:deezer" class="icon" aria-hidden="true" />
                                </a>
                                <a v-if="currentCategory.appleMusicPlaylist" :href="currentCategory.appleMusicPlaylist"
                                    target="_blank" rel="noopener noreferrer" class="music-link apple"
                                    :aria-label="t('category.playlist.apple')" role="listitem">
                                    <Icon name="simple-icons:applemusic" class="icon" aria-hidden="true" />
                                </a>
                            </div>

                            <div v-if="currentCategory.knowledgeUrl" class="knowledge-section">
                                <NuxtLink 
                                    :to="localePath(`${currentCategory.knowledgeUrl}`)" 
                                    class="knowledge-link"
                                    :aria-label="t('category.knowledge.link', { genre: currentCategory.headline })"
                                >
                                    <Icon name="material-symbols:menu-book" aria-hidden="true" class="knowledge-icon" />
                                    {{ t('category.knowledge.title') }}
                                </NuxtLink>
                            </div>
                        </div>
                    </div>

                </article>
            </div>
        </NuxtLayout>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useHead, useLocalePath, useSeoMeta } from '#imports'

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
    return categories.value.find(cat => cat.slug === route.params.category)
})

useHead({
    title: computed(() => currentCategory.value ? `${currentCategory.value.headline} - Melody Mind` : 'Melody Mind'),
    meta: [
        {
            name: 'description',
            content: computed(() => currentCategory.value ? currentCategory.value.text : '')
        }
    ]
})

watch(() => currentCategory.value, (category) => {
  if (category) {
    useSeoMeta({
      title: computed(() => `${category.headline} - Melody Mind`),
      description: computed(() => category.introSubline),
      ogTitle: computed(() => `${category.headline} - Melody Mind`),
      ogDescription: computed(() => category.introSubline),
      ogType: 'website',
      ogImage: computed(() => category.imageUrl),
      twitterCard: 'summary_large_image',
      twitterImage: computed(() => category.imageUrl)
    })
  }
}, { immediate: true })

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

const onUsernameSet = () => {
    hasUsername.value = true
}

onMounted(() => {
    const storedUsername = localStorage.getItem('username')
    if (storedUsername) {
        hasUsername.value = true
    }
    loadCategories()
})
</script>

<style scoped lang="scss">
.categoryPage {
    color: var(--text-color);
}

.category {
    display: grid;
    gap: var(--padding-large);
    place-items: center;
    transition: all var(--transition-speed) var(--transition-bounce);
    margin: 0 auto;
}

.category-text {
    font-size: var(--font-size-responsive-md);
    line-height: var(--line-height-relaxed);
    margin: 0 auto;
    text-align: center;
    color: var(--text-secondary);
    max-width: var(--max-line-length);
}

.category-links {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: var(--content-width);
    margin: var(--padding-medium) auto;
    text-align: center;
}

.links-container {
    display: flex;
    flex-direction: column;
    gap: var(--padding-large);
    width: 100%;
    margin-top: var(--padding-medium);
}

.section-title {
    font-size: var(--font-size-responsive-xl);
    color: var(--primary-color);
    display: flex;
    align-items: center;
    gap: var(--padding-small);
    justify-content: center;
    margin-bottom: var(--padding-medium);
}

.section-description {
    color: var(--text-secondary);
    max-width: var(--max-line-length);
    margin: 0 auto var(--padding-large);
    line-height: var(--line-height-relaxed);
}

.knowledge-section,
.music-links {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    border-radius: var(--border-radius);
}

.music-links {
    margin: 0;
    background: transparent;
    box-shadow: none;
    border: none;
    padding: 0;
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
    border-radius: 16px;
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

    .icon {
        position: relative;
        z-index: 1;
        color: var(--text-color-dark);
        width: 32px;
        height: 32px;
        filter: drop-shadow(0 2px 4px rgb(0 0 0 / 20%));
        transition: all var(--transition-speed) var (--transition-bounce);
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

.knowledge-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--padding-medium);
    text-align: center;
    margin: var(--padding-medium) 0;
}

.knowledge-intro {
    font-size: var(--font-size-responsive-md);
    color: var(--text-secondary);
    max-width: var(--max-line-length);
    line-height: var(--line-height-normal);
}

.knowledge-link {
    display: flex;
    align-items: center;
    gap: var(--padding-small);
    background-color: var(--primary-color);
    color: var(--text-color-dark);
    padding: var(--padding-medium);
    border-radius: var(--border-radius);
    text-decoration: none;
    min-height: var(--min-touch-target);
    font-weight: var(--font-weight-semibold);
    transition: all var(--transition-speed) var(--transition-bounce);

    &:hover {
        background-color: var(--primary-color-dark);
        transform: translateY(-2px);
        box-shadow: var(--box-shadow-hover);
    }

    &:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }

    .knowledge-icon {
        font-size: var(--font-size-responsive-xl);
    }
}

@media (prefers-reduced-motion: reduce) {
    .category,
    .music-link,
    .knowledge-link {
        transition: none;
        transform: none;
    }
}

@media (width <= 767px) {
    .category-text {
        font-size: var(--font-size-responsive-sm);
    }

    .music-links-title {
        font-size: var(--font-size-responsive-lg);
    }

    .knowledge-link {
        justify-content: center;
    }
}
</style>
