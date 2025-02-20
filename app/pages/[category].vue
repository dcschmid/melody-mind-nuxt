<template>
    <div>
        <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
            <div class="categoryPage">
                <CategoryIntro :category="currentCategory || null" />

                <article class="category" :data-category="currentCategory?.slug" aria-labelledby="difficulty-heading"
                    v-if="currentCategory">
                    <CategoryCover :image-url="currentCategory.imageUrl" :headline="currentCategory.headline" />

                    <p class="category-text">{{ currentCategory.text }}</p>

                    <div v-if="currentCategory.knowledgeUrl" class="knowledge-section">
                        <p class="knowledge-intro">{{ t('category.knowledge.description', { genre: currentCategory.headline }) }}</p>
                        <NuxtLink 
                            :to="localePath(`${currentCategory.knowledgeUrl}`)" 
                            class="knowledge-link"
                            :aria-label="t('category.knowledge.link', { genre: currentCategory.headline })"
                        >
                            <Icon name="material-symbols:menu-book" aria-hidden="true" class="knowledge-icon" />
                            {{ t('category.knowledge.title') }}
                        </NuxtLink>
                    </div>

                    <div class="music-links"
                        v-if="currentCategory.spotifyPlaylist || currentCategory.deezerPlaylist || currentCategory.appleMusicPlaylist"
                        role="region" :aria-label="t('category.playlist.title')">
                        <h4 class="music-links-title" id="streaming-services-title">
                            <Icon name="material-symbols:headphones" aria-hidden="true" class="headphone-icon" />
                            {{ t('category.playlist.title') }}
                        </h4>
                        <p class="music-links-description">
                            {{ t('category.playlist.description', { genre: currentCategory.headline }) }}
                        </p>
                        <div class="music-links-container" role="list" aria-labelledby="streaming-services-title">
                            <a v-if="currentCategory.spotifyPlaylist" :href="currentCategory.spotifyPlaylist"
                                target="_blank" rel="noopener noreferrer" class="music-link spotify"
                                :aria-label="t('category.playlist.spotify')" role="listitem">
                                <Icon name="mdi:spotify" size="28" aria-hidden="true" />
                                <span class="visually-hidden">{{ t('category.playlist.spotify') }}</span>
                            </a>
                            <a v-if="currentCategory.deezerPlaylist" :href="currentCategory.deezerPlaylist" target="_blank"
                                rel="noopener noreferrer" class="music-link deezer"
                                :aria-label="t('category.playlist.deezer')" role="listitem">
                                <Icon name="simple-icons:deezer" size="28" aria-hidden="true" />
                                <span class="visually-hidden">{{ t('category.playlist.deezer') }}</span>
                            </a>
                            <a v-if="currentCategory.appleMusicPlaylist" :href="currentCategory.appleMusicPlaylist"
                                target="_blank" rel="noopener noreferrer" class="music-link apple"
                                :aria-label="t('category.playlist.apple')" role="listitem">
                                <Icon name="mdi:apple" size="28" aria-hidden="true" />
                                <span class="visually-hidden">{{ t('category.playlist.apple') }}</span>
                            </a>
                        </div>
                    </div>

                    <CategoryDifficultySelector v-if="hasUsername" :categorySlug="currentCategory.slug" />
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

.music-links {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: var(--padding-medium) 0;
    width: 100%;
}

.music-links-title {
    display: flex;
    align-items: center;
    gap: var(--padding-small);
    font-size: var(--font-size-responsive-xl);
    font-weight: var(--font-weight-semibold);
    margin-bottom: var(--padding-medium);
    color: var(--text-color);
    line-height: var(--line-height-tight);
}

.headphone-icon {
    font-size: var(--font-size-responsive-xl);
    color: var(--primary-color);
}

.music-links-description {
    text-align: center;
    color: var(--text-secondary);
    margin-bottom: var(--padding-medium);
    max-width: var(--max-line-length);
    line-height: var(--line-height-normal);
    font-size: var(--font-size-base);
}

.music-links-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: var(--padding-medium);
}

.music-link {
    display: flex;
    justify-content: center;
    align-items: center;
    width: var(--min-touch-target);
    height: var(--min-touch-target);
    border-radius: var(--border-radius-full);
    background-color: var(--background-color);
    transition: all var(--transition-speed) var(--transition-bounce);
    border: var(--border-width) solid transparent;

    &:hover {
        transform: translateY(-2px);
        box-shadow: var(--box-shadow-hover);
    }

    &:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }

    &.spotify {
        color: var(--success-color);
        border-color: var(--success-color);

        &:hover {
            background-color: var(--success-color);
            color: var(--button-text-color);
        }
    }

    &.deezer {
        color: var(--highlight-color);
        border-color: var(--highlight-color);

        &:hover {
            background-color: var(--highlight-color);
            color: var(--button-text-color);
        }
    }

    &.apple {
        color: var(--text-color);
        border-color: var(--text-color);
        background: var(--surface-color);
        
        &:hover {
            background: var(--primary-color);
            border-color: var(--primary-color);
            color: var(--button-text-color);
        }
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
    color: var(--button-text-color);
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
        padding: 0 var(--padding-small);
    }

    .music-links-title {
        font-size: var(--font-size-responsive-lg);
    }

    .knowledge-link {
        width: 100%;
        justify-content: center;
    }
}
</style>
