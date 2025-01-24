<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true">
        <div class="gameHome" id="main-content">
            <section class="intro">
                <h1 tabindex="-1" class="page-title">{{ $t('gameHome.title') }}</h1>
                <p class="intro-text page-subtitle" v-if="$t('gameHome.description')">{{ $t('gameHome.description') }}</p>
            </section>

            <section class="search-section" role="search">
                <SearchBar id="category-search" v-model="searchQuery" :placeholder="$t('gameHome.searchPlaceholder')" />
            </section>

            <section class="categories-section" role="region" aria-labelledby="categories-heading">
                <h2 id="categories-heading" class="visually-hidden">{{ $t('gameHome.categoriesTitle') }}</h2>
                <div class="categories-grid" role="list">
                    <CategoryCard v-for="category in filteredCategories" :key="category.slug"
                        :headline="category.headline" :image-url="category.imageUrl"
                        :category-url="localePath(category.categoryUrl)" :is-playable="category.isPlayable"
                        :intro-subline="category.introSubline" role="listitem" @select="navigateToCategory(category)" />
                </div>
            </section>
        </div>
    </NuxtLayout>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRequestURL } from '#imports'

const router = useRouter()

const { searchQuery, filteredCategories, loadCategories } = useCategories()
const { locale, t } = useI18n()
const localePath = useLocalePath()
const url = useRequestURL()

useSeoMeta({
    title: computed(() => t('gameHome.title')),
    ogTitle: computed(() => t('gameHome.title')),
    description: computed(() => t('gameHome.description')),
    ogDescription: computed(() => t('gameHome.description')),
    ogType: 'website',
    robots: 'index, follow',
    viewport: 'width=device-width, initial-scale=1',
    twitterCard: 'summary_large_image',
    ogUrl: computed(() => url.href)
})

const navigateToCategory = (category) => {
    if (category.isPlayable) {
        router.push(localePath(category.categoryUrl))
    }
}

onMounted(() => {
    loadCategories(locale.value)
})
</script>

<style scoped lang="scss">
.gameHome {
    width: 100%;
    margin: 0 auto;
}

.intro {
    text-align: center;
    margin-bottom: var(--padding-large);
}

.page-title {
    font-size: var(--font-size-responsive-2xl);
    font-weight: 700;
    text-align: center;
    margin-bottom: var(--padding-large);
}

.page-subtitle {
    font-size: var(--font-size-responsive-lg);
    color: var(--text-secondary);
    text-align: center;
    margin-bottom: var(--padding-medium);
}

.search-section {
    margin-bottom: var(--padding-large);
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;

    @media (prefers-reduced-motion: reduce) {
        * {
            transition: none !important;
        }
    }
}

@media (prefers-reduced-motion: no-preference) {
    .category-card {
        animation: fadeIn 0.5s ease-out;
    }
}

@media (min-width: 640px) {
    .categories-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1024px) {
    .categories-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (max-width: 768px) {

    .categories-grid {
        gap: var(--padding-medium);
    }
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
    border: 0;
}
</style>
