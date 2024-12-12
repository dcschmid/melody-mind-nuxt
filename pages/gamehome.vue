<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true">
        <main class="gameHome" id="main-content">
            <section class="intro" v-motion-slide-top>
                <h1>{{ $t('gameHome.title') }}</h1>
            </section>

            <section class="search-section" v-motion-slide-visible>
                <div class="search-wrapper">
                    <div class="search-input-container">
                        <Icon name="ic:baseline-search" size="24" class="search-icon" aria-hidden="true" />
                        <input
                            id="category-search"
                            v-model="searchQuery"
                            type="search"
                            class="filterInput"
                            :placeholder="$t('gameHome.searchPlaceholder')"
                            :aria-label="$t('gameHome.searchPlaceholder')"
                            @input="filterCategories"
                        />
                    </div>
                </div>
            </section>

            <section class="categories-section" aria-label="Spielkategorien">
                <div class="categories-grid">
                    <div
                        v-for="category in filteredCategories"
                        :key="category.slug"
                        class="category-card"
                        :class="{ 'not-playable': !category.isPlayable }"
                        :aria-disabled="!category.isPlayable"
                    >
                        <NuxtLink
                            v-if="category.isPlayable"
                            :to="localePath(category.categoryUrl)"
                            class="category-link"
                            :aria-label="$t('gameHome.playCategory', { category: category.headline })"
                        >
                            <div class="category-content">
                                <div class="image-container">
                                    <img :src="category.imageUrl" :alt="category.headline" loading="lazy" />
                                </div>
                                <div class="category-info">
                                    <h2>{{ category.headline }}</h2>
                                </div>
                            </div>
                        </NuxtLink>
                        <div
                            v-else
                            class="category-content coming-soon"
                            :aria-label="$t('gameHome.comingSoon', { category: category.headline })"
                        >
                            <div class="image-container">
                                <img :src="category.imageUrl" :alt="category.headline" loading="lazy" />
                                <div class="coming-soon-badge">
                                    {{ $t('gameHome.comingSoonLabel') }}
                                </div>
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
    max-width: var(--content-width);
    margin: 0 auto;
    padding: var(--padding-medium);
}

.intro {
    text-align: center;
    margin-bottom: var(--padding-large);

    h1 {
        font-size: var(--header-font-size);
        color: var(--text-color);
        margin-bottom: var(--padding-medium);
        font-weight: 700;
    }
}

.search-section {
    margin-bottom: var(--padding-large);
}

.search-wrapper {
    max-width: min(600px, 90%);
    margin: 0 auto;
}

.search-input-container {
    position: relative;
    display: flex;
    align-items: center;

    .search-icon {
        position: absolute;
        left: var(--padding-medium);
        color: var(--text-secondary);
    }
}

.filterInput {
    width: 100%;
    padding: var(--padding-medium) var(--padding-medium) var(--padding-medium) calc(var(--padding-medium) * 3);
    font-size: var(--body-font-size);
    color: var(--text-color);
    background: var(--surface-color);
    border: 2px solid var(--secondary-color);
    border-radius: var(--border-radius);
    transition: all 0.3s var(--transition-bounce);

    &:focus {
        outline: none;
        border-color: var(--highlight-color);
        box-shadow: 0 0 0 3px rgba(0, 229, 255, 0.2);
        transform: scale(1.01);
    }

    &::placeholder {
        color: var(--text-secondary);
    }
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
    gap: var(--padding-large);
    padding: var(--padding-small);

    @media (min-width: 640px) {
        grid-template-columns: repeat(2, 1fr);
    }

    @media (min-width: 1024px) {
        grid-template-columns: repeat(3, 1fr);
    }
}

.category-card {
    position: relative;
    border-radius: var(--border-radius);
    overflow: hidden;
    background: var(--surface-color);
    transition: all 0.3s var(--transition-bounce);
    border: 1px solid rgb(255 255 255 / 10%);

    &:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: var(--box-shadow-hover);

        .image-container img {
            transform: scale(1.1);
        }
    }

    &.not-playable {
        opacity: 0.9;
        filter: grayscale(20%);
        pointer-events: none;

        .coming-soon-badge {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75em;
            font-weight: 400;
            letter-spacing: 0.5px;
            backdrop-filter: blur(2px);
            z-index: 2;
            text-transform: uppercase;
        }
    }
}

.category-content {
    position: relative;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.image-container {
    position: relative;
    aspect-ratio: 16/9;
    overflow: hidden;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s var(--transition-bounce);
    }

    &::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(
            to bottom,
            transparent 0%,
            rgba(0, 0, 0, 0.8) 100%
        );
        z-index: 1;
    }
}

.category-info {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 15px;
    background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.4) 80%, transparent 100%);
    color: var(--text-color);
    z-index: 2;
    text-align: left;

    h2 {
        font-size: var(--body-font-size);
        font-weight: 600;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }

    .category-description {
        font-size: 0.9em;
        color: var(--text-secondary);
        margin: 0;
        opacity: 0;
        transform: translateY(10px);
        transition: all 0.3s var(--transition-bounce);
    }
}

.category-card:hover .category-description {
    opacity: 1;
    transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}

@media (max-width: 768px) {
    .gameHome {
        padding: var(--padding-small);
    }

    .categories-grid {
        gap: var(--padding-medium);
    }

    .category-info {
        h2 {
            font-size: 1.1em;
        }
    }
}
</style>
