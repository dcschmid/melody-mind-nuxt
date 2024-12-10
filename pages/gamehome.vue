<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <main class="gameHome" id="main-content">
            <section class="intro" v-motion-slide-top>
                <h1>{{ $t('gameHome.title') }}</h1>
            </section>

            <section class="search-section" v-motion-slide-visible>
                <div class="search-wrapper">
                    <label for="category-search" class="sr-only">{{ $t('gameHome.searchPlaceholder') }}</label>
                    <input id="category-search" v-model="searchQuery" type="search" class="filterInput"
                        :placeholder="$t('gameHome.searchPlaceholder')" :aria-label="$t('gameHome.searchPlaceholder')"
                        @input="filterCategories" />
                </div>
            </section>

            <section class="categories-section" aria-label="Spielkategorien">
                <div class="categories-grid">
                    <div v-for="category in filteredCategories" :key="category.slug" class="category-card"
                        :class="{ 'not-playable': !category.isPlayable }" :aria-disabled="!category.isPlayable">
                        <NuxtLink v-if="category.isPlayable" :to="localePath(category.categoryUrl)"
                            class="category-link"
                            :aria-label="$t('gameHome.playCategory', { category: category.headline })">
                            <div class="category-content">
                                <div class="image-container">
                                    <img :src="category.imageUrl" :alt="category.headline" loading="lazy" />
                                </div>
                                <div class="category-info">
                                    <h2>{{ category.headline }}</h2>
                                </div>
                            </div>
                        </NuxtLink>
                        <div v-else class="category-content coming-soon"
                            :aria-label="$t('gameHome.comingSoon', { category: category.headline })">
                            <div class="image-container">
                                <img :src="category.imageUrl" :alt="category.headline" loading="lazy" />
                            </div>
                            <div class="category-info">
                                <h2>{{ category.headline }}</h2>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </NuxtLayout>
</template>

<script setup>
definePageMeta({
    middleware: 'auth'
})

const isSSR = ref(true)

onMounted(() => {
    isSSR.value = false
})

const searchQuery = ref('')
const categories = ref([])
const localePath = useLocalePath()

const { locale } = useI18n()
const loadCategories = async () => {
    const cacheKey = `categories_${locale.value}`
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

const filteredCategories = computed(() => {
    if (!searchQuery.value) return categories.value
    const query = searchQuery.value.toLowerCase()
    return categories.value.filter(category =>
        category.headline.toLowerCase().includes(query) ||
        category.introSubline.toLowerCase().includes(query)
    )
})

onMounted(() => {
    loadCategories()
})
</script>

<style scoped lang="scss">
.gameHome {
    width: 100%;
    max-width: var(--max-line-length);
    margin: 0 auto;
    padding: var(--padding-medium);

    @media (min-width: 768px) {
        padding: var(--padding-large);
    }
}

.intro {
    text-align: center;
    margin-bottom: 2rem;

    h1 {
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        color: var(--text-color);
        margin-bottom: 1rem;
    }
}

.search-wrapper {
    max-width: 600px;
    margin: 0 auto 3rem;
    padding: 0 1rem;
}

.filterInput {
    width: 100%;
    padding: 1rem;
    font-size: var(--body-font-size);
    color: var(--text-color);
    background: var(--background-color);
    border: 2px solid var(--secondary-color);
    border-radius: var(--border-radius);
    transition: all 0.3s ease;

    &:focus {
        outline: none;
        border-color: var(--highlight-color);
        box-shadow: 0 0 0 3px rgba(var(--highlight-color), 0.2);
    }
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
    gap: 2rem;
    padding: 1rem;

    @media (min-width: 640px) {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    }

    @media (min-width: 1024px) {
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    }
}

.category-card {
    position: relative;
    border-radius: var(--border-radius);
    overflow: hidden;
    background: var(--secondary-color);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

    &:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    &.not-playable {
        opacity: 0.7;
        filter: grayscale(30%);
        pointer-events: none;
    }
}

.category-link {
    text-decoration: none;
    color: inherit;
}

.category-content {
    position: relative;
    height: 100%;
}

.image-container {
    position: relative;
    aspect-ratio: 1;
    overflow: hidden;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }

    &::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(to bottom,
                transparent 0%,
                rgba(0, 0, 0, 0.7) 100%);
    }
}

.category-info {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1.5rem;
    color: white;
    z-index: 1;

    h2 {
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
}

@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}

// Dark mode adjustments
@media (prefers-color-scheme: dark) {
    .category-card {
        background: var(--secondary-color);
    }
}

// Print styles
@media print {
    .category-card {
        break-inside: avoid;
        page-break-inside: avoid;
    }
}

.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
</style>
