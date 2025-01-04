<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <div class="categoryPage">
            <CategoryIntro :category="currentCategory || null" />

            <article class="category" :data-category="currentCategory?.slug" aria-labelledby="difficulty-heading"
                v-if="currentCategory">
                <CategoryCover :image-url="currentCategory.imageUrl" :headline="currentCategory.headline" />

                <p class="text">{{ currentCategory.text }}</p>

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

                <UsernameInput ref="usernameInput" v-if="!hasUsername" @username-set="onUsernameSet" />
                <CategoryDifficultySelector v-if="hasUsername" :categorySlug="currentCategory.slug" />
            </article>
        </div>
    </NuxtLayout>
</template>

<script setup lang="ts">
const route = useRoute()
const { locale, t } = useI18n()
const url = useRequestURL()

const currentCategory = computed(() => {
    return categories.value.find(cat => cat.slug === route.params.category)
})

useSeoMeta({
    title: computed(() => currentCategory.value?.headline || t('seo.category.defaultTitle')),
    ogTitle: computed(() => currentCategory.value?.headline || t('seo.category.defaultTitle')),
    description: computed(() => currentCategory.value?.introSubline || t('seo.category.defaultDescription')),
    ogDescription: computed(() => currentCategory.value?.introSubline || t('seo.category.defaultDescription')),
    ogUrl: url.href,
    ogType: 'website',
    robots: 'index, follow',
    viewport: 'width=device-width, initial-scale=1'
})

interface Category {
    slug: string
    headline: string
    introSubline: string
    imageUrl: string
    text: string
    spotifyPlaylist: string
    deezerPlaylist: string
    appleMusicPlaylist: string
}

const categories = ref<Category[]>([])
const usernameInput = ref(null)
const hasUsername = ref(false)

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
    gap: clamp(var(--padding-medium), 3vw, var(--padding-large));
    place-items: center;
    transition: all var(--transition-speed);
}

.text {
    font-size: clamp(1.125rem, 2vw, var(--body-font-size));
    line-height: var(--line-height-body);
    margin: 0 auto;
    text-align: center;
    color: var(--text-secondary);
}

.music-links {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: var(--padding-small) 0;
}

.music-links-title {
    display: flex;
    align-items: center;
    gap: var(--padding-small);
    font-size: var(--heading-font-size);
    font-weight: var(--font-weight-bold);
    margin-bottom: var(--padding-medium);
    color: var(--text-primary);
}

.headphone-icon {
    font-size: 28px;
    color: var(--primary-color);
}

.music-links-description {
    text-align: center;
    color: var(--text-secondary);
    margin-bottom: var(--padding-medium);
    max-width: 600px;
    line-height: 1.5;
    font-size: var(--text-sm);
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
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background-color: var(--background-color);
    transition: all var(--transition-speed) ease-in-out;
    border: 2px solid transparent;
}

.music-link:hover {
    transform: translateY(-2px);
    box-shadow: var(--box-shadow);
}

.music-link.spotify {
    color: #1db954;
    border-color: #1db954;
}

.music-link.spotify:hover {
    background-color: #1db954;
    color: white;
}

.music-link.deezer {
    color: #00b6f0;
    border-color: #00b6f0;
}

.music-link.deezer:hover {
    background-color: #00b6f0;
    color: white;
}

.music-link.apple {
    color: var(--text-primary);
    border-color: var(--text-primary);
    background: linear-gradient(145deg, var(--background-color) 0%, var(--background-color) 100%);
    transition: all var(--transition-speed) ease-in-out;
}

.music-link.apple:hover {
    background: linear-gradient(145deg, #fc3c44 0%, #ff2d55 100%);
    border-color: transparent;
    color: white;
    transform: translateY(-2px);
    box-shadow: var(--box-shadow);
}

.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}

@media (width <=767px) {
    .text {
        font-size: clamp(1.125rem, 4vw, 1.25rem);
    }
}
</style>
